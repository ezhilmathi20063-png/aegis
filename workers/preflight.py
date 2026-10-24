
from pathlib import Path
from pypdf import PdfReader


def check_file_exists(file_path: str) -> dict:
    """Check whether a document exists and is not empty."""
    path = Path(file_path)

    if not path.exists():
        return {"status": "error", "reason": "file_not_found"}

    if not path.is_file():
        return {"status": "error", "reason": "not_a_file"}

    if path.stat().st_size == 0:
        return {"status": "error", "reason": "empty_file"}

    return {"status": "ready_for_next_check", "reason": None}


def check_pdf(file_path: str) -> dict:
    """Check whether a file can be read as a PDF and count its pages."""
    basic_check = check_file_exists(file_path)

    if basic_check["status"] == "error":
        return basic_check

    path = Path(file_path)

    if path.suffix.lower() != ".pdf":
        return {"status": "error", "reason": "not_a_pdf"}

    try:
        reader = PdfReader(str(path), strict=True)

        if reader.is_encrypted:
            return {"status": "error", "reason": "encrypted_pdf"}

        page_count = len(reader.pages)

        if page_count == 0:
            return {"status": "error", "reason": "no_pages"}

        return {
            "status": "ready_for_ocr",
            "reason": None,
            "page_count": page_count,
        }

    except Exception:
        return {"status": "error", "reason": "unreadable_pdf"}

def get_pdf_page_rotations(file_path: str) -> dict:
    """Report declared rotation metadata for each PDF page."""
    basic_check = check_pdf(file_path)

    if basic_check["status"] != "ready_for_ocr":
        return basic_check

    try:
        reader = PdfReader(str(file_path))
        rotations = [page.rotation for page in reader.pages]

        return {
            "status": "checked",
            "page_rotations": rotations,
            "rotated_pages": [
                index + 1
                for index, rotation in enumerate(rotations)
                if rotation % 360 != 0
            ],
        }

    except Exception:
        return {"status": "error", "reason": "unreadable_pdf"}
