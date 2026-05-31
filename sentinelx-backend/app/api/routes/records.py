from uuid import UUID

from app.core.pagination import DEFAULT_PAGE_LIMIT, LimitQuery
from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.db.session import get_db
from app.schemas.record import ParsedRecordRead, RawRecordRead
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/records", tags=["records"])


@router.get("/raw", response_model=list[RawRecordRead])
def list_raw_records(
    db: Session = Depends(get_db),
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
) -> list[RawRecord]:
    return db.query(RawRecord).order_by(RawRecord.fetched_at.desc()).limit(limit).all()


@router.get("/raw/{record_id}", response_model=RawRecordRead)
def get_raw_record(record_id: UUID, db: Session = Depends(get_db)) -> RawRecord:
    record = db.get(RawRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Raw record not found")
    return record


@router.get("/parsed", response_model=list[ParsedRecordRead])
def list_parsed_records(
    db: Session = Depends(get_db),
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
) -> list[ParsedRecord]:
    return (
        db.query(ParsedRecord)
        .order_by(ParsedRecord.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/parsed/{record_id}", response_model=ParsedRecordRead)
def get_parsed_record(record_id: UUID, db: Session = Depends(get_db)) -> ParsedRecord:
    record = db.get(ParsedRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Parsed record not found")
    return record
