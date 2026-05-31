from datetime import UTC, datetime
from uuid import UUID

from app.db.models.scrape_job import ScrapeJob
from app.db.models.source import Source
from app.db.session import SessionLocal
from app.services.redis_stream_service import get_redis_stream_service
from app.services.scraper_service import ScraperService
from app.workers.celery_app import celery_app
from app.workers.parse_worker import parse_raw_record_task


@celery_app.task(name="scrape_source_task", bind=True, max_retries=3)
def scrape_source_task(self, job_id: str) -> dict:
    db = SessionLocal()
    streams = get_redis_stream_service()
    try:
        job_uuid = UUID(job_id)
        scraper = ScraperService(db)
        raw = scraper.run_job(job_uuid)
        if raw:
            parse_raw_record_task.delay(str(raw.id))
            return {"raw_record_id": str(raw.id), "status": "completed"}
        return {"status": "no_record"}
    except Exception as exc:
        db.rollback()
        job = db.get(ScrapeJob, UUID(job_id))
        if job:
            job.retry_count += 1
            if job.retry_count < 3:
                job.status = "retrying"
                db.commit()
                streams.publish(
                    "scrape_jobs",
                    {"job_id": job_id, "status": "retrying", "error": str(exc)},
                )
                raise self.retry(exc=exc, countdown=30 * job.retry_count) from exc
            job.status = "failed"
            job.error_message = str(exc)
            db.commit()
        raise
    finally:
        db.close()


@celery_app.task(name="app.workers.scrape_worker.run_scheduled_sources")
def run_scheduled_sources() -> int:
    db = SessionLocal()
    streams = get_redis_stream_service()
    count = 0
    try:
        sources = db.query(Source).filter(Source.is_active.is_(True)).all()
        for source in sources:
            job = ScrapeJob(source_id=source.id, status="pending")
            db.add(job)
            db.commit()
            db.refresh(job)
            streams.publish(
                "scrape_jobs",
                {"job_id": str(job.id), "source_id": str(source.id), "status": "pending"},
            )
            scrape_source_task.delay(str(job.id))
            count += 1
        return count
    finally:
        db.close()


def create_and_enqueue_job(source_id: UUID) -> ScrapeJob:
    db = SessionLocal()
    streams = get_redis_stream_service()
    try:
        job = ScrapeJob(source_id=source_id, status="pending", created_at=datetime.now(UTC))
        db.add(job)
        db.commit()
        db.refresh(job)
        streams.publish(
            "scrape_jobs",
            {"job_id": str(job.id), "source_id": str(source_id), "status": "pending"},
        )
        scrape_source_task.delay(str(job.id))
        return job
    finally:
        db.close()
