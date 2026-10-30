import json
import pandas as pd

path = "datasets/fathomnet/annotations/train.json"

with open(path) as f:
    data = json.load(f)

# Turn each section into a table (like an Excel sheet)
images = pd.DataFrame(data["images"])
annotations = pd.DataFrame(data["annotations"])
categories = pd.DataFrame(data["categories"])

# 1. What columns does the images table have?
print("IMAGE COLUMNS:", list(images.columns))
print()

# 2. Any column that looks like a link or file name?
for col in images.columns:
    if "url" in col.lower() or "file" in col.lower():
        print("Found:", col)
        print("Example:", images[col].iloc[0])
print()

# 3. How many photos, boxes, and animal types?
print("Photos:", len(images))
print("Animal boxes:", len(annotations))
print("Animal types:", len(categories))