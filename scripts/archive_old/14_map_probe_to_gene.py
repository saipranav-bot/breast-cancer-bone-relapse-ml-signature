import pandas as pd
import mygene
import os


print("Loading significant genes...")


# Load selected probes

sig_genes = pd.read_csv(
    "results/tables/selected_relapse_genes.csv"
)


print(sig_genes.head())


# Extract probe IDs

probes = sig_genes["gene"].tolist()


print("\nNumber of probes:")
print(len(probes))


# Connect to MyGene database

mg = mygene.MyGeneInfo()


print("\nMapping probes to gene symbols...")


results = mg.querymany(
    probes,
    scopes="reporter",
    fields="symbol,name",
    species="human"
)


mapping = []


for item in results:

    probe = item.get("query")

    symbol = item.get("symbol", "NA")

    name = item.get("name", "NA")

    mapping.append(
        [
            probe,
            symbol,
            name
        ]
    )


mapping_df = pd.DataFrame(
    mapping,
    columns=[
        "probe",
        "gene_symbol",
        "gene_name"
    ]
)


print("\nMapping result:")
print(mapping_df)


# Merge with statistics

final = sig_genes.merge(
    mapping_df,
    left_on="gene",
    right_on="probe",
    how="left"
)


os.makedirs("results/tables", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)


final.to_csv(
    "results/tables/relapse_genes_mapped.csv",
    index=False
)


print("\nSaved:")
print(
    "results/tables/relapse_genes_mapped.csv"
)
