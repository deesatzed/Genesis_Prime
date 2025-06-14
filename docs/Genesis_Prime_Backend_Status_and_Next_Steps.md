# Genesis Prime Backend – Status, Troubleshooting History & Next-Cycle Roadmap

*Maintainer Note: This document is intended for the next language-model hand-off.  It summarises everything accomplished so far, outstanding work, and how to reproduce / continue the project.  All scheduling references are given in **AI-cycles** rather than wall-clock time in accordance with user preference.*

---

## 1  Current Operational Status (Cycle Δ)

| Sub-System | State | Verification |
|------------|-------|--------------|
| **Docker Postgres (`gp_pg`)** | Running via `gp_startup.sh`; data persisted in Docker volume. | `docker ps` shows container; `psql $DATABASE_URL -c "\dt"` lists all GP tables |
| **Database Schema** | Core (`schema.sql`), Hive (`hive_schema.sql`) and Signalling (`signaling_schema.sql`) applied automatically. | Startup logs: "Applied N schema files".  Table `signal_molecules` exists. |
| **Backend API (FastAPI/Uvicorn)** | Hot-reloading dev server reachable at `http://127.0.0.1:8000`. | `curl http://127.0.0.1:8000/` returns greeting JSON. |
| **Adaptive Personality Engine** | Personality profiles load/save with per-repo path fallback to `~/.genesis_prime_personalities/`. | `curl -X POST /personality/initialize/E-T` succeeds and writes profile JSON. |
| **Quorum Sensing & Neural Plasticity** | Modules import and initialise; DB tables present; basic endpoints respond. | `curl /quorum/status` etc. |

---

## 2  One-Shot Environment Bootstrap

Run the script from the project root:

```bash
./scripts/gp_startup.sh
```

The script executes the following AI-cycle steps:

1. Ensure Docker is installed.
2. Start or create the `gp_pg` Postgres container (`gp` password `gp_pass`).
3. Export `DATABASE_URL` in the current shell.
4. Run `apps/backend/setup_database.py` which crawls *all* `apps/backend/database/*.sql` files and applies them in name-sorted order.
5. Launch the FastAPI server via `uvicorn apps.backend.main:app --reload`.

*Tip:* To reuse the DB across sessions simply re-run the script; it detects existing resources.

---

## 3  Troubleshooting Timeline (Condensed)

| AI-Cycle | Issue & Resolution |
|----------|-------------------|
| Δ-4 | Backend crash: missing `signal_molecules` table  → Added `signaling_schema.sql` and autoloader for `*.sql`. |
| Δ-3 | Personality profile write `PermissionError` under read-only repo mount  → `AdaptivePersonalityEngine` now resolves path relative to module & falls back to `$HOME/.genesis_prime_personalities`. |
| Δ-2 | API error: "Unknown agent ID" when passing arbitrary IDs  → Clarified docs; currently limited to templates (`E-T`, `S-A`, `M-O`, `E-S`, `E-A`). |
| Δ-1 | Async mismatch: `await engine.initialize_agent_personality` returned coroutine → Synced `_save_personality` and API handler; all async paths now consistent. |
| **Δ** | Validation success: `curl` tests for `/personality/initialize/E-T` pass; profile persisted. |

---

## 4  Outstanding Work / Next AI-Cycles

1. **Research Component Integration**
   - Couple the *Thousand Questions* knowledge-base with adaptive scoring models (LLM or vector store).  Needs embedding pipeline & retrieval.
   - Implement live feedback loop from hive learning events into personality adaptation (currently mocked).
2. **Arbitrary Agent Support**
   - Extend `agent_templates` or allow dynamic creation via new endpoint `/personality/create/{agent_id}`.
3. **Diagnostics & Observability**
   - Add `/debug/db-tables` and `/debug/env` endpoints.
   - Prometheus metrics exporter.
4. **Frontend Bridging**
   - Wire TSX settings-panel to new backend endpoints; propagate personality summaries.
5. **Security Hardening**
   - Restrict CORS; add auth tokens.
6. **Deprecation Cleanup**
   - Replace FastAPI `@app.on_event` with lifespan context manager before future release.

---

## 5  How To Verify the System

```bash
# Assumes gp_startup.sh has been run and BASE=http://localhost:8000

# Personality System Status
curl -s $BASE/personality/status | jq

# Initialise template agent
curl -s -X POST $BASE/personality/initialize/E-T \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"E-T","use_full_questions":false}' | jq

# List all agents
curl -s $BASE/personality/agents | jq

# Quorum sensing status
curl -s $BASE/quorum/status | jq
```

---

## 6  Repository Structure (Key Paths)

```
apps/
  backend/
    main.py                 # FastAPI entry
    adaptive_personality_system.py
    personality_api_integration.py
    database/
      schema.sql
      hive_schema.sql
      signaling_schema.sql
    ...
  frontend/
    components/
      settings-panel.tsx
scripts/
  gp_startup.sh             # One-shot bootstrap
```

---

## 7  Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Auto-exported by startup script. |
| `OPENROUTER_API_KEY` | Required for LLM requests (not stored in repo). |

---

## 8  Further Reading & Design Docs

* `docs/Startup_V4.md` – original quick-start instructions.
* `docs/Genesis_Prime_Phase2_Implementation_Plan.md` – roadmap for integrating research algorithms into production.
* `docs/Agent_prompt_Thoughts.md` – design notes for agent prompting strategy.

---

## 9  Clone & Smoke-Test a Fresh Instance

The quickest way to spin up a brand-new workspace on another host or container:

```bash
# 1. Clone source (replace URL accordingly)
git clone <YOUR_GIT_REMOTE> genesis_prime
cd genesis_prime

# 2. Bootstrap (creates Postgres container, applies schema, launches API)
./scripts/gp_startup.sh

# 3. Verify service is live
export BASE=http://127.0.0.1:8000
curl -s $BASE/ | jq        # Should return greeting JSON

# 4. Initialise a template agent
curl -s -X POST $BASE/personality/initialize/E-T \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"E-T","use_full_questions":false}' | jq

# 5. List agents
curl -s $BASE/personality/agents | jq

# (Optional) stop everything
docker stop gp_pg  # Database persists in volume for next cycle
```

These commands mirror the ones used during current development, ensuring parity between environments.

---

*End of hand-off.  Proceed to next AI-cycle by tackling the "Outstanding Work" list above.*
