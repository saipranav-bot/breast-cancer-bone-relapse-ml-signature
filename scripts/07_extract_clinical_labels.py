import pandas as pd
import os


file = "data/raw/GSE2034_series_matrix.txt"


print("Reading GEO clinical metadata...")


clinical_lines = []


with open(file, "r") as f:

    for line in f:

        if line.startswith("!Sample_"):

            clinical_lines.append(line.strip())


print("\nNumber of metadata lines:")
print(len(clinical_lines))


# Convert metadata into dataframe

metadata = {}

for line in clinical_lines:

    parts = line.split("\t")

    key = parts[0]

    values = parts[1:]

    metadata[key] = values



clinical = pd.DataFrame(metadata)


print("\nClinical metadata shape:")
print(clinical.shape)


print("\nAvailable metadata:")
print(clinical.columns.tolist())


print("\nFirst rows:")
print(clinical.head())


os.makedirs(
    "data/processed",
    exist_ok=True
)


clinical.to_csv(
    "data/processed/GSE2034_clinical_metadata.csv",
    index=False
)


print("\nSaved:")
print(
    "data/processed/GSE2034_clinical_metadata.csv"
)
