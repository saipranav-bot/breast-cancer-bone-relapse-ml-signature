import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


# =====================================
# Load dataset
# =====================================

print("Loading dataset...")

df = pd.read_csv(
    "data/processed/final_ML_clean.csv"
)

print("Original shape:")
print(df.shape)



# =====================================
# Remove unwanted columns
# =====================================

# Remove sample IDs and index columns

remove_cols = []

for col in df.columns:

    if (
        "sample" in col.lower()
        or "id" == col.lower()
        or "unnamed" in col.lower()
    ):
        remove_cols.append(col)


df = df.drop(
    columns=remove_cols,
    errors="ignore"
)



# =====================================
# Separate X and y
# =====================================

X = df.drop(
    columns=["bone_relapse"]
)

y = df["bone_relapse"]



# Keep only numeric gene expression columns

X = X.select_dtypes(
    include=["number"]
)


print("\nAfter cleaning:")

print("Features:")
print(X.shape)


print("\nLabels:")
print(y.value_counts())



# =====================================
# Cross validation
# =====================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)



# =====================================
# Logistic Regression
# =====================================

logistic = Pipeline(
    [
        (
            "scaler",
            StandardScaler()
        ),

        (
            "model",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)



logistic_auc = cross_val_score(
    logistic,
    X,
    y,
    cv=cv,
    scoring="roc_auc"
)



# =====================================
# Random Forest
# =====================================


rf = RandomForestClassifier(
    n_estimators=500,
    class_weight="balanced",
    random_state=42
)


rf_auc = cross_val_score(
    rf,
    X,
    y,
    cv=cv,
    scoring="roc_auc"
)



# =====================================
# Results
# =====================================

print("\n==============================")
print("5 Fold Cross Validation")
print("==============================")


print("\nLogistic Regression ROC-AUC:")

print(logistic_auc)

print(
    "Mean:",
    round(logistic_auc.mean(),3)
)



print("\nRandom Forest ROC-AUC:")

print(rf_auc)

print(
    "Mean:",
    round(rf_auc.mean(),3)
)
