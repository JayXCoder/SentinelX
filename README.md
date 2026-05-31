# SentinelX — ChamPeng

AI-powered competitive intelligence for **ChamPeng** (coding-agent IDE + multi-model platform). Monitors **OpenAI**, **Anthropic**, **Cursor**, and **Antigravity** with **Qwen/Qwen3.5-2B** via SGLang.

See [docs/champeng-profile.md](docs/champeng-profile.md) and [docs/sentinelx_master.md](docs/sentinelx_master.md).

## One-command ship

```bash
cp .env.example .env
# Set HF_TOKEN, BRIGHT_DATA_API_KEY, BRIGHT_DATA_ZONE in .env
chmod +x scripts/bootstrap-champeng.sh
./scripts/bootstrap-champeng.sh
```

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:4002 |
| Backend API | http://localhost:4000/docs |
| Intelligence API | http://localhost:4001/docs |
| WebSocket | ws://localhost:4000/ws |

### GPU + Qwen inference

```bash
docker compose --profile ai up -d sglang_qwen
```

Requires NVIDIA GPU + `HF_TOKEN` in `.env`.

## Monorepo

| Path | Role |
|------|------|
| [sentinelx-backend/](sentinelx-backend/) | Ingestion, Bright Data, agents, WebSocket |
| [sentinelx-intelligence/](sentinelx-intelligence/) | Correlation, risk scores, RAG, graph |
| [sentinelx-frontend/](sentinelx-frontend/) | ChamPeng dashboard + marketing |

## Documentation

| Location | Index |
|----------|-------|
| [docs/master-checklist.md](docs/master-checklist.md) | MVP checklist |
| [docs/champeng-profile.md](docs/champeng-profile.md) | Company + competitors |
| [docs/platform-architecture.md](docs/platform-architecture.md) | Ports & services |

## Stop stack

```bash
docker compose down
```
