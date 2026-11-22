# LQT repository audit — 2026-09-20

## Result

The archive is a substantial C++ reference implementation and is now a usable
single-agent repository with a terminating local gate. It is not complete as a
truthful specification-level implementation handoff: the imported authorities
are now being checked against the source, one RTA model path remains explicitly
partial, and the tested Python reference is not yet in this checkout.

## Inventory

| Surface | Observed |
| --- | ---: |
| Public headers | 30 |
| C++ source translation units | 23 |
| Test translation units | 21 |
| Examples | 3 |
| Registered test cases in source | 237 |
| CMake present | Yes |
| Git metadata present in archive | No |
| Canonical LQT/RTA documents present | Yes, under `docs/authority/` |

## Executable evidence

GCC 13.3 compiled every library and test translation unit with
`-Wall -Wextra -Wpedantic`. All 21 test binaries completed with 237 passing
cases. Five consecutive targeted `test_concurrency` runs also passed all seven
cases. The full direct-GCC fallback gate is **passed**. CMake/CTest was not run
because CMake is not installed in the environment.

## Implementation classification

### Substantially implemented and locally exercised

- LQT container header/footer, CRCs, byte readers/writers, and TLV metadata.
- Standard tensor descriptors, codebooks, index unpacking, deltas, masks, and
  reconstruction.
- Edit-log chaining, persistence tests, mutation APIs, and rollback tests.
- RTA block structure, sparse encodings, references, and CRC-protected
  serialization.
- Recursive-weight serialization and the local analysis/validation/cache test
  surfaces.
- GGUF/ONNX fixture ingestion paths exercised by the included tests.

“Substantially implemented” means the local code path exists and the included
tests exercise it. It is not a whitepaper equivalence claim.

### Partial or explicitly unresolved

- `ReaderWriterLock` now passes its local stress gate after a
  `notify_one()`-to-`notify_all()` lost-wakeup repair; fairness and intended
  reader-preference semantics still need comparison against the canonical
  authority when supplied.
- `LqtModel::reconstruct()` for `RecursiveTensor` returns a dimension-envelope
  vector, and the source comment calls this a placeholder. This is not full
  RTA model reconstruction.
- Big-endian support is primarily a read-side path; writer portability remains
  bounded.
- Converter support is fixture-driven and must not be generalized beyond the
  tested GGUF/ONNX subset.
- SIMD claims require generated-code or benchmark evidence in addition to
  compile-time dispatch.
- The historical report's 119-case count is stale relative to the current
  source tree and current runtime result.

### Not verifiable in this snapshot

- Numerical equivalence to the tested Python LQT/RTA/RWA reference.
- Full equivalence to the imported authority claims; see
  `docs/LQT_AUTHORITY_MATRIX.md`.
- Completeness of any Python reference implementation claimed by the reports.
- Release readiness on a CMake/CTest host.

## First-agent order

1. Materialize the tested Python LQT/RTA/RWA reference and complete the
   clause-level source/test matrix.
2. Replace or formally constrain the RecursiveTensor placeholder path.
3. Reclassify converters, SIMD, endianness, and remaining deviations against
   the actual release boundary.
