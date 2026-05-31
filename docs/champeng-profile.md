# ChamPeng — SentinelX tenant profile

SentinelX is configured for **ChamPeng**, a coding-agent platform with an IDE (Cursor-style) that serves **own models** (including **Qwen/Qwen3.5-2B** via SGLang) and **third-party models** (OpenAI, Anthropic, etc.).

## Company

| Field | Value |
|-------|--------|
| Name | ChamPeng |
| Segment | AI coding agents + IDE |
| Model stack | Qwen/Qwen3.5-2B (hosted) + external APIs |

## Product context (fed to AI)

Edit in the dashboard under **Workspace** or via `PATCH /workspace/profile`:

- Product summary and positioning vs Cursor, OpenAI, Anthropic, Antigravity
- Team lenses: **HR** (hiring, culture), **Sales** (pricing, deals), **Tech** (models, security, APIs)
- Custom comparison prompts for RAG

## Competitors monitored

| Competitor | Source | Category |
|------------|--------|----------|
| OpenAI | https://openai.com/news/ | `competitor_openai` |
| Anthropic | https://www.anthropic.com/news | `competitor_anthropic` |
| Cursor | https://cursor.com/blog | `competitor_cursor` |
| Antigravity | https://antigravity.google/ | `competitor_antigravity` |

Add more via **Workspace → Add competitor source** (creates a `/sources` row).

## Human-in-the-loop

| Team | Use case |
|------|----------|
| HR | Hiring signals, culture, talent movement at competitors |
| Sales | Pricing, packaging, enterprise wins, objection handling |
| Tech | CVEs, model releases, API changes, architecture moves |

On any signal detail page (`/dashboard/signals/{id}`):

- View **source URL**, archived excerpt, and **story timeline**
- Add **team notes** (stored in `human_notes`)
- **Ask SentinelX** with ChamPeng workspace context injected

## Historical data & scrape cache

- Raw HTML and parsed text are stored in PostgreSQL permanently.
- Re-scrapes within `SCRAPE_CACHE_HOURS` (default 24) **reuse cached HTML** — no Bright Data call.
- Duplicate content (same SHA-256 hash per source) is not stored twice.

## Bootstrap

```bash
./scripts/bootstrap-champeng.sh
```

## Intelligence questions (RAG explorer)

Example prompts:

- What are the top competitive risks to ChamPeng from Cursor and Antigravity?
- Summarize OpenAI and Anthropic moves relevant to coding agents.
- Which vendor risks affect ChamPeng's multi-model routing?
- What should our sales team say when a prospect mentions Cursor agent mode?
