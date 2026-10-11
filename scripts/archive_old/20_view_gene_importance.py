import pandas as pd


importance = pd.read_csv(
    "results/tables/logistic_gene_importance.csv"
)


print("\nTop predictive genes")
print("===================")

print(
    importance.head(20)
)
