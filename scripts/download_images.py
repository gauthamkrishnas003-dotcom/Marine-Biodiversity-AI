import json
import time
import urllib.request
from pathlib import Path
from fathomnet.api import images

# ---- Settings you can change ----
HOW_MANY = 200
# ---------------------------------

json_path = "datasets/fathomnet/annotations/train.json"
out_dir = Path("datasets/fathomnet/images")
out_dir.mkdir(parents=True, exist_ok=True)

with open(json_path) as f:
    data = json.load(f)

done = 0
failed = 0

for img in data["images"][:HOW_MANY]:
    file_name = img["file_name"]            # e.g. 44f7713a-....png
    save_path = out_dir / file_name

    # Skip if we already downloaded it (so you can re-run safely)
    if save_path.exists():
        done += 1
        continue

    try:
        uuid = file_name.rsplit(".", 1)[0]
        info = images.find_by_uuid(uuid)
        urllib.request.urlretrieve(info.url, save_path)
        done += 1
        print(f"[{done}/{HOW_MANY}] saved {file_name}")
        time.sleep(0.2)                     # be polite to the server
    except Exception as e:
        failed += 1
        print(f"FAILED {file_name}: {e}")

print(f"\nFinished. Downloaded: {done}, failed: {failed}")