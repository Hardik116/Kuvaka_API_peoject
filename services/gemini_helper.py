import os
import json
import google.generativeai as genai

# Configure Gemini API with key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"


def call_gemini(prompt: str) -> str:
    """
    Call Gemini API with a prompt and return the raw text response.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""



def clean_gemini_response(text: str) -> dict:
    """
    Clean Gemini output by removing code fences and parse JSON.
    Returns a dictionary or empty dict if parsing fails.
    """
    if not text:
        return {}

    text = text.strip()
    # Remove code fences if present
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()

    try:
        return json.loads(text)  # Convert string to dictionary
    except json.JSONDecodeError:
        # Fallback: return empty dict if parsing fails
        return {}