import pandas as pd
import os


print("Loading expression matrix...")


# Load log2 expression matrix
expr = pd.read_csv(
    "data/processed/GSE2034_expression_log2.csv",
    index_col=0
)


print("Expression shape:")
print(expr.shape)


print("\nLoading labels...")


labels = pd.read_csv(
    "data/processed/GSE2034_labels.csv"
)


print(labels.head())


# Remove quotes from sample IDs
labels["sample_id"] = (
    labels["sample_id"]
    .str.replace('"', '')
)


# Expression samples are columns
# Transpose expression:
# genes become columns
# patients become rows

expr_ml = expr.T


print("\nAfter transpose:")
print(expr_ml.shape)


print("\nFirst samples:")
print(expr_ml.head())


# Rename index for merging

expr_ml.index.name = "sample_id"


# Merge expression and labels

print("\nMerging expression with clinical labels...")


ml_data = expr_ml.merge(
    labels,
    on="sample_id",
    how="inner"
)


print("\nFinal ML dataset:")
print(ml_data.shape)


print("\nPreview:")
print(ml_data.iloc[:, :5].head())


print("\nClass distribution:")
print(
    ml_data["bone_relapse"].value_counts()
)


# Create output folder

os.makedirs(
    "data/processed",
    exist_ok=True
)


# Save final dataset

ml_data.to_csv(
    "data/processed/GSE2034_ML_dataset.csv",
    index=False
)


print("\nSaved:")
print(
    "data/processed/GSE2034_ML_dataset.csv"
)
