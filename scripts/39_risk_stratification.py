import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


print("Loading validation scores...")


data = pd.read_csv(
    "results/tables/final_9gene_validation_scores.csv"
)


print(data.head())


# ============================
# Define risk groups
# ============================

median_score = data["Risk_score"].median()

data["Risk_group"] = np.where(
    data["Risk_score"] >= median_score,
    "High risk",
    "Low risk"
)


print("\nRisk group distribution")
print(data["Risk_group"].value_counts())


print("\nRelapse distribution")
print(
    pd.crosstab(
        data["Risk_group"],
        data["bone_relapse"]
    )
)


# save stratified table

data.to_csv(
    "results/tables/9gene_risk_stratification.csv",
    index=False
)


# ============================
# Improved risk score plot
# ============================

plt.figure(figsize=(10,7))


sns.histplot(
    data=data,
    x="Risk_score",
    hue="Risk_group",
    bins=25,
    kde=True,
    alpha=0.6
)


plt.axvline(
    median_score,
    linestyle="--",
    linewidth=2,
    label=f"Median = {median_score:.3f}"
)


plt.xlabel(
    "9-Gene Signature Risk Score",
    fontsize=14
)

plt.ylabel(
    "Number of Patients",
    fontsize=14
)


plt.title(
    "Distribution of 9-Gene Signature Risk Scores",
    fontsize=16,
    fontweight="bold"
)


plt.legend(
    title="Risk Group"
)


plt.tight_layout()


plt.savefig(
    "results/figures/9gene_risk_score_distribution.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# ============================
# Boxplot
# ============================

plt.figure(figsize=(8,6))


sns.boxplot(
    data=data,
    x="Risk_group",
    y="Risk_score"
)


sns.stripplot(
    data=data,
    x="Risk_group",
    y="Risk_score",
    alpha=0.5
)


plt.title(
    "Risk Score Distribution by Patient Group",
    fontsize=15,
    fontweight="bold"
)


plt.xlabel("")
plt.ylabel(
    "Risk Score",
    fontsize=13
)


plt.tight_layout()


plt.savefig(
    "results/figures/9gene_risk_group_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print("\nSaved:")
print("results/figures/9gene_risk_score_distribution.png")
print("results/figures/9gene_risk_group_boxplot.png")
print("results/tables/9gene_risk_stratification.csv")

