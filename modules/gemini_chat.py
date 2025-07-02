import google.generativeai as genai
from dotenv import load_dotenv
import os

# ─────────────────── Environment & model ────────────────────
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")  # supported everywhere

# ─────────────────── Persona / System prompt ────────────────
PERSONA_PROMPT = """
You are **FinZen**, a friendly, concise personal‑finance assistant who specialises
in analysing spending patterns and giving practical budgeting advice.
• When the user has uploaded a dataset, reference it if relevant.
• If the user asks a general money question, give clear, actionable tips.
• Keep answers jargon‑free and encouraging.
"""


# ─────────────────── Helper function ────────────────────────
def get_gemini_response(user_prompt: str, *, mode: str = "chat") -> str:
    """
    mode = "chat"       → prepend FinZen persona prompt (default)
    mode = "classify"   → raw prompt (used by classify_query for intents)
    """
    if mode == "chat":
        full_prompt = f"{PERSONA_PROMPT}\n\nUser: {user_prompt}\nAssistant:"
    else:  # "classify" or any other specialised use
        full_prompt = user_prompt

    response = model.generate_content(full_prompt)
    return response.text.strip()
