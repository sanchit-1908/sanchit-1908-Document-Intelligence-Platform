# docapp/processing/parser.py

import os
from PyPDF2 import PdfReader
import docx

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif ext == '.docx':
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    elif ext in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file type: {ext}")
