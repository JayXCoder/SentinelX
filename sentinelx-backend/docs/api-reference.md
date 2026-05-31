# Backend API reference

Base URL: `http://localhost:4000` (Docker: service `api`, host port **4000**).

OpenAPI: `/docs` · ReDoc: `/redoc`

## Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Overall API health |
| GET | `/health/redis` | Redis connectivity |
| GET | `/health/postgres` | PostgreSQL connectivity |
| GET | `/health/qdrant` | Qdrant connectivity |
| GET | `/health/sglang` | SGLang server reachability |
| GET | `/health/bright-data` | Bright Data config (`mode`: `api`, `proxy`, or `off`) |

## Sources

| Method | Path | Description |
|--------|------|-------------|
| POST | `/sources` | Create source |
| GET | `/sources` | List sources (`active_only` query) |
| GET | `/sources/{source_id}` | Get source |
| PATCH | `/sources/{source_id}` | Update source |
| DELETE | `/sources/{source_id}` | Delete source (204) |

## Scrape jobs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/scrape-jobs` | Create job |
| GET | `/scrape-jobs` | List jobs |
| GET | `/scrape-jobs/{job_id}` | Get job |
| POST | `/scrape-jobs/{job_id}/retry` | Retry failed job |
| POST | `/scrape-jobs/run-source/{source_id}` | Enqueue scrape for source |

## Records

| Method | Path | Description |
|--------|------|-------------|
| GET | `/records/raw` | List raw records |
| GET | `/records/raw/{record_id}` | Get raw record |
| GET | `/records/parsed` | List parsed records |
| GET | `/records/parsed/{record_id}` | Get parsed record |

## Agents & signals

| Method | Path | Query / body | Description |
|--------|------|--------------|-------------|
| POST | `/agents/process/{parsed_record_id}` | `agents[]`, `async_mode` | Run agents on one record |
| POST | `/agents/process-batch` | `ProcessBatchRequest` | Queue batch processing |
| GET | `/agents/status` | — | Available agent names |
| GET | `/agents/signals` | `signal_type`, `limit` (default 50) | **Dashboard primary read** |
| GET | `/agents/signals/{signal_id}` | — | Single signal |
| GET | `/agents/signals/{signal_id}/export` | — | Kai Zhe export payload |

### `GET /agents/signals`

**Query parameters**

| Param | Type | Description |
|-------|------|-------------|
| `signal_type` | string | Filter: `cyber`, `gtm`, `vendor_risk`, `financial`, `osint`, `executive_summary`, etc. |
| `limit` | int | Max rows (default `50`) |

**Response** — array of `IntelligenceSignalRead`:

```json
{
  "id": "uuid",
  "parsed_record_id": "uuid",
  "signal_type": "cyber",
  "category": "threat",
  "title": "string",
  "summary": "string",
  "entities": [],
  "severity": 7,
  "confidence": 0.85,
  "source_reliability": 0.9,
  "evidence": ["..."],
  "recommended_action": "string | null",
  "created_at": "2026-05-28T12:00:00Z"
}
```

## Monitoring

| Method | Path | Description |
|--------|------|-------------|
| GET | `/monitoring/streams` | Redis stream stats |
| GET | `/monitoring/workers` | Celery worker status |
| GET | `/monitoring/jobs` | Recent scrape jobs |
| GET | `/monitoring/errors` | Recent errors |

## Signal type → frontend mapping

| `signal_type` | Frontend surface |
|---------------|------------------|
| `cyber` | Threat feed |
| `gtm` | Competitors |
| `vendor_risk` | Vendors |
| `executive_summary` | Overview summary text |
| (all) | Overview metrics, alerts (severity ≥ 6) |

## Realtime (WebSocket)

| Protocol | Path | Description |
|----------|------|-------------|
| WS | `/ws` | Live dashboard events (JSON messages) |

**Env (frontend):** `NEXT_PUBLIC_WS_URL=ws://localhost:4000/ws`

The API process runs a background Redis `XREAD` listener on Jay signal streams and Kai Zhe output streams (`correlated_events`, `risk_scores`, `executive_alerts`). Each message is mapped and broadcast to all connected clients.

### Event types

| `type` | Source streams | `data` shape |
|--------|----------------|--------------|
| `new_signal` | `cyber_signals`, `gtm_signals`, `financial_signals`, `vendor_risk_signals`, `osint_signals`, `executive_summaries` | Intelligence signal (frontend `IntelligenceSignal`) |
| `new_correlated_event` | `correlated_events` | Correlated event |
| `new_risk_score` | `risk_scores` | Risk score |
| `new_alert` | `executive_alerts` | Alert summary |
| `system_status_update` | On connect | `{ status, clients }` |

**Example message:**

```json
{
  "type": "new_signal",
  "data": {
    "id": "uuid",
    "signal_type": "cyber",
    "title": "…",
    "severity": 7,
    "created_at": "2026-05-29T12:00:00Z"
  }
}
```

Implementation: `app/api/routes/ws.py`, `app/services/realtime_hub.py`, `app/services/realtime_listener.py`.

## Error conventions

| Status | Meaning |
|--------|---------|
| 404 | Entity not found |
| 422 | Validation error (Pydantic) |
| 500 | Unhandled server error |

Update this file when adding routes under `app/api/routes/`.
