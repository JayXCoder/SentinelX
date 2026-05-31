from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class SourceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    source_type: str = Field(min_length=1, max_length=64)
    base_url: str
    category: str | None = Field(default=None, max_length=128)
    scraping_strategy: str = Field(default="http", max_length=32)
    frequency_minutes: int = Field(default=60, ge=1, le=10080)
    is_active: bool = True

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, value: str) -> str:
        parsed = HttpUrl(value)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("base_url must use http or https")
        return str(parsed)


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    source_type: str | None = Field(default=None, min_length=1, max_length=64)
    base_url: str | None = None
    category: str | None = Field(default=None, max_length=128)
    scraping_strategy: str | None = Field(default=None, max_length=32)
    frequency_minutes: int | None = Field(default=None, ge=1, le=10080)
    is_active: bool | None = None

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        parsed = HttpUrl(value)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("base_url must use http or https")
        return str(parsed)


class SourceRead(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
