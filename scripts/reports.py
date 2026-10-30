import json
from pathlib import Path

path = "datasets/fathomnet/annotations/train.json"

with open(path) as f:
    data = json.load(f)

lines = []
lines.append(f"Sections: {list(data.keys())}")

for name, content in data.items():
    if isinstance(content, list):
        lines.append(f"\n{name}: {len(content)} items")
        if content:
            lines.append("First example:")
            lines.append(json.dumps(content[0], indent=2)[:600])
    else:
        lines.append(f"\n{name}: {str(content)[:300]}")

report = "\n".join(lines)
print(report)

# Also save it to a file
Path("outputs").mkdir(exist_ok=True)
Path("outputs/json_report.txt").write_text(report)
print("\nSaved to outputs/json_report.txt")