from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.models.source import Source
from app.db.session import get_db
from app.schemas.source import SourceCreate, SourceRead, SourceUpdate

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourceRead, status_code=status.HTTP_201_CREATED)
def create_source(
    payload: SourceCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> Source:
    source = Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("", response_model=list[SourceRead])
def list_sources(
    db: Session = Depends(get_db),
    active_only: bool = False,
) -> list[Source]:
    query = db.query(Source)
    if active_only:
        query = query.filter(Source.is_active.is_(True))
    return query.order_by(Source.created_at.desc()).all()


@router.get("/{source_id}", response_model=SourceRead)
def get_source(source_id: UUID, db: Session = Depends(get_db)) -> Source:
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.patch("/{source_id}", response_model=SourceRead)
def update_source(
    source_id: UUID,
    payload: SourceUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> Source:
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(source, key, value)
    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> None:
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
