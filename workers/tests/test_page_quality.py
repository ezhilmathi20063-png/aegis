from pypdf import PdfWriter

from workers.page_quality import inspect_pdf_pages


def test_pdf_with_blank_page_is_reported(tmp_path):
    sample = tmp_path / "blank_page.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with sample.open("wb") as output:
        writer.write(output)

    result = inspect_pdf_pages(str(sample))

    assert result["status"] == "checked"
    assert result["page_count"] == 1
    assert result["pages_without_extractable_text"] == [1]


def test_missing_pdf_is_reported(tmp_path):
    result = inspect_pdf_pages(str(tmp_path / "missing.pdf"))

    assert result["status"] == "error"
    assert result["reason"] == "file_not_found"
