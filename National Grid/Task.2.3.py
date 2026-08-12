"""
Task 2.3: Business Intelligence and Reliability Analysis

National Electricity Grid Network Analysis
Prepared by: Team Member 2 - Data Analyst
Dataset: Seeded synthetic dataset (seed = 42)
Network: 10 utilities, 44 substations, 55 lines
Reference year: 2026

1. Utility Footprint Analysis

The utility footprint analysis shows that GRIDCo has the largest network presence, operating 24 of the 55 lines in the dataset. 
Its network is particularly concentrated at the high-voltage transmission level, with 9 lines operating at 330 kV. 
This represents 37.5% of GRIDCo's total lines.

NEDCo operates 14 lines and has a stronger concentration at the 11 kV distribution level, with 6 of its lines operating at this voltage. ECG operates 10 lines across several voltage levels, while CEB, CIE, and SONABEL have smaller footprints concentrated primarily at 330 kV.

Utility	11 kV	33 kV	69 kV	161 kV	330 kV	Total
GRIDCo	5	3	3	4	9	24
NEDCo	6	2	4	2	0	14
ECG	3	3	2	1	1	10
CEB	0	0	0	0	3	3
CIE	0	0	0	0	2	2
SONABEL	0	0	0	0	2	2

Geographically, GRIDCo also has the widest footprint, operating lines in 9 of the 12 line-bearing regions. 
ECG operates across 6 regions, while NEDCo operates across 7.

Finding: The distribution of lines across utilities and voltage levels provides a useful internal consistency check.
 GRIDCo has the strongest transmission-oriented footprint, while NEDCo has a greater distribution-level presence.

2. Capacity Utilization Mapping

The dataset does not contain actual electricity load or demand, meaning a true capacity-utilization ratio cannot be calculated.
 Therefore, the analysis uses the rank of substation capacity as a proxy for identifying strategically important assets.

The substations in the top 15% of the capacity distribution have capacities of at least 333 MVA.

Substation	Region	Type	Voltage (kV)	Capacity (MVA)
Cotonou Transmission Hub	Benin	Transmission	161	487.6
Bobo-Dioulasso Hub	Burkina Faso	Transmission	161	445.9
Aflao Border Station	Togo border	Transmission	330	423.2
Nkawkaw	Eastern	Bulk Supply Point	69	389.2
Ho	Volta	Transmission	330	382.1
Ejisu	Ashanti	Transmission	330	355.9
Suhum	Eastern	Bulk Supply Point	69	339.0

These high-capacity substations represent strategically important assets that should be monitored when considering future network expansion and resilience.

The bottom 15% of substations have capacities of 27 MVA or below.

Substation	Region	Type	Voltage (kV)	Capacity (MVA)
Achimota	Greater Accra	Distribution	11	6.4
Kpong	Volta	Distribution	11	11.2
Takoradi	Western	Distribution	33	14.0
Hohoe	Volta	Distribution	11	18.2
Sunyani	Bono	Distribution	33	19.6
Mallam	Greater Accra	Transmission	330	25.2
Assin Fosu	Central	Distribution	11	26.2

Finding: Mallam is particularly significant because it combines relatively low rated capacity with high network connectivity. Its position in the bottom capacity group does not necessarily indicate inadequate service, but its combination of low capacity and high structural importance makes it a strong candidate for further capacity and reliability assessment.

3. Growth Opportunities: Underserved Regions

The analysis identifies regions that fall below the median in both substation count and total substation capacity.

Region	Number of Substations	Total Capacity (MVA)
Cote d'Ivoire	1	262.6
Burkina Faso border	1	156.1
Cote d'Ivoire border	1	285.1
Upper West	1	27.1
Guinea	1	251.6
Togo	1	120.2

Several of these regions represent international interconnection points.
 Their low substation count is therefore not necessarily evidence of inadequate domestic infrastructure.

Upper West is the strongest genuine domestic growth opportunity. 
It has only one substation and a total capacity of 27.1 MVA, which is substantially lower than the other regions in the analysis.

This finding becomes even more significant when combined with the asset-age analysis,
 which shows that Upper West also has the oldest average infrastructure in the network.

Finding: Upper West should receive particular attention in future infrastructuredevelopment planning because it combines limited network coverage, 
very low capacity, and aging infrastructure.

4. Technical-Loss Proxy Analysis

Because the dataset does not contain the electrical parameters required for an engineering-grade calculation of technical losses, 
a relative loss-risk proxy was calculated using:

Loss Proxy = Line Length (km) ÷ Line Voltage (kV)

A higher score indicates a combination of long transmission distance and relatively low operating voltage.

Voltage	Average Loss Proxy
11 kV	6.823
33 kV	1.887
69 kV	1.008
161 kV	0.155
330 kV	0.555

The results show a strong decline in the loss-proxy score as voltage increases. 
The average score for 11 kV lines is approximately 12 times that of 161 kV lines.

The highest-risk line according to this proxy is:

Hohoe → Sogakope

Distance: 152.5 km
Voltage: 11 kV
Loss proxy: 13.86

All ten of the highest-ranked lines by this proxy operate at 11 kV.

Finding: Long-distance electricity transmission at relatively low voltage represents a structural loss-risk signal in the dataset. 
The Hohoe-Sogakope corridor is the strongest candidate for further engineering investigation and possible voltage-upgrade consideration.

However, actual load data and electrical characteristics would be required before making a final investment decision.

5. Asset Age Profile

The asset-age analysis uses 2026 as the reference year.

Statistic	Value
Mean age	29.7 years
Median age	26.5 years
Minimum age	4 years
Maximum age	59 years
Standard deviation	16.1 years

The network therefore contains a substantial amount of relatively mature infrastructure.

Oldest regions by average asset age
Region	Average Age
Upper West	49.0 years
Upper East	44.5 years
Northern	38.7 years
Western	38.2 years
Newest regions by average asset age
Region	Average Age
Togo border	11.0 years
Togo	12.0 years
Cote d'Ivoire	16.0 years

By substation type, Distribution substations have an average age of 31.1 years, Transmission substations average 29.3 years, and Bulk Supply Points average 28.1 years.

Finding: Aging infrastructure is particularly pronounced in Upper West, Upper East, and Northern regions. The combination of aging infrastructure with low network capacity and limited substation coverage makes the northern regions important candidates for infrastructure investment.

6. Reliability Risk Analysis

The reliability analysis combines three indicators:

Substation age - 40%
Degree centrality -40%
Maintenance flag - 20%

The resulting score provides a relative reliability-risk ranking, rather than a prediction of actual equipment failure.

Rank	Substation	Region	Age	Degree Centrality	Maintenance	Risk Score
1	Mallam	Greater Accra	47	0.122	Yes	91.3
2	Cape Coast	Central	34	0.122	Yes	81.8
3	Aboadze	Western	59	0.073	No	64.0
4	Tamale	Northern	57	0.073	No	62.5
5	Kaneshie	Greater Accra	56	0.073	No	61.8
6	Kasoa	Central	23	0.073	Yes	57.8
7	Winneba	Central	56	0.049	No	53.8
8	Bolgatanga	Upper East	34	0.098	No	53.8
9	Ho	Volta	30	0.098	No	50.9
10	Axim	Western	52	0.049	No	50.9

Mallam has the highest reliability-risk score of 91.3. 
Its risk is driven by its combination of relatively high age,
 high network connectivity, and a maintenance flag.

Cape Coast ranks second, also combining high connectivity with a maintenance flag.

The results are consistent with the earlier network-centrality analysis from Task 1.2, 
where Mallam and Cape Coast were identified among the most-connected substations. 
This provides an internal consistency check between the analyses.

7. Strategic Recommendations
1. Prioritize Mallam for reliability and capacity assessment

Mallam should be treated as a high-priority asset because it combines high network connectivity,
 relatively old infrastructure, a maintenance flag, and comparatively low rated capacity.

It should be included among the first substations considered in the N-1 contingency analysis to determine the consequences of its potential failure.

2. Prioritize Cape Coast for reliability assessment

Cape Coast also combines high network connectivity with an active maintenance flag.
 Its potential failure could therefore have a disproportionate effect on network connectivity.

It should also be tested through contingency analysis.

3. Direct regional investment toward Upper West

Upper West represents the clearest domestic growth opportunity. 
The region has only one substation, total capacity of 27.1 MVA, 
and the oldest average infrastructure in the dataset.

Investment should therefore consider both network expansion and infrastructure replacement/modernization.

4. Investigate long-distance 11 kV corridors

The highest loss-proxy lines should be subjected to further engineering investigation, particularly the Hohoe-Sogakope corridor.

Potential voltage upgrades should only be considered after actual electricity-load data 
and engineering measurements confirm that the losses are material.

5. Evaluate critical assets using multiple indicators

Criticality should not be determined using only network connectivity or capacity.

A substation can be critical because it:

handles substantial capacity,
connects many network elements,
is old,
has maintenance exposure,
or combines several of these characteristics.

The final assessment should therefore compare capacity concentration and network centrality together.

6. Clearly communicate the limitations of the analysis

The conclusions should be presented as directional findings from synthetic data, 
rather than confirmed operational conditions.

The major limitations are:

no actual electricity-load data;
no measured technical-loss data;
only two maintenance-flagged lines;
capacity utilization is based on ranking rather than actual utilization;
the reliability weights are analytical assumptions rather than statistically estimated weights.

These limitations should be clearly stated in the final presentation to avoid overstating the findings.
"""