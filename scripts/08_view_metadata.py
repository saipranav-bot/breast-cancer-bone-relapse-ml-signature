import pandas as pd


file = "data/processed/GSE2034_clinical_metadata.csv"


# Load metadata

clinical = pd.read_csv(file)


print("==============================")
print("Metadata dimensions")
print("==============================")

print(clinical.shape)


print("\n==============================")
print("Metadata columns")
print("==============================")

for col in clinical.columns:
    print(col)


print("\n==============================")
print("First 5 samples")
print("==============================")

pd.set_option(
    "display.max_columns",
    None
)

print(
    clinical.head()
)
