from fastapi.testclient import TestClient
from ..app.main import app
from fastapi import status

client = TestClient(app)

def test_main():
    response = client.get("/health_check")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}