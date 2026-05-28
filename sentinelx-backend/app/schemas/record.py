from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RawRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: UUID
    scrape_job_id: UUID
    url: str
    raw_html: str | None
    raw_text: str | None
    content_hash: str
    fetched_at: datetime
    metadata: dict = Field(validation_alias="record_metadata")


class ParsedRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    raw_record_id: UUID
    title: str | None
    clean_text: str
    detected_entities: list
    detected_language: str | None
    published_at: datetime | None
    parsed_metadata: dict
    created_at: datetime
