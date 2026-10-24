from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(file_path: str) -> dict:
    """Extract selectable PDF text and preserve page numbers."""
    path = Path(file_path)

    if not path.is_file():
        return {"status": "error", "reason": "file_not_found"}

    if path.suffix.lower() != ".pdf":
        return {"status": "error", "reason": "not_a_pdf"}

    if path.stat().st_size == 0:
        return {"status": "error", "reason": "empty_file"}

    try:
        reader = PdfReader(str(path), strict=True)

        if reader.is_encrypted:
            return {"status": "error", "reason": "encrypted_pdf"}

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()

            pages.append({
                "page_number": page_number,
                "text": text,
                "needs_ocr": not bool(text),
            })

        if not pages:
            return {"status": "error", "reason": "no_pages"}

        return {
            "status": "checked",
            "page_count": len(pages),
            "pages": pages,
        }

    except Exception:
        return {"status": "error", "reason": "unreadable_pdf"}
