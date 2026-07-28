import pandas as pd


importance = pd.read_csv(
    "results/random_forest_gene_importance.csv"
)


print("\nTop Random Forest predictive genes")
print("===============================")


print(
    importance.head(20)
)
