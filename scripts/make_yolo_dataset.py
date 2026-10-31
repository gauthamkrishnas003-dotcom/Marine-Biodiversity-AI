import json
import random
import shutil
from collections import defaultdict
from pathlib import Path

random.seed(42)   # same shuffle every time

json_path = "datasets/fathomnet/annotations/subset_top20.json"
img_dir = Path("datasets/fathomnet/images")
out_dir = Path("datasets/yolo_top20")

with open(json_path) as f:
    data = json.load(f)

# YOLO wants class numbers 0, 1, 2... (not our original ids)
cats = sorted(data["categories"], key=lambda c: c["id"])
id_to_yolo = {c["id"]: i for i, c in enumerate(cats)}
class_names = [c["name"] for c in cats]

# Group annotations by image
by_image = defaultdict(list)
for a in data["annotations"]:
    by_image[a["image_id"]].append(a)

# Shuffle images, then split 80 / 10 / 10
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

# Fresh output folder
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
            # keep the box inside the picture
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(W, x + w), min(H, y + h)
            if x2 <= x1 or y2 <= y1:
                continue                      # skip broken boxes
            xc = (x1 + x2) / 2 / W
            yc = (y1 + y2) / 2 / H
            bw = (x2 - x1) / W
            bh = (y2 - y1) / H
            cls = id_to_yolo[a["category_id"]]
            lines.append(f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

        # copy the picture and write its label file
        shutil.copy(img_dir / img["file_name"],
                    out_dir / "images" / split / img["file_name"])
        label_name = Path(img["file_name"]).stem + ".txt"
        (out_dir / "labels" / split / label_name).write_text("\n".join(lines))

# data.yaml tells YOLO where everything is
yaml_lines = [
    f"path: {out_dir.resolve().as_posix()}",
    "train: images/train",
    "val: images/val",
    "test: images/test",
    f"nc: {len(class_names)}",
    "names:",
] + [f"  {i}: {name}" for i, name in enumerate(class_names)]
(out_dir / "data.yaml").write_text("\n".join(yaml_lines))

print("Train images:", len(splits["train"]))
print("Val images:  ", len(splits["val"]))
print("Test images: ", len(splits["test"]))
print("Classes:", len(class_names))
print("Saved to", out_dir)