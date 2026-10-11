import pandas as pd
import GEOparse
import os


print("Downloading GPL96 annotation...")


gpl = GEOparse.get_GEO(
    "GPL96",
    destdir="data/raw"
)


print("Annotation loaded")


# GPL table

annotation = gpl.table


print(annotation.head())


print(annotation.columns)


# Load selected probes

sig = pd.read_csv(
    "results/tables/selected_relapse_genes.csv"
)


probes = sig["gene"]


# Find matching probes

mapped = annotation[
    annotation["ID"].isin(probes)
]


print("\nMapped probes:")
print(mapped.head())


print("\nNumber mapped:")
print(mapped.shape)


# Keep useful columns

mapped = mapped[
    [
        "ID",
        "Gene Symbol",
        "Gene Title"
    ]
]


mapped.to_csv(
    "results/tables/GPL96_clean_annotation.csv",
    index=False
)


print("\nSaved:")
print(
    "results/tables/GPL96_clean_annotation.csv"
)
