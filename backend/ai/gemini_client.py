import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_with_gemini(prompt: str) -> str:
    """
    Send a prompt to Google Gemini.

    The client is created only when this function is called,
    so the FastAPI server can start even if the API key is missing.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text