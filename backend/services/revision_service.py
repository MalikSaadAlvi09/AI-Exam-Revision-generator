"""AI revision content generation orchestrator."""

from typing import Dict

from backend.services.gemini_service import generate_json

CONTENT_TYPES = {
    "mcqs": "50 exam-style MCQs with options, answers, explanations, and difficulty",
    "flashcards": "flashcards with question, answer, category, and topic",
    "important": "important likely exam questions including short/long/definitions/true-false",
    "summary": "summaries in 500 words, 100 words, 50 words, 10 lines, and 1 paragraph",
    "revision": "10-minute revision guide with key concepts, common mistakes, and exam hacks",
    "cheatsheet": "one-page cheat sheet with formulas, mnemonics, keywords, and tips",
    "definitions": "critical definitions and concise meanings",
    "formulas": "formula sheet if formulas exist, otherwise key relationships",
    "keyconcepts": "key concepts with hierarchy and dependency links",
    "interview": "interview questions and polished answers",
}


def generate_all_outputs(text: str) -> Dict[str, dict]:
    """Generate all revision assets for the uploaded material."""
    return {key: generate_json(prompt, text) for key, prompt in CONTENT_TYPES.items()}
