"""
Task 1.2: Exploratory Data Analysis (Data Analyst)
----------------------------------------------------
Covers every required activity:
- Descriptive statistics for numerical variables
- Frequency distributions for categorical variables
- Top utilities by number of lines operated
- Most-connected substations by number of lines
- Geographic distribution of substations and lines by region
- Substation status (Active/Inactive) and voltage-level distribution
"""
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

utilities = pd.read_csv("utilities.csv")
substations = pd.read_csv("substations.csv")
lines = pd.read_csv("lines.csv")

print("=" * 90)
print("1. DESCRIPTIVE STATISTICS FOR NUMERICAL VARIABLES")
print("=" * 90)

print("\n--- Substations: numeric summary ---")
sub_numeric = substations[["Voltage (kV)", "Capacity (MVA)", "Commissioning Year"]]
print(sub_numeric.describe().round(2))

print("\n--- Lines: numeric summary ---")
lines_numeric = lines[["Voltage (kV)", "Length (km)", "Capacity (MVA)"]]
print(lines_numeric.describe().round(2))

print("\n" + "=" * 90)
print("2. FREQUENCY DISTRIBUTIONS FOR CATEGORICAL VARIABLES")
print("=" * 90)

print("\n--- Substation Type ---")
print(substations["Type"].value_counts())

print("\n--- Substation Status ---")
print(substations["Status"].value_counts())

print("\n--- Substation Region ---")
print(substations["Region"].value_counts())

print("\n--- Voltage Level (kV) ---")
print(substations["Voltage (kV)"].value_counts().sort_index())

print("\n--- Line Status ---")
print(lines["Status"].value_counts())

print("\n--- Line Type ---")
print(lines["Line Type"].value_counts())

print("\n--- Utility Type ---")
print(utilities["Type"].value_counts())

print("\n" + "=" * 90)
print("3. TOP UTILITIES BY NUMBER OF LINES OPERATED")
print("=" * 90)

lines_with_utility = lines.merge(
    utilities[["Utility ID", "Name", "Alias"]], on="Utility ID", how="left"
)
top_utilities = (
    lines_with_utility.groupby(["Alias", "Name"])
    .size()
    .reset_index(name="Line Count")
    .sort_values("Line Count", ascending=False)
)
print(top_utilities.to_string(index=False))

print("\n" + "=" * 90)
print("4. MOST-CONNECTED SUBSTATIONS (BY NUMBER OF LINES)")
print("=" * 90)

connection_counts = pd.concat([
    lines["Source Substation"],
    lines["Destination Substation"],
]).value_counts().reset_index()
connection_counts.columns = ["Substation", "Connections"]
top_connected = connection_counts.head(10)
print(top_connected.to_string(index=False))

print("\n" + "=" * 90)
print("5. GEOGRAPHIC DISTRIBUTION: SUBSTATIONS AND LINES BY REGION")
print("=" * 90)

subs_by_region = substations["Region"].value_counts().reset_index()
subs_by_region.columns = ["Region", "Substation Count"]
print("\n--- Substations per Region ---")
print(subs_by_region.to_string(index=False))

# Lines by region of their source substation
lines_region = lines.merge(
    substations[["Substation ID", "Region"]],
    left_on="Source Substation ID", right_on="Substation ID", how="left"
)
lines_by_region = lines_region["Region"].value_counts().reset_index()
lines_by_region.columns = ["Region", "Line Count (by source substation)"]
print("\n--- Lines per Region (by source substation) ---")
print(lines_by_region.to_string(index=False))

print("\n" + "=" * 90)
print("6. SUBSTATION STATUS AND VOLTAGE-LEVEL DISTRIBUTION")
print("=" * 90)

status_voltage_crosstab = pd.crosstab(substations["Voltage (kV)"], substations["Status"])
print("\n--- Status by Voltage Level (crosstab) ---")
print(status_voltage_crosstab)

inactive_pct = (substations["Status"] == "Inactive").mean() * 100
print(f"\nOverall inactive substation rate: {inactive_pct:.1f}%")

# ---------------------------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")

# Chart 1: Substations by region
plt.figure(figsize=(9, 5))
subs_by_region_sorted = subs_by_region.sort_values("Substation Count", ascending=False)
plt.bar(subs_by_region_sorted["Region"], subs_by_region_sorted["Substation Count"], color="#2E5090")
plt.title("Number of Substations by Region")
plt.xlabel("Region")
plt.ylabel("Number of Substations")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("eda_charts/01_substations_by_region.png", dpi=150)
plt.close()

# Chart 2: Voltage level distribution
plt.figure(figsize=(8, 5))
voltage_counts = substations["Voltage (kV)"].value_counts().sort_index()
plt.bar(voltage_counts.index.astype(str), voltage_counts.values, color="#C0392B")
plt.title("Distribution of Substation Voltage Levels")
plt.xlabel("Voltage Level (kV)")
plt.ylabel("Number of Substations")
plt.tight_layout()
plt.savefig("eda_charts/02_voltage_distribution.png", dpi=150)
plt.close()

# Chart 3: Top 10 most-connected substations
plt.figure(figsize=(9, 5))
top10 = top_connected.head(10).sort_values("Connections")
plt.barh(top10["Substation"], top10["Connections"], color="#1E8449")
plt.title("Top 10 Most-Connected Substations")
plt.xlabel("Number of Lines Connected")
plt.tight_layout()
plt.savefig("eda_charts/03_top_connected_substations.png", dpi=150)
plt.close()

# Chart 4: Top utilities by line count
plt.figure(figsize=(8, 5))
top_util_sorted = top_utilities.sort_values("Line Count")
plt.barh(top_util_sorted["Alias"], top_util_sorted["Line Count"], color="#7D3C98")
plt.title("Number of Lines Operated by Utility")
plt.xlabel("Line Count")
plt.tight_layout()
plt.savefig("eda_charts/04_lines_by_utility.png", dpi=150)
plt.close()

# Chart 5: Substation status
plt.figure(figsize=(6, 5))
status_counts = substations["Status"].value_counts()
plt.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%",
        colors=["#2ECC71", "#E74C3C"], startangle=90)
plt.title("Substation Status: Active vs Inactive")
plt.tight_layout()
plt.savefig("eda_charts/05_substation_status.png", dpi=150)
plt.close()

# Chart 6: Capacity distribution histogram
plt.figure(figsize=(8, 5))
plt.hist(substations["Capacity (MVA)"], bins=15, color="#2874A6", edgecolor="white")
plt.title("Distribution of Substation Capacity (MVA)")
plt.xlabel("Capacity (MVA)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("eda_charts/06_capacity_distribution.png", dpi=150)
plt.close()

# Chart 7: Commissioning year distribution (asset age profile)
plt.figure(figsize=(9, 5))
plt.hist(substations["Commissioning Year"], bins=15, color="#B9770E", edgecolor="white")
plt.title("Substation Commissioning Year Distribution (Asset Age Profile)")
plt.xlabel("Commissioning Year")
plt.ylabel("Number of Substations")
plt.tight_layout()
plt.savefig("eda_charts/07_commissioning_year.png", dpi=150)
plt.close()

# Chart 8: Line status
plt.figure(figsize=(6, 5))
line_status_counts = lines["Status"].value_counts()
plt.pie(line_status_counts.values, labels=line_status_counts.index, autopct="%1.1f%%",
        colors=["#3498DB", "#F39C12"], startangle=90)
plt.title("Line Status: Active vs Under Maintenance")
plt.tight_layout()
plt.savefig("eda_charts/08_line_status.png", dpi=150)
plt.close()

print("\n\nAll 8 charts saved to eda_charts/")

# Save summary tables to CSV for the report
subs_by_region_sorted.to_csv("eda_charts/table_substations_by_region.csv", index=False)
top_utilities.to_csv("eda_charts/table_top_utilities.csv", index=False)
top_connected.to_csv("eda_charts/table_top_connected_substations.csv", index=False)
sub_numeric.describe().round(2).to_csv("eda_charts/table_substation_numeric_summary.csv")
lines_numeric.describe().round(2).to_csv("eda_charts/table_lines_numeric_summary.csv")

print("Summary tables saved to eda_charts/ as CSV")

