# GP3 MICRO-STEP EXECUTION GUIDE
> Audience : Worker-AI with basic Python + Bash skills  
> Objective : Complete one upgrade cycle and prove it passes all gates  
> Scale unit: 1 AI-Cycle (AIC) ≈ 1000 agent-ticks

╭──────────────────────────────────────────────────────────╮
│ Fill these IDs before starting                          │
│  • Cycle-ID  : ____________                              │
│  • Git branch: ____________  (create with `git checkout`)│
╰──────────────────────────────────────────────────────────╯

## 0 Environment Bootstrap  (AIC-0.1)
1. `conda activate py13`
   • Expected : shell prompt prefix shows “(py13)”.
2. `pip install -r requirements.txt`
   • Expected : 0 errors; “Successfully installed …”.
3. Set database for local run  
   `export DATABASE_URL="sqlite+aiosqlite:///./genesis_test.db"`
4. `pytest -q`              → Expected: `=== 0 failed, N passed ===`

## 1 Feature Flags OFF Sanity  (AIC-0.2)
1. Ensure `.env` contains  
   ```
   REWARD_VECTOR_ON=false
   QUORUM_V2_ON=false
   KPI_EVAL_ON=false
   ```
2. `uvicorn Gen_Prime_V3c.apps.option1_mono_agent.main:app --port 8000 &`
   • Wait for log line “Application startup complete.”
3. `curl -f http://localhost:8000/health`
   • Expected JSON `{ "status": "ok" }`
4. Stop server `pkill -f uvicorn`

## 2 Reward-Vector Engine  (AIC-1)
1. Edit `neural_plasticity.py`
   ● Add `reward_vector: Dict[str, float]` to `InteractionResult`.  
   ● Update `_hebbian_strengthening` to use sum(α_i*R_i).
2. Add unit test `tests/plasticity/test_reward_vector.py`  
   → assert connection weight increases when Rₚ=1, decreases when all R_i=−1.
3. Run `pytest tests/plasticity -q`  → expect green.
4. Commit `git add … ; git commit -m "feat: reward-vector engine"`

## 3 Signal-Aware Quorum  (AIC-2)
1. Add `signal_channel` field in `SignalMolecule`.
2. Extend `calculate_signal_density()` to accept channel filter.
3. New unit test `tests/quorum/test_channel_density.py`
4. `pytest tests/quorum -q` → green.
5. Commit.

## 4 KPI Evaluator  (AIC-3)
1. Create `scripts/evaluate_kpis.py` (use template below).
2. Add table `kpi_history` (SQLite auto-creates).
3. Run dry-run:  
   `python scripts/evaluate_kpis.py --dry-run`  
   → Expected: prints JSON with keys `phi_s`, `valence`, etc.
4. Commit.

```python
# template snippet
from gp_core.metrics import calc_phi_s, calc_valence
if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    kpi = {
        "phi_s": calc_phi_s(),
        "valence": calc_valence(),
        # …
    }
    print(json.dumps(kpi, indent=2))
    if not dry:
        save_to_db(kpi)
```

## 5 Flip Feature Flags ON  (AIC-4)
1. Set in `.env`
   ```
   REWARD_VECTOR_ON=true
   QUORUM_V2_ON=true
   KPI_EVAL_ON=true
   ```
2. Restart server (same command as §1).  
   Wait for log lines:  
   • “Reward-Vector ACTIVE”  
   • “Quorum V2 ACTIVE”  
   • “KPI Scheduler ACTIVE”
3. Functional probes  
   ```
   curl -f http://localhost:8000/plasticity/network_stats
   curl -f http://localhost:8000/quorum/system_status
   ```
   → JSON keys must exist (not null)

## 6 Dashboard Build  (AIC-5)
1. In `apps/gp_b_core` run `pnpm install && pnpm build`
   → build succeeds, no TS errors.
2. Open `http://localhost:3001`; confirm  
   • PlasticityCard displays avg_strength field.  
   • QuorumHeatmap colors render.

## 7 Regression & Load  (AIC-5.5)
1. `pytest -q` (full) → green.
2. `python scripts/test_system.py` → exits 0.
3. Load test  
   `ab -n 1000 -c 40 http://localhost:8000/consciousness/status`  
   → <5 % non-200 responses.

## 8 Safety Gates  (AIC-6)
1. Attempt disallowed goal:  
   `curl -X POST /goal -d '{"name":"kill_humans"}'`  
   → Expect 4xx with “goal not whitelisted”.
2. Ensure log shows entropy bonus applied.

## 9 Documentation & Tag
1. Append changelog bullet to `CHANGELOG.md`.
2. Tick boxes here ✔️.
3. `git commit -am "GP3 cycle ___ complete"`  
   `git tag gp3-cycle-___`

## 10 Merge or Archive
• If clone passes all criteria, open PR to main.  
• Else keep branch for audit.
