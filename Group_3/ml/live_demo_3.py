 from ultralytics import YOLO
import cv2
from gpiozero import Servo
from time import sleep, time

# --------------------
# Servo setup
# --------------------
SERVO_GPIO = 18

servo = Servo(
    SERVO_GPIO,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.5 / 1000
)

def angle_to_value(angle):
    angle = max(0, min(180, angle))
    return (angle / 90.0) - 1.0


def move_servo(angle):
    servo.value = angle_to_value(angle)
    sleep(0.4)     # allow full motion
    servo.detach() # stops jitter completely


# --------------------
# Label → Angle mapping
# --------------------
ANGLE_MAP = {
    "USB_Drive": 45,
    "RAM": 35,
    "CPU": 180
}

# --------------------
# YOLO setup
# --------------------
model = YOLO("best.pt")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 15)

print("E-Waste sorting started")

last_label = None
last_move_time = 0

DETECTION_STABILITY_FRAMES = 3
MOVE_COOLDOWN = 2.0  # seconds between moves

stable_counter = 0
candidate_label = None


try:

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(
            frame,
            conf=0.25,
            imgsz=320,
            verbose=False
        )

        detected_label = None
        detected_conf = 0

        if results and results[0].boxes is not None:

            boxes = results[0].boxes

            if len(boxes) > 0:

                best_i = int(boxes.conf.argmax().item())

                cls = int(boxes[best_i].cls[0])
                detected_conf = float(boxes[best_i].conf[0])
                detected_label = model.names[cls]


        # --------------------
        # Stability filtering
        # --------------------

        if detected_label in ANGLE_MAP and detected_conf > 0.6:

            if detected_label == candidate_label:
                stable_counter += 1
            else:
                candidate_label = detected_label
                stable_counter = 1

        else:
            stable_counter = 0
            candidate_label = None


        # --------------------
        # Move servo ONLY if stable detection
        # --------------------

        if (
            candidate_label
            and stable_counter >= DETECTION_STABILITY_FRAMES
            and candidate_label != last_label
            and time() - last_move_time > MOVE_COOLDOWN
        ):

            angle = ANGLE_MAP[candidate_label]

            print(f"Detected stable: {candidate_label}")
            print(f"Moving servo to {angle}°")

            move_servo(angle)

            last_label = candidate_label
            last_move_time = time()

            stable_counter = 0


except KeyboardInterrupt:

    print("\nStopping system...")


finally:

    cap.release()
    servo.detach()
