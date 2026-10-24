
from pypdf import PdfWriter

from workers.preflight import check_file_exists, check_pdf


def test_missing_file_is_reported():
    result = check_file_exists("this_file_does_not_exist.pdf")
    assert result["status"] == "error"
    assert result["reason"] == "file_not_found"


def test_existing_file_is_ready(tmp_path):
    sample = tmp_path / "sample.pdf"
    sample.write_bytes(b"sample content")

    result = check_file_exists(str(sample))
    assert result["status"] == "ready_for_next_check"


def test_valid_pdf_reports_page_count(tmp_path):
    sample = tmp_path / "valid.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with sample.open("wb") as output:
        writer.write(output)

    result = check_pdf(str(sample))
    assert result["status"] == "ready_for_ocr"
    assert result["page_count"] == 1


def test_invalid_pdf_is_rejected(tmp_path):
    sample = tmp_path / "invalid.pdf"
    sample.write_bytes(b"This is not a real PDF")

    result = check_pdf(str(sample))
    assert result["status"] == "error"
    assert result["reason"] == "unreadable_pdf"


def test_non_pdf_is_rejected(tmp_path):
    sample = tmp_path / "notes.txt"
    sample.write_text("Hello Aegis", encoding="utf-8")

    result = check_pdf(str(sample))
    assert result["status"] == "error"
    assert result["reason"] == "not_a_pdf"
