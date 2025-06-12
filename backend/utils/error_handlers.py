from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = 500, payload: Dict[str, Any] = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

class FileProcessingError(APIError):
    """Raised when there's an error processing uploaded files"""
    def __init__(self, message: str, payload: Dict[str, Any] = None):
        super().__init__(message, status_code=400, payload=payload)

class OpenAIError(APIError):
    """Raised when there's an error with OpenAI API"""
    def __init__(self, message: str, payload: Dict[str, Any] = None):
        super().__init__(message, status_code=503, payload=payload)

class ValidationError(APIError):
    """Raised when input validation fails"""
    def __init__(self, message: str, payload: Dict[str, Any] = None):
        super().__init__(message, status_code=400, payload=payload)

def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        """Handle API errors"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        """Handle HTTP errors"""
        response = jsonify({
            'status': 'error',
            'message': error.description,
            'code': error.code
        })
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        """Handle all other errors"""
        # Log the full traceback
        logger.error(f"Unhandled error: {str(error)}")
        logger.error(traceback.format_exc())
        
        response = jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'code': 500
        })
        response.status_code = 500
        return response

def validate_file(file, allowed_extensions: set, max_size: int) -> None:
    """Validate uploaded file"""
    if not file:
        raise ValidationError("No file provided")
    
    if file.filename == '':
        raise ValidationError("No file selected")
    
    if not '.' in file.filename or \
       file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        raise ValidationError(
            f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    if file.content_length and file.content_length > max_size:
        raise ValidationError(f"File size exceeds maximum limit of {max_size/1024/1024}MB")

def handle_openai_error(error: Exception) -> None:
    """Handle OpenAI API errors"""
    error_message = str(error)
    if "rate_limit" in error_message.lower():
        raise OpenAIError("OpenAI API rate limit exceeded. Please try again later.")
    elif "authentication" in error_message.lower():
        raise OpenAIError("OpenAI API authentication failed. Please check your API key.")
    else:
        raise OpenAIError(f"OpenAI API error: {error_message}") 