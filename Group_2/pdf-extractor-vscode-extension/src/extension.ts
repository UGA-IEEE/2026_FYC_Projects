import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

// Try to use pdfplumber via Python subprocess
// Since we can't directly use Node PDF libraries easily, we'll use a subprocess approach

async function extractPdfText(pdfPath: string): Promise<string> {
  const { spawn } = require('child_process');
  
  return new Promise((resolve, reject) => {
    // Use Python with pdfplumber to extract text
    const pythonScript = `
import pdfplumber
import sys

try:
    with pdfplumber.open('${pdfPath}') as pdf:
        text = ''
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + '\\n\\n'
        print(text)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
`;
    
    const python = spawn('python', ['-c', pythonScript], {
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let stdout = '';
    let stderr = '';
    
    python.stdout.on('data', (data: Buffer) => {
      stdout += data.toString();
    });
    
    python.stderr.on('data', (data: Buffer) => {
      stderr += data.toString();
    });
    
    python.on('close', (code: number) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`Python error: ${stderr}`));
      }
    });
    
    python.on('error', (err: Error) => {
      reject(err);
    });
  });
}

async function extractAndSavePdf(pdfUri: vscode.Uri): Promise<void> {
  const pdfPath = pdfUri.fsPath;
  const fileName = path.basename(pdfPath, '.pdf');
  const dir = path.dirname(pdfPath);
  const txtPath = path.join(dir, `${fileName}.txt`);
  
  try {
    vscode.window.showInformationMessage(`Extracting text from ${fileName}.pdf...`);
    
    const text = await extractPdfText(pdfPath);
    
    fs.writeFileSync(txtPath, text, 'utf-8');
    
    vscode.window.showInformationMessage(`✓ Extracted: ${fileName}.txt`);
    
    // Refresh the file explorer
    const textFileUri = vscode.Uri.file(txtPath);
    await vscode.commands.executeCommand('vscode.open', textFileUri);
    
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    vscode.window.showErrorMessage(`Failed to extract PDF: ${message}`);
  }
}

async function autoExtractAllPdfs(): Promise<void> {
  const folders = vscode.workspace.workspaceFolders;
  
  if (!folders || folders.length === 0) {
    vscode.window.showErrorMessage('No workspace folder open');
    return;
  }
  
  const workspaceRoot = folders[0].uri.fsPath;
  const pdfs = fs.readdirSync(workspaceRoot)
    .filter(file => file.endsWith('.pdf'))
    .map(file => path.join(workspaceRoot, file));
  
  if (pdfs.length === 0) {
    vscode.window.showInformationMessage('No PDF files found in workspace');
    return;
  }
  
  vscode.window.showInformationMessage(`Found ${pdfs.length} PDF(s). Extracting...`);
  
  let successCount = 0;
  for (const pdfPath of pdfs) {
    try {
      const fileName = path.basename(pdfPath, '.pdf');
      const txtPath = path.join(workspaceRoot, `${fileName}.txt`);
      
      const text = await extractPdfText(pdfPath);
      fs.writeFileSync(txtPath, text, 'utf-8');
      
      successCount++;
    } catch (error) {
      const fileName = path.basename(pdfPath);
      console.error(`Failed to extract ${fileName}:`, error);
    }
  }
  
  vscode.window.showInformationMessage(`✓ Extracted ${successCount}/${pdfs.length} PDFs`);
}

export function activate(context: vscode.ExtensionContext) {
  console.log('PDF Extractor extension activated');
  
  // Command: Extract single PDF (right-click)
  let extractCommand = vscode.commands.registerCommand(
    'pdf-extractor.extractPdf',
    async (uri: vscode.Uri) => {
      if (uri && uri.fsPath.endsWith('.pdf')) {
        await extractAndSavePdf(uri);
      }
    }
  );
  
  // Command: Auto-extract all PDFs in workspace
  let autoExtractCommand = vscode.commands.registerCommand(
    'pdf-extractor.autoExtract',
    async () => {
      await autoExtractAllPdfs();
    }
  );
  
  context.subscriptions.push(extractCommand);
  context.subscriptions.push(autoExtractCommand);
}

export function deactivate() {}
