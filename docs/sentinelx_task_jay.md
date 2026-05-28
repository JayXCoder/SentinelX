# SentinelX — task.md for Jay

## Owner

**Jay**

## Assigned Scope

Jay is responsible for the backend intelligence ingestion and AI processing pipeline.

Jay owns the following architecture section:

```text
Web Data Sources
    ↓
Bright Data Infrastructure
    ↓
Distributed Scraping + Collection
    ↓
Redis Streaming Pipeline
    ↓
AI Processing Layer
    ├── Cyber Intelligence Agents
    ├── GTM Intelligence Agents
    ├── Financial Intelligence Agents
    ├── Vendor Risk Agents
    ├── OSINT Agents
    └── Executive Summary Agents
```

---

# 1. Main Objective

Build the complete backend pipeline that collects public web intelligence, streams it through Redis, processes it with AI agents, and outputs structured intelligence signals for Kai Zhe’s correlation and scoring layer.

The goal is to make Jay’s part work as a production-style data and AI ingestion system.

It must be able to:

- collect data from public web sources
- use Bright Data infrastructure for reliable scraping
- distribute scraping jobs using Celery
- stream collected records through Redis
- process records using Qwen through SGLang
- generate structured intelligence events
- store processed signals in PostgreSQL
- store embeddings in Qdrant
- expose FastAPI endpoints for monitoring and control

---

# 2. Technology Stack

Jay’s assigned stack:

- FastAPI
- Celery
- Redis
- PostgreSQL
- Qdrant
- Qwen
- SGLang
- Bright Data
- Docker

---

# 3. Service Responsibilities

Jay needs to build these backend service areas:

## 3.1 Scraper Service

Responsible for:

- managing scraping jobs
- creating source configurations
- triggering scraping workers
- tracking scraping status
- storing raw data records

## 3.2 Parser Service

Responsible for:

- cleaning raw scraped content
- extracting useful text
- extracting metadata
- extracting entities
- normalizing content

## 3.3 Redis Streaming Pipeline

Responsible for:

- moving records between stages
- decoupling scraper workers from AI workers
- handling asynchronous event flow
- supporting real-time processing

## 3.4 AI Processing Layer

Responsible for:

- running intelligence agents
- classifying signals
- extracting insights
- summarizing content
- creating structured intelligence outputs

## 3.5 Persistence Layer

Responsible for:

- saving raw sources
- saving parsed records
- saving processed signals
- saving embeddings
- saving agent outputs

---

# 4. Suggested Folder Structure

```text
sentinelx-backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── sources.py
│   │   │   ├── scrape_jobs.py
│   │   │   ├── records.py
│   │   │   ├── agents.py
│   │   │   └── monitoring.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── models/
│   │       ├── source.py
│   │       ├── scrape_job.py
│   │       ├── raw_record.py
│   │       ├── parsed_record.py
│   │       └── intelligence_signal.py
│   ├── schemas/
│   │   ├── source.py
│   │   ├── scrape_job.py
│   │   ├── record.py
│   │   └── signal.py
│   ├── services/
│   │   ├── bright_data_service.py
│   │   ├── scraper_service.py
│   │   ├── parser_service.py
│   │   ├── redis_stream_service.py
│   │   ├── sglang_service.py
│   │   └── embedding_service.py
│   ├── workers/
│   │   ├── celery_app.py
│   │   ├── scrape_worker.py
│   │   ├── parse_worker.py
│   │   └── ai_worker.py
│   └── agents/
│       ├── cyber_agent.py
│       ├── gtm_agent.py
│       ├── financial_agent.py
│       ├── vendor_risk_agent.py
│       ├── osint_agent.py
│       └── executive_summary_agent.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic/
└── README.md
```

---

# 5. Database Tables

## 5.1 sources

Stores target websites and data source definitions.

Required fields:

- id
- name
- source_type
- base_url
- category
- scraping_strategy
- frequency_minutes
- is_active
- created_at
- updated_at

Example source types:

- company_website
- news
- social
- github
- cve
- job_board
- review_site
- forum

---

## 5.2 scrape_jobs

Tracks scraping jobs.

Required fields:

- id
- source_id
- status
- started_at
- finished_at
- error_message
- records_collected
- retry_count
- created_at

Job statuses:

- pending
- running
- completed
- failed
- retrying

---

## 5.3 raw_records

Stores raw scraped data.

Required fields:

- id
- source_id
- scrape_job_id
- url
- raw_html
- raw_text
- content_hash
- fetched_at
- metadata

---

## 5.4 parsed_records

Stores cleaned and normalized data.

Required fields:

- id
- raw_record_id
- title
- clean_text
- detected_entities
- detected_language
- published_at
- parsed_metadata
- created_at

---

## 5.5 intelligence_signals

Stores AI-generated intelligence outputs.

Required fields:

- id
- parsed_record_id
- signal_type
- category
- title
- summary
- entities
- severity
- confidence
- source_reliability
- evidence
- created_at

Signal types:

- cyber
- gtm
- financial
- vendor_risk
- osint
- executive_summary

---

# 6. Redis Stream Design

Jay must define and implement the Redis streams used by the ingestion and AI pipeline.

## Required Streams

```text
scrape_jobs
raw_records
parsed_records
cyber_signals
gtm_signals
financial_signals
vendor_risk_signals
osint_signals
executive_summaries
```

## Stream Flow

```text
scrape_jobs
    ↓
scrape_worker
    ↓
raw_records
    ↓
parse_worker
    ↓
parsed_records
    ↓
ai_worker
    ↓
intelligence signal streams
```

---

# 7. FastAPI Endpoints

## 7.1 Health Endpoints

```text
GET /health
GET /health/redis
GET /health/postgres
GET /health/qdrant
GET /health/sglang
```

---

## 7.2 Source Management

```text
POST /sources
GET /sources
GET /sources/{source_id}
PATCH /sources/{source_id}
DELETE /sources/{source_id}
```

---

## 7.3 Scraping Jobs

```text
POST /scrape-jobs
GET /scrape-jobs
GET /scrape-jobs/{job_id}
POST /scrape-jobs/{job_id}/retry
POST /scrape-jobs/run-source/{source_id}
```

---

## 7.4 Records

```text
GET /records/raw
GET /records/raw/{record_id}
GET /records/parsed
GET /records/parsed/{record_id}
```

---

## 7.5 Agent Processing

```text
POST /agents/process/{parsed_record_id}
POST /agents/process-batch
GET /agents/status
GET /agents/signals
GET /agents/signals/{signal_id}
```

---

## 7.6 Monitoring

```text
GET /monitoring/streams
GET /monitoring/workers
GET /monitoring/jobs
GET /monitoring/errors
```

---

# 8. Celery Worker Tasks

## 8.1 Scrape Worker

Task name:

```text
scrape_source_task
```

Responsibilities:

- receive source id
- fetch source configuration
- scrape target data through Bright Data
- handle retries
- store raw record
- publish raw record event to Redis

---

## 8.2 Parse Worker

Task name:

```text
parse_raw_record_task
```

Responsibilities:

- consume raw record
- clean HTML
- extract text
- extract title
- extract timestamps
- detect language
- extract entities
- save parsed record
- publish parsed record event

---

## 8.3 AI Worker

Task name:

```text
process_parsed_record_task
```

Responsibilities:

- consume parsed record
- route record to correct AI agent
- call Qwen through SGLang
- generate intelligence signal
- save signal into PostgreSQL
- publish signal into Redis stream
- generate embedding
- store embedding in Qdrant

---

# 9. Bright Data Integration

## Goals

Bright Data should be used to make scraping reliable and scalable.

## Required Features

- proxy-based scraping
- support for JavaScript rendered pages
- anti-bot resilience
- retry handling
- geo-based scraping support
- rate limit control

## Implementation Tasks

- create BrightDataService
- configure proxy authentication
- create scraping request wrapper
- implement retry logic
- log request status
- store failed requests
- expose Bright Data health check

---

# 10. AI Agent Requirements

Each AI agent must follow a consistent input and output format.

## Agent Input Format

```json
{
  "record_id": "string",
  "source_type": "string",
  "title": "string",
  "clean_text": "string",
  "entities": [],
  "metadata": {}
}
```

## Agent Output Format

```json
{
  "signal_type": "cyber | gtm | financial | vendor_risk | osint | executive_summary",
  "category": "string",
  "title": "string",
  "summary": "string",
  "entities": [],
  "severity": 0,
  "confidence": 0.0,
  "source_reliability": 0.0,
  "evidence": [],
  "recommended_action": "string"
}
```

---

# 11. Cyber Intelligence Agent

## Purpose

Detect cybersecurity-related signals.

## Detects

- leaked credentials
- exposed API keys
- CVEs
- phishing campaigns
- malware indicators
- ransomware activity
- breach mentions
- exploit releases

## Output

Publishes to:

```text
cyber_signals
```

---

# 12. GTM Intelligence Agent

## Purpose

Detect sales, market and competitor signals.

## Detects

- competitor pricing changes
- feature launches
- product announcements
- customer complaints
- buying intent
- hiring trends
- technology adoption

## Output

Publishes to:

```text
gtm_signals
```

---

# 13. Financial Intelligence Agent

## Purpose

Detect financial and business movement signals.

## Detects

- funding rounds
- acquisitions
- layoffs
- bankruptcy indicators
- executive changes
- expansion plans
- revenue signals

## Output

Publishes to:

```text
financial_signals
```

---

# 14. Vendor Risk Agent

## Purpose

Detect vendor-related risk signals.

## Detects

- vendor breaches
- vendor downtime
- legal issues
- compliance problems
- SSL changes
- infrastructure instability
- negative sentiment

## Output

Publishes to:

```text
vendor_risk_signals
```

---

# 15. OSINT Agent

## Purpose

Analyze open-source intelligence signals.

## Detects

- public discussions
- social media trends
- suspicious activity
- community sentiment
- geopolitical signals
- underground forum mentions

## Output

Publishes to:

```text
osint_signals
```

---

# 16. Executive Summary Agent

## Purpose

Generate business-readable summaries.

## Generates

- executive summaries
- short intelligence briefs
- strategic implications
- recommended next actions

## Output

Publishes to:

```text
executive_summaries
```

---

# 17. Qwen + SGLang Integration

## Tasks

- run Qwen model through SGLang
- create SGLangService wrapper
- support prompt templates
- support structured JSON output
- validate AI outputs
- retry failed model responses
- log AI latency
- log token usage if available

## Prompt Template Requirements

Each prompt must ask the model to return valid JSON.

The output must be:

- structured
- consistent
- parseable
- evidence-based
- confidence-scored

---

# 18. Qdrant Embedding Storage

## Tasks

- generate embeddings for parsed records
- generate embeddings for intelligence signals
- create Qdrant collections
- store metadata with each vector
- expose utility function for vector insertion

## Suggested Collections

```text
parsed_records_embeddings
intelligence_signals_embeddings
cyber_embeddings
gtm_embeddings
vendor_risk_embeddings
financial_embeddings
osint_embeddings
```

---

# 19. Docker Requirements

Jay’s services must run under Docker.

## Required Containers

```text
api
celery_worker
celery_beat
redis
postgres
qdrant
sglang_qwen
```

## Docker Compose Must Support

- environment variables
- service dependencies
- volumes
- restart policies
- network isolation

---

# 20. Logging and Monitoring

## Required Logs

- scraping job logs
- Bright Data request logs
- Redis stream logs
- Celery task logs
- AI model request logs
- parsing error logs
- PostgreSQL persistence logs
- Qdrant insertion logs

## Required Metrics

- jobs completed
- jobs failed
- records scraped
- records parsed
- signals generated
- AI latency
- Redis backlog size
- worker status

---

# 21. Error Handling

## Must Handle

- scraping failures
- Bright Data proxy failure
- timeout errors
- invalid HTML
- parser failure
- Redis connection failure
- Celery task failure
- Qwen output parsing failure
- PostgreSQL failure
- Qdrant failure

## Failure Strategy

- retry when safe
- log error details
- mark job as failed
- preserve failed payload
- expose failure through monitoring API

---

# 22. Integration Contract With Kai Zhe

Jay must provide Kai Zhe with structured intelligence signals.

Each signal must include:

- signal id
- signal type
- category
- title
- summary
- affected entities
- source
- timestamp
- severity
- confidence
- evidence
- recommended action

Kai Zhe will consume these outputs for:

- correlation
- scoring
- knowledge graph updates
- RAG memory

---

# 23. Integration Contract With Frontend Team

Jay must expose backend APIs for Raymond and Geng Xin.

Frontend needs:

- source list
- scrape job status
- recent records
- generated signals
- AI processing status
- system health
- monitoring statistics

---

# 24. MVP Completion Checklist

## Scraping

- [ ] Source CRUD complete
- [ ] Scrape job creation complete
- [ ] Bright Data scraping complete
- [ ] Raw record storage complete
- [ ] Retry logic complete

## Parsing

- [ ] HTML parser complete
- [ ] Text cleaner complete
- [ ] Metadata extractor complete
- [ ] Parsed record storage complete

## Redis

- [ ] Redis streams created
- [ ] Producers implemented
- [ ] Consumers implemented
- [ ] Stream monitoring endpoint complete

## AI Agents

- [ ] Cyber Agent complete
- [ ] GTM Agent complete
- [ ] Financial Agent complete
- [ ] Vendor Risk Agent complete
- [ ] OSINT Agent complete
- [ ] Executive Summary Agent complete

## Storage

- [ ] PostgreSQL models complete
- [ ] PostgreSQL migrations complete
- [ ] Qdrant collections created
- [ ] Embedding storage complete

## API

- [ ] Health endpoints complete
- [ ] Source endpoints complete
- [ ] Job endpoints complete
- [ ] Record endpoints complete
- [ ] Agent endpoints complete
- [ ] Monitoring endpoints complete

## Docker

- [ ] Dockerfile complete
- [ ] docker-compose.yml complete
- [ ] Environment variables documented
- [ ] All services start successfully

---

# 25. Suggested Build Order

## Phase 1 — Foundation

- setup FastAPI
- setup PostgreSQL
- setup Redis
- setup Celery
- setup Docker Compose

## Phase 2 — Source and Scraper System

- create source model
- create scrape job model
- build Bright Data integration
- build scraping worker

## Phase 3 — Parsing Pipeline

- build parser worker
- clean raw content
- create parsed records
- publish to Redis stream

## Phase 4 — AI Agent Layer

- connect Qwen through SGLang
- build structured output prompts
- implement each intelligence agent
- save signals

## Phase 5 — Embeddings and Qdrant

- generate embeddings
- create Qdrant collections
- store vector records

## Phase 6 — Monitoring and Integration

- expose monitoring APIs
- prepare frontend API responses
- prepare Kai Zhe integration contract

---

# 26. Final Deliverable

Jay’s final deliverable is a working backend ingestion and AI intelligence pipeline that can:

1. register data sources
2. run scraping jobs through Bright Data
3. store raw records
4. parse records
5. process records with AI agents
6. generate structured intelligence signals
7. stream outputs through Redis
8. store structured data in PostgreSQL
9. store embeddings in Qdrant
10. provide API endpoints for the frontend and Kai Zhe’s correlation layer

This is the foundation layer of SentinelX.

