from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from pypdf import PdfReader
import re

app = FastAPI(title="ResumeIQ API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KNOWN_SKILLS = [
    "python", "java", "c++", "javascript", "typescript",
    "react", "node.js", "django", "flask", "fastapi",
    "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "git", "github", "docker", "aws", "azure",
]

SECTIONS = [
    "summary", "objective", "education", "experience",
    "skills", "projects", "certifications", "achievements"
]

def extract_text(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

def find_email(text):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else ""

def find_phone(text):
    match = re.search(r"(?:\+?\d[\d\s().-]{8,}\d)", text)
    return match.group(0).strip() if match else ""

def find_name(text):
    for line in text.splitlines():
        line = line.strip()
        words = line.split()
        if line and "@" not in line and not any(ch.isdigit() for ch in line):
            if 2 <= len(words) <= 5 and all(w.replace("-", "").isalpha() for w in words):
                return line
    return ""

def analyze(text):
    lowered = text.lower()
    skills = sorted({s for s in KNOWN_SKILLS if s.lower() in lowered})
    sections = [s.title() for s in SECTIONS if s in lowered]
    score = round(len(sections) / len(SECTIONS) * 100)

    return {
        "resume": {
            "name": find_name(text),
            "email": find_email(text),
            "phone": find_phone(text),
            "skills": skills,
        },
        "analysis": {
            "score": score,
            "word_count": len(text.split()),
            "detected_sections": sections,
        },
    }

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ResumeIQ API"}

@app.post("/api/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file.")

    text = extract_text(data)
    if not text:
        raise HTTPException(status_code=422, detail="No readable text found in PDF.")

    return analyze(text)
