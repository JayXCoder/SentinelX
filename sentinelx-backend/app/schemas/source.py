from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SourceBase(BaseModel):
    name: str
    source_type: str
    base_url: str
    category: str | None = None
    scraping_strategy: str = "http"
    frequency_minutes: int = 60
    is_active: bool = True


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: str | None = None
    source_type: str | None = None
    base_url: str | None = None
    category: str | None = None
    scraping_strategy: str | None = None
    frequency_minutes: int | None = None
    is_active: bool | None = None


class SourceRead(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
