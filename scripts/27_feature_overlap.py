import pandas as pd


print("Loading feature importance files...")


# Logistic regression
logistic = pd.read_csv(
    "results/logistic_gene_importance.csv"
)


# Random forest
rf = pd.read_csv(
    "results/random_forest_gene_importance.csv"
)


# SVM
svm = pd.read_csv(
    "results/svm_gene_importance.csv"
)



# Select important genes

logistic_genes = set(
    logistic.head(10)["Gene"]
)


rf_genes = set(
    rf.head(10)["Gene"]
)


svm_genes = set(
    svm.head(10)["Gene"]
)



# Combine all genes

all_genes = (
    logistic_genes |
    rf_genes |
    svm_genes
)



results = []


for gene in all_genes:

    results.append(
        {
            "Gene": gene,

            "Logistic_selected":
            gene in logistic_genes,

            "RF_selected":
            gene in rf_genes,

            "SVM_selected":
            gene in svm_genes,

            "Consensus_score":
            sum(
                [
                    gene in logistic_genes,
                    gene in rf_genes,
                    gene in svm_genes
                ]
            )
        }
    )



consensus = pd.DataFrame(
    results
)


consensus = consensus.sort_values(
    "Consensus_score",
    ascending=False
)



print("\nConsensus biomarker ranking")
print("==========================")

print(consensus)



consensus.to_csv(
    "results/consensus_biomarkers.csv",
    index=False
)



print("\nSaved:")
print(
    "results/consensus_biomarkers.csv"
)
