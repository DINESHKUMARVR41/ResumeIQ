# ResumeIQ — AI Resume Intelligence

A clean HTML/CSS/JavaScript + FastAPI foundation for an AI-powered resume intelligence platform.

## Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python + FastAPI
- PDF extraction: pypdf

## Current features

- Resume upload UI
- PDF validation
- PDF text extraction
- Basic name/email/phone detection
- Basic skill detection
- Resume section detection
- Basic resume content score
- Frontend dashboard

## Run the backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Run the frontend

Open `frontend/index.html` in a browser. For best results, use VS Code Live Server.

## Planned modules

1. Better resume parser
2. Job description analysis
3. ATS matching
4. Skill-gap analysis
5. LLM analysis
6. Resume improvement
7. Agent orchestration
8. Database and authentication
9. Production deployment

The advanced modules are intentionally not implemented in this starter.
