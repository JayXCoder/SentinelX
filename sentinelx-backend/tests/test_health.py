from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_status():
    response = client.get("/agents/status")
    assert response.status_code == 200
    assert "cyber" in response.json()["available_agents"]
