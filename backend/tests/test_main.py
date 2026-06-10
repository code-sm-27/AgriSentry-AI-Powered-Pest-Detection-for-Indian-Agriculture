import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_detect_no_file():
    response = client.post("/detect")
    assert response.status_code == 422 # Unprocessable Entity (missing file)

def test_detect_invalid_file():
    # Sending a simple text file instead of an image
    files = {"file": ("test.txt", b"this is not an image", "text/plain")}
    response = client.post("/detect", files=files)
    assert response.status_code == 500
    assert "detail" in response.json()
