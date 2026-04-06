# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BoardAI** – AI-powered CBSE mock test platform for Class 10 and Class 12 students. Students complete a diagnostic, receive a Gemini-generated mock test, attempt it online or offline, and get AI evaluation with improvement plans.

## Commands

### Backend (Python FastAPI)
```bash
cd backend
python -m venv venv && venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env                             # add GEMINI_API_KEY
python data/seed_chroma.py                       # seed vector DB (run once)
uvicorn app.main:app --reload --port 8000        # dev server
```
API docs: http://localhost:8000/docs

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev          # dev server on port 5173
npm run build        # production build to dist/
npm run preview      # preview production build
```

## Architecture

### Backend (`backend/`)
- **`app/main.py`** – FastAPI app factory; registers all routers under `/api/v1`, configures CORS, mounts `/pdfs` static files, calls `init_db()` on startup
- **`app/config.py`** – Pydantic `Settings` reading from `.env`; all config accessed via `from app.config import settings`
- **`app/database/db.py`** – SQLAlchemy engine + `SessionLocal` + `get_db()` dependency + `init_db()` (called at startup, creates tables)
- **`app/database/models.py`** – All ORM models: `Student`, `DiagnosticSession`, `TestSession`, `StudentAnswer`, `EvaluationReport`; JSON fields stored as serialised strings (SQLite compatible)
- **`app/schemas/schemas.py`** – All Pydantic request/response schemas
- **`app/routes/`** – Route handlers (thin, delegate to services):
  - `profile.py` → `/api/v1/students`
  - `diagnostic.py` → `/api/v1/diagnostics`
  - `test.py` → `/api/v1/tests`
  - `evaluation.py` → `/api/v1/evaluation`
  - `feedback.py` → `/api/v1/reports`
- **`app/services/gemini_service.py`** – All Gemini API calls; returns parsed dicts; includes `_extract_json()` to handle markdown code fences in LLM responses
- **`app/services/rag_service.py`** – ChromaDB client (singleton pattern with `_client`/`_collection` globals); `query_context()` filters by `class_level` and `subject` metadata
- **`app/services/pdf_service.py`** – reportlab PDF generation for question papers and evaluation reports
- **`app/services/upload_service.py`** – File validation and saving for scanned answer sheets
- **`app/utils/cbse_constants.py`** – CBSE syllabus data, `PAPER_STRUCTURE`, diagnostic question templates; `get_diagnostic_questions(subject)` is the source of truth for diagnostic flow (no Gemini call)
- **`data/cbse_knowledge_base.py`** – Sample CBSE Q&A pairs for ChromaDB seeding
- **`data/seed_chroma.py`** – Run once to populate ChromaDB; safe to re-run (uses `upsert`)

### Frontend (`frontend/src/`)
- **`App.jsx`** – `createBrowserRouter` with all routes; `Protected` component wraps authenticated routes
- **`store/useStudentStore.js`** – Zustand with `persist` middleware; stores `student` and `diagnostics` map in localStorage; `isLoggedIn()` drives Protected routes
- **`store/useTestStore.js`** – Ephemeral test state (current test, answers dict, timer); reset on unmount
- **`api/client.js`** – Axios instance with base URL `/api/v1`, student ID header injection, error normalisation
- **`hooks/useTimer.js`** – Countdown timer synced to `useTestStore`; calls `onExpire` when time runs out
- **`constants/cbse_constants.js`** → mirror of backend constants for subject/class display
- **Pages flow**: `HomePage` → `OnboardingPage` → `DashboardPage` → `DiagnosticPage` → `GenerateTestPage` → `TestModePage` → `OnlineTestPage` OR `UploadPage` → `EvaluatePage` → `ResultsPage`

### AI / Data Flow
1. **Diagnostic** – Questions served from `cbse_constants.py` (no Gemini); responses analysed by `gemini_service.analyze_diagnostic_responses()`
2. **Test generation** – `rag_service.query_context()` retrieves relevant CBSE content from ChromaDB → passed as context to `gemini_service.generate_mock_test()`; Gemini returns JSON parsed by `_extract_json()`
3. **Evaluation** – All Q+A pairs batched into one `gemini_service.evaluate_answers()` call; per-question scores + topic analysis returned
4. **Improvement plan** – Separate `gemini_service.generate_improvement_plan()` call using evaluation summary

## Key Conventions

- **JSON in SQLite**: `subjects`, `sections`, `weak_topics`, etc. are stored as `json.dumps()` strings in `Text` columns; decoded with `json.loads()` in routes
- **Gemini JSON parsing**: Always use `_extract_json()` — Gemini wraps JSON in markdown code fences
- **ChromaDB singleton**: `get_client()` and `get_collection()` return cached globals; don't create new clients per request
- **Free tier limits**: Gemini `gemini-1.5-flash` is used (fastest free model); test generation takes 15-30s; client axios timeout is set to 120s

## Environment Variables (backend/.env)
```
GEMINI_API_KEY=       # Required — get from Google AI Studio
DATABASE_URL=sqlite:///./boardai.db
CHROMA_PERSIST_DIR=./chroma_data
UPLOAD_DIR=./uploads
PDF_OUTPUT_DIR=./generated_pdfs
CORS_ORIGINS=http://localhost:5173
```
