from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EntityOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str
    entity_type: str
    aliases: list
    description: str | None
    entity_metadata: dict
    first_seen: datetime | None
    last_seen: datetime | None
    created_at: datetime


class EntityRelationshipOut(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    source_entity_id: UUID
    target_entity_id: UUID
    relationship_type: str
    confidence: float
    evidence_signal_ids: list
    first_seen: datetime | None
    last_seen: datetime | None
    rel_metadata: dict


class GraphTimelineEntry(BaseModel):
    timestamp: datetime
    event_type: str
    title: str
    summary: str
    severity: int
    confidence: float


class GraphTimelineOut(BaseModel):
    entity_id: UUID
    entity_name: str
    timeline: list[GraphTimelineEntry]


class EntityWithRelationships(BaseModel):
    entity: EntityOut
    outgoing: list[EntityRelationshipOut]
    incoming: list[EntityRelationshipOut]
