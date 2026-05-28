from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.agents import AGENT_REGISTRY, DEFAULT_AGENTS
from app.db.models.intelligence_signal import IntelligenceSignal
from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.db.models.source import Source
from app.schemas.signal import AgentInput, KaiZheSignalExport
from app.services.embedding_service import EmbeddingService
from app.services.redis_stream_service import SIGNAL_STREAM_BY_TYPE, get_redis_stream_service
from app.services.sglang_service import SGLangService


class AgentProcessingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.streams = get_redis_stream_service()
        self.embeddings = EmbeddingService()
        self.sglang = SGLangService()

    def process_record(
        self,
        parsed_record_id: UUID,
        agents: list[str] | None = None,
    ) -> list[IntelligenceSignal]:
        parsed = (
            self.db.query(ParsedRecord)
            .options(
                joinedload(ParsedRecord.raw_record).joinedload(RawRecord.source),
            )
            .filter(ParsedRecord.id == parsed_record_id)
            .first()
        )
        if not parsed:
            raise ValueError(f"Parsed record not found: {parsed_record_id}")

        source: Source = parsed.raw_record.source
        agent_input = AgentInput(
            record_id=str(parsed.id),
            source_type=source.source_type,
            title=parsed.title or "",
            clean_text=parsed.clean_text,
            entities=parsed.detected_entities or [],
            metadata=parsed.parsed_metadata or {},
        )

        self.embeddings.upsert(
            "parsed_records_embeddings",
            parsed.id,
            parsed.clean_text,
            {"parsed_record_id": str(parsed.id), "source_id": str(source.id)},
        )

        selected = agents or DEFAULT_AGENTS
        signals: list[IntelligenceSignal] = []

        for agent_name in selected:
            agent_cls = AGENT_REGISTRY.get(agent_name)
            if not agent_cls:
                continue
            agent = agent_cls(self.sglang)
            output = agent.process(agent_input)

            signal = IntelligenceSignal(
                parsed_record_id=parsed.id,
                signal_type=output.signal_type,
                category=output.category,
                title=output.title,
                summary=output.summary,
                entities=output.entities,
                severity=output.severity,
                confidence=output.confidence,
                source_reliability=output.source_reliability,
                evidence=output.evidence,
                recommended_action=output.recommended_action,
            )
            self.db.add(signal)
            self.db.commit()
            self.db.refresh(signal)
            signals.append(signal)

            stream = SIGNAL_STREAM_BY_TYPE.get(output.signal_type, "cyber_signals")
            export = self.to_kai_zhe_export(signal, source, parsed)
            self.streams.publish(stream, export.model_dump(mode="json"))

            typed_collection = f"{output.signal_type}_embeddings"
            if typed_collection in (
                "cyber_embeddings",
                "gtm_embeddings",
                "financial_embeddings",
                "vendor_risk_embeddings",
                "osint_embeddings",
            ):
                self.embeddings.upsert(
                    typed_collection,
                    signal.id,
                    f"{signal.title}\n{signal.summary}",
                    {"signal_id": str(signal.id), "signal_type": signal.signal_type},
                )
            self.embeddings.upsert(
                "intelligence_signals_embeddings",
                signal.id,
                f"{signal.title}\n{signal.summary}",
                {"signal_id": str(signal.id)},
            )

        return signals

    @staticmethod
    def to_kai_zhe_export(
        signal: IntelligenceSignal,
        source: Source,
        parsed: ParsedRecord,
    ) -> KaiZheSignalExport:
        return KaiZheSignalExport(
            signal_id=str(signal.id),
            signal_type=signal.signal_type,
            category=signal.category,
            title=signal.title,
            summary=signal.summary,
            entities=signal.entities or [],
            source={
                "source_id": str(source.id),
                "source_name": source.name,
                "source_url": source.base_url,
                "source_type": source.source_type,
            },
            timestamp=signal.created_at,
            severity=signal.severity,
            confidence=signal.confidence,
            source_reliability=signal.source_reliability,
            evidence=signal.evidence or [],
            recommended_action=signal.recommended_action,
        )
