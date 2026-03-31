from ultralytics import YOLO
import cv2

if __name__ == '__main__':
    model = YOLO(r'C:\ewaste_runs\train2\weights\best.pt')
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model.predict(frame, conf=0.5, verbose=False)
        annotated = results[0].plot()
        
        cv2.imshow('E-Waste Detector', annotated)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()