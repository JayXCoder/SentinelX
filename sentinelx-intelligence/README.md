# SentinelX Intelligence Layer (Kai Zhe)

Correlation engine, risk scoring, knowledge graph, and RAG memory.

## Documentation (required)

As this service moves from scaffold to implementation, **every module and endpoint must be documented** before merge.

| Doc | Contents |
|-----|----------|
| [docs/README.md](docs/README.md) | Index and standards |
| [docs/architecture.md](docs/architecture.md) | Target system design (Mermaid) |
| [docs/api-reference.md](docs/api-reference.md) | REST catalog (mark ✅ when live) |
| [docs/workflow.md](docs/workflow.md) | Correlation, scoring, RAG flows |
| [docs/integration.md](docs/integration.md) | Contract with Jay's signal export |

Task spec: [../docs/sentinelx_task_kai_zhe.md](../docs/sentinelx_task_kai_zhe.md)

**Rule:** Implement API → update `docs/api-reference.md` + flip status from ☐ to ✅.

## Scaffold status

Folder structure is scaffolded. Implementation is owned by Kai Zhe.

```bash
docker compose --profile intelligence up -d --build
```

Host port **4001** when the service is ready.
