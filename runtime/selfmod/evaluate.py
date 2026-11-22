"""Live-run evaluator (protected). Runs in a subprocess inside the candidate copy.

    PYTHONPATH=<candidate_root> python -m runtime.selfmod.evaluate \
        --split select|final --seeds 0,1,2 --out result.json

No test code (operator rule 2026-11-21): the check is the running system. For each seed
the live cognition loop (SelfModLoop: CognitiveEngine + sentinel + Bayes + motivation +
IALA + LQT Psi self-modification) runs N_TRAIN training passages and N_HELDOUT
held-out passages, scored by objective.score_seed from the run's own metrics.
Writes one JSON with per-seed scores/guards/signals, the sha256 + path of every
cognition/mutable module actually imported (proving it came from the candidate root),
and timings. Exit 0 iff the JSON was written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["select", "final"], default="select")
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--keep-records", action="store_true")
    args = ap.parse_args()

    t_start = time.time()
    logging.basicConfig(level=logging.WARNING)
    import torch
    torch.set_num_threads(1)
    root = Path(__file__).resolve().parents[2]
    from runtime.selfmod import config as C
    seeds = [int(s) for s in args.seeds.split(",")] if args.seeds else list(
        C.SELECT_SEEDS if args.split == "select" else C.FINAL_SEEDS)
    result = {"root": str(root), "split": args.split, "seeds": seeds, "argv": sys.argv}
    try:
        from runtime.loop import LoopConfig, load_corpus
        from runtime.selfmod.harness import SelfModLoop
        from runtime.selfmod.objective import passage_plan, score_seed
        import cognition.mutable as M
        import cognition.mutable.bayes_policy, cognition.mutable.plasticity_policy  # noqa: F401
        import cognition.mutable.reflection_policy, cognition.mutable.motivation_policy  # noqa: F401
        import cognition.mutable.proposer_policy  # noqa: F401
        mods = {}
        for name in C.MUTABLE_MODULES:
            mod = sys.modules[f"cognition.mutable.{name}"]
            p = Path(mod.__file__).resolve()
            if root not in p.parents:
                raise RuntimeError(f"cognition.mutable.{name} imported from {p}, not candidate root {root}")
            mods[name] = {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        result["mutable_modules"] = mods

        corpus = load_corpus(root / "lqt" / "iala" / "theorems", 600)
        result["per_seed"] = {}
        records_all = {}
        work = Path(tempfile.mkdtemp(prefix="selfmod_eval_"))
        for seed in seeds:
            ts = time.time()
            plan = passage_plan(corpus, seed, args.split)
            cfg = LoopConfig(out_dir=work / f"seed{seed}", seed=seed, hidden_dim=C.HIDDEN_DIM,
                             seq_len=C.SEQ_LEN, metacog_state_dim=C.METACOG_STATE_DIM,
                             lqt_backend=C.LQT_BACKEND)
            loop = SelfModLoop(cfg)
            try:
                recs = [loop.run_passage(corpus[i], "train") for i in plan["train"]]
                recs += [loop.run_passage(corpus[i], "heldout") for i in plan["heldout"]]
                w0 = loop.W0_norm
            finally:
                loop.close()
            sc = score_seed(recs, w0)
            sc["seconds"] = time.time() - ts
            sc["plan"] = plan
            result["per_seed"][str(seed)] = sc
            records_all[str(seed)] = recs
        if args.keep_records:
            result["records"] = records_all
    except Exception as e:  # recorded, never hidden: the gate rejects on error
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()[-4000:]
    result["seconds"] = time.time() - t_start
    Path(args.out).write_text(json.dumps(result, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
