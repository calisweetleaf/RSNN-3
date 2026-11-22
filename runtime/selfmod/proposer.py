"""Proposal generator (protected mechanics; heuristics live in cognition/mutable/proposer_policy.py).

Input: the incumbent's engine-state signals (objective.score_seed, mean over selection
seeds), the per-rule reject streaks, the loop detector, and a per-generation RNG.
Output: a proposal dict (module, target, kind, transform args) plus its causal chain:
the signal, its value, the rule's threshold, the rule's score and every competing
rule's score.

Object level (depth 0): rules in proposer_policy.RULES -> edit of an object module.
Meta level (depth 1): when a rule has been rejected META_TRIGGER_REJECTS times in a row,
the proposal is an edit of proposer_policy itself (soften the rule's step, move its
threshold, or down-weight it). The runner then re-runs the *edited* proposer_policy on
the same signals to obtain the object edit that is evaluated with it; both are
accepted or rejected together (the meta edit is judged by the object improvement it
produces). config.MAX_META_DEPTH = 1: a meta proposal never spawns another meta edit.
"""

from __future__ import annotations

import ast
import importlib.util
import math
import random
import types
from typing import Any, Dict, List, Optional, Tuple

from runtime.selfmod import ast_edit
from runtime.selfmod import config as C


def load_policy_from_source(src: str) -> types.ModuleType:
    """Execute proposer_policy source (already passed gate.scan_module) as a module."""
    mod = types.ModuleType("proposer_policy_candidate")
    exec(compile(src, "proposer_policy.py", "exec"), mod.__dict__)
    return mod


def _rule_const(pol, name: Optional[str], default: float = 1.0) -> float:
    return float(getattr(pol, name)) if name else default


def score_rules(pol, signals: Dict[str, float], streaks: Dict[str, int], detector, gen: int) -> List[Dict[str, Any]]:
    scored = []
    for rule in pol.RULES:
        value = float(signals.get(rule["signal"], float("nan")))
        thr = _rule_const(pol, rule["thr"])
        if math.isnan(value):
            continue
        s = float(pol.rule_score(_rule_const(pol, rule["weight"]), value, rule["cmp"], thr,
                                 streaks.get(rule["name"], 0)))
        probe = {"module": rule["module"], "target": rule["target"], "kind": rule["kind"],
                 "factor": _rule_const(pol, rule.get("step")) if rule["kind"] == "const_scale" else 1.0,
                 "delta": _rule_const(pol, rule.get("step")), "coef": _rule_const(pol, rule.get("step")),
                 "old": rule.get("old"), "new": rule.get("new"), "index": rule.get("index")}
        blocked = detector.is_blocked(probe, gen)
        scored.append({"rule": rule["name"], "signal": rule["signal"], "value": value, "cmp": rule["cmp"],
                       "thr": thr, "score": s, "blocked": blocked})
    return scored


def object_proposal(pol, signals, streaks, detector, gen: int, rng: random.Random,
                    sources: Dict[str, str], exclude=()) -> Dict[str, Any]:
    """exclude: 'module.target' keys not to propose (none by default)."""
    scored = score_rules(pol, signals, streaks, detector, gen)
    rule_key = {r["name"]: f'{r["module"]}.{r["target"]}' for r in pol.RULES}
    live = [s for s in scored if s["score"] > 0 and not s["blocked"] and rule_key[s["rule"]] not in exclude]
    chain: Dict[str, Any] = {"scores": scored}
    if live:
        live.sort(key=lambda s: -s["score"])
        if rng.random() < float(pol.EXPLORATION) and len(live) > 1:
            pick = rng.choice(live[1:])
            chain["selection"] = "exploration (EXPLORATION draw) among triggered rules"
        else:
            pick = live[0]
            chain["selection"] = "argmax score"
        rule = next(r for r in pol.RULES if r["name"] == pick["rule"])
        chain["trigger"] = {k: pick[k] for k in ("rule", "signal", "value", "cmp", "thr", "score")}
        p = {"module": rule["module"], "target": rule["target"], "kind": rule["kind"], "rule": rule["name"]}
        jitter = 1.0 + rng.uniform(-float(pol.STEP_JITTER), float(pol.STEP_JITTER))
        step = _rule_const(pol, rule.get("step")) if rule.get("step") else None
        if rule["kind"] == "const_scale":
            p["factor"] = float(step) ** jitter
        elif rule["kind"] == "const_add":
            p["delta"] = float(step) * jitter
        elif rule["kind"] == "insert_term":
            p["arg"] = rule["arg"]
            p["coef"] = float(step) * jitter
        elif rule["kind"] == "swap_call":
            p["old"], p["new"] = rule["old"], rule["new"]
        elif rule["kind"] == "reorder":
            p["index"] = int(rule["index"])
        return {"proposal": p, "chain": chain}
    # no triggered, unblocked rule: log-normal jitter of one numeric constant (logged as such)
    chain["selection"] = "fallback: no triggered rule; random constant jitter (FALLBACK_SIGMA)"
    choices = []
    for m in C.OBJECT_MODULES:
        for name, v in ast_edit.numeric_constants(sources[f"{C.ALLOWED_EDIT_PREFIX}{m}.py"]).items():
            if v != 0.0 and f"{m}.{name}" not in exclude:
                choices.append((m, name))
    m, name = rng.choice(sorted(choices))
    p = {"module": m, "target": name, "kind": "const_scale", "rule": "fallback_jitter",
         "factor": math.exp(rng.gauss(0.0, float(pol.FALLBACK_SIGMA)))}
    return {"proposal": p, "chain": chain}


META_ACTIONS = ("soften_step", "move_threshold", "down_weight")


def meta_proposal(pol, rule_name: str, n_prior_meta: int, signals: Dict[str, float]) -> Optional[Dict[str, Any]]:
    """Edit of proposer_policy for a rule that keeps being rejected."""
    rule = next((r for r in pol.RULES if r["name"] == rule_name), None)
    if rule is None:
        return None
    order = [a for a in META_ACTIONS if not (a == "soften_step" and not rule.get("step"))]
    action = order[n_prior_meta % len(order)]
    p = {"module": "proposer_policy", "kind": "const_scale", "rule": f"meta:{action}:{rule_name}", "meta_action": action}
    if action == "soften_step":
        cur = float(getattr(pol, rule["step"]))
        p["target"] = rule["step"]
        if rule["kind"] == "const_scale" and cur > 0:
            # step -> step ** META_SOFTEN (toward the no-op factor 1), as a scale edit
            p["factor"] = cur ** (float(pol.META_SOFTEN) - 1.0)
        else:
            p["factor"] = float(pol.META_SOFTEN)
    elif action == "move_threshold":
        # move the threshold past the current signal so the rule fires less eagerly
        p["target"] = rule["thr"]
        f = float(pol.META_THR_FACTOR)
        p["factor"] = f if rule["cmp"] == ">" else 1.0 / f
    else:
        p["target"] = rule["weight"]
        p["factor"] = float(pol.META_WEIGHT_FACTOR)
    return p

