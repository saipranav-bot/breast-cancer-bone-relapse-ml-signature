import pandas as pd
import numpy as np
import os


print("Loading ML dataset...")


data = pd.read_csv(
    "data/processed/GSE2034_ML_dataset.csv"
)


print("Original dataset:")
print(data.shape)


# Separate features and labels

X = data.drop(
    columns=[
        "sample_id",
        "bone_relapse"
    ]
)

y = data["bone_relapse"]


print("\nExpression matrix:")
print(X.shape)


# Calculate variance of each gene

print("\nCalculating gene variance...")


variance = X.var(axis=0)


print("\nVariance summary:")
print(variance.describe())


# Select top variable genes

top_genes = (
    variance
    .sort_values(
        ascending=False
    )
    .head(2000)
    .index
)


X_filtered = X[top_genes]


print("\nAfter filtering:")
print(X_filtered.shape)


# Add labels back

final_data = X_filtered.copy()

final_data["bone_relapse"] = y


# Save

os.makedirs(
    "data/processed",
    exist_ok=True
)


final_data.to_csv(
    "data/processed/GSE2034_variance_filtered.csv",
    index=False
)


print("\nSaved:")
print(
    "data/processed/GSE2034_variance_filtered.csv"
)
