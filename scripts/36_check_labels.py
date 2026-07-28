import pandas as pd

print("Loading labels...")

labels = pd.read_csv(
    "data/processed/GSE2034_labels.csv"
)

print("\nShape:")
print(labels.shape)

print("\nColumns:")
print(labels.columns)

print("\nFirst rows:")
print(labels.head())

print("\nClass distribution:")
print(labels.iloc[:,1].value_counts())
