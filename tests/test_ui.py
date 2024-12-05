import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the main UI route
def test_home_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Email Data" in response.data 


def test_home_post(client):
    response = client.post("/", data={
        "subject": "Purchase Order #12345",
        "body": "Please find attached the PO details."
    })
    assert response.status_code == 200
    assert b"PO" in response.data  
