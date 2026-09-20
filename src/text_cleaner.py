"""Text normalization and cleaning utilities."""

from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize unicode, whitespace, and common resume punctuation safely."""
    if not text:
        return ""

    normalized = unicodedata.normalize("NFKC", str(text))
    normalized = normalized.replace("\u00a0", " ")
    normalized = normalized.replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def clean_text(text: str) -> str:
    """Return analysis-ready text while preserving useful tokens like emails and URLs."""
    normalized = normalize_text(text)
    if not normalized:
        return ""

    cleaned = normalized.lower()
    cleaned = re.sub(r"[^\w\s@./:+#-]", " ", cleaned)
    cleaned = re.sub(r"(?<!\w)[_/.-]{2,}(?!\w)", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()
