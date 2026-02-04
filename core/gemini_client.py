import os
import json
from dotenv import load_dotenv
from google import genai

from prompts.tutor_persona import QUIZ_PROMPT
from models.quiz_format import Quiz

# Load environment variables
load_dotenv()

# ---------------- BASIC GEMINI CALL ----------------
def call_gemini(prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ---------------- TEXT SUMMARIZATION ----------------
def summarize_text(text: str) -> str:
    prompt = (
        "You are a helpful teacher. "
        "Summarize the following text in simple, clear language:\n\n"
        f"{text}"
    )

    return call_gemini(prompt)


# ---------------- TEACHING SCRIPT ----------------
from prompts.script_templates import TEACHING_SCRIPT_TEMPLATE

def gemini_teaching_script(text: str) -> str:
    prompt = TEACHING_SCRIPT_TEMPLATE.format(text=text)

    return call_gemini(prompt)

# ---------------- QUIZ GENERATION ----------------
def generate_quiz(text: str) -> Quiz:
    prompt = QUIZ_PROMPT + "\n\n" + text
    response = call_gemini(prompt)

    if not response or not response.strip():
        raise ValueError("Gemini returned empty response")

    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        quiz_data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Gemini returned invalid JSON:\n{response}")

    return Quiz(**quiz_data)
