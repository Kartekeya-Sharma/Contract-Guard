import re
import spacy
from typing import List

# Load spaCy model for NLP processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def split_into_clauses(text: str) -> List[str]:
    """
    Split contract text into individual clauses using regex and NLP.
    Returns a list of clause texts.
    """
    # First, try to split by numbered clauses (e.g., "1.", "2.", etc.)
    numbered_clauses = re.split(r'\n\s*\d+\.\s+', text)
    
    if len(numbered_clauses) > 1:
        # Remove empty clauses and clean up
        clauses = [clause.strip() for clause in numbered_clauses if clause.strip()]
        return clauses
    
    # If no numbered clauses found, try bullet points
    bullet_clauses = re.split(r'\n\s*[•\-\*]\s+', text)
    
    if len(bullet_clauses) > 1:
        clauses = [clause.strip() for clause in bullet_clauses if clause.strip()]
        return clauses
    
    # If no clear markers found, use NLP to split by sentences
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    
    # Group sentences into logical clauses
    clauses = []
    current_clause = []
    
    for sentence in sentences:
        # Check if sentence starts with common clause indicators
        if re.match(r'^(WHEREAS|NOW, THEREFORE|IN WITNESS WHEREOF|IN CONSIDERATION|THE PARTIES AGREE|SECTION|ARTICLE)', 
                   sentence, re.IGNORECASE):
            if current_clause:
                clauses.append(' '.join(current_clause))
                current_clause = []
        current_clause.append(sentence)
    
    if current_clause:
        clauses.append(' '.join(current_clause))
    
    # Clean up clauses
    clauses = [clause.strip() for clause in clauses if clause.strip()]
    
    # If still no clauses found, return the whole text as one clause
    if not clauses:
        return [text.strip()]
    
    return clauses 