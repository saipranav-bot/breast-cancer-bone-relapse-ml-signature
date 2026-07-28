import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# Load data
data = pd.read_csv(
    "data/processed/final_ML_clean.csv"
)


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


X = data[genes]
y = data["bone_relapse"]


print("Features:")
print(X.shape)

print("\nLabels:")
print(y.value_counts())


model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier",
     LogisticRegression(
         max_iter=1000,
         class_weight="balanced",
         random_state=42
     ))
])


cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


auc = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="roc_auc"
)


print("\n5 Fold CV ROC-AUC")
print("================")

print(auc)

print("\nMean AUC:")
print(round(auc.mean(),3))
