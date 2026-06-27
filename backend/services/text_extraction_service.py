"""Unified file extraction gateway."""

from pathlib import Path

from backend.services.docx_service import extract_docx_text
from backend.services.ocr_service import extract_image_text
from backend.services.pdf_service import extract_pdf_text
from backend.services.ppt_service import extract_ppt_text


def extract_text_for_file(file_path: str, content_type: str) -> str:
    """Dispatch to format-specific extractor based on MIME or extension."""
    suffix = Path(file_path).suffix.lower()
    if content_type == "application/pdf" or suffix == ".pdf":
        return extract_pdf_text(file_path)
    if "word" in content_type or suffix == ".docx":
        return extract_docx_text(file_path)
    if "presentation" in content_type or suffix in {".ppt", ".pptx"}:
        return extract_ppt_text(file_path)
    if content_type.startswith("text/") or suffix == ".txt":
        return Path(file_path).read_text(encoding="utf-8", errors="ignore")
    if content_type.startswith("image/") or suffix in {".png", ".jpg", ".jpeg"}:
        return extract_image_text(file_path)
    raise ValueError("Unsupported file format")
