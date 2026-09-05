"""
resume_parser.py

All resume parsing/extraction/scoring logic lives here.
main.py stays responsible for the API, file handling, and PDF reading only.

Public entry point: parse_resume(text)
"""

import re

# --------------------------------------------------------------------------
# 1. SKILLS
# --------------------------------------------------------------------------

# Centralized skill list. Keys are lowercase for matching; values are the
# "pretty" display form returned to the frontend.
KNOWN_SKILLS = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "c#": "C#",
    "c": "C",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "node.js": "Node.js",
    "express": "Express",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "firebase": "Firebase",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "computer vision": "Computer Vision",
    "aws": "AWS",
    "azure": "Azure",
    "google cloud": "Google Cloud",
    "gcp": "GCP",
    "streamlit": "Streamlit",
}

# Skills that are single letters or very short tokens need word-boundary
# matching, otherwise "c" would match inside "certificate", "javascript", etc.
_SHORT_SKILLS = {"c", "c++", "c#", "r"}


def detect_skills(text: str) -> list:
    """Scan the resume text and return the list of known skills found.

    Case-insensitive. No duplicates. Uses word boundaries for short/ambiguous
    tokens (like "C") to avoid false positives inside other words.
    """
    lowered = text.lower()
    found = []

    for key, display_name in KNOWN_SKILLS.items():
        if key in _SHORT_SKILLS:
            # Word-boundary match only, e.g. standalone "C" not "css" or "certificate"
            pattern = r"(?<![a-zA-Z0-9+#.])" + re.escape(key) + r"(?![a-zA-Z0-9+#.])"
            if re.search(pattern, lowered):
                found.append(display_name)
        else:
            if key in lowered:
                found.append(display_name)

    # Preserve order, remove any accidental duplicates
    seen = set()
    unique_found = []
    for skill in found:
        if skill not in seen:
            seen.add(skill)
            unique_found.append(skill)

    return unique_found


# --------------------------------------------------------------------------
# 2. SECTIONS
# --------------------------------------------------------------------------

# Maps section header variations -> normalized section name.
SECTION_ALIASES = {
    "summary": [
        "summary", "professional summary", "profile", "objective", "career objective",
    ],
    "education": [
        "education", "academic background", "qualifications",
    ],
    "experience": [
        "experience", "work experience", "employment", "professional experience",
    ],
    "skills": [
        "skills", "technical skills", "technologies", "technical expertise",
    ],
    "projects": [
        "projects", "academic projects", "personal projects",
    ],
    "certifications": [
        "certifications", "certificates", "licenses",
    ],
    "achievements": [
        "achievements", "awards", "accomplishments",
    ],
    "interests": [
        "interests", "hobbies", "activities",
    ],
}


def detect_sections(text: str) -> list:
    """Detect which resume sections are present, normalized to a canonical
    lowercase name (e.g. "Professional Experience" -> "experience").

    Matching is done against whole lines to reduce false positives (so the
    word "summary" appearing mid-sentence in a paragraph is less likely to
    be mistaken for a section header than a short line that IS the header).
    """
    lowered_lines = [line.strip().lower() for line in text.splitlines()]
    found_sections = []

    for normalized_name, variations in SECTION_ALIASES.items():
        for line in lowered_lines:
            # Strip trailing punctuation/colons resumes often use after headers
            cleaned_line = line.rstrip(":").strip()
            if cleaned_line in variations:
                found_sections.append(normalized_name)
                break

    # Fallback: if nothing matched as a standalone line, fall back to a looser
    # substring search so we still detect something on messily formatted PDFs.
    if not found_sections:
        lowered_text = text.lower()
        for normalized_name, variations in SECTION_ALIASES.items():
            if any(variation in lowered_text for variation in variations):
                found_sections.append(normalized_name)

    return found_sections


# --------------------------------------------------------------------------
# 3. CONTACT INFO: EMAIL / PHONE / NAME
# --------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Basic normalization: collapse excess whitespace, keep line breaks."""
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_email(text: str):
    """Return the first email address found, or None."""
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else None


def extract_phone(text: str):
    """Return the first phone number found, or None.

    Supports Indian formats (+91 9876543210, +91-9876543210, 9876543210)
    as well as reasonable general international formats.
    """
    patterns = [
        r"\+91[-\s]?\d{5}[-\s]?\d{5}",   # +91 9876543210 / +91-98765-43210
        r"\+91[-\s]?\d{10}",             # +91 9876543210 (no split)
        r"\b[6-9]\d{9}\b",               # bare 10-digit Indian mobile number
        r"\+?\d{1,3}[-\s]?\(?\d{2,4}\)?[-\s]?\d{3,4}[-\s]?\d{3,4}",  # generic international
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return None


def extract_name(text: str):
    """Heuristic name extraction: assume the candidate's name is near the
    top of the resume, on its own line, made up of 2-4 alphabetic words,
    with no digits or email/phone-like content.

    This is NOT reliable for every resume layout. If nothing confident is
    found, return None rather than guessing.
    """
    lines = clean_text(text).splitlines()

    # Only look at the first ~10 lines; names are almost always near the top.
    for line in lines[:10]:
        if "@" in line or any(ch.isdigit() for ch in line):
            continue

        words = line.split()
        if 2 <= len(words) <= 4 and all(
            word.replace("-", "").replace(".", "").isalpha() for word in words
        ):
            # Avoid matching section headers or generic labels
            if line.strip().lower() not in _ALL_SECTION_WORDS():
                return line.strip()

    return None


def _ALL_SECTION_WORDS():
    """Flatten all section alias strings for quick membership checks."""
    words = set()
    for variations in SECTION_ALIASES.values():
        words.update(variations)
    return words


# --------------------------------------------------------------------------
# 4. EDUCATION
# --------------------------------------------------------------------------

# Each pattern uses word boundaries so short keywords like "me" (M.E.) don't
# accidentally match inside unrelated words like "resume".
DEGREE_PATTERNS = [
    r"\bb\.?e\.?\b", r"\bb\.?tech\b", r"\bm\.?e\.?\b", r"\bm\.?tech\b",
    r"\bb\.?sc\.?\b", r"\bm\.?sc\.?\b", r"\bbca\b", r"\bmca\b",
    r"\bmba\b", r"\bph\.?d\.?\b",
]
_DEGREE_REGEX = re.compile("|".join(DEGREE_PATTERNS), re.IGNORECASE)


def extract_education(text: str) -> list:
    """Find lines that mention a recognizable degree keyword and return
    them as-is (trimmed). Simple and modular, not a full parser.
    """
    results = []
    for line in clean_text(text).splitlines():
        if _DEGREE_REGEX.search(line):
            trimmed = line.strip()
            if trimmed and trimmed not in results:
                results.append(trimmed)
    return results


# --------------------------------------------------------------------------
# 5. SCORING
# --------------------------------------------------------------------------

def calculate_score(candidate: dict, sections: list, skills: list, education: list) -> dict:
    """Compute a simple, explainable resume score out of 100.

    Breakdown (max points):
      - contact_information:                20
      - sections:                            25
      - skills:                              25
      - projects_or_experience:              20
      - certifications_or_achievements:      10
    """
    # --- Contact information (max 20) ---
    contact_points = 0
    if candidate.get("name"):
        contact_points += 7
    if candidate.get("email"):
        contact_points += 7
    if candidate.get("phone"):
        contact_points += 6

    # --- Sections (max 25) ---
    total_possible_sections = len(SECTION_ALIASES)
    sections_points = round((len(sections) / total_possible_sections) * 25)

    # --- Skills (max 25) ---
    # Cap the "credit" at 10 skills so the score doesn't reward skill-stuffing.
    skills_points = min(len(skills), 10) / 10 * 25
    skills_points = round(skills_points)

    # --- Projects or experience (max 20) ---
    projects_or_experience_points = 0
    if "projects" in sections:
        projects_or_experience_points += 10
    if "experience" in sections:
        projects_or_experience_points += 10

    # --- Certifications or achievements (max 10) ---
    certifications_points = 0
    if "certifications" in sections:
        certifications_points += 5
    if "achievements" in sections:
        certifications_points += 5

    breakdown = {
        "contact_information": contact_points,
        "sections": sections_points,
        "skills": skills_points,
        "projects_or_experience": projects_or_experience_points,
        "certifications_or_achievements": certifications_points,
    }

    total = sum(breakdown.values())
    total = max(0, min(100, total))

    return {
        "total": total,
        "breakdown": breakdown,
    }


# --------------------------------------------------------------------------
# 6. MAIN ENTRY POINT
# --------------------------------------------------------------------------

def parse_resume(text: str) -> dict:
    """Take raw extracted PDF text and return the full structured resume dict.

    This is the single function main.py should call.
    """
    text = text or ""

    candidate = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }

    skills = detect_skills(text)
    sections = detect_sections(text)
    education = extract_education(text)
    score = calculate_score(candidate, sections, skills, education)

    return {
        "candidate": candidate,
        "skills": skills,
        "education": education,
        "sections": sections,
        "score": score,
        "word_count": len(text.split()),
        "character_count": len(text),
    }
