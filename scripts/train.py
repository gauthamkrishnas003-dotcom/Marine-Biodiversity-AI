from ultralytics import YOLO

def main():
    # Continue from the model you already trained
    model = YOLO("runs/detect/experiments/baseline_v1/weights/best.pt")

    model.train(
        data="datasets/yolo_top20/data.yaml",
        epochs=30,
        imgsz=416,         # bigger pictures help with small animals
        batch=8,
        device="cpu",
        workers=0,
        patience=10,       # stop early if it stops improving
        project="experiments",
        name="baseline_v2",
    )

if __name__ == "__main__":
    main()