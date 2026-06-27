"""Image OCR extraction service."""

from PIL import Image
import pytesseract


def extract_image_text(file_path: str) -> str:
    """Run OCR on image files containing notes."""
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)
