import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"


def call_gemini(prompt: str) -> str:
    """Call Gemini API and return raw text response"""
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else ""



def clean_gemini_response(text: str) -> dict:
    """Clean Gemini output by removing code fences and return a dict"""
    if not text:
        return {}

    text = text.strip()
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