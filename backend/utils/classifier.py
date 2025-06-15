import re
from typing import Dict, List, Tuple

class RuleBasedClassifier:
    def __init__(self):
        # Define risk levels and their descriptions
        self.risk_levels = {
            'high': 'Significant potential impact on business operations or legal obligations',
            'medium': 'Moderate impact that requires attention but may be manageable',
            'low': 'Minimal impact or standard industry practice'
        }
        
        # Define clause patterns with their risk levels and specific concerns
        self.clause_patterns = {
            'confidentiality': {
                'patterns': [
                    r'confidential(?:ity)?',
                    r'non-disclosure',
                    r'nda',
                    r'proprietary information',
                    r'trade secret'
                ],
                'risk_level': 'high',
                'specific_concerns': [
                    'Data protection requirements',
                    'Information sharing restrictions',
                    'Security measures needed',
                    'Potential breach consequences'
                ]
            },
            'termination': {
                'patterns': [
                    r'terminat(?:ion|e)',
                    r'end of agreement',
                    r'cancellation',
                    r'expiration'
                ],
                'risk_level': 'high',
                'specific_concerns': [
                    'Early termination penalties',
                    'Notice period requirements',
                    'Post-termination obligations',
                    'Transition requirements'
                ]
            },
            'payment': {
                'patterns': [
                    r'payment',
                    r'invoice',
                    r'fee',
                    r'price',
                    r'cost',
                    r'payment terms'
                ],
                'risk_level': 'medium',
                'specific_concerns': [
                    'Payment schedule',
                    'Late payment penalties',
                    'Currency and exchange rates',
                    'Tax implications'
                ]
            },
            'liability': {
                'patterns': [
                    r'liability',
                    r'indemnification',
                    r'warranty',
                    r'guarantee',
                    r'hold harmless'
                ],
                'risk_level': 'high',
                'specific_concerns': [
                    'Financial exposure limits',
                    'Insurance requirements',
                    'Exclusion clauses',
                    'Third-party claims'
                ]
            },
            'intellectual_property': {
                'patterns': [
                    r'intellectual property',
                    r'ip',
                    r'copyright',
                    r'patent',
                    r'trademark',
                    r'license'
                ],
                'risk_level': 'high',
                'specific_concerns': [
                    'IP ownership rights',
                    'Usage restrictions',
                    'Infringement risks',
                    'Licensing terms'
                ]
            },
            'governance': {
                'patterns': [
                    r'govern(?:ance|ing) law',
                    r'jurisdiction',
                    r'dispute resolution',
                    r'arbitration',
                    r'mediation'
                ],
                'risk_level': 'medium',
                'specific_concerns': [
                    'Legal jurisdiction',
                    'Dispute resolution process',
                    'Compliance requirements',
                    'Regulatory framework'
                ]
            },
            'service_level': {
                'patterns': [
                    r'service level',
                    r'sla',
                    r'performance',
                    r'uptime',
                    r'availability'
                ],
                'risk_level': 'medium',
                'specific_concerns': [
                    'Performance metrics',
                    'Service availability',
                    'Response time requirements',
                    'Penalty clauses'
                ]
            },
            'data_protection': {
                'patterns': [
                    r'data protection',
                    r'privacy',
                    r'gdpr',
                    r'personal data',
                    r'data security'
                ],
                'risk_level': 'high',
                'specific_concerns': [
                    'Data handling requirements',
                    'Privacy compliance',
                    'Security measures',
                    'Data breach procedures'
                ]
            }
        }

    def classify_clause(self, text: str) -> Dict:
        """
        Classify a clause and provide detailed risk analysis.
        """
        text = text.lower()
        max_matches = 0
        best_match = None
        matched_patterns = []

        # Find the best matching clause type
        for clause_type, info in self.clause_patterns.items():
            matches = sum(1 for pattern in info['patterns'] if re.search(pattern, text))
            if matches > max_matches:
                max_matches = matches
                best_match = clause_type
                matched_patterns = [p for p in info['patterns'] if re.search(p, text)]

        if not best_match:
            return {
                'type': 'other',
                'risk_level': 'low',
                'risk_description': 'Standard clause with minimal risk',
                'specific_concerns': ['No specific concerns identified'],
                'matched_patterns': []
            }

        # Get the risk information for the matched clause type
        risk_info = self.clause_patterns[best_match]
        
        # Generate a detailed risk description
        risk_description = f"This {best_match.replace('_', ' ')} clause has {risk_info['risk_level']} risk level. "
        risk_description += f"It requires attention to: {', '.join(risk_info['specific_concerns'][:2])}."

        return {
            'type': best_match,
            'risk_level': risk_info['risk_level'],
            'risk_description': risk_description,
            'specific_concerns': risk_info['specific_concerns'],
            'matched_patterns': matched_patterns
        }

    def analyze_contract(self, clauses: List[str]) -> List[Dict]:
        """
        Analyze a list of clauses and return detailed risk analysis for each.
        """
        return [self.classify_clause(clause) for clause in clauses] 