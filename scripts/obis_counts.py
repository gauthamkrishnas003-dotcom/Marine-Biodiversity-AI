import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path
import yaml

# Read the class names from your merged dataset
with open("datasets/yolo_top20_merged/data.yaml") as f:
    names = list(yaml.safe_load(f)["names"].values())

# "Sponges" is our own merged label, so we look up the phylum Porifera instead
LOOKUP = {"Sponges": "Porifera"}

rows = []
for name in names:
    query = LOOKUP.get(name, name)
    url = ("https://api.obis.org/v3/occurrence?"
           + urllib.parse.urlencode({"scientificname": query, "size": 1}))
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            total = json.load(r).get("total", 0)
    except Exception as e:
        total = f"error: {e}"
    rows.append((name, query, total))
    print(f"{name:32s} -> {total}")

Path("outputs").mkdir(exist_ok=True)
with open("outputs/obis_counts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["class", "obis_query", "obis_records"])
    w.writerows(rows)
print("\nSaved outputs/obis_counts.csv")