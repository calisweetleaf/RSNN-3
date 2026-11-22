# LQT Library Changelog

All notable changes to the LQT reference implementation are documented here.
Format: Keep a Changelog. Versioning tracks the LQT binary format version it targets (v1.3).

## [Patch 4] — 2026-06-04 — Full RTA + Recursive Weights Reference Implementation

### Added
- `include/lqt/rta_ops.h` + `src/rta_ops.cpp` — `rta_contract()`, `rta_project()`, `rta_expand()`, `SparseTensor5D` (Odin).
- `include/lqt/rta_analysis.h` + `src/rta_analysis.cpp` — `rta_fractal_iterate()`, `rta_entropy()`, `rta_normalize()`, `rta_apply_function()`, `rta_density()`, `rta_find_fixed_point()` (Thor).
- `include/lqt/rw_compute.h` + `src/rw_compute.cpp` — full `rw_compute_effective_value()` with depth-limited recursion, `rw_converge()`, component computations (Loki).
- `include/lqt/rw_dynamics.h` + `src/rw_dynamics.cpp` — `DynamicalSystemsAnalyzer`: all 17 theorems from the specification (Freya).
- `include/lqt/rw_validation.h` + `src/rw_validation.cpp` — `ValidationEngine` 4-pass: configuration, convergence, stability, mathematical consistency (Tyr).
- `include/lqt/rw_evolution.h` + `src/rw_evolution.cpp` — `EvolutionEngine`, `PatternLibrary` with tournament selection + crossover + mutation (Heimdall).
- `include/lqt/rw_cache.h` + `src/rw_cache.cpp` — `TieredCacheManager` L1/L2 LRU, `PerformanceTracker` (Baldur).
- `RecursiveWeight::reconstruct()` upgraded to full depth-limited effective value formula (Skadi).
- `RecursiveWeight::convergence_value()` — iterates to fixed-point (Skadi).
- `tests/test_rta_ops.cpp` + `tests/test_rw_reference.cpp` — 28 new test cases (Njord).

### Reference source
- `recursive_tensor.py` (167KB) — RTA Python reference implementation
- `recursive_tensor_whitepaper.md` (102KB) — RTA theoretical specification
- `recursive_weights_core.py` (271KB) — RecursiveWeight Python reference
- `recursive_weights_technical_specs.md` (119KB) — RW technical specification
- `recursive-weights-comprehensive-reference.md` (47KB) — implementation guide

## [Patch 2] — 2026-06-04

### Added
- `LqtModel::edit_log()` — public getter for the in-memory edit log.
- `LqtModel::edit_codebook(id, index, value)` — atomic codebook entry mutation with validation and audit log.
- `LqtModel::update_delta(id, buffer)` — atomic delta buffer replacement with audit trail.
- `LqtModel::hot_swap_module(name, blob)` — module hot-swap with audit log entry.
- `LqtModel::add_rta_block(name, block)` / `get_rta_block(name)` — RTA block registry in the model.
- `LqtModel::reconstruct()` now routes `RecursiveTensor` descriptors through the RTA block path.
- `LqtModel::reconstruct()` now handles `codebook_id == LQT_ID_NONE` via affine dequantization fallback.
- `BigEndianByteReader` in `endian.h` — byte-swapping cursor for big-endian files.
- `make_reader()` factory in `endian.h` — returns the correct reader type based on file flags.
- `lqt/simd.h` — compile-time SIMD dispatch infrastructure (AVX2/NEON/scalar fallback).
- `lqt/converters.h` + `src/converters.cpp` — `from_gguf()` and `from_onnx()` conversion stubs.
- New test files: `test_model_mutations.cpp`, `test_integration_roundtrip.cpp`.

### Fixed
- EditLog is now persisted in `LqtModel::save()` as a `0x000B` TLV chunk and restored on `load()`.
- Affine-only tensors no longer throw when `codebook_id` is absent; they use `dequant_affine()`.

### Known remaining gaps
- Big-endian write path not implemented (files are always written little-endian).
- GGUF/ONNX converters produce skeleton LqtModel with zero-filled tensor blobs.
- SIMD fast paths are stubs requiring platform-specific intrinsic implementation.
- `LqtModel::save()` does not yet emit the edit log offset into the footer's `edit_log_offset` field.

## [Unreleased]
### Added
- Repository skeleton, CMake build scaffold, toolchain bring-up (GCC 11.5.0 / CMake 3.22.2 / C++17).
- Specification absorption pass over canonical lqt.md (§2 binary layout) and v1.3 binary spec.
- Binary-contract decision log and spec-contradiction register (see SPEC_COMPLIANCE.md).
- A1 container: 36-byte header, 64-byte footer, CRC-32 (zlib) + CRC-64 (XZ), little-endian
  ByteReader/ByteWriter, fp16<->fp32. Verified against published CRC check vectors.
- A2 TLV metadata system + chunk registry with forward-compatible unknown-type skipping,
  codebook/delta/mask tables, hyperparameters, JSON-bearing chunks.
- A3 tensor descriptors, FP16 vector-quantization codebooks (scalar/vector/hierarchical/
  expandable), INT4/INT8/INT16/INT32 index unpacking, multi-stage reconstruction.
- A4 delta buffers (FP16/FP32, dense + sparse) and sparse masks (bitmap + RLE).
- A5 Recursive Tensor Architecture: rank-5 blocks, all six sparse encodings, reference
  block (Direct/Transformed/Fractal), per-block CRC-64.
- A6 recursive weights {B, Phi, R, T, epsilon} with harmonic phase and reconstruction.
- A7 append-only tamper-evident edit log, 4-constraint mutation validator, atomic
  transactions with rollback.
- A8 reader-preference reader-writer lock, lock-free DoubleBuffer hot-swap, POSIX mmap.
- A10 LqtModel: full .lqt container assembly + parse, whole-file CRC32 verification,
  reconstruction by tensor name, save()/load().
- Test suite: 9 ctest suites, 119 cases, zero warnings under -Wall -Wextra -Wpedantic.
- Usage examples: write_lqt, load_reconstruct, mutate_lqt.
