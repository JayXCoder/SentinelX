import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.models.entity import Entity
from app.db.models.rag_memory import RAGMemory
from app.services.qdrant_service import QdrantService
from app.services.sglang_service import SGLangService

logger = get_logger(__name__)

RAG_SYSTEM_PROMPT = """You are an enterprise intelligence analyst for SentinelX.
Your task is to answer questions based ONLY on the provided intelligence context.
Your answers must be:
- Evidence-based and grounded in the provided context
- Structured and parseable as JSON
- Confidence-scored (0.0 to 1.0)
- Not hallucinated — if the context doesn't support an answer, say so

Respond with JSON matching this structure:
{
  "answer": "string",
  "confidence": float,
  "supporting_evidence": ["string"],
  "related_entities": ["string"],
  "related_events": ["string"],
  "recommended_action": "string"
}"""


class RAGService:
    def __init__(self) -> None:
        self._qdrant = QdrantService()
        self._sglang = SGLangService()

    def store_memory(
        self,
        db: Session,
        text_chunk: str,
        memory_type: str,
        collection: str,
        metadata: dict[str, Any],
        signal_id: uuid.UUID | None = None,
        event_id: uuid.UUID | None = None,
        entity_id: uuid.UUID | None = None,
    ) -> RAGMemory:
        vector_id = str(uuid.uuid4())
        qdrant_payload = {
            "memory_type": memory_type,
            "signal_id": str(signal_id) if signal_id else None,
            "event_id": str(event_id) if event_id else None,
            "entity_id": str(entity_id) if entity_id else None,
            **metadata,
        }
        self._qdrant.upsert(collection, vector_id, text_chunk, qdrant_payload)

        mem = RAGMemory(
            id=uuid.uuid4(),
            qdrant_vector_id=vector_id,
            source_signal_id=signal_id,
            correlated_event_id=event_id,
            entity_id=entity_id,
            memory_type=memory_type,
            text_chunk=text_chunk,
            metadata=metadata,
        )
        db.add(mem)
        db.flush()
        logger.info("RAG memory stored", extra={"type": memory_type, "collection": collection})
        return mem

    def query(
        self,
        text: str,
        collection: str = "signals_memory",
        top_k: int = 5,
        score_threshold: float = 0.5,
    ) -> list[dict[str, Any]]:
        return self._qdrant.search(collection, text, top_k=top_k, score_threshold=score_threshold)

    def ask(
        self,
        db: Session,
        question: str,
        entity_id: uuid.UUID | None = None,
        top_k: int = 5,
    ) -> dict[str, Any]:
        filter_payload: dict[str, Any] | None = None
        if entity_id:
            filter_payload = {"entity_id": str(entity_id)}

        # Search across all relevant collections
        context_chunks: list[str] = []
        for collection in ["signals_memory", "correlated_events_memory", "risk_explanations_memory"]:
            results = self._qdrant.search(
                collection,
                question,
                top_k=top_k,
                score_threshold=0.4,
                filter_payload=filter_payload,
            )
            for r in results:
                payload = r.get("payload", {})
                text = payload.get("text_chunk") or payload.get("summary") or str(payload)
                if text:
                    context_chunks.append(text)

        if not context_chunks:
            return {
                "answer": "No relevant intelligence context found for this question.",
                "confidence": 0.0,
                "supporting_evidence": [],
                "related_entities": [],
                "related_events": [],
                "recommended_action": "Ingest more intelligence signals related to this topic.",
            }

        entity_context = ""
        if entity_id:
            entity = db.query(Entity).filter(Entity.id == entity_id).first()
            if entity:
                entity_context = f"\nFocused on entity: {entity.name} ({entity.entity_type})"

        context_text = "\n\n".join(context_chunks[:10])
        user_prompt = (
            f"Question: {question}{entity_context}\n\n"
            f"Intelligence Context:\n{context_text}\n\n"
            f"Answer the question using ONLY the provided context."
        )

        try:
            result = self._sglang.complete_json(RAG_SYSTEM_PROMPT, user_prompt)
            logger.info("RAG answer generated", extra={"question_len": len(question)})
            return result
        except Exception as exc:
            logger.error("RAG SGLang call failed", extra={"error": str(exc)})
            return {
                "answer": f"Intelligence context retrieved but AI generation failed: {exc}",
                "confidence": 0.3,
                "supporting_evidence": context_chunks[:3],
                "related_entities": [],
                "related_events": [],
                "recommended_action": "Check SGLang service availability.",
            }

    def reindex_entity(
        self,
        db: Session,
        entity_id: uuid.UUID,
    ) -> int:
        memories = db.query(RAGMemory).filter(RAGMemory.entity_id == entity_id).all()
        reindexed = 0
        for mem in memories:
            try:
                collection_map = {
                    "signal_summary": "signals_memory",
                    "evidence_chunk": "signals_memory",
                    "executive_summary": "executive_memory",
                    "correlated_event": "correlated_events_memory",
                    "risk_explanation": "risk_explanations_memory",
                }
                collection = collection_map.get(mem.memory_type, "signals_memory")
                self._qdrant.upsert(
                    collection,
                    mem.qdrant_vector_id,
                    mem.text_chunk,
                    mem.mem_metadata or {},
                )
                reindexed += 1
            except Exception as exc:
                logger.error("Reindex failed for memory", extra={"id": str(mem.id), "error": str(exc)})
        return reindexed
