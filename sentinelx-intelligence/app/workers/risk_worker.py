import uuid

from app.core.logging import get_logger
from app.db.models.correlated_event import CorrelatedEvent
from app.db.session import SessionLocal
from app.services.redis_stream_service import RedisStreamService
from app.services.risk_scoring_service import RiskScoringService
from app.workers.celery_app import celery_app

logger = get_logger(__name__)


@celery_app.task(name="app.workers.risk_worker.calculate_risk_score_task", bind=True, max_retries=3)
def calculate_risk_score_task(self, event_id: str) -> dict:
    db = SessionLocal()
    redis_svc = RedisStreamService()

    try:
        event = db.query(CorrelatedEvent).filter(
            CorrelatedEvent.id == uuid.UUID(event_id)
        ).first()

        if not event:
            logger.warning("Correlated event not found", extra={"event_id": event_id})
            return {"event_id": event_id, "scores_created": 0}

        svc = RiskScoringService()
        scores = svc.recalculate_for_event(db, event)

        for score in scores:
            redis_svc.publish("risk_scores", {
                "score_id": str(score.id),
                "entity_id": str(score.entity_id),
                "entity_name": score.entity_name,
                "score_type": score.score_type,
                "score_value": score.score_value,
                "risk_level": score.risk_level,
            })

            if score.risk_level in ("high", "critical"):
                redis_svc.publish("executive_alerts", {
                    "alert_type": "risk_score",
                    "entity_name": score.entity_name,
                    "score_type": score.score_type,
                    "score_value": score.score_value,
                    "risk_level": score.risk_level,
                    "explanation": score.explanation,
                })

        logger.info(
            "Risk scoring complete",
            extra={"event_id": event_id, "scores": len(scores)},
        )
        return {"event_id": event_id, "scores_created": len(scores)}

    except Exception as exc:
        db.rollback()
        logger.error("Risk scoring task failed", extra={"event_id": event_id, "error": str(exc)})
        raise self.retry(exc=exc, countdown=30)
    finally:
        db.close()
