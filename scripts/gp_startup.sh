#!/usr/bin/env bash
# gp_startup.sh – one-shot bootstrap for Genesis Prime dev instance
# 1. Ensure Docker Postgres container (gp_pg) is running (creates if absent)
# 2. Export DATABASE_URL env var for current shell
# 3. Populate DB schema & questions
# 4. Start FastAPI backend with hot-reload
# Usage: source ./scripts/gp_startup.sh  # keeps env vars in current shell

set -euo pipefail

PG_CONTAINER="gp_pg"
PG_IMAGE="postgres:16"
PG_PORT="5432"
PG_PASSWORD="pass"
PG_DB="sentient"
PG_USER="postgres"

# Detect docker
if ! command -v docker &>/dev/null; then
  echo "❌ Docker is required but not found. Install Docker and retry." >&2
  return 1 2>/dev/null || exit 1
fi

# Create or start container
if ! docker ps -a --format '{{.Names}}' | grep -q "^${PG_CONTAINER}$"; then
  echo "🚀 Creating Postgres container ${PG_CONTAINER}..."
  docker run --name "${PG_CONTAINER}" -e POSTGRES_PASSWORD="${PG_PASSWORD}" \
    -e POSTGRES_DB="${PG_DB}" -p ${PG_PORT}:5432 -d "${PG_IMAGE}"
else
  # Start if not running
  if ! docker ps --format '{{.Names}}' | grep -q "^${PG_CONTAINER}$"; then
    echo "🔄 Starting existing Postgres container ${PG_CONTAINER}..."
    docker start "${PG_CONTAINER}"
  else
    echo "✅ Postgres container ${PG_CONTAINER} already running."
  fi
fi

# Wait until DB is ready
echo "⏳ Waiting for Postgres to accept connections..."
until docker exec -i "${PG_CONTAINER}" pg_isready -U "${PG_USER}" -d "${PG_DB}" >/dev/null 2>&1; do
  sleep 1
done
echo "🟢 Postgres is ready."

# Export DATABASE_URL for this shell
export DATABASE_URL="postgresql://${PG_USER}:${PG_PASSWORD}@127.0.0.1:${PG_PORT}/${PG_DB}"
echo "📌 DATABASE_URL exported for current shell."

echo "📚 Running Genesis DB setup (schema & questions)..."
python -m apps.backend.setup_database || {
  echo "❌ DB setup failed"; return 1 2>/dev/null || exit 1;
}

echo "🚀 Launching Genesis Prime backend (hot-reload)..."
uvicorn apps.backend.main:app --reload
