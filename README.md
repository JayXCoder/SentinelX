# SentinelX

AI-powered enterprise intelligence platform. See [docs/sentinelx_master.md](docs/sentinelx_master.md).

## Documentation policy

**Every package must ship full documentation** in its `docs/` folder: architecture, API calls, data models, and Mermaid workflows. Treat docs as part of the feature — update them in the same change as code.

| Location | Index |
|----------|-------|
| Platform hub | [docs/README.md](docs/README.md) |
| Platform architecture & ports | [docs/platform-architecture.md](docs/platform-architecture.md) |
| End-to-end workflows (Mermaid) | [docs/platform-workflow.md](docs/platform-workflow.md) |
| Backend | [sentinelx-backend/docs/README.md](sentinelx-backend/docs/README.md) |
| Frontend | [sentinelx-frontend/docs/README.md](sentinelx-frontend/docs/README.md) |
| Intelligence | [sentinelx-intelligence/docs/README.md](sentinelx-intelligence/docs/README.md) |

## Monorepo layout

| Path | Owner | Status |
|------|-------|--------|
| [sentinelx-backend/](sentinelx-backend/) | Jay | Implemented |
| [sentinelx-intelligence/](sentinelx-intelligence/) | Kai Zhe | Scaffold |
| [sentinelx-frontend/](sentinelx-frontend/) | Raymond + Geng Xin | Implemented |

## Quick start — full stack (one command)

From the repo root:

```bash
cp .env.example .env
docker compose up -d --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:4002 |
| Backend API + docs | http://localhost:4000/docs |
| PostgreSQL | localhost:4543 |
| Redis | localhost:4637 |
| Qdrant | localhost:4633 |

Stop everything: `docker compose down`

### Optional profiles

- GPU + SGLang: `docker compose --profile ai up -d --build`
- Intelligence API (when implemented): `docker compose --profile intelligence up -d --build`

### Local frontend dev

```bash
cd sentinelx-frontend
cp .env.example .env.local
npm install
npm run dev
```

Requires the backend API at http://localhost:4000.

## Checklist

[docs/master-checklist.md](docs/master-checklist.md)

## CI

[.github/workflows/ci.yml](.github/workflows/ci.yml) — backend lint/test, frontend build, Docker images, compose validation.
