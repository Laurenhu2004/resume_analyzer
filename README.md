# Resume Analyzer

A full-stack web application that uses ChatGPT to provide feedback on resumes and produce improved versions in PDFs. Built with React, FastAPI, PostgreSQL, and OpenAI GPT-4.
Video demo: https://youtu.be/mfhnTMB_L3E?si=vSjRfVzmXSVfHGXc

## Features

- **Full Authentication System**: JWT-based authentication with secure password hashing
- **PDF Resume Upload**: Drag-and-drop interface for uploading resume PDFs
- **AI-Powered Analysis**: GPT-4 powered resume analysis with:
  - Overall score (0-100)
  - Structure and formatting
  - Keyword suggestions
  - ATS optimization tips
  - Personalized improvements
- **Improved Resume Generation**: Get an improved version of your resume
- **PDF Export**: Export the improved resume as a professionally formatted PDF
- **Dockerized**: Fully containerized app

## Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Chakra UI** - Component library
- **React Router** - Routing
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **PyPDF2** - PDF text extraction
- **OpenAI GPT-4** - AI analysis
- **ReportLab** - PDF generation
- **JWT** - Authentication

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Architecture

```
┌─────────────┐
│   Frontend  │ (React + Chakra UI)
│  Port 3000  │
└──────┬──────┘
       │
       │ HTTP/REST
       │
┌──────▼──────┐
│   Backend   │ (FastAPI)
│  Port 8000  │
└──────┬──────┘
       │
    ┌──┴──┐
    │     │
┌───▼──┐ ┌▼─────────┐
│  DB  │ │  OpenAI  │
│  PG  │ │   API    │
└──────┘ └──────────┘
```

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd resume_analyzer
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file** with your configuration:

   **Note**: Generate a secure `SECRET_KEY` using:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

1. **Register/Login**: Create an account or sign in
2. **Upload Resume**: Drag and drop your resume PDF or click to browse
3. **Review Analysis**: View your resume score and detailed feedback
4. **Edit Improved Version**: Review and customize the AI-generated improved resume
5. **Export PDF**: Download the improved resume as a PDF

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user (protected)

### Resume Analysis
- `POST /analyze/upload` - Upload and analyze resume (protected)
- `POST /analyze/improve` - Export improved resume as PDF (protected)

See full API documentation at http://localhost:8000/docs (Swagger UI)

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
resume_analyzer/
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── Dockerfile
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Core config and utilities
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- File size limits (5MB max)
- SQL injection protection (SQLAlchemy ORM)
- Environment variable validation

## License

MIT License
