from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert len(response.text) > 0
