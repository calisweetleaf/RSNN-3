#!/usr/bin/env python3
"""Render PNG diagnostics from real run artifacts in runtime/runs/*.

Usage (repo root):  python3 -m runtime.viz.render  [--runs-dir runtime/runs] [--out runtime/viz/out]

Only data that exists on disk is plotted. A panel whose source key/file is absent
says so in the panel ("no data: ...") instead of drawing anything synthetic.

Outputs (runtime/viz/out/):
  <run_id>__dashboard.png     per training run (metrics.jsonl): reflection, |dW|, sentinel,
                              Bayesian beliefs, IALA counts, motivation/breath, triaxial, checkpoints
  runs_compare.png            all training runs overlaid (reflection quality, |dW| sum)
  <run_id>__selfmod.png       selfmod runs (see _load_selfmod for accepted file layouts)
  <run_id>__native.png        runs with .lqt files: edit-log length per checkpoint, file sizes
  architecture.png            component data-flow graph built from AST-parsed imports
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[2]

# ----------------------------------------------------------------- style
BG, PANEL, FG, GRID, MUTED = "#0d1117", "#161b22", "#d6dde6", "#2a313c", "#7d8590"
PALETTE = ["#58a6ff", "#f78166", "#7ee787", "#d2a8ff", "#ffa657", "#79c0ff", "#ff7b72", "#e3b341"]

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": FG, "text.color": FG,
    "xtick.color": MUTED, "ytick.color": MUTED, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.grid": True, "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5, "legend.frameon": False,
    "font.family": "DejaVu Sans", "axes.prop_cycle": matplotlib.cycler(color=PALETTE),
})


def _nodata(ax, msg: str) -> None:
    ax.text(0.5, 0.5, "no data:\n" + msg, ha="center", va="center", color=MUTED,
            fontsize=8.5, transform=ax.transAxes, wrap=True)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)


def _save(fig, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return path


# ----------------------------------------------------------------- loading
def _load_jsonl(p: Path) -> List[dict]:
    rows = []
    if not p.exists():
        return rows
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # a partially-written last line during a live run
    return rows


def _load_json(p: Path) -> Optional[dict]:
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _col(rows: List[dict], key: str) -> Tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    for i, r in enumerate(rows):
        v = r.get(key)
        if isinstance(v, bool):
            v = float(v)
        if isinstance(v, (int, float)) and v is not None and np.isfinite(v):
            xs.append(r.get("step", i + 1)); ys.append(float(v))
    return np.asarray(xs), np.asarray(ys)


def _run_meta(run_dir: Path) -> dict:
    meta = _load_json(run_dir / "run.json") or {}
    seed = meta.get("seed", meta.get("config", {}).get("seed") if isinstance(meta.get("config"), dict) else None)
    if seed is None:
        m = re.search(r"seed(\d+)", run_dir.name)
        seed = int(m.group(1)) if m else "?"
    return {"meta": meta, "seed": seed}


def _dir_bytes(p: Path, pattern: str = "*") -> int:
    return sum(f.stat().st_size for f in p.rglob(pattern) if f.is_file())


# ----------------------------------------------------------------- per-run dashboard
def render_dashboard(run_dir: Path, out: Path) -> Optional[Path]:
    rows = _load_jsonl(run_dir / "metrics.jsonl")
    if not rows:
        return None
    info = _run_meta(run_dir)
    meta = info["meta"]
    cfg = meta.get("config", {}) if isinstance(meta.get("config"), dict) else {}
    backend = rows[-1].get("lqt_backend") or cfg.get("lqt_backend") or "?"
    canon = any(k.startswith(("breath_", "dream_", "rsl_")) for r in rows for k in r)
    fig, axes = plt.subplots(4 if canon else 3, 3, figsize=(17, 16.5 if canon else 12.5))
    sub = (f"steps {len(rows)} · backend {backend} · engine_learner {cfg.get('engine_learner', '?')} · "
           f"eta {cfg.get('eta', '?')} · status {meta.get('status', '?')}")
    fig.suptitle(f"RSI loop dashboard — run {run_dir.name} · seed {info['seed']}\n{sub}",
                 fontsize=13, fontweight="bold", y=0.995)

    # 1 reflection
    ax = axes[0, 0]
    keys = [("reflection_quality", "quality"), ("reflection_novelty", "novelty"),
            ("reflection_alignment", "alignment"), ("reflection_confidence", "confidence"),
            ("meta_confidence", "meta-confidence")]
    got = False
    for k, lab in keys:
        x, y = _col(rows, k)
        if len(x):
            ax.plot(x, y, lw=1.6 if k == "reflection_quality" else 1.0, label=lab,
                    alpha=1 if k == "reflection_quality" else 0.75); got = True
    if got:
        ax.set_title("Meta-reflective head scores"); ax.set_xlabel("step"); ax.set_ylabel("score [0–1]")
        ax.legend(ncol=2, loc="best")
    else:
        _nodata(ax, "reflection_* keys")

    # 2 |dW| log
    ax = axes[0, 1]
    got = False
    for k in ("W_R", "W_E", "W_M"):
        x, y = _col(rows, f"dW_{k}")
        m = y > 0
        if m.any():
            ax.semilogy(x[m], y[m], lw=1.3, marker="o", ms=2.5, label=f"|ΔW_{k[2:]}|"); got = True
    if got:
        ax.set_title("Realised LQT weight change per step (log)")
        ax.set_xlabel("step"); ax.set_ylabel("‖W_new − W_old‖_F (after re-quantisation)")
        ax.legend()
    else:
        _nodata(ax, "dW_W_R/E/M keys")

    # 3 sentinel severity
    ax = axes[0, 2]
    x1, y1 = _col(rows, "contradiction_severity")
    x2, y2 = _col(rows, "decoherence")
    if len(x1) or len(x2):
        if len(x1):
            ax.plot(x1, y1, lw=1.5, color=PALETTE[6], label="URSMIF contradiction severity")
        if len(x2):
            ax.plot(x2, y2, lw=1.2, color=PALETTE[4], label="triaxial decoherence severity")
        nc = [(r.get("step", i + 1), len(r.get("contradictions") or [])) for i, r in enumerate(rows)]
        tot = sum(c for _, c in nc)
        ax.set_ylim(-0.03, 1.03)
        ax.set_title(f"Sentinel severity (contradictions flagged: {tot})")
        ax.set_xlabel("step"); ax.set_ylabel("severity [0–1]"); ax.legend(loc="best")
    else:
        _nodata(ax, "contradiction_severity / decoherence")

    # 4 Bayesian
    ax = axes[1, 0]
    post = [(r.get("step", i + 1), r.get("belief_posterior")) for i, r in enumerate(rows)
            if isinstance(r.get("belief_posterior"), dict)]
    if post:
        names = sorted({k for _, d in post for k in d})
        obs_key = {"quality": "reflection_quality", "meta_confidence": "meta_confidence",
                   "ethical_alignment": "ethical_alignment"}
        for i, n in enumerate(names):
            c = PALETTE[i % len(PALETTE)]
            xs = [s for s, d in post if n in d]; ys = [d[n] for s, d in post if n in d]
            ax.plot(xs, ys, lw=1.8, color=c, label=f"posterior mean: {n}")
            if n in obs_key:
                ox, oy = _col(rows, obs_key[n])
                if len(ox):
                    ax.scatter(ox, oy, s=7, color=c, alpha=0.45, linewidths=0)
        ok = [all(r.get("bayes_update_ok", {}).values()) for r in rows if isinstance(r.get("bayes_update_ok"), dict)]
        ax.set_title(f"Bayesian belief trajectories (Beta means; dots = observations)\n"
                     f"updates ok {sum(ok)}/{len(ok)}", fontsize=9.5)
        ax.set_xlabel("step"); ax.set_ylabel("value [0–1]"); ax.legend(loc="best")
    else:
        _nodata(ax, "belief_posterior")

    # 5 IALA learned / rejected
    ax = axes[1, 1]
    x, y = _col(rows, "iala_learn_success")
    if len(x):
        learned = np.cumsum(y); rejected = np.cumsum(1 - y)
        ax.step(x, learned, where="post", lw=1.8, color=PALETTE[2], label=f"learned (Σ={int(learned[-1])})")
        ax.step(x, rejected, where="post", lw=1.8, color=PALETTE[1], label=f"rejected / not learned (Σ={int(rejected[-1])})")
        ax.set_xlabel("step"); ax.set_ylabel("cumulative passages")
        ax2 = ax.twinx(); ax2.grid(False)
        for k, c, lab in (("iala_metacog_confidence", PALETTE[3], "metacog confidence"),
                          ("iala_identity_coherence", PALETTE[5], "identity coherence")):
            xx, yy = _col(rows, k)
            if len(xx):
                ax2.plot(xx, yy, lw=1, ls="--", color=c, label=lab)
        ax2.set_ylabel("IALA score [0–1]", color=MUTED); ax2.set_ylim(-0.03, 1.03)
        h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, loc="upper left")
        ax.set_title("IALA learn_from_text outcomes")
    else:
        _nodata(ax, "iala_learn_success")

    # 6 motivation + breath phase
    ax = axes[1, 2]
    xm, ym = _col(rows, "motivation_drive")
    phases = [(r.get("step", i + 1), r.get("iala_phase")) for i, r in enumerate(rows) if r.get("iala_phase")]
    if len(xm) or phases:
        if len(xm):
            ax.plot(xm, ym, lw=1.6, color=PALETTE[4], label="motivation drive")
            ax.set_ylabel("drive [0–1]")
        if phases:
            order = []
            for _, p in phases:
                if p not in order:
                    order.append(p)
            cmap = {p: PALETTE[i % len(PALETTE)] for i, p in enumerate(order)}
            lo = (ym.min() if len(ym) else 0); hi = (ym.max() if len(ym) else 1)
            pad = max(hi - lo, 1e-3)
            band_y0, band_h = lo - 0.55 * pad, 0.3 * pad
            for s, p in phases:
                ax.add_patch(plt.Rectangle((s - 0.5, band_y0), 1, band_h, color=cmap[p], lw=0))
            ax.set_ylim(band_y0 - 0.05 * pad, hi + 0.25 * pad)
            for p in order:
                ax.plot([], [], marker="s", ls="", color=cmap[p], label=f"breath: {p}")
        ax.set_xlabel("step"); ax.legend(loc="upper right", ncol=2, fontsize=6.8)
        ax.set_title("Motivation drive + IALA breath phase (band)")
    else:
        _nodata(ax, "motivation_drive / iala_phase")

    # 7 triaxial
    ax = axes[2, 0]
    got = False
    for k, lab in (("ere", "ERE"), ("rbu", "RBU"), ("es", "ES")):
        x, y = _col(rows, k)
        if len(x):
            ax.plot(x, y, lw=1.3, label=lab); got = True
    if got:
        x, y = _col(rows, "psi_norm")
        if len(x):
            ax2 = ax.twinx(); ax2.grid(False)
            ax2.plot(x, y, lw=1, ls="--", color=MUTED, label="‖ψ‖")
            ax2.set_ylabel("‖ψ‖ (L2)", color=MUTED)
            h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
            ax.legend(h1 + h2, l1 + l2, loc="best", ncol=2)
        ax.set_title("Triaxial backbone axes"); ax.set_xlabel("step"); ax.set_ylabel("axis value")
    else:
        _nodata(ax, "ere/rbu/es")

    # 8 advantage / mod scale
    ax = axes[2, 1]
    xa, ya = _col(rows, "advantage"); xs_, ys_ = _col(rows, "mod_scale")
    if len(xa) or len(xs_):
        if len(xa):
            ax.bar(xa, ya, color=[PALETTE[2] if v >= 0 else PALETTE[1] for v in ya], width=0.8,
                   label="advantage = quality − prior mean")
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_ylabel("advantage (score units)"); ax.set_xlabel("step")
        if len(xs_):
            ax2 = ax.twinx(); ax2.grid(False)
            ax2.plot(xs_, ys_, lw=1, color=PALETTE[3], label="mod scale η·drive·(1−sev)·adv")
            ax2.set_ylabel("self-mod scale (dimensionless)", color=MUTED)
            lim = np.abs(ys_).max() * 1.1 or 1
            ax2.set_ylim(-lim, lim)
            h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
            ax.legend(h1 + h2, l1 + l2, loc="lower left")
        if len(ya):
            lim = np.abs(ya).max() * 1.1 or 1
            ax.set_ylim(-lim, lim)
        ax.set_title("Advantage signal driving self-modification")
    else:
        _nodata(ax, "advantage / mod_scale")

    # 9 checkpoint sizes
    ax = axes[2, 2]
    ck = sorted((run_dir / "checkpoints").glob("step_*")) if (run_dir / "checkpoints").exists() else []
    if ck:
        steps = [int(re.sub(r"\D", "", c.name) or 0) for c in ck]
        groups: Dict[str, List[int]] = defaultdict(list)
        cats = set()
        per = []
        for c in ck:
            d: Dict[str, int] = defaultdict(int)
            for f in c.rglob("*"):
                if f.is_file():
                    if f.suffix == ".lqt":
                        cat = "LQT .lqt"
                    elif f.suffix == ".rta":
                        cat = "RTNZ " + f.name.split(".")[0]
                    else:
                        cat = "other (" + f.suffix.lstrip(".") + ")" if f.suffix else "other"
                    d[cat] += f.stat().st_size; cats.add(cat)
            per.append(d)
        cats = sorted(cats)
        bottom = np.zeros(len(ck))
        for i, cat in enumerate(cats):
            vals = np.array([p.get(cat, 0) for p in per]) / 1024
            ax.bar(steps, vals, bottom=bottom, width=max(1, (steps[-1] - steps[0]) / max(len(steps), 1) * 0.6) if len(steps) > 1 else 4,
                   label=cat, color=PALETTE[i % len(PALETTE)])
            bottom += vals
        ax.set_xlabel("checkpoint step"); ax.set_ylabel("size on disk (KiB)")
        ax.set_title(f"Checkpoint sizes ({len(ck)} checkpoints)"); ax.legend(fontsize=6.5, loc="upper left", ncol=2)
        ax.set_ylim(0, bottom.max() * 1.45)
    else:
        finals = [f for f in list(run_dir.glob("*.lqt")) + list((run_dir / "lqt_store").glob("*")) if f.is_file()]
        if finals:
            labs = [str(f.relative_to(run_dir)) for f in finals]
            vals = [f.stat().st_size / 1024 for f in finals]
            y = np.arange(len(finals))
            ax.barh(y, vals, color=PALETTE[5])
            ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=7); ax.invert_yaxis()
            ax.set_xscale("log"); ax.set_xlabel("size on disk (KiB, log)")
            for yi, v in zip(y, vals):
                ax.text(v, yi, f" {v:,.1f}", va="center", fontsize=7)
            ax.set_title("Run-level store files (no checkpoints/step_* in this run)", fontsize=9.5)
        else:
            _nodata(ax, "checkpoints/step_* and run-level store")

    if canon:
        _canon_row(axes[3], rows)
    fig.tight_layout(rect=(0, 0, 1, 0.955 if not canon else 0.965))
    return _save(fig, out / f"{run_dir.name}__dashboard.png")


def _phase_band(ax, rows, key, y0, h, prefix):
    phases = [(r.get("step", i + 1), r.get(key)) for i, r in enumerate(rows) if r.get(key) is not None]
    order = []
    for _, p in phases:
        if str(p) not in order:
            order.append(str(p))
    cmap = {p: PALETTE[i % len(PALETTE)] for i, p in enumerate(order)}
    for st, p in phases:
        ax.add_patch(plt.Rectangle((st - 0.5, y0), 1, h, color=cmap[str(p)], lw=0))
    for p in order:
        ax.plot([], [], marker="s", ls="", color=cmap[p], label=f"{prefix}{p}")
    return bool(phases)


def _canon_row(axes, rows) -> None:
    """Rosemary canon metrics (runtime/rosemary_full.py): breath, dream, RSL memory."""
    ax = axes[0]
    xc, yc = _col(rows, "breath_coherence")
    xa, ya = _col(rows, "breath_dominant_weight")
    if len(xc) or any("breath_phase" in r for r in rows):
        if len(xc):
            ax.plot(xc, yc, lw=1.5, color=PALETTE[0], label="harmonic coherence")
        if len(xa):
            ax.plot(xa, ya, lw=1.1, color=PALETTE[3], label="dominant phase weight")
        vals = np.concatenate([yc, ya]) if (len(yc) or len(ya)) else np.array([0.0, 1.0])
        lo, hi = float(vals.min()), float(vals.max()); pad = max(hi - lo, 1e-3)
        if _phase_band(ax, rows, "breath_phase", lo - 0.5 * pad, 0.28 * pad, "canon breath: "):
            ax.set_ylim(lo - 0.55 * pad, hi + 1.1 * pad)
        ax.set_title("Rosemary canon: harmonic breath field"); ax.set_xlabel("step"); ax.set_ylabel("value [0–1]")
        ax.legend(fontsize=6.6, ncol=2, loc="upper left")
    else:
        _nodata(ax, "breath_* keys")
    ax = axes[1]
    xr, yr = _col(rows, "dream_receptivity"); xw, yw = _col(rows, "dream_awareness")
    ev = [(r.get("step", i + 1), r.get("dream_event")) for i, r in enumerate(rows) if r.get("dream_event")]
    act = [(r.get("step", i + 1), bool(r.get("dream_active_after"))) for i, r in enumerate(rows) if "dream_active_after" in r]
    if len(xr) or len(xw) or ev or act:
        for st, a in act:
            if a:
                ax.axvspan(st - 0.5, st + 0.5, color=PALETTE[3], alpha=0.15, lw=0)
        if len(xr):
            ax.plot(xr, yr, lw=1.4, marker="o", ms=2.5, color=PALETTE[4], label="dream receptivity")
        if len(xw):
            ax.plot(xw, yw, lw=1.4, marker="s", ms=2.5, color=PALETTE[5], label="dream awareness")
        mk = {"entered": ("v", PALETTE[2]), "declined": ("x", PALETTE[1]), "advanced": (".", PALETTE[0]),
              "exited": ("^", PALETTE[6])}
        for name, (m, c) in mk.items():
            pts = [st for st, e in ev if e == name]
            if pts:
                ax.scatter(pts, [1.02] * len(pts), marker=m, color=c, s=28, label=f"{name} ({len(pts)})", clip_on=False)
        if act:
            ax.plot([], [], color=PALETTE[3], alpha=0.4, lw=6, label="dream active")
        ax.set_ylim(-0.03, 1.08)
        steps_all = [r.get("step", i + 1) for i, r in enumerate(rows)]
        ax.set_xlim(min(steps_all) - 0.5, max(steps_all) + 0.5)
        ax.set_title("Rosemary canon: dream"); ax.set_xlabel("step"); ax.set_ylabel("value [0–1]")
        ax.legend(fontsize=6.6, ncol=2, loc="lower left")
    else:
        _nodata(ax, "dream_* keys")
    ax = axes[2]
    got = False
    for k, lab, c in (("rsl_active_memories", "active memories", PALETTE[2]),
                      ("rsl_storage_ops", "storage ops", PALETTE[0]),
                      ("rsl_sparse_entries", "sparse entries", PALETTE[4]),
                      ("rsl_paradox_resolutions", "paradox resolutions", PALETTE[6])):
        x, y = _col(rows, k)
        if len(x):
            ax.plot(x, y, lw=1.4, color=c, label=lab); got = True
    if got:
        ax.set_ylabel("count"); ax.set_xlabel("step")
        ax2 = ax.twinx(); ax2.grid(False)
        for k, lab, c in (("rsl_temporal_consistency", "temporal consistency", PALETTE[3]),
                          ("rsl_eigenstate_norm", "eigenstate norm", PALETTE[5])):
            x, y = _col(rows, k)
            if len(x):
                ax2.plot(x, y, lw=1, ls="--", color=c, label=lab)
        ax2.set_ylabel("RSL metric (dimensionless)", color=MUTED)
        h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, fontsize=6.6, loc="center left")
        ax.set_title("Rosemary canon: RSL memory")
    else:
        _nodata(ax, "rsl_* keys")


def render_compare(run_dirs: List[Path], out: Path) -> Optional[Path]:
    runs = [(d, _load_jsonl(d / "metrics.jsonl")) for d in run_dirs]
    runs = [(d, r) for d, r in runs if r]
    if len(runs) < 2:
        return None
    seeds = sorted({str(_run_meta(d)["seed"]) for d, _ in runs})
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
    fig.suptitle(f"Training runs compared — {len(runs)} runs · seeds {', '.join(seeds)}",
                 fontsize=12.5, fontweight="bold")
    for i, (d, rows) in enumerate(runs):
        c = PALETTE[i % len(PALETTE)]
        x, y = _col(rows, "reflection_quality")
        if len(x):
            axes[0].plot(x, y, lw=1.3, color=c, label=d.name)
        tot = None
        for k in ("W_R", "W_E", "W_M"):
            xx, yy = _col(rows, f"dW_{k}")
            if len(xx):
                tot = yy if tot is None else tot + yy if len(yy) == len(tot) else tot
        if tot is not None:
            m = tot > 0
            axes[1].semilogy(xx[m], tot[m], lw=1.2, color=c, label=d.name)
        post = [r["belief_posterior"].get("quality") for r in rows if isinstance(r.get("belief_posterior"), dict)]
        if post:
            axes[2].plot([r.get("step") for r in rows if isinstance(r.get("belief_posterior"), dict)], post,
                         lw=1.4, color=c, label=d.name)
    axes[0].set_title("reflection quality"); axes[0].set_ylabel("score [0–1]")
    axes[1].set_title("Σ |ΔW| over W_R, W_E, W_M (log)"); axes[1].set_ylabel("Frobenius norm")
    axes[2].set_title("posterior mean: quality"); axes[2].set_ylabel("Beta mean [0–1]")
    for ax in axes:
        ax.set_xlabel("step")
        if ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=7)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    return _save(fig, out / "runs_compare.png")


# ----------------------------------------------------------------- selfmod
_GEN_FILES = ("generations.jsonl", "selfmod.jsonl", "proposals.jsonl", "gate.jsonl", "edits.jsonl", "log.jsonl")


def _load_selfmod(run_dir: Path) -> Tuple[List[dict], Optional[dict], List[Path]]:
    """Return (generation rows, summary dict, files used). Accepts any *.jsonl whose rows carry
    a generation index and an accept flag; summary from summary.json / result.json / run.json."""
    used: List[Path] = []
    rows: List[dict] = []
    cands = [run_dir / n for n in _GEN_FILES] + sorted(run_dir.rglob("*.jsonl"))
    seen = set()
    for p in cands:
        if not p.exists() or p in seen:
            continue
        seen.add(p)
        rr = _load_jsonl(p)
        if rr and any(_accept_flag(r) is not None for r in rr):
            rows = rr; used.append(p); break
    summary = None
    for n in ("summary.json", "result.json", "results.json", "heldout.json", "run.json"):
        s = _load_json(run_dir / n)
        if s:
            summary = s if summary is None else {**s, **summary}
            used.append(run_dir / n)
    return rows, summary, used


def _accept_flag(r: dict) -> Optional[bool]:
    for k in ("accepted", "accept", "gate_accepted", "decision", "verdict", "status"):
        if k in r:
            v = r[k]
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                s = v.lower()
                if s.startswith("accept") or s in ("keep", "pass", "commit", "committed"):
                    return True
                if s.startswith("reject") or s in ("revert", "fail", "rolled_back", "rollback"):
                    return False
    return None


def _first(r: dict, keys) -> Any:
    for k in keys:
        if k in r and r[k] is not None:
            return r[k]
    return None


def _mean(d) -> Optional[float]:
    if isinstance(d, dict) and d:
        v = [float(x) for x in d.values() if isinstance(x, (int, float))]
        return float(np.mean(v)) if v else None
    return None


def render_selfmod(run_dir: Path, out: Path) -> Tuple[Optional[Path], str]:
    """Schema of runtime/selfmod/run.py: generations.jsonl rows {gen, incumbent_J{seed:J}, decision,
    reason, candidate{J_mean,J_per_seed,...}, mean_dJ, commit, proposal{rule,module,target,kind,edit},
    depth, meta_proposal}; run.json {base_commit, baseline[], min_delta, final_eval{baseline,selected,
    dJ_per_seed}, accepted_commits}."""
    rows = _load_jsonl(run_dir / "generations.jsonl")
    meta = _load_json(run_dir / "run.json") or {}
    if not rows:
        rows2, summary, used = _load_selfmod(run_dir)  # generic fallback for other layouts
        rows = rows2
    if not rows and not meta:
        return None, f"{run_dir.name}: no generations.jsonl / run.json"
    missing = []
    fig, axes = plt.subplots(2, 2, figsize=(17, 11.5))
    status = meta.get("status", "running" if "finished" not in meta else "?")
    fig.suptitle(f"Gated self-modification — run {run_dir.name} · base {str(meta.get('base_commit', '?'))[:7]} · "
                 f"{len(rows)}/{meta.get('generations', '?')} generations · status {status}\n"
                 f"{meta.get('objective', '')}",
                 fontsize=12, fontweight="bold")
    # 1 objective per generation
    ax = axes[0, 0]
    def _inc(r):
        return _mean(r.get("incumbent_J_fixed") or r.get("incumbent_J"))

    def _cand(r):
        # candidate J on the same fixed seeds as the incumbent: incumbent mean + logged mean dJ (fixed seeds)
        base_ = _inc(r)
        for k in ("mean_dJ_fixed", "mean_dJ"):
            if isinstance(r.get(k), (int, float)) and base_ is not None:
                return base_ + float(r[k])
        return (r.get("candidate") or {}).get("J_mean") if isinstance(r.get("candidate"), dict) else None

    inc = [(r.get("gen", i + 1), _inc(r)) for i, r in enumerate(rows)]
    inc = [(g, v) for g, v in inc if v is not None]
    cand = [(r.get("gen", i + 1), _cand(r), r.get("decision")) for i, r in enumerate(rows)]
    ev_pts = [(g, v, d) for g, v, d in cand if isinstance(v, (int, float))]
    noeval = [(g, d) for g, v, d in cand if not isinstance(v, (int, float))]
    if inc or ev_pts:
        if inc:
            ax.step([g for g, _ in inc], [v for _, v in inc], where="post", lw=1.8, color=PALETTE[0],
                    marker="_", ms=14, label="incumbent J (mean, fixed select seeds)")
        acc = [(g, v) for g, v, d in ev_pts if d == "accept"]
        rej = [(g, v) for g, v, d in ev_pts if d != "accept"]
        if acc:
            ax.scatter(*zip(*acc), marker="o", s=46, color=PALETTE[2], zorder=3, label=f"candidate accepted ({len(acc)})")
        if rej:
            ax.scatter(*zip(*rej), marker="x", s=36, color=PALETTE[1], zorder=3, label=f"candidate rejected ({len(rej)})")
        if noeval:
            ylo = min([v for _, v in inc] + [v for _, v, _ in ev_pts])
            ax.scatter([g for g, _ in noeval], [ylo] * len(noeval), marker="|", s=80, color=MUTED, zorder=3,
                       label=f"rejected before eval ({len(noeval)}: edit error / RLDIS precheck)")
        if isinstance(meta.get("min_delta"), (int, float)):
            ax.text(0.99, 0.02, f"accept needs mean ΔJ > min_delta = {meta['min_delta']:.3g}", ha="right",
                    va="bottom", transform=ax.transAxes, fontsize=7.5, color=MUTED)
        fr = [(r.get("gen"), r.get("mean_dJ_fresh")) for r in rows if isinstance(r.get("mean_dJ_fresh"), (int, float))]
        if fr:
            ax.text(0.99, 0.98, "fresh-seed mean ΔJ per gen: " + ", ".join(f"g{g}:{v:+.3g}" for g, v in fr[-6:]),
                    transform=ax.transAxes, fontsize=7, color=MUTED, va="top", ha="right")
        ax.set_xlabel("generation"); ax.set_ylabel("J = −NLPD + λ·quality (held-out, fixed seeds)")
        ax.set_title("Objective per generation"); ax.legend(fontsize=7, loc="upper left")
    else:
        _nodata(ax, "incumbent_J / candidate.J_mean in generations.jsonl"); missing.append("objective per generation")
    # 2 cumulative accepted
    ax = axes[0, 1]
    dec = [(r.get("gen", i + 1), r.get("decision")) for i, r in enumerate(rows) if r.get("decision")]
    if dec:
        g = [x for x, _ in dec]
        ax.step(g, np.cumsum([d == "accept" for _, d in dec]), where="post", lw=2, marker="o", ms=4,
                color=PALETTE[2], label="accepted (committed)")
        ax.step(g, np.cumsum([d != "accept" for _, d in dec]), where="post", lw=1.4, marker="x", ms=5,
                color=PALETTE[1], label="rejected")
        meta_g = [r.get("gen") for r in rows if r.get("meta_proposal")]
        for mg in meta_g:
            ax.axvline(mg, color=PALETTE[3], lw=0.8, ls=":")
        if meta_g:
            ax.plot([], [], color=PALETTE[3], ls=":", label=f"meta-proposal (policy edit) ({len(meta_g)})")
        ax.set_xlabel("generation"); ax.set_ylabel("cumulative edits"); ax.legend(fontsize=7.5, loc="upper left")
        ax.set_title("Cumulative accepted vs rejected edits")
    else:
        _nodata(ax, "decision field"); missing.append("decisions")
    # 3 held-out baseline vs final, seed spread
    ax = axes[1, 0]
    fe = meta.get("final_eval") or {}
    bars = []
    for lab, key in (("baseline\n(pre-selfmod surface)", "baseline"), ("final\n(selected surface)", "selected")):
        ps = (fe.get(key) or {}).get("J_per_seed")
        if isinstance(ps, dict) and ps:
            bars.append((lab, ps))
    provisional = False
    if not bars and isinstance(meta.get("baseline"), list):
        for i, b in enumerate(meta["baseline"]):
            ps = b.get("J_per_seed") if isinstance(b, dict) else None
            if isinstance(ps, dict) and ps:
                bars.append((f"baseline rep {i}\n(select split)", ps))
        provisional = bool(bars)
    if bars:
        seeds_all = sorted({s for _, ps in bars for s in ps}, key=str)
        for i, (lab, ps) in enumerate(bars):
            vals = [ps[s] for s in seeds_all if s in ps]
            m = float(np.mean(vals))
            ax.bar(i, m, color=PALETTE[0] if (i == 0 or provisional) else PALETTE[2], width=0.55, alpha=0.85,
                   yerr=np.std(vals) if len(vals) > 1 else None, capsize=7, ecolor=FG)
            ax.scatter(np.full(len(vals), i) + np.linspace(-0.14, 0.14, len(vals)), vals, s=16, color=FG, zorder=3)
            ax.annotate(f"mean {m:.4g}\nn={len(vals)} seeds", (i, m), textcoords="offset points", xytext=(70, 0),
                        fontsize=7.5, va="center")
        if len(bars) == 2:
            for s in seeds_all:
                if s in bars[0][1] and s in bars[1][1] and not provisional:
                    ax.plot([0, 1], [bars[0][1][s], bars[1][1][s]], color=MUTED, lw=0.6, alpha=0.6)
        lo = min(min(ps.values()) for _, ps in bars); hi = max(max(ps.values()) for _, ps in bars)
        pad = max(hi - lo, 1e-6)
        ax.set_ylim(lo - 0.6 * pad, hi + 0.6 * pad)
        ax.set_xticks(range(len(bars))); ax.set_xticklabels([b[0] for b in bars])
        ax.set_xlim(-0.6, len(bars) - 0.1)
        dj = fe.get("dJ_mean"); si = fe.get("seeds_improved")
        if provisional:
            missing.append("final held-out eval not written yet (showing preregistered baseline replicates)")
            ax.set_title(f"Baseline replicates (select split) — final held-out not written yet\n"
                         f"replicate max |ΔJ| {meta.get('replicate_max_abs_dJ', float('nan')):.3g} → min_delta "
                         f"{meta.get('min_delta', float('nan')):.3g}", fontsize=9.5)
            ax.set_ylabel("J per seed (lines join the same seed)")
        else:
          ax.set_title(f"Fresh held-out (split {fe.get('split', '?')}, seeds {fe.get('seeds', '?')})"
                     + (f"\nΔJ mean {dj:+.4g} · seeds improved {si}/{len(seeds_all)}" if dj is not None else ""),
                     fontsize=9.5)
          ax.set_ylabel("J per seed (lines join the same seed)")
    else:
        why = "run still in progress" if "finished" not in meta else "final_eval missing"
        _nodata(ax, f"run.json final_eval.baseline/selected.J_per_seed ({why})"); missing.append(f"held-out final_eval ({why})")
    # 4 lineage
    ax = axes[1, 1]
    accs = [r for r in rows if r.get("decision") == "accept"]
    base = str(meta.get("base_commit", "base"))[:7]
    if accs:
        ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
        n = len(accs) + 1
        ys = np.linspace(0.92, 0.06, n) if n > 1 else [0.5]
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        nodes = [(f"{base}  base", "")]
        for r in accs:
            pr = r.get("proposal") or {}
            ed = pr.get("edit") or {}
            sha = str(r.get("commit") or "(uncommitted: --no-commit)")[:7]
            d = f"gen {r.get('gen')} · d{r.get('depth', 0)} · {pr.get('rule', '?')}: {pr.get('module', '?')}.{pr.get('target', '?')} " \
                f"{ed.get('old', '')}→{ed.get('new', '')}"
            if r.get("mean_dJ") is not None:
                d += f" · ΔJ {r['mean_dJ']:+.3g}"
            nodes.append((sha, d))
        for i in range(1, n):
            ax.annotate("", xy=(0.06, ys[i] + 0.012), xytext=(0.06, ys[i - 1] - 0.012),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE[2], lw=1.3))
        fs = 7.5 if n <= 14 else 6.2
        for i, (sha, d) in enumerate(nodes):
            ax.scatter([0.06], [ys[i]], s=70, color=PALETTE[0] if i == 0 else PALETTE[2], zorder=3)
            ax.text(0.10, ys[i], f"{sha}   {d}"[:120], va="center", fontsize=fs, family="DejaVu Sans Mono")
        ax.set_title(f"Lineage of accepted commits ({len(accs)}) on forge branch")
    else:
        _nodata(ax, "no accepted generation yet" if rows else "generations.jsonl")
        missing.append("lineage (no accepted commits)")
    from matplotlib.ticker import MaxNLocator
    for a_ in (axes[0, 0], axes[0, 1]):
        a_.xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, out / f"{run_dir.name}__selfmod.png"), "; ".join(missing)


# ----------------------------------------------------------------- native .lqt
def render_native(run_dir: Path, out: Path) -> Tuple[Optional[Path], str]:
    lqts = sorted(run_dir.rglob("*.lqt"))
    if not lqts:
        return None, f"{run_dir.name}: no .lqt files"
    if not any(re.search(r"step_?\d+", str(q.relative_to(run_dir))) for q in lqts):
        return None, (f"only run-level .lqt ({', '.join(str(q.relative_to(run_dir)) for q in lqts)}, "
                      f"{sum(q.stat().st_size for q in lqts)} B); no per-checkpoint .lqt, so no edit-log-over-time view")
    info = _run_meta(run_dir)
    L = None
    err = ""
    try:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        import lqt_py as L  # noqa: N811
    except Exception as e:  # .so not built after a reset
        err = f"lqt_py import failed ({type(e).__name__}: {e})"
    recs = []
    for p in lqts:
        m = re.search(r"step_?(\d+)", str(p.relative_to(run_dir)))
        step = int(m.group(1)) if m else None  # run-level store (not a numbered checkpoint)
        n_edit, verified = None, None
        if L is not None:
            try:
                model = L.LqtModel.load(str(p))
                n_edit = len(model.edit_log()); verified = bool(model.verify_edit_log())
            except Exception as e:
                err = f"LqtModel.load failed on {p.name}: {e}"
        recs.append({"path": p, "step": step, "bytes": p.stat().st_size, "edits": n_edit, "verified": verified})
    fig, axes = plt.subplots(1, 2, figsize=(16, 5.6))
    fig.suptitle(f"Native LQT checkpoints — run {run_dir.name} · seed {info['seed']} · {len(lqts)} .lqt files",
                 fontsize=12.5, fontweight="bold")
    extra = [r for r in recs if r["step"] is None]       # e.g. runs/<id>/lqt_store/*.lqt, drawn apart
    recs = sorted([r for r in recs if r["step"] is not None], key=lambda r: r["step"])
    xs = [r["step"] for r in recs]
    names = sorted({r["path"].stem for r in recs})
    ax = axes[0]
    if any(r["edits"] is not None for r in recs):
        for i, nm in enumerate(names):
            sel = [(x, r) for x, r in zip(xs, recs) if r["path"].stem == nm and r["edits"] is not None]
            if sel:
                ax.plot([s[0] for s in sel], [s[1]["edits"] for s in sel], marker="o", lw=1.5,
                        label=f"{nm}" + ("" if all(s[1]["verified"] for s in sel) else " (chain FAIL)"))
        ax.set_xlabel("checkpoint step"); ax.set_ylabel("EditLog entries (hash-chained)")
        ax.set_title("LqtModel.edit_log() length over time"); ax.legend(fontsize=7)
    else:
        _nodata(ax, err or "edit logs unreadable")
    ax = axes[1]
    for i, nm in enumerate(names):
        sel = [(x, r) for x, r in zip(xs, recs) if r["path"].stem == nm]
        ax.plot([s[0] for s in sel], [s[1]["bytes"] / 1024 for s in sel], marker="s", lw=1.5, label=nm)
    ax.set_xlabel("checkpoint step"); ax.set_ylabel("file size (KiB)"); ax.set_title(".lqt checkpoint sizes")
    if recs:
        ax.legend(fontsize=7)
    xend = (max(xs) if xs else 0) + max(4, (max(xs) - min(xs)) * 0.12 if xs else 4)
    for r in extra:
        lab = f"{r['path'].relative_to(run_dir)} (run-level save)"
        if r["edits"] is not None:
            axes[0].scatter([xend], [r["edits"]], marker="D", s=40, color=PALETTE[4], zorder=3, label=lab)
            axes[0].annotate(f"{r['edits']} entries", (xend, r["edits"]), textcoords="offset points",
                             xytext=(0, 8), ha="center", fontsize=7, color=MUTED)
        axes[1].scatter([xend], [r["bytes"] / 1024], marker="D", s=40, color=PALETTE[4], zorder=3, label=lab)
        axes[1].annotate(f"{r['bytes']} B", (xend, r["bytes"] / 1024), textcoords="offset points",
                         xytext=(0, 8), ha="center", fontsize=7, color=MUTED)
    if extra:
        for a_, loc in zip(axes, ("center left", "upper left")):
            a_.legend(fontsize=7, loc=loc)
            a_.set_xlim(right=xend + 3)
    summ = _load_json(run_dir / "native_summary.json") or {}
    rb = summ.get("rollback_test")
    if isinstance(rb, dict):
        axes[0].text(0.02, 0.97, f"rollback test (native_summary.json): undid {rb.get('undone_updates')}\n"
                     f"entries {rb.get('edit_log_entries_before')} → {rb.get('edit_log_entries_after')} · "
                     f"exact={rb.get('exact')} · chain verified after={rb.get('verify_edit_log_after')}",
                     transform=axes[0].transAxes, va="top", fontsize=8, color=MUTED)
    for x, r in zip(xs, recs):
        axes[1].annotate(f"{r['bytes']} B", (x, r["bytes"] / 1024), textcoords="offset points", xytext=(0, 7),
                         ha="center", fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, out / f"{run_dir.name}__native.png"), err


# ----------------------------------------------------------------- architecture (from imports)
SCAN_DIRS = ["cognition", "runtime", "rosemary", "lqt_py", "bindings", "lqt/original-py-code",
             "lqt/recursive-tensor-cpp/python", "lqt/iala", "lqt/autodidactic-learning-substrate"]
FLAT_DIRS = ["lqt/original-py-code", "lqt/recursive-tensor-cpp/python"]  # put on sys.path by lqt_bridge
SKIP = re.compile(r"(/__pycache__/|/build/|/runs/|^runtime/viz/|/tests?/|/test_)")

# component -> (row, col) grid position; label
COMPONENTS = {
    "loop":      ("RSI loop\nruntime/loop.py · train.py", (0.42, 0.97)),
    "selfmod":   ("Self-mod gate\nruntime/selfmod · cognition/mutable", (0.80, 0.97)),
    "bridge":    ("LQT bridge\ncognition/lqt_bridge.py", (0.04, 0.76)),
    "triaxial":  ("Triaxial backbone\ntriaxial_backbone · stabilisers", (0.30, 0.76)),
    "engine":    ("Cognitive engine\ncognitive_engine · category_core", (0.56, 0.76)),
    "bayes":     ("Bayesian orchestrator\nbayesian_config_orchestrator", (0.82, 0.76)),
    "lqt":       ("LQT storage\nlqt_py/lqt_native · lqt_library\nrecursive_weights_core", (0.04, 0.52)),
    "sentinel":  ("URSMIF sentinel\nursmif_sentinel · ursmif_lobe", (0.30, 0.52)),
    "meta":      ("Meta-reflective head\nmeta_reflective_head.py", (0.56, 0.52)),
    "iala":      ("IALA\nautodidactic_learning · lqt/iala", (0.82, 0.52)),
    "rta":       ("RTA compute\nrecursive_tensor · rta_numpy\nmetacognitive_tensor", (0.04, 0.27)),
    "ethics":    ("Ethical tensor\nethical_tensor (orig + rosemary)", (0.30, 0.27)),
    "rosemary":  ("Rosemary infra\nsect agent · ntp · sis · integration", (0.56, 0.27)),
    "canon":     ("Rosemary canon (other)\nrosemary/canon/*", (0.82, 0.27)),
    "dream":     ("canon: dream", (1.06, 0.64)),
    "breath":    ("canon: breath", (1.06, 0.46)),
    "motivation": ("canon: motivation\n+ runtime/motivation_system", (1.06, 0.28)),
    "rsl":       ("canon: RSL memory", (1.06, 0.10)),
}


def _component(rel: str) -> Optional[str]:
    base = rel.rsplit("/", 1)[-1].lower()
    if rel.startswith(("runtime/selfmod/", "cognition/mutable/")):
        return "selfmod"
    if rel.endswith("__init__.py") and rel.count("/") <= 1:
        return None  # bare package markers carry no data flow
    if rel in ("runtime/loop.py", "runtime/train.py", "runtime/rosemary_full.py"):
        return "loop"
    if "dream" in base:
        return "dream"
    if "breath" in base:
        return "breath"
    if "motivation" in base:
        return "motivation"
    if rel.startswith("rosemary/") and (re.search(r"(^|_)rsl(_|\.|$)", base) or "memory" in base):
        return "rsl"
    if "autodidactic" in base:
        return "iala"
    if "bayesian" in base:
        return "bayes"
    if "ethical_tensor" in base:
        return "ethics"
    if rel == "cognition/lqt_bridge.py":
        return "bridge"
    if rel.startswith(("lqt_py/", "bindings/")) or base in ("lqt_library.py", "recursive_weights_core.py", "lqt_native"):
        return "lqt"
    if base in ("recursive_tensor.py", "rta_numpy.py", "metacognitive_tensor.py") or rel.startswith("lqt/recursive-tensor-cpp/"):
        return "rta"
    if base.startswith("trixial_tensor") or rel.startswith("lqt/original-py-code/"):
        return "lqt"
    if rel in ("cognition/triaxial_backbone.py", "cognition/corrective_stabilizers.py",
               "cognition/phase_transformations.py", "cognition/reference_matrices.py"):
        return "triaxial"
    if rel == "cognition/meta_reflective_head.py":
        return "meta"
    if "ursmif" in base:
        return "sentinel"
    if rel.startswith("cognition/"):
        return "engine"
    if rel == "runtime/bayesian_config_orchestrator.py":
        return "bayes"
    if rel == "runtime/autodidactic_learning.py" or rel.startswith(("lqt/iala/", "lqt/autodidactic-learning-substrate/")):
        return "iala"
    if rel.startswith("rosemary/canon/"):
        return "canon"
    if rel.startswith("rosemary/"):
        return "rosemary"
    return None


def _module_index() -> Dict[str, str]:
    """dotted module name (and flat names for FLAT_DIRS) -> repo-relative path."""
    idx: Dict[str, str] = {}
    for d in SCAN_DIRS:
        root = REPO / d
        if not root.exists():
            continue
        for f in root.rglob("*.py"):
            rel = f.relative_to(REPO).as_posix()
            if SKIP.search("/" + rel):
                continue
            parts = rel[:-3].split("/")
            if parts[-1] == "__init__":
                parts = parts[:-1]
            if "-" not in "/".join(parts):
                idx[".".join(parts)] = rel
            for fd in FLAT_DIRS:
                if rel.startswith(fd + "/"):
                    idx.setdefault(rel[len(fd) + 1:-3].replace("/", "."), rel)
    for so in list((REPO / "lqt_py").glob("lqt_native*.so")) if (REPO / "lqt_py").exists() else []:
        idx["lqt_native"] = "lqt_py/" + so.name
        idx["lqt_py.lqt_native"] = "lqt_py/" + so.name
    if "lqt_native" not in idx and (REPO / "bindings/lqt_native.cpp").exists():
        idx["lqt_native"] = "bindings/lqt_native.cpp"
    return idx


def _resolve(name: str, idx: Dict[str, str]) -> Optional[str]:
    while name:
        if name in idx:
            return idx[name]
        name = name.rpartition(".")[0]
    return None


def _imports_of(path: Path, rel: str) -> List[Tuple[str, List[str], int]]:
    try:
        tree = ast.parse(path.read_text(errors="replace"))
    except SyntaxError:
        return []
    pkg = rel[:-3].split("/")[:-1] if not rel.endswith("__init__.py") else rel.split("/")[:-1]
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out.append((a.name, [], node.lineno, []))
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = pkg[: len(pkg) - (node.level - 1)] if node.level > 1 else pkg
                mod = ".".join(base + ([node.module] if node.module else []))
            else:
                mod = node.module or ""
            names = [a.name for a in node.names]
            out.append((mod, names, node.lineno, [f"{mod}.{n}" if mod else n for n in names]))
        elif isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, str):
            fn = node.func
            fname = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if fname in ("import_module", "load_original", "_load_original"):
                out.append((node.args[0].value, ["(dynamic)"], node.lineno, []))
    return out


def build_import_graph() -> Tuple[Dict[Tuple[str, str], List[str]], Dict[str, List[str]]]:
    idx = _module_index()
    files_by_comp: Dict[str, List[str]] = defaultdict(list)
    edges: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    for rel in sorted(set(idx.values())):
        c = _component(rel)
        if c:
            files_by_comp[c].append(rel)
        if not rel.endswith(".py"):
            continue
        for mod, names, line, subs in _imports_of(REPO / rel, rel):
            # `from pkg import submodule` targets the submodule file(s), not pkg/__init__.py
            sub_tgts = [idx[s_] for s_ in subs if s_ in idx]
            for tgt in (sub_tgts or [_resolve(mod, idx)]):
                _add_edge(edges, c, rel, tgt, line)
    return edges, files_by_comp


def _short(rel: str) -> str:
    return "/".join(rel.split("/")[-2:])


def _add_edge(edges, c, rel, tgt, line) -> None:
    if not tgt or tgt == rel:
        return
    ct = _component(tgt)
    if c and ct and c != ct:
        tag = f"{_short(rel)}:{line} → {_short(tgt)}"
        if tag not in edges[(c, ct)]:
            edges[(c, ct)].append(tag)


def _clip_to_box(c, toward, hw, hh):
    """Point where the ray c->toward leaves the rectangle of half-size (hw, hh) around c."""
    dx, dy = toward[0] - c[0], toward[1] - c[1]
    if dx == 0 and dy == 0:
        return c
    t = min(hw / abs(dx) if dx else np.inf, hh / abs(dy) if dy else np.inf)
    return (c[0] + dx * t, c[1] + dy * t)


def render_architecture(out: Path) -> Tuple[Path, Dict[str, Any]]:
    edges, files = build_import_graph()
    fig = plt.figure(figsize=(26, 14))
    ax = fig.add_axes([0.005, 0.03, 0.60, 0.86]); ax.set_xlim(-0.08, 1.17); ax.set_ylim(0.02, 1.04)
    ax.axis("off")
    fig.suptitle("RSI biocognitive stack — data flow from real imports "
                 "(AST of cognition/, runtime/, rosemary/, lqt*, incl. load_original()/import_module() literals)\n"
                 "solid box = files exist · dashed = no file matched yet · arrow = importer → imported · #n = evidence at right",
                 fontsize=13.5, fontweight="bold", y=0.985)
    W, H = 0.17, 0.085
    keys = list(COMPONENTS)
    for key, (label, (x, y)) in COMPONENTS.items():
        present = bool(files.get(key))
        col = PALETTE[keys.index(key) % len(PALETTE)]
        ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.004,rounding_size=0.012",
                                    fc=PANEL if present else BG, ec=col if present else MUTED,
                                    lw=1.8 if present else 1.0, ls="-" if present else (0, (4, 3)), zorder=2))
        n = len(files.get(key, []))
        ax.text(x, y + 0.006, label, ha="center", va="center", fontsize=8, zorder=3,
                color=FG if present else MUTED, linespacing=1.2)
        ax.text(x + W / 2 - 0.006, y - H / 2 + 0.006, f"{n} file{'s' if n != 1 else ''}", ha="right",
                va="bottom", fontsize=6.5, color=MUTED, zorder=3)
    fig.canvas.draw()
    T = ax.transData; Ti = T.inverted()
    pairs = sorted(edges, key=lambda e: (keys.index(e[0]), keys.index(e[1])))
    legend = []
    placed: List[Tuple[float, float]] = []
    for i, (a, b) in enumerate(pairs, 1):
        ca, cb = COMPONENTS[a][1], COMPONENTS[b][1]
        pa = _clip_to_box(ca, cb, W / 2 + 0.006, H / 2 + 0.008)
        pb = _clip_to_box(cb, ca, W / 2 + 0.006, H / 2 + 0.008)
        rad = 0.22 if (b, a) in edges else 0.08
        col = PALETTE[keys.index(a) % len(PALETTE)]
        ax.add_patch(FancyArrowPatch(pa, pb, arrowstyle="-|>", mutation_scale=15,
                                     connectionstyle=f"arc3,rad={rad}", color=col,
                                     lw=1.0 + 0.3 * min(len(edges[(a, b)]), 5), alpha=0.85, zorder=1,
                                     shrinkA=0, shrinkB=0))
        # label on the arc (quadratic Bezier, display space like arc3), at the t nearest the middle
        # that is clear of every box and every earlier label
        (x1, y1), (x2, y2) = T.transform(pa), T.transform(pb)
        cx, cy = (x1 + x2) / 2 + rad * (y2 - y1), (y1 + y2) / 2 - rad * (x2 - x1)
        best = None
        for t in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.18, 0.82, 0.12, 0.88):
            mx = (1 - t) ** 2 * x1 + 2 * t * (1 - t) * cx + t ** 2 * x2
            my = (1 - t) ** 2 * y1 + 2 * t * (1 - t) * cy + t ** 2 * y2
            q = Ti.transform((mx, my))
            in_box = any(abs(q[0] - bx) < W / 2 + 0.012 and abs(q[1] - by) < H / 2 + 0.012
                         for _, (bx, by) in COMPONENTS.values())
            near = any(abs(q[0] - u) < 0.03 and abs(q[1] - v) < 0.02 for u, v in placed)
            if best is None:
                best = q
            if not in_box and not near:
                best = q; break
        placed.append(tuple(best))
        lx_, ly_ = best
        ax.text(lx_, ly_, f"#{i}", fontsize=7.5, color=col, ha="center", va="center", zorder=5,
                fontweight="bold", bbox=dict(boxstyle="round,pad=0.18", fc=BG, ec=col, lw=0.6, alpha=0.95))
        legend.append((i, COMPONENTS[a][0].split("\n")[0], COMPONENTS[b][0].split("\n")[0], edges[(a, b)], col))
    # evidence panel: two columns
    cols = [fig.add_axes([0.615, 0.03, 0.19, 0.86]), fig.add_axes([0.805, 0.03, 0.19, 0.86])]
    for c in cols:
        c.axis("off"); c.set_xlim(0, 1); c.set_ylim(0, 1)
    cols[0].text(0, 1.0, "Import evidence (file:line → imported file)", fontsize=10.5, fontweight="bold", va="top")
    step_h, ev_h, maxev = 0.0185, 0.0158, 2
    col_i, y = 0, 0.965
    for i, sa, sb, ev, col in legend:
        need = step_h + ev_h * (min(len(ev), maxev) + (len(ev) > maxev)) + 0.006
        if y - need < 0 and col_i == 0:
            col_i, y = 1, 0.965
        c = cols[col_i]
        if y - need < 0:
            c.text(0, y, "… (truncated)", fontsize=7, color=MUTED, va="top"); break
        c.text(0, y, f"#{i}  {sa} → {sb}", fontsize=7.6, fontweight="bold", color=col, va="top"); y -= step_h
        for e in ev[:maxev]:
            c.text(0.03, y, e if len(e) <= 64 else e[:61] + "…", fontsize=6.4, color=FG, alpha=0.8,
                   va="top", family="DejaVu Sans Mono"); y -= ev_h
        if len(ev) > maxev:
            c.text(0.03, y, f"+{len(ev) - maxev} more (render_report.json)", fontsize=6.3, color=MUTED, va="top"); y -= ev_h
        y -= 0.006
    absent = [COMPONENTS[k][0].split("\n")[0] for k in COMPONENTS if not files.get(k)]
    if absent:
        ax.text(-0.07, 0.03, "No file matched yet: " + ", ".join(absent), fontsize=8.5, color=MUTED, va="bottom")
    p = _save(fig, out / "architecture.png")
    return p, {"edges": {f"{a}->{b}": v for (a, b), v in edges.items()},
               "files": {k: v for k, v in files.items()}, "absent": absent}


# ----------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=str(REPO / "runtime/runs"))
    ap.add_argument("--out", default=str(REPO / "runtime/viz/out"))
    a = ap.parse_args(argv)
    runs_dir, out = Path(a.runs_dir), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    report: Dict[str, Any] = {"pngs": [], "missing": []}
    run_dirs = sorted(d for d in runs_dir.iterdir() if d.is_dir()) if runs_dir.exists() else []
    train_dirs = []
    for d in run_dirs:
        if (d / "metrics.jsonl").exists():
            p = render_dashboard(d, out)
            if p:
                report["pngs"].append(str(p)); train_dirs.append(d)
            else:
                report["missing"].append(f"{d.name}: metrics.jsonl empty")
        if "selfmod" in d.name or (d / "generations.jsonl").exists():
            p, miss = render_selfmod(d, out)
            if p:
                report["pngs"].append(str(p))
            if miss:
                report["missing"].append(f"{d.name} selfmod: {miss}")
        if "native" in d.name or any(d.rglob("*.lqt")):
            p, miss = render_native(d, out)
            if p:
                report["pngs"].append(str(p))
            if miss:
                report["missing"].append(f"{d.name} native: {miss}")
    p = render_compare(train_dirs, out)
    if p:
        report["pngs"].append(str(p))
    p, arch = render_architecture(out)
    report["pngs"].append(str(p)); report["architecture"] = arch
    (out / "render_report.json").write_text(json.dumps(report, indent=2))
    for x in report["pngs"]:
        print("PNG", x)
    for m in report["missing"]:
        print("MISSING", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
