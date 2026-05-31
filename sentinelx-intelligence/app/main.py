from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import analytics, correlation, health, knowledge_graph, rag, risk_scores
from app.core.config import get_settings
from app.core.cors import configure_cors
from app.core.logging import get_logger, setup_logging
from app.core.middleware import ObservabilityMiddleware
from app.db.base import Base
from app.db.session import engine
from app.services.qdrant_service import QdrantService
from app.services.redis_stream_service import get_redis_stream_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    logger = get_logger(__name__)

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")

    try:
        get_redis_stream_service().ensure_streams()
        logger.info("Redis streams ensured")
    except Exception as exc:
        logger.warning("Redis stream init skipped: %s", exc)

    try:
        QdrantService().ensure_collections()
        logger.info("Qdrant collections ensured")
    except Exception as exc:
        logger.warning("Qdrant collection init skipped: %s", exc)

    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

    configure_cors(app, settings.cors_origins)
    app.add_middleware(ObservabilityMiddleware)

    app.include_router(health.router)
    app.include_router(correlation.router)
    app.include_router(risk_scores.router)
    app.include_router(knowledge_graph.router)
    app.include_router(rag.router)
    app.include_router(analytics.router)

    return app


app = create_app()
