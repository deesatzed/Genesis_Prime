# Genesis Prime V4 – Runtime Startup Cheatsheet

> Last verified: 2025-06-13 (AIC-ref 0x01)

## 1  Backend API (FastAPI)
```bash
# activate environment
conda activate py13

# free port 8000 (ignore error if nothing bound)
sudo kill -9 $(sudo lsof -t -i:8000) || true

# choose DB (SQLite fallback)
export DATABASE_URL="sqlite+aiosqlite:///./genesis_test.db"

# configure module path for uvicorn
export PYTHONPATH=$PWD/apps/backend:$PYTHONPATH

# start server
uvicorn apps.backend.main:app --host 0.0.0.0 --port 8000
```

Backend available at `http://localhost:8000`.

### New Environment Flags (Phase-2)

| Variable | Purpose | Default |
|----------|---------|---------|
| `PROMPT_VERSION` | Hot-reload prompt pack version (1,2,…) | `1` |
| `METRICS_POLL_MS` | Front-end polling interval for `/metrics` | `5000` |
| `MESSAGE_SCHEMA` | Toggle JSON message schema v2 (`on`\|`off`) | `off` |

### New API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/metrics` | Session token / cost counters |
| `POST` | `/metrics/reset` | Reset counters & rotate session id |
| `GET`  | `/agents` | List active agents (light summary) |
| `GET`  | `/agents/{id}/prompt` | Return current prompt (dev-tool) |

All new routes are CORS-enabled and require no auth in local dev.

---

## 2  Frontend Dashboard (Next-js)
```bash
# one-time install
cd apps/frontend
pnpm install

# allow required post-install scripts (Prisma, Tailwind, sharp, etc.)
pnpm approve-builds @prisma/client @prisma/engines @tailwindcss/oxide esbuild prisma sharp unrs-resolver

# run dev server on port 3001
pnpm run dev -p 3001   # or  pnpm build && pnpm start -p 3001 for prod build
```

Dashboard served at `http://localhost:3001` and expects the backend at port 8000.

---

## 3  Troubleshooting Quick Notes
* If build scripts are re-blocked, rerun `pnpm approve-builds …`.
* Use `pnpm dev -p <port>` to bind to a different port.
* Environment variables can be placed in `.env.local` (Next) and `.env` (backend) for convenience.
