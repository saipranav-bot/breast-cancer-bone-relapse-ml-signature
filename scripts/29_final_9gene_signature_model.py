import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    roc_curve
)


# ============================
# Load data
# ============================

print("Loading dataset...")

data = pd.read_csv("data/processed/final_ML_clean.csv")

# Target
target = "bone_relapse"


# Consensus biomarkers
genes = [
    "GPRC5A",
    "IGLV1-44",
    "TNFRSF11B",
    "IGKC",
    "PP14571",
    "IGLC1",
    "IGLL5",
    "IGLJ3",
    "IGHD"
]


# Check genes
available = [
    g for g in genes if g in data.columns
]

print("\nGenes used:")
print(available)


X = data[available]

y = data[target]


print("\nFeature matrix:")
print(X.shape)


print("\nLabels:")
print(y.value_counts())


# ============================
# Train test split
# ============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================
# Logistic regression model
# ============================

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier",
     LogisticRegression(
         max_iter=1000,
         class_weight="balanced",
         random_state=42
     ))
])


print("\nTraining 9-gene signature model...")

model.fit(
    X_train,
    y_train
)


# Predictions

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:,1]


# ============================
# Results
# ============================

print("\nResults")
print("================")

print(
    "Accuracy:",
    accuracy_score(y_test,pred)
)

print(
    "ROC-AUC:",
    roc_auc_score(y_test,prob)
)


print("\nClassification Report")

print(
    classification_report(
        y_test,
        pred
    )
)


# ============================
# ROC curve
# ============================

fpr,tpr,_ = roc_curve(
    y_test,
    prob
)

plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC={roc_auc_score(y_test,prob):.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "9-Gene Biomarker Signature ROC"
)

plt.legend()

plt.savefig(
    "results/figures/9gene_signature_ROC.png",
    dpi=300,
    bbox_inches="tight"
)


# ============================
# Save coefficients
# ============================

coef = pd.DataFrame({

    "Gene": available,

    "Coefficient":
    model.named_steps["classifier"].coef_[0]

})


coef["Absolute_effect"] = (
    coef["Coefficient"]
    .abs()
)


coef = coef.sort_values(
    "Absolute_effect",
    ascending=False
)


coef.to_csv(
    "results/tables/9gene_signature_coefficients.csv",
    index=False
)


print("\nSaved:")
print("results/figures/9gene_signature_ROC.png")
print("results/tables/9gene_signature_coefficients.csv")
