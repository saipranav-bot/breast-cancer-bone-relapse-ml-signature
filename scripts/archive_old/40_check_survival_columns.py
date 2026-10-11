import pandas as pd

clinical = pd.read_csv(
    "data/processed/GSE2034_clinical_metadata.csv"
)

print("Columns containing survival information:")
print()

for c in clinical.columns:
    if any(x in c.lower() for x in [
        "time",
        "month",
        "year",
        "survival",
        "relapse",
        "event",
        "status",
        "death",
        "follow"
    ]):
        print(c)

print("\nAll columns:")
print(list(clinical.columns))
