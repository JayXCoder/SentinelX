"""API key authentication — optional when API_KEY env is unset (local dev)."""

from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    settings = get_settings()
    expected = settings.api_key
    if not expected:
        return
    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
