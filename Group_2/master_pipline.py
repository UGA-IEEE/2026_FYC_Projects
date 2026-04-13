import sys
import time
from pathlib import Path

from PyPDF2 import PdfReader
from smbus2 import SMBus
import gpiod

CAPITAL_SIGN = 1
NUMBER_SIGN = 2

DOUBLE_MAP = [
    ("000100", "101001", "("),
    ("000100", "010110", ")"),
    ("010101", "100001", "\\"),
    ("010101", "010010", "/"),
    ("010001", "101001", "["),
    ("010001", "010110", "]"),
    ("010101", "101001", "{"),
    ("010101", "010110", "}"),
    ("010000", "010110", "<"),
    ("010000", "101001", ">"),
]

WORD_MAP = {
    "and": "111011",
    "for": "111111",
    "the": "011011",
    "with": "011111",
    "of": "101111",
}

G_PIN = 16
CHIP_PATH = "/dev/gpiochip0"
I2C_BUS = 1
TPIC_ADDR = 0x60
SUBADDR_WRITE_AND_LATCH = 0x44


def initialize_braille_map():
    braille_map = {chr(i): "000000" for i in range(128)}

    braille_map["a"] = "100000"
    braille_map["b"] = "101000"
    braille_map["c"] = "110000"
    braille_map["d"] = "110100"
    braille_map["e"] = "100100"
    braille_map["f"] = "111000"
    braille_map["g"] = "111100"
    braille_map["h"] = "101100"
    braille_map["i"] = "011000"
    braille_map["j"] = "011100"
    braille_map["k"] = "100010"
    braille_map["l"] = "101010"
    braille_map["m"] = "110010"
    braille_map["n"] = "110110"
    braille_map["o"] = "100110"
    braille_map["p"] = "111010"
    braille_map["q"] = "111110"
    braille_map["r"] = "101110"
    braille_map["s"] = "011010"
    braille_map["t"] = "011110"
    braille_map["u"] = "100011"
    braille_map["v"] = "101011"
    braille_map["w"] = "011101"
    braille_map["x"] = "110011"
    braille_map["y"] = "110111"
    braille_map["z"] = "100111"

    braille_map[" "] = "000000"

    braille_map["1"] = braille_map["a"]
    braille_map["2"] = braille_map["b"]
    braille_map["3"] = braille_map["c"]
    braille_map["4"] = braille_map["d"]
    braille_map["5"] = braille_map["e"]
    braille_map["6"] = braille_map["f"]
    braille_map["7"] = braille_map["g"]
    braille_map["8"] = braille_map["h"]
    braille_map["9"] = braille_map["i"]
    braille_map["0"] = braille_map["j"]

    braille_map[","] = "001000"
    braille_map[";"] = "001010"
    braille_map[":"] = "001100"
    braille_map["."] = "001101"
    braille_map["!"] = "001110"
    braille_map["?"] = "001011"
    braille_map["-"] = "001001"
    braille_map["'"] = "000010"
    braille_map['"'] = "001011"

    braille_map[chr(CAPITAL_SIGN)] = "000001"
    braille_map[chr(NUMBER_SIGN)] = "010100"

    return braille_map


def match_double_cell(c1, c2):
    for cell1, cell2, replacement in DOUBLE_MAP:
        if c1 == cell1 and c2 == cell2:
            return replacement
    return None


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = " ".join(
        page.extract_text() for page in reader.pages if page.extract_text()
    )
    full_text = full_text.replace("\n", "")
    return full_text.strip()


def resolve_doubles(patterns):
    output = []
    i = 0

    while i < len(patterns):
        if i < len(patterns) - 1:
            replacement = match_double_cell(patterns[i], patterns[i + 1])
            if replacement is not None:
                output.append(replacement)
                i += 2
                continue

        output.append(patterns[i])
        i += 1

    return output


def convert_text_to_braille(text, braille_map):
    braille_lines = []
    braille_patterns = []

    i = 0
    text_length = len(text)

    while i < text_length and len(braille_patterns) < 1023:
        if i == 0:
            word_pattern = WORD_MAP.get(text)
            if word_pattern:
                braille_patterns.append(word_pattern)
                break

        c = text[i]

        if c == " ":
            if braille_patterns:
                braille_lines.append(resolve_doubles(braille_patterns))
                braille_patterns = []
            i += 1
            continue

        if c.isupper():
            braille_patterns.append(braille_map[chr(CAPITAL_SIGN)])
            c = c.lower()

        if c.isdigit():
            braille_patterns.append(braille_map[chr(NUMBER_SIGN)])

        if ord(c) < 128:
            braille_patterns.append(braille_map.get(c, "000000"))

        i += 1

    if braille_patterns:
        braille_lines.append(resolve_doubles(braille_patterns))

    return braille_lines


def save_debug_files(base_dir, text, braille_lines):
    neededtxt_path = base_dir / "neededtxt.txt"
    braille_output_path = base_dir / "BrailleOutput.txt"

    neededtxt_path.write_text(text, encoding="utf-8")

    with braille_output_path.open("w", encoding="utf-8") as f:
        for line in braille_lines:
            f.write(" ".join(line) + "\n")

    return neededtxt_path, braille_output_path


def is_binary_token(token):
    return len(token) == 6 and all(c in "01" for c in token)


def braille6_to_byte(token):
    return int(token, 2)
    # If your hardware bit order is reversed, use:
    # return int(token[::-1], 2)


def send_braille_over_i2c(braille_lines):
    lines = gpiod.request_lines(
        CHIP_PATH,
        consumer="tpic2810-braille",
        config={
            G_PIN: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT),
        },
    )

    # G low = outputs enabled
    lines.set_value(G_PIN, gpiod.line.Value.INACTIVE)

    bus = SMBus(I2C_BUS)

    try:
        for line in braille_lines:
            for token in line:
                if not is_binary_token(token):
                    print(f"Skipping non-binary token: {token}")
                    continue

                value = braille6_to_byte(token)
                print(f"Writing {token} -> 0x{value:02X}")
                bus.write_i2c_block_data(TPIC_ADDR, SUBADDR_WRITE_AND_LATCH, [value])
                time.sleep(0.5)

    finally:
        try:
            bus.write_i2c_block_data(TPIC_ADDR, SUBADDR_WRITE_AND_LATCH, [0x00])
            # G high = outputs disabled
            lines.set_value(G_PIN, gpiod.line.Value.ACTIVE)
        except Exception:
            pass
        bus.close()


def process_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    base_dir = pdf_path.parent

    print(f"Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("Warning: No text could be extracted.")
        return 1

    print("PDF text extracted.")

    braille_map = initialize_braille_map()
    braille_lines = convert_text_to_braille(text, braille_map)
    print("Braille conversion complete.")

    neededtxt_path, braille_output_path = save_debug_files(base_dir, text, braille_lines)
    print(f"Saved extracted text: {neededtxt_path}")
    print(f"Saved braille output: {braille_output_path}")

    print("Sending data over I2C...")
    send_braille_over_i2c(braille_lines)
    print("I2C transmission complete.")

    return 0


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {Path(sys.argv[0]).name} /path/to/file.pdf")
        sys.exit(1)

    sys.exit(process_pdf(sys.argv[1]))


if __name__ == "__main__":
    main()
