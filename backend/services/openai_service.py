import os
from openai import OpenAI
from typing import Dict, List
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

CLAUSE_ANALYSIS_PROMPT = """
You are a legal assistant analyzing a contract clause. Analyze the following clause and provide:
1. Classification (e.g., Termination, Confidentiality, IP Ownership, Payment, Governing Law)
2. Risk Level (Low, Medium, High)
3. Plain English explanation

Return the results as JSON in this format:
{
    "type": "clause_type",
    "risk": "risk_level",
    "explanation": "plain_english_explanation"
}

CLAUSE:
{clause}
"""

QUERY_PROMPT = """
You are a legal assistant answering questions about a contract. Use the following clauses to answer the user's question.
Provide a clear, concise answer in plain English.

USER QUESTION:
{query}

RELEVANT CLAUSES:
{clauses}
"""

def analyze_clause(clause: str) -> Dict:
    """
    Analyze a single clause using OpenAI's GPT model.
    Returns a dictionary with type, risk, and explanation.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a legal assistant analyzing contract clauses."},
                {"role": "user", "content": CLAUSE_ANALYSIS_PROMPT.format(clause=clause)}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        # Parse the response
        analysis = json.loads(response.choices[0].message.content)
        
        # Add the original clause to the response
        analysis['clause'] = clause
        
        return analysis
    except Exception as e:
        raise Exception(f"Error analyzing clause with OpenAI: {str(e)}")

def answer_query(query: str, clauses: List[Dict]) -> str:
    """
    Answer a user's question about the contract using relevant clauses.
    """
    try:
        # Format clauses for the prompt
        formatted_clauses = "\n\n".join([
            f"Clause: {c['clause']}\nType: {c['type']}\nRisk: {c['risk']}\nExplanation: {c['explanation']}"
            for c in clauses
        ])
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a legal assistant answering questions about contracts."},
                {"role": "user", "content": QUERY_PROMPT.format(
                    query=query,
                    clauses=formatted_clauses
                )}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error answering query with OpenAI: {str(e)}") 