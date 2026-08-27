### Task 5: Visualization and Network Analysis

**Top Substation and Operational Importance**

Mallam Substation is one of the most highly connected substations in the network, with a degree centrality of **0.1220**, tied with Kumasi Central Substation and Cape Coast Substation. A highly connected substation is operationally important because it has direct connections to several other substations. Therefore, a failure at such a substation could potentially affect multiple parts of the electricity network. However, the N-1 contingency analysis showed that removing Mallam Substation did not disconnect the network, as the number of connected components remained **1 before and after its removal**. This suggests that the network has some resilience to the loss of this highly connected substation.

**Suggested Improvement to the Network Visualization**

One improvement would be to **size the nodes according to their degree centrality**. Highly connected substations could be displayed with larger nodes, while less-connected substations could have smaller nodes. This would make important network hubs easier to identify visually and would help users quickly understand which substations play the most important role in network connectivity.

**Key Network Results**

The network analysis produced **42 substations (nodes)** and **55 transmission lines (edges)**. The three substations with the highest degree centrality were Mallam Substation, Kumasi Central Substation, and Cape Coast Substation, each with a centrality of **0.1220**. The N-1 contingency analysis showed that the network remained connected after removing the top hub, with **1 connected component before removal and 1 connected component after removal**.
