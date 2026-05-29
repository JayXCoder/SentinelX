# Platform workflows

End-to-end flows across backend, intelligence (planned), and frontend.

## 1. Ingestion pipeline (implemented)

Source data enters through scraping and exits as intelligence signals consumed by the dashboard.

```mermaid
sequenceDiagram
  participant Beat as Celery beat
  participant Scrape as scrape_source_task
  participant BD as Bright Data / HTTP
  participant Parse as parse_raw_record_task
  participant AI as process_parsed_record_task
  participant SGL as SGLang Qwen
  participant PG as PostgreSQL
  participant QD as Qdrant
  participant API as FastAPI /agents/signals
  participant UI as Next.js dashboard

  Beat->>Scrape: run_scheduled_sources (every 15m)
  Scrape->>BD: fetch source URL
  BD-->>Scrape: HTML / payload
  Scrape->>PG: raw_record
  Scrape->>Parse: delay(parse)
  Parse->>PG: parsed_record
  Parse->>AI: delay(process)
  AI->>SGL: agent prompts
  SGL-->>AI: structured output
  AI->>PG: intelligence_signals
  AI->>QD: embeddings (when enabled)
  UI->>API: GET /agents/signals
  API->>PG: query signals
  API-->>UI: JSON signals
```

## 2. Operator API workflow

```mermaid
flowchart TD
  A[POST /sources] --> B[POST /scrape-jobs or beat schedule]
  B --> C[scrape_source_task]
  C --> D[raw_record]
  D --> E[parse_raw_record_task]
  E --> F[parsed_record]
  F --> G[process_parsed_record_task]
  G --> H[intelligence_signals]
  H --> I[GET /agents/signals]
```

Manual reprocessing:

```mermaid
sequenceDiagram
  participant Op as Operator
  participant API as POST /agents/process/{id}
  participant Celery as Celery queue
  participant Svc as AgentProcessingService

  Op->>API: async_mode=true
  API->>Celery: process_parsed_record_task
  Celery->>Svc: run agents
  Op->>API: GET /agents/signals
```

## 3. Dashboard read path (implemented)

```mermaid
sequenceDiagram
  participant User as User browser
  participant Page as app/dashboard/*
  participant Client as lib/api-client.ts
  participant API as sentinelx-backend

  User->>Page: navigate
  Page->>Client: apiClient.*
  Client->>API: GET /agents/signals?signal_type=
  API-->>Client: IntelligenceSignal[]
  Client-->>Page: DTO mapped for UI
```

## 4. Intelligence layer (planned)

When `sentinelx-intelligence` is deployed (`--profile intelligence`):

```mermaid
sequenceDiagram
  participant UI as Frontend
  participant Jay as Backend :4000
  participant KZ as Intelligence :4001
  participant QD as Qdrant

  Jay->>KZ: signal export / webhooks (planned)
  UI->>KZ: GET /correlation/events
  UI->>KZ: POST /rag/ask
  UI->>KZ: GET /risk-scores
  KZ->>QD: vector search
  UI->>Jay: GET /agents/signals (fallback aggregates)
```

## 5. Local development workflow

```mermaid
flowchart LR
  subgraph optionA [Full stack Docker]
    DC[docker compose up -d --build]
    DC --> F4002[localhost:4002]
    DC --> A4000[localhost:4000]
  end

  subgraph optionB [Frontend dev]
    NPM[npm run dev :3000]
    NPM --> A4000
  end
```

## 6. Release / CI workflow

```mermaid
stateDiagram-v2
  [*] --> LintTest: push PR
  LintTest --> FrontendBuild: backend OK
  FrontendBuild --> DockerBuild: npm run build OK
  DockerBuild --> ComposeValidate: images OK
  ComposeValidate --> [*]: merge
  LintTest --> [*]: fail
  FrontendBuild --> [*]: fail
```
