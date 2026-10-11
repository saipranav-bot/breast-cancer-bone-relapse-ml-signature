
# Machine Learning-Based Discovery of a 9-Gene Signature for Bone Relapse Prediction in Breast Cancer


## Project Overview

This project develops a machine learning-based gene expression signature for predicting bone relapse risk in breast cancer patients.

The workflow integrates:

- Microarray gene expression analysis
- Bioinformatics preprocessing
- Statistical feature selection
- Machine learning classification
- Biomarker discovery
- Functional enrichment analysis
- Patient risk stratification


The objective is to identify stable gene biomarkers associated with bone relapse and develop a predictive 9-gene signature.


--------------------------------------------------

# Biological Question

Can gene expression profiles from primary breast cancer tumors predict future bone relapse risk?


Objectives:

1. Process breast cancer gene expression data.
2. Identify relapse-associated genes.
3. Build machine learning prediction models.
4. Select robust biomarkers.
5. Develop a final gene signature.
6. Understand biological pathways involved in relapse.



--------------------------------------------------

# Dataset Information


## GEO Dataset

Dataset:

GSE2034


Platform:

Affymetrix Human Genome U133A Array (GPL96)


Disease:

Breast cancer


Patients:

286


Clinical outcome:

Bone relapse


Class distribution:

Non-relapse:
217 samples


Bone relapse:
69 samples


Original expression matrix:

22,283 probe features × 286 patients



--------------------------------------------------

# Complete Workflow


## Stage 1 — Dataset Acquisition


Tools:

- Python
- GEO database
- GEOparse
- pandas


Input:

GSE2034 Series Matrix


Downloaded:

- Gene expression matrix
- Clinical metadata
- Platform annotation


Output:

Raw expression dataset.



--------------------------------------------------

# Stage 2 — Expression Processing


## Log2 Transformation

Expression values were transformed into log2 scale.


Purpose:

- Reduce technical variation
- Stabilize variance
- Improve model performance


## Quality Control


Methods:

- Expression distribution analysis
- Principal Component Analysis (PCA)


Purpose:

- Detect abnormal samples
- Evaluate dataset quality



--------------------------------------------------

# Stage 3 — Clinical Label Extraction


Clinical metadata was processed to identify:

- Bone relapse status
- Patient identifiers


Labels:

0 = No bone relapse

1 = Bone relapse


Final dataset:

286 patients with relapse labels.



--------------------------------------------------

# Stage 4 — Probe Annotation and Gene Mapping


Microarray probes were converted into gene symbols using GPL96 annotation.


Tools:

- Affymetrix GPL96 annotation
- pandas


Purpose:

Convert probe-level expression into biologically interpretable gene-level data.



--------------------------------------------------

# Stage 5 — Feature Reduction


Original data:

22,283 probes


Problem:

Machine learning cannot efficiently train with thousands of features and only 286 patients.


Feature reduction strategy:


## Variance Filtering


Low-expression and low-variance probes were removed.


Purpose:

Remove uninformative genes.


## Supervised Feature Selection


Genes associated with bone relapse were selected using machine learning.


Methods:

- Logistic Regression coefficients
- Random Forest importance
- SVM coefficients



Final reduced feature space:

20 relapse-associated genes.



--------------------------------------------------

# Stage 6 — Machine Learning Model Development


Three classification models were trained.


## Logistic Regression


Purpose:

Identify linear gene-risk relationships.


Performance:

ROC-AUC:

0.676



## Random Forest


Purpose:

Capture nonlinear gene interactions.


Performance:

ROC-AUC:

0.648



## Support Vector Machine


Purpose:

High-dimensional classification.


Performance:

ROC-AUC:

0.641



Model comparison showed Logistic Regression performed best.



--------------------------------------------------

# Stage 7 — Consensus Biomarker Discovery


Feature importance from three models was compared.


Methods combined:

- Logistic Regression
- Random Forest
- SVM


Genes selected repeatedly across models were considered stable biomarkers.


Consensus genes included:

- GPRC5A
- IGLV1-44
- TNFRSF11B
- IGKC
- PP14571
- IGLC1
- IGLL5
- IGLJ3
- IGHD



--------------------------------------------------

# Stage 8 — Development of 9-Gene Signature


A final predictive model was trained using only 9 genes.


Feature matrix:

286 patients × 9 genes


Genes:

GPRC5A

IGLV1-44

TNFRSF11B

IGKC

PP14571

IGLC1

IGLL5

IGLJ3

IGHD



Performance:

Training ROC-AUC:

0.708


5-fold cross validation:

Mean ROC-AUC:

0.703



--------------------------------------------------

# Stage 9 — Internal Re-evaluation of the Signature


NOTE: this is **not** an independent external validation. The signature was
re-scored on the *same* 286-patient GSE2034 cohort it was derived from, so the
reported AUC is an internal (optimistic) estimate. See "Limitations" below.


Process:

1. Extract signature genes from full expression matrix.
2. Map probes to genes.
3. Calculate patient risk scores.
4. Evaluate predictive performance.


Internal re-evaluation:

ROC-AUC:

0.738



--------------------------------------------------

# Stage 10 — Functional Enrichment Analysis


Purpose:

Understand biological mechanisms associated with the signature genes.


Tools:

- gseapy
- Enrichr
- GO database
- KEGG database


Analyses:

## Gene Ontology (GO)

Identified enrichment in:

- Immunoglobulin-mediated immune response
- B cell mediated immunity
- EGFR regulation
- Osteoclast differentiation regulation


## KEGG


Detected pathways:

- Osteoclast differentiation
- Cytokine-cytokine receptor interaction



--------------------------------------------------

# Stage 11 — Patient Risk Stratification


A risk score was calculated from the 9-gene expression profile.


Patients were classified into:

- High-risk group
- Low-risk group


Generated outputs:

- Risk score distribution
- Relapse rate comparison
- Risk group visualization



--------------------------------------------------

# Software and Tools


Programming:

- Python 3


Libraries:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- gseapy
- networkx


Bioinformatics resources:

- GEO
- Affymetrix GPL96
- Enrichr
- GO
- KEGG



--------------------------------------------------

# Project Structure


data/

    raw/
        GSE2034 series matrix (expression + clinical characteristics)
        GPL96 platform annotation

    processed/
        cleaned expression matrices
        clinical metadata and labels

    ml/
        train/test feature and label matrices


scripts/

    Numbered analysis scripts (canonical order in scripts/run_all.sh).
    Superseded/exploratory variants were removed to keep the workflow
    unambiguous; they remain retrievable from earlier commits in the git
    history.


results/

    tables/     CSV result tables
    figures/    ROC curves, heatmaps, enrichment and risk-stratification plots


## Reproducibility

Environment:

    conda env create -f environment.yml
    conda activate cancer_ml

Run the full pipeline from the repository root:

    bash scripts/run_all.sh

This downloads GSE2034 and the GPL96 annotation and rewrites every file under
data/ and results/. Steps 31–32 query Enrichr online; all other steps run
offline. The canonical script order is defined in scripts/run_all.sh.



--------------------------------------------------

# Key Results


Dataset:

286 breast cancer patients


Starting features:

22,283 probes


After preprocessing:

20 candidate genes


Final signature:

9 genes


Best model:

Logistic Regression


Cross-validation ROC-AUC:

0.703


Validation ROC-AUC:

0.738



--------------------------------------------------

# Limitations


These results should be interpreted as an exploratory analysis, not a validated
clinical signature.

* **No independent cohort.** The signature was selected and evaluated on the
  same 286 GSE2034 patients. Feature selection (variance filtering, supervised
  selection, model-based gene ranking) used the full cohort before the held-out
  split, so the reported AUCs are optimistically biased.
* **The signature is dominated by immunoglobulin genes** (IGKV1OR2-108, IGK,
  IGKV1-37, IGHM, IGH, IGLC1, IGLV1-44, IGHA1, IGKC, IGLJ3, IGHD, IGLL5). In
  breast cancer, immunoglobulin / B-cell infiltration is strongly associated
  with the ER-negative, immune-enriched phenotype. The signature therefore
  likely reflects immune and hormone-receptor biology rather than a bone-
  specific relapse mechanism, and may be confounded by ER status, which was not
  adjusted for.
* **Modest discrimination.** Test per-model ROC-AUC values are between ~0.64
  and 0.71, which is weak for a clinical classifier.
* **Uncharacterized features.** The mapped feature set includes non-informative
  annotation entries such as `PP14571`, `abParts`, `AC128677.4` and `CYAT1`,
  reflecting incomplete GPL96 probe annotation rather than validated genes.
* **Platform detectable genes only.** Several signature members are absent or
  unreliable on the Affymetrix U133A platform, so only a subset is carried into
  the validation heatmap.

Follow-up work would require an independent, ER-status-adjusted validation
cohort before any biological or clinical claim can be made.

---

# Conclusion


This project demonstrates a complete bioinformatics and machine learning workflow for discovering a gene expression signature associated with breast cancer bone relapse.

The identified 9-gene signature is enriched for immune / immunoglobulin genes
and recovers immune-related and bone-remodeling pathways, but given the
limitations above it should be treated as a hypothesis-generating result rather
than a validated biomarker.



--------------------------------------------------

# Author


V Sai Pranav


Bioinformatics and Computational Biology Project

