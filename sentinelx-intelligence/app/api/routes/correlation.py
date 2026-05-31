import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.pagination import DEFAULT_PAGE_LIMIT, LimitQuery, SkipQuery
from app.core.security import verify_api_key
from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.entity import Entity
from app.db.session import get_db
from app.schemas.correlation import CorrelatedEventOut, CorrelationRunRequest, CorrelationRunResult
from app.services.correlation_service import CorrelationService

router = APIRouter(prefix="/correlation", tags=["correlation"])


@router.post("/run", response_model=CorrelationRunResult)
def run_correlation(
    request: CorrelationRunRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> CorrelationRunResult:
    svc = CorrelationService()
    events = svc.run_all(db, time_window_hours=request.time_window_hours)
    return CorrelationRunResult(
        events_created=len(events),
        signal_ids_processed=[],
        event_ids=[str(e.id) for e in events],
    )


@router.post("/run/{signal_id}", response_model=CorrelationRunResult)
def run_correlation_for_signal(
    signal_id: str,
    request: CorrelationRunRequest,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> CorrelationRunResult:
    svc = CorrelationService()
    events = svc.run_for_signal(db, signal_id, time_window_hours=request.time_window_hours)
    return CorrelationRunResult(
        events_created=len(events),
        signal_ids_processed=[signal_id],
        event_ids=[str(e.id) for e in events],
    )


@router.get("/events", response_model=list[CorrelatedEventOut])
def list_events(
    skip: SkipQuery = 0,
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
    event_type: str | None = None,
    db: Session = Depends(get_db),
) -> list[CorrelatedEvent]:
    q = db.query(CorrelatedEvent)
    if event_type:
        q = q.filter(CorrelatedEvent.event_type == event_type)
    return q.order_by(CorrelatedEvent.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/events/{event_id}", response_model=CorrelatedEventOut)
def get_event(event_id: uuid.UUID, db: Session = Depends(get_db)) -> CorrelatedEvent:
    event = db.query(CorrelatedEvent).filter(CorrelatedEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Correlated event not found")
    return event


@router.get("/entities/{entity_id}/events", response_model=list[CorrelatedEventOut])
def events_for_entity(
    entity_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[CorrelatedEvent]:
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return (
        db.query(CorrelatedEvent)
        .filter(CorrelatedEvent.involved_entities.contains([{"name": entity.name}]))
        .order_by(CorrelatedEvent.created_at.desc())
        .all()
    )
