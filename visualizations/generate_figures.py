#!/usr/bin/env python3
"""Generate publication figures from RSNN-3 run artifacts (no synthetic points)."""

from __future__ import annotations

import difflib
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runtime" / "runs" / "rsnn3_release_seed1"
OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, GRID = "#070A12", "#0E1423", "#26324A"
FG, MUTED = "#F3F6FF", "#9AA8C1"
CYAN, VIOLET, GOLD, GREEN, RED = "#45D7FF", "#9B7BFF", "#FFCA58", "#55E39A", "#FF6B7A"
PHASES = ["INHALE", "HOLD", "EXHALE", "PAUSE_FALLING", "REST", "DREAM", "PAUSE_RISING"]
PHASE_COLORS = [CYAN, "#77B8FF", VIOLET, "#C875FF", "#60708F", "#FF6FD8", GOLD]


def load_rows():
    return [json.loads(line) for line in (RUN / "metrics.jsonl").read_text().splitlines() if line.strip()]


def load_rsei_rows():
    rows = []
    for line in (RUN / "chat" / "transcript.jsonl").read_text().splitlines():
        record = json.loads(line).get("record", {})
        if "rsei_dim" in record:
            rows.append(record)
    return rows


def setup():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
        "text.color": FG, "axes.labelcolor": FG, "axes.edgecolor": GRID,
        "xtick.color": MUTED, "ytick.color": MUTED, "grid.color": GRID,
        "font.family": "DejaVu Sans", "font.size": 11, "axes.titleweight": "bold",
    })


def polish(ax, title, ylabel=None, xlabel="Training cycle"):
    ax.set_title(title, loc="left", fontsize=14, pad=12)
    ax.grid(True, alpha=.45, linewidth=.7)
    ax.spines[["top", "right"]].set_visible(False)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def evidence(rows):
    x = np.array([r["step"] for r in rows])
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), constrained_layout=True)
    fig.suptitle("RSNN-3 · Empirical recursive-learning run", fontsize=22, fontweight="bold")
    ax = axes[0, 0]
    ax.plot(x, [r["iala_entities"] for r in rows], color=CYAN, lw=2.2, label="Knowledge entities")
    ax.plot(x, [r["iala_belief_states"] for r in rows], color=VIOLET, lw=1.8, label="Belief states")
    polish(ax, "Knowledge substrate growth", "Persistent states")
    ax.legend(frameon=False, labelcolor=FG)
    ax.annotate(f"{rows[-1]['iala_entities']} entities", (x[-1], rows[-1]["iala_entities"]),
                xytext=(-90, 10), textcoords="offset points", color=CYAN)

    ax = axes[0, 1]
    k = np.array([r["knowledge_influence_norm"] for r in rows])
    rw = np.array([r["recursive_influence_norm"] for r in rows])
    ax.plot(x, k, color=GREEN, lw=1.5, label="Recalled knowledge → cognition")
    ax.plot(x, rw, color=GOLD, lw=1.5, label="Recursive weights → cognition")
    polish(ax, "Measured forward-path influence", "Vector influence norm")
    ax.legend(frameon=False, labelcolor=FG)
    ax.text(.02, .94, f"knowledge active {np.count_nonzero(k)}/{len(k)} cycles  ·  recursive weights {np.count_nonzero(rw)}/{len(rw)}",
            transform=ax.transAxes, va="top", color=MUTED)

    ax = axes[1, 0]
    ax.plot(x, [r["lqt_edit_log"] for r in rows], color=VIOLET, lw=2.2, label="Verified edit-log entries")
    ax2 = ax.twinx()
    ax2.plot(x, [r["lqt_tensors"] for r in rows], color=CYAN, lw=1.8, label="Unified tensors")
    polish(ax, "Unified LQT model accumulation", "Cumulative edit-log entries")
    ax2.set_ylabel("Live tensors", color=CYAN); ax2.tick_params(axis="y", colors=CYAN)
    lines = ax.lines + ax2.lines
    ax.legend(lines, [l.get_label() for l in lines], frameon=False, labelcolor=FG)

    ax = axes[1, 1]
    vals = np.array([[r["reflection_quality"], r["reflection_novelty"], r["reflection_alignment"],
                      r["reflection_confidence"], r["meta_confidence"]] for r in rows])
    labels = ["Quality", "Novelty", "Alignment", "Confidence", "Meta-confidence"]
    for i, (label, color) in enumerate(zip(labels, [CYAN, VIOLET, GREEN, GOLD, RED])):
        ax.plot(x, vals[:, i], lw=1.25, color=color, label=label, alpha=.92)
    polish(ax, "Cognitive self-measurement", "Score [0, 1]")
    ax.set_ylim(.35, .65); ax.legend(ncol=3, frameon=False, labelcolor=FG)
    save(fig, "01_recursive_learning_evidence")


def self_modification(rows):
    x = np.array([r["step"] for r in rows])
    fig, axes = plt.subplots(2, 1, figsize=(16, 9), constrained_layout=True,
                             gridspec_kw={"height_ratios": [1, 1.25]})
    fig.suptitle("RSNN-3 · Recursive self-modification recorded in LQT", fontsize=22, fontweight="bold")
    ax = axes[0]
    for key, label, color in [("dW_W_R", "Reasoning field W_R", CYAN),
                              ("dW_W_E", "Ethical field W_E", GREEN),
                              ("dW_W_M", "Metacognitive field W_M", VIOLET)]:
        ax.semilogy(x, np.maximum(np.abs([r[key] for r in rows]), 1e-12), color=color, lw=1.5, label=label)
    polish(ax, "Per-cycle weight displacement", "‖ΔW‖₂ (log scale)")
    ax.legend(ncol=3, frameon=False, labelcolor=FG)

    ax = axes[1]
    signals = np.array([[abs(r["mod_scale"]), abs(r["dW_W_R"]), abs(r["dW_W_E"]), abs(r["dW_W_M"]),
                         max(r["lqt_elements_changed"], 1)] for r in rows]).T
    normalized = signals / np.maximum(signals.max(axis=1, keepdims=True), 1e-12)
    im = ax.imshow(normalized, aspect="auto", interpolation="nearest", cmap="magma", vmin=0, vmax=1,
                   extent=[x[0]-.5, x[-1]+.5, 4.5, -.5])
    ax.set_yticks(range(5), ["modulation scale", "ΔW_R", "ΔW_E", "ΔW_M", "LQT elements changed"])
    ax.set_xlabel("Training cycle"); ax.set_title("Coupled mutation activity (each row normalized to its observed maximum)", loc="left", fontsize=14, pad=12)
    cb = fig.colorbar(im, ax=ax, pad=.01); cb.set_label("Relative activity")
    save(fig, "02_lqt_self_modification")


def triaxial(rows):
    x = np.array([r["step"] for r in rows])
    fig = plt.figure(figsize=(16, 9), constrained_layout=True)
    fig.suptitle("RSNN-3 · Triaxial cognitive field trajectory", fontsize=22, fontweight="bold")
    ax = fig.add_subplot(121, projection="3d")
    ere, rbu, es = (np.array([r[k] for r in rows]) for k in ("ere", "rbu", "es"))
    ax.plot(ere, rbu, es, color=MUTED, lw=.8, alpha=.6)
    sc = ax.scatter(ere, rbu, es, c=x, cmap="plasma", s=22, depthshade=False)
    ax.scatter([ere[0]], [rbu[0]], [es[0]], color=GREEN, s=85, marker="o", label="start")
    ax.scatter([ere[-1]], [rbu[-1]], [es[-1]], color=RED, s=95, marker="X", label="end")
    ax.set_xlabel("ERE"); ax.set_ylabel("RBU"); ax.set_zlabel("ES")
    ax.set_title("State path across reasoning · belief · stabilization", loc="left", fontsize=14)
    ax.legend(frameon=False, labelcolor=FG); cb = fig.colorbar(sc, ax=ax, shrink=.65, pad=.08); cb.set_label("Cycle")
    ax.set_facecolor(PANEL)

    ax2 = fig.add_subplot(122)
    ax2.plot(x, ere, color=CYAN, label="ERE", lw=1.5)
    ax2.plot(x, rbu, color=VIOLET, label="RBU", lw=1.5)
    ax2.plot(x, es, color=GOLD, label="ES", lw=1.5)
    ax2.plot(x, [r["convergence_distance"] for r in rows], color=GREEN, label="Convergence distance", lw=1.2)
    polish(ax2, "Axes and convergence over recursive cycles", "Field value")
    ax2.legend(ncol=2, frameon=False, labelcolor=FG)
    save(fig, "03_triaxial_cognitive_dynamics")


def breath(rows):
    metrics = ["reflection_quality", "reflection_novelty", "ethical_alignment", "meta_confidence",
               "knowledge_influence_norm", "recursive_influence_norm", "motivation_drive"]
    labels = ["Reflection quality", "Novelty", "Ethical alignment", "Meta-confidence",
              "Knowledge influence", "Recursive influence", "Motivation"]
    matrix = np.array([[np.mean([r[m] for r in rows if r["iala_phase"] == p]) for m in metrics] for p in PHASES])
    z = (matrix - matrix.mean(axis=0)) / np.maximum(matrix.std(axis=0), 1e-9)
    fig, axes = plt.subplots(2, 1, figsize=(16, 8.5), constrained_layout=True,
                             gridspec_kw={"height_ratios": [.35, 1]})
    fig.suptitle("RSNN-3 · Seven-phase breath coupling", fontsize=22, fontweight="bold")
    ax = axes[0]
    phase_idx = [PHASES.index(r["iala_phase"]) for r in rows]
    ax.imshow(np.array(phase_idx)[None, :], aspect="auto", cmap=plt.matplotlib.colors.ListedColormap(PHASE_COLORS),
              vmin=0, vmax=6, interpolation="nearest")
    ax.set_yticks([]); ax.set_xlabel("Training cycle"); ax.set_title("Phase schedule · 20 cycles in every phase", loc="left", fontsize=14)
    ax.set_xticks(np.linspace(0, len(rows)-1, 8), [str(int(v)+1) for v in np.linspace(0, len(rows)-1, 8)])
    ax = axes[1]
    im = ax.imshow(z, aspect="auto", cmap="coolwarm", vmin=-2, vmax=2)
    ax.set_xticks(range(len(labels)), labels, rotation=25, ha="right")
    ax.set_yticks(range(len(PHASES)), [p.replace("_", " ").title() for p in PHASES])
    ax.set_title("Phase-conditioned metric means (z-score within each metric)", loc="left", fontsize=14, pad=12)
    for i in range(z.shape[0]):
        for j in range(z.shape[1]): ax.text(j, i, f"{z[i,j]:+.2f}", ha="center", va="center", fontsize=9, color=FG)
    cb = fig.colorbar(im, ax=ax, pad=.01); cb.set_label("Standard deviations from metric mean")
    save(fig, "04_breath_phase_coupling")


def voice():
    report = json.loads((RUN / "native_voice_training.json").read_text())
    curve = np.array(report["loss_curve"])
    evals = report["evaluations"]
    similarity = np.array([difflib.SequenceMatcher(None, e["target"], e["generated"]).ratio() for e in evals])
    fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), constrained_layout=True)
    fig.suptitle("RSNN-3 · Native voice grounding", fontsize=22, fontweight="bold")
    ax = axes[0]
    ax.semilogy(np.arange(1, len(curve)+1), curve, color=CYAN, lw=1.8)
    ax.axhline(1.25, color=GOLD, ls="--", lw=1.2, label="Runtime readiness gate")
    polish(ax, "Denoising next-byte + cognitive-grounding objective", "Training loss (log scale)", "Optimizer update")
    ax.legend(frameon=False, labelcolor=FG)
    ax.annotate(f"{curve[0]:.3f} → {curve[-1]:.4f}", (len(curve), curve[-1]), xytext=(-110, 18),
                textcoords="offset points", color=CYAN)
    ax = axes[1]
    bars = ax.barh(np.arange(len(similarity)), similarity, color=[GREEN if s == 1 else VIOLET for s in similarity])
    ax.set_yticks(np.arange(len(similarity)), [f"Grounding {i+1}" for i in range(len(similarity))])
    ax.invert_yaxis(); ax.set_xlim(0, 1.03)
    polish(ax, "Free-running reproduction after restart-safe training", "Sequence similarity", xlabel="Target ↔ generated similarity")
    for bar, s in zip(bars, similarity): ax.text(min(s+.015, .96), bar.get_y()+bar.get_height()/2, f"{s:.0%}", va="center", color=FG)
    save(fig, "05_native_voice_learning")


def capability(rows):
    x = np.arange(1, len(rows) + 1)
    dims = np.array([r["rsei_dim"] for r in rows])
    drives = np.array([r["motivation_drive"] for r in rows])
    probes = np.array([r.get("rsei_probe_score") or 0.0 for r in rows])
    params = np.array([r["bayesian_parameter_count"] for r in rows])
    strict = np.array([bool((r.get("rsei_event") or {}).get("strict_expansion")) for r in rows])
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), constrained_layout=True)
    fig.suptitle("RSNN-3 · Externally verified capability expansion", fontsize=22, fontweight="bold")

    ax = axes[0, 0]
    ax.step(x, dims, where="post", color=CYAN, lw=2.4, label="Exact verified dimension")
    ax.scatter(x[strict], dims[strict], color=GREEN, s=42, zorder=3, label="Strict expansion rewarded")
    ax.axhline(12, color=GOLD, ls="--", lw=1.1, label="Competence DAG size")
    polish(ax, "Capability is a reachable count—not a branching bound", "Verified competences", "Live RSEI cycle")
    ax.set_ylim(-.3, 12.8); ax.legend(frameon=False, labelcolor=FG)

    ax = axes[0, 1]
    ax.plot(x, drives, color=VIOLET, lw=2.2, label="RSEI motivation drive")
    ax.axhline(.5, color=MUTED, ls="--", lw=1.2, label="No-signal baseline")
    failed = probes < .8
    ax.scatter(x[failed], drives[failed], color=RED, marker="x", s=45, label="Probe failed · no expansion")
    polish(ax, "Reward responds to verified outcomes", "Drive", "Live RSEI cycle")
    ax.set_ylim(.45, .82); ax.legend(frameon=False, labelcolor=FG)

    ax = axes[1, 0]
    ax.step(x, params, where="post", color=GOLD, lw=2.2)
    ax.fill_between(x, 3, params, step="post", color=GOLD, alpha=.16)
    ax.axhline(3, color=MUTED, ls="--", lw=1.0)
    polish(ax, "Liquid Bayesian parameter growth", "Materialized belief parameters", "Live RSEI cycle")
    ax.text(.02, .94, f"3 bootstrap + {params[-1]-3} competence beliefs", transform=ax.transAxes,
            va="top", color=MUTED)

    ax = axes[1, 1]
    names = [r["rsei_goal"].replace("_", " ") for r in rows]
    colors = [GREEN if ok else RED for ok in strict]
    ax.barh(x, probes, color=colors, alpha=.9)
    ax.axvline(.8, color=GOLD, ls="--", lw=1.2, label="External pass threshold")
    ax.set_yticks(x, names, fontsize=8); ax.invert_yaxis(); ax.set_xlim(0, 1.05)
    polish(ax, "Held-out runtime probe per selected frontier goal", "Probe score", "External verification score")
    ax.legend(frameon=False, labelcolor=FG)
    save(fig, "06_rsei_verified_capability")


def manifest(rows, rsei_rows):
    files = [RUN / "metrics.jsonl", RUN / "chat" / "transcript.jsonl",
             RUN / "native_voice_training.json", RUN / "rsei_live_validation.json",
             RUN / "run.json", RUN / "model.lqt"]
    data = {
        "title": "RSNN-3 empirical visualization provenance",
        "run": str(RUN.relative_to(ROOT)),
        "observations": len(rows),
        "claims": {
            "iala_learn_success": sum(bool(r["iala_learn_success"]) for r in rows),
            "knowledge_active_cycles": sum(r["knowledge_influence_norm"] > 0 for r in rows),
            "recursive_weight_active_cycles": sum(r["recursive_influence_norm"] > 0 for r in rows),
            "final_knowledge_entities": rows[-1]["iala_entities"],
            "final_belief_states": rows[-1]["iala_belief_states"],
            "final_lqt_tensors": rows[-1]["lqt_tensors"],
            "final_verified_edit_entries": rows[-1]["lqt_edit_log"],
            "all_seven_phases": sorted(set(r["iala_phase"] for r in rows)),
            "rsei_live_cycles": len(rsei_rows),
            "rsei_verified_dimension": rsei_rows[-1]["rsei_dim"],
            "rsei_verified_competences": rsei_rows[-1]["rsei_verified"],
            "rsei_strict_expansions": sum(bool((r.get("rsei_event") or {}).get("strict_expansion")) for r in rsei_rows),
            "rsei_final_drive": rsei_rows[-1]["motivation_drive"],
            "dynamic_bayesian_parameters": rsei_rows[-1]["bayesian_parameter_count"],
            "dream_memories_integrated": rsei_rows[-1].get("dream_memories_integrated", 0),
        },
        "sources": {str(p.relative_to(ROOT)): {"bytes": p.stat().st_size,
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files},
        "figures": sorted(p.name for p in OUT.iterdir() if p.suffix in {".png", ".svg"}),
    }
    (OUT / "figure_manifest.json").write_text(json.dumps(data, indent=2))


def main():
    setup(); rows, rsei_rows = load_rows(), load_rsei_rows()
    evidence(rows); self_modification(rows); triaxial(rows); breath(rows); voice(); capability(rsei_rows)
    manifest(rows, rsei_rows)
    print(json.dumps({"figures": len(list(OUT.glob('*.png'))), "output": str(OUT)}, indent=2))


if __name__ == "__main__": main()
