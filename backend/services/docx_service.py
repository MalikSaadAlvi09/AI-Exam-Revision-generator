"""DOCX extraction utilities."""

from docx import Document


def extract_docx_text(file_path: str) -> str:
    """Extract paragraph text from DOCX notes."""
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
