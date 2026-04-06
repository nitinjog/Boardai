# BoardAI – CBSE Mock Test Platform

AI-powered mock test generation and evaluation for CBSE Class 10 & 12 students.  
Built with FastAPI · React · Google Gemini · ChromaDB · Tailwind CSS

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free Google Gemini API key → [Google AI Studio](https://aistudio.google.com/app/apikey)

---

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY

# Seed vector database with CBSE question bank
python data/seed_chroma.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```

API is now running at **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

---

### 2. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

App is now running at **http://localhost:5173**

The Vite dev server proxies `/api` requests to `localhost:8000` automatically.

---

## App Flow

```
Student Profile → Diagnostic Assessment → Generate Mock Test
    → Online Test (timed) OR Download PDF
    → Submit / Upload Scan → AI Evaluation → Report + Study Plan
```

1. **Profile** – Name, Class (10/12), Subject selection
2. **Diagnostic** – 7–10 self-assessment questions per subject (instant, no API call)
3. **Test Generation** – Gemini + ChromaDB RAG creates a personalised CBSE-pattern paper (15–30 seconds)
4. **Online Mode** – Timed test with auto-save, anti-copy controls, navigator sidebar
5. **Offline Mode** – Download question paper PDF, write answers by hand, upload a scan
6. **Evaluation** – Gemini grades all answers, identifies error types, builds topic-wise scores
7. **Report** – Score breakdown, topic chart (Recharts), Q-by-Q feedback, 4-week study plan PDF

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/students` | Create student profile |
| GET | `/api/v1/students/{id}` | Get student |
| POST | `/api/v1/diagnostics/start` | Start diagnostic, get questions |
| POST | `/api/v1/diagnostics/submit` | Submit responses, get analysis |
| POST | `/api/v1/tests/generate` | Generate Gemini mock test |
| GET | `/api/v1/tests/{id}` | Get test with questions |
| POST | `/api/v1/tests/{id}/start` | Mark test started |
| GET | `/api/v1/tests/{id}/download-pdf` | Download question paper PDF |
| POST | `/api/v1/tests/{id}/submit` | Submit online answers |
| POST | `/api/v1/evaluation/evaluate/{id}` | Trigger AI evaluation |
| POST | `/api/v1/evaluation/upload-scan` | Upload scanned answer sheet |
| GET | `/api/v1/reports/test/{testId}` | Get evaluation report |
| GET | `/api/v1/reports/{id}/download-pdf` | Download report PDF |
| GET | `/api/v1/reports/student/{id}` | Get test history |

---

## Environment Variables

**`backend/.env`**

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | **Required** — Google AI Studio API key | — |
| `DATABASE_URL` | SQLite database path | `sqlite:///./boardai.db` |
| `CHROMA_PERSIST_DIR` | ChromaDB storage directory | `./chroma_data` |
| `UPLOAD_DIR` | Uploaded answer sheets | `./uploads` |
| `PDF_OUTPUT_DIR` | Generated PDF files | `./generated_pdfs` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |

---

## Vector Database (ChromaDB)

The knowledge base is seeded from `backend/data/cbse_knowledge_base.py` which contains ~35 representative CBSE Q&A pairs across all subjects.

To add more content:
```python
# backend/data/cbse_knowledge_base.py
CBSE_QUESTIONS = [
    {
        "id": "unique_id",
        "text": "Q: Question text\nA: Answer text",
        "class_level": 10,
        "subject": "Mathematics",
        "topic": "Algebra",
        "type": "short_answer",
        "marks": 3,
    },
    ...
]
```

Then re-run: `python data/seed_chroma.py`

---

## Deployment

### Frontend → Netlify
```bash
cd frontend
npm run build
# Deploy dist/ to Netlify
```
Set environment: `VITE_API_BASE_URL=https://your-backend.onrender.com/api/v1`

### Backend → Render
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add environment variables in Render dashboard

**Note**: ChromaDB `chroma_data/` and uploaded files need persistent disk on Render (paid) or use a cloud bucket for production.

---

## Project Structure

```
boardai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── config.py            # Settings from .env
│   │   ├── database/
│   │   │   ├── db.py            # SQLAlchemy engine + get_db()
│   │   │   └── models.py        # ORM models
│   │   ├── schemas/schemas.py   # Pydantic schemas
│   │   ├── routes/              # API route handlers
│   │   ├── services/
│   │   │   ├── gemini_service.py   # Gemini API calls
│   │   │   ├── rag_service.py      # ChromaDB RAG
│   │   │   ├── pdf_service.py      # reportlab PDFs
│   │   │   └── upload_service.py   # File handling
│   │   └── utils/cbse_constants.py # CBSE syllabus data
│   ├── data/
│   │   ├── cbse_knowledge_base.py  # Seed content
│   │   └── seed_chroma.py          # Seeding script
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx              # Router
        ├── api/                 # Axios API layer
        ├── store/               # Zustand state
        ├── hooks/useTimer.js    # Countdown timer
        ├── pages/               # Route-level pages
        └── components/          # Shared UI components
```

---

## Subjects Supported

| Class 10 | Class 12 |
|----------|----------|
| Mathematics | Physics |
| Science | Chemistry |
| Social Science | Mathematics |
| English | Biology |
| Hindi | English |
| | Economics |
| | Accountancy |
| | Business Studies |
