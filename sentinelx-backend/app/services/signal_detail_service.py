from uuid import UUID

from app.db.models.human_note import HumanNote
from app.db.models.intelligence_signal import IntelligenceSignal
from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.schemas.signal import IntelligenceSignalRead
from app.schemas.signal_detail import (
    RecordExcerpt,
    SignalDetailResponse,
    SourceProvenance,
    StoryEvent,
)
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload


class SignalDetailService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_detail(self, signal_id: UUID) -> SignalDetailResponse | None:
        signal = (
            self.db.query(IntelligenceSignal)
            .options(
                joinedload(IntelligenceSignal.parsed_record)
                .joinedload(ParsedRecord.raw_record)
                .joinedload(RawRecord.source)
            )
            .filter(IntelligenceSignal.id == signal_id)
            .first()
        )
        if not signal:
            return None

        parsed = signal.parsed_record
        raw = parsed.raw_record
        source = raw.source

        entity_names = [
            e if isinstance(e, str) else e.get("value", str(e))
            for e in (signal.entities or [])
        ]

        related_query = self.db.query(IntelligenceSignal).filter(
            IntelligenceSignal.id != signal.id
        )
        if entity_names:
            clauses = [IntelligenceSignal.entities.contains([name]) for name in entity_names[:5]]
            related_query = related_query.filter(or_(*clauses))
        else:
            related_query = related_query.filter(
                IntelligenceSignal.parsed_record_id == signal.parsed_record_id
            )

        related = (
            related_query.order_by(IntelligenceSignal.created_at.desc()).limit(8).all()
        )

        notes = (
            self.db.query(HumanNote)
            .filter(
                HumanNote.target_type == "signal",
                HumanNote.target_id == str(signal_id),
            )
            .order_by(HumanNote.created_at.desc())
            .all()
        )

        story: list[StoryEvent] = [
            StoryEvent(
                id=str(signal.id),
                event_type="signal",
                title=signal.title,
                summary=signal.summary[:500],
                occurred_at=signal.created_at,
                severity=signal.severity,
                source_label=source.name if source else None,
            )
        ]
        for rel in reversed(related[-5:]):
            story.insert(
                0,
                StoryEvent(
                    id=str(rel.id),
                    event_type="related_signal",
                    title=rel.title,
                    summary=rel.summary[:300],
                    occurred_at=rel.created_at,
                    severity=rel.severity,
                    source_label=source.name if source else None,
                ),
            )

        excerpt = (parsed.clean_text or "")[:4000]

        return SignalDetailResponse(
            signal=IntelligenceSignalRead.model_validate(signal),
            source=SourceProvenance(
                source_id=source.id,
                source_name=source.name,
                source_url=source.base_url,
                source_type=source.source_type,
                category=source.category,
            ),
            record=RecordExcerpt(
                parsed_record_id=parsed.id,
                title=parsed.title,
                excerpt=excerpt,
                url=raw.url,
                fetched_at=raw.fetched_at,
                content_hash=raw.content_hash,
            ),
            related_signals=[
                IntelligenceSignalRead.model_validate(s) for s in related
            ],
            story_timeline=sorted(story, key=lambda e: e.occurred_at),
            human_notes=[
                {
                    "id": str(n.id),
                    "team_role": n.team_role,
                    "author_name": n.author_name,
                    "content": n.content,
                    "created_at": n.created_at.isoformat(),
                }
                for n in notes
            ],
        )
