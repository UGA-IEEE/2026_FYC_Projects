import time
import spidev
import gpiod

RCLK = 16
SRCLR = 2
chip_path = "/dev/gpiochip0"

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
spi.max_speed_hz = 50000
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

try:
    clear_register()

    for p in [0x00, 0x01, 0x02, 0x03, 0x55, 0xAA, 0xFF]:
        print(f"Writing 0x{p:02X}")
        write_595(p)
        time.sleep(1)

except KeyboardInterrupt:
    write_595(0x00)
    spi.close()
    print("Done.")