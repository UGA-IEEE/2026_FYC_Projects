from ultralytics import YOLO
import cv2
from gpiozero import Servo, PWMOutputDevice
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
    sleep(0.4)      # allow full motion
    servo.detach()  # stops jitter completely


# --------------------
# DC motor PWM setup
# --------------------
MOTOR_PWM_GPIO = 24

# frequency can be adjusted if needed
motor_pwm = PWMOutputDevice(MOTOR_PWM_GPIO, frequency=1000, initial_value=0)

def set_motor_speed(percent):
    """
    Set motor speed using PWM duty cycle.
    0%   = motor off
    50%  = 50% duty cycle
    100% = 100% duty cycle
    """
    percent = max(0, min(100, percent))   # clamp between 0 and 100
    duty_cycle = percent / 100.0
    motor_pwm.value = duty_cycle
    print(f"Motor speed set to {percent}% ({duty_cycle:.2f} duty cycle)")


# --------------------
# Ask user for motor speed
# --------------------
try:
    SPEED_PERCENT = float(input("Enter motor speed percentage (0-100): "))
except ValueError:
    print("Invalid input. Defaulting motor speed to 50%.")
    SPEED_PERCENT = 50

set_motor_speed(SPEED_PERCENT)


# --------------------
# Label → Angle mapping
# --------------------
ANGLE_MAP = {
    "USB_Drive": 35,
    "RAM": 3,
    "CPU": 25
}

# --------------------
# YOLO setup
# --------------------
model = YOLO("../ml_final/best.pt")

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
            conf=0.6,
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
    motor_pwm.off()
