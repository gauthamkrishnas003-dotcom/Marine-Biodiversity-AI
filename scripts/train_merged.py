from ultralytics import YOLO

def main():
    # Start from your trained model; the output layer is rebuilt for 18 classes
    model = YOLO("runs/detect/experiments/baseline_v2/weights/best.pt")
    model.train(
        data="datasets/yolo_top20_merged/data.yaml",
        epochs=20,
        imgsz=416,
        batch=8,
        device="cpu",
        workers=0,
        patience=10,
        project="experiments",
        name="merged_v1",
    )

if __name__ == "__main__":
    main()