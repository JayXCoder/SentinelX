from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SentinelX Backend"
    debug: bool = Field(default=False, validation_alias="SENTINELX_DEBUG")
    api_prefix: str = ""
    cors_origins: str = "*"

    database_url: str = (
        "postgresql+psycopg2://sentinelx:sentinelx@postgres:5432/sentinelx"
    )
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None

    sglang_base_url: str = "http://sglang_qwen:30000"
    sglang_model: str = "Qwen/Qwen3.5-2B"
    sglang_timeout_seconds: float = 120.0
    sglang_max_retries: int = 3

    bright_data_username: str | None = None
    bright_data_password: str | None = None
    bright_data_host: str = "brd.superproxy.io"
    bright_data_port: int = 22225
    bright_data_enabled: bool = False

    scrape_max_retries: int = 3
    scrape_timeout_seconds: float = 60.0
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_vector_size: int = 384

    stream_max_len: int = 10000
    stream_block_ms: int = 5000


@lru_cache
def get_settings() -> Settings:
    return Settings()
