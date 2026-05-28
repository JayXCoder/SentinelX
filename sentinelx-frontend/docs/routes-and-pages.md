# Routes and pages

## Route map

```mermaid
flowchart TB
  root[/] --> marketing[Landing]
  root --> dash[/dashboard]
  dash --> overview[Executive overview]
  dash --> threats[Threat feed]
  dash --> comp[Competitors]
  dash --> vend[Vendors]
  dash --> alerts[Alerts]
  dash --> explorer[Intelligence explorer]
  dash --> execRedirect[/dashboard/executive-overview → redirect]
```

## Page catalog

| Route | File | Data source | Functionality |
|-------|------|-------------|---------------|
| `/` | `app/page.tsx` | None (static marketing) | Hero, use cases, platform capabilities, FAQ, CTA |
| `/dashboard` | `app/dashboard/page.tsx` | `getDashboardOverview`, `getRiskScores` | KPI cards, summary, risk table |
| `/dashboard/threat-feed` | `app/dashboard/threat-feed/page.tsx` | `getCyberSignals` | Cyber signals list |
| `/dashboard/competitors` | `app/dashboard/competitors/page.tsx` | `getGtmSignals` | GTM / competitor signals |
| `/dashboard/vendors` | `app/dashboard/vendors/page.tsx` | `getVendorSummary` | Vendor risk entities |
| `/dashboard/alerts` | `app/dashboard/alerts/page.tsx` | `getAlerts` | High-severity active alerts |
| `/dashboard/intelligence-explorer` | `app/dashboard/intelligence-explorer/page.tsx` | `askRagQuestion` | RAG Q&A (when service live) |
| `/dashboard/executive-overview` | redirect | — | Redirects to `/dashboard` |

## Layout

| File | Scope |
|------|-------|
| `app/layout.tsx` | Root fonts, `ThemeProvider`, global CSS |
| `app/dashboard/layout.tsx` | `DashboardShell` — sidebar, mobile nav |

## Responsive behavior

`DashboardShell` provides:

- Desktop: fixed sidebar
- Mobile: drawer overlay + hamburger

Document new breakpoints or layout changes in [architecture.md](architecture.md).
