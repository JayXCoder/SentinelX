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
  participant BE as Backend :4000
  participant IN as Intelligence :4001

  U->>R: /dashboard
  R->>S: layout + search/filters
  S->>P: render child route
  P->>BE: signals / health
  P->>IN: analytics / scores / correlation
  BE-->>P: IntelligenceSignal[]
  IN-->>P: scores / events / RAG
  P-->>U: cards / tables / empty state
```

## Overview page data

`getDashboardOverview()` prefers `GET /analytics/overview` on the intelligence service, combined with backend signals for summary text and opportunity score. Falls back to signal-only aggregation if intelligence is unreachable.

## Threat feed filters

```mermaid
flowchart LR
  fetch[getCyberSignals] --> filter[filterSignals store]
  filter --> page[paginate page size 8]
  page --> UI[SignalFeed + Modal]
  search[SearchDialog ?q=] --> filter
```

## Realtime

```mermaid
stateDiagram-v2
  [*] --> TryWS: useRealtimeEvents mount
  TryWS --> Connected: WS /ws open on :4000
  TryWS --> Polling: timeout / error
  Connected --> Polling: socket close
  Polling --> Polling: poll signals every 30s
```

Backend `realtime_listener` tails Redis streams and pushes JSON to all WebSocket clients.

## Intelligence explorer (RAG)

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Loading: POST /rag/ask
  Loading --> Success: 200 + evidence
  Loading --> Error: network / 5xx
  Success --> Idle
  Error --> Idle
```

## Theme workflow

```mermaid
flowchart LR
  load[page load] --> read[read theme-store / system]
  read --> apply[set html class dark|light]
  toggle[ThemeToggle click] --> persist[persist preference]
  persist --> apply
```

## Build & deploy

```mermaid
flowchart TD
  dev[npm run dev] --> local[:3000 → API :4000 + :4001]
  ci[GitHub Actions npm run build] --> artifact[.next]
  docker[Docker ARG NEXT_PUBLIC_*] --> compose[compose frontend :4002]
```

## Error handling

Catch `ApiError` via `getApiErrorMessage()`. Empty arrays mean “no data yet”; intelligence fallbacks avoid hard failures on list pages except RAG (user-facing error).
