import os
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import logging
import chardet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_encoding(filepath):
    """
    Detect the encoding of a text file
    """
    with open(filepath, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def parse_document(filepath):
    """
    Extract text from PDF, DOCX, or TXT files
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    file_extension = os.path.splitext(filepath)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return parse_pdf(filepath)
        elif file_extension == '.docx':
            return parse_docx(filepath)
        elif file_extension == '.txt':
            return parse_txt(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        logger.error(f"Error parsing document {filepath}: {str(e)}")
        raise

def parse_pdf(filepath):
    """
    Extract text from PDF file
    """
    try:
        text = pdf_extract_text(filepath)
        if not text.strip():
            raise ValueError("No text content found in PDF")
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF {filepath}: {str(e)}")
        raise

def parse_docx(filepath):
    """
    Extract text from DOCX file
    """
    try:
        doc = Document(filepath)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        if not text.strip():
            raise ValueError("No text content found in DOCX")
        return text
    except Exception as e:
        logger.error(f"Error parsing DOCX {filepath}: {str(e)}")
        raise

def parse_txt(filepath):
    """
    Extract text from TXT file with automatic encoding detection
    """
    try:
        encoding = detect_encoding(filepath)
        if not encoding:
            encoding = 'utf-8'  # fallback to utf-8
            
        with open(filepath, 'r', encoding=encoding) as file:
            text = file.read()
            
        if not text.strip():
            raise ValueError("No text content found in TXT file")
            
        return text
    except UnicodeDecodeError:
        # If the detected encoding fails, try with utf-8
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            logger.error(f"Error parsing TXT {filepath} with UTF-8: {str(e)}")
            raise
    except Exception as e:
        logger.error(f"Error parsing TXT {filepath}: {str(e)}")
        raise 