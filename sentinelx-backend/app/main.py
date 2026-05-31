import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import agents, health, monitoring, notes, records, scrape_jobs, sources, workspace, ws
from app.core.config import get_settings
from app.core.cors import configure_cors
from app.core.middleware import ObservabilityMiddleware
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.services.embedding_service import EmbeddingService
from app.services.realtime_listener import run_realtime_listener
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

    stop_event = asyncio.Event()
    listener_task = asyncio.create_task(run_realtime_listener(stop_event))
    yield
    stop_event.set()
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    configure_cors(app, settings.cors_origins)
    app.add_middleware(ObservabilityMiddleware)

    app.include_router(health.router)
    app.include_router(sources.router)
    app.include_router(scrape_jobs.router)
    app.include_router(records.router)
    app.include_router(agents.router)
    app.include_router(monitoring.router)
    app.include_router(workspace.router)
    app.include_router(notes.router)
    app.include_router(ws.router)
    return app


app = create_app()
