"""Generation loop of the gated self-modification (protected).

    python -m runtime.selfmod.run --generations 30 --run-dir runtime/runs/2026-11-21_selfmod

Per generation: signals of the incumbent's live runs -> proposal (proposer +
cognition/mutable/proposer_policy; meta edits of proposer_policy at depth 1) -> AST edit
-> RLDIS precheck -> isolated candidate copy of the frozen snapshot -> invariants
(gate I1/I2) -> the live cognition loop runs the candidate on the fixed seeds and this
generation's fresh seeds, and the incumbent on the same fresh seeds (I3) -> keep the
edit only if the system's own metric goes up (objective.decide). On accept the loop
writes the edited cognition/mutable files and commits exactly those paths.
No test code: the gate is the running system (operator rule 2026-11-21).

Outputs in --run-dir: run.json, generations.jsonl, evals/. Scratch under $TMPDIR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from runtime.selfmod import ast_edit, gate, objective, proposer
from runtime.selfmod import config as C
from runtime.selfmod.rldis import LoopDetector, signature

REPO = Path(__file__).resolve().parents[2]


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def git(*args: str, check: bool = True) -> str:
    for attempt in range(10):
        p = subprocess.run(["git", "-C", str(REPO), "-c", "user.name=Hark (selfmod-loop)",
                            "-c", "user.email=hark@users.noreply.github.com", *args], capture_output=True, text=True)
        if p.returncode == 0 or "index.lock" not in (p.stderr or ""):
            if check and p.returncode != 0:
                raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
            return p.stdout.strip()
        time.sleep(1.0 + attempt)
    raise RuntimeError(f"git {' '.join(args)}: index.lock held for >50s")


def surface_hash(sources: Dict[str, str]) -> str:
    h = hashlib.sha256()
    for k in sorted(sources):
        h.update(k.encode() + b"\0" + sources[k].encode() + b"\0")
    return h.hexdigest()[:16]


def per_seed_J(ev: Dict[str, Any]) -> Dict[str, float]:
    return {s: round(v["J"], 6) for s, v in ev.get("per_seed", {}).items()}


def summarize(ev: Dict[str, Any]) -> Dict[str, Any]:
    ps = ev.get("per_seed", {})
    if not ps:
        return {"error": ev.get("error")}
    return {"J_mean": float(np.mean([v["J"] for v in ps.values()])),
            "nlpd_mean": float(np.mean([v["nlpd"] for v in ps.values()])),
            "quality_heldout_mean": float(np.mean([v["quality_heldout"] for v in ps.values()])),
            "iala_learned_mean": float(np.mean([v["iala_learned"] for v in ps.values()])),
            "dw_mean": float(np.mean([v["dw_mean"] for v in ps.values()])),
            "J_per_seed": per_seed_J(ev), "wall": ev.get("wall")}


def lqt_sink(rec: Dict[str, Any], edited: List[str]) -> Dict[str, Any]:
    """Accepted param edits land on the run's unified model.lqt (lqt-unify API, board seq 79)
    through runtime.selfmod.lqt_land, which replays every accepted commit as logged
    RecursiveWeightEdit/TensorAttach ops after the generation loop (see main)."""
    return {"pending": "landed on <run-dir>/model.lqt by runtime.selfmod.lqt_land at the end of the run"}


def commit_accept(paths: List[str], msg: str) -> str:
    git("add", "--", *paths)
    git("commit", "-m", msg, "--", *paths)
    return git("rev-parse", "HEAD")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--generations", type=int, default=30)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--replicates", type=int, default=2)
    ap.add_argument("--rng-seed", type=int, default=20261121)
    ap.add_argument("--no-commit", action="store_true", help="dry run: never write/commit the repo")
    args = ap.parse_args()

    run_dir = (REPO / args.run_dir).resolve() if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "evals").mkdir(exist_ok=True)
    scratch = Path(os.environ.get("TMPDIR", "/tmp")) / f"selfmod_{run_dir.name}_{int(time.time())}"
    scratch.mkdir(parents=True)
    log_path = run_dir / "generations.jsonl"
    run_json = run_dir / "run.json"

    base = git("rev-parse", "HEAD")
    snap = scratch / "snapshot"
    snap_manifest = gate.extract_snapshot(REPO, base, snap)
    mpaths = gate.mutable_paths()
    current = {p: (snap / p).read_text() for p in mpaths}
    baseline_sources = dict(current)
    for p in mpaths:  # the repo's mutable files must be the committed ones (exclusive dir)
        if (REPO / p).read_text() != current[p]:
            raise SystemExit(f"{p} in the working tree differs from base commit {base}; commit it first")

    meta: Dict[str, Any] = {
        "started": now(), "base_commit": base, "repo": str(REPO), "scratch": str(scratch),
        "generations": args.generations, "rng_seed": args.rng_seed, "python": sys.version.split()[0],
        "config": {k: getattr(C, k) for k in dir(C) if k.isupper()},
        "objective": "J = -NLPD_heldout + LAMBDA_Q * reflection_quality_heldout (see config.py)",
    }
    run_json.write_text(json.dumps(meta, indent=1, default=str))

    def evaluate(sources: Dict[str, str], tag: str, split: str = "select", seeds: str = None) -> Dict[str, Any]:
        cand = gate.build_candidate(snap, sources, {}, scratch)
        errs = gate.check_invariants(cand, snap_manifest)
        if errs:
            shutil.rmtree(cand, ignore_errors=True)
            return {"error": "invariants: " + "; ".join(errs)}
        ev = gate.run_evaluator(cand, run_dir / "evals" / f"{tag}.json", split=split, seeds=seeds)
        shutil.rmtree(cand, ignore_errors=True)
        return ev

    # ---------------------------------------------------------------- baseline + noise
    reps = []
    for r in range(args.replicates):
        ev = evaluate(current, f"baseline_rep{r}")
        if ev.get("error"):
            meta["status"] = f"baseline evaluation failed: {ev['error']}"
            meta["baseline_error"] = ev
            run_json.write_text(json.dumps(meta, indent=1, default=str))
            return 1
        reps.append(ev)
    seeds = [str(s) for s in C.SELECT_SEEDS]
    rep_diff = max(abs(reps[i]["per_seed"][s]["J"] - reps[0]["per_seed"][s]["J"])
                   for i in range(1, len(reps)) for s in seeds) if len(reps) > 1 else 0.0
    min_delta = max(C.MIN_DELTA_FLOOR, 3.0 * rep_diff)
    incumbent = reps[0]
    meta["baseline"] = [summarize(e) for e in reps]
    meta["replicate_max_abs_dJ"] = rep_diff
    meta["min_delta"] = min_delta
    meta["min_delta_rule"] = f"max(MIN_DELTA_FLOOR={C.MIN_DELTA_FLOOR}, 3 * max_seed |J_rep - J_rep0| = {3 * rep_diff:.3g})"
    meta["preregistered_at"] = now()
    run_json.write_text(json.dumps(meta, indent=1, default=str))

    detector = LoopDetector()
    detector.register_state(surface_hash(current), 0)
    streaks: Dict[str, int] = {}
    meta_count: Dict[str, int] = {}
    last_rejected_rule = None
    rng = random.Random(args.rng_seed)
    accepted_commits = []
    fixed = [str(s) for s in C.SELECT_SEEDS]
    pol_path = f"{C.ALLOWED_EDIT_PREFIX}proposer_policy.py"

    for gen in range(1, args.generations + 1):
        t0 = time.time()
        fresh = [str(C.FRESH_SEED_BASE + C.FRESH_PER_GEN * gen + k) for k in range(C.FRESH_PER_GEN)]
        rec: Dict[str, Any] = {"gen": gen, "ts": now(), "fresh_seeds": fresh,
                               "incumbent_J_fixed": per_seed_J(incumbent)}
        signals = objective.mean_signals(incumbent["per_seed"])
        rec["signals"] = signals
        mp = None
        p = None
        depth = 0
        edits: Dict[str, str] = {}
        try:
            pol = proposer.load_policy_from_source(current[pol_path])
            if (last_rejected_rule and not last_rejected_rule.startswith("fallback")
                    and streaks.get(last_rejected_rule, 0) >= int(pol.META_TRIGGER_REJECTS)
                    and C.MAX_META_DEPTH >= 1):
                mp = proposer.meta_proposal(pol, last_rejected_rule, meta_count.get(last_rejected_rule, 0), signals)
            if mp is not None:
                depth = 1
                meta_count[last_rejected_rule] = meta_count.get(last_rejected_rule, 0) + 1
                meta_src, info = ast_edit.apply(current[pol_path], mp)
                errs = gate.scan_module(meta_src, pol_path)
                if errs:
                    raise ast_edit.EditError(f"meta edit violates I2: {errs}")
                mp["edit"] = info
                edits[pol_path] = meta_src
                pol = proposer.load_policy_from_source(meta_src)
                rec["meta_proposal"] = mp
                rec["meta_trigger"] = {"rule": last_rejected_rule, "consecutive_rejects": streaks[last_rejected_rule]}
            op = proposer.object_proposal(pol, signals, streaks, detector, gen, rng, {**current, **edits})
            p = op["proposal"]
            rec["depth"] = depth
            rec["proposal"] = p
            rec["causal_chain"] = op["chain"]
            path = f"{C.ALLOWED_EDIT_PREFIX}{p['module']}.py"
            new_src, info = ast_edit.apply({**current, **edits}[path], p)
            p["edit"] = info
            edits[path] = new_src
            rec["diff"] = {k: ast_edit.diff(current[k], v, k) for k, v in edits.items()}
            rec["signature"] = signature(p)
        except (ast_edit.EditError, KeyError, ValueError, StopIteration) as e:
            rule = (p or {}).get("rule") or (mp or {}).get("rule")
            rec.update({"decision": "reject", "reason": f"proposal/edit error: {type(e).__name__}: {e}",
                        "wall": time.time() - t0})
            if rule:
                streaks[rule] = streaks.get(rule, 0) + 1
                last_rejected_rule = rule
            with log_path.open("a") as f:
                f.write(json.dumps(rec, default=str) + "\n")
            continue

        cand_sources = {**current, **edits}
        sh = surface_hash(cand_sources)
        rec["surface_hash"] = sh
        pre = detector.precheck(p, sh, gen)
        ev = None
        if pre:
            rec.update({"decision": "reject", "reason": pre})
        else:
            ev = evaluate(cand_sources, f"gen{gen:03d}", seeds=",".join(fixed + fresh))
            ev_inc_fresh = evaluate(current, f"gen{gen:03d}_incumbent_fresh", seeds=",".join(fresh))
            if ev.get("error") or ev_inc_fresh.get("error"):
                err = ev.get("error") or ev_inc_fresh.get("error")
                rec.update({"decision": "reject", "reason": f"live run: {err}",
                            "stderr_tail": (ev.get("stderr_tail") or ev_inc_fresh.get("stderr_tail") or "")[-800:]})
            else:
                d = objective.decide(ev, incumbent, ev_inc_fresh, fixed, fresh, min_delta)
                rec.update({"decision": "accept" if d["accept"] else "reject", "reason": d["reason"],
                            "mean_dJ_fixed": d.get("mean_dJ_fixed"), "mean_dJ_fresh": d.get("mean_dJ_fresh"),
                            "dJ_fixed": d.get("dJ_fixed"), "dJ_fresh": d.get("dJ_fresh"),
                            "n_improved": d.get("n_improved"), "candidate": summarize(ev),
                            "incumbent_fresh": summarize(ev_inc_fresh)})
        accepted = rec["decision"] == "accept"
        rec["rldis"] = detector.record(p, accepted, gen, sh if accepted else None)
        if accepted:
            edited = [k for k in edits if edits[k] != current[k]]
            current = cand_sources
            incumbent = {"per_seed": {s: ev["per_seed"][s] for s in fixed}, "seeds": [int(s) for s in fixed]}
            streaks[p["rule"]] = 0
            if mp is not None:
                streaks[last_rejected_rule] = 0
            last_rejected_rule = None
            trig = rec["causal_chain"].get("trigger", {})
            edit_desc = "; ".join(
                f"{q['module']}.{q['target']} {q['kind']} {q.get('edit', {}).get('old', '')}->{q.get('edit', {}).get('new', '')}"
                for q in ([mp] if mp else []) + [p])
            msg = (f"selfmod gen {gen} (depth {depth}): {edit_desc}\n\n"
                   f"rule {p['rule']} | signal {trig.get('signal')}={trig.get('value', float('nan')):.5g} "
                   f"{trig.get('cmp', '')} thr {trig.get('thr', float('nan')):.5g} | {rec['causal_chain'].get('selection')}\n"
                   f"{rec['reason']}\n"
                   f"J fixed incumbent {rec['incumbent_J_fixed']}\nJ fixed+fresh candidate {per_seed_J(ev)}\n"
                   f"J fresh incumbent {rec['incumbent_fresh']['J_per_seed']}\n"
                   f"live cognition runs on {len(fixed)} fixed + {len(fresh)} fresh seeds; run {run_dir.name}; base {base[:7]}")
            if not args.no_commit:
                for path in edited:
                    (REPO / path).write_text(current[path])
                rec["commit"] = commit_accept(edited, msg)
                accepted_commits.append(rec["commit"])
                rec["lqt_edit"] = lqt_sink(rec, edited)
        else:
            streaks[p["rule"]] = streaks.get(p["rule"], 0) + 1
            if mp is None:
                last_rejected_rule = p["rule"]
        rec["streaks"] = {k: v for k, v in streaks.items() if v}
        rec["rldis_state"] = detector.state()
        rec["wall"] = time.time() - t0
        with log_path.open("a") as f:
            f.write(json.dumps(rec, default=str) + "\n")

    # ---------------------------------------------------------------- fresh held-out
    meta["accepted_commits"] = accepted_commits
    meta["final_mutable_hash"] = surface_hash(current)
    meta["baseline_mutable_hash"] = surface_hash(baseline_sources)
    fb = evaluate(baseline_sources, "final_baseline", split="final")
    ff = evaluate(current, "final_selected", split="final")
    meta["final_eval"] = {"split": "final", "seeds": list(C.FINAL_SEEDS),
                          "baseline": summarize(fb), "selected": summarize(ff)}
    if not fb.get("error") and not ff.get("error"):
        dj = {s: ff["per_seed"][s]["J"] - fb["per_seed"][s]["J"] for s in fb["per_seed"]}
        meta["final_eval"]["dJ_per_seed"] = dj
        meta["final_eval"]["dJ_mean"] = float(np.mean(list(dj.values())))
        meta["final_eval"]["seeds_improved"] = sum(1 for v in dj.values() if v > 0)
    if accepted_commits and not args.no_commit:
        land = subprocess.run([sys.executable, "-m", "runtime.selfmod.lqt_land", "--run-dir", str(run_dir)],
                              cwd=run_dir, capture_output=True, text=True)
        meta["lqt_land"] = {"rc": land.returncode, "stdout_tail": land.stdout[-1500:],
                            "report": str(run_dir / "lqt_land.json")}
    meta["finished"] = now()
    meta["status"] = "ok"
    run_json.write_text(json.dumps(meta, indent=1, default=str))
    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
