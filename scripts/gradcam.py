import cv2
import numpy as np
import torch
from pathlib import Path
from ultralytics import YOLO

# ---- Settings ----
MODEL_PATH = "runs/detect/experiments/merged_v1/weights/best.pt"
IMAGE_DIR = Path("datasets/yolo_top20_merged/images/test")
HOW_MANY = 6
IMGSZ = 416
LAYER = 10            # which layer to look at (16 = fairly detailed, 10 = coarser)
# ------------------

yolo = YOLO(MODEL_PATH)
net = yolo.model.float().cpu().eval()
for p in net.parameters():
    p.requires_grad_(True)
names = yolo.names

stash = {}
def forward_hook(module, inputs, output):
    stash["act"] = output
    output.retain_grad()          # keep the gradient of this layer

hook = net.model[LAYER].register_forward_hook(forward_hook)

out_dir = Path("outputs/gradcam")
out_dir.mkdir(parents=True, exist_ok=True)

for path in sorted(IMAGE_DIR.glob("*.png"))[:HOW_MANY]:
    bgr = cv2.imread(str(path))
    bgr = cv2.resize(bgr, (IMGSZ, IMGSZ))        # simple resize (slightly stretches)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    x = torch.from_numpy(rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0

    net.zero_grad()
    with torch.enable_grad():
        out = net(x)
        preds = out[0] if isinstance(out, (list, tuple)) else out   # (1, 4+classes, boxes)
        scores = preds[0, 4:, :]                                    # class scores
        best = scores.max()                                         # strongest guess
        best.backward()

    cls_id = int(scores.max(dim=1).values.argmax())
    act = stash["act"]
    weights = act.grad.mean(dim=(2, 3), keepdim=True)
    cam = torch.relu((weights * act).sum(dim=1))[0].detach().numpy()
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
    cam = cv2.resize(cam, (IMGSZ, IMGSZ))

    heat = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(bgr, 0.55, heat, 0.45, 0)
    label = f"{names[cls_id]} (score {best.item():.2f})"
    cv2.putText(overlay, label, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    save_as = out_dir / f"cam_{path.stem[:8]}.png"
    cv2.imwrite(str(save_as), np.hstack([bgr, overlay]))
    print("Saved", save_as, "|", label)

hook.remove()