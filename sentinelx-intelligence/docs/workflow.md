# Intelligence workflows (target)

## Signal ingestion from backend

```mermaid
sequenceDiagram
  participant Jay as Backend export
  participant KZ as Intelligence service
  participant COR as Correlation engine
  participant PG as PostgreSQL

  Jay->>KZ: GET /agents/signals/{id}/export
  KZ->>COR: ingest signal + provenance
  COR->>PG: persist event / entity links
```

## Correlation run

```mermaid
flowchart TD
  A[POST /correlation/run] --> B[Load recent signals]
  B --> C[Entity resolution]
  C --> D[Cluster into events]
  D --> E[Persist correlation_events]
  E --> F[GET /correlation/events]
```

## Risk score recalculation

```mermaid
sequenceDiagram
  participant Op as Operator / scheduler
  participant API as POST /risk-scores/recalculate
  participant Engine as Scoring engine
  participant DB as PostgreSQL

  Op->>API: trigger
  API->>Engine: recompute by entity/type
  Engine->>DB: upsert risk_scores
  Op->>API: GET /risk-scores
```

## RAG query

```mermaid
sequenceDiagram
  participant UI as Intelligence explorer
  participant API as POST /rag/ask
  participant RAG as RAG service
  participant QD as Qdrant

  UI->>API: question
  API->>RAG: retrieve + generate
  RAG->>QD: vector search
  QD-->>RAG: chunks
  RAG-->>API: answer + citations
  API-->>UI: RagAnswerDto
```

## Frontend integration workflow

```mermaid
flowchart LR
  subgraph today [Current]
    T1[Dashboard] --> B1[Backend /agents/signals]
  end

  subgraph future [Target]
    T2[Dashboard] --> B2[Backend signals]
    T2 --> K1[Correlation API]
    T2 --> K2[RAG API]
    T2 --> K3[Risk scores API]
  end
```

Replace “target” diagrams with implemented paths as code lands.
