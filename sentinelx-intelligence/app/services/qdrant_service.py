from typing import Any
from uuid import UUID

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

COLLECTIONS = [
    "signals_memory",
    "correlated_events_memory",
    "risk_explanations_memory",
    "entity_memory",
    "executive_memory",
]


class QdrantService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._qdrant = QdrantClient(
            url=self.settings.qdrant_url,
            api_key=self.settings.qdrant_api_key,
        )
        self._embedder = TextEmbedding(model_name=self.settings.embedding_model)
        self._vector_size = self.settings.embedding_vector_size
        self._collections_ready = False

    def ensure_collections(self) -> None:
        if self._collections_ready:
            return
        for name in COLLECTIONS:
            try:
                if not self._qdrant.collection_exists(name):
                    self._qdrant.create_collection(
                        collection_name=name,
                        vectors_config=qmodels.VectorParams(
                            size=self._vector_size,
                            distance=qmodels.Distance.COSINE,
                        ),
                    )
                    logger.info("Created Qdrant collection", extra={"collection": name})
            except Exception as exc:
                logger.warning(
                    "Qdrant collection ensure skipped",
                    extra={"collection": name, "error": str(exc)},
                )
        self._collections_ready = True

    def embed_text(self, text: str) -> list[float]:
        vectors = list(self._embedder.embed([text[:8000]]))
        return vectors[0].tolist()

    def upsert(
        self,
        collection: str,
        point_id: str | UUID,
        text: str,
        payload: dict[str, Any],
    ) -> None:
        if not self._collections_ready:
            self.ensure_collections()
        vector = self.embed_text(text)
        self._qdrant.upsert(
            collection_name=collection,
            points=[
                qmodels.PointStruct(
                    id=str(point_id),
                    vector=vector,
                    payload=payload,
                )
            ],
        )
        logger.info("Upserted vector", extra={"collection": collection, "id": str(point_id)})

    def search(
        self,
        collection: str,
        text: str,
        top_k: int = 5,
        score_threshold: float = 0.5,
        filter_payload: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if not self._collections_ready:
            self.ensure_collections()
        vector = self.embed_text(text)
        try:
            return self._search_vectors(
                collection, vector, top_k, score_threshold, filter_payload
            )
        except Exception as exc:
            logger.warning(
                "Qdrant search failed",
                extra={"collection": collection, "error": str(exc)},
            )
            return []

    def _search_vectors(
        self,
        collection: str,
        vector: list[float],
        top_k: int,
        score_threshold: float,
        filter_payload: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        query_filter = None
        if filter_payload:
            conditions = [
                qmodels.FieldCondition(
                    key=k,
                    match=qmodels.MatchValue(value=v),
                )
                for k, v in filter_payload.items()
            ]
            query_filter = qmodels.Filter(must=conditions)

        if hasattr(self._qdrant, "search"):
            results = self._qdrant.search(
                collection_name=collection,
                query_vector=vector,
                limit=top_k,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True,
            )
        else:
            response = self._qdrant.query_points(
                collection_name=collection,
                query=vector,
                limit=top_k,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True,
            )
            results = response.points

        return [
            {
                "id": str(r.id),
                "score": r.score,
                "payload": r.payload,
            }
            for r in results
        ]


    def health_check(self) -> dict[str, Any]:
        try:
            collections = self._qdrant.get_collections()
            return {
                "status": "ok",
                "collections": [c.name for c in collections.collections],
            }
        except Exception as exc:
            return {"status": "unavailable", "error": str(exc)}
