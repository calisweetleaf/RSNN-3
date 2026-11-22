# Operator notepad

## 2026-09-20 — Initial archive reconstruction and harness pass

- **Base state:** extracted `lqt_COMPLETE_20260604_2040.zip`; no Git metadata
  was included.
- **Work landed:** added repository-specific arrival routing, scope, continuity
  state, semantic topology, and a reproducible gate entrypoint.
- **Validation:** all library and test translation units compile with GCC 13.3;
  230 cases pass across 20 completed binaries; `test_concurrency` deadlocks in
  `rwlock_stress`; CMake is unavailable.
- **Evidence correction:** inherited reports claim 119 passing cases and broad
  completion. Current source inventory contains 230 test cases. The inherited
  claim is retained as history, not accepted as current proof.
- **Unverified:** canonical LQT/RTA whitepapers are absent from the archive.
- **Next action:** repair and regression-test the concurrency deadlock, then run
  a clause-level LQT/RTA whitepaper reconciliation before promoting any
  completeness claim.
- **Hazard:** the `RecursiveTensor` model reconstruction branch is explicitly a
  dimension-envelope placeholder and must not be described as mathematically
  complete.

## 2026-09-20 — Surgeon repair of concurrency gate

- **Surgeon action:** changed only the reader-drain wakeup in
  `include/lqt/concurrency.h` from `writer_cv_.notify_one()` to
  `writer_cv_.notify_all()`. Multiple writers could otherwise consume the
  notification intended for the writer waiting on the final reader.
- **Targeted validation:** five consecutive `test_concurrency` runs passed all
  7 cases, including `rwlock_stress`.
- **Full validation:** the direct GCC fallback gate passed 21/21 binaries and
  237/237 registered cases. CMake/CTest remains unrun because CMake is absent.
- **Remaining:** canonical whitepapers are still absent, and the
  `RecursiveTensor` model path remains a dimension-envelope placeholder.
- **Next action:** add the supplied authorities and produce a clause-level
  LQT/RTA matrix before making any broader completeness claim.

## 2026-09-20 — Authority intake and first clause matrix

- **Authority intake:** imported the June 4 briefing, v1.3 binary format
  specification, and adaptive LQT transition document into `docs/authority/`.
- **Matrix:** added `docs/LQT_AUTHORITY_MATRIX.md`, separating implemented
  container/RTA storage surfaces from partial model reconstruction and
  unverified performance/security claims.
- **Next packet:** materialize the tested Python LQT/RTA/RWA reference, then
  build byte-level and numerical cross-language fixtures before changing the
  `RecursiveTensor` model path.

## 2026-11-21 — zig/aarch64 CMake+CTest gate (lane lqt-bindings)

- **Toolchain:** zig 0.x clang 22 (`zcc`/`zcxx`), CMake 4.4.5, Ninja; aarch64
  Neoverse V2 VM with SVE hidden. Default `-mcpu=native` emitted SVE and every
  test died SIGILL (19/21 ILLEGAL). Configure with `-DCMAKE_CXX_FLAGS=-mcpu=baseline`.
- **Command:** `cmake -S lqt -B lqt/build/zig -G Ninja -DCMAKE_BUILD_TYPE=Release
  -DCMAKE_AR=$(which zar) -DCMAKE_RANLIB=$(which zranlib) -DCMAKE_CXX_FLAGS=-mcpu=baseline`
  then `cmake --build lqt/build/zig -j2` and `ctest` (exit 8: one suite fails).
- **Baseline before edits:** 20/21 suites pass; `test_simd_avx2` 3/9 cases fail.
- **Repairs:** `ByteReader` gets a virtual destructor (make_reader returns
  `unique_ptr<ByteReader>` owning a `BigEndianByteReader`; clang flagged 42
  delete-non-virtual-dtor sites, now 0 warnings). Added `pack_indices`
  (inverse of `unpack_indices`) + `tests/test_pack_indices.cpp` (6 cases).
- **After:** 21/22 suites, 246/249 cases pass.
- **test_simd_avx2 root cause (not a SIMD bug):** NEON and scalar paths agree
  with each other and with `dequant_affine` (`(q - zero_point) * scale`). The
  test asserts `q * scale + zero_point`, which is the formula D-015 attributes
  to canon §3.1. The three failing cases are exactly the ones with
  `zero_point != 0`. This is an affine-convention contradiction between the
  implementation and the D-015 canon citation; it needs an operator/canon
  ruling, so neither side was changed.
- **Writer/reader symmetry (same day):** `LqtModel::serialize_to_bytes` now
  runs `TensorDescriptor::validate()` on every tensor. Found through the
  Python round trip: a rank-3 `RecursiveTensor` descriptor saved without
  error and `LqtModel::load` then rejected the file. Low-level
  `TensorDescriptor::serialize` is left unvalidated because
  `test_descriptor_codebook` crafts rejected bytes through it. Regression:
  `tests/test_descriptor_symmetry.cpp` (2 cases). Gate now 22/23 suites,
  248/251 cases. Only `test_simd_avx2` still fails (affine ruling above).
- **Bindings:** `bindings/` builds pybind11 `lqt_native` from these sources
  (PIC static `lqt_pic` + header-only rta). `python bindings/roundtrip_demo.py`
  prints ROUNDTRIP OK.
