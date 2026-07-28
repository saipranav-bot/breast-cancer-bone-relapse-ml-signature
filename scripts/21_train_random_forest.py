import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    roc_curve
)


print("Loading ML data...")


# Load train/test data

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



# Random Forest model

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=5,
    class_weight="balanced",
    random_state=42
)


print("\nTraining Random Forest...")


model.fit(
    X_train,
    y_train
)



# Predictions

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
    "Random Forest ROC Curve"
)


plt.legend()

plt.grid()


plt.savefig(
    "results/random_forest_ROC.png",
    dpi=300,
    bbox_inches="tight"
)



# Feature importance

importance = pd.DataFrame(
    {
        "Gene": X_train.columns,
        "Importance": model.feature_importances_
    }
)


importance = importance.sort_values(
    "Importance",
    ascending=False
)


importance.to_csv(
    "results/random_forest_gene_importance.csv",
    index=False
)



print("\nSaved:")
print("results/random_forest_ROC.png")
print("results/random_forest_gene_importance.csv")
