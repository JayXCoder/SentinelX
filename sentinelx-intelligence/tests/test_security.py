from app.core.config import get_settings
from app.main import app
from fastapi.testclient import TestClient


def test_rag_ask_requires_api_key_when_configured(monkeypatch):
    monkeypatch.setenv("API_KEY", "intel-secret")
    get_settings.cache_clear()
    client = TestClient(app)

    response = client.post("/rag/ask", json={"question": "Summarize vendor risk"})
    assert response.status_code == 401

    ok = client.post(
        "/rag/ask",
        json={"question": "Summarize vendor risk"},
        headers={"X-API-Key": "intel-secret"},
    )
    assert ok.status_code in (200, 500, 503)
    get_settings.cache_clear()
    monkeypatch.delenv("API_KEY", raising=False)
