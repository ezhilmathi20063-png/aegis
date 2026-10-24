from pathlib import Path
from pypdf import PdfReader


def inspect_pdf_pages(file_path: str) -> dict:
    """Report pages that have no extractable text.

    A page without extractable text may still contain a scanned image.
    """
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        return {"status": "error", "reason": "file_not_found"}

    if path.suffix.lower() != ".pdf":
        return {"status": "error", "reason": "not_a_pdf"}

    if path.stat().st_size == 0:
        return {"status": "error", "reason": "empty_file"}

    try:
        reader = PdfReader(str(path), strict=True)

        if reader.is_encrypted:
            return {"status": "error", "reason": "encrypted_pdf"}

        pages = list(reader.pages)

        if not pages:
            return {"status": "error", "reason": "no_pages"}

        pages_without_text = []

        for page_number, page in enumerate(pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                pages_without_text.append(page_number)

        return {
            "status": "checked",
            "page_count": len(pages),
            "pages_without_extractable_text": pages_without_text,
        }

    except Exception:
        return {"status": "error", "reason": "unreadable_pdf"}
