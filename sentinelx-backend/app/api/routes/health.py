from app.core.metrics import metrics_response
from app.db.session import get_db
from app.services.bright_data_service import BrightDataService
from app.services.embedding_service import EmbeddingService
from app.services.redis_stream_service import get_redis_stream_service
from app.services.sglang_service import SGLangService
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import Response

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "sentinelx-backend"}


@router.get("/metrics")
def metrics() -> Response:
    return metrics_response()


@router.get("/health/redis")
def health_redis() -> dict:
    streams = get_redis_stream_service()
    ok = streams.ping()
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
    return EmbeddingService().health_check()


@router.get("/health/sglang")
def health_sglang() -> dict:
    return SGLangService().health_check()


@router.get("/health/bright-data")
def health_bright_data() -> dict:
    return BrightDataService().health_check()
