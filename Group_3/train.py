from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    model.train(
        data=r'C:\ewaste_dataset\ewaste.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        workers=4,
        project=r'C:\ewaste_runs'
    )