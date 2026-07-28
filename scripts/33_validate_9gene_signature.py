import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


print("Loading data...")


# ==========================
# Load expression matrix
# ==========================

expr = pd.read_csv(
    "data/processed/GSE2034_expression_log2.csv",
    index_col=0
)


# ==========================
# Load labels
# ==========================

labels = pd.read_csv(
    "data/processed/GSE2034_labels.csv"
)


# ==========================
# Load signature coefficients
# ==========================

coef = pd.read_csv(
    "results/9gene_signature_coefficients.csv"
)


genes = coef["Gene"].tolist()


print("\nSignature genes:")
print(genes)



# ==========================
# Load GPL96 annotation
# ==========================

anno = pd.read_csv(
    "results/GPL96_clean_annotation.csv"
)


print("\nAnnotation columns:")
print(anno.columns)


# probe -> gene symbol

probe_col = "ID"
gene_col = "Gene Symbol"


probe_to_gene = dict(
    zip(
        anno[probe_col],
        anno[gene_col]
    )
)



# ==========================
# Convert probe IDs to genes
# ==========================

expr_gene = expr.copy()


expr_gene["Gene"] = (
    expr_gene.index
    .map(probe_to_gene)
)


# remove unmapped probes

expr_gene = expr_gene.dropna(
    subset=["Gene"]
)



# remove duplicate probes
# average expression

expr_gene = (
    expr_gene
    .groupby("Gene")
    .mean()
)


print("\nGene level matrix:")
print(expr_gene.shape)



# ==========================
# Select signature genes
# ==========================

available_genes = [
    g for g in genes
    if g in expr_gene.index
]


print("\nAvailable signature genes:")
print(available_genes)


if len(available_genes) < 5:
    raise Exception(
        "Too few genes mapped"
    )



X = (
    expr_gene
    .loc[available_genes]
    .T
)



print("\nFeature matrix:")
print(X.shape)



# ==========================
# Calculate risk score
# ==========================


coef_dict = dict(
    zip(
        coef["Gene"],
        coef["Coefficient"]
    )
)



risk_score = np.zeros(
    X.shape[0]
)



for gene in available_genes:

    risk_score += (
        X[gene]
        *
        coef_dict[gene]
    )



risk = pd.DataFrame({

    "sample_id":
    X.index,

    "Risk_score":
    risk_score

})



# ==========================
# Clean sample IDs
# ==========================

risk["sample_id"] = (
    risk["sample_id"]
    .astype(str)
    .str.replace('"',"")
    .str.strip()
)



labels["sample_id"] = (
    labels["sample_id"]
    .astype(str)
    .str.replace('"',"")
    .str.strip()
)



print("\nExpression IDs:")
print(risk["sample_id"].head())


print("\nLabel IDs:")
print(labels["sample_id"].head())



# ==========================
# Merge labels
# ==========================

risk = risk.merge(
    labels,
    how="inner",
    on="sample_id"
)



print("\nAfter merge:")
print(risk.shape)

print(risk.head())



if risk.shape[0] == 0:
    raise Exception(
        "No samples matched. Check sample IDs."
    )



# ==========================
# High / Low risk groups
# ==========================

median_score = (
    risk["Risk_score"]
    .median()
)


risk["Risk_group"] = np.where(
    risk["Risk_score"] >= median_score,
    "High",
    "Low"
)



print(
    risk["Risk_group"]
    .value_counts()
)



# save scores

risk.to_csv(
    "results/9gene_risk_scores.csv",
    index=False
)



# ==========================
# Risk score boxplot
# ==========================

plt.figure(
    figsize=(7,5)
)


sns.boxplot(
    data=risk,
    x="bone_relapse",
    y="Risk_score"
)


plt.title(
    "9-Gene Signature Risk Score"
)


plt.savefig(
    "results/9gene_risk_score_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# ==========================
# Validation heatmap
# ==========================


heat = X.copy()


heat["Risk_group"] = (
    risk
    .set_index("sample_id")
    .loc[heat.index]["Risk_group"]
)



heat = heat.sort_values(
    "Risk_group"
)



plt.figure(
    figsize=(12,6)
)


sns.heatmap(
    heat.drop(
        columns="Risk_group"
    ).T,
    cmap="RdBu_r",
    center=0
)


plt.title(
    "9-Gene Signature Validation Heatmap"
)


plt.savefig(
    "results/9gene_validation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



print("\nSaved:")
print("results/9gene_risk_scores.csv")
print("results/9gene_risk_score_boxplot.png")
print("results/9gene_validation_heatmap.png")

