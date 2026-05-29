# Backend documentation

**Owner:** Jay · **Package:** `sentinelx-backend`

## Documentation requirement

Every change to this service must update documentation here. Incomplete docs block merge for production features.

Document:

- **Architecture** — new modules, workers, external services
- **API** — every route, status code, query/body schema
- **Workflows** — Celery tasks, Redis streams, retries (Mermaid)
- **Data model** — SQLAlchemy models and migrations

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | Layering, agents, infrastructure |
| [api-reference.md](api-reference.md) | REST API catalog |
| [workflow.md](workflow.md) | Ingestion and agent pipelines |
| [data-model.md](data-model.md) | PostgreSQL entities and relationships |

Platform context: [../../docs/platform-architecture.md](../../docs/platform-architecture.md) · Task spec: [../../docs/sentinelx_task_jay.md](../../docs/sentinelx_task_jay.md)

Interactive API: http://localhost:4000/docs (OpenAPI).
