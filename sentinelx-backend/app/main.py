from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import agents, health, monitoring, records, scrape_jobs, sources
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.services.embedding_service import EmbeddingService
from app.services.redis_stream_service import get_redis_stream_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.core.logging import get_logger

    setup_logging()
    logger = get_logger(__name__)
    Base.metadata.create_all(bind=engine)
    try:
        get_redis_stream_service().ensure_streams()
    except Exception as exc:
        logger.warning("Redis stream init skipped: %s", exc)
    try:
        EmbeddingService().ensure_collections()
    except Exception as exc:
        logger.warning("Qdrant collection init skipped: %s", exc)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    origins = [o.strip() for o in settings.cors_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(sources.router)
    app.include_router(scrape_jobs.router)
    app.include_router(records.router)
    app.include_router(agents.router)
    app.include_router(monitoring.router)
    return app


app = create_app()
