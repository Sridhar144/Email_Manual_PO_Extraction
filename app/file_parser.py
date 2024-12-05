
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
from docx import Document
import pandas as pd
from .google_docs_parser import parse_google_doc

def parse_pdf(filepath):
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() for page in reader.pages)

def parse_image(filepath):
    return pytesseract.image_to_string(Image.open(filepath))

def parse_doc(filepath):
    doc = Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs)

def parse_excel(filepath):
    data = pd.read_excel(filepath)
    return data.to_dict(orient="records")

def save_attachment(filepath):
    ext = filepath.split('.')[-1]
    if ext == "pdf":
        return parse_pdf(filepath)
    elif ext in ["jpg", "jpeg", "png"]:
        return parse_image(filepath)
    elif ext == "docx":
        return parse_doc(filepath)
    elif ext in ["xlsx", "xls"]:
        return parse_excel(filepath)
    else:
        raise ValueError("Unsupported file format.")
