from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AgentInput(BaseModel):
    record_id: str
    source_type: str
    title: str
    clean_text: str
    entities: list = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class AgentOutput(BaseModel):
    signal_type: str
    category: str
    title: str
    summary: str
    entities: list = Field(default_factory=list)
    severity: int = 0
    confidence: float = 0.0
    source_reliability: float = 0.0
    evidence: list = Field(default_factory=list)
    recommended_action: str = ""


class IntelligenceSignalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    parsed_record_id: UUID
    signal_type: str
    category: str
    title: str
    summary: str
    entities: list
    severity: int
    confidence: float
    source_reliability: float
    evidence: list
    recommended_action: str | None
    created_at: datetime


class KaiZheSignalExport(BaseModel):
    """Integration contract for Kai Zhe's correlation layer."""

    signal_id: str
    signal_type: str
    category: str
    title: str
    summary: str
    entities: list
    source: dict
    timestamp: datetime
    severity: int
    confidence: float
    source_reliability: float
    evidence: list
    recommended_action: str | None = None


class ProcessBatchRequest(BaseModel):
    parsed_record_ids: list[UUID]
    agents: list[str] | None = None
