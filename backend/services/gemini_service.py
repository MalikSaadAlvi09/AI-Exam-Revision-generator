import os

import google.generativeai as genai
from fastapi import HTTPException


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "")
        if not text:
            raise HTTPException(status_code=502, detail="Empty response from Gemini")
        return text.strip()
