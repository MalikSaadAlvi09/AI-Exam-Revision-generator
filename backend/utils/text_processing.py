"""Text normalization helpers for extraction pipeline."""

import re
from collections import OrderedDict


def clean_text(text: str) -> str:
    """Normalize whitespace and remove repeated lines from extracted text."""
    normalized = re.sub(r"\s+", " ", text or "").strip()
    if not normalized:
        return ""
    lines = [line.strip() for line in re.split(r"(?<=[.!?])\s+", normalized) if line.strip()]
    unique = OrderedDict((line, None) for line in lines)
    return "\n".join(unique.keys())


def split_sections(text: str, max_chars: int = 1500) -> list[str]:
    """Split text into compact prompt-friendly sections."""
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(" ".join(current)) >= max_chars:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks
