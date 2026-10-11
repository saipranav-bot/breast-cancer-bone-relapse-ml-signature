import os
import gzip
import shutil
import urllib.request

# ==============================
# Download GSE2034 from GEO
# ==============================
# Expression matrix + clinical characteristics are taken from the GEO
# series matrix file. The 'bone relapses (1=yes, 0=no)' sample
# characteristic provides the prediction label used downstream.

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

SERIES_MATRIX_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE2nnn/GSE2034/"
    "matrix/GSE2034_series_matrix.txt.gz"
)

OUT_FILE = os.path.join(RAW_DIR, "GSE2034_series_matrix.txt")


def download(url, dest):
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as response:
        with open(dest, "wb") as out:
            shutil.copyfileobj(response, out)
    print(f"Saved {dest}")


if not os.path.exists(OUT_FILE):
    gz_file = OUT_FILE + ".gz"
    download(SERIES_MATRIX_URL, gz_file)
    with gzip.open(gz_file, "rb") as f_in, open(OUT_FILE, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(gz_file)
    print("Decompressed series matrix")
else:
    print(f"Already present: {OUT_FILE}")

print("Dataset downloaded successfully")
