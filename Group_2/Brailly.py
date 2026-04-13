import sys
import time
from pathlib import Path
from smbus2 import SMBus
import gpiod

# TPIC2810 settings
I2C_BUS = 1
TPIC_ADDR = 0x60      # common default if A2/A1/A0 are all low; adjust if needed
SUBADDR_WRITE_AND_LATCH = 0x44

# Optional GPIO line for G (output enable)
# Datasheet: G high -> all outputs off, G low -> outputs active
G_PIN = 16
chip_path = "/dev/gpiochip0"

if len(sys.argv) < 2:
    print("Usage: python3 Brailly.py /path/to/BrailleOutput.txt")
    raise SystemExit(1)

BRAILLE_FILE = Path(sys.argv[1])

def is_binary_token(token):
    return len(token) == 6 and all(c in "01" for c in token)

def braille6_to_byte(token):
    # Direct mapping: "100000" -> 0x20
    # If your wiring is reversed, use: return int(token[::-1], 2)
    return int(token, 2)

# Request GPIO for G pin so outputs can be enabled
lines = gpiod.request_lines(
    chip_path,
    consumer="tpic2810-braille",
    config={
        G_PIN: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT),
    },
)

# Enable outputs: G low
lines.set_value(G_PIN, gpiod.line.Value.INACTIVE)

bus = SMBus(I2C_BUS)

try:
    if not BRAILLE_FILE.exists():
        print(f"File not found: {BRAILLE_FILE}")
        raise SystemExit(1)

    with open(BRAILLE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            tokens = line.strip().split()

            for token in tokens:
                if not is_binary_token(token):
                    print(f"Skipping non-binary token: {token}")
                    continue

                value = braille6_to_byte(token)

                print(f"Writing {token} -> 0x{value:02X}")

                # TPIC2810: subaddress 0x44 writes data and transfers to outputs immediately
                bus.write_i2c_block_data(TPIC_ADDR, SUBADDR_WRITE_AND_LATCH, [value])

                time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    try:
        # Turn everything off
        bus.write_i2c_block_data(TPIC_ADDR, SUBADDR_WRITE_AND_LATCH, [0x00])
        # Disable outputs
        lines.set_value(G_PIN, gpiod.line.Value.ACTIVE)
    except Exception:
        pass

    bus.close()
    print("Done.")
