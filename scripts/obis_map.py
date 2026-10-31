import json
import urllib.parse
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt

SPECIES = "Strongylocentrotus fragilis"   # change this to any animal from your list

url = ("https://api.obis.org/v3/occurrence?"
       + urllib.parse.urlencode({"scientificname": SPECIES, "size": 1000}))

with urllib.request.urlopen(url, timeout=60) as r:
    data = json.load(r)

records = data.get("results", [])
print("Records downloaded:", len(records))

lons = [r["decimalLongitude"] for r in records if "decimalLongitude" in r and "decimalLatitude" in r]
lats = [r["decimalLatitude"] for r in records if "decimalLongitude" in r and "decimalLatitude" in r]
print("Records with a location:", len(lons))

plt.figure(figsize=(10, 5))
plt.scatter(lons, lats, s=8, alpha=0.5)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"OBIS records: {SPECIES}")
plt.grid(alpha=0.3)
plt.tight_layout()

Path("outputs").mkdir(exist_ok=True)
plt.savefig("outputs/obis_map.png")
print("Saved outputs/obis_map.png")