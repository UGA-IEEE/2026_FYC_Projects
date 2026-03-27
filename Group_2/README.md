Requirments: 
pyPDF2
BE SURE TO HAVE A PDF FILE IN THE GROUP 2 FOLDER.
For PDF_Text: IT IS IMPERATIVE TO CHANGE THE DIRECTORY TO THE EXACT FILE OF WHERE THE PDF IS IN THE SHELL FOR THIS TO WORK
EXAMPLE: PS C:\Users\JordanHoward\OneDrive - University of Georgia\Desktop\UGA\IEEE\2026_FYC_Projects\Group_2\pdfParser_python>
**INSTALL pyPDF2 with python -m pip install pypdf2**


Two runs are needed- run PDF_Text first, then BrailleAlphabet.c
Use gcc BrailleAlphabet.c -o BrailleAlphabet to compile
Use ./BrailleAlphabet to run in terminal. 
BrailleOutput.txt file output should be in the Group 2 folder. 

The code runs brailel with a (example is letter p in ASCII)
1 1
1 0
1 0
to
111010

**Speicial indicators are also used using this format**