# SentinelX Intelligence Layer (Kai Zhe)

Correlation engine, risk scoring, knowledge graph, and RAG memory.

## What this service does

Consumes intelligence signals from Jay's backend (via Redis streams), correlates related signals into higher-level events, calculates explainable risk scores, stores entities and relationships in a knowledge graph, and answers questions via RAG (Qdrant + Qwen).

## Documentation (required)

**Every module and endpoint must be documented** before merge.

| Doc | Contents |
|-----|----------|
| [docs/README.md](docs/README.md) | Index and standards |
| [docs/architecture.md](docs/architecture.md) | Target system design (Mermaid) |
| [docs/api-reference.md](docs/api-reference.md) | REST catalog (mark ✅ when live) |
| [docs/workflow.md](docs/workflow.md) | Correlation, scoring, RAG flows |
| [docs/integration.md](docs/integration.md) | Contract with Jay's signal export |

Task spec: [../docs/sentinelx_task_kai_zhe.md](../docs/sentinelx_task_kai_zhe.md)

**Rule:** Implement API → update `docs/api-reference.md` + flip status from ☐ to ✅.

## Port

- API: `4001` (host port when run via root `docker compose`)

## Service Stack

- FastAPI — REST API
- Celery — Correlation, scoring, and graph workers
- Redis — Stream consumption (Jay's signals) and output publishing
- PostgreSQL — Persistent storage (6 tables, `intel_alembic_version` version table)
- Qdrant — Vector embeddings for RAG (5 collections)
- Qwen via SGLang — AI-powered RAG answers and explanation generation

## Database Tables

| Table | Purpose |
|-------|---------|
| `intel_signals` | Received intelligence signals from Jay |
| `correlated_events` | Grouped multi-signal intelligence events |
| `risk_scores` | Calculated risk/opportunity scores per entity |
| `entities` | Discovered entities (company, vendor, threat, etc.) |
| `entity_relationships` | Knowledge graph edges between entities |
| `rag_memory` | RAG memory references linked to Qdrant vectors |

## Qdrant Collections

- `signals_memory`
- `correlated_events_memory`
- `risk_explanations_memory`
- `entity_memory`
- `executive_memory`

## Redis Streams

**Consumes from Jay:**
- `cyber_signals`, `gtm_signals`, `financial_signals`, `vendor_risk_signals`, `osint_signals`, `executive_summaries`

**Publishes:**
- `correlated_events`, `risk_scores`, `graph_updates`, `rag_memory_updates`, `executive_alerts`

## Running locally (Docker)

```bash
# Start core dependencies
docker compose up postgres redis qdrant -d

# Start intelligence API + workers
docker compose --profile intelligence up -d --build
```

## API Endpoints

| Group | Endpoints |
|-------|----------|
| Health | `GET /health`, `/health/redis`, `/health/postgres`, `/health/qdrant`, `/health/sglang` |
| Correlation | `POST /correlation/run`, `POST /correlation/run/{signal_id}`, `GET /correlation/events`, `GET /correlation/events/{event_id}`, `GET /correlation/entities/{entity_id}/events` |
| Risk Scores | `POST /risk-scores/recalculate`, `POST /risk-scores/recalculate/{entity_id}`, `GET /risk-scores`, `GET /risk-scores/{score_id}`, `GET /risk-scores/entity/{entity_id}`, `GET /risk-scores/type/{score_type}` |
| Graph | `GET /graph/entities`, `GET /graph/entities/{entity_id}`, `GET /graph/entities/{entity_id}/relationships`, `GET /graph/relationships`, `GET /graph/timeline/{entity_id}`, `POST /graph/rebuild` |
| RAG | `POST /rag/query`, `POST /rag/ask`, `GET /rag/memory/{entity_id}`, `POST /rag/reindex` |
| Analytics | `GET /analytics/overview`, `/top-risks`, `/top-opportunities`, `/vendor-risk-summary`, `/cyber-risk-summary`, `/market-movement-summary` |

## Celery Workers

```bash
# Worker
celery -A app.workers.celery_app.celery_app worker --loglevel=info

# Beat scheduler (runs correlation every 5 min)
celery -A app.workers.celery_app.celery_app beat --loglevel=info
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg2://sentinelx:sentinelx@postgres:5432/sentinelx` | PostgreSQL connection |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Celery broker |
| `CELERY_RESULT_BACKEND` | `redis://redis:6379/1` | Celery results |
| `QDRANT_URL` | `http://qdrant:6333` | Qdrant vector DB |
| `SGLANG_BASE_URL` | `http://sglang_qwen:30000` | SGLang/Qwen endpoint |
| `SGLANG_MODEL` | `Qwen/Qwen3.5-2B` | Model name |

See root [`.env.example`](../.env.example) for the full list (stream settings, correlation windows, consumer group, etc.).

## Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

Note: Uses `intel_alembic_version` as the version table (shared DB with Jay's backend).
