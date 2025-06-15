# Contract Guard

A full-stack web application for analyzing legal contracts using local LLMs. Contract Guard helps users understand their contracts by breaking them down into clauses, classifying them, and providing plain English explanations.

## Features

- Upload and analyze legal contracts (PDF, DOCX, TXT)
- Extract and classify individual clauses
- Risk level assessment
- Plain English explanations
- Interactive dashboard with visualizations
- Dark mode support
- Completely offline operation
- No API keys required

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- CUDA-capable GPU (recommended for better performance)

## Installation

### Backend Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

## Running the Application

### Start the Backend

1. Activate the virtual environment (if not already activated):

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the Flask server:

```bash
python backend/app.py
```

The backend will be available at `http://localhost:5000`

### Start the Frontend

1. In a new terminal, navigate to the frontend directory:

```bash
cd frontend
```

2. Start the development server:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Drag and drop a contract file (PDF, DOCX, or TXT) or click to select one
3. Wait for the analysis to complete
4. View the results in the interactive dashboard
5. Review individual clauses with their classifications and explanations

## Technical Details

### Backend

- Flask web framework
- HuggingFace Transformers for local LLM inference
- PDF and DOCX parsing
- Clause extraction and classification

### Frontend

- React.js
- Tailwind CSS for styling
- Chart.js for visualizations
- Framer Motion for animations
- Dark mode support

## Performance Tips

- For faster inference, use a CUDA-capable GPU
- The application uses FLAN-T5-XL by default, but you can modify the model in `backend/models/classify_llm.py`
- For better performance on CPU, consider using quantized models

## License

MIT License
