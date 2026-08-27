import pandas as pd

# ---------------------------------------------------------
# TASK 1.3: DATA INTEGRATION & RELATIONSHIP MAPPING
# ---------------------------------------------------------

# Load datasets
utilities = pd.read_csv("utilities.csv")
substations = pd.read_csv("substations.csv")
lines = pd.read_csv("lines.csv")

print("Datasets loaded successfully.")

print("\nNumber of records:")
print("Utilities:", len(utilities))
print("Substations:", len(substations))
print("Lines:", len(lines))


# ---------------------------------------------------------
# 1. CHECK DATASET COLUMNS
# ---------------------------------------------------------

print("\nUtilities columns:")
print(utilities.columns.tolist())

print("\nSubstations columns:")
print(substations.columns.tolist())

print("\nLines columns:")
print(lines.columns.tolist())


# ---------------------------------------------------------
# 2. CHECK FOR DUPLICATES
# ---------------------------------------------------------

print("\nDuplicate records:")
print("Utilities:", utilities.duplicated().sum())
print("Substations:", substations.duplicated().sum())
print("Lines:", lines.duplicated().sum())


# ---------------------------------------------------------
# 3. CHECK FOR MISSING VALUES
# ---------------------------------------------------------

print("\nMissing values:")

print("\nUtilities:")
print(utilities.isnull().sum())

print("\nSubstations:")
print(substations.isnull().sum())

print("\nLines:")
print(lines.isnull().sum())


# ---------------------------------------------------------
# 4. RELATIONSHIP: UTILITY → TRANSMISSION LINE
# ---------------------------------------------------------

valid_utility_ids = set(utilities["Utility ID"])

invalid_line_utilities = lines[
    ~lines["Utility ID"].isin(valid_utility_ids)
]

print("\nUtility → Line relationship")

print(
    "Invalid utility references:",
    len(invalid_line_utilities)
)

if len(invalid_line_utilities) == 0:
    print("All transmission lines reference valid utilities.")
else:
    print(invalid_line_utilities)


# ---------------------------------------------------------
# 5. RELATIONSHIP: SUBSTATION → TRANSMISSION LINE
# ---------------------------------------------------------

valid_substation_ids = set(substations["Substation ID"])

invalid_source_ids = lines[
    ~lines["Source Substation ID"].isin(valid_substation_ids)
]

invalid_destination_ids = lines[
    ~lines["Destination Substation ID"].isin(valid_substation_ids)
]

print("\nSubstation → Line relationships")

print(
    "Invalid source substation references:",
    len(invalid_source_ids)
)

print(
    "Invalid destination substation references:",
    len(invalid_destination_ids)
)

if len(invalid_source_ids) == 0:
    print("All source substations are valid.")

if len(invalid_destination_ids) == 0:
    print("All destination substations are valid.")


# ---------------------------------------------------------
# 6. INTEGRATE UTILITY INFORMATION WITH LINES
# ---------------------------------------------------------

lines_integrated = lines.merge(
    utilities[
        [
            "Utility ID",
            "Name",
            "Alias",
            "Code",
            "Type",
            "Country",
            "Active"
        ]
    ],
    on="Utility ID",
    how="left",
    suffixes=("", " Utility")
)

# Rename utility name for clarity
lines_integrated = lines_integrated.rename(
    columns={
        "Name": "Utility Name",
        "Alias": "Utility Alias",
        "Code": "Utility Code",
        "Type": "Utility Type",
        "Country": "Utility Country",
        "Active": "Utility Active"
    }
)


# ---------------------------------------------------------
# 7. ADD SOURCE SUBSTATION INFORMATION
# ---------------------------------------------------------

source_substations = substations.copy()

source_substations = source_substations.rename(
    columns={
        "Substation ID": "Source Substation ID",
        "Name": "Source Substation Name",
        "Short Name": "Source Short Name",
        "Region": "Source Region",
        "Country": "Source Country",
        "Latitude": "Source Latitude",
        "Longitude": "Source Longitude",
        "Voltage (kV)": "Source Voltage (kV)",
        "Capacity (MVA)": "Source Capacity (MVA)",
        "Commissioning Year": "Source Commissioning Year",
        "Type": "Source Type",
        "Status": "Source Status"
    }
)

lines_integrated = lines_integrated.merge(
    source_substations,
    on="Source Substation ID",
    how="left"
)


# ---------------------------------------------------------
# 8. ADD DESTINATION SUBSTATION INFORMATION
# ---------------------------------------------------------

destination_substations = substations.copy()

destination_substations = destination_substations.rename(
    columns={
        "Substation ID": "Destination Substation ID",
        "Name": "Destination Substation Name",
        "Short Name": "Destination Short Name",
        "Region": "Destination Region",
        "Country": "Destination Country",
        "Latitude": "Destination Latitude",
        "Longitude": "Destination Longitude",
        "Voltage (kV)": "Destination Voltage (kV)",
        "Capacity (MVA)": "Destination Capacity (MVA)",
        "Commissioning Year": "Destination Commissioning Year",
        "Type": "Destination Type",
        "Status": "Destination Status"
    }
)

lines_integrated = lines_integrated.merge(
    destination_substations,
    on="Destination Substation ID",
    how="left"
)


# ---------------------------------------------------------
# 9. DISPLAY INTEGRATED DATASET
# ---------------------------------------------------------

print("\nIntegrated dataset:")
print(lines_integrated.head())

print("\nIntegrated dataset shape:")
print(lines_integrated.shape)


# ---------------------------------------------------------
# 10. CHECK INTEGRATION RESULTS
# ---------------------------------------------------------

print("\nIntegration checks:")

print(
    "Missing utility names:",
    lines_integrated["Utility Name"].isnull().sum()
)

print(
    "Missing source substations:",
    lines_integrated["Source Substation Name"].isnull().sum()
)

print(
    "Missing destination substations:",
    lines_integrated["Destination Substation Name"].isnull().sum()
)


# ---------------------------------------------------------
# 11. RELATIONSHIP SUMMARY
# ---------------------------------------------------------

relationship_summary = pd.DataFrame({
    "Relationship": [
        "Utility → Line",
        "Substation → Line (Source)",
        "Substation → Line (Destination)"
    ],
    "Invalid References": [
        len(invalid_line_utilities),
        len(invalid_source_ids),
        len(invalid_destination_ids)
    ]
})

print("\nRelationship summary:")
print(relationship_summary)


# ---------------------------------------------------------
# 12. SAVE RESULTS
# ---------------------------------------------------------

lines_integrated.to_csv(
    "task_1_3_integrated_data.csv",
    index=False
)

relationship_summary.to_csv(
    "task_1_3_relationship_summary.csv",
    index=False
)

print("\nFiles created:")
print("task_1_3_integrated_data.csv")
print("task_1_3_relationship_summary.csv")

print("\nTASK 1.3 COMPLETED SUCCESSFULLY.")