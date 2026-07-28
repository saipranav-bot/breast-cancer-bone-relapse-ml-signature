import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    roc_curve
)

import matplotlib.pyplot as plt


print("Loading ML data...")

data = pd.read_csv(
    "data/processed/final_ML_clean.csv"
)


# remove sample IDs if present
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"])


print("Dataset:")
print(data.shape)


# separate features and label

X = data.drop(
    columns=["bone_relapse"]
)

y = data["bone_relapse"]


# ensure numeric

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.fillna(0)


print("\nFeatures:")
print(X.shape)


print("\nLabels:")
print(y.value_counts())


# split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\nTraining:")
print(X_train.shape)

print("Testing:")
print(X_test.shape)



# SVM model

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "svm",
        SVC(
            kernel="linear",
            probability=True,
            class_weight="balanced",
            random_state=42
        )
    )
])


print("\nTraining SVM...")

model.fit(
    X_train,
    y_train
)



# prediction

y_pred = model.predict(
    X_test
)

y_prob = model.predict_proba(
    X_test
)[:,1]



# metrics

print("\nResults")
print("================")

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred
    )
)


print(
    "ROC-AUC:",
    roc_auc_score(
        y_test,
        y_prob
    )
)


print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred
    )
)



# ROC curve

fpr, tpr, _ = roc_curve(
    y_test,
    y_prob
)


plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC={roc_auc_score(y_test,y_prob):.3f}"
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
    "SVM ROC Curve"
)

plt.legend()

plt.tight_layout()


plt.savefig(
    "results/svm_ROC.png",
    dpi=300
)


# gene coefficients

coef = model.named_steps["svm"].coef_[0]


importance = pd.DataFrame(
    {
        "Gene":X.columns,
        "Coefficient":coef,
        "Absolute_effect":abs(coef)
    }
)


importance = importance.sort_values(
    "Absolute_effect",
    ascending=False
)


importance.to_csv(
    "results/svm_gene_importance.csv",
    index=False
)


print("\nTop predictive genes")

print(
    importance.head(20)
)


print("\nSaved:")
print("results/svm_ROC.png")
print("results/svm_gene_importance.csv")
