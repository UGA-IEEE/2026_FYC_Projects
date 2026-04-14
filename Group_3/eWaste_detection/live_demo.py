from ultralytics import YOLO
import cv2

if __name__ == '__main__':
    model = YOLO('best.pt')
   
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   
    while True:
        ret, frame = cap.read()
        if not ret:
            break
       
        results = model.predict(frame, conf=0.5, imgsz=160, verbose=False)
        annotated = results[0].plot()
       
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"Detected: {model.names[cls]} ({conf:.2f})")
       
        cv2.imshow('E-Waste Detector', annotated)
       
        if cv2.waitKey(1) == ord('q'):
            break
   
    cap.release()
    cv2.destroyAllWindows()
