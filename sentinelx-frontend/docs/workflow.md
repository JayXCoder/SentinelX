# Frontend workflows

## Marketing site visit

```mermaid
flowchart TD
  A[GET /] --> B[Landing sections]
  B --> C{User action}
  C -->|View platform| D[#platform PlatformSection]
  C -->|Open dashboard| E[/dashboard]
  C -->|Toggle theme| F[ThemeToggle → theme-store]
```

## Dashboard session

```mermaid
sequenceDiagram
  participant U as User
  participant R as App Router
  participant S as DashboardShell
  participant P as Page component
  participant API as apiClient

  U->>R: /dashboard
  R->>S: layout + mobile drawer
  S->>P: render child route
  P->>API: fetch signals / aggregates
  API-->>P: data or ApiError
  P-->>U: tables / cards / empty state
```

## Overview page data derivation

`getDashboardOverview()` does not call a dedicated backend overview endpoint. It derives:

```mermaid
flowchart LR
  SIG[GET /agents/signals limit=100] --> COUNT[count signals]
  SIG --> CRIT[severity >= 7 → critical_alerts]
  SIG --> VR[vendor_risk count]
  SIG --> GTM[gtm → opportunity_score]
  SIG --> EXEC[executive_summary → summary text]
```

## Intelligence explorer (RAG)

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Loading: user submits question
  Loading --> Success: POST /rag/ask 200
  Loading --> Unavailable: 404/502
  Unavailable --> Idle: show Kai Zhe message
  Success --> Idle
```

## Theme workflow

```mermaid
flowchart LR
  load[page load] --> read[read theme-store / system]
  read --> apply[set html class dark|light]
  toggle[ThemeToggle click] --> persist[persist preference]
  persist --> apply
```

## Build & deploy workflow

```mermaid
flowchart TD
  dev[npm run dev] --> local[:3000 → API :4000]
  ci[GitHub Actions npm run build] --> artifact[.next standalone]
  docker[Docker build with ARG NEXT_PUBLIC_*] --> compose[compose frontend :4002]
```

## Error handling convention

Pages should catch `ApiError` and use `getApiErrorMessage()` for display. Empty arrays are valid for list UIs; distinguish “no data yet” vs “service down”.
