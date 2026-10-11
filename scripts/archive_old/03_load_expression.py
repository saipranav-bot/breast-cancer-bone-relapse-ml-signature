import GEOparse
import pandas as pd
import os


gse = GEOparse.get_GEO(
    geo="GSE2034",
    destdir="data/raw/",
    silent=False
)


print(gse)


# Get GPL platform data
platform = list(gse.gpls.values())[0]

print("\nPlatform:")
print(platform)


# Extract expression from samples

expression = {}

for sample_id, sample in gse.gsms.items():

    table = sample.table

    expression[sample_id] = (
        table
        .set_index("ID_REF")["VALUE"]
    )


expression_df = pd.DataFrame(expression)


print("\nShape:")
print(expression_df.shape)


print(expression_df.head())


os.makedirs(
    "data/processed",
    exist_ok=True
)

expression_df.to_csv(
    "data/processed/GSE2034_expression_full.csv"
)
