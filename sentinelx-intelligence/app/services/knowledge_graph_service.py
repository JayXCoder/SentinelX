import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.models.correlated_event import CorrelatedEvent
from app.db.models.entity import Entity
from app.db.models.intelligence_signal import IntelSignal
from app.db.models.relationship import EntityRelationship

logger = get_logger(__name__)

ENTITY_TYPE_KEYWORDS: dict[str, list[str]] = {
    "company": ["inc", "corp", "ltd", "llc", "company", "co."],
    "vendor": ["vendor", "supplier", "provider"],
    "technology": ["api", "sdk", "platform", "framework", "cloud", "saas"],
    "vulnerability": ["cve-", "vuln", "exploit", "zero-day"],
    "threat_actor": ["apt", "group", "ransomware", "gang"],
    "domain": [".com", ".org", ".net", ".io"],
    "ip_address": [".", ":", "::"],  # heuristic
}


def _infer_entity_type(name: str, ent_dict: dict[str, Any] | None) -> str:
    if ent_dict and ent_dict.get("type"):
        return ent_dict["type"]
    name_lower = name.lower()
    for etype, keywords in ENTITY_TYPE_KEYWORDS.items():
        if any(kw in name_lower for kw in keywords):
            return etype
    return "company"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class KnowledgeGraphService:
    def upsert_entity(
        self,
        db: Session,
        name: str,
        entity_type: str | None = None,
        ent_dict: dict[str, Any] | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Entity:
        name = name.strip()
        entity = db.query(Entity).filter(Entity.name.ilike(name)).first()
        now = _now_utc()

        if entity:
            entity.last_seen = now
            if description and not entity.description:
                entity.description = description
            if metadata:
                entity.entity_metadata = {**(entity.entity_metadata or {}), **metadata}
        else:
            inferred_type = entity_type or _infer_entity_type(name, ent_dict)
            aliases = []
            if ent_dict and ent_dict.get("aliases"):
                aliases = ent_dict["aliases"]
            entity = Entity(
                id=uuid.uuid4(),
                name=name,
                entity_type=inferred_type,
                aliases=aliases,
                description=description,
                entity_metadata=metadata or {},
                first_seen=now,
                last_seen=now,
            )
            db.add(entity)
            logger.info("Entity created", extra={"name": name, "type": inferred_type})

        db.flush()
        return entity

    def create_relationship(
        self,
        db: Session,
        source_entity_id: uuid.UUID,
        target_entity_id: uuid.UUID,
        relationship_type: str,
        confidence: float = 0.5,
        signal_ids: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EntityRelationship:
        existing = (
            db.query(EntityRelationship)
            .filter(
                EntityRelationship.source_entity_id == source_entity_id,
                EntityRelationship.target_entity_id == target_entity_id,
                EntityRelationship.relationship_type == relationship_type,
            )
            .first()
        )
        now = _now_utc()

        if existing:
            existing.last_seen = now
            existing.confidence = max(existing.confidence, confidence)
            if signal_ids:
                combined = list(set(existing.evidence_signal_ids or []) | set(signal_ids))
                existing.evidence_signal_ids = combined
            db.flush()
            return existing

        rel = EntityRelationship(
            id=uuid.uuid4(),
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            confidence=confidence,
            evidence_signal_ids=signal_ids or [],
            first_seen=now,
            last_seen=now,
            rel_metadata=metadata or {},
        )
        db.add(rel)
        db.flush()
        logger.info(
            "Relationship created",
            extra={
                "source": str(source_entity_id),
                "target": str(target_entity_id),
                "type": relationship_type,
            },
        )
        return rel

    def get_timeline(
        self,
        db: Session,
        entity_id: uuid.UUID,
    ) -> list[dict[str, Any]]:
        entity = db.query(Entity).filter(Entity.id == entity_id).first()
        if not entity:
            return []

        signals = (
            db.query(IntelSignal)
            .filter(IntelSignal.entities.contains([{"name": entity.name}]))
            .order_by(IntelSignal.timestamp)
            .all()
        )

        events = (
            db.query(CorrelatedEvent)
            .filter(CorrelatedEvent.involved_entities.contains([{"name": entity.name}]))
            .order_by(CorrelatedEvent.first_seen)
            .all()
        )

        timeline: list[dict[str, Any]] = []

        for sig in signals:
            ts = sig.timestamp or sig.created_at
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            timeline.append({
                "timestamp": ts.isoformat(),
                "event_type": sig.signal_type,
                "title": sig.title,
                "summary": sig.summary[:200],
                "severity": sig.severity,
                "confidence": sig.confidence,
            })

        for evt in events:
            ts = evt.first_seen or evt.created_at
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            timeline.append({
                "timestamp": ts.isoformat(),
                "event_type": evt.event_type,
                "title": evt.title,
                "summary": evt.summary[:200],
                "severity": evt.severity,
                "confidence": evt.confidence,
            })

        timeline.sort(key=lambda x: x["timestamp"])
        return timeline

    def rebuild(self, db: Session) -> dict[str, int]:
        signals = db.query(IntelSignal).all()
        entities_created = 0
        relationships_created = 0

        for sig in signals:
            sig_entities: list[Entity] = []
            for ent in (sig.entities or []):
                if isinstance(ent, dict):
                    name = (ent.get("name") or ent.get("text") or "").strip()
                elif isinstance(ent, str):
                    name = ent.strip()
                else:
                    continue
                if not name:
                    continue
                entity = self.upsert_entity(db, name, ent_dict=ent if isinstance(ent, dict) else None)
                sig_entities.append(entity)
                entities_created += 1

            for i, src in enumerate(sig_entities):
                for tgt in sig_entities[i + 1:]:
                    self.create_relationship(
                        db,
                        src.id,
                        tgt.id,
                        "mentioned_with",
                        confidence=sig.confidence,
                        signal_ids=[str(sig.id)],
                    )
                    relationships_created += 1

        db.commit()
        return {"entities_created": entities_created, "relationships_created": relationships_created}
