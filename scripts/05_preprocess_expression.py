import pandas as pd
import numpy as np
import os


input_file = "data/processed/GSE2034_expression_matrix.csv"

output_file = (
    "data/processed/"
    "GSE2034_expression_log2.csv"
)


print("Loading expression matrix...")

expr = pd.read_csv(
    input_file,
    index_col=0
)


print("Original shape:")
print(expr.shape)


# Log2 transformation

print("\nApplying log2 transformation...")

expr_log2 = np.log2(
    expr + 1
)


print("\nAfter transformation:")

print(expr_log2.head())


# Save

expr_log2.to_csv(
    output_file
)


print("\nSaved:")
print(output_file)
