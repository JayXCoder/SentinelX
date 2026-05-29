# Backend architecture

FastAPI application with Celery workers for async ingestion and Qwen/SGLang-powered intelligence agents.

## Layer diagram

```mermaid
flowchart TB
  subgraph api [API layer app/api/routes]
    health
    sources
    scrape_jobs
    records
    agents
    monitoring
  end

  subgraph services [Services app/services]
    scraper[ScraperService]
    parser[ParserService]
    agentsvc[AgentProcessingService]
    redis[RedisStreamService]
    sglang[SGLangService]
    embed[EmbeddingService]
    bright[BrightDataService]
  end

  subgraph workers [Celery app/workers]
    scrape_w[scrape_worker]
    parse_w[parse_worker]
    ai_w[ai_worker]
  end

  subgraph agents [Agents app/agents]
    cyber[cyber_agent]
    gtm[gtm_agent]
    vendor[vendor_risk_agent]
    fin[financial_agent]
    osint[osint_agent]
    exec[executive_summary_agent]
  end

  subgraph stores [Stores]
    PG[(PostgreSQL)]
    RD[(Redis)]
    QD[(Qdrant)]
    SG[SGLang HTTP]
  end

  api --> services
  workers --> services
  services --> agents
  agents --> sglang
  services --> PG
  services --> RD
  services --> QD
  sglang --> SG
```

## Directory layout

| Path | Responsibility |
|------|----------------|
| `app/main.py` | FastAPI app factory, router registration |
| `app/api/routes/` | HTTP handlers |
| `app/schemas/` | Pydantic request/response models |
| `app/db/models/` | SQLAlchemy ORM |
| `app/services/` | Business logic |
| `app/agents/` | LLM agent implementations |
| `app/workers/` | Celery tasks and beat schedule |
| `app/core/` | Config, logging, security |
| `alembic/` | Database migrations |

## Agent pipeline

Default agents (see `app/agents/__init__.py` → `DEFAULT_AGENTS`) run per parsed record:

```mermaid
flowchart LR
  PR[parsed_record] --> AP[AgentProcessingService]
  AP --> A1[cyber]
  AP --> A2[gtm]
  AP --> A3[vendor_risk]
  AP --> A4[financial]
  AP --> A5[osint]
  AP --> A6[executive_summary]
  A1 & A2 & A3 & A4 & A5 & A6 --> SIG[intelligence_signals]
```

## External dependencies

| Dependency | Env var | Usage |
|------------|---------|--------|
| PostgreSQL | `DATABASE_URL` | Sources, jobs, records, signals |
| Redis | `REDIS_URL`, `CELERY_*` | Broker, streams, cache |
| Qdrant | `QDRANT_URL` | Vector storage for RAG prep |
| SGLang | `SGLANG_BASE_URL`, `SGLANG_MODEL` | Qwen inference |
| Bright Data | `BRIGHT_DATA_*` | Managed scraping (optional) |

## Health surface

Aggregated dependency checks under `/health/*` — see [api-reference.md](api-reference.md).
