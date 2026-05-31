from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.signal import IntelligenceSignalRead


class SourceProvenance(BaseModel):
    source_id: UUID
    source_name: str
    source_url: str
    source_type: str
    category: str | None = None


class RecordExcerpt(BaseModel):
    parsed_record_id: UUID
    title: str | None = None
    excerpt: str = ""
    url: str | None = None
    fetched_at: datetime | None = None
    content_hash: str | None = None


class StoryEvent(BaseModel):
    id: str
    event_type: str
    title: str
    summary: str
    occurred_at: datetime
    severity: int = 0
    source_label: str | None = None


class SignalDetailResponse(BaseModel):
    signal: IntelligenceSignalRead
    source: SourceProvenance
    record: RecordExcerpt
    related_signals: list[IntelligenceSignalRead] = Field(default_factory=list)
    story_timeline: list[StoryEvent] = Field(default_factory=list)
    human_notes: list[dict] = Field(default_factory=list)
