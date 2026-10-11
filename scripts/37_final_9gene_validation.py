import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import roc_auc_score, roc_curve


print("Loading expression...")

expr = pd.read_csv(
    "data/processed/GSE2034_expression_log2.csv",
    index_col=0
)

print("Expression shape:")
print(expr.shape)


# clean sample IDs
expr.columns = (
    expr.columns
    .astype(str)
    .str.replace('"', '', regex=False)
)


# labels

labels = pd.read_csv(
    "data/processed/GSE2034_labels.csv"
)

labels["sample_id"] = (
    labels["sample_id"]
    .astype(str)
    .str.replace('"', '', regex=False)
)


# annotation

anno = pd.read_csv(
    "results/tables/GPL96_clean_annotation.csv"
)

anno["Gene Symbol"] = (
    anno["Gene Symbol"]
    .astype(str)
    .str.strip()
)


# 9 gene signature

genes = [
    "TNFRSF11B",
    "IGLJ3",
    "IGLC1",
    "PP14571",
    "GPRC5A",
    "IGLL5",
    "IGHD",
    "IGLV1-44",
    "IGKC"
]


print("\nSearching genes...")


gene_data = []


for gene in genes:

    probes = anno[
        anno["Gene Symbol"] == gene
    ]["ID"].tolist()


    if len(probes) > 0:

        temp = expr.loc[
            expr.index.intersection(probes)
        ].mean(axis=0)


        temp.name = gene

        gene_data.append(temp)

    else:

        print("Missing:", gene)



gene_matrix = pd.DataFrame(gene_data).T


print("\nAvailable genes:")
print(list(gene_matrix.columns))

print("\nGene matrix:")
print(gene_matrix.shape)



# merge labels

gene_matrix["sample_id"] = gene_matrix.index


merged = gene_matrix.merge(
    labels,
    on="sample_id",
    how="inner"
)


print("\nMerged:")
print(merged.shape)



# coefficients

coef = pd.read_csv(
    "results/tables/9gene_signature_coefficients.csv"
)


coef_dict = dict(
    zip(
        coef["Gene"],
        coef["Coefficient"]
    )
)


merged["Risk_score"] = 0


for gene, weight in coef_dict.items():

    if gene in merged.columns:

        merged["Risk_score"] += (
            merged[gene] * weight
        )



# save scores FIRST

merged.to_csv(
    "results/tables/final_9gene_validation_scores.csv",
    index=False
)


print("\nScores saved")



# ROC

auc = roc_auc_score(
    merged["bone_relapse"],
    merged["Risk_score"]
)


print("\nFinal Validation")
print("================")
print("Samples:", len(merged))
print("ROC-AUC:", round(auc,3))


fpr, tpr, _ = roc_curve(
    merged["bone_relapse"],
    merged["Risk_score"]
)


plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC={auc:.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "9-Gene Signature Validation ROC"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/figures/final_9gene_validation_ROC.png",
    dpi=300
)

plt.close()



# Heatmap

available_genes = [
    g for g in genes
    if g in merged.columns
]


print("\nHeatmap genes:")
print(available_genes)


heat = merged[
    available_genes + ["bone_relapse"]
].copy()


heat = heat.sort_values(
    "bone_relapse"
)



plt.figure(figsize=(12,6))


sns.heatmap(
    heat[available_genes].T,
    cmap="vlag",
    xticklabels=False,
    yticklabels=True
)


plt.title(
    "9-Gene Signature Expression Heatmap"
)

plt.xlabel(
    "Samples"
)

plt.ylabel(
    "Genes"
)


plt.tight_layout()


plt.savefig(
    "results/figures/final_9gene_validation_heatmap.png",
    dpi=300
)


plt.close()



print("\nSaved:")
print("results/tables/final_9gene_validation_scores.csv")
print("results/figures/final_9gene_validation_ROC.png")
print("results/figures/final_9gene_validation_heatmap.png")

