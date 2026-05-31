from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Service ────────────────────────────────────────────────────────────
    # APP_NAME
    app_name: str = "SentinelX Intelligence"
    # SENTINELX_DEBUG
    debug: bool = Field(default=False, validation_alias="SENTINELX_DEBUG")
    # CORS_ORIGINS  (comma-separated, e.g. "http://localhost:3000,https://app.example.com")
    cors_origins: str = Field(default="*", validation_alias="CORS_ORIGINS")
    # API_KEY — when set, mutating routes require X-API-Key header
    api_key: str | None = Field(default=None, validation_alias="API_KEY")
    rate_limit_per_minute: int = Field(default=60, validation_alias="RATE_LIMIT_PER_MINUTE")

    # ── Database ───────────────────────────────────────────────────────────
    # DATABASE_URL
    database_url: str = Field(
        default="postgresql+psycopg2://sentinelx:sentinelx@postgres:5432/sentinelx",
        validation_alias="DATABASE_URL",
    )

    # ── Redis / Celery ─────────────────────────────────────────────────────
    # REDIS_URL
    redis_url: str = Field(default="redis://redis:6379/0", validation_alias="REDIS_URL")
    # CELERY_BROKER_URL
    celery_broker_url: str = Field(default="redis://redis:6379/0", validation_alias="CELERY_BROKER_URL")
    # CELERY_RESULT_BACKEND
    celery_result_backend: str = Field(default="redis://redis:6379/1", validation_alias="CELERY_RESULT_BACKEND")

    # ── Qdrant ─────────────────────────────────────────────────────────────
    # QDRANT_URL
    qdrant_url: str = Field(default="http://qdrant:6333", validation_alias="QDRANT_URL")
    # QDRANT_API_KEY  (leave blank for local/unauthenticated)
    qdrant_api_key: str | None = Field(default=None, validation_alias="QDRANT_API_KEY")

    # ── SGLang / Qwen ──────────────────────────────────────────────────────
    # SGLANG_BASE_URL
    sglang_base_url: str = Field(default="http://sglang_qwen:30000", validation_alias="SGLANG_BASE_URL")
    # SGLANG_MODEL
    sglang_model: str = Field(default="Qwen/Qwen3.5-2B", validation_alias="SGLANG_MODEL")
    # SGLANG_TIMEOUT_SECONDS
    sglang_timeout_seconds: float = Field(default=120.0, validation_alias="SGLANG_TIMEOUT_SECONDS")
    # SGLANG_MAX_RETRIES
    sglang_max_retries: int = Field(default=3, validation_alias="SGLANG_MAX_RETRIES")

    # ── Embeddings ─────────────────────────────────────────────────────────
    # EMBEDDING_MODEL
    embedding_model: str = Field(default="BAAI/bge-small-en-v1.5", validation_alias="EMBEDDING_MODEL")
    # EMBEDDING_VECTOR_SIZE
    embedding_vector_size: int = Field(default=384, validation_alias="EMBEDDING_VECTOR_SIZE")

    # ── Redis Streams ──────────────────────────────────────────────────────
    # STREAM_MAX_LEN
    stream_max_len: int = Field(default=10000, validation_alias="STREAM_MAX_LEN")
    # STREAM_BLOCK_MS
    stream_block_ms: int = Field(default=5000, validation_alias="STREAM_BLOCK_MS")

    # ── Correlation ────────────────────────────────────────────────────────
    # CORRELATION_TIME_WINDOW_HOURS
    correlation_time_window_hours: int = Field(default=72, validation_alias="CORRELATION_TIME_WINDOW_HOURS")
    # CORRELATION_MIN_SIGNALS
    correlation_min_signals: int = Field(default=2, validation_alias="CORRELATION_MIN_SIGNALS")

    # ── Consumer group (Celery / Redis stream consumer) ────────────────────
    # CONSUMER_GROUP
    consumer_group: str = Field(default="intelligence_layer", validation_alias="CONSUMER_GROUP")
    # CONSUMER_NAME  (unique per worker replica)
    consumer_name: str = Field(default="intel_worker_1", validation_alias="CONSUMER_NAME")


@lru_cache
def get_settings() -> Settings:
    return Settings()
