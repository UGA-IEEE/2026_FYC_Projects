import time
import spidev
import gpiod
from pathlib import Path

RCLK = 16
SRCLR = 2
chip_path = "/dev/gpiochip0"

# Path to the output file produced by BrailleAlphabet.c
BRAILLE_FILE = Path("BrailleOutput.txt")

lines = gpiod.request_lines(
    chip_path,
    consumer="595-test",
    config={
        RCLK: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT),
        SRCLR: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT),
    },
)

# Initial states
lines.set_value(RCLK, gpiod.line.Value.INACTIVE)
lines.set_value(SRCLR, gpiod.line.Value.ACTIVE)   # keep SRCLR high (inactive)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000
spi.mode = 0

def latch():
    lines.set_value(RCLK, gpiod.line.Value.ACTIVE)
    time.sleep(0.001)
    lines.set_value(RCLK, gpiod.line.Value.INACTIVE)
    time.sleep(0.001)

def clear_register():
    # SRCLR is active low
    lines.set_value(SRCLR, gpiod.line.Value.INACTIVE)
    time.sleep(0.001)
    lines.set_value(SRCLR, gpiod.line.Value.ACTIVE)
    latch()

def write_595(value):
    spi.xfer2([value & 0xFF])
    latch()

def is_binary_token(token):
    return len(token) == 6 and all(c in "01" for c in token)

try:
    if not BRAILLE_FILE.exists():
        print(f"File not found: {BRAILLE_FILE}")
        raise SystemExit(1)

    clear_register()

    with open(BRAILLE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            tokens = line.strip().split()

            for token in tokens:
                # Only process 6-bit binary tokens from the C file
                if is_binary_token(token):
                    value = int(token, 2)
                    print(f"Writing {token} -> 0x{value:02X}")
                    write_595(value)
                    time.sleep(0.5)   # adjust delay as needed

                else:
                    print(f"Skipping non-binary token: {token}")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    write_595(0x00)
    spi.close()
    print("Done.")
