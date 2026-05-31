from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.core.metrics import metrics_response
from app.db.session import get_db
from app.services.qdrant_service import QdrantService
from app.services.redis_stream_service import get_redis_stream_service
from app.services.sglang_service import SGLangService

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "sentinelx-intelligence"}


@router.get("/metrics")
def metrics() -> Response:
    return metrics_response()


@router.get("/health/redis")
def health_redis() -> dict:
    svc = get_redis_stream_service()
    ok = svc.ping()
    return {"status": "ok" if ok else "unavailable", "redis": ok}


@router.get("/health/postgres")
def health_postgres(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "postgres": True}
    except Exception:
        return {"status": "unavailable", "postgres": False}


@router.get("/health/qdrant")
def health_qdrant() -> dict:
    return QdrantService().health_check()


@router.get("/health/sglang")
def health_sglang() -> dict:
    return SGLangService().health_check()
