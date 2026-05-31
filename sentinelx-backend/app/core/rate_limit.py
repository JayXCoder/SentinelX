import time
from collections.abc import Callable

import redis
from fastapi import HTTPException, Request, status

from app.core.config import get_settings

EXPENSIVE_PATH_PREFIXES = (
    "/rag/ask",
    "/rag/reindex",
    "/graph/rebuild",
    "/risk-scores/recalculate",
    "/correlation/run",
    "/scrape-jobs",
    "/agents/process",
)


def _client_key(request: Request) -> str:
    api_key = request.headers.get("x-api-key")
    if api_key:
        return f"apikey:{api_key[:16]}"
    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


def check_rate_limit(request: Request) -> None:
    path = request.url.path
    if not any(path.startswith(prefix) for prefix in EXPENSIVE_PATH_PREFIXES):
        return

    settings = get_settings()
    limit = settings.rate_limit_per_minute
    if limit <= 0:
        return

    window = 60
    now = int(time.time())
    bucket = now // window
    key = f"ratelimit:{_client_key(request)}:{path}:{bucket}"

    try:
        client = redis.from_url(settings.redis_url, decode_responses=True)
        count = client.incr(key)
        if count == 1:
            client.expire(key, window + 1)
        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )
    except redis.RedisError:
        return


def rate_limit_dependency() -> Callable:
    def _dependency(request: Request) -> None:
        check_rate_limit(request)

    return _dependency
