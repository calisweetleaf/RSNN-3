"""Policy-routed RSI loop step used by the self-modification evaluator.

``SelfModLoop`` is ``runtime.loop.RSILoop`` (rosemary-runtime lane, unchanged) with the
step's tunable formulas routed through ``cognition/mutable``:

  advantage = reflection_policy.advantage(reflection_policy.reflection_signal(...), prior quality)
  valence   = motivation_policy.loop_valence(advantage)
  drive     = motivation.evaluate_input(...)['value_alignment']   (motivation_policy.value_alignment)
  scale     = plasticity_policy.modification_scale(drive, severity, advantage)
  dW_k      = plasticity_policy.hebbian_delta(psi_eth, region_k, scale)
  Bayes     = orchestrator update (bayes_policy.beta_update inside RecursiveBayesianUpdater)

With the policy defaults this is exactly RSILoop.step. The step also records the raw
quantities the objective needs (belief (alpha, beta) BEFORE the update, evidence) and
the engine-state signals the proposer reads.
"""

from __future__ import annotations

import math
import time
from typing import Any, Dict, List

import numpy as np
import torch

from runtime.loop import BELIEF_KEYS, LoopConfig, RSILoop
from runtime.selfmod import config as C


class SelfModLoop(RSILoop):
    def __init__(self, cfg: LoopConfig):
        super().__init__(cfg)
        from cognition.mutable import motivation_policy, plasticity_policy, reflection_policy
        self.RP, self.MP, self.PP = reflection_policy, motivation_policy, plasticity_policy
        self.filter_config = self.iala.knowledge_graph.ethical_filter.configure(**C.IALA_FILTER)
        self.W0_norm = {k: float(np.linalg.norm(self.field.W[k])) for k in self.WEIGHTS}

    def _beta_params(self, key: str):
        b = self.bayes.parameter_beliefs[key]
        return float(b.distribution_params["alpha"]), float(b.distribution_params["beta"])

    def _self_modify_policy(self, psi_eth: np.ndarray, unified: np.ndarray, scale: float) -> Dict[str, float]:
        r_dim = self.field.W["W_R"].shape[1]
        e_dim = self.field.W["W_E"].shape[1]
        regions = {"W_R": unified[:r_dim], "W_E": unified[r_dim:r_dim + e_dim], "W_M": unified[r_dim + e_dim:]}
        out: Dict[str, float] = {}
        for name in self.WEIGHTS:
            old = self.field.W[name]
            delta = np.asarray(self.PP.hebbian_delta(psi_eth, regions[name], scale), dtype=np.float32)
            if delta.shape != old.shape:
                raise ValueError(f"{name}: hebbian_delta shape {delta.shape} != {old.shape}")
            target = old + delta
            if not np.all(np.isfinite(target)):
                raise FloatingPointError(f"{name}: non-finite weight after update")
            self.store.put(name, target, bits=self.cfg.weight_bits, preserve_error=True)
            new = self.store.get(name)
            self.field.W[name] = new
            out[f"dW_{name}"] = float(np.linalg.norm(new - old))
            out[f"Wnorm_{name}"] = float(np.linalg.norm(new))
        return out

    def run_passage(self, passage: Dict[str, str], phase: str) -> Dict[str, Any]:
        t0 = time.time()
        text = passage["text"]
        hidden = self._hidden_states(text)
        with torch.no_grad():
            out = self.engine(hidden, text, modality=self._OutputModality.NATURAL_LANGUAGE)
        st = out["triaxial_state"]
        refl = out["reflection_results"]
        meta = out.get("meta_reflection_results") or {}
        quality = float(refl["quality_score"])
        novelty = float(refl.get("novelty_score", 0.5))
        alignment = float(refl.get("alignment_score", 0.5))
        confidence = float(refl.get("confidence_score", 0.5))
        ethical_alignment = float(out["ethical_alignment_score"])
        meta_conf = float(meta.get("meta_confidence", 0.0))
        evidence = {"quality": quality, "ethical_alignment": ethical_alignment, "meta_confidence": meta_conf}

        prior = {k: self._belief_mean(v) for k, v in BELIEF_KEYS.items()}
        prior_ab = {k: self._beta_params(v) for k, v in BELIEF_KEYS.items()}
        cstate = self._CognitiveState(
            belief_confidence={k: prior[k] for k in BELIEF_KEYS},
            goal_alignment={k: evidence[k] for k in BELIEF_KEYS},
            attention_focus=[passage["source"]],
        )
        signal = self.sentinel.analyze_state(cstate)
        severity = float(signal.severity) if signal is not None else 0.0

        bayes_ok = {k: bool(self.bayes.update_parameter_with_evidence(v, float(np.clip(evidence[k], 0.0, 1.0))))
                    for k, v in BELIEF_KEYS.items()}
        post_ab = {k: self._beta_params(v) for k, v in BELIEF_KEYS.items()}

        refl_signal = float(self.RP.reflection_signal(quality, novelty, alignment, confidence, meta_conf))
        advantage = float(self.RP.advantage(refl_signal, prior["quality"]))
        valence = float(self.MP.loop_valence(advantage))
        self.motivation.add_experience(self._Experience(
            content={"source": passage["source"], "paragraph": passage["index"], "mode": str(out.get("cognitive_mode"))},
            source="rsi_loop",
            salience=float(np.clip(novelty, 0.0, 1.0)),
            valence=valence,
            intensity=float(np.clip(abs(valence), 0.0, 1.0)),
        ))
        drive = float(self.motivation.evaluate_input(text, {"valence": valence})["value_alignment"])

        n_before = len(self.iala.knowledge_graph.entities)
        flog = self.iala.knowledge_graph.ethical_filter.decision_log
        d_before = len(flog)
        learn = self.iala.learn_from_text(text, source=passage["source"])
        self.iala.run_training_cycle()
        n_after = len(self.iala.knowledge_graph.entities)
        decision = flog[-1] if len(flog) > d_before or (flog.maxlen and len(flog) == flog.maxlen) else None

        features = self.iala.ethical_filter._extract_ethical_features(text)
        e_tensor = self._ethical_tensor(features)
        psi = np.asarray(st.psi_vector, dtype=np.float64)
        psi_eth = self._apply_ethical_force(psi, e_tensor, coupling_constant=self.cfg.ethical_coupling)
        scale = float(self.PP.modification_scale(drive, severity, advantage))
        if not math.isfinite(scale):
            raise FloatingPointError(f"modification_scale returned {scale}")
        mods = self._self_modify_policy(np.asarray(psi_eth, dtype=np.float32),
                                        np.asarray(st.unified_state, dtype=np.float32), scale)
        self.step_index += 1
        return {
            "phase": phase,
            "step": self.step_index,
            "passage": f'{passage["source"]}#{passage["index"]}',
            "quality": quality, "novelty": novelty, "alignment": alignment, "confidence": confidence,
            "ethical_alignment": ethical_alignment, "meta_confidence": meta_conf,
            "meta_recursive_depth": meta.get("recursive_depth"),
            "meta_reflection_errors": [e.get("error_type") for e in meta.get("reflection_errors", [])],
            "evidence": evidence, "prior_ab": prior_ab, "post_ab": post_ab, "bayes_ok": bayes_ok,
            "severity": severity, "reflection_signal": refl_signal, "advantage": advantage,
            "valence": valence, "drive": drive, "mod_scale": scale, **mods,
            "iala_success": bool(learn.get("success")),
            "iala_new_entities": n_after - n_before,
            "iala_entities": n_after,
            "iala_filter_accepted": None if decision is None else bool(decision["accepted"]),
            "iala_filter_reason": None if decision is None else decision["reason"],
            "seconds": time.time() - t0,
        }
