import pandas as pd


clinical = pd.read_csv(
    "data/processed/GSE2034_clinical_metadata.csv"
)


chars = clinical[
    "!Sample_characteristics_ch1"
]


print("Unique clinical fields:\n")


fields = set()


for item in chars:

    text = item.replace('"','')

    key = text.split(":")[0]

    fields.add(key)


for f in sorted(fields):
    print(f)
