import json
from typing import Any

import redis

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

STREAM_NAMES = [
    "scrape_jobs",
    "raw_records",
    "parsed_records",
    "cyber_signals",
    "gtm_signals",
    "financial_signals",
    "vendor_risk_signals",
    "osint_signals",
    "executive_summaries",
]

SIGNAL_STREAM_BY_TYPE = {
    "cyber": "cyber_signals",
    "gtm": "gtm_signals",
    "financial": "financial_signals",
    "vendor_risk": "vendor_risk_signals",
    "osint": "osint_signals",
    "executive_summary": "executive_summaries",
}


class RedisStreamService:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = redis.from_url(settings.redis_url, decode_responses=True)
        self._max_len = settings.stream_max_len

    @property
    def client(self) -> redis.Redis:
        return self._client

    def ensure_streams(self) -> None:
        for name in STREAM_NAMES:
            try:
                self._client.xinfo_stream(name)
            except redis.exceptions.ResponseError:
                self._client.xadd(name, {"init": "1"}, maxlen=self._max_len)
                logger.info("Created redis stream", extra={"stream": name})

    def publish(self, stream: str, payload: dict[str, Any]) -> str:
        self.ensure_streams()
        data = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in payload.items()}
        message_id = self._client.xadd(stream, data, maxlen=self._max_len)
        logger.info("Published to stream", extra={"stream": stream, "id": message_id})
        return message_id

    def stream_info(self, stream: str) -> dict[str, Any]:
        try:
            info = self._client.xinfo_stream(stream)
            return {
                "name": stream,
                "length": info.get("length", 0),
                "groups": info.get("groups", 0),
                "last_generated_id": info.get("last-generated-id"),
            }
        except redis.exceptions.ResponseError:
            return {"name": stream, "length": 0, "exists": False}

    def all_streams_info(self) -> list[dict[str, Any]]:
        return [self.stream_info(name) for name in STREAM_NAMES]

    def backlog_size(self) -> dict[str, int]:
        return {name: self.stream_info(name).get("length", 0) for name in STREAM_NAMES}

    def ping(self) -> bool:
        return bool(self._client.ping())


def get_redis_stream_service() -> RedisStreamService:
    return RedisStreamService()
