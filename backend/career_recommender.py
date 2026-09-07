# =====================================================
# ResumeIQ — Career Recommendation Engine
# =====================================================

from typing import List, Dict, Any


# =====================================================
# CAREER PROFILES
# =====================================================

CAREER_PROFILES = {

    "Software Engineer": {
        "skills": [
            "Python",
            "Java",
            "C++",
            "JavaScript",
            "Git",
            "GitHub",
            "SQL",
            "Data Structures",
            "Algorithms"
        ],
        "keywords": [
            "software development",
            "programming",
            "backend",
            "frontend",
            "development",
            "applications"
        ],
        "description":
            "Builds software applications, services, and systems.",
    },

    "Backend Developer": {
        "skills": [
            "Python",
            "Java",
            "Node.js",
            "SQL",
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "FastAPI",
            "Django",
            "Flask",
            "Git",
            "Docker"
        ],
        "keywords": [
            "backend",
            "api",
            "rest api",
            "server",
            "database",
            "microservices"
        ],
        "description":
            "Designs APIs, backend services, databases, and server-side systems.",
    },

    "Frontend Developer": {
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git",
            "GitHub"
        ],
        "keywords": [
            "frontend",
            "ui",
            "ux",
            "web development",
            "responsive",
            "user interface"
        ],
        "description":
            "Builds interactive and responsive web interfaces.",
    },

    "Full Stack Developer": {
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express",
            "Python",
            "FastAPI",
            "SQL",
            "MongoDB",
            "Git",
            "GitHub"
        ],
        "keywords": [
            "full stack",
            "web development",
            "frontend",
            "backend",
            "api",
            "database"
        ],
        "description":
            "Works across frontend, backend, APIs, databases, and deployment.",
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Pandas",
            "NumPy",
            "SQL",
            "Git"
        ],
        "keywords": [
            "machine learning",
            "deep learning",
            "model",
            "prediction",
            "classification",
            "training",
            "data"
        ],
        "description":
            "Develops, trains, evaluates, and deploys machine learning systems.",
    },

    "Data Scientist": {
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "Statistics",
            "Data Visualization"
        ],
        "keywords": [
            "data science",
            "statistics",
            "analytics",
            "data analysis",
            "prediction",
            "visualization"
        ],
        "description":
            "Uses data, statistics, and machine learning to generate insights.",
    },

    "DevOps Engineer": {
        "skills": [
            "Linux",
            "Git",
            "GitHub",
            "Docker",
            "Kubernetes",
            "AWS",
            "Azure",
            "CI/CD"
        ],
        "keywords": [
            "devops",
            "deployment",
            "cloud",
            "ci/cd",
            "infrastructure",
            "automation"
        ],
        "description":
            "Automates development, deployment, infrastructure, and cloud operations.",
    }
}


# =====================================================
# NORMALIZATION
# =====================================================

def normalize_skill(skill: str) -> str:
    """
    Normalize skill names for comparison.
    """

    aliases = {
        "reactjs": "react",
        "react.js": "react",

        "nodejs": "node.js",
        "node": "node.js",

        "postgres": "postgresql",

        "sklearn": "scikit-learn",

        "ml": "machine learning",

        "dl": "deep learning",

        "tf": "tensorflow",
    }

    value = str(skill).strip().lower()

    return aliases.get(value, value)


# =====================================================
# CAREER MATCHING
# =====================================================

def calculate_career_match(
    resume_skills: List[str],
    resume_text: str,
    career_profile: Dict[str, Any]
) -> Dict[str, Any]:

    normalized_resume_skills = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    career_skills = career_profile["skills"]

    normalized_career_skills = {
        normalize_skill(skill)
        for skill in career_skills
    }

    matched_skills = sorted(
        normalized_resume_skills.intersection(
            normalized_career_skills
        )
    )

    missing_skills = sorted(
        normalized_career_skills -
        normalized_resume_skills
    )

    total_skills = len(normalized_career_skills)

    if total_skills:
        skill_score = (
            len(matched_skills) /
            total_skills
        ) * 100
    else:
        skill_score = 0

    text = resume_text.lower()

    matched_keywords = []

    for keyword in career_profile["keywords"]:

        if keyword.lower() in text:

            matched_keywords.append(keyword)

    keyword_score = (
        len(matched_keywords) /
        len(career_profile["keywords"]) * 100
        if career_profile["keywords"]
        else 0
    )

    final_score = (
        skill_score * 0.75 +
        keyword_score * 0.25
    )

    return {
        "score": round(final_score, 2),

        "skill_score": round(
            skill_score,
            2
        ),

        "keyword_score": round(
            keyword_score,
            2
        ),

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "matched_keywords": matched_keywords,
    }


# =====================================================
# CAREER RECOMMENDATION
# =====================================================

def analyze_career_recommendations(
    resume_text: str,
    resume_skills: List[str]
) -> Dict[str, Any]:

    recommendations = []

    for career_name, profile in CAREER_PROFILES.items():

        result = calculate_career_match(
            resume_skills,
            resume_text,
            profile
        )

        recommendations.append({

            "career": career_name,

            "description":
                profile["description"],

            "score":
                result["score"],

            "skill_score":
                result["skill_score"],

            "keyword_score":
                result["keyword_score"],

            "matched_skills":
                result["matched_skills"],

            "missing_skills":
                result["missing_skills"],

            "matched_keywords":
                result["matched_keywords"],
        })


    # Highest score first
    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    top_recommendations = recommendations[:3]


    return {
        "recommendations":
            top_recommendations,

        "total_careers_evaluated":
            len(CAREER_PROFILES)
    }