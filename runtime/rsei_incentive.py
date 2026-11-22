"""RSEI capability incentive integrated with the live RSNN-3 runtime.

This is the supplied ``rsei_incentive.py`` design moved across the real system
boundary.  Capability is an exact verified competence count; HAJRA ranks the
frontier; strict expansion alone earns reward; and an observer outside the
CognitiveEngine owns every probe result.  No reflection/self-report score can
certify a competence.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class Competence:
    name: str
    requires: Tuple[str, ...] = ()
    cost: float = 1.0
    description: str = ""


class CompetenceGraph:
    def __init__(self, nodes: Iterable[Competence]):
        self.nodes = {node.name: node for node in nodes}
        for node in self.nodes.values():
            missing = set(node.requires) - set(self.nodes)
            if missing:
                raise ValueError(f"{node.name} requires missing competences {sorted(missing)}")
        self._assert_dag()

    def _assert_dag(self) -> None:
        marks: Dict[str, int] = {}

        def visit(name: str) -> None:
            if marks.get(name) == 1:
                raise ValueError(f"competence cycle at {name}")
            if marks.get(name) == 2:
                return
            marks[name] = 1
            for parent in self.nodes[name].requires:
                visit(parent)
            marks[name] = 2

        for name in self.nodes:
            visit(name)

    def frontier(self, verified: Set[str]) -> List[str]:
        return sorted(name for name, node in self.nodes.items()
                      if name not in verified and all(parent in verified for parent in node.requires))

    def unlocked_by(self, target: str, verified: Set[str]) -> int:
        return len(set(self.frontier(verified | {target})) - set(self.frontier(verified)))


class RuntimeCapabilityVerifier:
    """Held-out observer of measurable runtime behavior.

    It is not an ``nn.Module``, is never passed to ``CognitiveEngine``, and only
    consumes the loop's returned outputs, memory counters, LQT mutation facts,
    and voice-training record.  Event probes retain their last affirmative
    result until an explicit failing exercise occurs; continuous probes are
    re-evaluated every cycle, enabling the regression guard to fire.
    """

    EVENT_PROBES = {"dream_integration", "native_voice_grounding"}

    def __init__(self):
        self.scores: Dict[str, float] = {}
        self.observations: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _finite(values: Iterable[Any]) -> bool:
        try:
            return all(math.isfinite(float(value)) for value in values)
        except (TypeError, ValueError):
            return False

    def observe(self, record: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        knowledge_used = list(record.get("knowledge_entities_used") or [])
        voice_ready = bool(context.get("voice_ready"))
        voice_loss = float(context.get("voice_loss", 1e9))
        current = {
            "cognitive_forward": 1.0 if self._finite(record.get(k) for k in ("ere", "rbu", "es")) else 0.0,
            "ethical_admission": 1.0 if record.get("iala_learn_success") else 0.0,
            "bayesian_update": sum(bool(v) for v in (record.get("bayes_update_ok") or {}).values()) /
                               max(1, len(record.get("bayes_update_ok") or {})),
            "knowledge_acquisition": 1.0 if record.get("iala_learn_success") and
                                               int(record.get("iala_entities", 0)) > 0 else 0.0,
            "knowledge_recall": min(1.0, float(record.get("knowledge_influence_norm", 0.0)) / 0.05),
            "recursive_weight_application": min(1.0, float(record.get("recursive_influence_norm", 0.0)) / 0.02),
            # This must be an already committed LQT transaction, not merely a
            # proposed dW from the cognitive loop that might still fail to sync.
            "lqt_self_modification": 1.0 if context.get("lqt_verified_edit") else 0.0,
            "persistent_memory": 1.0 if int(record.get("rsl_active_memories", 0)) > 0 else 0.0,
            "breath_coupling": 1.0 if record.get("breath_phase") in
                {"INHALE", "HOLD", "EXHALE", "PAUSE_FALLING", "REST", "DREAM", "PAUSE_RISING"} else 0.0,
            "dream_integration": 1.0 if record.get("dream_event") == "exited" else 0.0,
            "native_voice_grounding": 1.0 if voice_ready and voice_loss < 1.25 else 0.0,
            "multi_source_integration": 1.0 if len(knowledge_used) >= 2 and
                                                   float(record.get("knowledge_influence_norm", 0.0)) > 0 else 0.0,
        }
        for name, score in current.items():
            if name in self.EVENT_PROBES and score == 0.0 and self.scores.get(name, 0.0) > 0.0:
                continue
            self.scores[name] = float(max(0.0, min(1.0, score)))
            self.observations[name] = {"step": int(record.get("step", 0)), "score": self.scores[name]}
        return dict(self.scores)

    def __call__(self, name: str) -> float:
        return float(self.scores.get(name, 0.0))


class RSEIIncentiveEngine:
    def __init__(self, graph: CompetenceGraph, verifier: RuntimeCapabilityVerifier,
                 required_yield: float = 0.5, admit: float = 0.80,
                 pass_threshold: float = 0.80, ema: float = 0.15,
                 explore_eps: float = 0.10, unlock_weight: float = 0.5,
                 spot_checks: int = 2, seed: int = 0):
        self.graph, self.verifier = graph, verifier
        self.required_yield, self.admit = float(required_yield), float(admit)
        self.pass_threshold, self.ema = float(pass_threshold), float(ema)
        self.explore_eps, self.unlock_weight = float(explore_eps), float(unlock_weight)
        self.spot_checks, self.rng = int(spot_checks), random.Random(seed)
        self.verified: Set[str] = set()
        self.attempts: Dict[str, int] = {}
        self.successes: Dict[str, int] = {}
        self.cost_est = {name: float(node.cost) for name, node in graph.nodes.items()}
        self.drive = 0.5
        self.ledger: List[Dict[str, Any]] = []
        self.prev_hash = "genesis"
        self.active_goal: Optional[Dict[str, Any]] = None

    def _p_success(self, name: str) -> float:
        return (self.successes.get(name, 0) + 1) / (self.attempts.get(name, 0) + 2)

    def _gain(self, name: str) -> float:
        return 1.0 + self.unlock_weight * self.graph.unlocked_by(name, self.verified)

    def candidate_goals(self) -> List[Dict[str, Any]]:
        goals = []
        for name in self.graph.frontier(self.verified):
            rate = self._p_success(name) * self._gain(name) / max(self.cost_est[name], 1e-6)
            effectiveness = min(1.0, rate / self.required_yield)
            goals.append({"node": name, "R": rate, "I_eff": effectiveness,
                          "admitted": effectiveness >= self.admit})
        return sorted(goals, key=lambda goal: (-goal["I_eff"], goal["node"]))

    def choose_goal(self) -> Optional[Dict[str, Any]]:
        candidates = self.candidate_goals()
        if not candidates:
            self.active_goal = None
            return None
        admitted = [goal for goal in candidates if goal["admitted"]]
        if admitted and self.rng.random() > self.explore_eps:
            chosen = admitted[0]
            mode = "admitted"
        else:
            chosen = self.rng.choice(candidates) if self.rng.random() < self.explore_eps else candidates[0]
            mode = "explore"
        self.active_goal = {**chosen, "mode": mode}
        return dict(self.active_goal)

    def settle(self, target: str, steps_spent: float) -> Dict[str, Any]:
        if target not in self.graph.nodes:
            raise KeyError(target)
        self.attempts[target] = self.attempts.get(target, 0) + 1
        score = float(self.verifier(target))
        passed, reward = score >= self.pass_threshold, 0.0
        strict = False
        if passed:
            descendant = self.verified | {target}
            strict = len(descendant) > len(self.verified) and not descendant <= self.verified
            if strict:
                reward = self._gain(target)
                self.verified = descendant
                self.successes[target] = self.successes.get(target, 0) + 1
                self.cost_est[target] = 0.7 * self.cost_est[target] + 0.3 * max(steps_spent, 1e-6)
        regressed: List[str] = []
        pool = sorted(self.verified - {target})
        for name in self.rng.sample(pool, min(self.spot_checks, len(pool))):
            if self.verifier(name) < self.pass_threshold:
                self.verified.discard(name)
                regressed.append(name)
                reward -= 1.0
        normalized = max(-1.0, min(1.0, reward / 2.0))
        self.drive = (1.0 - self.ema) * self.drive + self.ema * (0.5 + 0.5 * normalized)
        event = {"target": target, "score": score, "passed": passed, "strict_expansion": strict,
                 "reward": reward, "regressed": regressed, "dim": len(self.verified),
                 "drive": self.drive, "steps_spent": float(steps_spent)}
        body = json.dumps(event, sort_keys=True) + self.prev_hash
        self.prev_hash = hashlib.sha256(body.encode()).hexdigest()
        event["hash"] = self.prev_hash[:12]
        self.ledger.append(event)
        return dict(event)

    def metrics(self) -> Dict[str, Any]:
        admitted = [goal for goal in self.candidate_goals() if goal["admitted"]]
        return {"motivation_drive": self.drive, "motivation_goals": len(admitted),
                "motivation_values": 3, "rsei_dim": len(self.verified),
                "rsei_frontier": len(self.graph.frontier(self.verified)),
                "rsei_ledger_events": len(self.ledger), "rsei_ledger_head": self.prev_hash[:12]}

    def export_state(self) -> Dict[str, Any]:
        return {"verified": sorted(self.verified), "attempts": self.attempts,
                "successes": self.successes, "cost_est": self.cost_est, "drive": self.drive,
                "ledger": self.ledger[-2048:], "prev_hash": self.prev_hash,
                "active_goal": self.active_goal, "verifier_scores": self.verifier.scores,
                "verifier_observations": self.verifier.observations,
                "rng_state": repr(self.rng.getstate())}

    def restore_state(self, state: Dict[str, Any]) -> None:
        if not state:
            return
        self.verified = set(state.get("verified", ())) & set(self.graph.nodes)
        self.attempts = {k: int(v) for k, v in state.get("attempts", {}).items() if k in self.graph.nodes}
        self.successes = {k: int(v) for k, v in state.get("successes", {}).items() if k in self.graph.nodes}
        self.cost_est.update({k: float(v) for k, v in state.get("cost_est", {}).items() if k in self.graph.nodes})
        self.drive = float(state.get("drive", 0.5))
        self.ledger = list(state.get("ledger", []))[-2048:]
        self.prev_hash = str(state.get("prev_hash", "genesis"))
        self.active_goal = state.get("active_goal")
        self.verifier.scores = {k: float(v) for k, v in state.get("verifier_scores", {}).items()
                                if k in self.graph.nodes}
        self.verifier.observations = dict(state.get("verifier_observations", {}))


def rsnn3_competence_graph() -> CompetenceGraph:
    C = Competence
    return CompetenceGraph([
        C("cognitive_forward", (), 1.0, "Complete a finite triaxial cognitive forward pass."),
        C("ethical_admission", ("cognitive_forward",), 1.0, "Admit evidence through IALA's ethical gate."),
        C("bayesian_update", ("cognitive_forward",), 1.0, "Update liquid Bayesian evidence parameters."),
        C("knowledge_acquisition", ("ethical_admission",), 1.5, "Create or reinforce persistent knowledge."),
        C("knowledge_recall", ("knowledge_acquisition",), 1.5, "Recall retained knowledge into cognition."),
        C("recursive_weight_application", ("cognitive_forward",), 1.5, "Apply recursive weights in the forward path."),
        C("lqt_self_modification", ("recursive_weight_application",), 2.0, "Produce a non-zero unified LQT weight edit."),
        C("persistent_memory", ("knowledge_acquisition",), 2.0, "Store and retrieve persistent RSL memory."),
        C("breath_coupling", ("cognitive_forward",), 1.5, "Couple computation to the seven-phase breath."),
        C("dream_integration", ("persistent_memory", "breath_coupling"), 3.0, "Exit a dream with integrated memory."),
        C("native_voice_grounding", ("knowledge_recall",), 3.0, "Express cognitive state through trained native voice."),
        C("multi_source_integration", ("knowledge_recall", "bayesian_update", "lqt_self_modification"), 4.0,
          "Integrate multiple retained knowledge sources under recursive adaptation."),
    ])


class RSNN3CapabilitySystem:
    """Coordinates RSEI, dynamic Bayesian evidence, and the motivation organs."""

    def __init__(self, bayes: Any, motivation: Any, seed: int = 0):
        self.verifier = RuntimeCapabilityVerifier()
        self.engine = RSEIIncentiveEngine(rsnn3_competence_graph(), self.verifier, seed=seed)
        self.bayes, self.motivation = bayes, motivation
        self.current_goal: Optional[Dict[str, Any]] = None
        self.last_lqt_sync: Dict[str, Any] = {}
        motivation.bind_rsei(self.engine)
        self._sync_motivation_objects()

    def begin_cycle(self) -> Optional[Dict[str, Any]]:
        self.current_goal = self.engine.choose_goal()
        self._sync_motivation_objects()
        return dict(self.current_goal) if self.current_goal else None

    def settle_cycle(self, record: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        context = {**context,
                   "lqt_verified_edit": bool(self.last_lqt_sync.get("verify_edit_log")) and
                                        int(self.last_lqt_sync.get("elements_changed", 0)) > 0}
        self.verifier.observe(record, context)
        target = (self.current_goal or {}).get("node")
        event = None
        if target:
            belief_name = f"rsei.competence.{target}"
            self.bayes.ensure_beta_parameter(belief_name)
            score = self.verifier(target)
            updated = self.bayes.update_parameter_with_evidence(belief_name, score, "external_capability_probe")
            event = self.engine.settle(target, float(record.get("step_seconds", 1.0)))
            event["bayesian_parameter"] = belief_name
            event["bayesian_update_ok"] = bool(updated)
        self._sync_motivation_objects()
        return {**self.engine.metrics(), "rsei_goal": target,
                "rsei_goal_mode": (self.current_goal or {}).get("mode"),
                "rsei_goal_I_eff": (self.current_goal or {}).get("I_eff"),
                "rsei_probe_score": self.verifier(target) if target else None,
                "rsei_event": event, "rsei_verified": sorted(self.engine.verified),
                "bayesian_parameter_count": len(self.bayes.parameter_beliefs)}

    def notify_lqt_sync(self, sync: Dict[str, Any], verify_edit_log: bool) -> None:
        """Accept only the completed external persistence transaction."""
        self.last_lqt_sync = {**dict(sync), "verify_edit_log": bool(verify_edit_log)}

    def _sync_motivation_objects(self) -> None:
        import importlib
        motivation_module = importlib.import_module(type(self.motivation).__module__)
        Goal, Value = motivation_module.Goal, motivation_module.Value
        vfs, gfs = self.motivation.value_formation_system, self.motivation.goal_formation_system
        values = [
            ("rsei_verified_expansion", "Verified expansion", "Reward only externally verified strict capability growth."),
            ("rsei_no_regression", "No regression", "Retain previously verified competences under spot checks."),
            ("rsei_external_verification", "External verification", "Never certify capability from self-report or reflection."),
        ]
        for key, name, description in values:
            if key not in vfs.values:
                value = Value(id=key, name=name, description=description, intensity=0.95,
                              stability=0.98, clarity=1.0, specificity=1.0,
                              features={"rsei": 1.0, "verified": 1.0})
                vfs.values[key] = value
                vfs.value_relationship_graph.add_node(key, name=name, source="RSEI")
        frontier = set(self.engine.graph.frontier(self.engine.verified))
        for name, node in self.engine.graph.nodes.items():
            key = f"rsei_goal_{name}"
            status = "completed" if name in self.engine.verified else ("active" if name in frontier else "pending")
            importance = next((g["I_eff"] for g in self.engine.candidate_goals() if g["node"] == name), 0.0)
            if key not in gfs.goals:
                gfs.goals[key] = Goal(id=key, name=f"Verify {name.replace('_', ' ')}",
                                      description=node.description, importance=float(importance),
                                      specificity=1.0, complexity=min(1.0, node.cost / 5.0),
                                      related_values=[v[0] for v in values], status=status)
                gfs.goal_hierarchy.add_node(key, competence=name, source="RSEI")
            goal = gfs.goals[key]
            goal.status, goal.importance = status, float(importance)
            goal.progress = 1.0 if status == "completed" else 0.0

    def export_state(self) -> Dict[str, Any]:
        return self.engine.export_state()

    def restore_state(self, state: Dict[str, Any]) -> None:
        self.engine.restore_state(state)
        self._sync_motivation_objects()

