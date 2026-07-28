import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    roc_curve
)


print("Loading ML data...")


X_train = pd.read_csv(
    "data/ml/X_train.csv"
)

X_test = pd.read_csv(
    "data/ml/X_test.csv"
)


y_train = pd.read_csv(
    "data/ml/y_train.csv"
)["bone_relapse"]


y_test = pd.read_csv(
    "data/ml/y_test.csv"
)["bone_relapse"]


print("Training:")
print(X_train.shape)

print("Testing:")
print(X_test.shape)


# Model

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)


print("\nTraining Logistic Regression...")


model.fit(
    X_train,
    y_train
)


# Prediction

y_pred = model.predict(
    X_test
)


y_prob = model.predict_proba(
    X_test
)[:,1]


# Evaluation

accuracy = accuracy_score(
    y_test,
    y_pred
)


auc = roc_auc_score(
    y_test,
    y_prob
)


print("\nResults")
print("================")
print("Accuracy:", accuracy)
print("ROC-AUC:", auc)


print("\nClassification Report")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# ROC curve

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_prob
)


plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC={auc:.3f}"
)


plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "Logistic Regression ROC Curve"
)

plt.legend()

plt.grid()


plt.savefig(
    "results/logistic_ROC.png",
    dpi=300,
    bbox_inches="tight"
)


# Gene importance

importance = pd.DataFrame(
    {
        "Gene": X_train.columns,
        "Coefficient": model.coef_[0]
    }
)


importance["Absolute_effect"] = (
    importance["Coefficient"]
    .abs()
)


importance = importance.sort_values(
    "Absolute_effect",
    ascending=False
)


importance.to_csv(
    "results/logistic_gene_importance.csv",
    index=False
)


print("\nSaved:")
print("results/logistic_ROC.png")
print("results/logistic_gene_importance.csv")
