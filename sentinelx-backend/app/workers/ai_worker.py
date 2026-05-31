from uuid import UUID

from app.db.session import SessionLocal
from app.services.agent_processing_service import AgentProcessingService
from app.workers.celery_app import celery_app


@celery_app.task(name="process_parsed_record_task", bind=True, max_retries=2)
def process_parsed_record_task(
    self,
    parsed_record_id: str,
    agents: list[str] | None = None,
) -> dict:
    db = SessionLocal()
    try:
        service = AgentProcessingService(db)
        signals = service.process_record(UUID(parsed_record_id), agents=agents)
        return {
            "parsed_record_id": parsed_record_id,
            "signals": [str(s.id) for s in signals],
            "count": len(signals),
        }
    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=45) from exc
    finally:
        db.close()
