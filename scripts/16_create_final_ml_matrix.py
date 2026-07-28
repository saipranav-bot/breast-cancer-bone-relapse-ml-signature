import pandas as pd
import os


print("Loading expression matrix...")

expression = pd.read_csv(
    "data/processed/GSE2034_expression_log2.csv",
    index_col=0
)


print("Expression shape:")
print(expression.shape)


print("\nLoading selected probes...")

selected = pd.read_csv(
    "results/selected_relapse_genes.csv"
)


probes = selected["gene"].tolist()


print("Number of selected probes:")
print(len(probes))


# Keep only selected probes

selected_expression = expression.loc[
    probes
]


print("\nSelected expression:")
print(selected_expression.shape)


# Transpose
# probes become columns
# patients become rows

ml_features = selected_expression.T


print("\nAfter transpose:")
print(ml_features.shape)


# Load annotation

annotation = pd.read_csv(
    "results/GPL96_clean_annotation.csv"
)


# Create mapping dictionary

probe_to_gene = dict(
    zip(
        annotation["ID"],
        annotation["Gene Symbol"]
    )
)


# Rename probes to gene symbols

ml_features.rename(
    columns=probe_to_gene,
    inplace=True
)


# Remove duplicate gene names

ml_features = (
    ml_features
    .loc[
        :,
        ~ml_features.columns.duplicated()
    ]
)


print("\nAfter gene mapping:")
print(ml_features.shape)


# Load labels

labels = pd.read_csv(
    "data/processed/GSE2034_labels.csv"
)


labels = labels.set_index(
    "sample_id"
)


# Remove quotes if present

labels.index = (
    labels.index
    .str.replace('"','')
)


# Merge

final = ml_features.merge(
    labels,
    left_index=True,
    right_index=True
)


print("\nFinal ML dataset:")
print(final.shape)


print("\nPreview:")
print(final.head())


os.makedirs(
    "data/processed",
    exist_ok=True
)


final.to_csv(
    "data/processed/final_ML_matrix.csv"
)


print("\nSaved:")
print(
    "data/processed/final_ML_matrix.csv"
)
