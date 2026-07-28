import pandas as pd
import os


clinical = pd.read_csv(
    "data/processed/GSE2034_clinical_metadata.csv"
)


# Extract sample IDs

samples = clinical[
    "!Sample_geo_accession"
]


# Extract relapse values

labels = []

for x in clinical[
    "!Sample_characteristics_ch1"
]:

    value = int(
        x.split(":")[1]
        .replace('"',"")
        .strip()
    )

    labels.append(value)


label_df = pd.DataFrame(
    {
        "sample_id": samples,
        "bone_relapse": labels
    }
)


print(label_df.head())


print("\nClass distribution:")
print(
    label_df["bone_relapse"].value_counts()
)


os.makedirs(
    "data/processed",
    exist_ok=True
)


label_df.to_csv(
    "data/processed/GSE2034_labels.csv",
    index=False
)


print("\nSaved:")
print(
    "data/processed/GSE2034_labels.csv"
)
