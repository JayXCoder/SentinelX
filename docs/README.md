# SentinelX documentation hub

All services in this monorepo **must maintain complete documentation** in their local `docs/` folder. Documentation is not optional: it is part of the definition of done for every feature, API route, worker, and UI surface.

## Documentation standard

Every package (`sentinelx-backend`, `sentinelx-frontend`, `sentinelx-intelligence`) must keep:

| Document | Purpose |
|----------|---------|
| [architecture.md](../sentinelx-backend/docs/architecture.md) (per package) | Components, dependencies, deployment boundaries |
| [api-reference.md](../sentinelx-backend/docs/api-reference.md) | Every HTTP endpoint, query params, request/response shapes |
| [workflow.md](../sentinelx-backend/docs/workflow.md) | End-to-end flows with **Mermaid** sequence/state diagrams |
| [data-model.md](../sentinelx-backend/docs/data-model.md) | Entities, stores, and relationships (where applicable) |

When you add or change code, **update the matching doc in the same PR**. Link new endpoints from the frontend `api-integration.md` and backend `api-reference.md`.

## Platform docs (this folder)

| Document | Description |
|----------|-------------|
| [platform-architecture.md](platform-architecture.md) | Monorepo topology, ports, Docker compose |
| [platform-workflow.md](platform-workflow.md) | Full-stack data and request flows (Mermaid) |
| [master-checklist.md](master-checklist.md) | Team delivery checklist |
| [sentinelx_master.md](sentinelx_master.md) | Product master spec |
| [sentinelx_task_jay.md](sentinelx_task_jay.md) | Backend task spec |
| [sentinelx_task_kai_zhe.md](sentinelx_task_kai_zhe.md) | Intelligence task spec |
| [sentinelx_task_raymond.md](sentinelx_task_raymond.md) | Frontend marketing task spec |
| [sentinelx_task_geng_xin.md](sentinelx_task_geng_xin.md) | Dashboard UI task spec |

## Service documentation

| Package | Docs index |
|---------|------------|
| Backend (Jay) | [sentinelx-backend/docs/README.md](../sentinelx-backend/docs/README.md) |
| Frontend (Raymond + Geng Xin) | [sentinelx-frontend/docs/README.md](../sentinelx-frontend/docs/README.md) |
| Intelligence (Kai Zhe) | [sentinelx-intelligence/docs/README.md](../sentinelx-intelligence/docs/README.md) |

## Mermaid in GitHub

Mermaid blocks in Markdown render on GitHub and in most IDEs. Use `flowchart`, `sequenceDiagram`, and `erDiagram` for architecture and workflows. Keep diagrams next to the prose they explain.
