import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.rag_memory import RAGMemory
from app.db.session import get_db
from app.schemas.rag import RAGAskRequest, RAGMemoryOut, RAGQueryRequest, RAGResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/query")
def rag_query(request: RAGQueryRequest, db: Session = Depends(get_db)) -> list[dict]:
    svc = RAGService()
    results = svc.query(
        text=request.text,
        collection=request.collection,
        top_k=request.top_k,
        score_threshold=request.score_threshold,
    )
    return results


@router.post("/ask", response_model=RAGResponse)
def rag_ask(request: RAGAskRequest, db: Session = Depends(get_db)) -> RAGResponse:
    svc = RAGService()
    result = svc.ask(
        db=db,
        question=request.question,
        entity_id=request.entity_id,
        top_k=request.top_k,
    )
    return RAGResponse(
        answer=result.get("answer", ""),
        confidence=float(result.get("confidence", 0.0)),
        supporting_evidence=result.get("supporting_evidence", []),
        related_entities=result.get("related_entities", []),
        related_events=result.get("related_events", []),
        recommended_action=result.get("recommended_action", ""),
    )


@router.get("/memory/{entity_id}", response_model=list[RAGMemoryOut])
def memory_for_entity(
    entity_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[RAGMemory]:
    return (
        db.query(RAGMemory)
        .filter(RAGMemory.entity_id == entity_id)
        .order_by(RAGMemory.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/reindex")
def reindex(entity_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
    from app.db.models.entity import Entity

    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    svc = RAGService()
    count = svc.reindex_entity(db, entity_id)
    return {"status": "ok", "reindexed": count, "entity_id": str(entity_id)}
