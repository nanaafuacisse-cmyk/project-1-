"""

"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json

report = []
def log(msg=""):
    print(msg)
    report.append(str(msg))

substations = pd.read_csv(r"C:\Users\EXPRESS COMPUTERS\Downloads\substations_clean.csv")
lines = pd.read_csv(r"C:\Users\EXPRESS COMPUTERS\Downloads\lines_clean.csv")

# ===========================================================================
# Build the graph
# ===========================================================================
log("=" * 70)
log("BUILDING THE NETWORK GRAPH")
log("=" * 70)
log("Graph type: UNDIRECTED -- AC power can flow either direction along a")
log("line depending on system conditions, unlike a scheduled flight with a")
log("fixed origin/destination.")

G = nx.Graph()

# Add nodes (substations) with attributes
for _, sub in substations.iterrows():
    G.add_node(
        sub["Substation ID"],
        name=sub["Name"],
        short_name=sub["Short Name"],
        region=sub["Region"],
        country=sub["Country"],
        voltage=sub["Voltage (kV)"],
        capacity=sub["Capacity (MVA)"],
        commissioning_year=sub["Commissioning Year"],
        type=sub["Type"],
        status=sub["Status"],
        lat=sub["Latitude"],
        lon=sub["Longitude"],
    )

# Add edges (lines) with attributes -- guard against any dangling FK just in case
valid_ids = set(substations["Substation ID"])
skipped = 0
for _, line in lines.iterrows():
    src, dst = line["Source Substation ID"], line["Destination Substation ID"]
    if src not in valid_ids or dst not in valid_ids:
        skipped += 1
        continue
    G.add_edge(
        src, dst,
        line_id=line["Line ID"],
        utility_id=line["Utility ID"],
        voltage=line["Voltage (kV)"],
        length_km=line["Length (km)"],
        capacity=line["Capacity (MVA)"],
        status=line["Status"],
        line_type=line["Line Type"],
    )

log(f"\nNodes (substations): {G.number_of_nodes()}")
log(f"Edges (lines): {G.number_of_edges()}")
log(f"Lines skipped (dangling FK, should be 0 given prior cleaning): {skipped}")

# ===========================================================================
# Connectivity / components
# ===========================================================================
log("\n" + "=" * 70)
log("CONNECTIVITY AND COMPONENTS")
log("=" * 70)

n_components = nx.number_connected_components(G)
log(f"Connected components: {n_components}")
if n_components > 1:
    comp_sizes = sorted([len(c) for c in nx.connected_components(G)], reverse=True)
    log(f"Component sizes: {comp_sizes}")
    log("Network is NOT fully connected -- some substations are isolated or in separate clusters.")
else:
    log("Network is fully connected -- every substation can reach every other via some path.")

# Work on the largest connected component for path-based metrics (diameter, avg path length)
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()
log(f"\nLargest connected component: {len(largest_cc)} of {G.number_of_nodes()} nodes")

if nx.is_connected(G_lcc):
    diameter = nx.diameter(G_lcc)
    avg_path_length = nx.average_shortest_path_length(G_lcc)
    log(f"Network diameter (largest component): {diameter} hops")
    log(f"Average shortest path length (largest component): {avg_path_length:.3f} hops")

# ===========================================================================
# Centrality measures
# ===========================================================================
log("\n" + "=" * 70)
log("CENTRALITY MEASURES")
log("=" * 70)

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
pagerank = nx.pagerank(G)
clustering = nx.clustering(G)

def top_n(d, n=10):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

id_to_name = substations.set_index("Substation ID")["Short Name"].to_dict()

log("\nTop 10 substations by DEGREE CENTRALITY (most direct connections):")
for sid, val in top_n(degree_centrality):
    log(f"  {id_to_name.get(sid, sid):25s} ({sid}): {val:.4f}  [{G.degree(sid)} connections]")

log("\nTop 10 substations by BETWEENNESS CENTRALITY (critical bridges between regions):")
for sid, val in top_n(betweenness_centrality):
    log(f"  {id_to_name.get(sid, sid):25s} ({sid}): {val:.4f}")

log("\nTop 10 substations by CLOSENESS CENTRALITY (fastest average reach):")
for sid, val in top_n(closeness_centrality):
    log(f"  {id_to_name.get(sid, sid):25s} ({sid}): {val:.4f}")

log("\nTop 10 substations by PAGERANK (importance via connections' connections):")
for sid, val in top_n(pagerank):
    log(f"  {id_to_name.get(sid, sid):25s} ({sid}): {val:.4f}")

avg_clustering = nx.average_clustering(G)
log(f"\nAverage clustering coefficient (network-wide): {avg_clustering:.4f}")
log("(How often a substation's neighbours are also connected to each other --")
log(" higher values suggest more meshed, redundant local structure.)")

# ===========================================================================
# Bridges (single points of failure)
# ===========================================================================
log("\n" + "=" * 70)
log("BRIDGES (single lines whose removal disconnects the network)")
log("=" * 70)

bridges = list(nx.bridges(G))
log(f"Number of bridge edges: {len(bridges)}")
if bridges:
    log("These lines are single points of failure -- if any one is lost, the")
    log("network splits into more pieces (no redundant path exists):")
    for u, v in bridges[:20]:
        log(f"  {id_to_name.get(u,u)} -- {id_to_name.get(v,v)}")
    if len(bridges) > 20:
        log(f"  ... and {len(bridges) - 20} more")
else:
    log("No bridges found -- every line has at least one redundant alternate path.")

# ===========================================================================
# Community detection
# ===========================================================================
log("\n" + "=" * 70)
log("COMMUNITY DETECTION")
log("=" * 70)

try:
    from networkx.algorithms.community import greedy_modularity_communities
    communities = list(greedy_modularity_communities(G))
    log(f"Detected {len(communities)} communities (greedy modularity maximisation)")
    for i, comm in enumerate(communities):
        regions_in_comm = substations[substations["Substation ID"].isin(comm)]["Region"].value_counts()
        top_region = regions_in_comm.idxmax() if len(regions_in_comm) else "N/A"
        log(f"  Community {i+1}: {len(comm)} substations, dominant region: {top_region}")
except Exception as e:
    log(f"Community detection failed: {e}")
    communities = []

# Compare detected communities against actual Region labels
log("\nComparison: does detected community structure line up with the Region column?")
region_counts = substations["Region"].value_counts()
log(f"Actual number of distinct regions/countries in the data: {len(region_counts)}")
log(f"Number of algorithmically detected communities: {len(communities)}")

# ===========================================================================
# Network efficiency
# ===========================================================================
log("\n" + "=" * 70)
log("NETWORK EFFICIENCY")
log("=" * 70)
efficiency = nx.global_efficiency(G)
log(f"Global efficiency: {efficiency:.4f}")
log("(Average of 1/shortest-path-length over all node pairs, 0-1 scale --")
log(" closer to 1 means information/power can reach across the network in")
log(" very few hops on average.)")

# ===========================================================================
# Critical substation classification (combining metrics)
# ===========================================================================
log("\n" + "=" * 70)
log("CRITICAL SUBSTATION CLASSIFICATION")
log("=" * 70)

metrics_df = pd.DataFrame({
    "Substation ID": list(G.nodes()),
    "Name": [id_to_name.get(n, n) for n in G.nodes()],
    "Region": [G.nodes[n]["region"] for n in G.nodes()],
    "Degree": [G.degree(n) for n in G.nodes()],
    "Degree Centrality": [degree_centrality[n] for n in G.nodes()],
    "Betweenness Centrality": [betweenness_centrality[n] for n in G.nodes()],
    "Closeness Centrality": [closeness_centrality[n] for n in G.nodes()],
    "PageRank": [pagerank[n] for n in G.nodes()],
})

# Simple composite "criticality score" -- normalized sum of the three structural metrics
for col in ["Degree Centrality", "Betweenness Centrality", "Closeness Centrality", "PageRank"]:
    rng = metrics_df[col].max() - metrics_df[col].min()
    metrics_df[col + " (norm)"] = (metrics_df[col] - metrics_df[col].min()) / rng if rng > 0 else 0

metrics_df["Criticality Score"] = metrics_df[
    ["Degree Centrality (norm)", "Betweenness Centrality (norm)",
     "Closeness Centrality (norm)", "PageRank (norm)"]
].mean(axis=1)

metrics_df = metrics_df.sort_values("Criticality Score", ascending=False).reset_index(drop=True)
metrics_df.to_csv("substation_criticality_ranking.csv", index=False)

log("Top 10 most critical substations (composite of degree, betweenness,")
log("closeness, and PageRank -- a STRUCTURAL proxy, not an electrical-load")
log("or voltage-stability measurement):")
log(metrics_df[["Name", "Region", "Degree", "Criticality Score"]].head(10).to_string(index=False))

log("\nIMPORTANT CAVEAT: graph centrality reflects topological position only.")
log("It does NOT represent electrical load, voltage stability, protection")
log("behaviour, or real-time power flow. A substation can be structurally")
log("'central' while carrying little actual load, or vice versa. These")
log("results should be read as structural observations / reliability")
log("proxies to guide further engineering investigation, not as definitive")
log("operational findings.")

# ===========================================================================
# N-1 Contingency Analysis
# ===========================================================================
log("\n" + "=" * 70)
log("N-1 CONTINGENCY ANALYSIS")
log("=" * 70)
log("Simplified educational approximation: remove one important substation")
log("at a time and measure the effect on network connectivity. This is NOT")
log("a substitute for real power-flow, transient-stability, or protection-")
log("coordination studies -- it develops intuition about redundancy only.")

top5_critical = metrics_df.head(5)["Substation ID"].tolist()
baseline_components = nx.number_connected_components(G)

contingency_results = []
for sid in top5_critical:
    G_test = G.copy()
    name = id_to_name.get(sid, sid)
    region = G.nodes[sid]["region"]
    degree_removed = G.degree(sid)
    G_test.remove_node(sid)
    new_components = nx.number_connected_components(G_test)
    if len(G_test.nodes()) > 0 and new_components > 0:
        largest_after = len(max(nx.connected_components(G_test), key=len))
    else:
        largest_after = 0
    contingency_results.append({
        "Substation": name, "Region": region, "Connections lost": degree_removed,
        "Components before": baseline_components, "Components after": new_components,
        "Fragmented?": "YES" if new_components > baseline_components else "no",
        "Largest remaining component": largest_after,
    })

contingency_df = pd.DataFrame(contingency_results)
log("\n" + contingency_df.to_string(index=False))
contingency_df.to_csv("n1_contingency_results.csv", index=False)

n_fragmenting = (contingency_df["Fragmented?"] == "YES").sum()
log(f"\n{n_fragmenting} of the top 5 most critical substations, if lost, would")
log("fragment the network into more pieces than it currently has.")
if n_fragmenting == 0:
    log("None of the top-5 most structurally central substations caused")
    log("fragmentation when removed individually -- this suggests the network")
    log("has meaningful redundancy (multiple paths) around its top hubs, at")
    log("least at this level of aggregation. This is a good discussion point:")
    log("a well-meshed regional network can tolerate a single substation loss,")
    log("whereas a radial (tree-like) network would fragment immediately.")

# ===========================================================================
# Visualization
# ===========================================================================
log("\n" + "=" * 70)
log("GENERATING VISUALIZATION")
log("=" * 70)

fig, ax = plt.subplots(figsize=(14, 10))
pos = {n: (G.nodes[n]["lon"], G.nodes[n]["lat"]) for n in G.nodes()}

node_sizes = [300 + 4000 * degree_centrality[n] for n in G.nodes()]
node_colors = [betweenness_centrality[n] for n in G.nodes()]

nx.draw_networkx_edges(G, pos, alpha=0.3, width=1, ax=ax)
nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors,
                                 cmap=plt.cm.YlOrRd, ax=ax)
labels = {n: id_to_name.get(n, n) for n in G.nodes() if degree_centrality[n] > np.percentile(list(degree_centrality.values()), 75)}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)

plt.colorbar(nodes, ax=ax, label="Betweenness Centrality")
ax.set_title("National Grid Network\n(node size = degree centrality, color = betweenness centrality)", fontsize=13)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("network_graph.png", dpi=150)
plt.close()
log("Saved network_graph.png")

# Save full metrics to JSON for reuse in later tasks (dashboard, etc.)
all_metrics = {
    "degree_centrality": {str(k): v for k, v in degree_centrality.items()},
    "betweenness_centrality": {str(k): v for k, v in betweenness_centrality.items()},
    "closeness_centrality": {str(k): v for k, v in closeness_centrality.items()},
    "pagerank": {str(k): v for k, v in pagerank.items()},
    "clustering": {str(k): v for k, v in clustering.items()},
}
with open("network_metrics.json", "w") as f:
    json.dump(all_metrics, f, indent=2)
log("Saved network_metrics.json")

with open("network_analysis_report.txt", "w") as f:
    f.write("\n".join(report))
print("\n\nFull report saved to network_analysis_report.txt")