from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import json
from services.openai_service import analyze_clause, answer_query
from utils.extract_pdf import extract_text_from_pdf
from utils.extract_docx import extract_text_from_docx
from utils.clause_splitter import split_into_clauses
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client.exposition import generate_latest
from utils.error_handlers import (
    register_error_handlers,
    validate_file,
    handle_openai_error,
    APIError
)
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register error handlers
register_error_handlers(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

FILE_PROCESSING_TIME = Histogram(
    'file_processing_seconds',
    'Time spent processing files',
    ['file_type']
)

OPENAI_API_CALLS = Counter(
    'openai_api_calls_total',
    'Total OpenAI API calls',
    ['endpoint', 'status']
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    start_time = time.time()
    
    try:
        if 'file' not in request.files:
            raise APIError("No file provided", status_code=400)
        
        file = request.files['file']
        validate_file(file, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text based on file type
        file_type = filename.rsplit('.', 1)[1].lower()
        with FILE_PROCESSING_TIME.labels(file_type=file_type).time():
            if file_type == 'pdf':
                text = extract_text_from_pdf(filepath)
            elif file_type == 'docx':
                text = extract_text_from_docx(filepath)
            else:  # txt
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
        
        # Split into clauses
        clauses = split_into_clauses(text)
        
        # Analyze each clause
        analyzed_clauses = []
        for clause in clauses:
            try:
                analysis = analyze_clause(clause)
                OPENAI_API_CALLS.labels(endpoint='analyze', status='success').inc()
                analyzed_clauses.append(analysis)
            except Exception as e:
                OPENAI_API_CALLS.labels(endpoint='analyze', status='error').inc()
                handle_openai_error(e)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            "status": "success",
            "clauses": analyzed_clauses
        }), 200
        
    except Exception as e:
        if isinstance(e, APIError):
            raise e
        raise APIError(str(e), status_code=500)
    
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(method='POST', endpoint='/api/analyze').observe(duration)
        REQUEST_COUNT.labels(
            method='POST',
            endpoint='/api/analyze',
            status='200' if 'e' not in locals() else '500'
        ).inc()

@app.route('/api/query', methods=['POST'])
def query_contract():
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            raise APIError("No query provided", status_code=400)
        
        query = data['query']
        answer = answer_query(query)
        OPENAI_API_CALLS.labels(endpoint='query', status='success').inc()
        
        return jsonify({
            'status': 'success',
            'answer': answer
        })
    
    except Exception as e:
        if isinstance(e, APIError):
            raise e
        raise APIError(str(e), status_code=500)
    
    finally:
        duration = time.time() - start_time
        REQUEST_LATENCY.labels(method='POST', endpoint='/api/query').observe(duration)
        REQUEST_COUNT.labels(
            method='POST',
            endpoint='/api/query',
            status='200' if 'e' not in locals() else '500'
        ).inc()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 