from pypdf import PdfWriter
from pypdf.generic import (
    DictionaryObject,
    NameObject,
    DecodedStreamObject,
)

from workers.ocr.extract_text import extract_pdf_text


def test_extracts_text_and_page_number(tmp_path):
    sample = tmp_path / "text.pdf"
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    stream = DecodedStreamObject()
    stream.set_data(
        b"BT /F1 12 Tf 72 720 Td (Aegis Synthetic Test) Tj ET"
    )
    page[NameObject("/Contents")] = writer._add_object(stream)

    font = DictionaryObject()
    font.update({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })

    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({
            NameObject("/F1"): writer._add_object(font)
        })
    })

    with sample.open("wb") as output:
        writer.write(output)

    result = extract_pdf_text(str(sample))

    assert result["status"] == "checked"
    assert result["page_count"] == 1
    assert result["pages"][0]["page_number"] == 1
    assert "Aegis Synthetic Test" in result["pages"][0]["text"]
    assert result["pages"][0]["needs_ocr"] is False


def test_missing_pdf_is_reported(tmp_path):
    result = extract_pdf_text(str(tmp_path / "missing.pdf"))

    assert result["status"] == "error"
    assert result["reason"] == "file_not_found"
