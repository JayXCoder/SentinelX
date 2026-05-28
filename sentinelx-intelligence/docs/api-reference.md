# Intelligence API reference (planned)

Base URL: `http://localhost:4001` · Env: `NEXT_PUBLIC_INTELLIGENCE_API_URL`

**Status:** Not implemented — catalog from task spec. Mark sections ✅ when live.

## Correlation

| Method | Path | Status |
|--------|------|--------|
| POST | `/correlation/run` | ☐ |
| POST | `/correlation/run/{signal_id}` | ☐ |
| GET | `/correlation/events` | ☐ (frontend calls today → empty fallback) |
| GET | `/correlation/events/{event_id}` | ☐ |
| GET | `/correlation/entities/{entity_id}/events` | ☐ |

## Risk scores

| Method | Path | Status |
|--------|------|--------|
| POST | `/risk-scores/recalculate` | ☐ |
| POST | `/risk-scores/recalculate/{entity_id}` | ☐ |
| GET | `/risk-scores` | ☐ (frontend fallback via signals) |
| GET | `/risk-scores/{score_id}` | ☐ |
| GET | `/risk-scores/entity/{entity_id}` | ☐ |
| GET | `/risk-scores/type/{score_type}` | ☐ |

## RAG

| Method | Path | Status |
|--------|------|--------|
| POST | `/rag/query` | ☐ |
| POST | `/rag/ask` | ☐ (frontend `askRagQuestion`) |
| GET | `/rag/memory/{entity_id}` | ☐ |
| POST | `/rag/reindex` | ☐ |

## Analytics

| Method | Path | Status |
|--------|------|--------|
| GET | `/analytics/overview` | ☐ |
| GET | `/analytics/top-risks` | ☐ |
| GET | `/analytics/top-opportunities` | ☐ |
| GET | `/analytics/vendor-risk-summary` | ☐ |
| GET | `/analytics/cyber-risk-summary` | ☐ |
| GET | `/analytics/market-movement-summary` | ☐ |

## WebSocket (planned)

| Path | Purpose |
|------|---------|
| `/ws` | Realtime signal and alert push |

Frontend env `NEXT_PUBLIC_WS_URL` defaults to `ws://localhost:4000/ws` until routing is finalized.

Update this table when endpoints ship; include request/response JSON examples per route.
