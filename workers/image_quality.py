from pathlib import Path
from pypdf import PdfReader


def inspect_page_dimensions(file_path: str) -> dict:
    """Report PDF page dimensions and flag unusually small pages."""
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

        pages = list(reader.pages)
        if not pages:
            return {"status": "error", "reason": "no_pages"}

        results = []

        for number, page in enumerate(pages, start=1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            results.append({
                "page": number,
                "width_points": round(width, 2),
                "height_points": round(height, 2),
                "small_page_warning": min(width, height) < 200,
            })

        return {
            "status": "checked",
            "page_count": len(results),
            "pages": results,
        }

    except Exception:
        return {"status": "error", "reason": "unreadable_pdf"}
