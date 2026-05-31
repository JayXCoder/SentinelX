from uuid import UUID

from app.core.pagination import DEFAULT_PAGE_LIMIT, LimitQuery
from app.core.security import verify_api_key
from app.db.models.scrape_job import ScrapeJob
from app.db.models.source import Source
from app.db.session import get_db
from app.schemas.scrape_job import ScrapeJobCreate, ScrapeJobRead
from app.workers.scrape_worker import create_and_enqueue_job, scrape_source_task
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/scrape-jobs", tags=["scrape-jobs"])


@router.post("", response_model=ScrapeJobRead, status_code=status.HTTP_201_CREATED)
def create_scrape_job(
    payload: ScrapeJobCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> ScrapeJob:
    source = db.get(Source, payload.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    job = create_and_enqueue_job(payload.source_id)
    return job


@router.get("", response_model=list[ScrapeJobRead])
def list_scrape_jobs(
    db: Session = Depends(get_db),
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
    status_filter: str | None = None,
) -> list[ScrapeJob]:
    query = db.query(ScrapeJob)
    if status_filter:
        query = query.filter(ScrapeJob.status == status_filter)
    return query.order_by(ScrapeJob.created_at.desc()).limit(limit).all()


@router.get("/{job_id}", response_model=ScrapeJobRead)
def get_scrape_job(job_id: UUID, db: Session = Depends(get_db)) -> ScrapeJob:
    job = db.get(ScrapeJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scrape job not found")
    return job


@router.post("/{job_id}/retry", response_model=ScrapeJobRead)
def retry_scrape_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> ScrapeJob:
    job = db.get(ScrapeJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scrape job not found")
    job.status = "pending"
    job.error_message = None
    job.retry_count += 1
    db.commit()
    scrape_source_task.delay(str(job.id))
    return job


@router.post("/run-source/{source_id}", response_model=ScrapeJobRead)
def run_source(
    source_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> ScrapeJob:
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return create_and_enqueue_job(source_id)
