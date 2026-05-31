from fastapi.testclient import TestClient

from app.main import app


def test_api_key_required_when_configured(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-secret-key")

    client = TestClient(app)
    response = client.post(
        "/sources",
        json={
            "name": "Secured",
            "source_type": "web",
            "base_url": "https://example.com",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"
