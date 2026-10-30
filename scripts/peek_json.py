import json

path = "datasets/fathomnet/annotations/train.json"

with open(path) as f:
    data = json.load(f)

# For each section, show the first item inside it
for name, content in data.items():
    print("=" * 50)
    print("SECTION:", name)
    print("=" * 50)

    # Only show examples if the section is a list
    if isinstance(content, list) and len(content) > 0:
        print(json.dumps(content[0], indent=2))
    else:
        print(content)