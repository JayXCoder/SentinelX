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

### Project setup

- ☐ Next.js project created
- ☐ TypeScript configured
- ☐ Tailwind CSS v4 configured
- ☐ Folder structure completed
- ☐ Dockerfile created
- ☐ Environment variables documented

### Layout

- ☐ Dashboard layout created
- ☐ Sidebar created
- ☐ Topbar created
- ☐ Responsive layout completed

### Pages

- ☐ Executive Overview page completed
- ☐ Threat Feed page completed
- ☐ Competitor Intelligence page completed
- ☐ Vendor Monitoring page completed
- ☐ Alerts page completed
- ☐ Intelligence Explorer page completed

### API integration

- ☐ API client completed
- ☐ Dashboard overview API integrated
- ☐ Signal APIs integrated
- ☐ Risk score APIs integrated
- ☐ Correlation APIs integrated
- ☐ RAG API integrated

### Real-time

- ☐ WebSocket or SSE client completed
- ☐ New alert event handled
- ☐ New signal event handled
- ☐ New risk score event handled
- ☐ Toast notification implemented

### UX states

- ☐ Loading states completed
- ☐ Error states completed
- ☐ Empty states completed
- ☐ Filters completed
- ☐ Search completed
- ☐ Pagination completed where required

---

## Geng Xin — Design system & UI/UX

**Owner:** Geng Xin · **Path:** `sentinelx-frontend/` · **Spec:** [sentinelx_task_geng_xin.md](sentinelx_task_geng_xin.md)

### Design system

- ☐ Color palette completed
- ☐ Typography system completed
- ☐ Spacing system completed
- ☐ Theme consistency completed

### Components

- ☐ Metric cards completed
- ☐ Risk score cards completed
- ☐ Tables completed
- ☐ Charts completed
- ☐ Modals completed
- ☐ Alert toasts completed
- ☐ Loading components completed

### Real-time UI

- ☐ Notification system completed
- ☐ Live update animations completed
- ☐ Realtime indicators completed

### Responsive

- ☐ Desktop layout completed
- ☐ Tablet layout completed
- ☐ Mobile layout completed

### Accessibility

- ☐ Keyboard navigation completed
- ☐ Focus states completed
- ☐ Color contrast verified

### Documentation

- ☐ Component documentation completed
- ☐ Design system documented
- ☐ Reusable component guidelines completed

---

## Platform — Docker & CI/CD

- ✅ Root `docker-compose.yml` (postgres, redis, qdrant, api, celery, sglang profile)
- ✅ GitHub Actions CI (lint, test, docker build, compose validate)
- ✅ SGLang service configured for `Qwen/Qwen3.5-2B`
