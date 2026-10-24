from PIL import Image, ImageDraw
import pymupdf

from workers.ocr.scanned_ocr import extract_scanned_pdf


def test_scanned_pdf_returns_recognized_text(tmp_path):
    # Create a synthetic image containing clear text.
    image_path = tmp_path / "synthetic_scan.png"
    image = Image.new("RGB", (1200, 400), "white")
    draw = ImageDraw.Draw(image)
    draw.text((60, 120), "AEGIS TEST DOCUMENT 12345", fill="black")
    image.save(image_path)

    # Embed the image into a PDF to simulate a scanned document.
    pdf_path = tmp_path / "synthetic_scan.pdf"

    with pymupdf.open() as document:
        page = document.new_page(width=600, height=200)
        page.insert_image(page.rect, filename=str(image_path))
        document.save(str(pdf_path))

    result = extract_scanned_pdf(str(pdf_path), page_number=1, dpi=150)

    assert result["status"] == "checked"
    assert result["page_number"] == 1
    assert isinstance(result["detections"], list)

    combined_text = " ".join(
        item["text"] for item in result["detections"]
    ).upper()

    assert "AEGIS" in combined_text
    assert any(
        item["page_number"] == 1
        for item in result["detections"]
    )
