# Nginx Proxy Manager (DuckDNS)

SentinelX listens on the **host** (Docker published ports). Point NPM at the machine running `docker compose`, not at container names.

| DuckDNS subdomain | NPM forward to | Purpose |
|-------------------|----------------|--------|
| `sentinelx-web` | `http://<host-ip>:4002` | Next.js UI |
| `sentinelx-websoc` | `http://<host-ip>:4000` | Backend API + WebSocket `/ws` |
| `sentinelx-intel` | `http://<host-ip>:4001` | Intelligence API |

Use **HTTPS** in NPM (Let’s Encrypt). Enable **Websockets Support** on the `sentinelx-websoc` proxy host.

## Router

Forward **80** and **443** to the host running NPM (not 4000–4002 directly unless you skip NPM).

## NPM proxy host settings

### sentinelx-web.duckdns.org

- Domain: `sentinelx-web.duckdns.org`
- Scheme: `http`
- Forward hostname / IP: LAN IP of Docker host (e.g. `192.168.x.x` or `127.0.0.1` if NPM is on the same box)
- Forward port: `4002`
- SSL: Request certificate, Force SSL
- Websockets: optional (UI uses separate WS host)

### sentinelx-websoc.duckdns.org

- Domain: `sentinelx-websoc.duckdns.org`
- Forward port: `4000`
- SSL: Force SSL
- **Websockets Support: ON** (required for `/ws`)

Custom locations are not required; the backend serves WebSocket at `GET/WS /ws`.

### sentinelx-intel.duckdns.org

- Domain: `sentinelx-intel.duckdns.org`
- Forward port: `4001`
- SSL: Force SSL

The dashboard usually calls intelligence via `https://sentinelx-web.duckdns.org/api/intelligence/*` (Next.js proxy). The `sentinelx-intel` host is for direct API access, tools, and CORS-aligned public URL in `.env`.

## DuckDNS

Create three A records (or one wildcard) pointing to your public IP:

- `sentinelx-web`
- `sentinelx-websoc`
- `sentinelx-intel`

## After NPM is live

```bash
docker compose up -d --build frontend
docker compose up -d api intelligence_api
```

Verify:

```bash
curl -fsS https://sentinelx-web.duckdns.org/
curl -fsS https://sentinelx-intel.duckdns.org/health
curl -fsS https://sentinelx-web.duckdns.org/api/realtime/ws-url
# Expect: {"url":"wss://sentinelx-websoc.duckdns.org/ws..."}
```

## Do not expose publicly

Postgres `4543`, Redis `4637`, Qdrant `4633`, SGLang `4300`.
