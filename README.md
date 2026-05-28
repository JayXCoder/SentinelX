# SentinelX

AI-powered enterprise intelligence platform. See [docs/sentinelx_master.md](docs/sentinelx_master.md).

## Monorepo layout

| Path | Owner | Status |
|------|-------|--------|
| [sentinelx-backend/](sentinelx-backend/) | Jay | Implemented |
| [sentinelx-intelligence/](sentinelx-intelligence/) | Kai Zhe | Scaffold |
| [sentinelx-frontend/](sentinelx-frontend/) | Raymond + Geng Xin | Scaffold |

## Quick start (backend stack)

```bash
cp sentinelx-backend/.env.example sentinelx-backend/.env
docker compose up -d postgres redis qdrant api celery_worker celery_beat
```

With GPU + SGLang (Qwen3.5-2B):

```bash
docker compose --profile ai up -d
```

API docs: http://localhost:4000/docs

### Ports (host, range 4000–4999)

| Service | Port |
|---------|------|
| Backend API | 4000 |
| Intelligence API (scaffold) | 4001 |
| Frontend (scaffold) | 4002 |
| SGLang (Qwen) | 4300 |
| PostgreSQL | 4543 |
| Redis | 4637 |
| Qdrant | 4633 |

## Checklist

Team progress: [docs/master-checklist.md](docs/master-checklist.md)

## CI

GitHub Actions runs lint, tests, and Docker builds on push/PR (see `.github/workflows/ci.yml`).
