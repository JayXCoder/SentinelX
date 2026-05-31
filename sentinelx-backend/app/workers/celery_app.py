from app.core.config import get_settings
from celery import Celery
from celery.schedules import crontab

settings = get_settings()

celery_app = Celery(
    "sentinelx",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.workers.scrape_worker",
        "app.workers.parse_worker",
        "app.workers.ai_worker",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.conf.beat_schedule = {
    "run-scheduled-sources": {
        "task": "app.workers.scrape_worker.run_scheduled_sources",
        "schedule": crontab(minute="*/15"),
    },
}
