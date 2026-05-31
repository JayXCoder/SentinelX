import uuid

from app.core.logging import get_logger
from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.intelligence_signal import IntelSignal
from app.db.session import SessionLocal
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.services.rag_service import RAGService
from app.services.redis_stream_service import RedisStreamService
from app.workers.celery_app import celery_app

logger = get_logger(__name__)


@celery_app.task(
    name="app.workers.graph_worker.update_knowledge_graph_task",
    bind=True,
    max_retries=3,
)
def update_knowledge_graph_task(
    self,
    signal_ids: list[str],
    event_id: str | None = None,
) -> dict:
    db = SessionLocal()
    redis_svc = RedisStreamService()
    kg_svc = KnowledgeGraphService()
    rag_svc = RAGService()

    entities_upserted = 0
    relationships_created = 0
    rag_memories_stored = 0

    try:
        signals = db.query(IntelSignal).filter(
            IntelSignal.id.in_([uuid.UUID(sid) for sid in signal_ids])
        ).all()

        for sig in signals:
            sig_entities = []
            for ent in (sig.entities or []):
                if isinstance(ent, dict):
                    name = (ent.get("name") or ent.get("text") or "").strip()
                    ent_dict = ent
                elif isinstance(ent, str):
                    name = ent.strip()
                    ent_dict = None
                else:
                    continue
                if not name:
                    continue
                entity = kg_svc.upsert_entity(db, name, ent_dict=ent_dict)
                sig_entities.append(entity)
                entities_upserted += 1

            for i, src in enumerate(sig_entities):
                for tgt in sig_entities[i + 1:]:
                    kg_svc.create_relationship(
                        db,
                        src.id,
                        tgt.id,
                        "mentioned_with",
                        confidence=sig.confidence,
                        signal_ids=[str(sig.id)],
                    )
                    relationships_created += 1

            rag_svc.store_memory(
                db=db,
                text_chunk=f"{sig.title}\n\n{sig.summary}",
                memory_type="signal_summary",
                collection="signals_memory",
                metadata={
                    "signal_id": str(sig.id),
                    "signal_type": sig.signal_type,
                    "severity": sig.severity,
                    "confidence": sig.confidence,
                    "timestamp": sig.timestamp.isoformat() if sig.timestamp else None,
                    "source_type": sig.source_type,
                },
                signal_id=sig.id,
            )
            rag_memories_stored += 1

        event = None
        if event_id:
            event = db.query(CorrelatedEvent).filter(
                CorrelatedEvent.id == uuid.UUID(event_id)
            ).first()
            if event:
                rag_svc.store_memory(
                    db=db,
                    text_chunk=(
                        f"{event.title}\n\n{event.summary}\n\n"
                        f"Correlation: {event.correlation_reason}"
                    ),
                    memory_type="correlated_event",
                    collection="correlated_events_memory",
                    metadata={
                        "event_id": str(event.id),
                        "event_type": event.event_type,
                        "severity": event.severity,
                        "confidence": event.confidence,
                    },
                    event_id=event.id,
                )
                rag_memories_stored += 1

        db.commit()

        redis_svc.publish("graph_updates", {
            "signal_ids": signal_ids,
            "event_id": event_id or "",
            "entities_upserted": entities_upserted,
            "relationships_created": relationships_created,
        })

        redis_svc.publish("rag_memory_updates", {
            "signal_ids": signal_ids,
            "event_id": event_id or "",
            "memories_stored": rag_memories_stored,
        })

        logger.info(
            "Graph worker complete",
            extra={
                "signals": len(signal_ids),
                "entities": entities_upserted,
                "relationships": relationships_created,
                "rag_memories": rag_memories_stored,
            },
        )
        return {
            "entities_upserted": entities_upserted,
            "relationships_created": relationships_created,
            "rag_memories_stored": rag_memories_stored,
        }

    except Exception as exc:
        db.rollback()
        logger.error("Graph worker failed", extra={"error": str(exc)})
        raise self.retry(exc=exc, countdown=45) from exc
    finally:
        db.close()
