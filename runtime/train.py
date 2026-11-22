#!/usr/bin/env python3
"""Train CLI for the integrated RSI loop (runtime.loop.RSILoop).

    python3 -m runtime.train --steps 40 --seed 0 --out runs/rsi_seed0 [--checkpoint-every 10]

Writes into --out (created; must be empty or absent unless --overwrite):
    metrics.jsonl          one JSON record per step, exactly as the loop produced it
    run.json               config, versions, wall time, exit status
    checkpoints/step_NNNN/ LQT weight store, Bayesian beliefs (YAML), motivation summary.
                           backend 'native' (default): lqt_store/psi_weights.lqt, a real
                           .lqt file (RecursiveWeight bucket per lattice position + the
                           hash-chained edit log of every weight update) + manifest.json;
                           each checkpoint is re-loaded and compared bit-exactly to the
                           live weights.  backend 'python': RTNZ .rta bucket store.
    run.json "lqt_native"  (native only) per-checkpoint .lqt bytes / verify_edit_log /
                           reload match, and an end-of-run rollback test: the last
                           step's three weight updates are rolled back through
                           LqtModel.rollback and compared to the weights before that step.
    curves.png             metric curves read back from metrics.jsonl
    run.log                log output

Native backend (default) = UNIFIED live model (operator correction 2026-11-21):
    model.lqt              the ONE model file of the run.  RecursiveWeight buckets on the
                           shared RW base codebook hold every learnable tensor of the
                           cognitive stack (Psi W_R/W_E/W_M, RTA tensor, ethical state,
                           metacognitive tensor, meta-reflective head, engine heads, RW
                           registry, IALA, Bayesian beliefs, motivation entities).  Genesis
                           writes it once from the seeded stack; the run then LOADS it, the
                           stack takes every value from it, every change a step makes is a
                           logged edit on it (D-025 bucket edits / delta / attach / detach),
                           and it is saved back to the same path.
    unified_table.json/.md per tensor: name, shape, group, representation, base, bits, scale,
                           base-only error, reload error vs live.
    live_sha256.json       sha256 of every live tensor at end of run, for
                           `python -m runtime.train --verify-model <run>/model.lqt` in a fresh process.
    run.json "unified"     genesis/save info, per-step edit counts, reload check, rollback checks.

The process runs with --out as its working directory, so files the operator's modules
write into the CWD (recursive_weights_core's recursive_weights.log) land in the run.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent

CURVES = [
    ("reflection_quality", "reflection quality (engine)"),
    ("ethical_alignment", "ethical alignment (engine)"),
    ("meta_confidence", "meta confidence (meta reflection)"),
    ("advantage", "advantage = quality - prior mean"),
    ("contradiction_severity", "URSMIF sentinel severity"),
    ("motivation_drive", "motivation drive"),
    ("dW_W_R", "|dW_R| (LQT write)"),
    ("dW_W_E", "|dW_E| (LQT write)"),
    ("dW_W_M", "|dW_M| (LQT write)"),
    ("convergence_distance", "triaxial convergence distance"),
    ("psi_norm", "|psi|"),
    ("iala_entities", "IALA knowledge entities"),
]


def plot_curves(records: List[Dict[str, Any]], path: Path) -> None:
    """One panel per metric; values plotted as recorded (log y for the dW norms)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    steps = [r["step"] for r in records]
    cols = 3
    rows = math.ceil(len(CURVES) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 3 * rows), squeeze=False)
    for ax, (key, title) in zip(axes.flat, CURVES):
        ys = [r.get(key) for r in records]
        pts = [(s, y) for s, y in zip(steps, ys) if isinstance(y, (int, float)) and math.isfinite(y)]
        if pts:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=".", linewidth=1)
            if key.startswith("dW_") and all(p[1] > 0 for p in pts):
                ax.set_yscale("log")
        else:
            ax.text(0.5, 0.5, "no finite values", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("step", fontsize=8)
        ax.tick_params(labelsize=7)
    for ax in list(axes.flat)[len(CURVES):]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _checkpoint(loop: Any, directory: Path, native: bool) -> Dict[str, Any]:
    """loop.checkpoint, then (native) reload the .lqt into a fresh store and compare bit-exactly."""
    info = loop.checkpoint(directory)
    if not native:
        return info
    import numpy as np
    from cognition.lqt_bridge import LQTStore
    store_dir = directory / "lqt_store"
    manifest = json.loads((store_dir / "manifest.json").read_text())
    fresh = LQTStore(loop.store.backend)
    fresh.load(store_dir)
    mismatch = {n: float(np.abs(fresh.get(n) - loop.store.get(n)).max()) for n in loop.WEIGHTS}
    if any(v != 0.0 for v in mismatch.values()):
        raise RuntimeError(f"{store_dir}: .lqt reload differs from live weights {mismatch}")
    info["lqt"] = {"step_dir": directory.name, "file": str(store_dir / manifest["file"]),
                   "bytes": manifest["bytes"], "sha256": manifest["sha256"],
                   "edit_log_entries": manifest["edit_log_entries"],
                   "verify_edit_log": loop.store.verify_edit_log() and manifest["verify_edit_log"],
                   "reload_max_abs_diff": max(mismatch.values())}
    return info


def _rollback_test(loop: Any, before: Dict[str, Any]) -> Dict[str, Any]:
    """Roll back the last step's W_R/W_E/W_M updates via LqtModel.rollback; compare to pre-step weights.

    Runs after the final checkpoint is written, so the saved run state is the
    un-rolled-back one; the live store is left rolled back (the run is over).
    """
    import numpy as np
    entries_before = len(loop.store.native.edit_log())
    undone = loop.store.rollback(len(loop.WEIGHTS))
    diffs = {n: float(np.abs(loop.store.get(n) - before[n]).max()) for n in loop.WEIGHTS}
    return {"undone_updates": undone, "edit_log_entries_before": entries_before,
            "edit_log_entries_after": len(loop.store.native.edit_log()),
            "max_abs_diff_vs_pre_step": diffs, "exact": all(v == 0.0 for v in diffs.values()),
            "verify_edit_log_after": loop.store.verify_edit_log()}


def _sha(a: Any) -> str:
    import hashlib
    import numpy as np
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.float32).tobytes()).hexdigest()


def verify_model(path: Path) -> int:
    """Fresh process: load model.lqt, verify the edit-log chain, reconstruct every
    tensor and compare its sha256 with the live-state hashes the run recorded."""
    import numpy as np
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from cognition.lqt_bridge import UnifiedModel, get_backend
    path = path.resolve()
    um = UnifiedModel.load(get_backend("native").L, path)
    expected = json.loads((path.parent / "live_sha256.json").read_text())
    got = {n: _sha(um.cache[n]) for n in um.meta}
    mism = sorted(n for n in set(expected) | set(got) if expected.get(n) != got.get(n))
    report = {"file": str(path), "tensors": len(got), "verify_edit_log": bool(um.model.verify_edit_log()),
              "edit_log_entries": len(um.model.edit_log()), "sha_mismatches": mism[:20],
              "n_sha_mismatches": len(mism), "all_reconstruct_equal_live": not mism}
    (path.parent / "verify_fresh_process.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if (not mism and report["verify_edit_log"]) else 1


def _write_table(rows: List[Dict[str, Any]], out: Path) -> None:
    (out / "unified_table.json").write_text(json.dumps(rows, indent=2))
    lines = ["| tensor | shape | group | repr | base | bits | scale | base-only max err | reload max err |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['name']}` | {tuple(r['shape'])} | {r['group']} | {r['repr']} | codebook 0 | "
                     f"{r['bits']} | {r['scale']:.4g} | {r['base_only_max_abs_err']:.3g} | {r['reload_max_abs_err']:.3g} |")
    (out / "unified_table.md").write_text("\n".join(lines) + "\n")


def run_unified(args: Any, out: Path, log: Any) -> int:
    """Genesis (if model.lqt absent) -> load model.lqt -> run computing from it -> save same file."""
    import numpy as np
    import torch
    from cognition.lqt_bridge import UnifiedModel, bind_unified, collect_live_tensors, get_backend
    from runtime.loop import LoopConfig, RSILoop
    from runtime.chat import StackIdentity

    L = get_backend("native").L
    model_path = out / "model.lqt"
    cfg = LoopConfig(out_dir=out, seed=args.seed, hidden_dim=args.hidden_dim, eta=args.eta,
                     lqt_backend="native", engine_learner=not args.no_engine_learner)
    info: Dict[str, Any] = {"argv": sys.argv, "seed": args.seed, "steps_requested": args.steps,
                            "config": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(cfg).items()},
                            "python": platform.python_version(), "torch": torch.__version__,
                            "numpy": np.__version__, "machine": platform.machine(),
                            "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "lqt_backend": "native-unified"}
    t0 = time.time()
    status = "ok"
    records: List[Dict[str, Any]] = []
    uni: Dict[str, Any] = {}
    loop = None
    try:
        # ---- genesis: seeded stack -> model.lqt (builder, no edit-log entries)
        if not model_path.exists():
            g = UnifiedModel(L, model_path)
            bind_unified(g)
            gl = RSILoop(cfg)
            live = collect_live_tensors(gl.engine, gl.iala, gl.bayes, gl.motivation)
            g.genesis(live)
            uni["genesis"] = {**g.save(), "tensors": len(g.meta),
                              "live_tensors": len(live), "seconds": time.time() - t0}
            gl.close()
            bind_unified(None)
            del g, gl
        # ---- run: load model.lqt; the stack takes every value from it
        t1 = time.time()
        um = UnifiedModel.load(L, model_path)
        bind_unified(um)
        loop = RSILoop(cfg)
        if loop.store.native is None or loop.store.native.unified is not um:
            raise RuntimeError("backbone Psi store is not bound to the loaded model.lqt")
        identity = StackIdentity(loop, um, cfg)
        identity._rebuild_evolution(um.stack.get("evolution", {}))
        identity._rebuild_dataclasses(um.stack.get("entities", []))
        identity._rebuild_rwa()
        loop.iala.restore_identity(um.stack.get("iala", {}))
        identity._rebuild_kg(um.stack.get("kg_entities", {}))
        loop.step_index = int(um.stack.get("step_index", 0))
        live = collect_live_tensors(loop.engine, loop.iala, loop.bayes, loop.motivation)
        um.apply_to_live(live)
        for n in loop.WEIGHTS:
            if not np.array_equal(loop.field.W[n], um.cache[n]):
                raise RuntimeError(f"{n}: backbone Psi does not equal model.lqt after load")
        uni["load"] = {**um.loaded_from, "tensors": len(um.meta), "live_tensors": len(live),
                       "seconds": time.time() - t1}
        snapshots: List[Dict[str, Any]] = []      # model state before each of the last steps
        step_ops: List[int] = []
        with open(out / "metrics.jsonl", "a", encoding="utf-8") as fh:
            for _ in range(args.steps):
                snapshots.append(dict(um.cache))
                snapshots = snapshots[-6:]
                depth0 = int(um.model.undo_depth)
                rec = loop.step()
                ts = time.time()
                live = collect_live_tensors(loop.engine, loop.iala, loop.bayes, loop.motivation)
                st = um.sync(live)
                loop.rsei.notify_lqt_sync(st, bool(um.model.verify_edit_log()))
                um.stack = identity._stack()
                ops = int(um.model.undo_depth) - depth0
                step_ops.append(ops)
                rec.update({"lqt_ops": ops, "lqt_tensors": len(um.meta), "lqt_edited": st["edited"],
                            "lqt_attached": st["attached"], "lqt_detached": st["detached"],
                            "lqt_elements_changed": st["elements_changed"], "lqt_changes": st["names"],
                            "lqt_edit_log": len(um.model.edit_log()), "sync_seconds": time.time() - ts})
                records.append(rec)
                fh.write(json.dumps(rec, default=str) + "\n")
                fh.flush()
                print(f"step {rec['step']:4d} q={rec['reflection_quality']:.5f} |dW_R|={rec['dW_W_R']:.3e} "
                      f"ops={ops} edited={st['edited']} attached={st['attached']} detached={st['detached']} "
                      f"log={rec['lqt_edit_log']} t={rec['step_seconds']:.2f}+{rec['sync_seconds']:.2f}s", flush=True)
                if args.checkpoint_every > 0 and rec["step"] % args.checkpoint_every == 0:
                    uni.setdefault("saves", []).append({"step": rec["step"], **um.save()})
        final = um.save()
        uni["final_save"] = final
        # live state at end (what the next run will load)
        live = collect_live_tensors(loop.engine, loop.iala, loop.bayes, loop.motivation)
        live_now = {n: t.get().copy() for n, t in live.items()}
        for n in loop.WEIGHTS:
            live_now[n] = np.asarray(loop.field.W[n], np.float32).copy()
        (out / "live_sha256.json").write_text(json.dumps({n: _sha(a) for n, a in sorted(live_now.items())}, indent=1))
        # ---- reload the saved file into a fresh LqtModel and compare with live
        fresh = UnifiedModel.load(L, model_path)
        reload_err = {n: (float(np.max(np.abs(fresh.cache[n] - live_now[n]))) if n in fresh.cache else None)
                      for n in live_now}
        missing = sorted(set(live_now) - set(fresh.meta)) + sorted(set(fresh.meta) - set(live_now))
        rows = um.table()
        for r in rows:
            r["reload_max_abs_err"] = reload_err.get(r["name"], float("nan"))
        _write_table(rows, out)
        bad = {n: e for n, e in reload_err.items() if e is None or e != 0.0}
        uni["reload"] = {"tensors": len(fresh.meta), "verify_edit_log": bool(fresh.model.verify_edit_log()),
                         "edit_log_entries": len(fresh.model.edit_log()), "name_mismatch": missing,
                         "nonzero_or_missing": dict(list(bad.items())[:20]), "n_bad": len(bad),
                         "all_equal": not bad and not missing}
        del fresh
        # ---- rollback on the live in-memory model (after the save; the file keeps the run's state)
        rb = []
        for k in (1, min(5, len(step_ops))):
            # k=1: undo the last step; k=5: then undo the 4 steps before it (state before step N-4)
            n_ops = step_ops[-1] if k == 1 else sum(step_ops[-k:-1])
            target = snapshots[-k]
            log_before = len(um.model.edit_log())
            um.rollback(n_ops)
            diff_names = sorted(set(target) ^ set(um.cache))
            maxdiff = max((float(np.max(np.abs(um.cache[n] - target[n]))) if um.cache[n].shape == target[n].shape
                           else float("inf")) for n in target if n in um.cache) if target else 0.0
            rb.append({"rolled_back_steps": k, "mutations_undone": n_ops, "edit_log_before": log_before,
                       "edit_log_after": len(um.model.edit_log()), "name_set_diff": diff_names[:10],
                       "max_abs_diff_vs_pre_step_state": maxdiff,
                       "exact": (not diff_names) and maxdiff == 0.0,
                       "verify_edit_log": bool(um.model.verify_edit_log())})
        uni["rollback"] = rb
        uni["edit_ops_per_step"] = [r["lqt_ops"] for r in records]
        uni["op_counts"] = um.op_counts
        uni["groups"] = {g: {"tensors": sum(1 for r in rows if r["group"] == g),
                             "elements": sum(r["elements"] for r in rows if r["group"] == g)}
                         for g in sorted({r["group"] for r in rows})}
        uni["repr"] = {k: sum(1 for r in rows if r["repr"] == k) for k in ("buckets", "base_eps")}
        uni["bucket_count"] = sum(r["elements"] for r in rows if r["repr"] == "buckets")
    except Exception as exc:
        status = f"error: {type(exc).__name__}: {exc}"
        log.exception("unified run failed")
        raise
    finally:
        if loop is not None:
            loop.close()
        if records:
            plot_curves(records, out / "curves.png")
        info.update({"status": status, "steps_completed": len(records), "wall_seconds": time.time() - t0,
                     "unified": uni})
        (out / "run.json").write_text(json.dumps(info, indent=2, default=str))
    ok = (uni.get("reload", {}).get("all_equal") and uni["reload"]["verify_edit_log"]
          and all(r["exact"] and r["verify_edit_log"] for r in uni.get("rollback", [])))
    return 0 if ok else 3


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify-model", type=Path, default=None,
                    help="fresh-process check of a unified run's model.lqt against its live_sha256.json")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--checkpoint-every", type=int, default=10)
    ap.add_argument("--hidden-dim", type=int, default=64)
    ap.add_argument("--eta", type=float, default=0.05)
    ap.add_argument("--lqt-backend", default=None, help="native | python (default: $LQT_BACKEND or native)")
    ap.add_argument("--no-engine-learner", action="store_true",
                    help="do not pass the IALA learner into CognitiveEngine (see LoopConfig.engine_learner)")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args(argv)
    if args.verify_model is not None:
        return verify_model(args.verify_model)
    if args.steps is None or args.out is None:
        ap.error("--steps and --out are required")

    out = args.out.resolve()
    if out.exists() and any(out.iterdir()) and not args.overwrite:
        print(f"refusing to write into non-empty {out} (use --overwrite)", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    os.chdir(out)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(out / "run.log", encoding="utf-8")],
        force=True,
    )
    log = logging.getLogger("runtime.train")
    if (args.lqt_backend or os.environ.get("LQT_BACKEND") or "native").strip().lower() == "native":
        return run_unified(args, out, log)

    from runtime.loop import LoopConfig, RSILoop
    import numpy as np
    import torch

    cfg = LoopConfig(out_dir=out, seed=args.seed, hidden_dim=args.hidden_dim, eta=args.eta,
                     lqt_backend=args.lqt_backend, engine_learner=not args.no_engine_learner)
    run_info: Dict[str, Any] = {
        "argv": sys.argv if argv is None else ["runtime.train", *argv],
        "steps_requested": args.steps,
        "seed": args.seed,
        "config": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(cfg).items()},
        "python": platform.python_version(), "torch": torch.__version__, "numpy": np.__version__,
        "machine": platform.machine(),
        "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    t_start = time.time()
    loop = RSILoop(cfg)
    run_info["init_seconds"] = time.time() - t_start
    run_info["corpus_passages"] = len(loop.passages)

    records: List[Dict[str, Any]] = []
    checkpoints: List[Dict[str, Any]] = []
    native = loop.store.native is not None
    run_info["lqt_backend"] = loop.store.backend.name
    weights_before_step: Dict[str, Any] = {}
    status = "ok"
    try:
        with open(out / "metrics.jsonl", "a", encoding="utf-8") as fh:
            for _ in range(args.steps):
                if native:
                    weights_before_step = {n: loop.store.get(n).copy() for n in loop.WEIGHTS}
                rec = loop.step()
                records.append(rec)
                fh.write(json.dumps(rec, default=str) + "\n")
                fh.flush()
                print(f"step {rec['step']:4d} q={rec['reflection_quality']:.5f} adv={rec['advantage']:+.5f} "
                      f"sev={rec['contradiction_severity']:.3f} drive={rec['motivation_drive']:.4f} "
                      f"|dW_R|={rec['dW_W_R']:.3e} ents={rec['iala_entities']} t={rec['step_seconds']:.2f}s",
                      flush=True)
                if args.checkpoint_every > 0 and rec["step"] % args.checkpoint_every == 0:
                    checkpoints.append(_checkpoint(loop, out / "checkpoints" / f"step_{rec['step']:04d}", native))
        if records and (not checkpoints or not checkpoints[-1]["dir"].endswith(f"step_{records[-1]['step']:04d}")):
            checkpoints.append(_checkpoint(loop, out / "checkpoints" / f"step_{records[-1]['step']:04d}", native))
        if native and records:
            run_info["lqt_native"] = {"checkpoints": [c["lqt"] for c in checkpoints],
                                      "rollback_test": _rollback_test(loop, weights_before_step)}
    except Exception as exc:
        status = f"error: {type(exc).__name__}: {exc}"
        log.exception("run failed")
        raise
    finally:
        loop.close()
        if records:
            plot_curves(records, out / "curves.png")
        run_info.update({"status": status, "steps_completed": len(records),
                         "wall_seconds": time.time() - t_start, "checkpoints": checkpoints})
        (out / "run.json").write_text(json.dumps(run_info, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
