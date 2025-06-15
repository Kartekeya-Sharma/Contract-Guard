import os
import logging
from PyPDF2 import PdfReader
import docx
import traceback

logger = logging.getLogger(__name__)

def parse_document(file_path):
    """
    Extract text from a document file (PDF, DOCX, or TXT)
    """
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return parse_pdf(file_path)
        elif file_extension == '.docx':
            return parse_docx(file_path)
        elif file_extension == '.txt':
            return parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
    except Exception as e:
        logger.error(f"Error parsing document: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def parse_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        raise

def parse_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing DOCX: {str(e)}")
        raise

def parse_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        logger.error(f"Error parsing TXT: {str(e)}")
        raise 