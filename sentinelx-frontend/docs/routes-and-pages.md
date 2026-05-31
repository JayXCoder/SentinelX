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

| Route | File | Data sources | Features |
|-------|------|--------------|----------|
| `/` | `app/page.tsx` | Static | Marketing landing |
| `/dashboard` | `app/dashboard/page.tsx` | `getDashboardOverview`, risk chart, top risks, correlated events, alerts | KPIs, realtime indicator |
| `/dashboard/threat-feed` | `threat-feed/page.tsx` | `getCyberSignals` | Filters, search (`?q=`), pagination, signal modal |
| `/dashboard/competitors` | `competitors/page.tsx` | `getGtmSignals`, `getRiskScoresByType(gtm_opportunity)` | Filters, pagination, opportunity score cards |
| `/dashboard/vendors` | `vendors/page.tsx` | `getVendorSummary` (intelligence) | Score cards, filters, pagination, vendor modal |
| `/dashboard/alerts` | `alerts/page.tsx` | `getAlerts` | High-severity signal alerts |
| `/dashboard/intelligence-explorer` | `intelligence-explorer/page.tsx` | `askRagQuestion` | Question form, evidence, entities |
| `/dashboard/executive-overview` | redirect | — | → `/dashboard` |

## Layout

| File | Scope |
|------|-------|
| `app/layout.tsx` | Root fonts, `ThemeProvider` |
| `app/dashboard/layout.tsx` | `DashboardShell` — sidebar, topbar, search, filters |

## Responsive behavior

- Desktop: fixed sidebar (`xl:static`)
- Mobile: drawer + hamburger (`DashboardShell`)
- Tables: horizontal scroll via `overflow-x-auto`
