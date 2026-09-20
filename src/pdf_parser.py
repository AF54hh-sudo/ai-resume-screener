"""PDF parsing helpers for uploaded resume files."""

from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

from src.text_cleaner import normalize_text


class PDFExtractionError(ValueError):
    """Raised when a PDF cannot be read or contains no extractable text."""


def _read_uploaded_file(uploaded_file: BinaryIO | BytesIO) -> bytes:
    if uploaded_file is None:
        raise PDFExtractionError("No PDF file was provided.")

    try:
        if hasattr(uploaded_file, "getvalue"):
            data = uploaded_file.getvalue()
        else:
            current_position = uploaded_file.tell() if hasattr(uploaded_file, "tell") else None
            data = uploaded_file.read()
            if current_position is not None and hasattr(uploaded_file, "seek"):
                uploaded_file.seek(current_position)
    except Exception as exc:
        raise PDFExtractionError("Could not read the uploaded PDF file.") from exc

    if not data:
        raise PDFExtractionError("The uploaded PDF is empty.")
    return data


def extract_text_from_pdf(uploaded_file: BinaryIO | BytesIO) -> str:
    """Extract normalized text from a PDF uploaded through Streamlit."""
    try:
        import fitz
    except ImportError as exc:
        raise PDFExtractionError(
            "PyMuPDF is not installed. Install dependencies with: pip install -r requirements.txt"
        ) from exc

    data = _read_uploaded_file(uploaded_file)

    try:
        with fitz.open(stream=data, filetype="pdf") as document:
            if document.page_count == 0:
                raise PDFExtractionError("The uploaded PDF has no pages.")

            page_text = []
            for page in document:
                text = page.get_text("text") or ""
                if text.strip():
                    page_text.append(text)
    except PDFExtractionError:
        raise
    except Exception as exc:
        raise PDFExtractionError("The uploaded PDF could not be parsed.") from exc

    extracted = normalize_text("\n\n".join(page_text))
    if not extracted:
        raise PDFExtractionError(
            "No readable text was found. The PDF may be scanned or image-only."
        )
    return extracted
