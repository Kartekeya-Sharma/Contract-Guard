import logging
import re
from collections import Counter
from typing import Dict, List

logger = logging.getLogger(__name__)

# Define clause types and their keywords
CLAUSE_KEYWORDS = {
    'confidentiality': [
        'confidential', 'non-disclosure', 'nda', 'proprietary', 'trade secret',
        'confidentiality', 'non-disclosure agreement'
    ],
    'termination': [
        'terminate', 'termination', 'end of agreement', 'cancellation',
        'expiration', 'early termination'
    ],
    'payment': [
        'payment', 'invoice', 'fee', 'price', 'cost', 'payment terms',
        'payment schedule', 'late payment'
    ],
    'liability': [
        'liability', 'indemnification', 'warranty', 'guarantee',
        'hold harmless', 'limitation of liability'
    ],
    'intellectual_property': [
        'intellectual property', 'ip', 'copyright', 'patent', 'trademark',
        'license', 'licensing'
    ],
    'governance': [
        'governing law', 'jurisdiction', 'dispute resolution', 'arbitration',
        'mediation', 'applicable law'
    ],
    'service_level': [
        'service level', 'sla', 'performance', 'uptime', 'availability',
        'service quality'
    ],
    'data_protection': [
        'data protection', 'privacy', 'gdpr', 'personal data', 'data security',
        'data handling'
    ]
}

# Define risk indicators
RISK_INDICATORS = {
    'High': [
        'unlimited', 'indemnify', 'warranty', 'guarantee', 'confidential',
        'terminate', 'breach', 'penalty', 'damages', 'liability'
    ],
    'Medium': [
        'reasonable', 'standard', 'normal', 'typical', 'usual',
        'customary', 'regular'
    ],
    'Low': [
        'limited', 'restricted', 'standard', 'basic', 'minimum'
    ]
}

# Define specific concerns for each clause type
CLAUSE_CONCERNS = {
    'confidentiality': [
        'Data protection requirements',
        'Information sharing restrictions',
        'Security measures needed',
        'Potential breach consequences'
    ],
    'termination': [
        'Early termination penalties',
        'Notice period requirements',
        'Post-termination obligations',
        'Transition requirements'
    ],
    'payment': [
        'Payment schedule',
        'Late payment penalties',
        'Currency and exchange rates',
        'Tax implications'
    ],
    'liability': [
        'Financial exposure limits',
        'Insurance requirements',
        'Exclusion clauses',
        'Third-party claims'
    ],
    'intellectual_property': [
        'IP ownership rights',
        'Usage restrictions',
        'Infringement risks',
        'Licensing terms'
    ],
    'governance': [
        'Legal jurisdiction',
        'Dispute resolution process',
        'Compliance requirements',
        'Regulatory framework'
    ],
    'service_level': [
        'Performance metrics',
        'Service availability',
        'Response time requirements',
        'Penalty clauses'
    ],
    'data_protection': [
        'Data handling requirements',
        'Privacy compliance',
        'Security measures',
        'Data breach procedures'
    ]
}

def generate_explanation(clause_type: str, risk_level: str, clause_text: str) -> str:
    """Generate a detailed explanation for the clause"""
    concerns = CLAUSE_CONCERNS.get(clause_type, ['No specific concerns identified'])
    explanation = f"This {clause_type.replace('_', ' ')} clause has {risk_level.lower()} risk level. "
    explanation += f"It requires attention to: {', '.join(concerns[:2])}."
    return explanation

def classify_clause(clause: str) -> Dict:
    """
    Classify a contract clause using rule-based analysis
    """
    try:
        # Convert to lowercase for case-insensitive matching
        clause_lower = clause.lower()
        
        # Find matching clause types
        clause_types = []
        for clause_type, keywords in CLAUSE_KEYWORDS.items():
            if any(keyword in clause_lower for keyword in keywords):
                clause_types.append(clause_type)
        
        # If no specific type found, classify as General
        clause_type = clause_types[0] if clause_types else 'General'
        
        # Determine risk level
        risk_level = 'Medium'  # Default risk level
        for level, indicators in RISK_INDICATORS.items():
            if any(indicator in clause_lower for indicator in indicators):
                risk_level = level
                break
        
        # Get specific concerns for this clause type
        specific_concerns = CLAUSE_CONCERNS.get(clause_type, [
            'Standard terms and conditions',
            'General contractual obligations',
            'Basic compliance requirements',
            'Standard business practices'
        ])
        
        # Generate explanation
        explanation = generate_explanation(clause_type, risk_level, clause)
        
        return {
            'type': clause_type,
            'risk_level': risk_level,
            'explanation': explanation,
            'specific_concerns': specific_concerns
        }
        
    except Exception as e:
        logger.error(f"Error classifying clause: {str(e)}")
        return {
            'type': 'Error',
            'risk_level': 'Unknown',
            'explanation': f'Error in classification: {str(e)}',
            'specific_concerns': ['Error occurred during classification']
        }

def normalize_classification(text):
    """
    Normalize the classification text to extract structured information
    """
    # Define valid types and risk levels
    valid_types = {
        'IP', 'Intellectual Property', 'Intellectual Property Rights',
        'Termination', 'Term', 'Termination Clause',
        'Confidentiality', 'Confidential', 'NDA',
        'Payment', 'Payments', 'Fees',
        'Liability', 'Limitation of Liability',
        'Warranty', 'Warranties',
        'Indemnification', 'Indemnity',
        'Force Majeure', 'Force Majeure Clause',
        'Governing Law', 'Jurisdiction',
        'Other'
    }
    
    valid_risk_levels = {'Low', 'Medium', 'High'}
    
    # Extract type
    type_match = re.search(r'Type:\s*([^\n]+)', text, re.IGNORECASE)
    if type_match:
        type_text = type_match.group(1).strip()
        # Find the closest matching valid type
        for valid_type in valid_types:
            if valid_type.lower() in type_text.lower():
                type_text = valid_type
                break
    else:
        type_text = 'Other'
    
    # Extract risk level
    risk_match = re.search(r'Risk:\s*([^\n]+)', text, re.IGNORECASE)
    if risk_match:
        risk_text = risk_match.group(1).strip()
        # Find the closest matching valid risk level
        for valid_risk in valid_risk_levels:
            if valid_risk.lower() in risk_text.lower():
                risk_text = valid_risk
                break
    else:
        risk_text = 'Medium'
    
    # Extract explanation
    explanation_match = re.search(r'Explanation:\s*([^\n]+)', text, re.IGNORECASE)
    explanation_text = explanation_match.group(1).strip() if explanation_match else 'No explanation provided'
    
    return {
        'type': type_text,
        'risk_level': risk_text,
        'explanation': explanation_text
    } 