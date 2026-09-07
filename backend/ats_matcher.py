# backend/ats_matcher.py

import re
from collections import Counter

from backend.resume_parser import detect_skills, detect_sections


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    # General English
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "than",
    "so",
    "to",
    "of",
    "in",
    "on",
    "at",
    "by",
    "for",
    "from",
    "with",
    "without",
    "into",
    "through",
    "during",
    "over",
    "under",
    "between",
    "about",
    "against",
    "within",
    "across",
    "after",
    "before",
    "above",
    "below",
    "up",
    "down",
    "out",
    "off",

    # Common verbs
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "should",
    "could",
    "can",
    "may",
    "might",
    "must",

    # Hiring / JD filler
    "work",
    "working",
    "works",
    "worked",
    "role",
    "roles",
    "job",
    "position",
    "candidate",
    "candidates",
    "team",
    "teams",
    "company",
    "organization",
    "organisation",
    "employee",
    "employees",
    "responsible",
    "responsibilities",
    "responsibility",
    "requirement",
    "requirements",
    "required",
    "preferred",
    "prefer",
    "including",
    "include",
    "includes",
    "ability",
    "abilities",
    "looking",
    "seeking",
    "seeks",
    "join",
    "joining",
    "help",
    "support",

    # Generic resume words
    "experience",
    "experienced",
    "skills",
    "skill",
    "knowledge",
    "strong",
    "excellent",
    "good",
    "understanding",
    "understand",
    "using",
    "use",
    "used",
    "develop",
    "developing",
    "developed",
    "development",
    "build",
    "building",
    "built",
    "create",
    "creating",
    "created",
    "design",
    "designing",
    "designed",
    "provide",
    "providing",
    "provided",
    "ensure",
    "ensuring",
    "across",
    "various",
    "multiple",
    "related",
    "relevant",
    "etc",
}


# ============================================================
# IMPORTANT MULTI-WORD PHRASES
# ============================================================

IMPORTANT_PHRASES = {
    # Education
    "computer science",
    "information technology",
    "software engineering",
    "computer engineering",
    "data science",

    # Data / Analytics
    "data analysis",
    "data analytics",
    "data visualization",
    "business intelligence",
    "statistical modeling",
    "statistical analysis",
    "financial forecasting",
    "business insights",
    "predictive analytics",
    "exploratory data analysis",
    "data driven",
    "data-driven",

    # AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",
    "generative ai",
    "reinforcement learning",
    "large language models",
    "language models",

    # Software
    "software development",
    "software engineering",
    "web development",
    "application development",
    "backend development",
    "frontend development",
    "full stack development",
    "api development",
    "rest api",
    "rest apis",
    "object oriented programming",
    "object-oriented programming",
    "problem solving",
    "version control",

    # Cloud / DevOps
    "cloud computing",
    "cloud services",
    "cloud infrastructure",
    "continuous integration",
    "continuous deployment",
    "ci/cd",
    "container orchestration",

    # Databases
    "database management",
    "database design",
    "relational database",
    "relational databases",

    # Business / professional
    "business analysis",
    "business requirements",
    "technical requirements",
    "technical skills",
    "technical knowledge",
    "analytical skills",
    "critical thinking",
    "communication skills",
    "project management",
    "stakeholder management",

    # Job titles
    "senior analyst",
    "data analyst",
    "business analyst",
    "software engineer",
    "software developer",
    "machine learning engineer",
    "data scientist",
    "backend developer",
    "frontend developer",
    "full stack developer",
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text while preserving characters that matter
    for technical terms such as C++, C#, Node.js, CI/CD, etc.
    """

    if not text:
        return ""

    text = text.lower()

    # Normalize common punctuation variations
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')

    # Normalize ampersand
    text = text.replace("&", " and ")

    # Keep letters, numbers, spaces and useful technical symbols
    text = re.sub(r"[^a-z0-9+#./\- ]+", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# TOKEN CLEANING
# ============================================================

def clean_keyword(keyword: str) -> str:
    """
    Clean an extracted keyword or phrase.
    """

    keyword = keyword.strip().lower()

    # Remove unnecessary punctuation at the edges
    keyword = re.sub(r"^[^a-z0-9+#]+", "", keyword)
    keyword = re.sub(r"[^a-z0-9+#./\-]+$", "", keyword)

    # A trailing period is almost always sentence punctuation (e.g. "AWS.")
    # rather than part of the term, so strip it even though "." is kept
    # elsewhere to support terms like "node.js".
    keyword = re.sub(r"\.$", "", keyword)

    # Normalize whitespace
    keyword = re.sub(r"\s+", " ", keyword)

    return keyword.strip()


def is_valid_keyword(keyword: str) -> bool:
    """
    Reject meaningless ATS keywords.
    """

    if not keyword:
        return False

    keyword = keyword.strip().lower()

    # Too short
    if len(keyword) < 2:
        return False

    # Common useless abbreviations
    invalid_exact = {
        "b.s",
        "bs",
        "m.s",
        "ms",
        "b.e",
        "be",
        "b.tech",
        "m.tech",
        "ph.d",
        "phd",
        "etc",
        "e.g",
        "i.e",
    }

    if keyword in invalid_exact:
        return False

    # Pure number
    if re.fullmatch(r"\d+", keyword):
        return False

    # Only punctuation
    if not re.search(r"[a-z0-9]", keyword):
        return False

    # Single generic word
    if keyword in STOP_WORDS:
        return False

    return True


# ============================================================
# PHRASE DETECTION
# ============================================================

def extract_phrases(text: str):
    """
    Extract meaningful multi-word phrases from job descriptions.

    Example:
        'experience in statistical modeling and financial forecasting'

    becomes:
        [
            'statistical modeling',
            'financial forecasting'
        ]
    """

    normalized = normalize_text(text)

    if not normalized:
        return []

    found = []

    # Longest phrases first.
    # This prevents a shorter phrase from taking precedence.
    phrases = sorted(
        IMPORTANT_PHRASES,
        key=lambda phrase: len(phrase.split()),
        reverse=True
    )

    for phrase in phrases:
        phrase_normalized = normalize_text(phrase)

        if not phrase_normalized:
            continue

        pattern = r"(?<![a-z0-9])" + re.escape(phrase_normalized) + r"(?![a-z0-9])"

        if re.search(pattern, normalized):
            found.append(phrase_normalized)

    return found


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_job_skills(job_description: str):
    """
    Extract known technical skills from the job description.

    Uses the centralized skill dictionary from resume_parser.py.
    """

    if not job_description:
        return []

    skills = detect_skills(job_description)

    return sorted(
        set(skill.strip() for skill in skills if skill and skill.strip()),
        key=str.lower
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(resume_skills, job_skills):
    """
    Compare resume skills against required job skills.
    """

    resume_lookup = {
        skill.strip().lower(): skill
        for skill in resume_skills
        if skill and skill.strip()
    }

    job_lookup = {
        skill.strip().lower(): skill
        for skill in job_skills
        if skill and skill.strip()
    }

    matched = []
    missing = []

    for normalized_skill, original_skill in job_lookup.items():

        if normalized_skill in resume_lookup:
            matched.append(original_skill)
        else:
            missing.append(original_skill)

    matched.sort(key=str.lower)
    missing.sort(key=str.lower)

    if not job_lookup:
        score = 0
    else:
        score = round(
            (len(matched) / len(job_lookup)) * 100,
            2
        )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }


# ============================================================
# GENERIC KEYWORD EXTRACTION
# ============================================================

def extract_keywords(job_description: str, limit: int = 15):
    """
    Extract meaningful ATS keywords from a job description.

    Strategy:
        1. Detect important multi-word phrases.
        2. Detect useful individual words.
        3. Remove words already represented by phrases.
        4. Remove stop words and useless abbreviations.
        5. Rank by frequency.
        6. Return clean unique keywords.

    This prevents output such as:

        statistical modeling
        statisticalmodeling
        statistical
        modeling

    and instead keeps:

        statistical modeling
    """

    if not job_description:
        return []

    normalized = normalize_text(job_description)

    if not normalized:
        return []

    # --------------------------------------------------------
    # STEP 1: Extract important phrases
    # --------------------------------------------------------

    phrases = extract_phrases(normalized)

    phrase_set = set(phrases)

    # Words that are already part of a meaningful phrase.
    phrase_words = set()

    for phrase in phrases:
        for word in phrase.split():
            if len(word) > 1:
                phrase_words.add(word)

    # --------------------------------------------------------
    # STEP 2: Extract individual words
    # --------------------------------------------------------

    tokens = normalized.split()

    word_counter = Counter()

    for token in tokens:

        token = clean_keyword(token)

        if not is_valid_keyword(token):
            continue

        # Ignore words that are already represented by a phrase.
        if token in phrase_words:
            continue

        # Ignore very short ordinary words.
        if len(token) < 3 and token not in {
            "c",
            "c++",
            "c#",
            "ai",
            "ml",
            "nlp",
            "sql",
            "aws",
            "gcp",
            "api",
            "ui",
            "ux",
        }:
            continue

        word_counter[token] += 1

    # --------------------------------------------------------
    # STEP 3: Select useful individual keywords
    # --------------------------------------------------------

    individual_keywords = [
        word
        for word, _count in word_counter.most_common()
    ]

    # --------------------------------------------------------
    # STEP 4: Combine phrases + words
    # --------------------------------------------------------

    keywords = []

    # Phrases have higher priority.
    for phrase in phrases:
        if is_valid_keyword(phrase):
            keywords.append(phrase)

    # Then individual meaningful words.
    for keyword in individual_keywords:

        if keyword in keywords:
            continue

        # Prevent a single word from being added if it is
        # already contained inside a selected phrase.
        contained_in_phrase = False

        for phrase in keywords:
            if " " in phrase and keyword in phrase.split():
                contained_in_phrase = True
                break

        if contained_in_phrase:
            continue

        keywords.append(keyword)

        if len(keywords) >= limit:
            break

    return keywords[:limit]


# ============================================================
# KEYWORD MATCHING
# ============================================================

def keyword_exists(text: str, keyword: str) -> bool:
    """
    Check whether a keyword or phrase actually exists in text.
    """

    normalized_text = normalize_text(text)
    normalized_keyword = normalize_text(keyword)

    if not normalized_text or not normalized_keyword:
        return False

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(normalized_keyword)
        + r"(?![a-z0-9])"
    )

    return bool(re.search(pattern, normalized_text))


def calculate_keyword_match(resume_text: str, keywords):
    """
    Compare extracted job-description keywords against
    the complete resume text.
    """

    if not keywords:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
        }

    matched = []
    missing = []

    for keyword in keywords:

        if keyword_exists(resume_text, keyword):
            matched.append(keyword)
        else:
            missing.append(keyword)

    score = round(
        (len(matched) / len(keywords)) * 100,
        2
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }


# ============================================================
# SECTION RELEVANCE
# ============================================================

def calculate_section_relevance(resume_text: str, job_description: str):
    """
    Determine whether important resume sections are present
    based on the job description.

    Sections considered:
        - Skills
        - Experience
        - Projects
        - Education
        - Certifications
    """

    resume_sections = detect_sections(resume_text)

    normalized_job = normalize_text(job_description)

    matched = []
    missing = []

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if "skills" in [section.lower() for section in resume_sections]:
        matched.append("Skills")
    else:
        missing.append("Skills")

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    experience_relevant_terms = {
        "experience",
        "experienced",
        "senior",
        "analyst",
        "developer",
        "engineer",
        "manager",
        "professional",
    }

    experience_relevant = any(
        term in normalized_job.split()
        for term in experience_relevant_terms
    )

    if experience_relevant:

        if "experience" in [
            section.lower()
            for section in resume_sections
        ]:
            matched.append("Experience")
        else:
            missing.append("Experience")

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    project_relevant_terms = {
        "project",
        "projects",
        "development",
        "develop",
        "build",
        "built",
        "software",
        "application",
        "api",
    }

    project_relevant = any(
        term in normalized_job.split()
        for term in project_relevant_terms
    )

    if project_relevant:

        if "projects" in [
            section.lower()
            for section in resume_sections
        ]:
            matched.append("Projects")
        else:
            missing.append("Projects")

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education_relevant_terms = {
        "degree",
        "bachelor",
        "master",
        "b.s",
        "b.e",
        "b.tech",
        "m.s",
        "m.e",
        "m.tech",
        "computer",
        "science",
        "education",
    }

    education_relevant = any(
        term in normalized_job
        for term in education_relevant_terms
    )

    if education_relevant:

        if "education" in [
            section.lower()
            for section in resume_sections
        ]:
            matched.append("Education")
        else:
            missing.append("Education")

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    certification_relevant_terms = {
        "certification",
        "certified",
        "certificate",
        "certifications",
    }

    certification_relevant = any(
        term in normalized_job.split()
        for term in certification_relevant_terms
    )

    if certification_relevant:

        if "certifications" in [
            section.lower()
            for section in resume_sections
        ]:
            matched.append("Certifications")
        else:
            missing.append("Certifications")

    # --------------------------------------------------------
    # Score
    # --------------------------------------------------------

    total = len(matched) + len(missing)

    if total == 0:
        score = 100
    else:
        score = round(
            (len(matched) / total) * 100,
            2
        )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }


# ============================================================
# ATS SCORE CALCULATION
# ============================================================

def calculate_ats_score(
    skill_score: float,
    keyword_score: float,
    section_score: float
):
    """
    Calculate the final ATS score.

    Weighting:
        Skills   = 60%
        Keywords = 30%
        Sections = 10%
    """

    weighted_skills = skill_score * 0.60
    weighted_keywords = keyword_score * 0.30
    weighted_sections = section_score * 0.10

    total = (
        weighted_skills
        + weighted_keywords
        + weighted_sections
    )

    return {
        "total": round(total),
        "skills": round(weighted_skills, 2),
        "keywords": round(weighted_keywords, 2),
        "sections": round(weighted_sections, 2),
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    skill_result,
    keyword_result,
    section_result
):
    """
    Generate simple actionable ATS recommendations.
    """

    recommendations = []

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if skill_result["missing"]:

        missing_preview = skill_result["missing"][:5]

        recommendations.append(
            "Consider adding relevant skills such as: "
            + ", ".join(missing_preview)
            + "."
        )

    # --------------------------------------------------------
    # Keywords
    # --------------------------------------------------------

    if keyword_result["missing"]:

        missing_preview = keyword_result["missing"][:5]

        recommendations.append(
            "Consider naturally including job-relevant keywords "
            "such as: "
            + ", ".join(missing_preview)
            + "."
        )

    # --------------------------------------------------------
    # Sections
    # --------------------------------------------------------

    if section_result["missing"]:

        recommendations.append(
            "Consider adding or strengthening these resume sections: "
            + ", ".join(section_result["missing"])
            + "."
        )

    # --------------------------------------------------------
    # Positive result
    # --------------------------------------------------------

    if not recommendations:
        recommendations.append(
            "Your resume is well aligned with the provided job description."
        )

    return recommendations


# ============================================================
# MAIN ATS ANALYSIS
# ============================================================

def analyze_ats_match(
    resume_text: str,
    resume_skills,
    job_description: str
):
    """
    Complete ATS analysis.

    Returns:

    {
        "score": 78,
        "breakdown": {
            "skills": {...},
            "keywords": {...},
            "sections": {...}
        },
        "skills": {
            "required": [...],
            "matched": [...],
            "missing": [...]
        },
        "keywords": {
            "matched": [...],
            "missing": [...]
        },
        "sections": {
            "matched": [...],
            "missing": [...]
        },
        "recommendations": [...]
    }
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not resume_text:
        raise ValueError("Resume text cannot be empty.")

    if not job_description:
        raise ValueError("Job description cannot be empty.")

    if resume_skills is None:
        resume_skills = []

    # --------------------------------------------------------
    # 1. Extract required skills
    # --------------------------------------------------------

    job_skills = extract_job_skills(job_description)

    # --------------------------------------------------------
    # 2. Skill matching
    # --------------------------------------------------------

    skill_result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    # --------------------------------------------------------
    # 3. Extract keywords
    # --------------------------------------------------------

    keywords = extract_keywords(
        job_description,
        limit=15
    )

    # --------------------------------------------------------
    # 4. Keyword matching
    # --------------------------------------------------------

    keyword_result = calculate_keyword_match(
        resume_text,
        keywords
    )

    # --------------------------------------------------------
    # 5. Section relevance
    # --------------------------------------------------------

    section_result = calculate_section_relevance(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # 6. Final ATS score
    # --------------------------------------------------------

    score = calculate_ats_score(
        skill_result["score"],
        keyword_result["score"],
        section_result["score"]
    )

    # --------------------------------------------------------
    # 7. Recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        skill_result,
        keyword_result,
        section_result
    )

    # --------------------------------------------------------
    # 8. Final response
    # --------------------------------------------------------

    return {
        "score": score["total"],

        "breakdown": {
            "skills": {
                "raw_score": skill_result["score"],
                "weighted_score": score["skills"],
            },

            "keywords": {
                "raw_score": keyword_result["score"],
                "weighted_score": score["keywords"],
            },

            "sections": {
                "raw_score": section_result["score"],
                "weighted_score": score["sections"],
            },
        },

        "skills": {
            "required": job_skills,
            "matched": skill_result["matched"],
            "missing": skill_result["missing"],
        },

        "keywords": {
            "matched": keyword_result["matched"],
            "missing": keyword_result["missing"],
        },

        "sections": {
            "matched": section_result["matched"],
            "missing": section_result["missing"],
        },

        "recommendations": recommendations,
    }