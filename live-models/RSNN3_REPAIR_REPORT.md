# RSNN-3 Repair Report

Date: 2026-11-21

## Outcome

RSNN-3 now admits neutral technical knowledge, retains it across processes, recalls it through its existing IALA/RTA and RSL paths, injects selected learned representations into later cognition, executes evolved recursive weights in its forward computation, persists the dynamic owners of learned tensors, and resumes the same native LQT model state after restart.

This repair edits the supplied implementation directly. Historical `rosemary` module and directory names remain where the existing RSNN-3 runtime imports them; they were not treated as the identity or purpose of the system.

## Root failures repaired

1. `EthicalLearningFilter` treated the absence of ethical keywords as negative evidence. Ordinary technical passages therefore received zero acceptance and IALA rejected them all. Neutral content now receives the configured neutral prior; explicit ethical valence still modulates admission and breath controls learning intensity.
2. Re-observing content recreated its recursive weight and erased evolved state. Content hashes are now idempotent entity identities.
3. Orthogonal representations were classified as contradictions. Structural contradiction now requires directional opposition rather than mere dissimilarity.
4. Autonomous acquisition manufactured a sentence claiming that knowledge had been acquired. It now selects an unseen, attributed passage from the configured local corpus and sends that passage through the same learning pipeline.
5. Learned IALA representations existed beside cognition. RTA-selected entities now enter the existing attention organ and measurably affect processed thought.
6. Cognitive recursive weights accumulated in the registry but no forward path executed them. The existing recursive-weight formulation now runs against the thought encoder's existing row bank and modulates encoded thought.
7. Knowledge graph identity, beliefs, relationships, learning history, filter state, cycle index, RWA owners, evolution owners, and lazily-created effective-weight state were incomplete across reload. The unified LQT stack metadata now rebuilds those owners before stored tensors are applied.
8. Runtime training and chat used divergent reconstruction logic. They now share the same identity reconstruction implementation.
9. The motivation subsystem could create state after checkpoint enumeration. The loop now drains its formation threads before observing, syncing, or saving state.
10. Rollback restored float tensors but not IALA graph identity. Interactive turns now snapshot and restore the corresponding non-tensor learning identity as well.
11. Knowledge admitted through the graph could bypass the existing memory attempt, and important `.rw` content could bypass the graph. All admitted knowledge now remains visible to cognition while preserving the existing RWA and memory routes.
12. The chat transcript and `--json` output omitted the detailed learning/influence record. They now retain the record needed to inspect what RSNN-3 actually changed and used.

## Clean release run

Run: `runtime/runs/rsnn3_release_seed1`

- Requested/completed cycles: 140 / 140
- IALA successful admissions: 140 / 140
- Final knowledge entities: 418
- Final Bayesian belief states: 406
- Later steps using learned knowledge: 139 / 140 (the first step has nothing prior to recall)
- Steps executing recursive cognitive weights: 140 / 140
- IALA phases exercised: INHALE, PAUSE_RISING, HOLD, EXHALE, PAUSE_FALLING, REST, DREAM
- Native unified tensors saved and reloaded: 3,866
- Native edit-log entries: 6,595
- Edit-log verification: true
- Reload name mismatches: 0
- Reload missing/non-equal tensors: 0
- Reload equality: exact
- One-step rollback: exact, edit log valid
- Five-step rollback: exact, edit log valid

The release run used the native C++ LQT backend compiled from the supplied source. `model.lqt`, `metrics.jsonl`, `run.json`, live hashes, plots, checkpoints, and logs are included in the runtime archive.

## Supplied-checkpoint recovery run

The supplied `2026-11-21_unified_seed0_r2/model.lqt` was copied into `runtime/runs/rsnn3_recovered/model.lqt` and continued rather than overwritten in place.

The recovered model:

- accepted a neutral sensor-calibration statement through IALA;
- saved it into the unified live model;
- reloaded in a separate process;
- recalled the statement through both IALA and RSL when asked how the sensor converts voltage to temperature;
- completed the full seven-phase breath sequence with REST MRC enabled;
- reached DREAM and continued into the next cycle;
- finished with a valid native edit-log chain.

## Scope that remains explicit

The repository's native language generation head still emits fixed/template sentences. The chat surface therefore reports recalled learned content plus computed internal state. This repair did not fabricate a text generator or attach an external LLM. RSNN-3's demonstrated result here is executable continual acquisition, retained and recalled knowledge, learned-state influence on subsequent computation, recursive weight execution, self-modifying native persistence, exact reload, and exact rollback.

## Run

From the extracted repository root:

```sh
python -m runtime.chat --model runtime/runs/rsnn3_recovered/model.lqt
```

Continue the clean release model:

```sh
python -m runtime.train --steps 14 --seed 1 --out runtime/runs/rsnn3_release_seed1 --overwrite
```

The included native module targets CPython 3.12 on Linux x86-64. Rebuild it with the commands in `CHAT.md` on another Python/platform combination.
