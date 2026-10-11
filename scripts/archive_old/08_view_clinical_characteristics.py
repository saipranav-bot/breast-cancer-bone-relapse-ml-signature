import pandas as pd


file = "data/processed/GSE2034_clinical_metadata.csv"


clinical = pd.read_csv(file)


print("Showing patient characteristics\n")


for i in range(10):

    print("==============================")
    print("Sample:", i+1)

    print(
        clinical.loc[
            i,
            "!Sample_characteristics_ch1"
        ]
    )
