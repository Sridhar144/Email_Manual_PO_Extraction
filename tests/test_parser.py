import pytest
from app.file_parser import parse_pdf, parse_image

def test_parse_pdf():

    text = parse_pdf("tests/sample_files/sample_po.pdf")
    assert "PO Number" in text
    assert "Item Name" in text
    assert "Quantity" in text


def test_parse_image():
   
    text = parse_image("tests/sample_files/sample_image_po.png")
    assert "PO Number" in text
    assert "Item Name" in text
    assert "Quantity" in text
