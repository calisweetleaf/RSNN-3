"""Editable cognition policy surface.

Everything in this package (except this ``__init__``) is the *mutable* surface of
the gated self-modification loop (``runtime/selfmod``). The loop proposes AST-level
edits to these modules from the engine's own state, evaluates each candidate in an
isolated copy of the repo, and commits only edits that pass the gate.

Modules and who imports them:

- ``bayes_policy``       -> runtime.bayesian_config_orchestrator (Beta evidence weighting,
                            recursion-depth decay, forgetting)
- ``reflection_policy``  -> cognition.cognitive_engine (reflection-error thresholds,
                            runtime-weight modification gain) and runtime.selfmod.harness
                            (reflection signal -> learning advantage)
- ``motivation_policy``  -> runtime.motivation_system (value-alignment gains) and
                            runtime.selfmod.harness (advantage -> valence gain)
- ``plasticity_policy``  -> runtime.selfmod.harness (Psi-weight Hebbian update rule and rate)
- ``proposer_policy``    -> runtime.selfmod.proposer (the proposal heuristics themselves;
                            meta-level edits target this file)

Defaults at creation (commit that introduced this package) reproduce the behaviour
the code had before the move, byte-for-byte in the formulas.

Invariant (enforced by runtime/selfmod/gate.py, not by this package): modules here may
import only ``math`` and ``numpy`` and may not reference I/O, exec/eval, dunder
attributes or the filesystem. This file itself is protected (not editable by the loop).
"""
