# SentinelX Backend (Jay)

Ingestion pipeline: scraping → Redis streams → parsing → Qwen/SGLang agents → PostgreSQL + Qdrant.

## Quick start

```bash
cp .env.example .env
docker compose -f ../docker-compose.yml up -d postgres redis qdrant
docker compose -f ../docker-compose.yml up -d api celery_worker celery_beat
```

API: http://localhost:4000/docs

## Services (host ports, 4000–4999)

| Service | Host port | Notes |
|---------|-----------|--------|
| API | 4000 | `uvicorn` listens on 4000 in container |
| PostgreSQL | 4543 | maps to 5432 in container |
| Redis | 4637 | maps to 6379 in container |
| Qdrant | 4633 | maps to 6333 in container |
| SGLang | 4300 | maps to 30000 in container |

## Celery tasks

- `scrape_source_task` — scrape via Bright Data (or direct HTTP fallback)
- `parse_raw_record_task` — parse HTML to structured records
- `process_parsed_record_task` — run all intelligence agents

## Migrations

```bash
alembic upgrade head
```

See `docs/sentinelx_task_jay.md` for the full specification.
