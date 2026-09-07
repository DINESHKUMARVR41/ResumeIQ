import json

from backend.ai.gemini_client import generate_with_gemini


def generate_career_analysis(
    resume_text: str,
    resume_skills: list,
    career_candidates: list
) -> str:

    prompt = f"""
You are ResumeIQ's senior career intelligence engine.

Analyze the candidate's resume and career compatibility.

IMPORTANT RULES:

1. Use only information present in the resume.
2. Do not invent experience.
3. Do not claim the candidate has a skill unless evidence exists.
4. Clearly distinguish existing skills from recommended skills.
5. Give practical and realistic recommendations.
6. Prioritize entry-level opportunities when experience is limited.

RESUME:

{resume_text}


DETECTED RESUME SKILLS:

{json.dumps(resume_skills, indent=2)}


CAREER ENGINE CANDIDATES:

{json.dumps(career_candidates, indent=2)}


Return your response using this structure:

Career Recommendation
Why This Career
Current Strengths
Missing Skills
Recommended Skills
Recommended Projects
30 Day Plan
60 Day Plan
90 Day Plan
Final Advice
"""

    return generate_with_gemini(prompt)