import asyncio
import json
from datetime import datetime
from typing import Any

from app.core.logging import get_logger
from app.services.realtime_hub import get_realtime_hub
from app.services.redis_stream_service import get_redis_stream_service

logger = get_logger(__name__)

_listener_loop: asyncio.AbstractEventLoop | None = None

# Jay signal streams + Kai Zhe output streams (shared Redis)
REALTIME_WATCH_STREAMS = [
    "cyber_signals",
    "gtm_signals",
    "financial_signals",
    "vendor_risk_signals",
    "osint_signals",
    "executive_summaries",
    "correlated_events",
    "risk_scores",
    "executive_alerts",
]

SIGNAL_STREAMS = {
    "cyber_signals",
    "gtm_signals",
    "financial_signals",
    "vendor_risk_signals",
    "osint_signals",
    "executive_summaries",
}


def _parse_fields(fields: dict[str, str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for key, value in fields.items():
        if key == "init":
            continue
        try:
            parsed[key] = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            parsed[key] = value
    return parsed


def _iso_timestamp(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str) and value:
        return value
    return datetime.utcnow().isoformat() + "Z"


def stream_message_to_event(stream: str, fields: dict[str, str]) -> dict[str, Any] | None:
    payload = _parse_fields(fields)
    if not payload:
        return None

    if stream in SIGNAL_STREAMS:
        signal_id = payload.get("signal_id") or payload.get("id")
        if not signal_id:
            return None
        entities = payload.get("entities") or []
        return {
            "type": "new_signal",
            "data": {
                "id": str(signal_id),
                "signal_type": payload.get("signal_type", "cyber"),
                "category": payload.get("category", ""),
                "title": payload.get("title", ""),
                "summary": payload.get("summary", ""),
                "entities": [str(e) for e in entities],
                "severity": int(payload.get("severity", 0)),
                "confidence": float(payload.get("confidence", 0)),
                "source_reliability": float(payload.get("source_reliability", 0)),
                "evidence": payload.get("evidence") or [],
                "recommended_action": payload.get("recommended_action"),
                "created_at": _iso_timestamp(payload.get("timestamp")),
            },
        }

    if stream == "correlated_events":
        event_id = payload.get("event_id") or payload.get("id")
        if not event_id:
            return None
        signal_ids = payload.get("signal_ids") or []
        return {
            "type": "new_correlated_event",
            "data": {
                "id": str(event_id),
                "event_type": payload.get("event_type", "executive_alert"),
                "title": payload.get("title", "Correlated event"),
                "summary": payload.get("summary", ""),
                "involved_entities": payload.get("involved_entities") or [],
                "signal_ids": [str(s) for s in signal_ids],
                "correlation_reason": payload.get("correlation_reason", ""),
                "confidence": float(payload.get("confidence", 0)),
                "severity": int(payload.get("severity", 0)),
                "first_seen": _iso_timestamp(payload.get("first_seen")),
                "last_seen": _iso_timestamp(payload.get("last_seen")),
            },
        }

    if stream == "risk_scores":
        score_id = payload.get("score_id") or payload.get("id")
        if not score_id:
            return None
        return {
            "type": "new_risk_score",
            "data": {
                "id": str(score_id),
                "entity_id": str(payload.get("entity_id", score_id)),
                "entity_name": payload.get("entity_name", "Unknown"),
                "score_type": payload.get("score_type", "vendor_risk"),
                "score_value": float(payload.get("score_value", 0)),
                "risk_level": payload.get("risk_level", "medium"),
                "explanation": payload.get("explanation", ""),
                "calculated_at": _iso_timestamp(payload.get("calculated_at")),
            },
        }

    if stream == "executive_alerts":
        return {
            "type": "new_alert",
            "data": {
                "title": f"{payload.get('entity_name', 'Entity')} — {payload.get('risk_level', 'alert')}",
                "severity": payload.get("risk_level", "high"),
                "alert_type": payload.get("alert_type", "risk_score"),
                "explanation": payload.get("explanation", ""),
                "score_type": payload.get("score_type"),
                "score_value": payload.get("score_value"),
            },
        }

    return None


def poll_streams_once(last_ids: dict[str, str]) -> dict[str, str]:
    redis = get_redis_stream_service().client
    try:
        results = redis.xread(streams=last_ids, count=20, block=5000)
    except Exception as exc:
        logger.warning("Realtime stream poll failed: %s", exc)
        return last_ids

    if not results:
        return last_ids

    hub = get_realtime_hub()
    loop = _listener_loop

    for stream_name, entries in results:
        stream = stream_name if isinstance(stream_name, str) else stream_name.decode()
        for message_id, fields in entries:
            last_ids[stream] = message_id
            event = stream_message_to_event(stream, fields)
            if event and loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(hub.broadcast(event), loop)

    return last_ids


async def run_realtime_listener(stop_event: asyncio.Event) -> None:
    global _listener_loop
    _listener_loop = asyncio.get_running_loop()
    last_ids = {name: "$" for name in REALTIME_WATCH_STREAMS}
    logger.info("Realtime Redis listener started", extra={"streams": REALTIME_WATCH_STREAMS})

    while not stop_event.is_set():
        try:
            last_ids = await asyncio.to_thread(poll_streams_once, last_ids)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.error("Realtime listener error: %s", exc)
            await asyncio.sleep(2)

    logger.info("Realtime Redis listener stopped")
