"""
Task 2.3: Business Intelligence and Reliability Analysis
National Electricity Grid Network Analysis — Data Analyst Deliverable

Prepared by: Team Member 2 (Data Analyst)
Dataset: Synthetic Ghana grid dataset, seed = 42
Network: 10 utilities, 44 substations, 55 lines
Reference year: 2026

1. Utility Footprint Analysis

The utility footprint analysis shows that GRIDCo operates the largest number of lines, with 24 out of the 55 lines in the network. NEDCo operates 14 lines, while ECG operates 10. The remaining utilities have smaller footprints.

Utility	11 kV	33 kV	69kV	161 kV	330 kV	Total
GRIDCo	5	3	3	4	9	24
NEDCo	6	2	4	2	0	14
ECG	3	3	2	1	1	10
CEB	0	0	0	0	3	3
CIE	0	0	0	0	2	2 
SONABEL	0	0	0	0	2	2

GRIDCo's largest concentration is at the 330 kV transmission level, where it operates 9 lines, representing 37.5% of its total lines. NEDCo has its largest concentration at 11 kV, where it operates 6 lines, representing approximately 43% of its footprint.

The geographic distribution also shows that GRIDCo has the widest coverage, operating lines across 9 of the 12 line-bearing regions.

Key Finding

GRIDCo has the largest and most transmission-oriented network footprint, while NEDCo has a stronger distribution-level presence. This pattern is consistent with the intended roles of the utilities within the synthetic dataset.

2. Capacity Utilization Mapping

The dataset does not contain actual electricity-load or demand information. Therefore, a true capacity-utilization ratio cannot be calculated. Instead, substation capacity rankings are used as a proxy for identifying assets that may have strategic importance.

Highest-Capacity Substations
Substation	Region	Type	Voltage (kV)	Capacity (MVA)
Cotonou Transmission Hub	Benin	Transmission	161	487.6
Bobo-Dioulasso Hub	Burkina Faso	Transmission	161	445.9
Aflao Border Station	Togo border	Transmission	330	423.2
Nkawkaw	Eastern	Bulk Supply Point	69	389.2
Ho	Volta	Transmission	330	382.1
Ejisu	Ashanti	Transmission	330	355.9
Suhum	Eastern	Bulk Supply Point	69	339.0

These high-capacity substations represent strategically important assets that should be monitored for future network expansion and resilience.

Lowest-Capacity Substations
Substation	Region	Type	Voltage (kV)	Capacity (MVA)
Achimota	Greater Accra	Distribution	11	6.4
Kpong	Volta	Distribution	11	11.2
Takoradi	Western	Distribution	33	14.0
Hohoe	Volta	Distribution	11	18.2
Sunyani	Bono	Distribution	33	19.6
Mallam	Greater Accra	Transmission	330	25.2
Assin Fosu	Central	Distribution	11	26.2

Mallam is the most important finding in this analysis. Although its rated capacity is only 25.2 MVA, it is a highly connected substation. Task 1.2 identified Mallam as one of the three most-connected substations, with five connected lines.

Therefore, Mallam should not simply be classified as a low-capacity asset. Its combination of low capacity and high network connectivity makes it a potential upgrade and reliability priority.

3. Growth Opportunities: Underserved Regions

The analysis identifies regions that fall below the median in both substation count and total capacity.

Region	Substations	Total Capacity (MVA)
Cote d'Ivoire	1	262.6
Burkina Faso border	1	156.1
Cote d'Ivoire border	1	285.1
Upper West	1	27.1
Guinea	1	251.6
Togo	1	120.2

Several of these locations are cross-border interconnection points. Their low number of substations does not necessarily represent inadequate domestic electricity infrastructure.

Upper West is the clearest domestic growth opportunity.

The region has:

only 1 substation;
only 27.1 MVA of total capacity; and
the oldest average infrastructure in the network at 49 years.

Task 1.2 also identified Upper West as having only one substation and highlighted it as a potential coverage gap, while noting that the result may partly reflect the way the synthetic dataset was generated.

Key Finding

Upper West should be prioritized for further infrastructure assessment because it combines very limited network coverage, extremely low capacity, and aging infrastructure.

4. Technical-Loss Proxy Analysis

The dataset does not contain the electrical measurements required to calculate actual technical losses. Therefore, a relative technical-loss proxy is calculated as:

Loss Proxy = Line Length (km) ÷ Line Voltage (kV)

A higher value indicates a longer line operating at a relatively lower voltage and therefore represents a greater relative loss-risk signal.

Voltage	Average Loss Proxy
11 kV	6.823
33 kV	1.887
69 kV	1.008
161 kV	0.155
330 kV	0.555

The results show that 11 kV lines have the highest average loss-proxy score, while 161 kV lines have the lowest.

The highest-risk line according to this proxy is:

Hohoe → Sogakope
Length: 152.5 km
Voltage: 11 kV
Loss-proxy score: 13.86

The analysis also shows that all ten of the highest-ranked lines by this proxy operate at 11 kV.

Key Finding

Long-distance lines operating at relatively low voltage represent the greatest loss-risk signal in the dataset. Hohoe–Sogakope is the strongest case and should be investigated as a potential candidate for voltage upgrading.

However, actual load and engineering data would be required before confirming that a voltage upgrade is economically or technically justified.

5. Asset Age Profile

The age of each asset is calculated relative to the 2026 reference year.

Statistic	Value
Mean age	29.7 years
Median age	26.5 years
Minimum age	4 years
Maximum age	59 years
Standard deviation	16.1 years
Oldest Regions
Region	Average Age
Upper West	49.0 years
Upper East	44.5 years
Northern	38.7 years
Western	38.2 years
Newest Regions
Region	Average Age
Togo border	11.0 years
Togo	12.0 years
Cote d'Ivoire	16.0 years

By substation type:

Distribution: 31.1 years
Transmission: 29.3 years
Bulk Supply Point: 28.1 years
Key Finding

The network has a relatively mature asset base, with an average age of 29.7 years. Upper West, Upper East, and Northern have particularly old infrastructure.

The age finding becomes more significant when combined with capacity and coverage. Upper West is not only one of the least-served regions but also has the oldest infrastructure, strengthening the case for targeted investment.

6. Reliability Risk Analysis

The reliability risk score combines three factors:

Substation age: 40%
Degree centrality: 40%
Maintenance status: 20%

The resulting score is a relative reliability-risk measure, not a prediction that a substation will actually fail.

Top 10 Reliability-Risk Substations
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
Key Finding

Mallam has the highest reliability-risk score at 91.3, followed by Cape Coast at 81.8.

Both substations have a degree centrality of 0.122 and currently have maintenance exposure. Their high connectivity means that disruption could have a greater structural impact on the network.

This finding is consistent with Task 1.2, which identified Mallam, Kumasi Central, and Cape Coast as the three most-connected substations, each with five connected lines.

The analysis therefore provides an important cross-validation between the exploratory analysis and the reliability analysis.

7. Strategic Recommendations
Recommendation 1: Prioritize Mallam for reliability and capacity assessment

Mallam should receive immediate analytical attention because it combines:

high network connectivity;
relatively old infrastructure;
a maintenance flag; and
comparatively low rated capacity.

Mallam should therefore be one of the first substations tested in the N-1 contingency analysis to determine the consequences of its potential failure.

Recommendation 2: Prioritize Cape Coast for reliability assessment

Cape Coast has high network connectivity and an active maintenance flag. Its high reliability-risk score indicates that it should also be subjected to detailed contingency and reliability analysis.

Recommendation 3: Prioritize Upper West for infrastructure investment

Upper West is the clearest domestic growth opportunity because it combines:

only one substation;
27.1 MVA total capacity;
the oldest average infrastructure in the network.

Investment should focus on both network expansion and modernization of aging infrastructure.

Recommendation 4: Investigate long-distance 11 kV corridors

The highest loss-proxy lines should be subjected to engineering investigation, with Hohoe–Sogakope receiving particular attention.

Potential voltage upgrades should only be pursued after actual load, conductor, and technical-loss data confirm the need.

Recommendation 5: Assess criticality using multiple indicators

Critical infrastructure should not be identified using only one measure.

The analysis demonstrates that capacity and network connectivity identify different dimensions of importance. A substation may be important because it handles large capacity, because it connects many network elements, or because it combines several risk factors.

The final assessment should therefore consider capacity, connectivity, age, and maintenance status together.

Recommendation 6: Clearly communicate the limitations of the analysis

The findings should be presented as directional signals from synthetic data rather than confirmed operational conditions.

The main limitations are:

The dataset contains no actual electricity-load data.
Capacity utilization is therefore estimated using a ranking-based proxy.
Technical losses are represented using a length-to-voltage proxy rather than engineering calculations.
Only two lines are currently marked as under maintenance.
The reliability-risk weights of 40%, 40%, and 20% are analytical assumptions rather than statistically derived weights.
The dataset is synthetic and may not perfectly represent the actual Ghanaian electricity network.
8. Overall Conclusion

The Business Intelligence and Reliability Analysis identifies several important areas for attention within the national electricity-grid dataset.

GRIDCo has the largest network footprint and is strongly concentrated in high-voltage transmission. The capacity analysis identifies several strategically important substations, while Mallam stands out as a particularly important asset because its relatively low capacity is combined with high connectivity and elevated reliability risk.

At the regional level, Upper West represents the clearest domestic infrastructure-development opportunity, combining very low capacity and substation coverage with the oldest average infrastructure.

The technical-loss proxy identifies long-distance 11 kV corridors as the greatest relative loss-risk category, with Hohoe–Sogakope representing the most significant case.

Finally, the reliability analysis identifies Mallam and Cape Coast as the two highest-priority substations for further reliability and contingency assessment.

Overall, the analysis supports three major strategic priorities:

1. Strengthen critical and highly connected substations.
2. Direct infrastructure investment toward underserved and aging regions, particularly Upper West.
3. Investigate long-distance low-voltage corridors for potential efficiency improvements.

Because the analysis is based on a synthetic dataset and uses proxies where direct operational measurements are unavailable, these findings should guide further investigation and decision-making rather than be treated as definitive evidence of actual grid failure, overload, or technical losses.

"""