import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import os


print("Loading variance filtered dataset...")


data = pd.read_csv(
    "data/processed/GSE2034_variance_filtered.csv"
)


print(data.shape)


# Separate X and y

X = data.drop(
    columns=["bone_relapse"]
)

y = data["bone_relapse"]


# Split groups

relapse = X[y == 1]

no_relapse = X[y == 0]


print("\nRelapse samples:")
print(relapse.shape)

print("No relapse samples:")
print(no_relapse.shape)


results = []


print("\nRunning statistical tests...")


for gene in X.columns:

    stat, pvalue = ttest_ind(
        relapse[gene],
        no_relapse[gene],
        equal_var=False
    )

    log2fc = (
        relapse[gene].mean()
        -
        no_relapse[gene].mean()
    )

    results.append(
        [
            gene,
            log2fc,
            pvalue
        ]
    )


results = pd.DataFrame(
    results,
    columns=[
        "gene",
        "log2FC",
        "p_value"
    ]
)


# Multiple testing correction

results["adjusted_p"] = (
    results["p_value"]
    *
    len(results)
)


# Filter significant genes

selected = results[
    (results["adjusted_p"] < 0.05)
    &
    (abs(results["log2FC"]) > 0.5)
]


print("\nSignificant genes:")
print(selected.shape)


print(
    selected.head()
)


os.makedirs(
    "results",
    exist_ok=True
)


selected.to_csv(
    "results/selected_relapse_genes.csv",
    index=False
)


print("\nSaved:")
print(
    "results/selected_relapse_genes.csv"
)
