from app.core.security import verify_api_key
from app.db.session import get_db
from app.schemas.workspace import WorkspaceProfileRead, WorkspaceProfileUpdate
from app.services.workspace_service import WorkspaceService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("/profile", response_model=WorkspaceProfileRead)
def get_profile(db: Session = Depends(get_db)) -> WorkspaceProfileRead:
    profile = WorkspaceService.get_or_create_default(db)
    return profile


@router.patch("/profile", response_model=WorkspaceProfileRead)
def update_profile(
    payload: WorkspaceProfileUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
) -> WorkspaceProfileRead:
    return WorkspaceService.update(db, payload)


@router.get("/context")
def get_rag_context(db: Session = Depends(get_db)) -> dict:
    profile = WorkspaceService.get_or_create_default(db)
    return {
        "company_name": profile.company_name,
        "context": WorkspaceService.context_for_rag(profile),
    }
