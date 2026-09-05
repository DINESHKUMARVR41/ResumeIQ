from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.resume_parser import parse_resume

app = FastAPI(title="ResumeIQ API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_and_page_count(data: bytes):
    """Read a PDF from raw bytes and return (text, page_count).

    Raises HTTPException on invalid/corrupted PDFs so the caller doesn't
    have to worry about pypdf-specific exceptions.
    """
    try:
        reader = PdfReader(BytesIO(data))
    except PdfReadError:
        raise HTTPException(status_code=422, detail="The uploaded file is not a valid PDF.")

    page_count = len(reader.pages)
    text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    return text, page_count


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ResumeIQ API"}


@app.post("/api/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    # --- File validation ---
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    # --- PDF reading ---
    text, page_count = extract_text_and_page_count(data)

    if not text:
        raise HTTPException(
            status_code=422,
            detail="No selectable text was found. OCR support will be added in a later module.",
        )

    # --- Parsing (delegated to resume_parser.py) ---
    resume = parse_resume(text)

    # --- Response ---
    return {
        "file": {
            "filename": file.filename,
            "pages": page_count,
        },
        "resume": resume,
    }
