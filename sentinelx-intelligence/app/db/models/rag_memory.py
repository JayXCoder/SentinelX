import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RAGMemory(Base):
    __tablename__ = "rag_memory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qdrant_vector_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    source_signal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("intel_signals.id")
    )
    correlated_event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("correlated_events.id")
    )
    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id")
    )
    memory_type: Mapped[str] = mapped_column(String(64), nullable=False)
    text_chunk: Mapped[str] = mapped_column(Text, nullable=False)
    mem_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    signal = relationship("IntelSignal", back_populates="rag_memories")
    correlated_event = relationship("CorrelatedEvent", back_populates="rag_memories")
    entity = relationship("Entity", back_populates="rag_memories")
