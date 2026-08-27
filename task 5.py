import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

# Load the cleaned datasets
substations = pd.read_csv('substations.csv')
lines = pd.read_csv('lines.csv')







# Interactive map of substations
fig = px.scatter_geo(
    substations,
    lat='Latitude',
    lon='Longitude',
    hover_name='Name',
    color='Region',
    title='National Grid Substation Locations',
    projection='natural earth'
)

fig.show()

# Save the interactive map as an HTML file
fig.write_html('substation_map.html')

print("Interactive substation map saved as substation_map.html")



# Network analysis of transmission lines
# The network is undirected because power can flow in either direction

G = nx.from_pandas_edgelist(
    lines,
    source='Source Substation',
    target='Destination Substation',
    edge_attr=['Length (km)', 'Voltage (kV)'],
    create_using=nx.Graph()
)

print("Number of nodes (substations):", G.number_of_nodes())
print("Number of edges (lines):", G.number_of_edges())



# Calculate degree centrality
degree_centrality = nx.degree_centrality(G)

# Get the top 10 most-connected substations
top_substations = sorted(
    degree_centrality.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("\nTop 10 Substations by Degree Centrality:")

for substation, centrality in top_substations:
    print(f"{substation}: {centrality:.4f}")



    # N-1 contingency analysis
# Remove the most-connected substation and check network fragmentation

top_hub = top_substations[0][0]

G_minus = G.copy()
G_minus.remove_node(top_hub)

print("\nN-1 Contingency Analysis")
print("Top substation removed:", top_hub)
print("Connected components before removing top hub:",
      nx.number_connected_components(G))
print("Connected components after removing top hub:",
      nx.number_connected_components(G_minus))



# Visualize the substation network

plt.figure(figsize=(12, 8))

nx.draw(
    G,
    with_labels=True,
    node_size=200,
    node_color='lightblue',
    font_size=6
)

plt.title('National Grid Substation Network')
plt.show()