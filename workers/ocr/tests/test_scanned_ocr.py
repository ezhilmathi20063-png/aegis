from pypdf import PdfWriter

from workers.ocr.scanned_ocr import extract_scanned_pdf


def test_page_number_zero_is_rejected(tmp_path):
    sample = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with sample.open("wb") as output:
        writer.write(output)

    result = extract_scanned_pdf(str(sample), page_number=0)

    assert result["status"] == "error"
    assert result["reason"] == "invalid_page_number"


def test_page_number_beyond_pdf_is_rejected(tmp_path):
    sample = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with sample.open("wb") as output:
        writer.write(output)

    result = extract_scanned_pdf(str(sample), page_number=2)

    assert result["status"] == "error"
    assert result["reason"] == "page_out_of_range"
