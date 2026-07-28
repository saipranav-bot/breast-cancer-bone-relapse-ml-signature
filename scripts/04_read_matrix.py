import pandas as pd
import os


# ==============================
# File paths
# ==============================

input_file = "data/raw/GSE2034_series_matrix.txt"

output_dir = "data/processed"

output_file = (
    "data/processed/"
    "GSE2034_expression_matrix.csv"
)


# ==============================
# Check input file
# ==============================

if not os.path.exists(input_file):
    raise FileNotFoundError(
        f"File not found: {input_file}"
    )


print("Reading GEO expression matrix...")


# ==============================
# Read expression matrix
# ==============================

expr = pd.read_csv(
    input_file,
    sep="\t",
    comment="!",
    index_col=0
)


# Remove empty columns if present

expr = expr.dropna(
    axis=1,
    how="all"
)


# Remove duplicate probes if present

expr = expr[~expr.index.duplicated(
    keep="first"
)]


# ==============================
# Dataset information
# ==============================

print("\n==============================")
print("Dataset information")
print("==============================")

print(
    "Number of genes/probes:",
    expr.shape[0]
)

print(
    "Number of samples:",
    expr.shape[1]
)


# ==============================
# Display data
# ==============================

print("\nFirst 5 genes:")

print(
    expr.head()
)


print("\nFirst 5 samples:")

print(
    expr.columns[:5]
)


# ==============================
# Expression statistics
# ==============================

print("\nExpression statistics:")

print(
    expr.describe().iloc[:5, :5]
)


# ==============================
# Save processed matrix
# ==============================

os.makedirs(
    output_dir,
    exist_ok=True
)


expr.to_csv(
    output_file
)


print("\n==============================")
print("Saved successfully")
print("==============================")

print(
    output_file
)
