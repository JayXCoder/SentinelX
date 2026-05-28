import json
from typing import Any

import redis

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

INPUT_STREAMS = [
    "cyber_signals",
    "gtm_signals",
    "financial_signals",
    "vendor_risk_signals",
    "osint_signals",
    "executive_summaries",
]

OUTPUT_STREAMS = [
    "correlated_events",
    "risk_scores",
    "graph_updates",
    "rag_memory_updates",
    "executive_alerts",
]

ALL_STREAMS = INPUT_STREAMS + OUTPUT_STREAMS


class RedisStreamService:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = redis.from_url(settings.redis_url, decode_responses=True)
        self._max_len = settings.stream_max_len
        self._group = settings.consumer_group
        self._consumer = settings.consumer_name

    @property
    def client(self) -> redis.Redis:
        return self._client

    def ensure_streams(self) -> None:
        for name in ALL_STREAMS:
            try:
                self._client.xinfo_stream(name)
            except redis.exceptions.ResponseError:
                self._client.xadd(name, {"init": "1"}, maxlen=self._max_len)
                logger.info("Created stream", extra={"stream": name})

        for name in INPUT_STREAMS:
            try:
                self._client.xgroup_create(name, self._group, id="0", mkstream=True)
                logger.info("Created consumer group", extra={"stream": name, "group": self._group})
            except redis.exceptions.ResponseError as exc:
                if "BUSYGROUP" not in str(exc):
                    logger.warning("Consumer group error", extra={"stream": name, "error": str(exc)})

    def publish(self, stream: str, payload: dict[str, Any]) -> str:
        data = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in payload.items()
        }
        message_id = self._client.xadd(stream, data, maxlen=self._max_len)
        logger.info("Published to stream", extra={"stream": stream, "id": message_id})
        return message_id

    def read_pending(
        self,
        stream: str,
        count: int = 10,
    ) -> list[dict[str, Any]]:
        try:
            results = self._client.xreadgroup(
                groupname=self._group,
                consumername=self._consumer,
                streams={stream: ">"},
                count=count,
                block=0,
            )
        except Exception as exc:
            logger.error("Stream read failed", extra={"stream": stream, "error": str(exc)})
            return []

        messages: list[dict[str, Any]] = []
        if not results:
            return messages

        for _stream_name, entries in results:
            for message_id, fields in entries:
                parsed: dict[str, Any] = {"_message_id": message_id}
                for k, v in fields.items():
                    try:
                        parsed[k] = json.loads(v)
                    except (json.JSONDecodeError, TypeError):
                        parsed[k] = v
                messages.append(parsed)

        return messages

    def ack(self, stream: str, message_id: str) -> None:
        self._client.xack(stream, self._group, message_id)

    def ping(self) -> bool:
        return bool(self._client.ping())

    def stream_lengths(self) -> dict[str, int]:
        lengths: dict[str, int] = {}
        for name in ALL_STREAMS:
            try:
                info = self._client.xinfo_stream(name)
                lengths[name] = info.get("length", 0)
            except redis.exceptions.ResponseError:
                lengths[name] = 0
        return lengths


def get_redis_stream_service() -> RedisStreamService:
    return RedisStreamService()
