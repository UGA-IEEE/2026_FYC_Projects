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

# Set initial values
lines.set_value(RCLK, 0)
lines.set_value(SRCLR, 1)   # keep clear inactive

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000
spi.mode = 0

def latch():
    lines.set_value(RCLK, 1)
    time.sleep(0.001)
    lines.set_value(RCLK, 0)
    time.sleep(0.001)

def clear_register():
    lines.set_value(SRCLR, 0)   # active low
    time.sleep(0.001)
    lines.set_value(SRCLR, 1)
    latch()

def write_595(value):
    spi.xfer2([value & 0xFF])
    latch()

try:
    print("Clearing register...")
    clear_register()
    time.sleep(1)

    print("Running patterns...")
    for p in [0x00, 0x01, 0x02, 0x03, 0x55, 0xAA, 0xFF]:
        print(f"Writing 0x{p:02X}")
        write_595(p)
        time.sleep(1)

    print("Walking bit test...")
    while True:
        for i in range(8):
            v = 1 << i
            print(f"Writing 0x{v:02X}")
            write_595(v)
            time.sleep(0.5)

except KeyboardInterrupt:
    write_595(0x00)
    spi.close()
    print("Done.")