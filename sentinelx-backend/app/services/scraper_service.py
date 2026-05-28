import hashlib
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.raw_record import RawRecord
from app.db.models.scrape_job import ScrapeJob
from app.db.models.source import Source
from app.services.bright_data_service import BrightDataService
from app.services.redis_stream_service import get_redis_stream_service


class ScraperService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.bright_data = BrightDataService()
        self.streams = get_redis_stream_service()

    def run_job(self, job_id: UUID) -> RawRecord | None:
        job = self.db.get(ScrapeJob, job_id)
        if not job:
            raise ValueError(f"Scrape job not found: {job_id}")

        source = self.db.get(Source, job.source_id)
        if not source:
            raise ValueError(f"Source not found: {job.source_id}")

        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        self.db.commit()

        try:
            render_js = source.scraping_strategy in ("browser", "js", "playwright")
            result = self.bright_data.fetch(source.base_url, render_js=render_js)
            html = result["html"]
            content_hash = hashlib.sha256(html.encode()).hexdigest()

            raw = RawRecord(
                source_id=source.id,
                scrape_job_id=job.id,
                url=result["url"],
                raw_html=html,
                raw_text=None,
                content_hash=content_hash,
                record_metadata={
                    "status_code": result["status_code"],
                    "via_proxy": result["via_proxy"],
                },
            )
            self.db.add(raw)
            job.records_collected += 1
            job.status = "completed"
            job.finished_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(raw)

            self.streams.publish(
                "raw_records",
                {
                    "raw_record_id": str(raw.id),
                    "source_id": str(source.id),
                    "scrape_job_id": str(job.id),
                },
            )
            return raw
        except Exception as exc:
            job.status = "failed"
            job.error_message = str(exc)
            job.finished_at = datetime.now(timezone.utc)
            self.db.commit()
            raise
