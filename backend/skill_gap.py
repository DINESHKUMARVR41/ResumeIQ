"""
ResumeIQ - Skill Gap Analysis

Compares skills detected in a resume against skills required
by a target job description.

Provides:
- Skill coverage percentage
- Matched skills
- Missing skills
- Skill categories
- Priority levels
- Gap reasons
- Suggested learning topics
"""


# ============================================================
# SKILL CATEGORIES
# ============================================================

SKILL_CATEGORIES = {

    # Programming
    "Python": "Programming",
    "Java": "Programming",
    "C": "Programming",
    "C++": "Programming",
    "C#": "Programming",
    "JavaScript": "Programming",
    "TypeScript": "Programming",
    "R": "Programming",

    # Web Development
    "HTML": "Web Development",
    "CSS": "Web Development",
    "React": "Web Development",
    "Node.js": "Web Development",
    "Express": "Web Development",
    "REST API": "Web Development",
    "FastAPI": "Web Development",
    "Django": "Web Development",
    "Flask": "Web Development",

    # Databases
    "SQL": "Database",
    "MySQL": "Database",
    "PostgreSQL": "Database",
    "MongoDB": "Database",
    "Firebase": "Database",

    # Development Tools
    "Git": "Development Tools",
    "GitHub": "Development Tools",

    # DevOps
    "Docker": "DevOps",
    "Kubernetes": "DevOps",

    # Cloud
    "AWS": "Cloud",
    "Azure": "Cloud",
    "Google Cloud": "Cloud",
    "GCP": "Cloud",

    # Data Science
    "Pandas": "Data Science",
    "NumPy": "Data Science",
    "Scikit-learn": "Machine Learning",

    # Artificial Intelligence
    "Machine Learning": "Artificial Intelligence",
    "Deep Learning": "Artificial Intelligence",
    "NLP": "Artificial Intelligence",
    "Computer Vision": "Artificial Intelligence",

    # Deep Learning Frameworks
    "TensorFlow": "Deep Learning",
    "PyTorch": "Deep Learning",

    # Application Development
    "Streamlit": "Application Development",
}


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "python": "Python",

    "java": "Java",

    "c": "C",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "typescript": "TypeScript",
    "ts": "TypeScript",

    "r": "R",

    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "react": "React",
    "reactjs": "React",
    "react.js": "React",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "express": "Express",
    "expressjs": "Express",

    "rest api": "REST API",
    "rest apis": "REST API",
    "rest": "REST API",

    "fastapi": "FastAPI",

    "django": "Django",

    "flask": "Flask",

    "sql": "SQL",

    "mysql": "MySQL",

    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",

    "mongodb": "MongoDB",
    "mongo": "MongoDB",

    "firebase": "Firebase",
    "firestore": "Firebase",

    "git": "Git",

    "github": "GitHub",

    "docker": "Docker",

    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",

    "aws": "AWS",
    "amazon web services": "AWS",

    "azure": "Azure",
    "microsoft azure": "Azure",

    "google cloud": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "gcp": "GCP",

    "pandas": "Pandas",

    "numpy": "NumPy",

    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "machine learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",
    "dl": "Deep Learning",

    "nlp": "NLP",
    "natural language processing": "NLP",

    "computer vision": "Computer Vision",
    "cv": "Computer Vision",

    "tensorflow": "TensorFlow",

    "pytorch": "PyTorch",

    "streamlit": "Streamlit",
}


# ============================================================
# LEARNING TOPICS
# ============================================================

LEARNING_TOPICS = {

    "Python": [
        "Python syntax and data types",
        "Functions and modules",
        "Object-oriented programming",
        "File handling",
        "Exception handling",
    ],

    "Java": [
        "Java syntax",
        "Object-oriented programming",
        "Collections",
        "Exception handling",
        "Java application development",
    ],

    "C": [
        "C syntax",
        "Pointers",
        "Arrays and strings",
        "Structures",
        "Memory management",
    ],

    "C++": [
        "C++ syntax",
        "Object-oriented programming",
        "STL",
        "Pointers and memory",
        "Competitive programming",
    ],

    "C#": [
        "C# syntax",
        "Object-oriented programming",
        ".NET fundamentals",
        "Collections",
        "Application development",
    ],

    "JavaScript": [
        "JavaScript fundamentals",
        "DOM manipulation",
        "Asynchronous JavaScript",
        "Promises and async/await",
        "Modern JavaScript",
    ],

    "TypeScript": [
        "TypeScript types",
        "Interfaces",
        "Generics",
        "Classes",
        "Type-safe application development",
    ],

    "R": [
        "R syntax",
        "Data frames",
        "Statistical analysis",
        "Data visualization",
        "Statistical computing",
    ],

    "HTML": [
        "HTML structure",
        "Semantic HTML",
        "Forms",
        "Accessibility",
        "HTML5",
    ],

    "CSS": [
        "CSS selectors",
        "Flexbox",
        "CSS Grid",
        "Responsive design",
        "Animations",
    ],

    "React": [
        "React components",
        "Props and state",
        "Hooks",
        "Routing",
        "API integration",
    ],

    "Node.js": [
        "Node.js fundamentals",
        "Modules",
        "File system",
        "HTTP servers",
        "REST APIs",
    ],

    "Express": [
        "Express fundamentals",
        "Routing",
        "Middleware",
        "REST APIs",
        "Error handling",
    ],

    "REST API": [
        "HTTP methods",
        "Request and response",
        "Status codes",
        "REST principles",
        "API authentication",
    ],

    "FastAPI": [
        "FastAPI fundamentals",
        "Path and query parameters",
        "Request validation",
        "Pydantic models",
        "API development",
    ],

    "Django": [
        "Django fundamentals",
        "Models",
        "Views",
        "Templates",
        "Django REST Framework",
    ],

    "Flask": [
        "Flask fundamentals",
        "Routes",
        "Request handling",
        "Templates",
        "REST API development",
    ],

    "SQL": [
        "SELECT queries",
        "Filtering and sorting",
        "JOIN operations",
        "GROUP BY and aggregation",
        "Subqueries",
    ],

    "MySQL": [
        "Database design",
        "SQL queries",
        "Indexes",
        "Transactions",
        "Database optimization",
    ],

    "PostgreSQL": [
        "PostgreSQL fundamentals",
        "Advanced SQL",
        "Indexes",
        "Transactions",
        "PostgreSQL optimization",
    ],

    "MongoDB": [
        "MongoDB documents",
        "Collections",
        "CRUD operations",
        "Queries",
        "Indexes",
    ],

    "Firebase": [
        "Firebase fundamentals",
        "Firestore",
        "Authentication",
        "Cloud Storage",
        "Firebase security rules",
    ],

    "Git": [
        "Git fundamentals",
        "Branches",
        "Merging",
        "Rebasing",
        "Conflict resolution",
    ],

    "GitHub": [
        "Repositories",
        "Pull requests",
        "Issues",
        "GitHub Actions",
        "Open-source workflow",
    ],

    "Docker": [
        "Docker images",
        "Containers",
        "Dockerfiles",
        "Docker Compose",
        "Container networking",
    ],

    "Kubernetes": [
        "Pods",
        "Deployments",
        "Services",
        "ConfigMaps and Secrets",
        "Kubernetes networking",
    ],

    "AWS": [
        "AWS fundamentals",
        "EC2",
        "S3",
        "IAM",
        "Cloud deployment",
    ],

    "Azure": [
        "Azure fundamentals",
        "Virtual machines",
        "Storage",
        "Azure identity",
        "Cloud deployment",
    ],

    "Google Cloud": [
        "Google Cloud fundamentals",
        "Compute",
        "Cloud Storage",
        "IAM",
        "Cloud deployment",
    ],

    "GCP": [
        "Google Cloud fundamentals",
        "Compute",
        "Cloud Storage",
        "IAM",
        "Cloud deployment",
    ],

    "Pandas": [
        "DataFrames",
        "Data cleaning",
        "Data filtering",
        "Grouping and aggregation",
        "Data analysis",
    ],

    "NumPy": [
        "NumPy arrays",
        "Array operations",
        "Indexing",
        "Broadcasting",
        "Numerical computing",
    ],

    "Scikit-learn": [
        "Data preprocessing",
        "Model training",
        "Classification",
        "Regression",
        "Model evaluation",
    ],

    "Machine Learning": [
        "Supervised learning",
        "Unsupervised learning",
        "Feature engineering",
        "Model evaluation",
        "Model optimization",
    ],

    "Deep Learning": [
        "Neural networks",
        "Backpropagation",
        "CNNs",
        "RNNs",
        "Model training",
    ],

    "NLP": [
        "Text preprocessing",
        "Tokenization",
        "Embeddings",
        "Text classification",
        "Transformer models",
    ],

    "Computer Vision": [
        "Image preprocessing",
        "CNNs",
        "Object detection",
        "Image classification",
        "Computer vision pipelines",
    ],

    "TensorFlow": [
        "TensorFlow tensors",
        "Neural networks",
        "Model training",
        "Model evaluation",
        "TensorFlow deployment",
    ],

    "PyTorch": [
        "PyTorch tensors",
        "Neural networks",
        "Datasets and DataLoaders",
        "Model training",
        "PyTorch deployment",
    ],

    "Streamlit": [
        "Streamlit components",
        "Widgets",
        "Session state",
        "Data visualization",
        "Application deployment",
    ],
}


# ============================================================
# PRIORITY RULES
# ============================================================

HIGH_PRIORITY_SKILLS = {
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "FastAPI",
    "Django",
    "React",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Google Cloud",
    "GCP",
}


MEDIUM_PRIORITY_CATEGORIES = {
    "Programming",
    "Web Development",
    "Database",
    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Cloud",
    "DevOps",
}


def calculate_priority(
    skill,
    total_required_skills,
    missing_count,
):
    """
    Determine priority for a missing skill.

    High:
        Core technical skill or very small requirement set.

    Medium:
        Important supporting technical skill.

    Low:
        Less critical supporting skill.
    """

    if skill in HIGH_PRIORITY_SKILLS:
        return "High"

    category = SKILL_CATEGORIES.get(
        skill,
        "Other",
    )

    if total_required_skills <= 3:
        return "High"

    if category in MEDIUM_PRIORITY_CATEGORIES:
        return "Medium"

    if missing_count <= 2:
        return "Medium"

    return "Low"


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def normalize_skill(skill):
    """
    Convert different representations of the same skill
    into a canonical skill name.

    Example:

        'python'     -> 'Python'
        'PYTHON'     -> 'Python'
        'reactjs'    -> 'React'
        'postgres'   -> 'PostgreSQL'
        'sklearn'    -> 'Scikit-learn'
    """

    if not skill:
        return None

    cleaned = str(skill).strip().lower()

    cleaned = cleaned.replace("–", "-")
    cleaned = cleaned.replace("—", "-")

    cleaned = " ".join(cleaned.split())

    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]

    # Case-insensitive lookup against canonical names
    for canonical_skill in SKILL_CATEGORIES:

        if cleaned == canonical_skill.lower():
            return canonical_skill

    return str(skill).strip()


def normalize_skill_list(skills):
    """
    Normalize and deduplicate a list of skills.
    """

    if not skills:
        return []

    normalized = []
    seen = set()

    for skill in skills:

        canonical = normalize_skill(skill)

        if not canonical:
            continue

        key = canonical.lower()

        if key in seen:
            continue

        seen.add(key)
        normalized.append(canonical)

    return normalized


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    resume_skills,
    required_skills,
):
    """
    Compare resume skills against required job skills.

    Parameters
    ----------
    resume_skills : list
        Skills detected from the resume.

    required_skills : list
        Skills detected from the job description.

    Returns
    -------
    dict
        Complete skill gap analysis.
    """

    # --------------------------------------------------------
    # Validate inputs
    # --------------------------------------------------------

    if resume_skills is None:
        resume_skills = []

    if required_skills is None:
        required_skills = []

    # --------------------------------------------------------
    # Normalize skills
    # --------------------------------------------------------

    resume_skills = normalize_skill_list(
        resume_skills
    )

    required_skills = normalize_skill_list(
        required_skills
    )

    # --------------------------------------------------------
    # Create lookup sets
    # --------------------------------------------------------

    resume_lookup = {
        skill.lower()
        for skill in resume_skills
    }

    # --------------------------------------------------------
    # Find matched and missing skills
    # --------------------------------------------------------

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        normalized = skill.lower()

        if normalized in resume_lookup:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    # --------------------------------------------------------
    # Coverage calculation
    # --------------------------------------------------------

    total_required = len(required_skills)

    matched_count = len(matched_skills)

    missing_count = len(missing_skills)

    if total_required == 0:

        coverage = 100

    else:

        coverage = round(
            (matched_count / total_required) * 100
        )

    # --------------------------------------------------------
    # Build detailed gaps
    # --------------------------------------------------------

    gaps = []

    for skill in missing_skills:

        category = SKILL_CATEGORIES.get(
            skill,
            "Other",
        )

        priority = calculate_priority(
            skill=skill,
            total_required_skills=total_required,
            missing_count=missing_count,
        )

        learning_focus = LEARNING_TOPICS.get(
            skill,
            [
                f"{skill} fundamentals",
                f"{skill} practical usage",
                f"{skill} project development",
                f"{skill} best practices",
            ],
        )

        gaps.append(
            {
                "skill": skill,

                "category": category,

                "priority": priority,

                "reason": (
                    f"{skill} is required by the target "
                    f"job but was not detected in the resume."
                ),

                "learning_focus": learning_focus,
            }
        )

    # --------------------------------------------------------
    # Sort gaps by priority
    # --------------------------------------------------------

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    gaps.sort(
        key=lambda gap: (
            priority_order.get(
                gap["priority"],
                3,
            ),
            gap["skill"].lower(),
        )
    )

    # --------------------------------------------------------
    # Priority counts
    # --------------------------------------------------------

    high_priority = sum(
        1
        for gap in gaps
        if gap["priority"] == "High"
    )

    medium_priority = sum(
        1
        for gap in gaps
        if gap["priority"] == "Medium"
    )

    low_priority = sum(
        1
        for gap in gaps
        if gap["priority"] == "Low"
    )

    # --------------------------------------------------------
    # Coverage message
    # --------------------------------------------------------

    if total_required == 0:

        coverage_message = (
            "No specific technical skills were detected "
            "in the job description."
        )

    elif coverage >= 80:

        coverage_message = (
            "Strong skill alignment. Your resume covers "
            "most of the required skills."
        )

    elif coverage >= 60:

        coverage_message = (
            "Good skill alignment, but some important "
            "skills are still missing."
        )

    elif coverage >= 40:

        coverage_message = (
            "Moderate skill alignment. Focus on the "
            "highest-priority missing skills."
        )

    else:

        coverage_message = (
            "Low skill alignment. Several required skills "
            "are missing from your resume."
        )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "coverage": coverage,

        "summary": {
            "required_skills": total_required,
            "matched_skills": matched_count,
            "missing_skills": missing_count,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
        },

        "coverage_message": coverage_message,

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "gaps": gaps,
    }