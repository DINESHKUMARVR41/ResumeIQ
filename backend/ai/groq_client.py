import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_with_groq(prompt: str) -> str:
    """
    Generate a response using Groq.

    The API key and model are loaded from .env.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add it to your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    client = Groq(
        api_key=api_key
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are ResumeIQ, an AI career assistant. "
                    "You help users understand their resume, "
                    "skills, career direction, ATS performance, "
                    "skill gaps, projects and career roadmap. "
                    "Use only the information provided in the "
                    "resume context. Never invent experience, "
                    "skills, achievements or qualifications."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    if not response.choices:
        raise RuntimeError(
            "Groq returned no response choices."
        )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return content