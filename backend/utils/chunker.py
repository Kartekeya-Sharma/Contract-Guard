import re
import nltk
from nltk.tokenize import sent_tokenize
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
def ensure_nltk_data():
    """
    Ensure all required NLTK data is downloaded
    """
    required_packages = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'stopwords']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            logger.info(f"Downloading NLTK package: {package}")
            nltk.download(package, quiet=True)

# Download NLTK data on module import
ensure_nltk_data()

def split_into_clauses(text):
    """
    Split text into clauses based on common legal document patterns
    """
    try:
        # Remove extra whitespace and normalize line endings
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Split on common clause markers
        # This is a simple implementation - you might want to make it more sophisticated
        clause_markers = [
            r'\d+\.\s',  # Numbered clauses (e.g., "1. ")
            r'\([a-z]\)\s',  # Lettered subclauses (e.g., "(a) ")
            r'WHEREAS\s',  # Whereas clauses
            r'THEREFORE\s',  # Therefore clauses
            r'IN WITNESS WHEREOF\s',  # Witness clauses
            r'IN CONSIDERATION OF\s',  # Consideration clauses
            r'THE PARTIES AGREE AS FOLLOWS:\s',  # Agreement clauses
        ]
        
        # Create pattern for splitting
        pattern = '|'.join(clause_markers)
        
        # Split text into clauses
        clauses = re.split(f'({pattern})', text)
        
        # Combine markers with their clauses and filter out empty strings
        result = []
        for i in range(0, len(clauses)-1, 2):
            if i+1 < len(clauses):
                clause = (clauses[i] + clauses[i+1]).strip()
                if clause:
                    result.append(clause)
        
        # If no clauses were found, return the whole text as one clause
        if not result:
            result = [text]
        
        logger.info(f"Split text into {len(result)} clauses")
        return result
        
    except Exception as e:
        logger.error(f"Error splitting text into clauses: {str(e)}")
        # Return the whole text as one clause if splitting fails
        return [text]

def clean_text(text):
    """
    Clean and normalize the text
    """
    try:
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?()\[\]{}"\'-]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error in clean_text: {str(e)}")
        raise 