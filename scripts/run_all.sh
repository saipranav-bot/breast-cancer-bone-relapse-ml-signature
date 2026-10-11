#!/usr/bin/env bash
# =============================================================
# End-to-end reproduction of the GSE2034 bone-relapse analysis.
#
# Usage (from the repository root):
#     bash scripts/run_all.sh
#
# Requires the environment described in environment.yml
# (Python with pandas, numpy, scipy, scikit-learn, matplotlib,
#  seaborn, GEOparse, gseapy, networkx).
#
# Stage 31/32 query Enrichr over the internet; all other steps
# run offline once GSE2034 and the GPL96 annotation are downloaded.
# =============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

mkdir -p data/raw data/processed data/ml results/tables results/figures

STEPS=(
  01_download_GEO
  04_read_matrix
  05_preprocess_expression
  06_quality_control
  07_extract_clinical_labels
  10_create_labels
  11_prepare_ml_dataset
  12_variance_filter
  13_supervised_feature_selection
  15_clean_probe_annotation
  16_create_final_ml_matrix
  17_clean_ml_features
  18_prepare_ml_data
  19_train_logistic_regression
  21_train_random_forest
  24_train_svm
  26_model_comparison
  27_feature_overlap
  28_final_biomarker_heatmap
  29_final_9gene_signature_model
  30_cv_9gene_signature
  31_GO_KEGG_enrichment
  32_enrichment_dotplot_network
  33_validate_9gene_signature
  34_9gene_validation_ROC
  37_final_9gene_validation
  39_risk_stratification
)

for step in "${STEPS[@]}"; do
  echo "########## ${step}"
  python "scripts/${step}.py"
done

echo "Pipeline complete."
