"""Gated self-modification loop (lane selfmod-loop).

The cognitive engine's tunable policy lives in ``cognition/mutable``. This package
proposes AST-level edits to that surface from the engine's own state, evaluates each
candidate in an isolated copy of the repo under a pre-registered objective, and lets
the loop commit only the edits that pass the gate.

Everything in this package (gate, live-run evaluator, objective, runner, loop detector)
is protected: the gate refuses any candidate that changes a file here.
"""
