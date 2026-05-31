from uuid import UUID

from app.core.security import verify_api_key
from app.db.models.human_note import HumanNote
from app.db.session import get_db
from app.schemas.workspace import HumanNoteCreate, HumanNoteRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[HumanNoteRead])
def list_notes(
    target_type: str,
    target_id: str,
    db: Session = Depends(get_db),
) -> list[HumanNote]:
    return (
        db.query(HumanNote)
        .filter(
            HumanNote.target_type == target_type,
            HumanNote.target_id == target_id,
        )
        .order_by(HumanNote.created_at.desc())
        .all()
    )


@router.post("", response_model=HumanNoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: HumanNoteCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> HumanNote:
    note = HumanNote(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> None:
    note = db.get(HumanNote, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
