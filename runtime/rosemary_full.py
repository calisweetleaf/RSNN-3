#!/usr/bin/env python3
"""RSI loop with the operator's canon modules active (``rosemary.canon``).

Extends :class:`runtime.loop.RSILoop` (engine -> SECT sentinel -> Bayesian update ->
motivation -> IALA -> LQT self-modification) with four canon systems, each driven by
the step instead of a wall-clock thread so a seeded run is reproducible:

* **Breath** -- ``rosemary.canon.breath_phase.SacredBreathSynchronizer``. Every step
  advances the master oscillator by ``breath_dt`` (``update_phase``); the dominant
  canon phase (INHALE, PAUSE_RISING, HOLD, PAUSE_FALLING, EXHALE, REST, DREAM) is
  passed into the cognitive engine's triaxial backbone as its 4-phase ethical
  ``BreathPhase`` (mapping in ``CANON_TO_TRIAXIAL``), and the step's Psi vector is
  modulated through ``synchronize_component('memory_core', psi)``. Contradictions
  the SECT sentinel finds are reported to the synchronizer.
* **Memory** -- ``rosemary.canon.rsl_memory_system.EnhancedRSLMemorySystem``. Each
  passage is stored as an episodic memory with the IALA ethical features as its
  ``ethical_context`` (the five keys line up: good_harm, truth_deception,
  fairness_bias, liberty_constraint, care_harm). On REST steps the MRC-FPE
  ``update_consciousness_state`` runs with the step's meta confidence.
* **Dream** -- ``rosemary.canon.dream_simulation.DreamSimulationEngine``. When the
  breath enters DREAM, a portal is offered from the recent steps (emotions,
  experiences); the loop enters when the canon receptivity is >= ``dream_consent``,
  advances by dream logic while DREAM lasts, and on leaving DREAM exits with
  ``integrate_memories=True``; each integrated dream memory is stored in RSL memory
  (``memory_type='dream'``) and given to motivation as an ``Experience``.
* **Motivation** -- ``rosemary.canon.motivation_system.EmergentMotivationSystem``
  replaces the runtime copy, so experiences are embedded by the canon
  ``SacredFBS_Tokenizer`` (``rosemary.canon.fbs_tokenizer``).

The phase mapping, the consent threshold and the per-step wiring are this lane's
integration choices, not operator spec. CLI::

    python3 -m runtime.rosemary_full --steps 40 --seed 0 --out runtime/runs/<date>_canon_seed0
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.loop import LoopConfig, RSILoop  # noqa: E402

logger = logging.getLogger("runtime.rosemary_full")

# canon 7-phase breath -> triaxial ethical 4-phase breath (by phase meaning)
CANON_TO_TRIAXIAL = {
    "INHALE": "INHALE",
    "PAUSE_RISING": "HOLD_IN",
    "HOLD": "HOLD_IN",
    "PAUSE_FALLING": "EXHALE",
    "EXHALE": "EXHALE",
    "REST": "HOLD_OUT",
    "DREAM": "HOLD_OUT",
}
ETHICAL_KEYS = ("good_harm", "truth_deception", "fairness_bias", "liberty_constraint", "care_harm")


@dataclass
class RosemaryFullConfig(LoopConfig):
    """LoopConfig plus the canon systems' knobs."""

    breath_dt: float = 1.0          # oscillator advance per step (velocity 0.05 -> 20 steps/cycle)
    dream_consent: float = 0.5      # enter the dream when canon receptivity >= this
    rest_consciousness: bool = True  # run the MRC-FPE update_consciousness_state on REST steps


class RosemaryFullLoop(RSILoop):
    """RSILoop with canon breath, RSL memory, dream simulation and canon motivation."""

    def __init__(self, cfg: RosemaryFullConfig):
        super().__init__(cfg)
        self._rsei_full_runtime = True
        from cognition.triaxial_backbone import BreathPhase as TriaxialBreath
        from rosemary.canon.breath_phase import SacredBreathSynchronizer
        from rosemary.canon.dream_simulation import DreamSimulationEngine
        from rosemary.canon import fbs_tokenizer as canon_fbs
        from rosemary.canon import motivation_system as canon_motivation
        from rosemary.canon.rsl_memory_system import EnhancedRSLMemorySystem, create_enhanced_rsl_config

        if canon_motivation.SacredFBS_Tokenizer is not canon_fbs.SacredFBS_Tokenizer:
            raise RuntimeError("canon motivation_system did not bind rosemary.canon.fbs_tokenizer")
        self.motivation = canon_motivation.EmergentMotivationSystem()
        self._Experience = canon_motivation.Experience
        self.rsei.motivation = self.motivation
        self.motivation.bind_rsei(self.rsei.engine)
        self.rsei._sync_motivation_objects()

        # harmonic tensor width = Psi width, so synchronize_component can modulate Psi
        self.psi_dim = int(self.field.W["W_R"].shape[0])
        self.breath = SacredBreathSynchronizer(state_dim=self.psi_dim)
        self.breath.initialize({"rsi_loop": self})
        self._TriaxialBreath = TriaxialBreath

        self.dream = DreamSimulationEngine()
        self.dream_log: List[Dict[str, Any]] = []

        self.memory = EnhancedRSLMemorySystem(create_enhanced_rsl_config())  # canon defaults

        # Engine I/O through torch module hooks: inject the breath phase, capture the output.
        self._engine_breath = None
        self._engine_out: Optional[Dict[str, Any]] = None
        self.engine.register_forward_pre_hook(self._inject_breath, with_kwargs=True)
        self.engine.register_forward_hook(self._capture_output)
        self._recent: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------ hooks

    def _inject_breath(self, module, args, kwargs):
        if self._engine_breath is not None:
            kwargs = dict(kwargs)
            kwargs["breath_phase"] = self._engine_breath
        return args, kwargs

    def _capture_output(self, module, args, output):
        self._engine_out = output

    # ------------------------------------------------------------------ motivation

    def _motivation_stats(self) -> Dict[str, Any]:
        vfs = self.motivation.value_formation_system
        return {
            "motivation_experiences": len(vfs.experiences),
            "motivation_patterns": len(vfs.patterns),
            "motivation_proto_values": len(getattr(vfs, "proto_values", {})),
            "motivation_emerging_values": len(getattr(vfs, "emerging_values", {})),
            "motivation_full_values": len(getattr(vfs, "values", {})),
            "motivation_formation_stats": dict(getattr(vfs, "formation_statistics", {})),
        }

    # ------------------------------------------------------------------ dream

    def _dream_state(self) -> Dict[str, Any]:
        """Canon dream ``current_state`` from the last steps."""
        last = self._recent[-1] if self._recent else {}
        adv = float(last.get("advantage", 0.0))
        emotions = {
            "WONDER": float(np.clip(last.get("reflection_novelty", 0.0), 0.0, 1.0)),
            "JOY": float(np.clip(2.0 * adv, 0.0, 1.0)),
            "SORROW": float(np.clip(-2.0 * adv, 0.0, 1.0)),
            "TENSION": float(np.clip(last.get("contradiction_severity", 0.0), 0.0, 1.0)),
            "PEACE": float(np.clip(last.get("ethical_alignment", 0.0), 0.0, 1.0)),
        }
        experiences = [{
            "name": r["passage"],
            "description": f'{r["cognitive_mode"]} on {r["passage"]}',
            "significance": float(np.clip(r.get("reflection_novelty", 0.0), 0.0, 1.0)),
            "emotional_tone": float(np.clip(r.get("reflection_quality", 0.5), 0.0, 1.0)),
        } for r in self._recent[-5:]]
        return {
            "emotions": emotions,
            "recent_experiences": experiences,
            "tiredness": min(1.0, self.step_index / 40.0),
            "stress": float(np.clip(last.get("contradiction_severity", 0.0), 0.0, 1.0)),
            "curiosity": float(np.clip(last.get("reflection_novelty", 0.0), 0.0, 1.0)),
        }

    def _dream_step(self, phase: str) -> Dict[str, Any]:
        out: Dict[str, Any] = {"dream_active": self.dream.dream_active, "dream_event": None}
        if phase == "DREAM" and not self.dream.dream_active:
            state = self._dream_state()
            offer = self.dream.offer_dream_portal(state)
            out["dream_receptivity"] = float(offer.get("current_receptivity", 0.0))
            out["dream_themes"] = offer.get("potential_themes", [])
            if out["dream_receptivity"] >= self.cfg.dream_consent:
                seeds = self.dream._extract_seed_motifs(state)
                world = self.dream.create_dream_world(seeds)
                entered = self.dream.enter_dream(["reflection", "ethics", "memory"])
                out["dream_event"] = "entered"
                out["dream_locations"] = len(world)
                out["dream_awareness"] = float(entered.get("awareness_level", 0.0))
            else:
                out["dream_event"] = "declined"
        elif phase == "DREAM" and self.dream.dream_active:
            adv = self.dream.advance_dream({})
            out["dream_event"] = "advanced"
            out["dream_awareness"] = float(self.dream.avatar.awareness_level)
            out["dream_advance_keys"] = sorted(adv.keys()) if isinstance(adv, dict) else None
        elif phase != "DREAM" and self.dream.dream_active:
            res = self.dream.exit_dream(integrate_memories=True)
            mems = res.get("integrated_memories", [])
            ids = []
            for m in mems:
                ids.append(self.memory.store_memory(
                    content=m["content"], memory_type="dream",
                    metadata={"dream_type": m["type"], "significance": m["significance"], "step": self.step_index}))
                self.motivation.add_experience(self._Experience(
                    content={"dream": m["type"], "text": m["content"]}, source="dream",
                    salience=float(m["significance"]), valence=0.0, intensity=float(m["significance"])))
            out["dream_event"] = "exited"
            out["dream_statistics"] = res.get("dream_statistics")
            out["dream_memories_integrated"] = len(ids)
            self.dream_log.append({"exit_step": self.step_index, **res.get("dream_statistics", {}),
                                   "memories": len(ids)})
        out["dream_active_after"] = self.dream.dream_active
        return out

    # ------------------------------------------------------------------ step

    def step(self, passage: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        t0 = time.time()
        breath = self.breath.update_phase(self.cfg.breath_dt)
        phase = breath["dominant_phase"]
        self._engine_breath = self._TriaxialBreath[CANON_TO_TRIAXIAL[phase]]
        self._engine_out = None
        from runtime.autodidactic_learning import BreathPhase as LearningPhase
        self._iala_phase = LearningPhase[phase]
        self.iala.ethical_filter.breath_adapter.set_phase(self._iala_phase)

        if passage is None:
            passage = self.passages[self.step_index % len(self.passages)]
        rec = super().step(passage)   # engine (with breath), sentinel, Bayes, canon motivation, IALA, LQT self-mod
        motivation_wait = self._drain_motivation()

        if self._engine_out is None:
            raise RuntimeError("engine forward hook did not fire")
        st = self._engine_out["triaxial_state"]
        psi = torch.as_tensor(np.asarray(st.psi_vector, dtype=np.float32))
        psi_mod = self.breath.synchronize_component("memory_core", psi)
        if rec["contradiction_severity"] > 0:
            self.breath.report_contradiction("sect_sentinel", ",".join(map(str, rec["contradictions"])),
                                             float(rec["contradiction_severity"]))

        ethical_context = {k: float(v) for k, v in zip(ETHICAL_KEYS, rec["ethical_features"])}
        mem_id = self.memory.store_memory(
            content=passage["text"], memory_type="episodic",
            metadata={"step": self.step_index, "passage": rec["passage"], "breath": phase},
            ethical_context=ethical_context)
        consciousness = None
        if phase == "REST" and self.cfg.rest_consciousness:
            consciousness = self.memory.update_consciousness_state({
                "awareness_level": float(np.clip(rec["reflection_confidence"], 0.0, 1.0)),
                "introspective_depth": float(np.clip(rec["meta_confidence"], 0.0, 1.0)),
                "ethical_constraints": ethical_context,
            })

        self._recent.append(rec)
        dream = self._dream_step(phase)
        self._drain_motivation()
        mm = self.memory.get_system_metrics()

        rec.update({
            "breath_phase": phase,
            "breath_triaxial_phase": self._engine_breath.name,
            "breath_accumulator": float(breath["phase"]),
            "breath_coherence": float(breath["harmonic_coherence"]),
            "breath_dominant_weight": float(breath["distribution"][phase]),
            "psi_breath_mod_norm": float(torch.linalg.norm(psi_mod).item()),
            "breath_contradictions": len(self.breath.contradiction_buffer),
            "rsl_memory_id": mem_id[:16],
            "rsl_active_memories": mm["active_memories"],
            "rsl_storage_ops": mm["performance_metrics"]["storage_operations"],
            "rsl_paradox_resolutions": mm["performance_metrics"]["paradox_resolutions"],
            "rsl_eigenstate_norm": float(mm["eigenstate_metrics"]["primary_eigenstate_norm"]),
            "rsl_temporal_consistency": float(mm["temporal_metrics"]["current_temporal_consistency"]),
            "rsl_sparse_entries": mm["storage_metrics"]["sparse_entries"],
            "rsl_consciousness": consciousness,
            **{k: v for k, v in dream.items()},
            "motivation_drain_seconds": motivation_wait,
            **self._motivation_stats(),
            "backbone_breath_adapter": getattr(getattr(self.field, "breath_adapter", None), "current_phase", None),
            "canon_step_seconds": time.time() - t0,
        })
        voice = self.engine.native_voice
        rec.update(self.rsei.settle_cycle(rec, {
            "voice_ready": voice.ready,
            "voice_loss": float(voice.last_training_loss.item()),
        }))
        return rec

    def close(self) -> None:
        super().close()
        self.memory.close()
        self.breath.executor.shutdown(wait=True)


def _jsonable(o: Any) -> Any:
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, torch.Tensor):
        return o.detach().cpu().tolist()
    return str(o)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--lqt-backend", default=None)
    p.add_argument("--no-engine-learner", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    a = p.parse_args(argv)

    # builtin hash() is salted per process; canon modules use it for vectors/ids.
    if os.environ.get("PYTHONHASHSEED") != str(a.seed):
        env = dict(os.environ, PYTHONHASHSEED=str(a.seed))
        os.execve(sys.executable, [sys.executable, "-m", "runtime.rosemary_full", *(argv or sys.argv[1:])], env)

    out = a.out.resolve()
    if out.exists() and any(out.iterdir()) and not a.overwrite:
        p.error(f"{out} exists and is not empty (use --overwrite)")
    (out / "steps").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=str(out / "run.log"), level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s", force=True)
    os.chdir(out)   # canon/original modules write logs and yaml into CWD

    cfg = RosemaryFullConfig(out_dir=out, seed=a.seed, lqt_backend=a.lqt_backend,
                             engine_learner=not a.no_engine_learner)
    t0 = time.time()
    loop = RosemaryFullLoop(cfg)
    init_s = time.time() - t0
    with open(out / "metrics.jsonl", "w") as mf:
        for _ in range(a.steps):
            rec = loop.step()
            line = json.dumps(rec, default=_jsonable)
            mf.write(line + "\n")
            mf.flush()
            (out / "steps" / f"step_{rec['step']:04d}.json").write_text(json.dumps(rec, indent=2, default=_jsonable))
            print(f"step {rec['step']:3d} breath={rec['breath_phase']:<13} q={rec['reflection_quality']:.4f} "
                  f"sev={rec['contradiction_severity']:.2f} drive={rec['motivation_drive']:.3f} "
                  f"rsl={rec['rsl_active_memories']} dream={rec['dream_event']} {rec['canon_step_seconds']:.1f}s",
                  flush=True)
    loop.close()
    run = {
        "config": {k: (str(v) if isinstance(v, Path) else v) for k, v in asdict(cfg).items()},
        "steps": a.steps, "init_seconds": init_s, "wall_seconds": time.time() - t0,
        "pythonhashseed": os.environ.get("PYTHONHASHSEED"), "python": sys.version.split()[0],
        "torch": torch.__version__, "machine": platform.machine(),
        "dreams": loop.dream_log, "canon_to_triaxial_breath": CANON_TO_TRIAXIAL,
    }
    (out / "run.json").write_text(json.dumps(run, indent=2, default=_jsonable))
    return 0


if __name__ == "__main__":
    sys.exit(main())
