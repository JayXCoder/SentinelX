import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.entity import Entity
from app.db.models.relationship import EntityRelationship
from app.db.session import get_db
from app.schemas.graph import EntityOut, EntityRelationshipOut, EntityWithRelationships, GraphTimelineOut
from app.services.knowledge_graph_service import KnowledgeGraphService

router = APIRouter(prefix="/graph", tags=["knowledge-graph"])


@router.get("/entities", response_model=list[EntityOut])
def list_entities(
    skip: int = 0,
    limit: int = 50,
    entity_type: str | None = None,
    db: Session = Depends(get_db),
) -> list[Entity]:
    q = db.query(Entity)
    if entity_type:
        q = q.filter(Entity.entity_type == entity_type)
    return q.order_by(Entity.last_seen.desc()).offset(skip).limit(limit).all()


@router.get("/entities/{entity_id}", response_model=EntityOut)
def get_entity(entity_id: uuid.UUID, db: Session = Depends(get_db)) -> Entity:
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


@router.get("/entities/{entity_id}/relationships", response_model=EntityWithRelationships)
def entity_with_relationships(
    entity_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> EntityWithRelationships:
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    outgoing = (
        db.query(EntityRelationship)
        .filter(EntityRelationship.source_entity_id == entity_id)
        .all()
    )
    incoming = (
        db.query(EntityRelationship)
        .filter(EntityRelationship.target_entity_id == entity_id)
        .all()
    )

    return EntityWithRelationships(
        entity=EntityOut.model_validate(entity),
        outgoing=[EntityRelationshipOut.model_validate(r) for r in outgoing],
        incoming=[EntityRelationshipOut.model_validate(r) for r in incoming],
    )


@router.get("/relationships", response_model=list[EntityRelationshipOut])
def list_relationships(
    skip: int = 0,
    limit: int = 50,
    relationship_type: str | None = None,
    db: Session = Depends(get_db),
) -> list[EntityRelationship]:
    q = db.query(EntityRelationship)
    if relationship_type:
        q = q.filter(EntityRelationship.relationship_type == relationship_type)
    return q.order_by(EntityRelationship.last_seen.desc()).offset(skip).limit(limit).all()


@router.get("/timeline/{entity_id}", response_model=GraphTimelineOut)
def entity_timeline(entity_id: uuid.UUID, db: Session = Depends(get_db)) -> GraphTimelineOut:
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    svc = KnowledgeGraphService()
    raw_timeline = svc.get_timeline(db, entity_id)

    from app.schemas.graph import GraphTimelineEntry
    from datetime import datetime

    entries = []
    for item in raw_timeline:
        entries.append(
            GraphTimelineEntry(
                timestamp=datetime.fromisoformat(item["timestamp"]),
                event_type=item["event_type"],
                title=item["title"],
                summary=item["summary"],
                severity=item["severity"],
                confidence=item["confidence"],
            )
        )

    return GraphTimelineOut(
        entity_id=entity_id,
        entity_name=entity.name,
        timeline=entries,
    )


@router.post("/rebuild")
def rebuild_graph(db: Session = Depends(get_db)) -> dict:
    svc = KnowledgeGraphService()
    result = svc.rebuild(db)
    return {"status": "ok", **result}
