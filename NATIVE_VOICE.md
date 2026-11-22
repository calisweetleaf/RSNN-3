# RSNN-3 native voice

The native voice is a downstream expression organ inside `CognitiveEngine`, not
an external reasoner. It maps the live ethically aligned cognitive state to UTF-8
bytes. Every emitted byte is causally fed into the next decoding step, and the
cognitive state is injected at every recurrent depth and timestep.

This replaces the supplied prototype's 50,000-token table (49,500 entries were
meaningless `<ext_N>` placeholders), non-causal sampling, heuristic quality
score, and random weight perturbation. Training now uses next-byte cross entropy
plus a state-reconstruction grounding loss.

All voice parameters and its training counters are children of the cognitive
engine, so `collect_live_tensors` stores and edits them in the same `model.lqt`.
The replay text is stored only as non-tensor model identity metadata.

## Grounding with a dataset

```bash
python -m runtime.train_native_voice \
  --model runtime/runs/rsnn3_release_seed1/model.lqt \
  --dataset voice_pairs.jsonl --epochs 3 --updates-per-example 4
```

Each JSONL row uses `prompt` and `target` (or `user` and `response`). The prompt
runs through the complete RSNN-3 loop. The target is withheld from that loop and
can update only native-voice parameters.

## OpenRouter as a speech tutor

```bash
export OPENROUTER_API_KEY=...
python -m runtime.train_native_voice \
  --model runtime/runs/rsnn3_release_seed1/model.lqt \
  --teacher-model provider/cheap-instruct-model
```

OpenRouter receives a bounded rendering of the current state and is instructed
to verbalize only that state. Its response never enters IALA, RSL memory,
Bayesian beliefs, the cognitive engine input, or the recursive reasoning field.
It is a supervised label, not imported cognition. Run without `--teacher-model`
for the built-in grounding baseline and no network dependency.

Interactive chat supports `/teach TARGET`, which grounds the preceding turn's
state. Until 20 real gradient updates have occurred, chat deliberately uses its
auditable recall/state rendering rather than emitting random initialized bytes.

Raw self-code is not used as conversational ground truth. Architecture
self-training should generate explicit comprehension, prediction, invariant,
and patch-evaluation objectives; otherwise it rewards source-code echo rather
than architectural understanding. That path can use the same tutor boundary,
but admission into cognition remains IALA's responsibility.
