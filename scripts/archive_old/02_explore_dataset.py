import GEOparse
import pandas as pd
import os

# Load dataset
gse = GEOparse.get_GEO(
    geo="GSE2034",
    destdir="data/raw/",
    silent=True,
    how="quick"
)

print(gse)

# Number of samples
print("\nNumber of samples:")
print(len(gse.gsms))


# View first sample
sample = list(gse.gsms.values())[0]

print("\nFirst sample table:")
print(sample.table.head())


# Create expression matrix

expression = {}

for sample_id, sample in gse.gsms.items():
    expression[sample_id] = (
        sample.table
        .set_index("ID_REF")["VALUE"]
    )

expression_df = pd.DataFrame(expression)


print("\nExpression matrix:")
print(expression_df.head())


print("\nMatrix dimensions:")
print(expression_df.shape)


# Save matrix

os.makedirs("data/processed", exist_ok=True)

expression_df.to_csv(
    "data/processed/GSE2034_expression.csv"
)

print("\nSaved successfully")
