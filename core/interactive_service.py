# App/backend/core/interactive_service.py

from typing import Optional
from textblob import TextBlob

# We'll assume one of these exists (depending on what Member 2 actually named it)
# Try these common names — change the import once you know the real file/function
try:
    from .gemini_service import generate_content as call_gemini
except ImportError:
    try:
        from .gemini_client import generate_response as call_gemini
    except ImportError:
        # Fallback placeholder — replace with actual import once visible
        def call_gemini(prompt: str) -> str:
            raise NotImplementedError("Gemini client not found. Wait for Member 2 to commit gemini_service.py or similar.")

from prompts.interactive import (
    CHAT_SYSTEM_PROMPT,
    FRUSTRATED_INSTRUCTION,
    ELI5_SYSTEM_PROMPT
)


def is_negative_sentiment(text: str) -> bool:
    """Simple polarity check with TextBlob"""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity < -0.1  # threshold for "frustrated"


def build_chat_prompt(pdf_text: str, user_question: str) -> str:
    """Combines system prompt + context + question"""
    system_part = CHAT_SYSTEM_PROMPT

    if is_negative_sentiment(user_question):
        system_part += "\n" + FRUSTRATED_INSTRUCTION

    return f"""{system_part}

=== DOCUMENT CONTENT (use only this) ===
{pdf_text.strip()}

=== STUDENT QUESTION ===
{user_question.strip()}

Your answer:"""


def get_chat_response(pdf_text: str, user_question: str) -> str:
    """
    Main function for normal / frustrated chat (Tasks A + B)
    Returns Gemini's response
    """
    prompt = build_chat_prompt(pdf_text, user_question)
    try:
        return call_gemini(prompt).strip()
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"


def eli5_answer(previous_answer: str) -> str:
    """
    Task C: Rewrite any previous answer in ELI5 style
    """
    prompt = f"""{ELI5_SYSTEM_PROMPT}

Original answer to rewrite:
{previous_answer.strip()}

Simplified version for 5-year-old:"""

    try:
        return call_gemini(prompt).strip()
    except Exception as e:
        return f"Error in ELI5 mode: {str(e)}"


# ────────────────────────────────────────────────
#  Independent testing (run this file directly)
# ────────────────────────────────────────────────
if __name__ == "__main__":
    # Fake PDF content for testing
    sample_text = """
    Photosynthesis is the process by which green plants use sunlight to convert carbon dioxide 
    and water into glucose and oxygen. The formula is 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂.
    """

    print("=== TEST 1: Normal question ===")
    q1 = "What is photosynthesis?"
    print("Question:", q1)
    print("Answer:", get_chat_response(sample_text, q1))
    print()

    print("=== TEST 2: Frustrated / negative question ===")
    q2 = "This is so annoying, why can't I understand photosynthesis??"
    print("Question:", q2)
    print("Answer (should be kinder):", get_chat_response(sample_text, q2))
    print()

    print("=== TEST 3: ELI5 on a complex answer ===")
    complex_ans = "Photosynthesis involves chloroplasts capturing light energy to split water molecules, releasing oxygen and generating ATP and NADPH for the Calvin cycle to fix CO₂ into glucose."
    print("Original:", complex_ans)
    print("ELI5 version:", eli5_answer(complex_ans))