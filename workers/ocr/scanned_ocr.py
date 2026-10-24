from pathlib import Path

import pymupdf
from paddleocr import PaddleOCR


def extract_scanned_pdf(
    file_path: str,
    page_number: int = 1,
    dpi: int = 150,
) -> dict:
    """Render one PDF page and return OCR text with evidence regions."""
    path = Path(file_path)

    if not path.is_file():
        return {"status": "error", "reason": "file_not_found"}

    if path.suffix.lower() != ".pdf":
        return {"status": "error", "reason": "not_a_pdf"}

    if page_number < 1:
        return {"status": "error", "reason": "invalid_page_number"}

    try:
        with pymupdf.open(str(path)) as document:
            if page_number > len(document):
                return {"status": "error", "reason": "page_out_of_range"}

            page = document[page_number - 1]
            pixmap = page.get_pixmap(dpi=dpi, alpha=False)
            image_path = path.parent / f"{path.stem}_ocr_page_{page_number}.png"

            try:
                pixmap.save(str(image_path))
                ocr = PaddleOCR(
                    use_doc_orientation_classify=False,
                    use_doc_unwarping=False,
                    use_textline_orientation=False,
                )
                result = ocr.predict(str(image_path))

                detections = []
                for item in result or []:
                    data = item.get("res", item) if isinstance(item, dict) else {}
                    texts = data.get("rec_texts", [])
                    scores = data.get("rec_scores", [])
                    boxes = data.get("rec_boxes", data.get("dt_polys", []))

                    for index, text in enumerate(texts):
                        box = boxes[index] if index < len(boxes) else None
                        if hasattr(box, "tolist"):
                            box = box.tolist()

                        detections.append({
                            "text": str(text),
                            "page_number": page_number,
                            "bbox": box,
                            "confidence": (
                                float(scores[index])
                                if index < len(scores) else None
                            ),
                        })

                return {
                    "status": "checked",
                    "page_number": page_number,
                    "dpi": dpi,
                    "detections": detections,
                }
            finally:
                if image_path.exists():
                    image_path.unlink()

    except Exception as exc:
        return {
            "status": "error",
            "reason": "ocr_failed",
            "detail": str(exc),
        }
