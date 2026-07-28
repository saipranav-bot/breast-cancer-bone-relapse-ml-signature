import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os


print("Loading dataset...")


data = pd.read_csv(
    "data/processed/final_ML_clean.csv",
    index_col=0
)


print("Dataset shape:")
print(data.shape)


# Separate features and label

X = data.drop(
    columns=["bone_relapse"]
)

y = data["bone_relapse"]


print("\nFeature matrix:")
print(X.shape)


print("\nLabels:")
print(y.value_counts())


# Ensure all features are numeric

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)


# Remove missing values if any

X = X.fillna(0)


# Train-test split

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


# Scaling

scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(
    X_train
)


X_test_scaled = scaler.transform(
    X_test
)


# Convert back to dataframe

X_train_scaled = pd.DataFrame(
    X_train_scaled,
    columns=X.columns
)


X_test_scaled = pd.DataFrame(
    X_test_scaled,
    columns=X.columns
)


os.makedirs(
    "data/ml",
    exist_ok=True
)


X_train_scaled.to_csv(
    "data/ml/X_train.csv",
    index=False
)


X_test_scaled.to_csv(
    "data/ml/X_test.csv",
    index=False
)


y_train.to_csv(
    "data/ml/y_train.csv",
    index=False
)


y_test.to_csv(
    "data/ml/y_test.csv",
    index=False
)


print("\nML files saved successfully")
