import GEOparse
import os

os.makedirs("../data/raw", exist_ok=True)

gse = GEOparse.get_GEO(
    geo="GSE2034",
    destdir="../data/raw/",
    silent=False,
    how="quick"
)

print("Dataset downloaded successfully")
print(gse)
