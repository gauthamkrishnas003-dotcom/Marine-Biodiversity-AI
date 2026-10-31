from ultralytics import YOLO

model = YOLO("runs/detect/experiments/baseline_v2/weights/best.pt")

# Run on the test photos (the model never saw these)
model.predict(
    source="datasets/yolo_top20/images/test",
    imgsz=416,
    conf=0.25,          # only show guesses it is at least 25% sure about
    max_det=50,
    device="cpu",
    save=True,          # save pictures with the boxes drawn
    project="outputs",
    name="predictions",
    exist_ok=True,
)
print("Done! Open the folder outputs/predictions")