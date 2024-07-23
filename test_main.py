from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_pdf():
    with open("test.pdf", "rb") as pdf_file:
        response = client.post("/upload-pdf/", files={"file": ("test.pdf", pdf_file, "application/pdf")})
    assert response.status_code == 200
    assert "pdf_text" in response.json()

def test_query_pdf():
    query_request = {
        "question": "What is the summary of this document?",
        "pdf_text": "This is a sample PDF text for testing purposes."
    }
    response = client.post("/query-pdf/", json=query_request)
    assert response.status_code == 200
    assert "response" in response.json()
