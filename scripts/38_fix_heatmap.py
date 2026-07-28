import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv(
    "results/final_9gene_validation_scores.csv"
)


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


available = [
    g for g in genes
    if g in data.columns
]


print("Available genes:")
print(available)


heat = data[
    available + ["bone_relapse"]
].copy()


heat = heat.sort_values(
    "bone_relapse"
)


plt.figure(figsize=(12,6))


sns.heatmap(
    heat[available].T,
    cmap="vlag",
    xticklabels=False,
    yticklabels=True
)


plt.title(
    "Validation Heatmap of 9-Gene Signature\n(Platform detectable genes)"
)


plt.xlabel("Samples")
plt.ylabel("Genes")


plt.tight_layout()


plt.savefig(
    "results/final_validation_heatmap_fixed.png",
    dpi=300
)


plt.close()


print("Saved:")
print("results/final_validation_heatmap_fixed.png")
