# PDF Text Extractor VS Code Extension

Automatically extract text from PDF files and save as `.txt` without right-clicking.

## Features

- **Auto-Extract**: Automatically extract all PDFs in your workspace with a single command
- **Right-Click Extract**: Right-click any PDF and choose "Extract Text from PDF"
- **Automatic Save**: Extracted text is automatically saved as `filename.txt` in the same folder
- **Instant Preview**: The extracted text file opens automatically in the editor

## Installation

1. Place this folder in your VS Code extensions directory, or load it as a development extension:
   ```powershell
   code --extensionDevelopmentPath=.
   ```

2. Ensure Python 3.7+ is installed and `pdfplumber` is available:
   ```powershell
   python -m pip install pdfplumber
   ```

## Usage

### Option 1: Right-Click on a PDF
1. Open a folder with PDF files in VS Code
2. Right-click any `.pdf` file
3. Select **"Extract Text from PDF"**
4. Extracted text is saved as `filename.txt` and opens automatically

### Option 2: Auto-Extract All PDFs
1. Open the Command Palette: `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Search for **"Auto-extract all PDFs in folder"**
3. All PDFs in the workspace are extracted to `.txt` files

## Example

```
workspace/
  ├── document.pdf         → Extract to:  document.txt
  ├── another.pdf          → Extract to:  another.txt
  └── (extracted text files created here)
```

## Requirements

- VS Code 1.60.0+
- Python 3.7+
- `pdfplumber` Python package

## Technical Details

- Uses Python's `pdfplumber` library for PDF text extraction
- Runs extraction as a subprocess to avoid Node.js PDF library complexity
- Saves extracted text with UTF-8 encoding
- Works best with PDFs containing embedded text (not scanned images)

## Building

```powershell
npm install
npm run compile
```

## Running as Development Extension

```powershell
code --extensionDevelopmentPath=.
```

## Limitations

- Requires Python and `pdfplumber` to be installed separately
- Works best with native PDFs containing selectable text
- Scanned PDFs (images) will not extract text without OCR setup
