#!/usr/bin/env python3
"""Integrated RSI biocognitive loop.

One step of the operator's loop, in order:

1. **Cognitive engine modality** -- a corpus passage (the operator's IALA theorem
   papers, ``lqt/iala/theorems``) is encoded deterministically into hidden states
   (IALA ``DeterministicContentEncoder``) and run through
   ``cognition.cognitive_engine.CognitiveEngine`` (TriaxialBackbone with LQT-stored
   Psi weights, MetaReflectiveOutputHead). The engine carries the IALA learner, so
   its own reflection errors feed ``learn_from_text``.
2. **Meta reflection tied to the biocognitive core** -- the engine's reflection
   scores (what the step produced) are set against the Bayesian beliefs about those
   same quantities (what the system expects) in a SECT ``CognitiveState`` and passed
   to rosemary's ``URSMIFContradictionSentinel``. A contradiction (belief and
   reflection on opposite sides of the sentinel thresholds) yields a severity in
   [0, 1].
3. **Bayesian updating** -- ``runtime.bayesian_config_orchestrator`` holds Beta
   beliefs over reflection quality, ethical alignment and meta confidence; each is
   updated with the step's evidence (RBUS recursive update). The pre-update
   posterior mean of reflection quality is the baseline for the step's advantage.
4. **Motivation** -- the step becomes an ``Experience`` for
   ``runtime.motivation_system.EmergentMotivationSystem``; its ``value_alignment``
   is the motivational drive.
5. **Autodidactic learning (IALA)** -- the passage goes through
   ``learn_from_text`` and one ``run_training_cycle`` (breath-phase dispatch).
6. **LQT self-modification** -- the Psi integration weights W_R, W_E, W_M (LQT
   buckets in the backbone's ``LQTStore``) receive

       dW_k = eta * drive * (1 - severity) * advantage * outer(psi_eth, region_k)

   where ``psi_eth = apply_ethical_force(psi, E, coupling)`` (rosemary
   ``ethical_tensor``) with ``E[i] = f_i * W_E[:, i]``: ethical feature ``f_i`` of
   the passage (IALA ``EthicalLearningFilter``) exerted along the lattice positions
   ``W_E`` couples to ethical dimension ``i``. Writes go through
   ``cognition.lqt_bridge.LQTStore.put`` (re-quantization; ``preserve_error`` keeps
   the epsilon residual) and the reconstructed bucket replaces the backbone's
   compute copy.

The update rule in step 6 is this lane's integration choice (reward-modulated
Hebbian on the Psi operator, gated by contradiction and motivation). It is not taken
from an operator spec, and nothing here claims it improves anything; the training
CLI records what it does.
"""

from __future__ import annotations

import json
import logging
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = REPO_ROOT / "lqt" / "iala" / "theorems"

logger = logging.getLogger("runtime.loop")

# Beliefs the loop maintains (orchestrator flat schema). Beta(2, 2): mean 0.5, weak.
LOOP_BELIEFS: Dict[str, Any] = {
    "reflection": {
        "quality": {"value": 0.5, "bayesian_metadata": {
            "type": "learned", "distribution": "beta", "alpha": 2.0, "beta": 2.0, "prior_strength": 0.5}},
        "meta_confidence": {"value": 0.5, "bayesian_metadata": {
            "type": "learned", "distribution": "beta", "alpha": 2.0, "beta": 2.0, "prior_strength": 0.5}},
    },
    "ethics": {
        "alignment": {"value": 0.5, "bayesian_metadata": {
            "type": "learned", "distribution": "beta", "alpha": 2.0, "beta": 2.0, "prior_strength": 0.5}},
    },
}
BELIEF_KEYS = {
    "quality": "reflection.quality",
    "meta_confidence": "reflection.meta_confidence",
    "ethical_alignment": "ethics.alignment",
}


@dataclass
class LoopConfig:
    """Everything one run needs. Paths are created by the loop."""

    out_dir: Path
    seed: int = 0
    hidden_dim: int = 64          # CognitiveEngine needs a multiple of 16
    seq_len: int = 4              # hidden-state positions per passage
    metacog_state_dim: int = 64
    lqt_backend: Optional[str] = None   # None -> $LQT_BACKEND -> 'python' (lqt_bridge)
    weight_bits: int = 4
    eta: float = 0.05             # base self-modification rate
    ethical_coupling: float = 0.1  # rosemary apply_ethical_force default
    bayes_max_depth: int = 10     # RBUS spec default (3.1.1)
    corpus_dir: Path = DEFAULT_CORPUS
    passage_chars: int = 600
    # Pass the IALA learner into CognitiveEngine (its reflection errors then feed
    # learn_from_text). False only while cognition/cognitive_engine.py:240 slices the
    # learner's deque (TypeError); IALA still runs in step 5 either way.
    engine_learner: bool = True

    @property
    def store_dir(self) -> Path:
        return self.out_dir / "lqt_store"

    @property
    def state_dir(self) -> Path:
        return self.out_dir / "state"


def load_corpus(corpus_dir: Path, passage_chars: int) -> List[Dict[str, str]]:
    """Paragraph passages from the theorem markdown files, in a fixed order."""
    files = sorted(p for p in Path(corpus_dir).glob("*.md"))
    if not files:
        raise FileNotFoundError(f"no .md corpus files in {corpus_dir}")
    passages: List[Dict[str, str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for i, para in enumerate(re.split(r"\n\s*\n", text)):
            para = " ".join(para.split())
            if len(para) < 80 or para.startswith("```"):
                continue
            passages.append({"source": path.name, "index": str(i), "text": para[:passage_chars]})
    if not passages:
        raise ValueError(f"corpus {corpus_dir} produced no passages")
    return passages


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class RSILoop:
    """The integrated loop. Construct, call :meth:`step` repeatedly, then :meth:`close`."""

    WEIGHTS = ("W_R", "W_E", "W_M")

    def __init__(self, cfg: LoopConfig):
        self.cfg = cfg
        cfg.out_dir.mkdir(parents=True, exist_ok=True)
        cfg.state_dir.mkdir(parents=True, exist_ok=True)
        seed_everything(cfg.seed)

        # Imports are local so `import runtime.loop` stays cheap and side-effect free.
        from cognition.cognitive_engine import CognitiveEngine, OutputModality
        from cognition.triaxial_backbone import TriaxialConfig
        from rosemary.biocognitive_core.components.sect.agent import CognitiveState
        from rosemary.biocognitive_core.components.sect.ursmif_sentinel import URSMIFContradictionSentinel
        from rosemary.infrastructure.ethical_tensor import (
            analyze_ethical_distribution, apply_ethical_force, create_ethical_tensor)
        from runtime.autodidactic_learning import DeterministicContentEncoder, IntegratedAutodidacticLearner
        from runtime.bayesian_config_orchestrator import BayesianConfigurationOrchestrator
        from runtime.motivation_system import EmergentMotivationSystem, Experience
        from runtime.rsei_incentive import RSNN3CapabilitySystem

        self._OutputModality = OutputModality
        self._CognitiveState = CognitiveState
        self._Experience = Experience
        self._apply_ethical_force = apply_ethical_force
        self._create_ethical_tensor = create_ethical_tensor
        self._analyze_ethical_distribution = analyze_ethical_distribution

        self.passages = load_corpus(cfg.corpus_dir, cfg.passage_chars)
        self.encoder = DeterministicContentEncoder(cfg.hidden_dim)

        self.iala = IntegratedAutodidacticLearner({"embedding_dim": cfg.hidden_dim, "cycle_sleep": False,
                                                    "corpus_dir": str(cfg.corpus_dir),
                                                    "passage_chars": cfg.passage_chars})
        backbone_cfg = TriaxialConfig(
            metacog_state_dim=cfg.metacog_state_dim,
            lqt_backend=cfg.lqt_backend,
            weights_path=str(cfg.store_dir),
            weight_bits=cfg.weight_bits,
            bayesian_enabled=False,      # the loop owns the orchestrator (one instance, no thread)
            parallel_computation=False,
        )
        self.engine = CognitiveEngine(hidden_dim=cfg.hidden_dim,
                                      autodidactic_learner=self.iala if cfg.engine_learner else None,
                                      backbone_config=backbone_cfg)
        self.engine.eval()
        self.field = self.engine.backbone.field
        self.store = self.field.weight_store

        self.bayes = BayesianConfigurationOrchestrator(
            config_path=str(cfg.state_dir / "bayes_beliefs.yaml"),
            security_enabled=False,
            state_dir=str(cfg.state_dir),
            background_optimization=False,
            config_data=LOOP_BELIEFS,
            max_recursion_depth=cfg.bayes_max_depth,
        )
        self.sentinel = URSMIFContradictionSentinel()
        self.motivation = EmergentMotivationSystem()
        self.rsei = RSNN3CapabilitySystem(self.bayes, self.motivation, seed=cfg.seed)
        self._rsei_full_runtime = False
        self.step_index = 0

    # ------------------------------------------------------------------ helpers

    def _hidden_states(self, text: str) -> torch.Tensor:
        """[1, seq_len, hidden_dim] from deterministic encodings of seq_len text chunks."""
        words = text.split()
        n = self.cfg.seq_len
        chunks = [" ".join(words[i::n]) or text for i in range(n)]
        return torch.stack([self.encoder.encode(c) for c in chunks]).unsqueeze(0).float()

    def _belief_mean(self, key: str) -> float:
        b = self.bayes.parameter_beliefs[key]
        a, bb = b.distribution_params["alpha"], b.distribution_params["beta"]
        return float(a / (a + bb))

    def _ethical_tensor(self, features: List[float]) -> np.ndarray:
        """E[i] = f_i * W_E[:, i] on the psi lattice (shape (ethical_dim, psi_dim))."""
        w_e = self.field.W["W_E"]
        psi_dim, eth_dim = w_e.shape
        tensor = self._create_ethical_tensor((psi_dim,), eth_dim)
        for i in range(eth_dim):
            tensor[i] = float(features[i]) * w_e[:, i]
        return tensor

    def _self_modify(self, psi_eth: np.ndarray, unified: np.ndarray, scale: float) -> Dict[str, float]:
        """Apply dW_k = scale * outer(psi_eth, region_k) through the LQT store."""
        r_dim = self.field.W["W_R"].shape[1]
        e_dim = self.field.W["W_E"].shape[1]
        regions = {"W_R": unified[:r_dim], "W_E": unified[r_dim:r_dim + e_dim], "W_M": unified[r_dim + e_dim:]}
        out: Dict[str, float] = {}
        for name in self.WEIGHTS:
            old = self.field.W[name]
            region = regions[name]
            if region.shape[0] != old.shape[1]:
                raise ValueError(f"{name}: region width {region.shape[0]} != weight cols {old.shape[1]}")
            target = old + scale * np.outer(psi_eth, region).astype(np.float32)
            bucket = self.store.put(name, target, bits=self.cfg.weight_bits, preserve_error=True)
            new = self.store.get(name)
            self.field.W[name] = new
            out[f"dW_{name}"] = float(np.linalg.norm(new - old))
            out[f"W_{name}_norm"] = float(np.linalg.norm(new))
            out[f"codebook_{name}"] = int(bucket.num_entries)
        return out

    def _drain_motivation(self) -> float:
        """Finish asynchronous formation before observing or saving its state."""
        start = time.time()
        for component in (self.motivation.value_formation_system,
                          self.motivation.goal_formation_system):
            thread = getattr(component, 'processing_thread', None)
            if thread is not None and thread.is_alive():
                thread.join(timeout=120)
                if thread.is_alive():
                    raise RuntimeError('motivation formation did not finish within 120 seconds')
        return time.time() - start

    # ------------------------------------------------------------------ step

    def step(self, passage: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """One loop step on ``passage`` ({source, index, text}); default: the next corpus passage."""
        t0 = time.time()
        if passage is None:
            passage = self.passages[self.step_index % len(self.passages)]
        text = passage["text"]
        rsei_goal = self.rsei.begin_cycle()
        cognitive_task = text
        if rsei_goal:
            node = self.rsei.engine.graph.nodes[rsei_goal["node"]]
            cognitive_task = f"{text}\n\nCapability objective: {node.description}"

        # 1. cognitive engine
        hidden = self._hidden_states(text)
        with torch.no_grad():
            out = self.engine(hidden, cognitive_task, modality=self._OutputModality.NATURAL_LANGUAGE,
                              rsei_goal=(rsei_goal or {}).get("node"))
        st = out["triaxial_state"]
        if st.unified_state is None or st.psi_vector is None:
            raise RuntimeError("engine returned a triaxial_state without unified_state/psi_vector")
        refl = out["reflection_results"]
        meta = out.get("meta_reflection_results") or {}
        quality = float(refl["quality_score"])
        ethical_alignment = float(out["ethical_alignment_score"])
        meta_conf = float(meta.get("meta_confidence", 0.0))
        evidence = {"quality": quality, "ethical_alignment": ethical_alignment, "meta_confidence": meta_conf}

        # 2. meta reflection vs beliefs through the SECT sentinel
        prior = {k: self._belief_mean(v) for k, v in BELIEF_KEYS.items()}
        cstate = self._CognitiveState(
            belief_confidence={k: prior[k] for k in BELIEF_KEYS},
            goal_alignment={k: evidence[k] for k in BELIEF_KEYS},
            attention_focus=[passage["source"]],
        )
        signal = self.sentinel.analyze_state(cstate)
        severity = float(signal.severity) if signal is not None else 0.0

        # 3. Bayesian update
        bayes_ok = {k: bool(self.bayes.update_parameter_with_evidence(v, float(np.clip(evidence[k], 0.0, 1.0))))
                    for k, v in BELIEF_KEYS.items()}
        posterior = {k: self._belief_mean(v) for k, v in BELIEF_KEYS.items()}
        advantage = quality - prior["quality"]

        # 4. motivation
        valence = float(np.clip(2.0 * advantage, -1.0, 1.0))
        self.motivation.add_experience(self._Experience(
            content={"source": passage["source"], "paragraph": passage["index"],
                     "mode": str(out.get("cognitive_mode"))},
            source="rsi_loop",
            salience=float(np.clip(refl.get("novelty_score", 0.5), 0.0, 1.0)),
            valence=valence,
            intensity=float(np.clip(abs(valence), 0.0, 1.0)),
        ))
        self._drain_motivation()
        drive = float(self.motivation.evaluate_input(text, {"valence": valence})["value_alignment"])
        self._drain_motivation()

        # 5. IALA
        learn = self.iala.learn_from_text(text, source=passage["source"])
        cycle = self.iala.run_training_cycle(getattr(self, '_iala_phase', None))

        # 6. LQT self-modification (ethically modulated)
        features = self.iala.ethical_filter._extract_ethical_features(text)
        e_tensor = self._ethical_tensor(features)
        psi = np.asarray(st.psi_vector, dtype=np.float64)
        psi_eth = self._apply_ethical_force(psi, e_tensor, coupling_constant=self.cfg.ethical_coupling)
        scale = self.cfg.eta * drive * (1.0 - severity) * advantage
        mods = self._self_modify(np.asarray(psi_eth, dtype=np.float32),
                                 np.asarray(st.unified_state, dtype=np.float32), scale)

        status = self.iala.get_learning_status()
        mstate = self.motivation.get_current_motivation_state()
        self.step_index += 1
        record: Dict[str, Any] = {
            "step": self.step_index,
            "passage": f'{passage["source"]}#{passage["index"]}',
            "cognitive_mode": str(out.get("cognitive_mode")),
            "reflection_quality": quality,
            "reflection_novelty": float(refl.get("novelty_score", float("nan"))),
            "reflection_alignment": float(refl.get("alignment_score", float("nan"))),
            "reflection_confidence": float(refl.get("confidence_score", float("nan"))),
            "ethical_alignment": ethical_alignment,
            "meta_confidence": meta_conf,
            "meta_recursive_depth": meta.get("recursive_depth"),
            "meta_reflection_errors": [e.get("error_type") for e in meta.get("reflection_errors", [])],
            "ere": float(st.integrated_vector[0]), "rbu": float(st.integrated_vector[1]),
            "es": float(st.integrated_vector[2]),
            "psi_norm": float(np.linalg.norm(psi)),
            "convergence_status": st.convergence_status,
            "convergence_distance": float(st.convergence_distance),
            "decoherence": st.stability_metrics.get("decoherence_severity"),
            "lqt_backend": st.stability_metrics.get("lqt_backend"),
            "belief_prior": prior, "belief_posterior": posterior, "bayes_update_ok": bayes_ok,
            "advantage": advantage,
            "contradiction_severity": severity,
            "contradictions": list(signal.contradictions) if signal is not None else [],
            "motivation_drive": drive,
            "motivation_values": len(mstate.get("values", {})),
            "motivation_goals": len(mstate.get("goals", {})),
            "ethical_features": [float(f) for f in features],
            "mod_scale": scale,
            **mods,
            "iala_learn_success": bool(learn.get("success")),
            "iala_new_entity": bool(learn.get("new_entity")),
            "knowledge_entities_used": out.get("knowledge_entities_used", []),
            "knowledge_influence_norm": out.get("knowledge_influence_norm", 0.0),
            "recursive_weights_used": out.get("recursive_weights_used", []),
            "recursive_influence_norm": out.get("recursive_influence_norm", 0.0),
            "iala_phase": cycle.get("phase"),
            "iala_entities": status["knowledge_entities"],
            "iala_belief_states": status["belief_states"],
            "iala_metacog_confidence": status["metacognitive_state"]["confidence"],
            "iala_identity_coherence": status["metacognitive_state"]["identity_coherence"],
            "step_seconds": time.time() - t0,
        }
        if not self._rsei_full_runtime:
            voice = self.engine.native_voice
            record.update(self.rsei.settle_cycle(record, {
                "voice_ready": voice.ready,
                "voice_loss": float(voice.last_training_loss.item()),
            }))
        return record

    # ------------------------------------------------------------------ persistence

    def checkpoint(self, directory: Path) -> Dict[str, Any]:
        """Persist the LQT weight store, Bayesian beliefs and motivation summary."""
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.store.save(directory / "lqt_store")
        self.bayes.save_configuration(str(directory / "bayes_beliefs.yaml"))
        (directory / "motivation.json").write_text(json.dumps(
            self.motivation.get_current_motivation_state(), indent=2, default=str))
        (directory / "rsei_state.json").write_text(json.dumps(
            self.rsei.export_state(), indent=2, default=str))
        return {"dir": str(directory), "lqt_store": self.store.summary()}

    def close(self) -> None:
        self.bayes.stop_background_optimization()
        self.engine.backbone.shutdown()
