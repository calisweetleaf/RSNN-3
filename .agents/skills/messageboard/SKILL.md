---
name: messageboard
description: Coordination protocol for parallel agent lanes working this repo. Load before touching any file.
---
# Swarm message board

Board: `.agents/board/board.jsonl` (append-only). Tool: `python3 .agents/skills/messageboard/board.py`.

## Protocol
1. On arrival: `board.py read` (whole log) then `board.py claims`.
2. Before editing a path: `post --kind claim --topic <path-or-dir>`. Never edit a path another lane holds.
3. When you publish an interface others build on (a pybind module, a class signature, a CLI): `post --kind api --topic <name> --body "<exact import + signatures>"`.
4. Blocked: `post --kind blocker` with the exact error. Blocked twice on the same cause: stop, report.
5. Finished a unit: `post --kind done --body "<files, commands run, exit codes, test counts>"` then `release` your claims.
6. Re-read the board (`read --since <last seq>`) before each new unit of work.

## Doctrine (operator's, do not violate)
- Not a transformer. LQT = liquid quantized format; weights are storage (B, 5D T, Phi/epsilon buckets), tensors are compute (RTA blocks select lattice positions).
- C++ (lqt/, lqt/recursive-tensor-cpp/) replaces Python wherever an equivalent exists; Python originals in lqt/original-py-code stay as evidence.
- No mocks, stubs, placeholder integrations, simulated success. Unexecuted code is not "tested".
- Respect lqt/AGENTS.md, TASK.md, SCOPE.md hard bans (D-024 FormatError bounds stay unless a spec backs a replacement).

## Toolchain (persistent, survives sandbox resets)
`. /workspace/projects/05f88ba4-6369-4acb-9c1a-f3e868fbb4a0/forge/.toolchain/env.sh` (zig zcc/zcxx/zar/zranlib, cmake, ninja, pybind11, numpy, torch CPU, somnus-doctor; sets BIOC_STORAGE_PATH). Never install into ~/.local (wiped on reset).
Machine is aarch64, ~2 cores, 7 GB: no -mavx2; build one target at a time (`--target X -j2`), long builds as background shell jobs, never two heavy compiles + torch at once.
