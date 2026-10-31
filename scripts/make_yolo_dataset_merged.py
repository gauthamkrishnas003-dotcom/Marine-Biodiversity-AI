import json
import random
import shutil
from collections import defaultdict
from pathlib import Path

random.seed(42)   # same seed as before, so the split matches the old one

json_path = "datasets/fathomnet/annotations/subset_top20.json"
img_dir = Path("datasets/fathomnet/images")
out_dir = Path("datasets/yolo_top20_merged")

# These three names become one class
MERGE = {"Porifera": "Sponges", "sponge": "Sponges", "Hexactinellida": "Sponges"}

with open(json_path) as f:
    data = json.load(f)

# Old category id -> new (merged) name
old_name = {c["id"]: c["name"] for c in data["categories"]}
new_name = {cid: MERGE.get(n, n) for cid, n in old_name.items()}

# New class numbers 0, 1, 2... in the order of first appearance
class_names = []
for c in sorted(data["categories"], key=lambda c: c["id"]):
    n = new_name[c["id"]]
    if n not in class_names:
        class_names.append(n)
name_to_yolo = {n: i for i, n in enumerate(class_names)}

by_image = defaultdict(list)
for a in data["annotations"]:
    by_image[a["image_id"]].append(a)

images = data["images"][:]
random.shuffle(images)
n = len(images)
n_train = int(n * 0.8)
n_val = int(n * 0.1)
splits = {
    "train": images[:n_train],
    "val": images[n_train:n_train + n_val],
    "test": images[n_train + n_val:],
}

if out_dir.exists():
    shutil.rmtree(out_dir)

for split, items in splits.items():
    (out_dir / "images" / split).mkdir(parents=True)
    (out_dir / "labels" / split).mkdir(parents=True)
    for img in items:
        W, H = img["width"], img["height"]
        lines = []
        for a in by_image[img["id"]]:
            x, y, w, h = a["bbox"]
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(W, x + w), min(H, y + h)
            if x2 <= x1 or y2 <= y1:
                continue
            cls = name_to_yolo[new_name[a["category_id"]]]
            lines.append(f"{cls} {(x1+x2)/2/W:.6f} {(y1+y2)/2/H:.6f} "
                         f"{(x2-x1)/W:.6f} {(y2-y1)/H:.6f}")
        shutil.copy(img_dir / img["file_name"], out_dir / "images" / split / img["file_name"])
        (out_dir / "labels" / split / (Path(img["file_name"]).stem + ".txt")).write_text("\n".join(lines))

yaml_lines = [
    f"path: {out_dir.resolve().as_posix()}",
    "train: images/train", "val: images/val", "test: images/test",
    f"nc: {len(class_names)}", "names:",
] + [f"  {i}: {nm}" for i, nm in enumerate(class_names)]
(out_dir / "data.yaml").write_text("\n".join(yaml_lines))

print("Train / Val / Test:", len(splits["train"]), len(splits["val"]), len(splits["test"]))
print("Classes:", len(class_names))