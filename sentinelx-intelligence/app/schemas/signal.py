from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class SignalType(StrEnum):
    cyber = "cyber"
    gtm = "gtm"
    financial = "financial"
    vendor_risk = "vendor_risk"
    osint = "osint"
    executive_summary = "executive_summary"


class SignalSource(BaseModel):
    source_id: str | None = None
    source_name: str | None = None
    source_url: str | None = None
    source_type: str | None = None


class IntelSignalIn(BaseModel):
    """Schema for signals received from Jay's Redis streams."""

    signal_id: str
    signal_type: str
    category: str
    title: str
    summary: str
    entities: list = Field(default_factory=list)
    source: SignalSource | None = None
    timestamp: datetime | None = None
    severity: int = 0
    confidence: float = 0.0
    source_reliability: float = 0.0
    evidence: list = Field(default_factory=list)
    recommended_action: str | None = None


class IntelSignalOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    signal_id: str
    signal_type: str
    category: str
    title: str
    summary: str
    entities: list
    source_id: str | None
    source_name: str | None
    source_url: str | None
    source_type: str | None
    timestamp: datetime | None
    severity: int
    confidence: float
    source_reliability: float
    evidence: list
    recommended_action: str | None
    created_at: datetime
