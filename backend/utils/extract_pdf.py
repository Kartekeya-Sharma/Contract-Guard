from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def extract_text_from_pdf(filepath):
    """
    Extract text from a PDF file using pdfminer.six
    """
    try:
        # Configure layout parameters for better text extraction
        laparams = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5,
            detect_vertical=True
        )
        
        # Extract text with custom parameters
        text = extract_text(filepath, laparams=laparams)
        
        # Clean up the extracted text
        text = text.replace('\n\n', '\n')  # Remove double newlines
        text = ' '.join(text.split())  # Normalize whitespace
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}") 