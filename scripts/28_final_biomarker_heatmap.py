import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


print("Loading data...")


# expression dataset
data = pd.read_csv(
    "data/processed/final_ML_clean.csv",
    index_col=0
)


# consensus genes

genes = [
    "GPRC5A",
    "IGLV1-44",
    "TNFRSF11B",
    "IGKC",
    "PP14571",
    "IGLC1",
    "IGLL5",
    "IGLJ3",
    "IGHD"
]


# keep available genes

genes = [
    g for g in genes
    if g in data.columns
]


print("Genes used:")
print(genes)



# expression matrix

expr = data[genes]


# transpose for heatmap

expr = expr.T



# z-score each gene

expr_z = (
    expr
    .sub(expr.mean(axis=1), axis=0)
    .div(expr.std(axis=1), axis=0)
)



plt.figure(
    figsize=(12,6)
)


sns.heatmap(
    expr_z,
    cmap="RdBu_r",
    center=0,
    xticklabels=False,
    yticklabels=True
)



plt.title(
    "Consensus Biomarker Expression Heatmap"
)


plt.xlabel(
    "Samples"
)

plt.ylabel(
    "Genes"
)


plt.tight_layout()


plt.savefig(
    "results/final_biomarker_heatmap.png",
    dpi=300
)


print("\nSaved:")
print(
    "results/final_biomarker_heatmap.png"
)
