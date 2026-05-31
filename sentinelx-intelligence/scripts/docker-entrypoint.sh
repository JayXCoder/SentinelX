#!/bin/sh
set -e

echo "Waiting for PostgreSQL at postgres:5432..."
for i in $(seq 1 60); do
  if python -c "import socket; socket.gethostbyname('postgres'); s=socket.create_connection(('postgres', 5432), 2); s.close()" 2>/dev/null; then
    echo "PostgreSQL is reachable."
    break
  fi
  if [ "$i" -eq 60 ]; then
    echo "ERROR: Could not reach postgres after 60 attempts."
    exit 1
  fi
  sleep 2
done

echo "Running intelligence database migrations..."
python /app/scripts/run_migrations.py

echo "Starting Intelligence API on port 4001..."
exec uvicorn app.main:app --host 0.0.0.0 --port 4001
