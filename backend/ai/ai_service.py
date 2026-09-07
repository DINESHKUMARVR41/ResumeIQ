from backend.ai.gemini_client import (
    generate_with_gemini
)

from backend.ai.groq_client import (
    generate_with_groq
)


def ask_gemini(prompt: str) -> str:

    return generate_with_gemini(prompt)


def ask_groq(prompt: str) -> str:

    return generate_with_groq(prompt)


def ask_ai(
    prompt: str,
    provider: str = "gemini"
) -> str:

    if provider == "gemini":

        return ask_gemini(prompt)


    if provider == "groq":

        return ask_groq(prompt)


    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )