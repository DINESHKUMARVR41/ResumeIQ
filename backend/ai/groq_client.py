import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_with_groq(prompt: str) -> str:
    """
    Send a prompt to Groq.

    The client is created only when the function is called.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add it to your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
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
                    "You are ResumeIQ, an expert AI "
                    "career advisor."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return content