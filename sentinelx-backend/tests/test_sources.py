import pytest
from app.main import app
from app.schemas.source import SourceCreate
from fastapi.testclient import TestClient
from pydantic import ValidationError

client = TestClient(app)


def test_create_source_rejects_invalid_url():
    response = client.post(
        "/sources",
        json={
            "name": "Bad",
            "source_type": "web",
            "base_url": "ftp://internal.local/secret",
            "category": "test",
        },
    )
    assert response.status_code == 422


def test_source_schema_accepts_https_url():
    model = SourceCreate(
        name="Example",
        source_type="web",
        base_url="https://example.com",
    )
    assert model.base_url.startswith("https://")


def test_source_schema_rejects_file_scheme():
    with pytest.raises(ValidationError):
        SourceCreate(
            name="Bad",
            source_type="web",
            base_url="file:///etc/passwd",
        )
