import os

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///./.pytest-intel.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:4637/0")
os.environ.pop("API_KEY", None)


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    from app.core.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
