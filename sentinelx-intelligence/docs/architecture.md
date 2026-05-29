# Intelligence architecture (target)

Planned FastAPI service on port **4001** (compose profile `intelligence`). Consumes Jay's signals and provides correlation, risk scoring, knowledge graph, and RAG.

## Target system context

```mermaid
flowchart TB
  subgraph jay [sentinelx-backend]
    SIG[GET /agents/signals]
    EXP[GET /agents/signals/id/export]
  end

  subgraph kz [sentinelx-intelligence]
    COR[Correlation engine]
    RISK[Risk scoring]
    KG[Knowledge graph]
    RAG[RAG memory]
    API[FastAPI :4001]
  end

  subgraph stores [Shared stores]
    PG[(PostgreSQL)]
    QD[(Qdrant)]
    RD[(Redis)]
  end

  subgraph ui [sentinelx-frontend]
    DASH[Dashboard pages]
  end

  EXP --> COR
  SIG -.-> COR
  COR --> PG
  RAG --> QD
  RISK --> PG
  API --> COR & RISK & RAG & KG
  DASH --> API
```

## Planned modules

| Module | Responsibility |
|--------|----------------|
| Correlation | Cluster signals into events, entity timelines |
| Risk scoring | Entity-level scores by type |
| Knowledge graph | Entities and relationships |
| RAG | Query memory, reindex, entity recall |
| Analytics | Aggregated summaries for dashboard widgets |

## Deployment

```bash
docker compose --profile intelligence up -d --build
```

Until Dockerfile is fully implemented, this profile may remain disabled in production compose defaults.
