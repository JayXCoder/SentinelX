# Platform architecture

SentinelX is a monorepo with three application packages orchestrated by root `docker-compose.yml`.

## System context

```mermaid
flowchart TB
  subgraph clients [Clients]
    Browser[Browser / Dashboard user]
    Ops[Operators / API clients]
  end

  subgraph frontend [sentinelx-frontend :4002]
    Next[Next.js 15 App Router]
  end

  subgraph backend [sentinelx-backend :4000]
    API[FastAPI]
    CW[Celery worker]
    CB[Celery beat]
  end

  subgraph intelligence [sentinelx-intelligence :4001]
    Intel[FastAPI scaffold]
  end

  subgraph data [Data plane]
    PG[(PostgreSQL :4543)]
    RD[(Redis :4637)]
    QD[(Qdrant :4633)]
  end

  subgraph ai [Optional profile ai]
    SG[SGLang Qwen :4300]
  end

  Browser --> Next
  Next -->|REST live| API
  Next -.->|REST planned| Intel
  Ops --> API
  API --> PG
  API --> RD
  API --> QD
  API --> SG
  CW --> PG
  CW --> RD
  CW --> QD
  CW --> SG
  CB --> CW
  Intel -.-> PG
  Intel -.-> QD
```

## Port map (host)

| Port | Service |
|------|---------|
| 4000 | Backend API + OpenAPI `/docs` |
| 4001 | Intelligence API (profile `intelligence`) |
| 4002 | Frontend (Next.js) |
| 4300 | SGLang (profile `ai`, GPU) |
| 4543 | PostgreSQL |
| 4637 | Redis |
| 4633 | Qdrant |

## Deployment units

```mermaid
flowchart LR
  subgraph compose [docker compose default]
    postgres
    redis
    qdrant
    api
    celery_worker
    celery_beat
    frontend
  end

  subgraph profiles [Optional profiles]
    ai[sglang_qwen]
    intel[intelligence_api]
  end

  compose --> profiles
```

## CI/CD

```mermaid
flowchart LR
  push[git push / PR] --> CI[GitHub Actions]
  CI --> BL[backend-lint-test]
  CI --> FB[frontend-build]
  CI --> BD[backend-docker]
  CI --> FD[frontend-docker]
  CI --> SB[stack-docker-build]
  CI --> CC[compose-config]
```

See [.github/workflows/ci.yml](../.github/workflows/ci.yml).
