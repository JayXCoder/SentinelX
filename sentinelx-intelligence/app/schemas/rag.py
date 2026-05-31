from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    text: str = Field(min_length=3)
    collection: str = "signals_memory"
    top_k: int = Field(default=5, ge=1, le=20)
    score_threshold: float = Field(default=0.5, ge=0.0, le=1.0)


class RAGAskRequest(BaseModel):
    question: str = Field(min_length=5)
    entity_id: UUID | None = None
    top_k: int = Field(default=5, ge=1, le=20)
    workspace_context: str | None = Field(default=None, max_length=12000)
    signal_context: str | None = Field(default=None, max_length=12000)


class RAGResponse(BaseModel):
    answer: str
    confidence: float
    supporting_evidence: list[str]
    related_entities: list[str]
    related_events: list[str]
    recommended_action: str


class RAGMemoryOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    qdrant_vector_id: str
    source_signal_id: UUID | None
    correlated_event_id: UUID | None
    entity_id: UUID | None
    memory_type: str
    text_chunk: str
    mem_metadata: dict
    created_at: datetime
