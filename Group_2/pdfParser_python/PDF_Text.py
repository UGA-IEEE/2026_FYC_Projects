
from pathlib import Path
from PyPDF2 import PdfReader


base_dir = Path(__file__).parent
# part 1: Find and Rename
pdf_files = [f for f in base_dir.glob("*.pdf") if f.name != "neededtxt.pdf"]


if not pdf_files:
    target_path = base_dir / "neededtxt.pdf"
    if not target_path.exists():
        print("No PDF found.")
        exit()
else:
# rename file for BrailleAlphabet code
    target_path = base_dir / "neededtxt.pdf"
    pdf_files[0].replace(target_path)
    print(f"File Renamed: {pdf_files[0].name} neededtxt.pdf")


# Part 2: Extract Text
reader = PdfReader(target_path)
full_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
full_text = full_text.replace("\n", "")


#Part 3: Print to Terminal
if full_text.strip():
    print(full_text)
    print("End\n")
   
    # Also save to actual .txt file
    (base_dir / "neededtxt.txt").write_text(full_text, encoding="utf-8")
else:
    print("Warning: No text could be extracted.")

