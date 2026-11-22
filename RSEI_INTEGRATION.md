# RSNN-3 RSEI Capability Incentive

Date: 2026-11-21

## What is integrated

`runtime/rsei_incentive.py` connects the supplied RSEI incentive design to the live RSNN-3 loop. It does not replace the cognitive engine, IALA, motivation, RSL, breath/dream, recursive weights, native voice, or LQT. It observes those organs from outside the cognitive forward path and turns demonstrated behavior into capability evidence.

The implementation retains the parts supported by the supplied verification report:

- capability is the exact count of externally verified reachable competences;
- reward requires strict expansion of the verified set;
- the HAJRA frontier is ranked by `P(success) * gain / cost`, with admission at `I_eff >= 0.80` and a bounded exploration floor;
- reflection quality, confidence, self-description, and generated text cannot certify a competence;
- reward is linear in verified expansion and makes no doubly-exponential growth assumption;
- regression spot checks can remove a competence and apply a negative reward;
- every settlement is appended to a hash-chained capability ledger.

## Live competence DAG

The current graph contains twelve runtime competences: cognitive forward execution, ethical admission, Bayesian update, knowledge acquisition, knowledge recall, recursive-weight application, LQT self-modification, persistent memory, breath coupling, dream integration, native-voice grounding, and multi-source integration. Prerequisites determine the reachable frontier.

`RuntimeCapabilityVerifier` owns the probes. It is not an `nn.Module`, is never passed into `CognitiveEngine`, and consumes only returned runtime records, persistence facts, and voice-training state. This makes the verifier external to the cognition being rewarded while still shipping in the standalone system.

## Dynamic liquid Bayesian parameters

The Bayesian orchestrator can now materialize a Beta belief for any competence selected by the frontier. It is not capped to the three bootstrap parameters. Each new parameter is registered with the existing recursive updater, collected by the live tensor bridge, written to LQT, and reconstructed from stack identity before tensor values are applied after restart.

The live run grew from 3 bootstrap beliefs to 15 total beliefs: one new competence parameter for every node in the DAG.

## Motivation integration

RSEI creates three actual values in the existing motivation system:

1. verified expansion;
2. no regression;
3. external verification.

It also creates an actual goal object for every competence and updates each goal's pending, active, or completed state from the verified set and frontier. `motivation_drive` is the RSEI reward EMA once bound; it is no longer the inert 0.500 no-signal baseline.

## Live-system result

The persisted release model was continued through the real chat/runtime/LQT path for 22 RSEI cycles. It reached 12 of 12 externally verified competences. The first eleven expanded through ordinary live turns. Dream integration correctly remained unverified through repeated zero-score probes, decreasing drive instead of paying itself. After the canon oscillator entered DREAM, advanced, exited, and stored three integrated dream memories, the external probe passed and the final strict expansion was admitted.

- exact verified dimension: 12 / 12
- strict expansions: 12
- dynamic Bayesian parameters: 15 total (3 bootstrap + 12 competences)
- motivation values: 3
- final frontier: 0
- dream memories integrated at final expansion: 3
- LQT edit log: 10,029 entries, chain valid
- live unified tensors after the final turn: 5,388

The observed drive rose from 0.500 to 0.783 during successful expansion, fell on failed dream probes, and recovered when dream integration was externally observed. This is the intended behavior: capability evidence changes motivation; aspiration alone does not.

## Persistence and restart

RSEI verified state, attempts, successes, cost estimates, verifier observations, reward drive, ledger tail, and head hash are saved inside the unified stack. Dynamic Bayesian belief schemas are saved separately from their tensor values so owners exist before LQT restores them. The canon breath coordinate and cycle count are also persisted; this repairs the earlier restart behavior that reset the oscillator and could indefinitely postpone DREAM.

The evidence figure is `visualizations/figures/06_rsei_verified_capability.png`, with SVG alongside it. Its source rows are the real `runtime/runs/rsnn3_release_seed1/chat/transcript.jsonl`; hashes and exact claims are recorded in `visualizations/figures/figure_manifest.json`.
