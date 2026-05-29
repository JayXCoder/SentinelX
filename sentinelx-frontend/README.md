# SentinelX Frontend

Next.js dashboard (Raymond + Geng Xin). Marketing landing and executive dashboard wired to `sentinelx-backend`.

## Documentation (required)

Document **all routes, API integrations, UI behavior, and user workflows** in `docs/` — including Mermaid diagrams for data flow and navigation.

| Doc | Contents |
|-----|----------|
| [docs/README.md](docs/README.md) | Index and standards |
| [docs/architecture.md](docs/architecture.md) | App Router, components, theming |
| [docs/api-integration.md](docs/api-integration.md) | Every `apiClient` call and env var |
| [docs/workflow.md](docs/workflow.md) | User journeys (Mermaid) |
| [docs/routes-and-pages.md](docs/routes-and-pages.md) | URL → data source map |

Specs: [../docs/sentinelx_task_raymond.md](../docs/sentinelx_task_raymond.md), [../docs/sentinelx_task_geng_xin.md](../docs/sentinelx_task_geng_xin.md)

**Rule:** New page or API usage → update `docs/api-integration.md` and `docs/routes-and-pages.md` in the same PR.

## Setup

```bash
cp .env.example .env.local
npm install
npm run dev
```

- App: http://localhost:3000  
- Dashboard: `/dashboard`

## Environment

| Variable | Default |
|----------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:4000` |
| `NEXT_PUBLIC_INTELLIGENCE_API_URL` | `http://localhost:4001` |
| `NEXT_PUBLIC_WS_URL` | `ws://localhost:4000/ws` |

## Backend integration (summary)

| UI area | API |
|---------|-----|
| Overview, alerts | `GET /agents/signals` (aggregated client-side) |
| Threat feed | `?signal_type=cyber` |
| Competitors | `?signal_type=gtm` |
| Vendors | `?signal_type=vendor_risk` |
| RAG / correlation | Intelligence service (graceful fallback) |

Details: [docs/api-integration.md](docs/api-integration.md)

## Stack

Next.js 15 · TypeScript · Tailwind v4 · Zustand · Framer Motion · Lucide

## Docker

From repo root: `docker compose up -d --build` → http://localhost:4002
