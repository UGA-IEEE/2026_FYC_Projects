from pathlib import Path
from PyPDF2 import PdfReader
import sys


# Get PDF path from command-line argument
if len(sys.argv) < 2:
    print("Usage: python3 PDF_Text.py /path/to/file.pdf")
    exit()

input_pdf = Path(sys.argv[1])

if not input_pdf.exists():
    print(f"File not found: {input_pdf}")
    exit()

base_dir = input_pdf.parent

# part 1: Find and Rename
target_path = base_dir / "neededtxt.pdf"

if input_pdf.name != "neededtxt.pdf":
    if target_path.exists():
        target_path.unlink()  # remove old neededtxt.pdf if it exists
    input_pdf.replace(target_path)
    print(f"File Renamed: {input_pdf.name} -> neededtxt.pdf")
else:
    target_path = input_pdf


# Part 2: Extract Text
reader = PdfReader(target_path)
full_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
full_text = full_text.replace("\n", "")


# Part 3: Print to Terminal
if full_text.strip():
    print(full_text)
    print("End\n")

    # Also save to actual .txt file
    (base_dir / "neededtxt.txt").write_text(full_text, encoding="utf-8")
else:
    print("Warning: No text could be extracted.")
