"""PowerPoint extraction utilities."""

from pptx import Presentation


def extract_ppt_text(file_path: str) -> str:
    """Extract text from all slides in PPT/PPTX files."""
    presentation = Presentation(file_path)
    lines = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                lines.append(shape.text)
    return "\n".join(lines)
