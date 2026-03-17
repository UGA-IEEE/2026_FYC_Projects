import time
import spidev
import gpiod

# BCM numbers
RCLK = 16
SRCLR = 2

# Open GPIO chip.
# On many Pi 5 systems this is gpiochip4, but check `gpiodetect` if needed.
chip = gpiod.Chip("gpiodetect")

rclk = chip.get_line(RCLK)
srclr = chip.get_line(SRCLR)

rclk.request(consumer="595-test-rclk", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
srclr.request(consumer="595-test-srclr", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[1])

spi = spidev.SpiDev()
spi.open(0, 0)               # SPI0 CE0 device node; CE0 is not used by the 595 here
spi.max_speed_hz = 50000     # start slow
spi.mode = 0b00

def latch():
    rclk.set_value(0)
    time.sleep(0.001)
    rclk.set_value(1)
    time.sleep(0.001)
    rclk.set_value(0)

def clear_register():
    # SRCLR is active low
    srclr.set_value(0)
    time.sleep(0.001)
    srclr.set_value(1)
    latch()

def write_595(value: int):
    # Shift 8 bits into the shift register
    spi.xfer2([value & 0xFF])

    # Copy shift register -> output register
    latch()

def run_patterns():
    patterns = [
        0x00,  # QA=0 QB=0
        0x01,  # QA=1 QB=0
        0x02,  # QA=0 QB=1
        0x03,  # QA=1 QB=1
        0x55,  # 01010101
        0xAA,  # 10101010
        0xFF,  # all high
        0x00,  # all low
    ]

    for p in patterns:
        print(f"Writing 0x{p:02X}")
        write_595(p)
        time.sleep(1.0)

try:
    print("Clearing register...")
    clear_register()
    time.sleep(1)

    print("Running fixed patterns...")
    run_patterns()

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
    rclk.release()
    srclr.release()
    print("Done.")