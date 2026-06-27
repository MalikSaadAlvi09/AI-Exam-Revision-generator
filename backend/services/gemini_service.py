"""Gemini integration service with resilient JSON extraction."""

import json
import os
from typing import Any, Dict

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def _fallback_response(section: str) -> Dict[str, Any]:
    """Provide deterministic fallback when API is unavailable."""
    return {
        "message": f"Gemini API is not configured. {section} was generated using local fallback.",
        "items": [],
    }


def generate_json(section: str, source_text: str) -> Dict[str, Any]:
    """Generate structured revision content using Gemini and parse JSON output."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return _fallback_response(section)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = (
        "Return strictly valid JSON with no markdown. "
        f"Generate high-quality '{section}' revision output for this study material: {source_text[:12000]}"
    )
    result = model.generate_content(prompt)
    text = (result.text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return {"message": text or "Generation failed", "items": []}
