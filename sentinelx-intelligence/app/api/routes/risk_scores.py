import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.pagination import DEFAULT_PAGE_LIMIT, LimitQuery, SkipQuery
from app.core.security import verify_api_key
from app.db.models.entity import Entity
from app.db.models.risk_score import RiskScore
from app.db.session import get_db
from app.schemas.risk_score import RecalculateRequest, RecalculateResult, RiskScoreOut
from app.services.risk_scoring_service import RiskScoringService

router = APIRouter(prefix="/risk-scores", tags=["risk-scores"])


@router.post("/recalculate", response_model=RecalculateResult)
def recalculate_all(
    request: RecalculateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> RecalculateResult:
    svc = RiskScoringService()
    scores = svc.recalculate_all(db)
    entity_ids = list({str(s.entity_id) for s in scores})
    return RecalculateResult(scores_created=len(scores), entity_ids=entity_ids)


@router.post("/recalculate/{entity_id}", response_model=RecalculateResult)
def recalculate_entity(
    entity_id: uuid.UUID,
    request: RecalculateRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> RecalculateResult:
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    svc = RiskScoringService()
    scores = svc.recalculate_entity(db, entity_id)
    return RecalculateResult(scores_created=len(scores), entity_ids=[str(entity_id)])


@router.get("", response_model=list[RiskScoreOut])
def list_scores(
    skip: SkipQuery = 0,
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
    risk_level: str | None = None,
    db: Session = Depends(get_db),
) -> list[RiskScore]:
    q = db.query(RiskScore)
    if risk_level:
        q = q.filter(RiskScore.risk_level == risk_level)
    return q.order_by(RiskScore.calculated_at.desc()).offset(skip).limit(limit).all()


@router.get("/{score_id}", response_model=RiskScoreOut)
def get_score(score_id: uuid.UUID, db: Session = Depends(get_db)) -> RiskScore:
    score = db.query(RiskScore).filter(RiskScore.id == score_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Risk score not found")
    return score


@router.get("/entity/{entity_id}", response_model=list[RiskScoreOut])
def scores_for_entity(
    entity_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[RiskScore]:
    return (
        db.query(RiskScore)
        .filter(RiskScore.entity_id == entity_id)
        .order_by(RiskScore.calculated_at.desc())
        .all()
    )


@router.get("/type/{score_type}", response_model=list[RiskScoreOut])
def scores_by_type(
    score_type: str,
    skip: SkipQuery = 0,
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
    db: Session = Depends(get_db),
) -> list[RiskScore]:
    return (
        db.query(RiskScore)
        .filter(RiskScore.score_type == score_type)
        .order_by(RiskScore.score_value.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
