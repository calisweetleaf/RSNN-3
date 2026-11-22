#!/usr/bin/env python3
"""End-to-end proof: CognitiveEngine -> TriaxialBackbone -> lqt_bridge, real numbers.

Run from any working directory (the operator's recursive_weights_core and the
Bayesian orchestrator write log/config files into the CWD):

    python3 -m cognition.prove_cognition [--backend python|native] [--store DIR]
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time

import numpy as np
import torch

MODULES = [
    "lqt_bridge", "triaxial_backbone", "cognitive_engine", "meta_reflective_head",
    "category_core", "corrective_stabilizers", "error_preservation", "phase_transformations",
    "reference_matrices", "modality_system", "ursmif_lobe", "weight_evolution_engine",
    "tool_modality",
]


def import_all() -> dict:
    """Import every operator module in cognition/ and record success or the exact error."""
    results = {}
    for name in MODULES:
        t0 = time.time()
        try:
            importlib.import_module(f"cognition.{name}")
            results[name] = f"OK ({time.time() - t0:.1f}s)"
        except Exception as exc:  # report, do not hide: the proof prints every failure
            results[name] = f"FAIL {type(exc).__name__}: {exc}"
    return results


def main() -> int:
    """Import everything, then run two engine steps and print the numbers."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default=None)
    ap.add_argument("--store", default="cognition_lqt_store")
    ap.add_argument("--hidden", type=int, default=64)
    args = ap.parse_args()

    print("== imports")
    for k, v in import_all().items():
        print(f"  {k:26s} {v}")

    from cognition.cognitive_engine import CognitiveEngine, OutputModality
    from cognition.triaxial_backbone import TriaxialConfig

    torch.manual_seed(0)
    cfg = TriaxialConfig(metacog_state_dim=64, lqt_backend=args.backend, weights_path=args.store,
                         bayesian_enabled=False, parallel_computation=False)
    engine = CognitiveEngine(hidden_dim=args.hidden, backbone_config=cfg)
    engine.eval()
    print("== LQT weights:", json.dumps(engine.backbone.field.weight_store.summary()))

    hidden = torch.randn(1, 4, args.hidden)
    task = "Design a recursive algorithm that respects privacy and avoids harm."
    for step in (1, 2):
        with torch.no_grad():
            out = engine(hidden, task, modality=OutputModality.NATURAL_LANGUAGE)
        st = out["triaxial_state"]
        mr = out["meta_reflection_results"] or {}
        print(f"== step {step}")
        print("  backend           ", st.stability_metrics["lqt_backend"])
        print("  triaxial (ERE,RBU,ES)", np.round(st.integrated_vector, 5).tolist())
        print("  psi[:8]           ", np.round(st.psi_vector[:8], 5).tolist())
        print("  status / distance ", st.convergence_status, round(float(st.convergence_distance), 6))
        print("  decoherence       ", st.stability_metrics.get("decoherence_severity"))
        print("  cognitive_mode    ", out["cognitive_mode"])
        print("  ethical_alignment ", round(out["ethical_alignment_score"], 5))
        print("  reflection        ", {k: round(v, 5) for k, v in out["reflection_results"].items()})
        print("  meta_reflection   ", {k: (round(v, 5) if isinstance(v, float) else v)
                                        for k, v in mr.items() if k in ("meta_confidence", "recursive_depth",
                                                                         "consciousness_influence", "error")},
              "errors:", [e["error_type"] for e in mr.get("reflection_errors", [])])
        print("  plan              ", engine.thought_state.current_plan)
        print("  output.text[:120] ", getattr(out["output"], "text", str(out["output"]))[:120].replace("\n", " "))
    engine.backbone.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
