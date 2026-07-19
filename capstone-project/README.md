# Capstone Project - AI-Powered Incident Report System

A full-stack incident report system with AI classification, image analysis, RAG-powered Q&A, and PDF report generation.

## Features

| Feature | AI Technique Used |
|---------|------------------|
| Auto-classify incidents | Few-shot + Chain of Thought + JSON output (Module 02) |
| Image analysis | GPT-4o Vision (Module 01) |
| RAG Q&A chat | Embeddings + Vector search + Grounded answers (Module 03) |
| AI Agent processing | ReAct loop + Tool use (Module 04) |
| PDF report generation | Structured prompt + ReportLab |
| AI Analytics | Context window + Pattern detection (Module 01+02) |

## Users

- **Reporter** - Submit incidents, track status, download PDF reports
- **Admin** - Dashboard, Ask AI (RAG), AI Analytics, Monthly Reports

## Setup

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set your API key

Create a `.env` file in the `backend/` folder:

```
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
```

### 3. Run the server

```bash
python run.py
```

### 4. Open in browser

```
http://localhost:5001
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/incidents | Submit new incident (AI Agent processes) |
| GET | /api/incidents | List all incidents (with filters) |
| GET | /api/incidents/:id | Get incident detail |
| PUT | /api/incidents/:id | Update status |
| POST | /api/ai/ask | Ask AI a question (RAG) |
| POST | /api/ai/analytics | AI pattern detection |
| POST | /api/ai/monthly | Generate monthly report |
| GET | /api/stats | Dashboard statistics |
| GET | /api/pdf/:id | Download incident PDF |

## How It Works

```
Reporter submits report (text + optional image)
    |
    v
AI Agent (Module 04) decides what to do:
    1. classify_incident()  - Few-shot + CoT + JSON (Module 02)
    2. analyze_image()      - GPT-4o Vision (Module 01)
    3. save_to_database()   - SQLite storage
    4. generate_report()    - Structured prompt (Module 02)
    5. send_notification()  - Alert response team
    |
    v
RAG (Module 03) enables:
    - Admin asks questions -> semantic search -> grounded answers
    - All incidents stored as vectors in ChromaDB
    - Citations included with every answer
    |
    v
Output:
    - Classified incident (JSON)
    - AI-generated professional report
    - Downloadable PDF
    - Dashboard with statistics
```
