"""PDF extraction utilities."""

import fitz


def extract_pdf_text(file_path: str) -> str:
    """Extract all readable text from a PDF file."""
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text("text"))
    return "\n".join(text)
