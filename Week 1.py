import pandas as pd 
import numpy as np 

utilities = pd.read_csv('utilities.csv') 
substations = pd.read_csv('substations.csv') 
lines = pd.read_csv('lines.csv')

print(substations.head())
print(lines.head())
print(utilities)

print(substations.isnull().sum())
print(lines.isnull().sum())
print(utilities.isnull().sum())

# Check for duplicates
print(utilities.duplicated().sum())

# Remove duplicates
utilities = utilities.drop_duplicates()

utilities.info()

# Remove duplicates
utilities = utilities.drop_duplicates()

# Remove extra spaces from text columns
for col in utilities.select_dtypes(include='object'):
    utilities[col] = utilities[col].str.strip()

# Standardize text
utilities['Country'] = utilities['Country'].str.title()
utilities['Code'] = utilities['Code'].str.upper()

# Check results
print(utilities.isnull().sum())
print("Duplicates:", utilities.duplicated().sum())
print(utilities.info())

# Number of records
print(len(utilities))

# Countries represented
print(utilities['Country'].value_counts())

# Utility types
print(utilities['Type'].value_counts())

# Active status
print(utilities['Active'].value_counts())