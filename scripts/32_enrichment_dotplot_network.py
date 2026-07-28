import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import textwrap


print("Loading enrichment results...")


go = pd.read_csv(
    "results/9gene_GO_enrichment.csv"
)

kegg = pd.read_csv(
    "results/9gene_KEGG_enrichment.csv"
)


# ==========================
# GO Dotplot
# ==========================

print("Creating GO dotplot...")


go_top = go.sort_values(
    "Adjusted P-value"
).head(10)


go_top["logFDR"] = -np.log10(
    go_top["Adjusted P-value"]
)


plt.figure(figsize=(10,7))


plt.scatter(
    go_top["logFDR"],
    range(len(go_top)),
    s=120
)


plt.yticks(
    range(len(go_top)),
    [
        "\n".join(textwrap.wrap(x,35))
        for x in go_top["Term"]
    ]
)


plt.xlabel("-log10 Adjusted P-value")

plt.title(
    "GO Enrichment of 9-Gene Bone Relapse Signature"
)


plt.tight_layout()


plt.savefig(
    "results/9gene_GO_dotplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ==========================
# KEGG Dotplot
# ==========================

print("Creating KEGG dotplot...")


kegg_top = kegg.sort_values(
    "Adjusted P-value"
).head(10)


kegg_top["logFDR"] = -np.log10(
    kegg_top["Adjusted P-value"]
)


plt.figure(figsize=(9,5))


plt.scatter(
    kegg_top["logFDR"],
    range(len(kegg_top)),
    s=150
)


plt.yticks(
    range(len(kegg_top)),
    kegg_top["Term"]
)


plt.xlabel("-log10 Adjusted P-value")

plt.title(
    "KEGG Pathway Enrichment"
)


plt.tight_layout()


plt.savefig(
    "results/9gene_KEGG_dotplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# ==========================
# Improved Gene-GO Network
# ==========================

print("Creating improved gene-pathway network...")


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


terms = [
    "Immunoglobulin Mediated Immune Response",
    "B Cell Mediated Immunity",
    "Regulation of Osteoclast Differentiation",
    "Negative Regulation of Protein Tyrosine Kinase Signaling",
    "Cytokine Related Signaling"
]


G = nx.Graph()


for gene in genes:
    G.add_node(
        gene,
        category="gene"
    )


for term in terms:
    G.add_node(
        term,
        category="GO"
    )



connections = {

"TNFRSF11B":[
    "Regulation of Osteoclast Differentiation"
],

"IGKC":[
    "Immunoglobulin Mediated Immune Response",
    "B Cell Mediated Immunity"
],

"IGLC1":[
    "Immunoglobulin Mediated Immune Response"
],

"IGLJ3":[
    "B Cell Mediated Immunity"
],

"IGHD":[
    "B Cell Mediated Immunity",
    "Immunoglobulin Mediated Immune Response"
],

"GPRC5A":[
    "Cytokine Related Signaling",
    "Negative Regulation of Protein Tyrosine Kinase Signaling"
],

"PP14571":[
    "Cytokine Related Signaling"
],

"IGLL5":[
    "B Cell Mediated Immunity"
],

"IGLV1-44":[
    "Immunoglobulin Mediated Immune Response"
]

}



for gene, pathways in connections.items():

    for pathway in pathways:

        G.add_edge(
            gene,
            pathway
        )



gene_nodes = [
    n for n,d in G.nodes(data=True)
    if d["category"]=="gene"
]


go_nodes = [
    n for n,d in G.nodes(data=True)
    if d["category"]=="GO"
]



pos = {}


for i,node in enumerate(gene_nodes):
    pos[node]=(-1,i)


for i,node in enumerate(go_nodes):
    pos[node]=(1,i*1.5)



plt.figure(figsize=(14,10))


nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=gene_nodes,
    node_size=2000
)


nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=go_nodes,
    node_size=3500
)


nx.draw_networkx_edges(
    G,
    pos,
    width=1
)


labels={}


for node in G.nodes():

    if node in go_nodes:
        labels[node]="\n".join(
            textwrap.wrap(node,22)
        )

    else:
        labels[node]=node



nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=8
)


plt.axis("off")


plt.title(
    "Gene–GO Network\n9-Gene Bone Relapse Signature",
    fontsize=15
)


plt.savefig(
    "results/9gene_GO_network_improved.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



print("\nSaved:")
print("results/9gene_GO_dotplot.png")
print("results/9gene_KEGG_dotplot.png")
print("results/9gene_GO_network_improved.png")
