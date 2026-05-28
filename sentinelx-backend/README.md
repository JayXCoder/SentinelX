# SentinelX Backend (Jay)

Ingestion pipeline: scraping → Redis streams → parsing → Qwen/SGLang agents → PostgreSQL + Qdrant.

## Documentation (required)

Maintain **complete, up-to-date documentation** for every architectural change, API route, Celery task, and agent behavior.

| Doc | Contents |
|-----|----------|
| [docs/README.md](docs/README.md) | Index and documentation standards |
| [docs/architecture.md](docs/architecture.md) | Layers, agents, dependencies |
| [docs/api-reference.md](docs/api-reference.md) | All REST endpoints and schemas |
| [docs/workflow.md](docs/workflow.md) | Ingestion pipeline (Mermaid) |
| [docs/data-model.md](docs/data-model.md) | PostgreSQL ER diagram |

Full task spec: [../docs/sentinelx_task_jay.md](../docs/sentinelx_task_jay.md) · Platform flows: [../docs/platform-workflow.md](../docs/platform-workflow.md)

**Rule:** No new endpoint or worker without updating `docs/api-reference.md` and `docs/workflow.md`.

## Quick start

```bash
cp .env.example .env
docker compose -f ../docker-compose.yml up -d postgres redis qdrant api celery_worker celery_beat
```

API: http://localhost:4000/docs

## Services (host ports)

| Service | Port |
|---------|------|
| API | 4000 |
| PostgreSQL | 4543 |
| Redis | 4637 |
| Qdrant | 4633 |
| SGLang (`--profile ai`) | 4300 |

## Celery tasks

- `scrape_source_task` — Bright Data or HTTP fallback
- `parse_raw_record_task` — HTML → structured records
- `process_parsed_record_task` — intelligence agents

## Migrations

```bash
alembic upgrade head
```
