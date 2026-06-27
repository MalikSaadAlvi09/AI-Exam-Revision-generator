# AI-Exam-Revision-generator

AI Exam Revision Generator is a full-stack AI web application that converts PDFs, slides, documents, and notes into MCQs, flashcards, summaries, cheat sheets, and 10-minute revision guides using Google Gemini AI.

## Project Structure

- `/backend` - FastAPI API, JWT auth, SQLAlchemy models, text extraction and Gemini generation services.
- `/frontend` - Static modern UI pages with glassmorphism styling, upload flow, dashboard, and revision outputs.

## Backend Setup

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start API:
   ```bash
   uvicorn backend.main:app --reload
   ```

## Key API Endpoints

- `POST /register`
- `POST /login`
- `GET /profile`
- `POST /upload`
- `POST /generate`
- `GET /summary`
- `GET /mcqs`
- `GET /flashcards`
- `GET /important`
- `GET /revision`
- `GET /cheatsheet`
- `GET /history`
- `DELETE /history`
