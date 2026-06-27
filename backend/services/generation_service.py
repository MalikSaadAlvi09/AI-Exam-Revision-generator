from typing import Dict

from backend.services.gemini_service import GeminiService


class GenerationService:
    OUTPUT_PROMPTS = {
        "mcqs": "Generate 50 MCQs with 4 options, correct answer, explanation, and difficulty levels.",
        "flashcards": "Generate concise flashcards with question, answer, and category.",
        "important": "Generate likely exam questions including long, short, and definition-based questions.",
        "summary": "Generate summaries in 500 words, 100 words, 50 words, and 10 lines.",
        "cheatsheet": "Generate a one-page exam cheat sheet with formulas, keywords, and memory tricks.",
        "revision": "Generate a 10-minute revision guide focusing on high-impact topics.",
        "key_concepts": "Extract key concepts with brief explanations.",
        "formula_sheet": "Generate a formula sheet where applicable. If not applicable, state clearly.",
        "definitions": "Generate essential definitions from the material.",
        "interview_questions": "Generate interview questions and ideal answers based on the material.",
    }

    def __init__(self):
        self.gemini = GeminiService()

    def generate_all(self, source_text: str) -> Dict[str, str]:
        cleaned = self._clean_text(source_text)
        outputs: Dict[str, str] = {}
        for key, instruction in self.OUTPUT_PROMPTS.items():
            prompt = (
                "You are an expert exam prep assistant. "
                f"{instruction}\n\n"
                "Material:\n"
                f"{cleaned}"
            )
            outputs[key] = self.gemini.generate(prompt)
        return outputs

    @staticmethod
    def _clean_text(text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        unique_lines = list(dict.fromkeys(lines))
        return "\n".join(unique_lines)
