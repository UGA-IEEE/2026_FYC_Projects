Must have same name as the pdf text file

PDF Extractor Extension
This extension lets you quickly extract text from PDF files inside VS Code.

✨ Features
Right-click any PDF in Explorer → Extract Text from PDF
Extracted text is automatically saved as filename_extracted.txt in the same folder
The saved file is opened directly in VS Code for editing
Supports extracting text from standard text-based PDFs
📖 Usage
Open the Explorer in VS Code.
Right-click a .pdf file.
Choose "Extract Text from PDF".
The extension will:
Save the extracted content as filename_extracted.txt
Open the file in a new editor tab
⚙️ Requirements
Works only with .pdf files.
Uses the pdf-parse library under the hood.
⚠️ Known Issues
Image-based or scanned PDFs may not extract text (OCR is not yet supported).
Formatting (like tables and layouts) may not be preserved.
📝 Release Notes
0.0.2
Added auto-save feature: extracted text is now saved as filename_extracted.txt and opened directly in VS Code.
0.0.1
Initial release of PDF Extractor