import os
import google.generativeai as genai
from dotenv import load_dotenv

def get_gemini_client():
    """Initializes and returns the Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    return model

def generate_code(model, prompt):
    """
    Sends the prompt to Gemini and returns the generated code.
    """
    print("🤖 Sending prompt to Gemini...")
    try:
        response = model.generate_content(prompt, generation_config={'temperature': 0.1})
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return None
