# Current repository context

**Snapshot:** `lqt_COMPLETE_20260604_2040.zip`
**Working state:** harnessed for a single-agent implementation pass
**State date:** 2026-09-21

## What is physically present

- C++17 library with 30 public headers and 23 source translation units.
- 21 test translation units and 3 examples.
- CMake configuration, but no vendored build toolchain.
- Historical implementation reports and a deviation register.
- The canonical briefing, v1.3 binary specification, and adaptive-systems
  transition document are now imported under `docs/authority/` from the
  persistent source artifacts. The tested Python reference is still not in
  this checkout.

## Verification performed

- GCC 13.3 compiled all 23 library translation units with
  `-Wall -Wextra -Wpedantic`.
- GCC linked all 21 test binaries successfully.
- All 21 test binaries completed successfully: 237 individual cases passed.
- The first gate exposed a lost-wakeup deadlock in `rwlock_stress`. Surgeon
  changed the reader-drain notification from `notify_one()` to `notify_all()`;
  five targeted runs and the full gate now terminate successfully.
- CMake/CTest validation was **not run** because `cmake` was absent in the
  environment as of 2026-09-20. As of 2026-09-21, `cmake` is present in the
  current environment; `scripts/gate.sh` now runs the CMake/CTest path.
  20/21 test suites pass via CTest; `test_simd_avx2` fails 3 of 9 cases
  (`simd_dequant_int8_scalar_agreement_64`,
  `simd_dequant_int8_non_multiple_of_8`,
  `simd_dequant_int4_non_multiple_of_16`) — pre-existing, in the
  uncommitted `src/simd.cpp` / `include/lqt/simd.h` / `include/lqt/endian.h`
  working-tree changes present before the D-024 patch below; not touched or
  caused by this patch, and not yet root-caused.

## Current implementation reading

- Container, TLV, reconstruction, delta/mask, edit log, mutation, converter,
  RTA structure, recursive-weight, analysis, validation, evolution, cache, and
  model round-trip surfaces are materially present.
- The RTA standalone surface is not enough to establish complete RTA semantics.
- `LqtModel::reconstruct()`'s `RecursiveTensor` branch (D-024, 2026-09-21) now
  computes a real value, on the doctrine fixed by `docs/TRIAXIAL_ARCHITECTURE.md`
  §3: weights are storage buckets, tensors are compute engines. Positions
  with no attached `RecursiveWeight` bucket use the tensor's own codebook
  index (structural base, real decode of 5 of 6 RTA sparse encodings:
  `Uniform`, `Hierarchical`, `RLE`, `CompressedBitmap`, `CsrCscCsf`).
  Positions with an attached bucket are fully overridden by that bucket's
  own B/Phi/epsilon (its own codebook index, not the tensor's shared one),
  placed by flattening its `tensor_position` (T) against the RTA block's
  dims. Two sub-cases remain explicitly bounded (thrown `FormatError`, not
  a guess): `PerDimension` sparse encoding (aggregate density only, no
  exact membership rule in any supplied source) and any `RtaReference`
  entries (the wire format has no field binding a reference to an output
  element; the canonical whitepaper's own resolution pseudocode is itself
  incomplete — see D-024 in `docs/SPEC_COMPLIANCE.md`).
- `src/simd.cpp` still documents scalar implementations with architecture paths
  that must be checked against the actual generated code and benchmark evidence.
- Historical docs disagree with the current source tree: they report 119 cases
  and broad completion, while the source contains 237 registered tests. The
  initial clause matrix is now in `docs/LQT_AUTHORITY_MATRIX.md`.

## Blockers

1. Materialize the tested Python reference and complete clause-level
   implementation reconciliation.
2. Obtain or design a real resolution specification for `RtaReference`
   (Direct/Transformed/Fractal) and for turning `PerDimension` density into
   exact element membership; both are currently intentional, tested,
   thrown-error bounds (D-024), not implementations.
3. Root-cause the 3 failing `test_simd_avx2` cases surfaced now that CTest
   runs (pre-existing in the working tree, unrelated to D-024).
4. Decide whether converter and remaining SIMD limitations are acceptable
   for the next LQT release or must be promoted to implementation packets.
