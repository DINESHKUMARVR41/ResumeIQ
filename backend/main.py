from io import BytesIO

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.resume_parser import parse_resume
from backend.ats_matcher import analyze_ats_match
from backend.skill_gap import analyze_skill_gap

from backend.career_recommender import (
    analyze_career_recommendations
)

# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="ResumeIQ API",
    description="Backend API for ResumeIQ resume analysis and ATS matching",
    version="0.3.0"
)


# ============================================================
# CORS Configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PDF Text Extraction Helper
# ============================================================

def extract_text_and_page_count(data: bytes):
    """
    Extract selectable text and page count from a PDF.
    """

    try:
        reader = PdfReader(BytesIO(data))

        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

        text = "\n".join(text_parts).strip()

        return text, len(reader.pages)

    except PdfReadError:
        raise HTTPException(
            status_code=422,
            detail="The uploaded file is not a valid PDF."
        )

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Could not read the PDF file."
        )


# ============================================================
# Health Check
# ============================================================

@app.get("/api/health")
async def health_check():
    """
    Check whether the ResumeIQ backend is running.
    """

    return {
        "status": "ok",
        "service": "ResumeIQ API",
        "version": "0.3.0"
    }


# ============================================================
# Resume Analysis
# ============================================================

@app.post("/api/resume/analyze")
async def analyze_resume(
    file: UploadFile = File(...)
):
    """
    Upload and analyze a resume PDF.
    """

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No resume selected."
        )

    # --------------------------------------------------------
    # Validate PDF extension
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded resume is empty."
        )

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    resume_text, page_count = extract_text_and_page_count(data)

    # --------------------------------------------------------
    # Check whether PDF contains selectable text
    # --------------------------------------------------------

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No selectable text was found in the PDF. "
                "OCR will be added in a future module."
            )
        )

    # --------------------------------------------------------
    # Parse resume
    # --------------------------------------------------------

    parsed_resume = parse_resume(resume_text)

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "file": {
            "filename": file.filename,
            "pages": page_count
        },
        "resume": parsed_resume
    }


# ============================================================
# ATS Analysis
# ============================================================

@app.post("/api/ats/analyze")
async def analyze_ats(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Compare a resume against a job description.
    """

    # --------------------------------------------------------
    # Validate resume filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No resume selected."
        )

    # --------------------------------------------------------
    # Validate PDF
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description."
        )

    # --------------------------------------------------------
    # Read uploaded resume
    # --------------------------------------------------------

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded resume is empty."
        )

    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    resume_text, page_count = extract_text_and_page_count(data)

    # --------------------------------------------------------
    # Check for selectable text
    # --------------------------------------------------------

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No selectable text was found in the PDF. "
                "OCR will be added in a future module."
            )
        )

    # --------------------------------------------------------
    # Parse existing resume
    # --------------------------------------------------------

    parsed_resume = parse_resume(resume_text)

    # --------------------------------------------------------
    # Run ATS analysis
    # --------------------------------------------------------

    ats_result = analyze_ats_match(
        resume_text=resume_text,
        resume_skills=parsed_resume.get("skills", []),
        job_description=job_description
    )

    # --------------------------------------------------------
    # Return ATS result
    # --------------------------------------------------------

    return {
        "file": {
            "filename": file.filename,
            "pages": page_count
        },
        "ats": ats_result
    }
# ============================================================
# Skill Gap Analysis
# ============================================================

@app.post("/api/skill-gap/analyze")
async def analyze_skill_gap_api(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze the skill gap between a resume
    and a job description.
    """

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No resume selected."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description."
        )

    # --------------------------------------------------------
    # Read file
    # --------------------------------------------------------

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded resume is empty."
        )

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    resume_text, page_count = (
        extract_text_and_page_count(data)
    )

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No selectable text was found in the PDF. "
                "OCR will be added in a future module."
            )
        )

    # --------------------------------------------------------
    # Parse resume
    # --------------------------------------------------------

    parsed_resume = parse_resume(
        resume_text
    )

    resume_skills = parsed_resume.get(
        "skills",
        []
    )

    # --------------------------------------------------------
    # Extract required skills from JD
    # --------------------------------------------------------

    ats_result = analyze_ats_match(
        resume_text=resume_text,
        resume_skills=resume_skills,
        job_description=job_description
    )

    required_skills = (
        ats_result
        .get("skills", {})
        .get("required", [])
    )

    # --------------------------------------------------------
    # Analyze skill gap
    # --------------------------------------------------------

    skill_gap_result = analyze_skill_gap(
        resume_skills=resume_skills,
        required_skills=required_skills
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "file": {
            "filename": file.filename,
            "pages": page_count
        },

        "skill_gap": skill_gap_result
    }
# =====================================================
# MODULE 05 — AI CAREER RECOMMENDATIONS
# =====================================================

@app.post("/api/career/recommend")
async def recommend_career(
    file: UploadFile = File(...)
):

    try:

        data = await file.read()

        text, page_count = extract_text_and_page_count(
            data
        )

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume."
            )

        # Extract resume skills
        resume_skills = detect_skills(text)

        # Generate career recommendations
        result = analyze_career_recommendations(
            resume_text=text,
            resume_skills=resume_skills
        )

        return {
            "success": True,

            "resume": {
                "skills": resume_skills,
                "page_count": page_count
            },

            "career": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Career recommendation failed: {str(e)}"
        )