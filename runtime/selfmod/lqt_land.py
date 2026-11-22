"""Land accepted self-modification param edits on the run's unified model.lqt (lqt-unify API, board seq 79).

    python -m runtime.selfmod.lqt_land --run-dir runtime/runs/2026-11-21_selfmod

1. Genesis (if <run-dir>/model.lqt is absent): the seeded cognitive stack (RSILoop, native
   backend, bound UnifiedModel) -> model.lqt, exactly as runtime/train.py run_unified does.
2. Every numeric module-level constant of cognition/mutable/*_policy.py at the run's base
   commit is attached as its own tensor ``selfmod/policy/<module>/<NAME>`` (shape (1,),
   group 'selfmod_policy') through a logged TensorAttach.
3. For every accepted generation in generations.jsonl, in order, the constants whose value
   changed are written with ``UnifiedModel.edit`` (logged RecursiveWeightEdit ops); new
   constants (insert_term) are attached (logged TensorAttach). The model is saved and the
   hash-chained edit log verified.
The values come from the loop's own git commits (``git show <commit>:<path>``), so model.lqt
and git carry the same accepted edits. Writes <run-dir>/lqt_land.json.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict

import numpy as np

from runtime.selfmod import ast_edit
from runtime.selfmod import config as C

REPO = Path(__file__).resolve().parents[2]


def constants_at(commit: str) -> Dict[str, float]:
    out = {}
    for m in C.MUTABLE_MODULES:
        path = f"{C.ALLOWED_EDIT_PREFIX}{m}.py"
        src = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{path}"], check=True,
                             capture_output=True, text=True).stdout
        for k, v in ast_edit.numeric_constants(src).items():
            out[f"selfmod/policy/{m}/{k}"] = float(v)
    return out


def genesis(run_dir: Path, L: Any, model_path: Path) -> Dict[str, Any]:
    from cognition.lqt_bridge import UnifiedModel, bind_unified, collect_live_tensors
    from runtime.loop import LoopConfig, RSILoop
    t0 = time.time()
    g = UnifiedModel(L, model_path)
    bind_unified(g)
    cfg = LoopConfig(out_dir=run_dir / "genesis_stack", seed=0, hidden_dim=C.HIDDEN_DIM,
                     seq_len=C.SEQ_LEN, metacog_state_dim=C.METACOG_STATE_DIM, lqt_backend="native")
    gl = RSILoop(cfg)
    live = collect_live_tensors(gl.engine, gl.iala, gl.bayes, gl.motivation)
    g.genesis(live)
    info = {**g.save(), "tensors": len(g.meta), "live_tensors": len(live), "seconds": time.time() - t0}
    gl.close()
    bind_unified(None)
    return info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = (REPO / args.run_dir).resolve()
    from cognition.lqt_bridge import UnifiedModel, get_backend
    L = get_backend("native").L
    model_path = run_dir / "model.lqt"
    meta = json.loads((run_dir / "run.json").read_text())
    report: Dict[str, Any] = {"model": str(model_path), "base_commit": meta["base_commit"]}
    if not model_path.exists():
        report["genesis"] = genesis(run_dir, L, model_path)
    um = UnifiedModel.load(L, model_path)
    d0 = int(um.model.undo_depth)
    base = constants_at(meta["base_commit"])
    attached = 0
    for name, v in sorted(base.items()):
        if name not in um.meta:
            um.add(name, np.array([v], np.float32), group="selfmod_policy", logged=True)
            attached += 1
    report["baseline_attach_ops"] = int(um.model.undo_depth) - d0
    report["baseline_constants"] = len(base)
    prev = base
    gens = []
    for line in (run_dir / "generations.jsonl").read_text().splitlines():
        rec = json.loads(line)
        if rec.get("decision") != "accept" or not rec.get("commit"):
            continue
        cur = constants_at(rec["commit"])
        dstart = int(um.model.undo_depth)
        changed = {}
        for name, v in sorted(cur.items()):
            if name not in um.meta:
                um.add(name, np.array([v], np.float32), group="selfmod_policy", logged=True)
                changed[name] = [None, v]
            elif prev.get(name) != v:
                um.edit(name, np.array([v], np.float32))
                changed[name] = [prev.get(name), v]
        stored = {n: float(um.cache[n][0]) for n in changed}
        gens.append({"gen": rec["gen"], "commit": rec["commit"], "changed": changed,
                     "stored_after": stored, "logged_ops": int(um.model.undo_depth) - dstart})
        prev = cur
    report["accepted_generations"] = gens
    report["save"] = um.save(model_path)
    report["undo_depth"] = int(um.model.undo_depth)
    um2 = UnifiedModel.load(L, model_path)
    report["reload_check"] = {n: float(um2.cache[n][0]) for g in gens for n in g["changed"]}
    report["verify_edit_log"] = bool(um2.model.verify_edit_log())
    (run_dir / "lqt_land.json").write_text(json.dumps(report, indent=1, default=str))
    print(json.dumps({k: report[k] for k in ("save", "baseline_attach_ops", "verify_edit_log")}, default=str))
    for g in gens:
        print(g["gen"], g["commit"][:7], g["logged_ops"], g["changed"], g["stored_after"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
