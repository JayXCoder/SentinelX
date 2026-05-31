from app.db.models.intelligence_signal import IntelligenceSignal
from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.db.models.scrape_job import ScrapeJob
from app.db.session import get_db
from app.services.redis_stream_service import get_redis_stream_service
from app.workers.celery_app import celery_app
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/streams")
def monitoring_streams() -> dict:
    streams = get_redis_stream_service()
    return {"streams": streams.all_streams_info(), "backlog": streams.backlog_size()}


@router.get("/workers")
def monitoring_workers() -> dict:
    inspect = celery_app.control.inspect()
    return {
        "active": inspect.active() if inspect else {},
        "stats": inspect.stats() if inspect else {},
        "registered": inspect.registered() if inspect else {},
    }


@router.get("/jobs")
def monitoring_jobs(db: Session = Depends(get_db)) -> dict:
    total = db.query(func.count(ScrapeJob.id)).scalar() or 0
    completed = (
        db.query(func.count(ScrapeJob.id))
        .filter(ScrapeJob.status == "completed")
        .scalar()
        or 0
    )
    failed = (
        db.query(func.count(ScrapeJob.id))
        .filter(ScrapeJob.status == "failed")
        .scalar()
        or 0
    )
    return {
        "scrape_jobs": {"total": total, "completed": completed, "failed": failed},
        "raw_records": db.query(func.count(RawRecord.id)).scalar() or 0,
        "parsed_records": db.query(func.count(ParsedRecord.id)).scalar() or 0,
        "signals_generated": db.query(func.count(IntelligenceSignal.id)).scalar() or 0,
    }


@router.get("/errors")
def monitoring_errors(db: Session = Depends(get_db), limit: int = 20) -> dict:
    failed_jobs = (
        db.query(ScrapeJob)
        .filter(ScrapeJob.status == "failed")
        .order_by(ScrapeJob.finished_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "failed_jobs": [
            {
                "id": str(j.id),
                "source_id": str(j.source_id),
                "error_message": j.error_message,
                "retry_count": j.retry_count,
            }
            for j in failed_jobs
        ]
    }
