# Contract Guard

Contract Guard is an AI-powered web application that helps users analyze legal contracts. It extracts clauses from uploaded documents (PDF, DOCX, TXT), classifies them, assesses risk levels, and provides plain English explanations using OpenAI's GPT.

## Features

- 📄 Upload and analyze contracts (PDF, DOCX, TXT)
- 🔍 Extract and classify individual clauses
- ⚠️ Risk assessment (Low, Medium, High)
- 💡 Plain English explanations using GPT
- 📊 Interactive dashboard with charts
- 💬 Ask questions about your contract
- 🌙 Dark mode support
- 📱 Fully responsive design

## Tech Stack

### Frontend

- React.js with Vite
- Tailwind CSS for styling
- Recharts for data visualization
- React Query for data fetching
- React Dropzone for file uploads

### Backend

- Python Flask
- OpenAI GPT API
- pdfminer.six for PDF processing
- python-docx for DOCX processing
- spaCy for NLP

## Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Kartekeya-Sharma/contract-guard.git
cd contract-guard
```

2. Set up the backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Set up the frontend:

```bash
cd frontend
npm install
```

4. Create environment files:

Backend (.env):

```
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
```

Frontend (.env):

```
VITE_API_URL=http://localhost:5000
```

## Running Locally

1. Start the backend:

```bash
cd backend
flask run
```

2. Start the frontend:

```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:5173

## Deployment

### Backend (Render)

1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Set start command: `gunicorn app:app`
5. Add environment variables:
   - OPENAI_API_KEY
   - FLASK_ENV=production

### Frontend (Render)

1. Create a new Static Site
2. Connect your GitHub repository
3. Set build command: `cd frontend && npm install && npm run build`
4. Set publish directory: `frontend/dist`
5. Add environment variables:
   - VITE_API_URL (your backend URL)

## Docker Support

Build and run with Docker Compose:

```bash
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT API
- The open-source community for amazing tools and libraries
- All contributors who help improve this project
