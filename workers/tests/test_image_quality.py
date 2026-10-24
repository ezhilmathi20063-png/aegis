from pypdf import PdfWriter

from workers.image_quality import inspect_page_dimensions


def test_normal_page_dimensions_are_reported(tmp_path):
    sample = tmp_path / "normal.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    with sample.open("wb") as output:
        writer.write(output)

    result = inspect_page_dimensions(str(sample))

    assert result["status"] == "checked"
    assert result["page_count"] == 1
    assert result["pages"][0]["width_points"] == 612
    assert result["pages"][0]["height_points"] == 792
    assert result["pages"][0]["small_page_warning"] is False


def test_small_page_gets_warning(tmp_path):
    sample = tmp_path / "small.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=150)

    with sample.open("wb") as output:
        writer.write(output)

    result = inspect_page_dimensions(str(sample))

    assert result["status"] == "checked"
    assert result["pages"][0]["small_page_warning"] is True
