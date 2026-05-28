import uuid
from datetime import datetime

from app.core.logging import get_logger
from app.db.models.intelligence_signal import IntelSignal
from app.db.session import SessionLocal
from app.schemas.signal import IntelSignalIn
from app.services.correlation_service import CorrelationService
from app.services.redis_stream_service import RedisStreamService
from app.workers.celery_app import celery_app

logger = get_logger(__name__)

INPUT_STREAMS = [
    "cyber_signals",
    "gtm_signals",
    "financial_signals",
    "vendor_risk_signals",
    "osint_signals",
    "executive_summaries",
]


def _store_signal(db, message: dict) -> IntelSignal | None:
    signal_id = message.get("signal_id")
    if not signal_id:
        logger.warning("Signal missing signal_id, skipping")
        return None

    existing = db.query(IntelSignal).filter(IntelSignal.signal_id == signal_id).first()
    if existing:
        return existing

    try:
        parsed = IntelSignalIn(**{k: v for k, v in message.items() if not k.startswith("_")})
    except Exception as exc:
        logger.error("Signal validation failed", extra={"error": str(exc), "signal_id": signal_id})
        return None

    source = parsed.source or {}
    source_dict = source.model_dump() if hasattr(source, "model_dump") else (source or {})

    ts = parsed.timestamp
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts)
        except ValueError:
            ts = None

    sig = IntelSignal(
        id=uuid.uuid4(),
        signal_id=parsed.signal_id,
        signal_type=parsed.signal_type,
        category=parsed.category,
        title=parsed.title,
        summary=parsed.summary,
        entities=parsed.entities or [],
        source_id=source_dict.get("source_id"),
        source_name=source_dict.get("source_name"),
        source_url=source_dict.get("source_url"),
        source_type=source_dict.get("source_type"),
        timestamp=ts,
        severity=parsed.severity,
        confidence=parsed.confidence,
        source_reliability=parsed.source_reliability,
        evidence=parsed.evidence or [],
        recommended_action=parsed.recommended_action,
    )
    db.add(sig)
    db.flush()
    return sig


@celery_app.task(name="app.workers.correlation_worker.correlate_signals_task", bind=True, max_retries=3)
def correlate_signals_task(self) -> dict:
    redis_svc = RedisStreamService()
    db = SessionLocal()
    new_signal_ids: list[str] = []

    try:
        for stream in INPUT_STREAMS:
            messages = redis_svc.read_pending(stream, count=50)
            for msg in messages:
                message_id = msg.pop("_message_id", None)
                sig = _store_signal(db, msg)
                if sig:
                    new_signal_ids.append(str(sig.id))
                if message_id:
                    redis_svc.ack(stream, message_id)

        db.commit()

        if not new_signal_ids:
            return {"signals_ingested": 0, "events_created": 0}

        svc = CorrelationService()
        events = svc.run_all(db)

        for event in events:
            redis_svc.publish("correlated_events", {
                "event_id": str(event.id),
                "event_type": event.event_type,
                "title": event.title,
                "severity": event.severity,
                "confidence": event.confidence,
                "signal_ids": event.signal_ids,
            })

        logger.info(
            "Correlation task complete",
            extra={"signals": len(new_signal_ids), "events": len(events)},
        )
        return {"signals_ingested": len(new_signal_ids), "events_created": len(events)}

    except Exception as exc:
        db.rollback()
        logger.error("Correlation task failed", extra={"error": str(exc)})
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()
