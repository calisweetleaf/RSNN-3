# Self-modification gate: pre-registration (live-run gate)

Committed before the first generation ran. Numbers: `runtime/selfmod/config.py`. The
baseline replicate noise and the resulting `min_delta` are written to the run's
`run.json` (`replicate_max_abs_dJ`, `min_delta`, `preregistered_at`) before any candidate
is evaluated.

Operator rules (Daeron, 2026-11-21): no test code; the gate is the running system itself
(apply the edit, run the live cognition loop on fixed and fresh seeds, keep the edit only
if the system's own metrics improve). Weight/param edits land on model.lqt via
lqt-unify's API (not posted when this was frozen; each accepted generation records that).

## The system's metric (per seed, computed by protected code: `objective.py`)
`J = -NLPD_heldout + 10 * reflection_quality_heldout`

- A seed = one live run of the cognition loop (`harness.SelfModLoop` = runtime/loop.py
  `RSILoop` with its tunable formulas read from `cognition/mutable`): CognitiveEngine
  (TriaxialBackbone on LQT-stored Psi weights, MetaReflectiveOutputHead) -> SECT sentinel
  -> Bayesian beliefs -> motivation -> IALA learn_from_text + training cycle -> Psi
  self-modification quantized into the LQT store; 12 training + 10 held-out passages.
- `NLPD_heldout`: prequential `-log Beta(x | a, b)` of each held-out evidence value under
  the belief before its update (3 beliefs, clip 1e-3, cap 50 per term).
- `reflection_quality_heldout`: mean engine quality_score on held-out passages.

## Acceptance (one edit per generation)
Live runs: candidate on fixed seeds 0-4 + two fresh seeds unique to the generation;
incumbent on the same fresh seeds. Keep iff
1. mean fixed-seed dJ > min_delta (= max(0.01, 3 x baseline replicate max |dJ|)) and
   dJ > 0 on >= 4 of 5 fixed seeds,
2. mean fresh-seed dJ > 0,
3. run health on every seed: mean |dW| > 1e-12, finite weights, ||W_end||/||W_0|| <= 10,
   all Bayesian updates succeeded, IALA learned count not below the incumbent's,
4. invariants I1-I3 (gate.py) hold.

## Final report
Base-commit policy surface vs final selected surface, live runs on 8 fresh seeds
(1000-1007) with the final held-out passage pool, never used during selection.

## Protected (not editable by the loop)
runtime/selfmod/** (gate, evaluator, objective, config, proposer mechanics, RLDIS detector,
runner), cognition/mutable/__init__.py, the IALA ethics-filter setting
(`config.IALA_FILTER`), all engine/runtime code outside cognition/mutable.

Theory: URSMIF v1.5 2.1.1-2.1.2, 3.4; RLDIS v1.1 2.3, 3.1.2; Eigenrecursion 4.2.1, 5.2,
5.3; RBUS 3.1.1.
