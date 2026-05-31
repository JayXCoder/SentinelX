from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class EventType(StrEnum):
    cyber_incident = "cyber_incident"
    vendor_risk_event = "vendor_risk_event"
    market_opportunity = "market_opportunity"
    competitor_movement = "competitor_movement"
    financial_instability = "financial_instability"
    reputation_event = "reputation_event"
    executive_alert = "executive_alert"


class CorrelatedEventOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    event_type: str
    title: str
    summary: str
    involved_entities: list
    signal_ids: list
    correlation_reason: str
    confidence: float
    severity: int
    first_seen: datetime | None
    last_seen: datetime | None
    created_at: datetime


class CorrelationRunRequest(BaseModel):
    signal_types: list[str] | None = None
    time_window_hours: int = Field(default=72, ge=1, le=720)
    min_signals: int = Field(default=2, ge=1)


class CorrelationRunResult(BaseModel):
    events_created: int
    signal_ids_processed: list[str]
    event_ids: list[str]
