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

- ☐ Consume cyber signals
- ☐ Consume GTM signals
- ☐ Consume financial signals
- ☐ Consume vendor risk signals
- ☐ Consume OSINT signals
- ☐ Create correlated events
- ☐ Store correlated events
- ☐ Publish correlated event stream

### Risk scoring

- ☐ Cyber exposure scoring complete
- ☐ Vendor risk scoring complete
- ☐ GTM opportunity scoring complete
- ☐ Market threat scoring complete
- ☐ Reputation scoring complete
- ☐ Risk level mapping complete
- ☐ Explanation generation complete

### Knowledge graph

- ☐ Entity model complete
- ☐ Relationship model complete
- ☐ Entity upsert logic complete
- ☐ Relationship creation logic complete
- ☐ Entity timeline endpoint complete

### RAG memory

- ☐ Qdrant collections created
- ☐ Signal memory stored
- ☐ Event memory stored
- ☐ Risk explanation memory stored
- ☐ RAG query endpoint complete
- ☐ Qwen answer generation complete

### API

- ☐ Correlation endpoints complete
- ☐ Risk score endpoints complete
- ☐ Graph endpoints complete
- ☐ RAG endpoints complete
- ☐ Analytics endpoints complete

### Docker

- ☐ Dockerfile complete
- ☐ docker-compose service configured
- ☐ Environment variables documented
- ☐ Service starts successfully

---

## Raymond — Frontend architecture & dashboard

**Owner:** Raymond · **Path:** `sentinelx-frontend/` · **Spec:** [sentinelx_task_raymond.md](sentinelx_task_raymond.md)

> **2026-05-28:** `FrontendRef/` transferred into `sentinelx-frontend/` (Next.js 15 + Tailwind v4). Marketing landing (Handhold-inspired), light/dark theme, and dashboard wired to Jay's API at `GET /agents/signals` (port 4000). Mobile dashboard drawer + responsive grids added. Intelligence-service endpoints (correlation, dedicated risk scores, RAG, analytics) not live yet.

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

- ✅ API client completed
- ✅ Dashboard overview API integrated (aggregated from `/agents/signals`)
- ✅ Signal APIs integrated (`/agents/signals?signal_type=…`)
- ☐ Risk score APIs integrated (no `/risk-scores` service; vendor page uses signal-derived scores only)
- ☐ Correlation APIs integrated (`/correlation/events` called but service absent; UI shows static placeholder events)
- ☐ RAG API integrated (`askRagQuestion` wired; `/rag/ask` absent — UI shows error/empty state)

### Real-time

- ✅ WebSocket client completed (`lib/websocket-client.ts`)
- ✅ New alert event handled (Zustand store + toast)
- ✅ New signal event handled
- ✅ New risk score event handled
- ✅ Toast notification implemented
- ☐ Live backend WebSocket endpoint (no `/ws` on backend yet; client fails silently)

### UX states

- ✅ Loading states completed
- ✅ Error states completed
- ✅ Empty states completed
- ☐ Filters completed (label-only panels on threat/competitor pages; `use-filters` store exists, not wired to UI)
- ☐ Search completed (topbar button only, no search flow)
- ☐ Pagination completed where required

---

## Geng Xin — Design system & UI/UX

**Owner:** Geng Xin · **Path:** `sentinelx-frontend/` · **Spec:** [sentinelx_task_geng_xin.md](sentinelx_task_geng_xin.md)

> **2026-05-28:** Warm Handhold-inspired palette, DM Sans + Source Serif 4, light/dark via `ThemeProvider` + CSS variables. CTA system (`btn-cta` classes) for visible buttons. Marketing scroll animations (Framer Motion). Dashboard uses semantic tokens; charts/tables/modals still placeholders.

### Design system

- ✅ Color palette completed (`app/globals.css` — light/dark tokens)
- ✅ Typography system completed (DM Sans body/logo, Source Serif display)
- ✅ Spacing system completed (Tailwind v4 + section rhythm)
- ✅ Theme consistency completed (light/dark toggle, shared tokens on landing + dashboard)

### Components

- ✅ Metric cards completed
- ☐ Risk score cards completed (vendor rows show scores; no dedicated score-card component)
- ☐ Tables completed (`TopEntitiesTable` is static mock data)
- ☐ Charts completed (`RiskChart` is static bar placeholders)
- ☐ Modals completed
- ✅ Alert toasts completed
- ✅ Loading components completed
- ✅ CTA buttons completed (`btn-cta` / `CtaButton` — solid, warm, secondary, ghost)

### Real-time UI

- ✅ Notification system completed
- ✅ Live update animations completed (marketing: fade-in, stagger, floating demo; not live data-driven dashboard animations)
- ☐ Realtime indicators completed (dashboard “Realtime” / “When WS available” copy is static, not connection state)

### Responsive

- ✅ Desktop layout completed
- ✅ Tablet layout completed (responsive grids on landing + dashboard)
- ✅ Mobile layout completed (marketing header; dashboard hamburger + slide-out nav)

### Accessibility

- ☐ Keyboard navigation completed (partial: FAQ `<details>`, focus on CTAs only)
- ☐ Focus states completed (`focus-visible` on `btn-cta` only; not audited app-wide)
- ☐ Color contrast verified (not formally tested)

### Documentation

- ☐ Component documentation completed
- ☐ Design system documented
- ☐ Reusable component guidelines completed

---

## Platform — Docker & CI/CD

- ✅ Root `docker-compose.yml` — full stack in one command (`api`, `frontend`, postgres, redis, qdrant, celery; port 4002)
- ✅ GitHub Actions CI — backend lint/test/docker; frontend `npm run build` + Docker; `docker compose build api frontend`
- ✅ SGLang service configured for `Qwen/Qwen3.5-2B` (`--profile ai`)
- ✅ Intelligence scaffold on `--profile intelligence` (port 4001 when implemented)
