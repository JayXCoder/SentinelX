#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Starting SentinelX stack (intelligence + frontend + optional AI)"
docker compose up -d --build postgres redis qdrant api celery_worker celery_beat intelligence_api intel_celery_worker intel_celery_beat frontend

if docker info 2>/dev/null | grep -qi nvidia; then
  echo "==> NVIDIA detected — starting SGLang (Qwen/Qwen3.5-2B)"
  docker compose --profile ai up -d sglang_qwen || true
else
  echo "==> No GPU profile: demo signals work; live agent inference needs: docker compose --profile ai up -d"
fi

echo "==> Waiting for API health..."
for _ in $(seq 1 60); do
  if curl -sf http://localhost:4000/health >/dev/null; then
    break
  fi
  sleep 2
done

echo "==> Waiting for Intelligence API..."
for _ in $(seq 1 60); do
  if curl -sf http://localhost:4001/health >/dev/null; then
    break
  fi
  sleep 2
done

echo "==> Seeding ChamPeng profile..."
docker compose exec -T api python /app/scripts/seed_champeng.py

echo "==> Ingesting signals + correlation (intelligence worker)..."
docker compose exec -T intel_celery_worker celery -A app.workers.celery_app.celery_app call app.workers.correlation_worker.correlate_signals_task >/dev/null 2>&1 || true

echo "==> Knowledge graph + risk scores..."
docker compose exec -T intelligence_api python -c "
import urllib.request
for path, body in [
    ('/graph/rebuild', None),
    ('/risk-scores/recalculate', b'{\"force\": true}'),
]:
    req = urllib.request.Request('http://127.0.0.1:4001'+path, data=body, method='POST',
        headers={'Content-Type':'application/json'} if body else {})
    urllib.request.urlopen(req, timeout=120)
print('graph+risk ok')
" 2>/dev/null || true

echo "==> Indexing RAG vectors (Qdrant)..."
docker compose exec -T intelligence_api python -c "
from app.db.session import SessionLocal
from app.db.models.intelligence_signal import IntelSignal
from app.workers.graph_worker import update_knowledge_graph_task
db = SessionLocal()
ids = [str(s.id) for s in db.query(IntelSignal).all()]
db.close()
if ids:
    print(update_knowledge_graph_task(ids))
" 2>/dev/null || true

echo ""
echo "ChamPeng stack ready:"
echo "  Dashboard:    http://localhost:4002"
echo "  Backend API:  http://localhost:4000/docs"
echo "  Intelligence: http://localhost:4001/docs"
