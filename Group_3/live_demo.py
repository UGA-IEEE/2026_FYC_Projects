from ultralytics import YOLO
import cv2

if __name__ == '__main__':
    model = YOLO(r'C:\Users\hieu1\ml_projects\runs\train2\weights\best.pt')
    
    cap = cv2.VideoCapture(0)  # Your webcam
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model.predict(frame, conf=0.25, verbose=False)
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"Detected: {model.names[cls]} ({conf:.2f})")
        annotated = results[0].plot()  # Draw boxes on frame
        
        cv2.imshow('E-Waste Detector', annotated)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()