import json
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path

path = "datasets/fathomnet/annotations/train.json"

with open(path) as f:
    data = json.load(f)

# Dictionary: category id -> animal name
names = {c["id"]: c["name"] for c in data["categories"]}

# Count how many times each animal appears in the whole dataset
counts = Counter(a["category_id"] for a in data["annotations"])

print("TOP 15 MOST COMMON ANIMALS")
for cat_id, n in counts.most_common(15):
    print(f"{names[cat_id]}: {n}")

print()
print("Animal types that appear at least once:", len(counts))
print("Animal types with only 1 example:",
      sum(1 for n in counts.values() if n == 1))
print("Animal types with fewer than 10 examples:",
      sum(1 for n in counts.values() if n < 10))
print("Animal types with 1000+ examples:",
      sum(1 for n in counts.values() if n >= 1000))

# Draw a bar chart of the top 15
top = counts.most_common(15)
labels = [names[c] for c, _ in top]
values = [n for _, n in top]

plt.figure(figsize=(10, 6))
plt.barh(labels[::-1], values[::-1])
plt.xlabel("Number of annotations")
plt.title("Top 15 animals in FathomNet train.json")
plt.tight_layout()

Path("outputs").mkdir(exist_ok=True)
plt.savefig("outputs/top_animals.png")
print("\nChart saved to outputs/top_animals.png")