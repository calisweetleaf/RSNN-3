#!/usr/bin/env python3
"""Ground RSNN-3's native voice in its own live cognitive states.

Examples may come from JSONL or an OpenRouter speech tutor.  Tutor responses are
labels only: they never enter the cognitive loop, IALA, memory, or beliefs.
All learned voice tensors are synchronized into the supplied unified model.lqt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List

import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.chat import ChatSession


BASELINE: List[Dict[str, str]] = [
    {"prompt": "Hello. Are you present?", "target": "I am present. What are we examining?"},
    {"prompt": "What just happened inside you?", "target": "I processed your words, updated my internal state, and checked what I already know before answering."},
    {"prompt": "If you are uncertain, say so directly.", "target": "I will distinguish what I know, what I infer, and what remains uncertain."},
    {"prompt": "Do not invent an answer.", "target": "If my state does not support an answer, I will say that the evidence is insufficient."},
    {"prompt": "What does learning mean here?", "target": "Learning means changing my retained representations through admitted evidence, not merely repeating text."},
    {"prompt": "What is your relationship to a speech tutor?", "target": "A speech tutor can shape how I express a state, but it does not supply that state or decide what I believe."},
    {"prompt": "Explain your answer compactly.", "target": "I will state the conclusion, the evidence that supports it, and any important uncertainty."},
    {"prompt": "Recall something relevant before answering.", "target": "I searched retained knowledge and memory for relevant material, then conditioned this response on the resulting state."},
    {"prompt": "Can your language change?", "target": "Yes. My voice uses an open byte vocabulary, so its learned forms can change without a fixed word dictionary."},
    {"prompt": "Are fluent words automatically true?", "target": "No. Fluency is expression; truth depends on the cognitive state, evidence, and consistency checks beneath it."},
    {"prompt": "Describe self-correction.", "target": "I compare output against reflection signals, retain the error, and alter the responsible parameters without rewriting the evidence."},
    {"prompt": "What should you do with contradiction?", "target": "I should preserve the contradiction, measure its severity, and resolve it through evidence rather than hide it."},
]


def load_jsonl(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        prompt = str(row.get("prompt", row.get("user", ""))).strip()
        target = str(row.get("target", row.get("response", ""))).strip()
        if not prompt or not target:
            raise ValueError(f"{path}:{number}: expected prompt/user and target/response")
        rows.append({"prompt": prompt, "target": target})
    return rows


class OpenRouterTutor:
    def __init__(self, model: str, api_key: str):
        self.model, self.api_key = model, api_key

    def teach(self, prompt: str, turn: Dict[str, Any]) -> str:
        record = turn["record"]
        state = {
            "mode": record["cognitive_mode"],
            "breath": record["breath_phase"],
            "reflection": {k: record[k] for k in ("reflection_quality", "reflection_novelty",
                                                    "reflection_alignment", "reflection_confidence")},
            "ethical_alignment": record["ethical_alignment"],
            "meta_confidence": record["meta_confidence"],
            "knowledge_used": record.get("knowledge_entities_used", []),
            "recall": turn["recall"],
        }
        instruction = (
            "You are a speech tutor for RSNN-3. Verbalize only the supplied internal state in a direct, "
            "natural response to the user. You are not its reasoner and must not add facts, hidden analysis, "
            "identity claims, or knowledge absent from the state. If support is insufficient, say so. "
            "Return only the utterance.\nUSER: " + prompt + "\nSTATE: " + json.dumps(state, default=str)
        )
        body = json.dumps({"model": self.model, "temperature": 0.25, "messages": [
            {"role": "system", "content": "Translate grounded cognitive state into concise speech."},
            {"role": "user", "content": instruction},
        ]}).encode("utf-8")
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {self.api_key}",
                                              "Content-Type": "application/json",
                                              "HTTP-Referer": "https://somnus.local/rsnn3",
                                              "X-Title": "RSNN-3 Native Voice"})
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"OpenRouter tutor request failed: {exc}") from exc
        return str(result["choices"][0]["message"]["content"]).strip()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", type=Path, required=True, help="unified model.lqt to update in place")
    parser.add_argument("--dataset", type=Path, help="JSONL with prompt/user and target/response fields")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--updates-per-example", type=int, default=7,
                        help="optimizer updates per four-example grounded batch")
    parser.add_argument("--teacher-model", help="OpenRouter model id; replaces each target with tutor output")
    parser.add_argument("--api-key-env", default="OPENROUTER_API_KEY")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(list(argv) if argv is not None else None)

    rows = load_jsonl(args.dataset) if args.dataset else list(BASELINE)
    tutor = None
    if args.teacher_model:
        key = os.environ.get(args.api_key_env, "")
        if not key:
            parser.error(f"--teacher-model requires ${args.api_key_env}")
        tutor = OpenRouterTutor(args.teacher_model, key)

    chat_args = SimpleNamespace(seed=args.seed, mrc=False, iala_filter=None, save_every=0, json=False)
    session = ChatSession(args.model.resolve(), chat_args)
    losses, utterances, grounded = [], [], []
    try:
        for epoch in range(max(1, args.epochs)):
            for index, row in enumerate(rows, 1):
                turn = session.turn(row["prompt"])
                target = tutor.teach(row["prompt"], turn) if tutor else row["target"]
                grounded.append((session.loop._engine_out["voice_state"].detach().cpu(), target))
                utterances.append({"epoch": epoch + 1, "index": index,
                                   "prompt": row["prompt"], "target": target})
                print(f"grounded epoch={epoch + 1} example={index}/{len(rows)}", flush=True)

        # Train after collecting states.  This matters for unified LQT: interleaving
        # optimizer updates with cognitive turns would log a full voice edit at every
        # example.  Batching produces the same gradients with one final atomic sync.
        voice = session.loop.engine.native_voice
        voice.train()
        # Keep the grounding set in one batch when practical.  Sequential tiny
        # batches made the recursive decoder overwrite earlier speech mappings.
        batch_size = min(16, len(grounded))
        for start in range(0, len(grounded), batch_size):
            batch = grounded[start:start + batch_size]
            states = torch.cat([item[0] for item in batch], dim=0)
            targets = [item[1] for item in batch]
            for _ in range(max(1, args.updates_per_example)):
                session.voice_optimizer.zero_grad(set_to_none=True)
                learned = voice.loss(states, targets)
                learned["loss"].backward()
                torch.nn.utils.clip_grad_norm_(voice.parameters(), 1.0)
                session.voice_optimizer.step()
                voice.note_training(len(batch), float(learned["loss"].detach()))
                losses.append(float(learned["loss"].detach()))
                last = {k: float(v.detach()) for k, v in learned.items()}
            print(f"trained batch={start // batch_size + 1} loss={last['loss']:.4f} "
                  f"lang={last['language']:.4f} ground={last['grounding']:.4f}", flush=True)
        voice.eval()
        evaluations = []
        with torch.no_grad():
            for state, target in grounded:
                generated, confidence = voice.generate(state, max_bytes=min(256, voice.config.max_bytes),
                                                        greedy=True)
                evaluations.append({"target": target, "generated": generated[0],
                                    "confidence": confidence[0]})
        session.voice_replay.extend({"prompt": item["prompt"], "target": item["target"],
                                     "turn": item["index"]} for item in utterances)
        live = session.collect(session.loop.engine, session.loop.iala, session.loop.bayes,
                               session.loop.motivation)
        sync = session.um.sync(live, keep=session.dormant)
        session.loop.rsei.notify_lqt_sync(sync, bool(session.um.model.verify_edit_log()))
        report = {
            "model": str(args.model.resolve()), "examples": len(rows), "epochs": args.epochs,
            "updates": ((len(grounded) + batch_size - 1) // batch_size) * max(1, args.updates_per_example),
            "teacher_model": args.teacher_model, "tutor_boundary": "voice weights only",
            "loss_first": losses[0], "loss_last": losses[-1], "utterances": utterances,
            "loss_curve": losses, "evaluations": evaluations,
            "lqt_sync": sync,
            "state": session.state(),
        }
        report_path = args.model.resolve().parent / "native_voice_training.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        session.save()
        print(json.dumps({k: report[k] for k in ("model", "examples", "epochs", "updates",
                                                  "teacher_model", "loss_first", "loss_last")}, indent=2))
    finally:
        session.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
