import pandas as pd


print("Loading clinical metadata...")


clinical = pd.read_csv(
    "data/processed/GSE2034_clinical_metadata.csv"
)


print("\nShape:")
print(clinical.shape)


print("\nColumns:")
for c in clinical.columns:
    print(c)


print("\nFirst rows:")
print(clinical.head())

