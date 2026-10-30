import json
import socket
import time
import urllib.request
from pathlib import Path
from fathomnet.api import images

socket.setdefaulttimeout(20)    # give up on any single request after 20 seconds

json_path = "datasets/fathomnet/annotations/subset_top20.json"
out_dir = Path("datasets/fathomnet/images")
out_dir.mkdir(parents=True, exist_ok=True)

with open(json_path) as f:
    data = json.load(f)

total = len(data["images"])
done = 0
failed = 0

for i, img in enumerate(data["images"], start=1):
    file_name = img["file_name"]
    save_path = out_dir / file_name
    temp_path = out_dir / (file_name + ".part")

    if save_path.exists():          # already have it, skip
        done += 1
        continue

    try:
        uuid = file_name.rsplit(".", 1)[0]
        info = images.find_by_uuid(uuid)
        urllib.request.urlretrieve(info.url, temp_path)
        temp_path.rename(save_path)
        done += 1
        print(f"[{i}/{total}] saved {file_name}")
        time.sleep(0.1)
    except Exception as e:
        failed += 1
        print(f"[{i}/{total}] FAILED {file_name}: {e}")
        if temp_path.exists():
            temp_path.unlink()

print(f"\nFinished. Have: {done}, failed: {failed}")