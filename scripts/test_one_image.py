import json
from pathlib import Path
from fathomnet.api import images

# Read the first image's file name from your JSON
with open("datasets/fathomnet/annotations/train.json") as f:
    data = json.load(f)

file_name = data["images"][0]["file_name"]   # e.g. 44f7713a-....png
uuid = file_name.rsplit(".", 1)[0]           # remove ".png"
print("Looking up:", uuid)

# Ask FathomNet for this image's information
info = images.find_by_uuid(uuid)
print("Found! URL:", info.url)