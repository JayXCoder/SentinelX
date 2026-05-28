import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ParsedRecord(Base):
    __tablename__ = "parsed_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    raw_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raw_records.id"), nullable=False, unique=True
    )
    title: Mapped[str | None] = mapped_column(Text)
    clean_text: Mapped[str] = mapped_column(Text, nullable=False)
    detected_entities: Mapped[list] = mapped_column(JSONB, default=list)
    detected_language: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    parsed_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    raw_record = relationship("RawRecord", back_populates="parsed_record")
    signals = relationship("IntelligenceSignal", back_populates="parsed_record")
