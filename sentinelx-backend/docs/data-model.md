# Backend data model

PostgreSQL schema managed by Alembic. Primary entities for the ingestion pipeline.

## ER diagram

```mermaid
erDiagram
  SOURCE ||--o{ SCRAPE_JOB : triggers
  SOURCE ||--o{ RAW_RECORD : produces
  SCRAPE_JOB ||--o| RAW_RECORD : creates
  RAW_RECORD ||--|| PARSED_RECORD : parses_to
  PARSED_RECORD ||--o{ INTELLIGENCE_SIGNAL : generates

  SOURCE {
    uuid id PK
    string name
    string url
    string source_type
    boolean is_active
    json schedule_config
  }

  SCRAPE_JOB {
    uuid id PK
    uuid source_id FK
    string status
    int retry_count
    text error_message
  }

  RAW_RECORD {
    uuid id PK
    uuid source_id FK
    uuid scrape_job_id FK
    text raw_content
    string content_type
  }

  PARSED_RECORD {
    uuid id PK
    uuid raw_record_id FK
    json structured_data
    string parser_version
  }

  INTELLIGENCE_SIGNAL {
    uuid id PK
    uuid parsed_record_id FK
    string signal_type
    string category
    string title
    text summary
    json entities
    int severity
    float confidence
  }
```

## Entity summary

| Model | Table | Purpose |
|-------|-------|---------|
| `Source` | `sources` | Crawl targets and schedule |
| `ScrapeJob` | `scrape_jobs` | Per-run scrape status |
| `RawRecord` | `raw_records` | Fetched HTML/payload |
| `ParsedRecord` | `parsed_records` | Structured extraction |
| `IntelligenceSignal` | `intelligence_signals` | Agent output for API/UI |

## Qdrant (vectors)

Embeddings stored in Qdrant collections via `EmbeddingService` — collection names and dimensions are defined in service code. Document collection changes here when implemented.

## Kai Zhe export

`GET /agents/signals/{id}/export` returns `KaiZheSignalExport` with joined source and parsed record context for the intelligence layer.
