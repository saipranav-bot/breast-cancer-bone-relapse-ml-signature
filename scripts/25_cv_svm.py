import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


print("Loading dataset...")


data = pd.read_csv(
    "data/processed/final_ML_clean.csv"
)


# remove non-feature columns

if "Unnamed: 0" in data.columns:
    data = data.drop(
        columns=["Unnamed: 0"]
    )


X = data.drop(
    columns=["bone_relapse"]
)

y = data["bone_relapse"]


# convert numeric

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.fillna(0)



print("Features:")
print(X.shape)


print("\nLabels:")
print(y.value_counts())



# model

svm_model = Pipeline(
    [
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
    ]
)



cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)



auc = cross_val_score(
    svm_model,
    X,
    y,
    cv=cv,
    scoring="roc_auc"
)



print("\n==============================")
print("5 Fold Cross Validation")
print("==============================")


print("\nSVM ROC-AUC:")
print(auc)


print(
    "Mean:",
    round(
        auc.mean(),
        3
    )
)
