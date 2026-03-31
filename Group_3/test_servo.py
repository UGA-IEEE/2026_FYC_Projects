from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Use pigpio for hardware PWM
factory = PiGPIOFactory()

# Change GPIO pin if needed (using GPIO 17)
servo = Servo(17, pin_factory=factory)

print("Testing servo on GPIO 17")
print("Press Ctrl+C to stop")

try:
    while True:
        print("Moving to center...")
        servo.mid()
        sleep(1)
        
        print("Moving to max (right)...")
        servo.max()
        sleep(1)
        
        print("Moving to center...")
        servo.mid()
        sleep(1)
        
        print("Moving to min (left)...")
        servo.min()
        sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")
    servo.mid()