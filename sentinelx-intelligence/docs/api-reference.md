# Intelligence API reference

Base URL: `http://localhost:4001` · Env: `NEXT_PUBLIC_INTELLIGENCE_API_URL`

**Status:** Implemented — consumed by `sentinelx-frontend` `lib/api-client.ts`.

## Correlation

| Method | Path | Status |
|--------|------|--------|
| POST | `/correlation/run` | ✅ |
| POST | `/correlation/run/{signal_id}` | ✅ |
| GET | `/correlation/events` | ✅ |
| GET | `/correlation/events/{event_id}` | ✅ |
| GET | `/correlation/entities/{entity_id}/events` | ✅ |

Query params for list: `skip`, `limit`, `event_type`.

## Risk scores

| Method | Path | Status |
|--------|------|--------|
| POST | `/risk-scores/recalculate` | ✅ |
| POST | `/risk-scores/recalculate/{entity_id}` | ✅ |
| GET | `/risk-scores` | ✅ |
| GET | `/risk-scores/{score_id}` | ✅ |
| GET | `/risk-scores/entity/{entity_id}` | ✅ |
| GET | `/risk-scores/type/{score_type}` | ✅ |

`score_type` values: `cyber_exposure`, `vendor_risk`, `gtm_opportunity`, `market_threat`, `financial_risk`, `reputation_risk`.

## Knowledge graph

| Method | Path | Status |
|--------|------|--------|
| GET | `/graph/entities` | ✅ |
| GET | `/graph/entities/{entity_id}` | ✅ |
| GET | `/graph/timeline/{entity_id}` | ✅ |

## RAG

| Method | Path | Status |
|--------|------|--------|
| POST | `/rag/query` | ✅ |
| POST | `/rag/ask` | ✅ |
| GET | `/rag/memory/{entity_id}` | ✅ |
| POST | `/rag/reindex` | ✅ |

**Ask body:** `{ "question": "string", "entity_id": "uuid?", "top_k": 5 }`

**Response:** `{ answer, confidence, supporting_evidence[], related_entities[], related_events[], recommended_action }`

## Analytics

| Method | Path | Status |
|--------|------|--------|
| GET | `/analytics/overview` | ✅ |
| GET | `/analytics/top-risks` | ✅ |
| GET | `/analytics/top-opportunities` | ✅ |
| GET | `/analytics/vendor-risk-summary` | ✅ |
| GET | `/analytics/cyber-risk-summary` | ✅ |
| GET | `/analytics/market-movement-summary` | ✅ |

## Health

| Method | Path | Status |
|--------|------|--------|
| GET | `/health` | ✅ |

## Realtime (via backend WebSocket)

Dashboard realtime is served by the **Jay backend** at `WS /ws` (port 4000), which tails Redis streams including intelligence outputs (`correlated_events`, `risk_scores`, `executive_alerts`). This service publishes those stream messages from Celery workers; no separate WebSocket port on :4001.
