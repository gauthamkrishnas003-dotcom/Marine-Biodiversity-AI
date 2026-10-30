import json

# Path to the file you downloaded
path = "datasets/fathomnet/annotations/train.json"

# Open and read the file (this may take 10-20 seconds, it's a big file)
with open(path) as f:
    data = json.load(f)

# What kind of thing is it?
print("Type:", type(data))

# What are the main sections inside it?
print("Sections:", list(data.keys()))

# How many items are in each section?
for name, content in data.items():
    print(name, "->", len(content), "items")