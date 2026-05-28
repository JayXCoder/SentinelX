from uuid import UUID

from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.db.session import SessionLocal
from app.services.parser_service import ParserService
from app.services.redis_stream_service import get_redis_stream_service
from app.workers.ai_worker import process_parsed_record_task
from app.workers.celery_app import celery_app


@celery_app.task(name="parse_raw_record_task", bind=True, max_retries=3)
def parse_raw_record_task(self, raw_record_id: str) -> dict:
    db = SessionLocal()
    streams = get_redis_stream_service()
    parser = ParserService()
    try:
        raw = db.get(RawRecord, UUID(raw_record_id))
        if not raw:
            raise ValueError(f"Raw record not found: {raw_record_id}")

        parsed_data = parser.parse(html=raw.raw_html, text=raw.raw_text, url=raw.url)
        existing = (
            db.query(ParsedRecord)
            .filter(ParsedRecord.raw_record_id == raw.id)
            .first()
        )
        if existing:
            parsed = existing
        else:
            parsed = ParsedRecord(raw_record_id=raw.id, **parsed_data)
            db.add(parsed)
        db.commit()
        db.refresh(parsed)

        streams.publish(
            "parsed_records",
            {"parsed_record_id": str(parsed.id), "raw_record_id": str(raw.id)},
        )
        process_parsed_record_task.delay(str(parsed.id))
        return {"parsed_record_id": str(parsed.id)}
    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=20)
    finally:
        db.close()
