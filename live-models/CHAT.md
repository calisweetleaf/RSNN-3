# RSNN-3: run the unified model (`runtime/chat.py`)

## 1. Build `lqt_native` (pybind11 module over the C++ liblqt)

Needs Python 3.12, CMake >= 3.16, Ninja, a C++17 compiler, and pip packages
`numpy torch scipy networkx pyyaml matplotlib requests psutil pybind11 prometheus-client lz4 cryptography pydantic`
(versions used on 2026-11-21: numpy 2.5.5, torch 2.15.0+cpu, scipy 1.18.1,
networkx 3.7, pyyaml 6.0.4, pybind11 3.1.0).

```sh
# forge sandbox: the toolchain env gives zig (zcc/zcxx/zar/zranlib), cmake, ninja, the venv
. ../.toolchain/env.sh            # skip on your own machine; use your compiler/venv

cmake -S bindings -B bindings/build -G Ninja -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_AR=$(which zar) -DCMAKE_RANLIB=$(which zranlib) \
      -Dpybind11_DIR=$(python -c 'import pybind11;print(pybind11.get_cmake_dir())')
cmake --build bindings/build --target lqt_native -j1
```

On a normal toolchain drop the two `-DCMAKE_AR/-DCMAKE_RANLIB` flags (they point
CMake at zig's archiver). The build copies `lqt_native*.so` into `lqt_py/`.
x86-64 builds get the AVX2 flags for `lqt/src/simd.cpp` automatically; aarch64
uses NEON. Check it loads:

```sh
python -c "from cognition.lqt_bridge import get_backend; print(get_backend('native').L.LqtModel)"
```

## 2. Run the chat

From the repo root:

```sh
python -m runtime.chat --model runtime/runs/<run>/model.lqt            # interactive
python -m runtime.chat --model <path> --once "your sentence"           # one turn, save, exit
printf 'first line\nsecond line\n/state\n/quit\n' | python -m runtime.chat --model <path>
```

* The model file is created by genesis from the seeded stack if it does not exist.
* Model config (seed, hidden_dim, eta, ...) is read from `run.json` next to the model when present.
* Commands: `/state`, `/save`, `/rollback N` (undo the last N turns' logged edits), `/quit`.
* Flags: `--save-every N` (default 5; 0 = only on exit), `--mrc` (run the slow REST-phase
  MRC fixed point), `--iala-filter selfmod|THRESHOLD,PRIOR` (IALA ethical filter setting;
  default = neutral prior 1.0 and threshold 0.5; neutral technical content is admitted at reliability 0.8),
  `--json` (full per-turn record).
* Working files go to `<model dir>/chat/` (`transcript.jsonl`, `chat.log`, Bayesian state).

## 3. What a turn does

One step of `runtime.rosemary_full.RosemaryFullLoop` on your text: canon breath phase ->
cognitive engine (triaxial backbone, RTA, ethical / metacognitive / meta-reflective head)
-> SECT sentinel -> Bayesian update -> canon motivation (canon FBS tokenizer) -> IALA
`learn_from_text` + training cycle -> Psi self-modification -> RSL episodic memory ->
dream portal on DREAM phase. Acquired IALA representations feed the engine’s existing attention layer. The engine also executes its recursive weights against its existing thought-encoder row bank; evolved weights therefore affect subsequent computation. Then every changed stack tensor is written into the same
`model.lqt` as logged edits (`UnifiedModel.sync`), hash-chained and verifiable.

## 4. Where the reply text comes from

The repo has no native text generator, so none is faked. The engine's language head
returns fixed sentences picked by if/else, `SacredFBS_Tokenizer.decode` returns a tensor
description string, and `CrossModalHarmonicBridge.generate` only replays stored strings;
none of them is used. The reply is:

* **recall**: text the system stored earlier. IALA knowledge entities picked by IALA's
  `RTAAttention.select`, plus RSL episodic and dream memories fetched with `retrieve_memory`
  and ranked by canon FBS harmonic resonance. Some IALA entity texts are the engine's own
  meta-reflection notes, written by `MetaLearningBridge`;
* **dream**: memory text the canon dream engine integrates when a dream ends;
* **state**: cognitive mode, reflection scores, meta-reflection errors, the IALA filter
  verdict, contradiction severity, breath phase, and motivation drive.

## 5. What persists between sessions

* All float state is in `model.lqt` as tensors.
* The non-float identity of entities created at run time (evolution RecursiveWeights,
  IALA RWA weights and knowledge-entity text, canon motivation entities) and the RSL
  memory records are saved in the model's module graph as `unified.stack` JSON, so the
  next load can rebuild them.
* A stored tensor whose owner cannot be rebuilt stays in the file untouched ("dormant").
  It is listed in the banner and never detached.
* Not persisted: the breath oscillator (each session starts at INHALE), the canon
  motivation experience queues, and the RSL system's internal tensors (its records are
  re-stored on load).

## RSNN-3 repair and executable evidence (2026-11-21)

RSNN-3 is the system being repaired. Historical module/directory names are retained for import compatibility and lineage. The implementation has not been replaced.

The separate runtime archive contains `runtime/runs/rsnn3_release_seed1/model.lqt` and the recovered supplied checkpoint in `runtime/runs/rsnn3_recovered/model.lqt`. Extract it over this tree. Start the recovered model with:

```sh
python -m runtime.chat --model runtime/runs/rsnn3_recovered/model.lqt
```

To continue the native training loop on the release model (appends metrics):

```sh
python -m runtime.train --steps 14 --seed 1 --out runtime/runs/rsnn3_release_seed1 --overwrite
```

`--overwrite` permits reuse of the run directory; the existing model is resumed. `--json` now includes the actual per-turn learning and influence record. Native binary included for CPython 3.12/Linux x86-64; rebuild using the instructions above for another platform. CPU installation may use the PyTorch CPU wheel index to avoid installing CUDA libraries on CPU-only hosts.

Repair details and measured results are in `RSNN3_REPAIR_REPORT.md`. The unchanged language-generation head remains templated; the chat surface exposes recalled knowledge and computed state. No external LLM or fabricated generative capability was added.
