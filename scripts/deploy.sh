#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required commands are available
check_requirements() {
    print_status "Checking requirements..."
    
    commands=("python" "pip" "node" "npm" "git")
    for cmd in "${commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            print_error "$cmd is required but not installed"
            exit 1
        fi
    done
}

# Setup Python environment
setup_python() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r backend/requirements.txt
    
    # Download spaCy model
    python -m spacy download en_core_web_sm
}

# Setup Node environment
setup_node() {
    print_status "Setting up Node environment..."
    
    # Install dependencies
    cd frontend
    npm install
    cd ..
}

# Generate secure keys
generate_keys() {
    print_status "Generating secure keys..."
    
    # Generate Flask secret key
    FLASK_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
    
    # Update .env files
    sed -i "s/FLASK_SECRET_KEY=.*/FLASK_SECRET_KEY=$FLASK_SECRET_KEY/" backend/.env
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    cd backend
    python -m pytest tests/
    cd ..
    
    # Frontend tests
    cd frontend
    npm test
    cd ..
}

# Build for production
build_production() {
    print_status "Building for production..."
    
    # Build frontend
    cd frontend
    npm run build
    cd ..
    
    # Create production requirements
    pip freeze > backend/requirements.prod.txt
}

# Main deployment function
deploy() {
    print_status "Starting deployment..."
    
    # Check requirements
    check_requirements
    
    # Setup environments
    setup_python
    setup_node
    
    # Generate keys
    generate_keys
    
    # Run tests
    run_tests
    
    # Build for production
    build_production
    
    print_status "Deployment completed successfully!"
}

# Handle errors
trap 'print_error "Deployment failed!"' ERR

# Run deployment
deploy 