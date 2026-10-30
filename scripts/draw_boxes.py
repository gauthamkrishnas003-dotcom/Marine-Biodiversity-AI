import json
from pathlib import Path
from PIL import Image, ImageDraw

json_path = "datasets/fathomnet/annotations/train.json"
img_dir = Path("datasets/fathomnet/images")
out_dir = Path("outputs")
out_dir.mkdir(exist_ok=True)

HOW_MANY = 5   # how many preview pictures to make

with open(json_path) as f:
    data = json.load(f)

# Dictionary: category id -> animal name
names = {c["id"]: c["name"] for c in data["categories"]}

# Group the annotations by photo: image_id -> list of animals
by_image = {}
for a in data["annotations"]:
    by_image.setdefault(a["image_id"], []).append(a)

made = 0
for img in data["images"]:
    path = img_dir / img["file_name"]
    if not path.exists():
        continue                      # skip photos we haven't downloaded

    picture = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(picture)

    for a in by_image.get(img["id"], []):
        x, y, w, h = a["bbox"]        # left, top, width, height
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
        draw.text((x, max(0, y - 12)), names[a["category_id"]], fill="yellow")

    save_as = out_dir / f"preview_{made + 1}.png"
    picture.save(save_as)
    print("Saved", save_as)

    made += 1
    if made >= HOW_MANY:
        break