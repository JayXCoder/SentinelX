import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EntityRelationship(Base):
    __tablename__ = "entity_relationships"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False
    )
    target_entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_signal_ids: Mapped[list] = mapped_column(JSONB, default=list)
    first_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rel_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    source_entity = relationship(
        "Entity",
        foreign_keys=[source_entity_id],
        back_populates="outgoing_relationships",
    )
    target_entity = relationship(
        "Entity",
        foreign_keys=[target_entity_id],
        back_populates="incoming_relationships",
    )
