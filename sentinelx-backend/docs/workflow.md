# Backend workflows

## Celery task chain

```mermaid
stateDiagram-v2
  [*] --> Scheduled: beat every 15m
  [*] --> Manual: POST scrape-jobs

  Scheduled --> scrape_source_task
  Manual --> scrape_source_task

  scrape_source_task --> raw_record: success
  scrape_source_task --> failed: max retries

  raw_record --> parse_raw_record_task
  parse_raw_record_task --> parsed_record
  parsed_record --> process_parsed_record_task
  process_parsed_record_task --> intelligence_signals
  intelligence_signals --> [*]
```

## Task reference

| Celery task | Module | Trigger |
|-------------|--------|---------|
| `scrape_source_task` | `scrape_worker` | Job created, beat schedule |
| `parse_raw_record_task` | `parse_worker` | After raw record saved |
| `process_parsed_record_task` | `ai_worker` | After parse completes |
| `run_scheduled_sources` | `scrape_worker` | Celery beat crontab `*/15` |

## Scrape retry workflow

```mermaid
sequenceDiagram
  participant Task as scrape_source_task
  participant DB as PostgreSQL
  participant RS as Redis stream scrape_jobs

  Task->>Task: exception
  Task->>DB: retry_count += 1
  alt retry_count < 3
    Task->>DB: status=retrying
    Task->>RS: publish retry event
    Task->>Task: Celery retry countdown
  else max retries
    Task->>DB: status=failed, error_message
  end
```

## Redis streams (monitoring)

Operational events are published for observability. Inspect via `GET /monitoring/streams`.

```mermaid
flowchart LR
  scrape[scrape_worker] -->|publish| SJ[stream: scrape_jobs]
  parse[parse_worker] -->|publish| PJ[stream: parse_jobs]
  ai[ai_worker] -->|publish| AJ[stream: agent_jobs]
```

## Agent processing (sync vs async)

```mermaid
flowchart TD
  REQ[POST /agents/process/id] --> MODE{async_mode?}
  MODE -->|false| SYNC[AgentProcessingService.process_record]
  MODE -->|true| QUEUE[process_parsed_record_task.delay]
  SYNC --> OUT[signals in response]
  QUEUE --> OUT2[status queued]
```

## Database migration workflow

```bash
cd sentinelx-backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

CI runs `alembic upgrade head` before pytest.

## Local run workflow

```mermaid
flowchart TD
  A[cp .env.example .env] --> B[docker compose up postgres redis qdrant]
  B --> C[alembic upgrade head]
  C --> D[uvicorn or compose api service]
  D --> E[compose celery_worker + celery_beat]
  E --> F[POST /sources + scrape jobs]
  F --> G[GET /agents/signals]
```
