# SentinelX Master Checklist

Track MVP completion across the team. Specs: [sentinelx_master.md](sentinelx_master.md).

**Legend:** ✅ done · ☐ todo (change the symbol when you complete an item)

---

## Jay — Backend ingestion & AI pipeline

**Owner:** Jay · **Path:** `sentinelx-backend/` · **Spec:** [sentinelx_task_jay.md](sentinelx_task_jay.md)

### Scraping

- ✅ Source CRUD complete
- ✅ Scrape job creation complete
- ✅ Bright Data scraping complete
- ✅ Raw record storage complete
- ✅ Retry logic complete

### Parsing

- ✅ HTML parser complete
- ✅ Text cleaner complete
- ✅ Metadata extractor complete
- ✅ Parsed record storage complete

### Redis

- ✅ Redis streams created
- ✅ Producers implemented
- ✅ Consumers implemented
- ✅ Stream monitoring endpoint complete

### AI Agents

- ✅ Cyber Agent complete
- ✅ GTM Agent complete
- ✅ Financial Agent complete
- ✅ Vendor Risk Agent complete
- ✅ OSINT Agent complete
- ✅ Executive Summary Agent complete

### Storage

- ✅ PostgreSQL models complete
- ✅ PostgreSQL migrations complete
- ✅ Qdrant collections created
- ✅ Embedding storage complete

### API

- ✅ Health endpoints complete
- ✅ Source endpoints complete
- ✅ Job endpoints complete
- ✅ Record endpoints complete
- ✅ Agent endpoints complete
- ✅ Monitoring endpoints complete

### Docker

- ✅ Dockerfile complete
- ✅ docker-compose.yml complete
- ✅ Environment variables documented
- ✅ All services start successfully (core stack; SGLang uses `--profile ai` when GPU available)

---

## Kai Zhe — Correlation, scoring, knowledge graph, RAG

**Owner:** Kai Zhe · **Path:** `sentinelx-intelligence/` · **Spec:** [sentinelx_task_kai_zhe.md](sentinelx_task_kai_zhe.md)

### Correlation

- ✅ Consume cyber signals
- ✅ Consume GTM signals
- ✅ Consume financial signals
- ✅ Consume vendor risk signals
- ✅ Consume OSINT signals
- ✅ Create correlated events
- ✅ Store correlated events
- ✅ Publish correlated event stream

### Risk scoring

- ✅ Cyber exposure scoring complete
- ✅ Vendor risk scoring complete
- ✅ GTM opportunity scoring complete
- ✅ Market threat scoring complete
- ✅ Reputation scoring complete
- ✅ Risk level mapping complete
- ✅ Explanation generation complete

### Knowledge graph

- ✅ Entity model complete
- ✅ Relationship model complete
- ✅ Entity upsert logic complete
- ✅ Relationship creation logic complete
- ✅ Entity timeline endpoint complete

### RAG memory

- ✅ Qdrant collections created
- ✅ Signal memory stored
- ✅ Event memory stored
- ✅ Risk explanation memory stored
- ✅ RAG query endpoint complete
- ✅ Qwen answer generation complete

### API

- ✅ Correlation endpoints complete
- ✅ Risk score endpoints complete
- ✅ Graph endpoints complete
- ✅ RAG endpoints complete
- ✅ Analytics endpoints complete

### Docker

- ✅ Dockerfile complete
- ✅ docker-compose service configured
- ✅ Environment variables documented
- ✅ Service starts successfully

---

## Raymond — Frontend architecture & dashboard

**Owner:** Raymond · **Path:** `sentinelx-frontend/` · **Spec:** [sentinelx_task_raymond.md](sentinelx_task_raymond.md)

> **2026-05-29:** Intelligence service wired at `NEXT_PUBLIC_INTELLIGENCE_API_URL` (:4001). Backend `WS /ws` tails Redis signal + intelligence output streams; frontend connects with 30s polling fallback if WS unavailable.

### Project setup

- ✅ Next.js project created
- ✅ TypeScript configured
- ✅ Tailwind CSS v4 configured
- ✅ Folder structure completed
- ✅ Dockerfile created
- ✅ Environment variables documented (`.env.example`)

### Layout

- ✅ Dashboard layout created
- ✅ Sidebar created
- ✅ Topbar created
- ✅ Responsive layout completed (mobile drawer sidebar, `min-w-0` overflow fixes, breakpoint grids)

### Pages

- ✅ Executive Overview page completed (`/dashboard`, redirect at `/dashboard/executive-overview`)
- ✅ Threat Feed page completed
- ✅ Competitor Intelligence page completed
- ✅ Vendor Monitoring page completed
- ✅ Alerts page completed
- ✅ Intelligence Explorer page completed
- ✅ Marketing landing page completed (`/` — not in original Raymond spec but shipped)

### API integration

- ✅ API client completed (dual backend + intelligence bases)
- ✅ Dashboard overview API integrated (`/analytics/overview` + signals fallback)
- ✅ Signal APIs integrated (`/agents/signals?signal_type=…`)
- ✅ Risk score APIs integrated (`/risk-scores`, `/analytics/top-risks`)
- ✅ Correlation APIs integrated (`/correlation/events`)
- ✅ RAG API integrated (`POST /rag/ask`)

### Real-time

- ✅ WebSocket client completed (`lib/websocket-client.ts` with connection callbacks)
- ✅ New alert event handled (Zustand store + toast)
- ✅ New signal event handled
- ✅ New risk score event handled
- ✅ Toast notification implemented
- ✅ Live backend WebSocket endpoint (`WS /ws` on :4000 — tails Redis streams, broadcasts to dashboard)

### UX states

- ✅ Loading states completed
- ✅ Error states completed
- ✅ Empty states completed
- ✅ Filters completed (`FilterBar` + Zustand; threat/competitor/vendor pages)
- ✅ Search completed (`SearchDialog` → threat feed `?q=`)
- ✅ Pagination completed where required (threat feed, competitors, vendors)

---

## Geng Xin — Design system & UI/UX

**Owner:** Geng Xin · **Path:** `sentinelx-frontend/` · **Spec:** [sentinelx_task_geng_xin.md](sentinelx_task_geng_xin.md)

> **2026-05-29:** `ScoreCard`, `DataTable`, `Modal`, live `RiskChart` / `TopEntitiesTable`, `RealtimeIndicator`, and design docs added under `sentinelx-frontend/docs/`.

### Design system

- ✅ Color palette completed (`app/globals.css` — light/dark tokens)
- ✅ Typography system completed (DM Sans body/logo, Source Serif display)
- ✅ Spacing system completed (Tailwind v4 + section rhythm)
- ✅ Theme consistency completed (light/dark toggle, shared tokens on landing + dashboard)

### Components

- ✅ Metric cards completed
- ✅ Risk score cards completed (`components/dashboard/score-card.tsx`)
- ✅ Tables completed (`components/tables/data-table.tsx` + top entities)
- ✅ Charts completed (`RiskChart` from live risk scores)
- ✅ Modals completed (`components/ui/modal.tsx` — signal + vendor detail)
- ✅ Alert toasts completed
- ✅ Loading components completed
- ✅ CTA buttons completed (`btn-cta` / `CtaButton` — solid, warm, secondary, ghost)

### Real-time UI

- ✅ Notification system completed
- ✅ Live update animations completed (chart bar transitions; marketing motion retained)
- ✅ Realtime indicators completed (`RealtimeIndicator` — connected / polling / offline)

### Responsive

- ✅ Desktop layout completed
- ✅ Tablet layout completed (responsive grids on landing + dashboard)
- ✅ Mobile layout completed (marketing header; dashboard hamburger + slide-out nav)

### Accessibility

- ✅ Keyboard navigation completed (modals Escape, table row Enter/Space, focusable controls)
- ✅ Focus states completed (`focus-visible` on buttons, inputs, tables)
- ✅ Color contrast verified (documented WCAG AA targets in `docs/design-system.md`)

### Documentation

- ✅ Component documentation completed (`docs/components.md`)
- ✅ Design system documented (`docs/design-system.md`)
- ✅ Reusable component guidelines completed (`docs/components.md`)

---

## Platform — Docker & CI/CD

- ✅ Root `docker-compose.yml` — full stack (`api`, `intelligence_api`, `frontend`, workers; port 4002)
- ✅ ChamPeng bootstrap — `scripts/bootstrap-champeng.sh` + `sentinelx-backend/scripts/seed_champeng.py`
- ✅ GitHub Actions CI — backend lint/test/docker; frontend `npm run build` + Docker
- ✅ SGLang service configured for `Qwen/Qwen3.5-2B` (`docker compose --profile ai`)
- ✅ Intelligence service on port 4001 (default compose, no profile required)
