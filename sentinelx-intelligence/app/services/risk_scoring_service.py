import uuid
from datetime import UTC
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.entity import Entity
from app.db.models.intelligence_signal import IntelSignal
from app.db.models.risk_score import RiskScore
from app.rules.scoring_rules import build_explanation, score_and_level
from app.schemas.risk_score import ScoreType

logger = get_logger(__name__)

ALL_SCORE_TYPES = [e.value for e in ScoreType]

SIGNAL_TYPE_TO_SCORE_TYPES: dict[str, list[str]] = {
    "cyber": ["cyber_exposure"],
    "vendor_risk": ["vendor_risk", "reputation_risk"],
    "gtm": ["gtm_opportunity", "market_threat"],
    "financial": ["financial_risk", "market_threat"],
    "osint": ["reputation_risk", "cyber_exposure"],
    "executive_summary": ["cyber_exposure", "vendor_risk", "gtm_opportunity"],
}


def _signal_entity_names(sig: IntelSignal) -> list[str]:
    names: list[str] = []
    for ent in sig.entities or []:
        if isinstance(ent, dict):
            name = (ent.get("name") or ent.get("text") or "").strip()
            if name:
                names.append(name)
        elif isinstance(ent, str) and ent.strip():
            names.append(ent.strip())
    return names


def _signals_for_entity(db: Session, entity: Entity) -> list[IntelSignal]:
    matched: list[IntelSignal] = []
    for sig in db.query(IntelSignal).all():
        if entity.name in _signal_entity_names(sig):
            matched.append(sig)
    return matched


def _signal_to_dict(sig: IntelSignal) -> dict[str, Any]:
    ts = sig.timestamp or sig.created_at
    if ts and ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    return {
        "severity": sig.severity,
        "confidence": sig.confidence,
        "source_reliability": sig.source_reliability,
        "timestamp": ts,
        "entity_importance": 0.5,
    }


class RiskScoringService:
    def recalculate_all(self, db: Session) -> list[RiskScore]:
        entities = db.query(Entity).all()
        created: list[RiskScore] = []
        for entity in entities:
            created.extend(self._score_entity(db, entity))
        if created:
            db.commit()
        return created

    def recalculate_entity(self, db: Session, entity_id: uuid.UUID) -> list[RiskScore]:
        entity = db.query(Entity).filter(Entity.id == entity_id).first()
        if not entity:
            logger.warning("Entity not found for scoring", extra={"entity_id": str(entity_id)})
            return []
        scores = self._score_entity(db, entity)
        if scores:
            db.commit()
        return scores

    def recalculate_for_event(
        self,
        db: Session,
        event: CorrelatedEvent,
    ) -> list[RiskScore]:
        signal_ids = [str(s) for s in (event.signal_ids or [])]
        signals = db.query(IntelSignal).filter(IntelSignal.id.in_(signal_ids)).all()
        if not signals:
            return []

        entity_names: set[str] = set()
        for sig in signals:
            for ent in (sig.entities or []):
                if isinstance(ent, dict):
                    name = (ent.get("name") or ent.get("text") or "").strip()
                    if name:
                        entity_names.add(name)
                elif isinstance(ent, str) and ent.strip():
                    entity_names.add(ent.strip())

        created: list[RiskScore] = []
        for name in entity_names:
            entity = db.query(Entity).filter(Entity.name.ilike(name)).first()
            if entity:
                scores = self._score_entity(db, entity, event=event)
                created.extend(scores)

        if created:
            db.commit()
        return created

    def _score_entity(
        self,
        db: Session,
        entity: Entity,
        event: CorrelatedEvent | None = None,
    ) -> list[RiskScore]:
        signals = _signals_for_entity(db, entity)

        if not signals:
            return []

        score_type_signals: dict[str, list[dict]] = {st: [] for st in ALL_SCORE_TYPES}
        for sig in signals:
            sig_dict = _signal_to_dict(sig)
            for score_type in SIGNAL_TYPE_TO_SCORE_TYPES.get(sig.signal_type, []):
                score_type_signals[score_type].append(sig_dict)

        created: list[RiskScore] = []
        for score_type, sig_dicts in score_type_signals.items():
            if not sig_dicts:
                continue
            score_value, risk_level = score_and_level(sig_dicts, score_type)
            explanation = build_explanation(score_value, risk_level, score_type, sig_dicts)

            rs = RiskScore(
                id=uuid.uuid4(),
                entity_id=entity.id,
                entity_name=entity.name,
                score_type=score_type,
                score_value=score_value,
                risk_level=risk_level,
                explanation=explanation,
                evidence_signal_ids=[str(s.id) for s in signals],
                correlated_event_id=event.id if event else None,
            )
            db.add(rs)
            created.append(rs)
            logger.info(
                "Risk score calculated",
                extra={
                    "entity": entity.name,
                    "score_type": score_type,
                    "score": score_value,
                    "level": risk_level,
                },
            )

        return created
