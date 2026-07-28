import pandas as pd
import gseapy as gp
import matplotlib.pyplot as plt

# 9-gene signature
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

print("Genes:")
print(genes)


# ==========================
# GO Biological Process
# ==========================

print("\nRunning GO enrichment...")

go = gp.enrichr(
    gene_list=genes,
    gene_sets=[
        "GO_Biological_Process_2025",
        "GO_Molecular_Function_2025",
        "GO_Cellular_Component_2025"
    ],
    organism="human",
    outdir=None
)

go_results = go.results

print("\nTop GO terms:")
print(go_results[['Term','Adjusted P-value']].head(10))

go_results.to_csv(
    "results/9gene_GO_enrichment.csv",
    index=False
)


# ==========================
# KEGG Pathway
# ==========================

print("\nRunning KEGG enrichment...")

kegg = gp.enrichr(
    gene_list=genes,
    gene_sets="KEGG_2021_Human",
    organism="human",
    outdir=None
)

kegg_results = kegg.results

print("\nTop KEGG pathways:")
print(kegg_results[['Term','Adjusted P-value']].head(10))


kegg_results.to_csv(
    "results/9gene_KEGG_enrichment.csv",
    index=False
)


# ==========================
# Plot GO
# ==========================

top_go = go_results.head(10)

plt.figure(figsize=(8,6))

plt.barh(
    top_go["Term"][::-1],
    -top_go["Adjusted P-value"].apply(lambda x: -__import__('math').log10(x))[::-1]
)

plt.xlabel("-log10 adjusted P-value")
plt.title("9-Gene Signature GO Enrichment")

plt.tight_layout()

plt.savefig(
    "results/9gene_GO_barplot.png",
    dpi=300
)

plt.close()


print("\nSaved:")
print("results/9gene_GO_enrichment.csv")
print("results/9gene_KEGG_enrichment.csv")
print("results/9gene_GO_barplot.png")
