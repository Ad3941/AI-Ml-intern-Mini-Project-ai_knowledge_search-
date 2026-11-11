import os
from io import BytesIO
from pypdf import PdfReader
from docx import Document

def load_file(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text from .txt, .md, .pdf, or .docx files."""
    ext = os.path.splitext(filename)[1].lower()
    
    try:
        if ext in [".txt", ".md"]:
            return file_bytes.decode("utf-8", errors="ignore")
        
        elif ext == ".pdf":
            reader = PdfReader(BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
            
        elif ext == ".docx":
            doc = Document(BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text
            
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
            
    except Exception as e:
        raise RuntimeError(f"Error parsing {filename}: {str(e)}")