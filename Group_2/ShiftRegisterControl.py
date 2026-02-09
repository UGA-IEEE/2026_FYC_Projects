import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
DATA_PIN = 17   # Pin 14 on Chip
CLOCK_PIN = 27  # Pin 11 on Chip
LATCH_PIN = 22  # Pin 12 on Chip

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

def shift_out(val):
    """
    Shifts 8 bits out. 
    We send the Most Significant Bit (Bit 7) first, 
    so the Least Significant Bit (Bit 0) ends up at Q0 (Pin 15).
    """
    GPIO.output(LATCH_PIN, GPIO.LOW)
    
    # Range 7 down to 0 (7, 6, 5... 0)
    for i in range(7, -1, -1):
        # Get the bit at position 'i'
        bit = (val >> i) & 1
        
        GPIO.output(DATA_PIN, bit)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)
        
    GPIO.output(LATCH_PIN, GPIO.HIGH)

try:
    print("Testing 2 LEDs...")
    
    while True:
        print("LED 1 ON (Q0)")
        shift_out(1)  # Binary 00000001
        time.sleep(1)

        print("LED 2 ON (Q1)")
        shift_out(2)  # Binary 00000010
        time.sleep(1)

        print("BOTH ON")
        shift_out(3)  # Binary 00000011
        time.sleep(1)

        print("BOTH OFF")
        shift_out(0)  # Binary 00000000
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()