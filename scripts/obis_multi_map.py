import json
import statistics
import urllib.parse
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt

SPECIES = [
    "Strongylocentrotus fragilis",
    "Paragorgia arborea",
    "Heterochone calyx",
    "Chionoecetes tanneri",
]
COLORS = ["tab:red", "tab:blue", "tab:green", "tab:orange"]

plt.figure(figsize=(11, 6))

for name, color in zip(SPECIES, COLORS):
    url = ("https://api.obis.org/v3/occurrence?"
           + urllib.parse.urlencode({"scientificname": name, "size": 1000}))
    with urllib.request.urlopen(url, timeout=60) as r:
        records = json.load(r).get("results", [])

    pts = [(r["decimalLongitude"], r["decimalLatitude"])
           for r in records
           if "decimalLongitude" in r and "decimalLatitude" in r]
    if not pts:
        print(f"{name}: no records with a location")
        continue

    lons = [p[0] for p in pts]
    lats = [p[1] for p in pts]
    print(f"{name}: {len(pts)} points | "
          f"lat {min(lats):.1f} to {max(lats):.1f} (median {statistics.median(lats):.1f}) | "
          f"lon {min(lons):.1f} to {max(lons):.1f} (median {statistics.median(lons):.1f})")

    plt.scatter(lons, lats, s=10, alpha=0.4, color=color, label=name)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("OBIS records for four of the model's animals (first 1,000 records each)")
plt.legend(markerscale=2)
plt.grid(alpha=0.3)
plt.tight_layout()

Path("outputs").mkdir(exist_ok=True)
plt.savefig("outputs/obis_multi_map.png", dpi=150)
print("\nSaved outputs/obis_multi_map.png")