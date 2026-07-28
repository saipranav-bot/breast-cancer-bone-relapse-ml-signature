import pandas as pd
import re


print("Loading final ML matrix...")


data = pd.read_csv(
    "data/processed/final_ML_matrix.csv",
    index_col=0
)


print("Original shape:")
print(data.shape)


# Clean column names

clean_columns = []

for col in data.columns:

    if col == "bone_relapse":
        clean_columns.append(col)

    else:
        col = col.split("///")[0]
        col = col.strip()
        clean_columns.append(col)


data.columns = clean_columns


# Remove duplicate columns

data = data.loc[
    :,
    ~data.columns.duplicated()
]


print("\nAfter cleaning:")
print(data.shape)


print("\nColumns:")
print(list(data.columns))


data.to_csv(
    "data/processed/final_ML_clean.csv"
)


print("\nSaved:")
print(
    "data/processed/final_ML_clean.csv"
)
