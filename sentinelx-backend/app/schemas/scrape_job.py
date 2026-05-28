from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScrapeJobCreate(BaseModel):
    source_id: UUID


class ScrapeJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: UUID
    status: str
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None
    records_collected: int
    retry_count: int
    created_at: datetime
