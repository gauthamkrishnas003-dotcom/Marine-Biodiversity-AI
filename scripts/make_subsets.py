import json
import random
from collections import Counter, defaultdict

random.seed(42)                 # makes the random choice repeatable

TOP_N = 20                      # how many animal types to keep
IMAGES_PER_CLASS = 100          # max images per animal type

path = "datasets/fathomnet/annotations/train.json"
with open(path) as f:
    data = json.load(f)

names = {c["id"]: c["name"] for c in data["categories"]}
counts = Counter(a["category_id"] for a in data["annotations"])
top_ids = [c for c, _ in counts.most_common(TOP_N)]

# For each top animal: which images contain it?
images_by_class = defaultdict(set)
for a in data["annotations"]:
    if a["category_id"] in top_ids:
        images_by_class[a["category_id"]].add(a["image_id"])

# Pick up to 100 random images for each animal
chosen = set()
for c in top_ids:
    ids = sorted(images_by_class[c])
    random.shuffle(ids)
    chosen.update(ids[:IMAGES_PER_CLASS])

# Build the smaller dataset (only top animals, only chosen images)
subset = {
    "images": [i for i in data["images"] if i["id"] in chosen],
    "annotations": [a for a in data["annotations"]
                    if a["image_id"] in chosen and a["category_id"] in top_ids],
    "categories": [c for c in data["categories"] if c["id"] in top_ids],
}

out_path = "datasets/fathomnet/annotations/subset_top20.json"
with open(out_path, "w") as f:
    json.dump(subset, f)

print("Images in subset:", len(subset["images"]))
print("Annotations in subset:", len(subset["annotations"]))
print("\nAnimals kept:")
for c in top_ids:
    print(f"  {names[c]}")
print("\nSaved to", out_path)