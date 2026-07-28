import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.utils import resample


print("Loading risk scores...")


risk = pd.read_csv(
    "results/9gene_risk_scores.csv"
)


print(risk.head())


# ==========================
# ROC
# ==========================

y_true = risk["bone_relapse"]

score = risk["Risk_score"]


auc = roc_auc_score(
    y_true,
    score
)


print("\nROC-AUC:")
print(round(auc,3))


fpr, tpr, thresholds = roc_curve(
    y_true,
    score
)



plt.figure(figsize=(6,6))


plt.plot(
    fpr,
    tpr,
    label=f"9-gene signature AUC={auc:.3f}"
)


plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)


plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - 9 Gene Signature"
)


plt.legend()


plt.savefig(
    "results/9gene_validation_ROC.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()



# ==========================
# Bootstrap CI
# ==========================

boot_auc=[]


for i in range(1000):

    sample = resample(
        risk,
        replace=True,
        random_state=i
    )


    if len(sample["bone_relapse"].unique()) < 2:
        continue


    boot_auc.append(
        roc_auc_score(
            sample["bone_relapse"],
            sample["Risk_score"]
        )
    )



lower = np.percentile(
    boot_auc,
    2.5
)


upper = np.percentile(
    boot_auc,
    97.5
)


print("\n95% Confidence Interval:")
print(
    round(lower,3),
    "-",
    round(upper,3)
)



metrics = pd.DataFrame({

    "Metric":[
        "AUC",
        "Lower_CI",
        "Upper_CI"
    ],

    "Value":[
        auc,
        lower,
        upper
    ]

})


metrics.to_csv(
    "results/9gene_ROC_metrics.csv",
    index=False
)


print("\nSaved:")
print(
    "results/9gene_validation_ROC.png"
)

print(
    "results/9gene_ROC_metrics.csv"
)

