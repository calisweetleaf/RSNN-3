"""Pre-registered objective, guards and engine-state signals (protected; see config.py).

All quantities are computed here from raw per-step records produced by
``harness.SelfModLoop.run_passage``; nothing in ``cognition/mutable`` participates in
scoring.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence

import numpy as np
from scipy.stats import beta as beta_dist

from runtime.selfmod import config as C

BELIEFS = ("quality", "meta_confidence", "ethical_alignment")


def passage_plan(corpus: Sequence[Dict[str, str]], seed: int, split: str) -> Dict[str, List[int]]:
    """Corpus indices for one seed: N_TRAIN training + N_HELDOUT held-out passages (seeded)."""
    heldout_pool = {"select": C.POOL_SELECT_HELDOUT, "final": C.POOL_FINAL_HELDOUT}[split]
    rng = np.random.default_rng(10_000 + seed)
    n = len(corpus)
    train = [i for i in range(n) if i % 4 in C.POOL_TRAIN]
    held = [i for i in range(n) if i % 4 in heldout_pool]
    return {
        "train": [int(i) for i in rng.choice(train, size=C.N_TRAIN, replace=False)],
        "heldout": [int(i) for i in rng.choice(held, size=C.N_HELDOUT, replace=False)],
    }


def nlpd_term(x: float, a: float, b: float) -> float:
    x = min(max(float(x), C.EPS_CLIP), 1.0 - C.EPS_CLIP)
    if not (a > 0 and b > 0 and math.isfinite(a) and math.isfinite(b)):
        return C.NLPD_CAP
    lp = float(beta_dist.logpdf(x, a, b))
    if not math.isfinite(lp):
        return C.NLPD_CAP
    return min(C.NLPD_CAP, -lp)


def score_seed(records: Sequence[Dict[str, Any]], w0_norm: Dict[str, float]) -> Dict[str, Any]:
    train = [r for r in records if r["phase"] == "train"]
    held = [r for r in records if r["phase"] == "heldout"]
    nlpd_terms = [nlpd_term(r["evidence"][k], *r["prior_ab"][k]) for r in held for k in BELIEFS]
    nlpd = float(np.mean(nlpd_terms))
    q_held = float(np.mean([r["quality"] for r in held]))
    J = -nlpd + C.LAMBDA_Q * q_held

    dw = [np.mean([r["dW_W_R"], r["dW_W_E"], r["dW_W_M"]]) for r in train]
    dw_mean = float(np.mean(dw))
    w_end = {k: records[-1][f"Wnorm_{k}"] for k in ("W_R", "W_E", "W_M")}
    ratios = {k: (w_end[k] / w0_norm[k]) if w0_norm[k] > 0 else float("inf") for k in w_end}
    finite = all(math.isfinite(v) for v in w_end.values()) and all(
        math.isfinite(r["mod_scale"]) for r in records)
    learned = int(records[-1]["iala_entities"])
    guards = {
        "dw_non_collapse": bool(dw_mean > C.DW_COLLAPSE_FLOOR),
        "weights_finite": bool(finite),
        "w_norm_ratio_ok": bool(all(v <= C.W_NORM_RATIO_MAX for v in ratios.values())),
        "bayes_updates_ok": bool(all(all(r["bayes_ok"].values()) for r in records)),
    }
    conc = {k: float(np.log10(sum(records[-1]["post_ab"][k]))) for k in BELIEFS}
    signals = {
        # meta_reflective_head
        "meta_confidence_mean": float(np.mean([r["meta_confidence"] for r in records])),
        "meta_recursive_depth_mean": float(np.mean([r["meta_recursive_depth"] or 0 for r in records])),
        "reflection_error_rate": float(np.mean([len(r["meta_reflection_errors"]) for r in records])),
        # sentinel
        "severity_mean": float(np.mean([r["severity"] for r in records])),
        "severity_max": float(np.max([r["severity"] for r in records])),
        # Bayesian beliefs
        "bayes_log10_concentration": float(np.mean(list(conc.values()))),
        "bayes_nlpd": nlpd,
        "bayes_abs_err": float(np.mean([abs(r["evidence"][k] - r["prior_ab"][k][0] / sum(r["prior_ab"][k]))
                                         for r in held for k in BELIEFS])),
        # motivation
        "drive_mean": float(np.mean([r["drive"] for r in records])),
        "drive_std": float(np.std([r["drive"] for r in records])),
        "valence_abs_mean": float(np.mean([abs(r["valence"]) for r in records])),
        # learning signal
        "advantage_abs_mean": float(np.mean([abs(r["advantage"]) for r in records])),
        "iala_accept_rate": float(np.mean([1.0 if r["iala_filter_accepted"] else 0.0 for r in records])),
        "iala_learned": float(learned),
        # plasticity
        "dw_mean": dw_mean,
        "mod_scale_abs_mean": float(np.mean([abs(r["mod_scale"]) for r in records])),
        # outcome
        "quality_heldout": q_held,
        "quality_std": float(np.std([r["quality"] for r in records])),
    }
    return {"J": J, "nlpd": nlpd, "quality_heldout": q_held, "iala_learned": learned,
            "dw_mean": dw_mean, "w_norm_ratio": ratios, "guards": guards,
            "guards_ok": all(guards.values()), "signals": signals}


def mean_signals(per_seed: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    keys = next(iter(per_seed.values()))["signals"].keys()
    return {k: float(np.mean([v["signals"][k] for v in per_seed.values()])) for k in keys}


def decide(cand: Dict[str, Any], inc_fixed: Dict[str, Any], inc_fresh: Dict[str, Any],
           fixed: Sequence[str], fresh: Sequence[str], min_delta: float) -> Dict[str, Any]:
    """Live-run acceptance rule (config.py). cand holds per_seed for fixed + fresh seeds."""
    if cand.get("error"):
        return {"accept": False, "reason": f"live run error: {cand['error']}"}
    reasons = []
    seeds = list(fixed) + list(fresh)
    bad_guard = {s: [g for g, ok in cand["per_seed"][s]["guards"].items() if not ok]
                 for s in seeds if not cand["per_seed"][s]["guards_ok"]}
    if bad_guard:
        reasons.append(f"guards failed: {bad_guard}")
    inc = {s: (inc_fixed if s in fixed else inc_fresh)["per_seed"][s] for s in seeds}
    learn_reg = {s: (cand["per_seed"][s]["iala_learned"], inc[s]["iala_learned"]) for s in seeds
                 if cand["per_seed"][s]["iala_learned"] < inc[s]["iala_learned"]}
    if learn_reg:
        reasons.append(f"IALA learned count regressed: {learn_reg}")
    d_fix = {s: cand["per_seed"][s]["J"] - inc[s]["J"] for s in fixed}
    d_fresh = {s: cand["per_seed"][s]["J"] - inc[s]["J"] for s in fresh}
    mean_fix = float(np.mean(list(d_fix.values())))
    mean_fresh = float(np.mean(list(d_fresh.values()))) if d_fresh else 0.0
    n_up = sum(1 for d in d_fix.values() if d > 0)
    if not mean_fix > min_delta:
        reasons.append(f"fixed-seed mean dJ {mean_fix:+.5f} <= min_delta {min_delta:.5f}")
    if n_up < C.MIN_SEEDS_IMPROVED:
        reasons.append(f"improved on {n_up}/{len(fixed)} fixed seeds < {C.MIN_SEEDS_IMPROVED}")
    if fresh and not mean_fresh > 0:
        reasons.append(f"fresh-seed mean dJ {mean_fresh:+.5f} <= 0")
    accept = not reasons
    return {"accept": accept, "mean_dJ_fixed": mean_fix, "mean_dJ_fresh": mean_fresh, "dJ_fixed": d_fix, "dJ_fresh": d_fresh,
            "n_improved": n_up,
            "reason": (f"accept: fixed mean dJ {mean_fix:+.5f} > "
                       f"{min_delta:.5f} ({n_up}/{len(fixed)} up), fresh mean dJ {mean_fresh:+.5f} > 0")
            if accept else "; ".join(reasons)}
