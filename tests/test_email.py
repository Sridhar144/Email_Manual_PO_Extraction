import pytest
from app.iterative_classifier import iterative_classification
from app.email_handler import extract_email_content
from app.po_extraction import extract_po_details


def test_classification():

    subject = "Purchase Order #12345"
    body = "Please find attached the PO details for your reference."
    
    classification, score = iterative_classification(subject, body, classifier=None) 
    assert classification == "PO"
    assert score > 0.8

def test_po_extraction():
    email_body = "Customer PO Number: 12345\nItem Name: Widget\nQuantity: 100\nRate per Unit: 50"
    po_details = extract_po_details(email_body, text_gen_model=None) 
    
    assert po_details["Customer PO Number"] == "12345"
    assert po_details["Item Names"] == ["Widget"]
    assert po_details["Quantities"] == ["100"]
    assert po_details["Rate per Unit"] == ["50"]
