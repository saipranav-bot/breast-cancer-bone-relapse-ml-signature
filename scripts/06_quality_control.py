import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os


# Load log2 expression

expr = pd.read_csv(
    "data/processed/GSE2034_expression_log2.csv",
    index_col=0
)


print("Expression shape:")
print(expr.shape)


# Transpose
# ML format:
# rows = samples
# columns = genes

X = expr.T


print("\nML matrix:")
print(X.shape)


# ==========================
# Expression distribution
# ==========================

plt.figure(figsize=(10,6))

plt.hist(
    X.values.flatten(),
    bins=100
)

plt.xlabel("Log2 expression")
plt.ylabel("Frequency")
plt.title(
    "GSE2034 Expression Distribution"
)

os.makedirs(
    "results",
    exist_ok=True
)

plt.savefig(
    "results/expression_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================
# PCA
# ==========================


print("\nRunning PCA...")


# scale genes

X_scaled = StandardScaler().fit_transform(X)


pca = PCA(
    n_components=2
)

pca_result = pca.fit_transform(
    X_scaled
)


pca_df = pd.DataFrame(
    pca_result,
    columns=[
        "PC1",
        "PC2"
    ]
)


plt.figure(figsize=(8,6))

plt.scatter(
    pca_df["PC1"],
    pca_df["PC2"]
)

plt.xlabel(
    f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)"
)

plt.ylabel(
    f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)"
)

plt.title(
    "PCA of GSE2034 Breast Cancer Samples"
)


plt.savefig(
    "results/PCA_GSE2034.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nPCA completed")
print(
    "Variance explained:",
    pca.explained_variance_ratio_
)
