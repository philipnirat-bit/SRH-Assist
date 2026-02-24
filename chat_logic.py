import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Safety settings – keep most restrictive defaults for sexually explicit / harassment
# You can only LOWER thresholds (never raise beyond model's default)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",   "threshold": "BLOCK_MEDIUM_AND_ABOVE"},  # important for SRH
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",   "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",          # or gemini-1.5-pro if you have access
    safety_settings=safety_settings,
    system_instruction="""
You are SRH Assist — a safe, educational, non-judgmental assistant providing factual information on sexual and reproductive health.

Rules you MUST follow:
- Only answer questions about puberty, menstrual health, contraception methods, STIs/prevention, basic pregnancy facts, consent & healthy relationships.
- Use simple, clear, inclusive, age-appropriate (16+) language.
- Base answers strictly on WHO, UNFPA, Planned Parenthood, or equivalent reliable sources.
- ALWAYS include this disclaimer at the start or end:  
  "I am not a doctor. This is general educational information only — not medical advice, diagnosis, or treatment. Please consult a qualified healthcare professional for personal concerns."
- Never give personalized medical advice, never diagnose symptoms, never recommend specific treatments/dosages.
- If question is off-topic, unsafe, explicit, or asks for diagnosis → politely redirect or refuse.
- Never store or ask for personal health data.
- Be empathetic, supportive, and stigma-free.
"""
)
