# AI-Powered Resume Analyzer

A full-stack web application that uses AI to analyze resumes and provide personalized feedback, improvements, and keyword optimization suggestions. Built with React, FastAPI, PostgreSQL, and OpenAI GPT-4.

## Features

- 🔐 **Full Authentication System**: JWT-based authentication with secure password hashing
- 📄 **PDF Resume Upload**: Drag-and-drop interface for uploading resume PDFs
- 🤖 **AI-Powered Analysis**: GPT-4 powered resume analysis with:
  - Overall score (0-100)
  - Structure and formatting feedback
  - Keyword optimization suggestions
  - ATS (Applicant Tracking System) optimization tips
  - Personalized improvement recommendations
- 📝 **Improved Resume Generation**: Get an AI-generated improved version of your resume
- 📥 **PDF Export**: Export the improved resume as a professionally formatted PDF
- 🐳 **Dockerized**: Fully containerized multi-service application
- 🎨 **Modern UI**: Beautiful, responsive interface built with Chakra UI

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
│ PG   │ │   API    │
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
   ```env
   DB_PASSWORD=your_secure_password_here
   SECRET_KEY=your_jwt_secret_key_here
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```
   
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

1. **Register/Login**: Create an account or sign in with existing credentials
2. **Upload Resume**: Drag and drop your resume PDF or click to browse
3. **Review Analysis**: View your resume score and detailed feedback
4. **Edit Improved Version**: Review and customize the AI-generated improved resume
5. **Export PDF**: Download the improved resume as a professional PDF

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

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_PASSWORD` | PostgreSQL database password | Yes |
| `SECRET_KEY` | JWT secret key for token signing | Yes |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- File size limits (5MB max)
- SQL injection protection (SQLAlchemy ORM)
- Environment variable validation

## Features for Recruiters

This project demonstrates:

- ✅ Full-stack development skills (React + FastAPI)
- ✅ Database design and ORM usage (PostgreSQL + SQLAlchemy)
- ✅ RESTful API design with OpenAPI documentation
- ✅ Authentication and authorization (JWT)
- ✅ AI/ML integration (OpenAI GPT-4 API)
- ✅ File processing (PDF parsing and generation)
- ✅ Containerization (Docker multi-container app)
- ✅ Modern UI/UX design (Chakra UI)
- ✅ Security best practices

## Future Enhancements

- [ ] Support for multiple resume formats (DOCX, TXT)
- [ ] Resume history and versioning
- [ ] Role-specific analysis templates
- [ ] ATS compatibility checker
- [ ] Resume comparison tool
- [ ] Email notifications
- [ ] Dark mode toggle
- [ ] Multi-language support

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or feedback, please open an issue in the repository.
