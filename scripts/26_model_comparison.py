import matplotlib.pyplot as plt
import pandas as pd


models = [
    "Logistic Regression",
    "Random Forest",
    "SVM"
]


auc_values = [
    0.676,
    0.648,
    0.641
]


results = pd.DataFrame(
    {
        "Model": models,
        "ROC_AUC": auc_values
    }
)


print(results)



plt.figure(figsize=(7,5))


plt.bar(
    results["Model"],
    results["ROC_AUC"]
)


plt.ylabel(
    "Mean 5-fold ROC-AUC"
)


plt.xlabel(
    "Machine Learning Model"
)


plt.title(
    "Model Performance Comparison"
)


plt.ylim(
    0,
    1
)


plt.xticks(
    rotation=45,
    ha="right"
)


for i, v in enumerate(auc_values):
    plt.text(
        i,
        v+0.02,
        str(round(v,3)),
        ha="center"
    )


plt.tight_layout()


plt.savefig(
    "results/model_comparison.png",
    dpi=300
)


print("\nSaved:")
print("results/model_comparison.png")
