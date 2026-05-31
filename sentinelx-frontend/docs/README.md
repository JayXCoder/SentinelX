# Frontend documentation

**Owners:** Raymond (marketing) · Geng Xin (dashboard) · **Package:** `sentinelx-frontend`

## Documentation requirement

All UI routes, API integrations, state stores, and user-visible behavior must be documented in this folder **before or with** the code change.

Required coverage:

- **Architecture** — App Router structure, layout shells, design system
- **API integration** — every `apiClient` call, env vars, fallbacks
- **Workflows** — page load, navigation, theme, error states (Mermaid)
- **Routes** — URL map and data dependencies per page

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | Next.js layout, components, styling |
| [design-system.md](design-system.md) | Colors, typography, spacing, accessibility |
| [components.md](components.md) | Reusable component catalog and guidelines |
| [api-integration.md](api-integration.md) | Backend and intelligence HTTP usage |
| [workflow.md](workflow.md) | User and data-fetch flows |
| [routes-and-pages.md](routes-and-pages.md) | Route catalog |

Platform: [../../docs/platform-workflow.md](../../docs/platform-workflow.md) · Specs: [../../docs/sentinelx_task_raymond.md](../../docs/sentinelx_task_raymond.md), [../../docs/sentinelx_task_geng_xin.md](../../docs/sentinelx_task_geng_xin.md)
