#!/usr/bin/env python3
"""Chat with the live unified model (one ``model.lqt``).

    python -m runtime.chat --model runtime/runs/<run>/model.lqt            # interactive
    python -m runtime.chat --model <path> --once "text"                    # one turn, then save + exit
    printf 'line one\\nline two\\n' | python -m runtime.chat --model <path>  # stdin: one turn per line

The model is loaded with ``cognition.lqt_bridge.UnifiedModel`` (genesis from the
seeded stack when the file does not exist) and bound before the stack is built,
so the triaxial backbone's Psi store is a bucket view of it and every other
learnable tensor of the stack takes its value from it.

One turn = one step of :class:`runtime.rosemary_full.RosemaryFullLoop` on the
user's text (canon breath phase -> cognitive engine [triaxial backbone, RTA,
ethical/metacognitive/meta-reflective head] -> SECT sentinel -> Bayesian update
-> canon motivation (canon FBS tokenizer) -> IALA ``learn_from_text`` +
``run_training_cycle`` -> LQT self-modification of Psi -> canon RSL episodic
memory -> canon dream portal on DREAM phase).  The REST-phase MRC fixed point
(``update_consciousness_state``) is off unless ``--mrc``.  After the step every
change to a stack tensor becomes logged edits on the same model
(``UnifiedModel.sync``); the file is saved every ``--save-every`` turns and on exit.

What produces the reply text.  ``CognitiveEngine.native_voice`` is a byte-level
recursive decoder conditioned on the engine's ethically aligned cognitive state.
It is trained as an expression organ; teacher text never enters cognition, IALA,
beliefs, or memory.  Until it has received enough grounded examples, chat exposes
the auditable recall/state rendering below rather than pretending random weights
constitute language:

  * recall: text the system stored earlier -- IALA knowledge entities selected by
    IALA's ``RTAAttention.select`` (its own lexical+structural scoring) and RSL
    episodic/dream memories fetched with ``EnhancedRSLMemorySystem.retrieve_memory``,
    ranked by canon FBS harmonic resonance (``SacredFrequencySubstrate.extract_fbs``
    + cosine mapped to [0, 1], as ``CrossModalHarmonicBridge`` defines it);
  * dream: memory text the canon dream engine integrates when a dream exits;
  * the step's own numbers: cognitive mode, reflection scores, meta-reflection
    errors, IALA ethical filter verdict on the text, contradiction severity,
    breath phase, motivation drive.

Persistence of non-tensor identity.  model.lqt stores floats.  The owners of
tensors created at run time (evolution RecursiveWeights, IALA RWA content
weights and knowledge entities, canon motivation entities) also carry ints and
text; those go into the model's module graph as ``unified.stack`` JSON (no float
values) so the owners can be rebuilt on the next load, and RSL memory records are
kept there too.  A stored tensor whose owner cannot be rebuilt is kept in the
file untouched (dormant) and reported; it is never detached.
"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

BANNER_SOURCE = (
    "reply text = RSNN-3 native byte voice conditioned on this turn's cognitive state once trained; "
    "before readiness, auditable IALA/RSL recall + computed state. External tutors can supervise voice "
    "weights but cannot write knowledge, memory, beliefs, or reasoning state.")

RE_EVOLUTION = re.compile(r"^engine\.weight_registry\._weights\['(evolution_cycle_(\d+))'\]\.")
RE_RWA = re.compile(r"^engine\.autodidactic_learner\.rwa_store\['(rw_content_[0-9a-f]+)'\]\.")
KG_ENTITY_FIELDS = ("content_hash", "content_text", "source_url", "timestamp", "ethical_vector",
                    "ethical_archetype", "ethical_coherence", "reliability_score", "contradiction_level",
                    "integration_difficulty", "abstraction_level", "abstraction_rank", "coherence_scores",
                    "application_count", "synthesis_count")


def _quiet_logs() -> None:
    """Module-level stream handlers (operator modules add their own) -> off; the root file handler stays."""
    for lg in [logging.getLogger()] + [l for l in logging.Logger.manager.loggerDict.values()
                                       if isinstance(l, logging.Logger)]:
        for h in list(lg.handlers):
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler):
                lg.removeHandler(h)


def _jsonable(v: Any) -> bool:
    try:
        json.dumps(v)
        return True
    except (TypeError, ValueError):
        return False


class StackIdentity:
    """Shared runtime identity for training and chat over the same LQT model."""

    def __init__(self, loop, um, cfg):
        import numpy as np
        self.np, self.loop, self.um, self.cfg = np, loop, um, cfg
        self.chat_meta = {}
        self.rsl_records = []

    def _rebuild_evolution(self, stored: Dict[str, Any]) -> Dict[str, Any]:
        """CognitiveEngine._trigger_self_modification weights (evolution_cycle_N).

        Ints/floats that are not tensors: base_codebook_index, contribution_weight,
        dimension_size.  From ``stack['evolution']`` when the saving process recorded
        them; for a model written before that record existed they follow from the
        creating code: base_codebook_index = N % 10, dimension_size = hidden_dim,
        contribution_weight = 0.05 + 0.1 * perf with perf = phase_offsets[1] / pi
        (the code sets phase_offsets = [0, perf * pi])."""
        np, um, engine = self.np, self.um, self.loop.engine
        import torch
        import cognition.cognitive_engine as ce
        keys: Dict[str, int] = {}
        for name in um.meta:
            m = RE_EVOLUTION.match(name)
            if m:
                keys[m.group(1)] = int(m.group(2))
        registry = engine.weight_registry
        existing = set(getattr(registry, "_weights", {}))
        made, derived = [], []
        for key, n in sorted(keys.items(), key=lambda kv: kv[1]):
            if key in existing:
                continue
            p = f"engine.weight_registry._weights['{key}']."
            shape = lambda field: tuple(um.meta[p + field]["shape"])  # noqa: E731
            rec = stored.get(key)
            if rec is None:
                perf = float(um.cache[p + "phase_offsets"].reshape(-1)[1]) / np.pi
                rec = {"base_codebook_index": n % 10, "dimension_size": shape("base_phase")[0],
                       "contribution_weights": [0.05 + 0.1 * perf] if (p + "recursive_refs.0.relative_position") in um.meta else [],
                       "derived": True}
                derived.append(key)
            refs = [ce.RecursiveReference(relative_position=torch.zeros(shape(f"recursive_refs.{i}.relative_position")),
                                          contribution_weight=float(cw),
                                          transformation_matrix=torch.zeros(shape(f"recursive_refs.{i}.transformation_matrix")))
                    for i, cw in enumerate(rec["contribution_weights"])]
            w = ce.RecursiveWeight(
                base_codebook_index=int(rec["base_codebook_index"]),
                tensor_position=torch.zeros(shape("tensor_position")),
                phase_transform=ce.PhaseTransformation(base_phase=torch.zeros(shape("base_phase")),
                                                       harmonic_amplitudes=torch.zeros(shape("harmonic_amplitudes")),
                                                       frequencies=torch.zeros(shape("frequencies")),
                                                       phase_offsets=torch.zeros(shape("phase_offsets"))),
                recursive_refs=refs,
                error_preservation=torch.zeros(shape("error_preservation")),
                dimension_size=int(rec["dimension_size"]))
            registry.register_weight(key, w)
            made.append(key)
        # Effective RW state is allocated lazily by forward(). Recreate its owner
        # before the saved tensors are applied, including the base thought weight.
        for key, weight in registry._weights.items():
            for field in ('_ema_effective_weight', '_last_effective_weight'):
                name = f"engine.weight_registry._weights[{key!r}].{field}"
                if name in um.meta:
                    setattr(weight, field, torch.zeros(tuple(um.meta[name]['shape'])))
        if keys:
            engine.evolution_cycles = max(int(getattr(engine, "evolution_cycles", 0)), max(keys.values()))
        return {"rebuilt": len(made), "derived_scalars": len(derived)}

    def _rebuild_rwa(self) -> Dict[str, Any]:
        """IALA RWA content weights (rw_content_<sha16>): id is the whole identity
        (LocalRWARegistry.create_weight(id)); the three tensors come from the model."""
        iala = self.loop.iala
        registry = iala.knowledge_graph.recursive_weight_registry
        ids = sorted({m.group(1) for m in (RE_RWA.match(n) for n in self.um.meta) if m})
        made = 0
        for wid in ids:
            if wid in iala.rwa_store:
                continue
            iala.rwa_store[wid] = registry.create_weight(wid, initial_complexity=0.0)
            made += 1
        return {"rebuilt": made}

    def _rebuild_kg(self, stored: Dict[str, Any]) -> Dict[str, Any]:
        """IALA knowledge entities: text + scalars from stack['kg_entities']; their
        RecursiveWeight is LocalRWARegistry.create_weight(hash), tensors from the model."""
        from runtime.autodidactic_learning import TriaxialKnowledgeEntity
        kg = self.loop.iala.knowledge_graph
        made = 0
        for h, rec in stored.items():
            if h in kg.entities:
                continue
            w = kg.recursive_weight_registry.create_weight(h, initial_complexity=len(rec["content_text"]) / 1000.0)
            ent = TriaxialKnowledgeEntity(recursive_weight=w, **{k: rec[k] for k in KG_ENTITY_FIELDS if k in rec})
            kg.entities[h] = ent
            kg.relationship_graph.add_node(h, entity=ent)
            made += 1
        return {"rebuilt": made}

    def _resolve(self, path: str) -> Any:
        roots = {"motivation": self.loop.motivation, "engine": self.loop.engine, "iala": self.loop.iala}
        head, *rest = path.split(".")
        obj = roots[head]
        for part in rest:
            obj = getattr(obj, part)
        return obj

    def _rebuild_dataclasses(self, stored: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Canon motivation entities (dataclasses keyed in dict containers): non-float
        fields from the stack; float fields are the model tensor's elements and are
        set by the apply step that follows."""
        import importlib
        made = 0
        for rec in stored:
            cont = self._resolve(rec["container"])
            if rec["key"] in cont:
                continue
            mod, qual = rec["cls"].split(":")
            cls = getattr(importlib.import_module(mod), qual)
            obj = cls.__new__(cls)
            for f in dataclasses.fields(cls):
                if f.name in rec["fields"]:
                    setattr(obj, f.name, rec["fields"][f.name])
                elif f.name in rec["float_fields"]:
                    setattr(obj, f.name, 0.0)     # element of the model tensor, applied next
                elif f.default is not dataclasses.MISSING:
                    setattr(obj, f.name, f.default)
                elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
                    setattr(obj, f.name, f.default_factory())       # type: ignore[misc]
            cont[rec["key"]] = obj
            made += 1
        return {"rebuilt": made}

    # ------------------------------------------------------------------ stack identity

    def _stack(self) -> Dict[str, Any]:
        """JSON identity of run-time entities (no float tensor values)."""
        engine, iala = self.loop.engine, self.loop.iala
        evo = {}
        for key, w in getattr(engine.weight_registry, "_weights", {}).items():
            if not key.startswith("evolution_cycle_"):
                continue
            refs = getattr(w, "recursive_refs", [])
            evo[key] = {"base_codebook_index": int(getattr(w, "base_codebook_index", 0)),
                        "dimension_size": int(getattr(w, "dimension_size", self.cfg.hidden_dim)),
                        "contribution_weights": [float(r.contribution_weight) for r in refs]}
        kg = {}
        for h, e in iala.knowledge_graph.entities.items():
            kg[h] = {k: getattr(e, k) for k in KG_ENTITY_FIELDS}
            kg[h]["ethical_vector"] = [float(x) for x in kg[h]["ethical_vector"]]
            kg[h]["coherence_scores"] = {k: float(v) for k, v in kg[h]["coherence_scores"].items()}
            for k in ("timestamp", "ethical_coherence", "reliability_score", "contradiction_level",
                      "integration_difficulty"):
                kg[h][k] = float(kg[h][k])
        entities, skipped = [], 0
        for cpath, cont in self._motivation_containers():
            for key, obj in cont.items():
                if not dataclasses.is_dataclass(obj) or not isinstance(key, str):
                    skipped += 1
                    continue
                fields, floats, ok = {}, [], True
                for f in dataclasses.fields(obj):
                    v = getattr(obj, f.name)
                    if isinstance(v, float) and not isinstance(v, bool):
                        floats.append(f.name)
                    elif _jsonable(v):
                        fields[f.name] = v
                    else:
                        ok = False
                        break
                if not ok:
                    skipped += 1
                    continue
                cls = type(obj)
                entities.append({"container": cpath, "key": key, "cls": f"{cls.__module__}:{cls.__qualname__}",
                                 "fields": fields, "float_fields": floats})
        self.chat_meta["identity_skipped"] = skipped
        breath = getattr(self.loop, "breath", None)
        breath_state = None
        if breath is not None:
            breath_state = {
                "phase_accumulator": float(breath.phase_accumulator.detach().item()),
                "cycle_count": int(getattr(breath, "cycle_count", 0)),
            }
        return {"chat": self.chat_meta, "voice_replay": self.voice_replay[-512:],
                "evolution": evo, "kg_entities": kg, "entities": entities,
                "iala": iala.export_identity(), "bayes": self.loop.bayes.export_identity(),
                "rsei": self.loop.rsei.export_state(), "step_index": self.loop.step_index,
                "breath": breath_state,
                "rsl": [{k: r[k] for k in ("content", "memory_type", "metadata", "ethical_context")}
                        for r in self.rsl_records]}

    def _motivation_containers(self) -> List[Tuple[str, Dict[str, Any]]]:
        from cognition.lqt_bridge import MOTIVATION_CONTAINERS
        out, seen = [], set()

        def find(obj: Any, path: str, depth: int) -> None:
            if depth > 4 or not hasattr(obj, "__dict__"):
                return
            for k, v in vars(obj).items():
                if k in MOTIVATION_CONTAINERS and isinstance(v, dict):
                    if id(v) not in seen:
                        seen.add(id(v))
                        out.append((f"{path}.{k}", v))
                elif hasattr(v, "__dict__") and (type(v).__module__ or "").startswith(("runtime", "rosemary.canon")):
                    find(v, f"{path}.{k}", depth + 1)
        find(self.loop.motivation, "motivation", 0)
        return out


class ChatSession(StackIdentity):
    """One process talking to one model.lqt."""

    def __init__(self, model_path: Path, args: argparse.Namespace):
        import numpy as np
        from cognition.lqt_bridge import UnifiedModel, bind_unified, collect_live_tensors, get_backend
        from runtime.rosemary_full import RosemaryFullConfig, RosemaryFullLoop

        self.np = np
        self.args = args
        self.collect = collect_live_tensors
        self.model_path = model_path
        self.work = model_path.parent / "chat"
        (self.work / "state").mkdir(parents=True, exist_ok=True)
        self.L = get_backend("native").L

        run_cfg = self._run_config(model_path.parent / "run.json")
        cfg = RosemaryFullConfig(out_dir=self.work, seed=int(run_cfg.get("seed", args.seed)),
                                 hidden_dim=int(run_cfg.get("hidden_dim", 64)),
                                 seq_len=int(run_cfg.get("seq_len", 4)),
                                 metacog_state_dim=int(run_cfg.get("metacog_state_dim", 64)),
                                 eta=float(run_cfg.get("eta", 0.05)),
                                 weight_bits=int(run_cfg.get("weight_bits", 4)),
                                 lqt_backend="native",
                                 engine_learner=bool(run_cfg.get("engine_learner", True)),
                                 rest_consciousness=bool(args.mrc))
        self.cfg = cfg
        t0 = time.time()
        self.genesis = not model_path.exists()
        if self.genesis:
            self.um = UnifiedModel(self.L, model_path)
        else:
            self.um = UnifiedModel.load(self.L, model_path)
        bind_unified(self.um)
        self.loop = RosemaryFullLoop(cfg)
        _quiet_logs()
        if self.loop.store.native is None or self.loop.store.native.unified is not self.um:
            raise RuntimeError("backbone Psi store is not bound to the loaded model.lqt")
        self.load_info: Dict[str, Any] = {"genesis": self.genesis, "run_config": run_cfg}
        self.dormant: set = set()
        self.rsl_records: List[Dict[str, Any]] = []
        self.voice_replay: List[Dict[str, Any]] = []
        self.chat_meta: Dict[str, Any] = {"turns_total": 0, "sessions": 0}
        if self.genesis:
            live = self.collect(self.loop.engine, self.loop.iala, self.loop.bayes, self.loop.motivation)
            self.um.genesis(live)
            self.load_info.update({"tensors": len(self.um.meta), "live_tensors": len(live)})
        else:
            self._attach_loaded()
        self.chat_meta["sessions"] = int(self.chat_meta.get("sessions", 0)) + 1
        self.um.stack = self._stack()
        save = self.um.save()
        self.load_info.update({"seconds": time.time() - t0, "save_after_load": save})
        self.iala_filter = None
        if args.iala_filter:
            if args.iala_filter == "selfmod":
                from runtime.selfmod.config import IALA_FILTER as spec
            else:
                th, prior = (float(x) for x in args.iala_filter.split(","))
                spec = {"acceptance_threshold": th, "neutral_prior": prior}
            self.iala_filter = self.loop.iala.knowledge_graph.ethical_filter.configure(**spec)
        from rosemary.canon.fbs_tokenizer import SacredFBS_Tokenizer
        self.tokenizer = SacredFBS_Tokenizer()
        _quiet_logs()
        self.turn_identity = []
        self.turn_ops: List[int] = []         # logged mutations per turn (for /rollback)
        self.turn_rsl: List[int] = []         # RSL records added per turn
        self.turns_this_session = 0
        self.transcript = self.work / "transcript.jsonl"
        import torch
        self.voice_optimizer = torch.optim.AdamW(self.loop.engine.native_voice.parameters(), lr=2e-3,
                                                  weight_decay=1e-4)

    # ------------------------------------------------------------------ load

    @staticmethod
    def _run_config(path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        cfg = json.loads(path.read_text()).get("config", {})
        return {k: cfg[k] for k in ("seed", "hidden_dim", "seq_len", "metacog_state_dim", "eta",
                                    "weight_bits", "engine_learner") if k in cfg}

    def _attach_loaded(self) -> None:
        """Rebuild owners of stored run-time tensors, then every live tensor takes the model's value."""
        np = self.np
        um, loop = self.um, self.loop
        stack = dict(um.stack)
        self.chat_meta = {"turns_total": 0, "sessions": 0,
                          **dict(stack.get("chat", self.chat_meta))}
        self.voice_replay = list(stack.get("voice_replay", []))[-512:]
        loop.iala.restore_identity(stack.get("iala", {}))
        loop.bayes.restore_identity(stack.get("bayes", {}))
        loop.rsei.restore_state(stack.get("rsei", {}))
        loop.step_index = int(stack.get("step_index", self.chat_meta.get("turns_total", 0)))
        breath_state = stack.get("breath") or {}
        transcript_path = self.work / "transcript.jsonl"
        prior_records: List[Dict[str, Any]] = []
        if transcript_path.exists():
            for line in transcript_path.read_text(encoding="utf-8").splitlines()[-5:]:
                try:
                    prior_records.append(json.loads(line).get("record", {}))
                except (json.JSONDecodeError, TypeError):
                    continue
        # Migration for models saved before breath identity became part of the
        # unified stack: recover the last observed oscillator coordinate once.
        if not breath_state and prior_records:
            breath_state = {"phase_accumulator": prior_records[-1].get("breath_accumulator", 0.0),
                            "cycle_count": 0}
        if breath_state:
            loop.breath.phase_accumulator.data.fill_(float(breath_state.get("phase_accumulator", 0.0)))
            loop.breath.cycle_count = int(breath_state.get("cycle_count", 0))
        loop._recent.extend(r for r in prior_records if r)
        rebuilt = {"evolution_weights": self._rebuild_evolution(stack.get("evolution", {})),
                   "rwa_content": self._rebuild_rwa(),
                   "kg_entities": self._rebuild_kg(stack.get("kg_entities", {})),
                   "dataclass_entities": self._rebuild_dataclasses(stack.get("entities", []))}
        rsl = stack.get("rsl", [])
        t_rsl = time.time()
        for r in rsl:
            mid = loop.memory.store_memory(content=r["content"], memory_type=r["memory_type"],
                                           metadata=r.get("metadata"), ethical_context=r.get("ethical_context"))
            self.rsl_records.append({**r, "memory_id": mid})
        live = self.collect(loop.engine, loop.iala, loop.bayes, loop.motivation)
        live_only = sorted(set(live) - set(um.meta))
        self.dormant = {n for n in um.meta if n not in live and um.meta[n]["group"] != "psi"}
        applied = 0
        for name, t in live.items():
            if name not in um.meta:
                continue        # attached as a logged TensorAttach at the first sync
            got = t.get()
            if tuple(got.shape) != tuple(um.meta[name]["shape"]):
                raise RuntimeError(f"{name}: live shape {tuple(got.shape)} != model {um.meta[name]['shape']}")
            t.set(um.cache[name])
            applied += 1
        for n in loop.WEIGHTS:
            if not np.array_equal(loop.field.W[n], um.cache[n]):
                raise RuntimeError(f"{n}: backbone Psi does not equal model.lqt after load")
        groups: Dict[str, int] = {}
        for n in self.dormant:
            groups[um.meta[n]["group"]] = groups.get(um.meta[n]["group"], 0) + 1
        self.load_info.update({"tensors": len(um.meta), "live_tensors": len(live), "applied": applied,
                               "rebuilt": rebuilt, "live_only_to_attach": len(live_only),
                               "dormant": len(self.dormant), "dormant_groups": groups,
                               "rsl_restored": len(rsl), "rsl_restore_seconds": time.time() - t_rsl,
                               "loaded_from": um.loaded_from})

    # ------------------------------------------------------------------ recall

    def _resonance(self, a: Any, b: Any) -> float:
        np = self.np
        na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
        if na == 0.0 or nb == 0.0:
            return 0.0
        return float((np.dot(a, b) / (na * nb) + 1.0) / 2.0)

    def recall(self, text: str, k: int = 3) -> Dict[str, Any]:
        """What the system stored before this turn that relates to ``text``."""
        sub = self.tokenizer.substrate
        q = sub.extract_fbs(text)
        kg = self.loop.iala.knowledge_graph
        ents = self.loop.iala.synthesis_engine.rta_attention.select(text, list(kg.entities.values()), max_entities=k)
        iala_hits = [{"text": e.content_text, "source": e.source_url, "archetype": e.ethical_archetype,
                      "fbs_resonance": self._resonance(q, sub.extract_fbs(e.content_text))} for e in ents]
        mem_hits = []
        for r in self.rsl_records:
            got = self.loop.memory.retrieve_memory(r["memory_id"])
            if got is None:
                raise RuntimeError(f"RSL memory {r['memory_id']} recorded but not retrievable")
            content = str(got["content"])
            mem_hits.append({"text": content, "memory_type": r["memory_type"], "turn": (r.get("metadata") or {}).get("turn"),
                             "fbs_resonance": self._resonance(q, sub.extract_fbs(content))})
        mem_hits.sort(key=lambda h: h["fbs_resonance"], reverse=True)
        return {"iala": iala_hits, "rsl": mem_hits[:k], "iala_entities": len(kg.entities),
                "rsl_records": len(self.rsl_records)}

    # ------------------------------------------------------------------ turn

    def turn(self, text: str) -> Dict[str, Any]:
        np, um, loop = self.np, self.um, self.loop
        t0 = time.time()
        pre = self.recall(text)
        t_recall = time.time() - t0
        fbs = self.tokenizer.encode(text)
        depth0 = int(um.model.undo_depth)
        log0 = len(um.model.edit_log())
        n_rsl0 = len(self.rsl_records)
        dlog = loop.iala.ethical_filter.decision_log
        n_dec0 = len(dlog)
        idx = self.chat_meta["turns_total"] + 1
        t1 = time.time()
        self.turn_identity.append({
            "iala": copy.deepcopy(loop.iala.export_identity()),
            "bayes": copy.deepcopy(loop.bayes.export_identity()),
            "rsei": copy.deepcopy(loop.rsei.export_state()),
            "step_index": loop.step_index,
            "breath_accumulator": float(loop.breath.phase_accumulator.detach().item()),
            "breath_cycle_count": int(loop.breath.cycle_count),
        })
        rec = loop.step({"source": "manual_input", "index": str(idx), "text": text})
        t_step = time.time() - t1
        voice = loop.engine.native_voice
        native_text, native_conf = "", 0.0
        if voice.ready:
            generated, scores = voice.generate(loop._engine_out["voice_state"], greedy=True)
            native_text, native_conf = generated[0], scores[0]
        # the canon loop stored this turn as an RSL episodic memory under rec['rsl_memory_id'] (prefix);
        # find it by content so recall can fetch it next turn
        mid = self._last_memory_id(text)
        self.rsl_records.append({"content": text, "memory_type": "episodic", "memory_id": mid,
                                 "metadata": {"turn": idx, "breath": rec["breath_phase"]},
                                 "ethical_context": dict(zip(("good_harm", "truth_deception", "fairness_bias",
                                                              "liberty_constraint", "care_harm"),
                                                             rec["ethical_features"]))})
        for m in self._dream_memories(rec):
            self.rsl_records.append(m)
        t2 = time.time()
        live = self.collect(loop.engine, loop.iala, loop.bayes, loop.motivation)
        st = um.sync(live, keep=self.dormant)
        loop.rsei.notify_lqt_sync(st, bool(um.model.verify_edit_log()))
        t_sync = time.time() - t2
        ops = int(um.model.undo_depth) - depth0
        self.turn_ops.append(ops)
        self.turn_rsl.append(len(self.rsl_records) - n_rsl0)
        self.chat_meta["turns_total"] = idx
        self.turns_this_session += 1
        decisions = [d for d in list(dlog)[n_dec0:] if d.get("content_head") == text[:80]]
        saved = None
        if self.args.save_every > 0 and self.turns_this_session % self.args.save_every == 0:
            saved = self.save()
        out = {"turn": idx, "text": text, "recall": pre, "record": rec, "ethical_decision": decisions[-1] if decisions else None,
               "native_voice": {"ready": voice.ready, "text": native_text, "confidence": native_conf,
                                "training_steps": int(voice.training_steps.item()),
                                "examples_seen": int(voice.examples_seen.item())},
               "fbs_norm": float(np.linalg.norm(fbs)), "fbs_dim": int(fbs.shape[0]),
               "lqt": {"ops": ops, "edit_log_before": log0, "edit_log_after": len(um.model.edit_log()),
                       "edited": st["edited"], "attached": st["attached"], "detached": st["detached"],
                       "elements_changed": st["elements_changed"], "tensors": len(um.meta),
                       "verify_edit_log": bool(um.model.verify_edit_log())},
               "saved": saved,
               "seconds": {"recall": t_recall, "step": t_step, "sync": t_sync, "total": time.time() - t0}}
        out["reply"] = native_text if voice.ready and native_text else self.compose(out)
        with open(self.transcript, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: out[k] for k in ("turn", "text", "reply", "record", "ethical_decision", "lqt", "seconds")}, default=str) + "\n")
        return out

    def teach_voice(self, target: str, repeats: int = 1) -> Dict[str, Any]:
        """Ground the current cognitive state in an utterance.

        The target is intentionally never sent to ``loop.step``.  This enforces
        the tutor boundary: it changes voice parameters only, never IALA or the
        cognitive state that the voice is learning to express.
        """
        import torch
        if not target.strip():
            raise ValueError("voice target cannot be empty")
        state = self.loop._engine_out["voice_state"].detach()
        history = []
        voice = self.loop.engine.native_voice
        voice.train()
        for _ in range(max(1, int(repeats))):
            self.voice_optimizer.zero_grad(set_to_none=True)
            losses = voice.loss(state, [target])
            losses["loss"].backward()
            torch.nn.utils.clip_grad_norm_(voice.parameters(), 1.0)
            self.voice_optimizer.step()
            voice.note_training(1, float(losses["loss"].detach()))
            history.append({k: float(v.detach()) for k, v in losses.items()})
        voice.eval()
        self.voice_replay.append({"prompt": self.loop.engine.thought_state.problem_representation,
                                  "target": target, "turn": self.chat_meta["turns_total"]})
        live = self.collect(self.loop.engine, self.loop.iala, self.loop.bayes, self.loop.motivation)
        synced = self.um.sync(live, keep=self.dormant)
        self.loop.rsei.notify_lqt_sync(synced, bool(self.um.model.verify_edit_log()))
        self.um.stack = self._stack()
        return {"updates": len(history), "first": history[0], "last": history[-1],
                "training_steps": int(voice.training_steps.item()), "lqt": synced}

    def _last_memory_id(self, content: str) -> str:
        """Id of the episodic memory the canon loop just stored for this turn (rec['rsl_memory_id'] is a prefix)."""
        mem = self.loop.memory
        for mid in reversed(list(mem.active_memories)):
            if mem.active_memories[mid]["content"] == content and \
                    mem.memory_metadata.get(mid, {}).get("memory_type") == "episodic":
                return mid
        raise RuntimeError("RSL active_memories holds no episodic memory for this turn")

    def _dream_memories(self, rec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Dream memories the canon loop stored this step (exit_dream integrate_memories=True)."""
        if rec.get("dream_event") != "exited":
            return []
        mem = self.loop.memory
        out = []
        for mid, md in mem.memory_metadata.items():
            if md.get("memory_type") == "dream" and (md.get("metadata") or {}).get("step") == self.loop.step_index:
                out.append({"content": mem.active_memories[mid]["content"], "memory_type": "dream", "memory_id": mid,
                            "metadata": {"turn": self.chat_meta["turns_total"] + 1, **md["metadata"]},
                            "ethical_context": None})
        return out

    def compose(self, t: Dict[str, Any]) -> str:
        """The reply: stored text the system recalled + the turn's computed state."""
        r = t["record"]
        lines: List[str] = []
        recall = t["recall"]
        if recall["iala"]:
            for h in recall["iala"]:
                lines.append(f'IALA recall [{h["archetype"]}, res {h["fbs_resonance"]:.3f}]: {h["text"][:300]}')
        if recall["rsl"]:
            for h in recall["rsl"]:
                lines.append(f'RSL {h["memory_type"]} memory (turn {h["turn"]}, res {h["fbs_resonance"]:.3f}): {h["text"][:300]}')
        if not recall["iala"] and not recall["rsl"]:
            lines.append(f'recall: nothing stored yet (IALA entities {recall["iala_entities"]}, '
                         f'RSL records {recall["rsl_records"]})')
        for m in self.rsl_records:
            if m["memory_type"] == "dream" and m["metadata"].get("turn") == t["turn"]:
                lines.append(f'dream memory ({m["metadata"].get("dream_type")}): {str(m["content"])[:300]}')
        d = t["ethical_decision"]
        verdict = (f'{"accepted" if d["accepted"] else "rejected"} (p={d["acceptance_probability"]:.3f} vs '
                   f'{d["threshold"]:.3f})') if d else "no filter decision (rw-file save path)"
        errs = ",".join(e for e in (r.get("meta_reflection_errors") or []) if e) or "none"
        lines.append(f'state: mode {r["cognitive_mode"].split(".")[-1]} | breath {r["breath_phase"]} | '
                     f'q {r["reflection_quality"]:.4f} nov {r["reflection_novelty"]:.4f} '
                     f'align {r["reflection_alignment"]:.4f} conf {r["reflection_confidence"]:.4f} | '
                     f'meta {r["meta_confidence"]:.4f} errors {errs} | eth {r["ethical_alignment"]:.4f} '
                     f'IALA filter {verdict} | severity {r["contradiction_severity"]:.3f} | '
                     f'drive {r["motivation_drive"]:.4f} adv {r["advantage"]:+.4f}')
        return "\n".join(lines)

    # ------------------------------------------------------------------ commands

    def save(self) -> Dict[str, Any]:
        self.um.stack = self._stack()
        return self.um.save()

    def rollback(self, n_turns: int) -> Dict[str, Any]:
        """Undo the last ``n_turns`` turns' logged mutations on the model; the live
        stack takes the model's values again.  Run-time owners whose tensors the
        rollback detached are removed from their containers.  Non-tensor process
        state (RSL memory system contents, breath oscillator, canon motivation
        experience queues) is not rewound; the turns' RSL records are dropped
        from recall and from the saved stack."""
        np, um, loop = self.np, self.um, self.loop
        n_turns = min(int(n_turns), len(self.turn_ops))
        if n_turns <= 0:
            return {"rolled_back_turns": 0}
        identity = self.turn_identity[-n_turns]
        del self.turn_identity[-n_turns:]
        ops = sum(self.turn_ops[-n_turns:])
        log0 = len(um.model.edit_log())
        um.rollback(ops)
        del self.turn_ops[-n_turns:]
        drop = sum(self.turn_rsl[-n_turns:])
        del self.turn_rsl[-n_turns:]
        if drop:
            del self.rsl_records[-drop:]
        self.chat_meta["turns_total"] -= n_turns
        loop.iala.restore_identity(identity["iala"])
        loop.bayes.restore_identity(identity["bayes"])
        loop.rsei.restore_state(identity["rsei"])
        loop.step_index = int(identity["step_index"])
        loop.breath.phase_accumulator.data.fill_(float(identity["breath_accumulator"]))
        loop.breath.cycle_count = int(identity["breath_cycle_count"])
        removed = self._remove_unowned()
        live = self.collect(loop.engine, loop.iala, loop.bayes, loop.motivation)
        for name, t in live.items():
            if name in um.meta and tuple(t.get().shape) == tuple(um.meta[name]["shape"]):
                t.set(um.cache[name])
        for n in loop.WEIGHTS:
            loop.field.W[n] = np.array(um.cache[n], dtype=np.float32)
        loop.store._cache.clear()
        live_only = sorted(set(live) - set(um.meta))
        return {"rolled_back_turns": n_turns, "mutations_undone": ops, "edit_log_before": log0,
                "edit_log_after": len(um.model.edit_log()), "owners_removed": removed,
                "live_tensors_not_in_model": live_only[:10], "n_live_not_in_model": len(live_only),
                "verify_edit_log": bool(um.model.verify_edit_log())}

    def _remove_unowned(self) -> Dict[str, int]:
        """After a rollback: drop run-time owners whose tensors are no longer in the model."""
        um, loop = self.um, self.loop
        names = set(um.meta)
        out = {"evolution": 0, "rwa": 0, "kg": 0, "motivation": 0}
        reg = getattr(loop.engine.weight_registry, "_weights", {})
        for key in [k for k in reg if k.startswith("evolution_cycle_")]:
            if not any(n.startswith(f"engine.weight_registry._weights['{key}'].") for n in names):
                del reg[key]
                out["evolution"] += 1
        for wid in list(loop.iala.rwa_store):
            if not any(n.startswith(f"engine.autodidactic_learner.rwa_store['{wid}'].") for n in names):
                del loop.iala.rwa_store[wid]
                out["rwa"] += 1
        kg = loop.iala.knowledge_graph
        for h in list(kg.entities):
            if not any(f"['{h}']" in n for n in names):
                del kg.entities[h]
                if kg.relationship_graph.has_node(h):
                    kg.relationship_graph.remove_node(h)
                out["kg"] += 1
        reg_w = getattr(kg.recursive_weight_registry, "weights", {})
        out["iala_registry"] = 0
        for wid in list(reg_w):
            if wid not in loop.iala.rwa_store and wid not in kg.entities and not any(f"['{wid}']" in n for n in names):
                del reg_w[wid]
                out["iala_registry"] += 1
        for cpath, cont in self._motivation_containers():
            for key in list(cont):
                if f"{cpath}[{key!r}]" not in names and dataclasses.is_dataclass(cont[key]) and \
                        any(isinstance(getattr(cont[key], f.name), float) for f in dataclasses.fields(cont[key])):
                    del cont[key]
                    out["motivation"] += 1
        return out

    def state(self) -> Dict[str, Any]:
        um, loop = self.um, self.loop
        mm = loop.memory.get_system_metrics()
        return {"model": str(self.model_path), "tensors": len(um.meta), "dormant": len(self.dormant),
                "edit_log_entries": len(um.model.edit_log()), "undo_depth": int(um.model.undo_depth),
                "verify_edit_log": bool(um.model.verify_edit_log()), "turns_total": self.chat_meta["turns_total"],
                "turns_this_session": self.turns_this_session, "sessions": self.chat_meta.get("sessions"),
                "ops_per_turn": self.turn_ops, "iala_entities": len(loop.iala.knowledge_graph.entities),
                "iala_rwa_store": len(loop.iala.rwa_store), "rsl_records": len(self.rsl_records),
                "rsl_active_memories": mm["active_memories"],
                "evolution_cycles": int(getattr(loop.engine, "evolution_cycles", 0)),
                "native_voice": {"ready": loop.engine.native_voice.ready,
                                 "training_steps": int(loop.engine.native_voice.training_steps.item()),
                                 "examples_seen": int(loop.engine.native_voice.examples_seen.item()),
                                 "last_training_loss": float(loop.engine.native_voice.last_training_loss.item()),
                                 "replay_examples": len(self.voice_replay)},
                "rsei": loop.rsei.engine.metrics(),
                "bayesian_parameters": len(loop.bayes.parameter_beliefs),
                "breath_phase": loop.breath.update_phase(0.0)["dominant_phase"],
                "rest_mrc": self.cfg.rest_consciousness, "op_counts": um.op_counts}

    def close(self) -> Dict[str, Any]:
        info = self.save()
        self.loop.close()
        return info


def _print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str), flush=True)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", type=Path, required=True, help="unified model.lqt (created by genesis if absent)")
    ap.add_argument("--once", default=None, help="run one turn on this text, save, exit")
    ap.add_argument("--save-every", type=int, default=5, help="save model.lqt every N turns (0: only on exit)")
    ap.add_argument("--mrc", action="store_true", help="run the REST-phase MRC fixed point (slow)")
    ap.add_argument("--seed", type=int, default=0, help="seed when the model dir has no run.json")
    ap.add_argument("--iala-filter", default=None,
                    help="IALA EthicalLearningFilter setting: 'selfmod' (runtime/selfmod/config.IALA_FILTER) or "
                         "THRESHOLD,NEUTRAL_PRIOR; default: the filter's own defaults, as the model's run used")
    ap.add_argument("--json", action="store_true", help="print each turn's full record as JSON")
    a = ap.parse_args(argv)

    # builtin hash() is salted per process; canon modules use it for vectors/ids (as runtime.rosemary_full).
    if os.environ.get("PYTHONHASHSEED") != str(a.seed):
        env = dict(os.environ, PYTHONHASHSEED=str(a.seed))
        os.execve(sys.executable, [sys.executable, "-m", "runtime.chat", *(argv if argv is not None else sys.argv[1:])], env)

    model = a.model.resolve()
    (model.parent / "chat").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=str(model.parent / "chat" / "chat.log"), level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s", force=True)
    os.chdir(model.parent / "chat")       # canon/original modules write logs and yaml into CWD
    _quiet_logs()

    session = ChatSession(model, a)
    print(f"runtime.chat | model {model}", flush=True)
    print(f"  {'genesis (new file)' if session.genesis else 'loaded'}: {session.load_info['tensors']} tensors, "
          f"{session.load_info.get('dormant', 0)} dormant {session.load_info.get('dormant_groups', {})}, "
          f"rebuilt {session.load_info.get('rebuilt', {})}, RSL restored {session.load_info.get('rsl_restored', 0)}, "
          f"edit log {session.load_info['save_after_load']['edit_log_entries']} "
          f"verify {session.load_info['save_after_load']['verify_edit_log']}, {session.load_info['seconds']:.1f}s", flush=True)
    print(f"  {BANNER_SOURCE}", flush=True)
    print(f"  IALA ethical filter: {session.iala_filter if session.iala_filter else 'filter defaults (--iala-filter)'}",
          flush=True)
    print(f"  REST MRC fixed point: {'on' if a.mrc else 'off (--mrc)'}; save every {a.save_every} turns + on exit. "
          f"Commands: /state /save /teach TARGET /rollback N /quit", flush=True)

    def run_turn(text: str) -> None:
        out = session.turn(text)
        if a.json:
            _print({k: out[k] for k in ("turn", "recall", "record", "ethical_decision", "lqt", "seconds", "fbs_norm")})
        print(f"\n[turn {out['turn']}] you: {text}", flush=True)
        print(out["reply"], flush=True)
        s = out["seconds"]
        print(f"  (lqt ops {out['lqt']['ops']}: edited {out['lqt']['edited']} attached {out['lqt']['attached']} "
              f"detached {out['lqt']['detached']}; edit log {out['lqt']['edit_log_before']}->{out['lqt']['edit_log_after']} "
              f"verify {out['lqt']['verify_edit_log']}; {s['total']:.2f}s = recall {s['recall']:.2f} + step {s['step']:.2f} "
              f"+ sync {s['sync']:.2f}{'; saved' if out['saved'] else ''})", flush=True)

    def command(line: str) -> bool:
        parts = line.split()
        cmd = parts[0].lower()
        if cmd == "/quit":
            return False
        if cmd == "/state":
            _print(session.state())
        elif cmd == "/save":
            _print(session.save())
        elif cmd == "/rollback":
            if len(parts) != 2 or not parts[1].isdigit():
                print("usage: /rollback N", flush=True)
            else:
                _print(session.rollback(int(parts[1])))
        elif cmd == "/teach":
            target = line.partition(" ")[2]
            if not target:
                print("usage: /teach TARGET (grounds the preceding turn's cognitive state)", flush=True)
            else:
                _print(session.teach_voice(target, repeats=4))
        else:
            print(f"unknown command {cmd}; commands: /state /save /teach TARGET /rollback N /quit", flush=True)
        return True

    status = 0
    try:
        if a.once is not None:
            run_turn(a.once)
        else:
            interactive = sys.stdin.isatty()
            while True:
                if interactive:
                    try:
                        line = input("you> ")
                    except EOFError:
                        break
                else:
                    line = sys.stdin.readline()
                    if not line:
                        break
                line = line.strip()
                if not line:
                    continue
                if line.startswith("/"):
                    if not command(line):
                        break
                    continue
                run_turn(line)
    except KeyboardInterrupt:
        status = 130
    finally:
        info = session.close()
        print(f"saved {info['file']} ({info['bytes']} B) edit log {info['edit_log_entries']} "
              f"verify_edit_log {info['verify_edit_log']} sha256 {info['sha256'][:16]}", flush=True)
    return status


if __name__ == "__main__":
    sys.exit(main())
