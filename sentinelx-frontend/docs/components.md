# Component guidelines

**Owners:** Geng Xin (visual system) · Raymond (data wiring)

## When to add a component

1. Used on two or more dashboard pages, or
2. Encapsulates a distinct interaction (modal, pagination, realtime status)

Prefer extending existing primitives before creating new variants.

## UI primitives (`components/ui/`)

| Component | File | Props / behavior |
|-----------|------|------------------|
| `Input` | `input.tsx` | Optional `label`, full-width rounded field |
| `Modal` | `modal.tsx` | `open`, `title`, `onClose`, Escape dismiss, focus ring |
| `Badge` | `badge.tsx` | Optional `level` maps risk level to color |
| `CtaButton` | `cta-button.tsx` | Marketing + dashboard CTAs via `btn-cta` classes |

## Dashboard (`components/dashboard/`)

| Component | Purpose |
|-----------|---------|
| `MetricCard` | KPI value + delta + tone |
| `ScoreCard` | Risk score with level badge; optional `onSelect` |
| `SignalFeed` | List of intelligence signals |
| `FilterBar` | Risk level, time range, keyword (Zustand-backed) |
| `PaginationControls` | Previous/next with totals |
| `RealtimeIndicator` | WebSocket / polling / offline status |
| `SearchDialog` | Global search → threat feed with `?q=` |
| `RiskChart` | Bar chart from `/risk-scores` aggregation |
| `TopEntitiesTable` | Data table from `/analytics/top-risks` |
| `CorrelatedEvents` | Live list from `/correlation/events` |
| `LoadingState` / `ErrorState` | Standard async UI |

## Tables (`components/tables/`)

`DataTable<T>` — generic columns with optional row click and keyboard Enter/Space.

## State

- **Filters / search / realtime:** `stores/dashboard-store.ts`
- **Theme:** `stores/theme-store.ts`
- **Page data:** hooks in `hooks/` calling `apiClient`

## Styling rules

- Use semantic tokens: `bg-background`, `text-foreground`, `border-border`, `text-accent`
- Avoid raw hex in feature components except chart gradients
- Loading: `LoadingState` or skeleton-style bordered panels
- Empty: muted copy inside `rounded-2xl border border-border bg-background`

## Example: score card on vendor page

```tsx
<ScoreCard score={entity} onSelect={setSelectedVendor} />
<Modal open={Boolean(selectedVendor)} title={selectedVendor?.entity_name} onClose={...}>
  ...
</Modal>
```
