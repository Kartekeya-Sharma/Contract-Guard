from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
import time
import traceback
from utils.document_parser import parse_document
from utils.chunker import split_into_clauses
from models.classify_llm import classify_clause

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path):
    """Process the uploaded file and return analysis results"""
    try:
        # Extract text from document
        logger.info('Extracting text from document')
        text = parse_document(file_path)
        logger.info(f"Text extracted successfully from {file_path}")
        
        # Split into clauses
        logger.info('Splitting text into clauses')
        clauses = split_into_clauses(text)
        logger.info(f"Text split into {len(clauses)} clauses")
        
        # Classify each clause
        results = []
        for i, clause in enumerate(clauses, 1):
            try:
                logger.info(f'Classifying clause {i}/{len(clauses)}')
                classification = classify_clause(clause)
                results.append({
                    'text': clause,
                    'type': classification['type'],
                    'risk_level': classification['risk_level'],
                    'explanation': classification['explanation'],
                    'specific_concerns': classification['specific_concerns']
                })
                logger.info(f"Clause {i}/{len(clauses)} classified successfully")
            except Exception as e:
                logger.error(f"Error classifying clause {i}: {str(e)}")
                results.append({
                    'text': clause,
                    'type': 'Error',
                    'risk_level': 'Unknown',
                    'explanation': f'Error in classification: {str(e)}',
                    'specific_concerns': ['Error occurred during classification']
                })
        
        return {
            'status': 'success',
            'message': 'File processed successfully',
            'clauses': results
        }
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'status': 'error',
            'message': f'Error processing file: {str(e)}',
            'clauses': []
        }

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return '', 200

    start_time = time.time()
    logger.info("Upload request received")
    
    try:
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        logger.info(f"Received file: {file.filename}")
        
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logger.info(f"Saving file to: {file_path}")
        file.save(file_path)
        logger.info("File saved successfully")
        
        # Process the file
        logger.info("Starting file processing")
        result = process_file(file_path)
        logger.info(f"File processing completed: {result}")
        
        end_time = time.time()
        logger.info(f"Total processing time: {end_time - start_time:.2f} seconds")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    logger.info('Starting Flask application')
    app.run(debug=True, host='0.0.0.0', port=5001) 