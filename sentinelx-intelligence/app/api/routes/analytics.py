from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.entity import Entity
from app.db.models.intelligence_signal import IntelSignal
from app.db.models.risk_score import RiskScore
from app.db.session import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)) -> dict:
    total_signals = db.query(func.count(IntelSignal.id)).scalar() or 0
    total_events = db.query(func.count(CorrelatedEvent.id)).scalar() or 0
    total_entities = db.query(func.count(Entity.id)).scalar() or 0
    total_scores = db.query(func.count(RiskScore.id)).scalar() or 0

    critical_scores = (
        db.query(func.count(RiskScore.id))
        .filter(RiskScore.risk_level == "critical")
        .scalar() or 0
    )
    high_scores = (
        db.query(func.count(RiskScore.id))
        .filter(RiskScore.risk_level == "high")
        .scalar() or 0
    )

    return {
        "total_signals_ingested": total_signals,
        "total_correlated_events": total_events,
        "total_entities_tracked": total_entities,
        "total_risk_scores": total_scores,
        "critical_risks": critical_scores,
        "high_risks": high_scores,
    }


@router.get("/top-risks")
def top_risks(limit: int = 10, db: Session = Depends(get_db)) -> list[dict]:
    scores = (
        db.query(RiskScore)
        .filter(RiskScore.risk_level.in_(["critical", "high"]))
        .order_by(RiskScore.score_value.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "entity_id": str(s.entity_id),
            "entity_name": s.entity_name,
            "score_type": s.score_type,
            "score_value": s.score_value,
            "risk_level": s.risk_level,
            "explanation": s.explanation,
            "calculated_at": s.calculated_at.isoformat(),
        }
        for s in scores
    ]


@router.get("/top-opportunities")
def top_opportunities(limit: int = 10, db: Session = Depends(get_db)) -> list[dict]:
    scores = (
        db.query(RiskScore)
        .filter(RiskScore.score_type == "gtm_opportunity")
        .order_by(RiskScore.score_value.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "entity_id": str(s.entity_id),
            "entity_name": s.entity_name,
            "score_value": s.score_value,
            "risk_level": s.risk_level,
            "explanation": s.explanation,
            "calculated_at": s.calculated_at.isoformat(),
        }
        for s in scores
    ]


@router.get("/vendor-risk-summary")
def vendor_risk_summary(db: Session = Depends(get_db)) -> dict:
    scores = (
        db.query(RiskScore)
        .filter(RiskScore.score_type == "vendor_risk")
        .order_by(RiskScore.score_value.desc())
        .limit(50)
        .all()
    )
    by_level: dict[str, list[str]] = {"critical": [], "high": [], "medium": [], "low": []}
    for s in scores:
        level = s.risk_level
        if level in by_level:
            by_level[level].append(s.entity_name)
    return {
        "total_vendors_assessed": len(scores),
        "by_risk_level": by_level,
        "avg_score": round(sum(s.score_value for s in scores) / max(len(scores), 1), 2),
    }


@router.get("/cyber-risk-summary")
def cyber_risk_summary(db: Session = Depends(get_db)) -> dict:
    scores = (
        db.query(RiskScore)
        .filter(RiskScore.score_type == "cyber_exposure")
        .order_by(RiskScore.score_value.desc())
        .limit(50)
        .all()
    )
    cyber_signals = (
        db.query(func.count(IntelSignal.id))
        .filter(IntelSignal.signal_type == "cyber")
        .scalar() or 0
    )
    cyber_events = (
        db.query(func.count(CorrelatedEvent.id))
        .filter(CorrelatedEvent.event_type == "cyber_incident")
        .scalar() or 0
    )
    return {
        "total_cyber_signals": cyber_signals,
        "total_cyber_incidents": cyber_events,
        "entities_with_cyber_exposure": len(scores),
        "critical_exposure": sum(1 for s in scores if s.risk_level == "critical"),
        "avg_exposure_score": round(
            sum(s.score_value for s in scores) / max(len(scores), 1), 2
        ),
    }


@router.get("/market-movement-summary")
def market_movement_summary(db: Session = Depends(get_db)) -> dict:
    market_events = (
        db.query(CorrelatedEvent)
        .filter(
            CorrelatedEvent.event_type.in_(["competitor_movement", "market_opportunity"])
        )
        .order_by(CorrelatedEvent.created_at.desc())
        .limit(20)
        .all()
    )
    threat_scores = (
        db.query(RiskScore)
        .filter(RiskScore.score_type == "market_threat")
        .order_by(RiskScore.score_value.desc())
        .limit(10)
        .all()
    )
    return {
        "recent_market_events": len(market_events),
        "competitor_movements": sum(
            1 for e in market_events if e.event_type == "competitor_movement"
        ),
        "market_opportunities": sum(
            1 for e in market_events if e.event_type == "market_opportunity"
        ),
        "top_market_threats": [
            {"entity": s.entity_name, "score": s.score_value, "level": s.risk_level}
            for s in threat_scores
        ],
    }
