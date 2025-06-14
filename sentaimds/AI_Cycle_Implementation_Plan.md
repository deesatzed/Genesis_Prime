# Genesis Prime – Short-Term High-Leverage Implementation Plan (AI-Cycle Format)

> Scale unit: **1 AI-Cycle (AIC) ≈ 1000 coordinated agent-ticks**  
> • On local hardware, an AIC completes in ~5–7 wall-clock minutes (for reference only).  
> • Multiple cycles may execute in parallel shards; the sequence below represents logical ordering, **not** elapsed human time.

| Cycle | Deliverable | Rationale | Key Tasks |
|-------|-------------|-----------|-----------|
| **AIC-0  (System Hardening)** | • SQLite fallback logic<br>• `/health` endpoint | Ensure every agent-cluster boots without external DB. | 1. Add dynamic `database_router` to settings.<br>2. Implement `@app.get("/health")` returning 200 + version.<br>3. Unit-test: boot with missing Postgres – expect pass. |
| **AIC-1  (Reward-Vector Engine)** | • `reward_vector` (⟨Rₚ, R꜀, Rₛ, Rₑ⟩) integrated into Neural-Plasticity | Higher-bandwidth learning signal. | 1. Extend `InteractionResult` schema.<br>2. Modify weight update to `Δw = Σ_i α_i·R_i`.<br>3. Persist vector to `learning_history`. |
| **AIC-2  (Signal-Aware Quorum)** | • Quorum density tracked per reward channel<br>• Behaviour trigger on channel deterioration | Links affective feedback to emergent behaviours. | 1. Add `signal_channel` to `SignalMolecule`.<br>2. Update `_check_quorum_thresholds` to inspect per-channel densities.<br>3. Integration-test with synthetic signals. |
| **AIC-3  (KPI Evaluator v0)** | • Script `evaluate_kpis.py` + scheduler<br>• `/consciousness/kpi_history` API | Objective consciousness metrics feed UI & governance. | 1. Mock Φₛ, Φ𝚌, Valence-Coherence, Self-Repair, ToM-Acc.<br>2. Write to `kpi_history` (SQLite/Postgres).<br>3. Expose REST endpoint with pagination. |
| **AIC-4  (Frontend Widgets)** | • Dashboard components: `PlasticityCard`, `QuorumHeatmap`, `KpiTrend` | Visualises new data for overseers. | 1. `api.ts` hooks `getPlasticityStats`, `getQuorumStatus`, `getKpiHistory`.<br>2. Build components with Tailwind + Recharts.<br>3. Wrap in SWR auto-refresh every 0.2 AIC. |
| **AIC-5  (Risk Guardrails v1)** | • Entropy regulariser in plasticity<br>• Goal-whitelist enforcement | Closes highest-priority safety gaps early. | 1. Compute entropy of reward vector; add bonus term.<br>2. YAML goal whitelist in `ThemisCore`, assert pre-action.<br>3. Canary tests: reject disallowed goal. |

---

## Success Metrics (evaluate at the end of AIC-5)

Metric | Target
-------|--------
Plasticity avg strength Δ | +15 % vs baseline
Distinct quorum behaviours | ≥ 2
KPI card fields populated | ≥ 4 metrics with trendline
Dashboard latency | < 0.1 AIC (95-percentile)
Mode-collapse events | 0

---

## Execution Notes

1. **Parallelism** – Agent shards may run cycles out-of-order; guard via feature flags.
2. **Rollback** – Each deliverable must include migration-safe toggles.
3. **Audit hooks** – Emit provenance hash per cycle for reproducibility.
