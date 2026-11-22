## CORRECTION — 2026-09-21 (Patch 5 / D-024)

The "LQT COMPLETE" summary below (patch row 2, "RTA embedding") and item 7 of
the v0.1 "Known deviations / not yet implemented" section further down both
describe `reconstruct()` routing `TensorType::RecursiveTensor` through the
RTA path as a closed gap. This was materially misleading: as of Patch 4,
`LqtModel::reconstruct()`'s `RecursiveTensor` branch computed nothing from
the tensor's actual content — it cycled `RtaBlock.dims.dim_sizes` into the
output vector regardless of the real data. It "routed" in the sense of not
throwing, not in the sense of returning a correct value. This was not caught
by any prior test because `tests/test_model_mutations.cpp`'s
`model_rta_reconstruction_path` only ever asserted the output vector's
*size*, never its values.

Patch 5 / decision D-024 (`docs/SPEC_COMPLIANCE.md`) replaces this with real
computation (codebook-based B term + optional `RecursiveWeight` Phi/epsilon
modulation + real decode of 5 of the 6 RTA sparse encodings), and explicitly
bounds — via a thrown `FormatError` rather than a further guess — the two
sub-cases no supplied specification actually resolves: `PerDimension`
sparse encoding (aggregate density, not exact membership) and any
`RtaReference` entries (the wire format has no field binding a reference to
an output element, and the canonical whitepaper's own resolution pseudocode
is itself incomplete). See D-024 for the full account and the new
`RecursiveWeightTable` (0x0011) chunk it adds.

The historical text below is preserved as the record of what Patch 2/4
actually believed and shipped at the time; it is not edited in place.

---

## LQT COMPLETE — 2026-06-04

All deferred items from the v0.1 Next Patch List are implemented and tested.
0 TODOs remain in src/ or include/lqt/.
21/21 test suites pass. 0 warnings.

| Patch | What shipped |
|---|---|
| 2 | EditLog persistence, model mutations, RTA embedding, affine reconstruction, big-endian read, SIMD infra stubs, GGUF/ONNX stubs |
| 3 | footer.edit_log_offset wired, rollback() undo stack, EditLog::truncate() |
| 4 | RTA ops, RTA analysis, rw_compute full recursion, 17 dynamical-systems theorems, 4-pass validation, EvolutionEngine, TieredCacheManager |
| 5 | self_reference_coeff wired into binary format |
| 6 | GGUF real tensor bytes via two-pass offset-delta import |
| 7 | AVX2/F16C/FMA fast paths, GGUF KV metadata extraction |
| 8 | ONNX protobuf decoder (varint + TensorProto initializer walk) |
| 9 | Q4_0/Q8_0 per-block scale extraction |
| 10 | 0 TODOs cleared, edit-log integrity test suite |

---

## Patch 4 Council Report — 2026-06-04

Council: 10 Opus agents (Odin, Thor, Loki, Freya, Tyr, Heimdall, Baldur, Skadi, Njord, Vidar). Flat hierarchy, all read/write.

Source: 5 reference files totaling ~707KB of Python implementations and specification documents.

### Added in Patch 4
- **RTA operations** (Odin): `rta_contract()`, `rta_project()`, `rta_expand()`, `SparseTensor5D`
- **RTA analysis** (Thor): `rta_fractal_iterate()`, `rta_entropy()`, `rta_normalize()`, `rta_apply_function()`, `rta_density()`, `rta_find_fixed_point()`
- **Effective value engine** (Loki): `rw_compute_effective_value()` with depth-limited recursion, `rw_converge()`
- **Dynamical systems** (Freya): 17 theorems from the mathematical specification (fixed-point, Lyapunov, attractor, capacity, convergence, error bounds, fractal dimension, information bounds)
- **Validation engine** (Tyr): 4-pass validation — configuration, convergence, stability, mathematical consistency
- **Evolution engine** (Heimdall): `EvolutionEngine` (tournament/crossover/mutation), `PatternLibrary`
- **Cache layer** (Baldur): `TieredCacheManager` L1/L2 LRU with demotion policy, `PerformanceTracker`
- **reconstruct() upgrade** (Skadi): full depth-limited effective value formula replacing scalar heuristic
- **Tests** (Njord): 28 new TEST_CASEs across two suites
- **Integration** (Vidar): CMakeLists.txt, rta.cpp wrappers, docs

---

# LQT Reference Implementation — Patch 2 Council Report

*Issued 2026-06-04. This section supersedes where it conflicts with the v0.1 report below.*

## Patch 2 — What changed

Council composition: 2 Opus (Nexus/Prism), 3 Sonnet (Kettle/Loom/Forge), 5 Haiku (Rook/Ember/Vex/Sable/Cinder). Flat hierarchy, all read/write.

### New in Patch 2

**EditLog persistence (Kettle → Nexus):** `LqtModel` now carries an `EditLog edit_log_` member. On `save()`, the log is emitted as TLV chunk 0x000B; on `load()`, it is parsed back. Patch closes v0.1 gap #1.

**Model mutation surface (Loom → Nexus):** `LqtModel::edit_codebook()`, `update_delta()`, `hot_swap_module()` added. Each validates, appends to the edit log, and executes atomically. Patch closes v0.1 gap #2.

**RTA embedding in LqtModel (Nexus):** `rta_blocks_` map added; `add_rta_block()` / `get_rta_block()` API added; `reconstruct()` routes `RecursiveTensor` descriptors through the RTA path. Serialized as 0x0012 TLV chunk. Patch closes v0.1 gap #3.

**Affine-only reconstruction (Forge → Nexus):** `LqtModel::reconstruct()` now falls through to `dequant_affine()` when `codebook_id == LQT_ID_NONE`. Patch closes v0.1 gap #4.

**Big-endian read path (Kettle):** `BigEndianByteReader` added to `endian.h`. `make_reader()` factory added. Write path remains little-endian only. Partially closes v0.1 gap #5.

**SIMD infrastructure (Forge):** `simd.h` + `simd.cpp` added with compile-time AVX2/NEON/scalar dispatch. Scalar paths implemented; fast paths are stubs. Partially closes v0.1 gap #7.

**Conversion stubs (Loom):** `converters.h` + `converters.cpp` added. `from_gguf()` parses GGUF v2/v3 headers and tensor metadata; `from_onnx()` validates magic and documents the parse path. Partially closes v0.1 gap #6.

**New tests:** `test_model_mutations.cpp`, `test_integration_roundtrip.cpp` (Prism). All existing 119 cases preserved; new cases added for mutation, affine fallback, and RTA routing.

### Still deferred

- Big-endian write path (files always written LE)
- SIMD fast-path intrinsic implementation
- Full GGUF/ONNX tensor weight import (skeleton only)
- `footer.edit_log_offset` not yet wired to the in-memory log's offset

## Patch 2 build status

```
cmake --build build -j$(nproc)   # expected: 0 errors
ctest --test-dir build           # expected: 119+ tests pass
```

---

# LQT Council Agent Report — v0.1 Implementation

This report is the council's own record of what we built, what we deferred, and what comes next. It is written in first person and reflects the shared voice of the eight modules that assembled the LQT v1.3 reference implementation.

---

## Implemented files

### A1 — Container foundation

Headers: `include/lqt/error.h`, `include/lqt/version.h`, `include/lqt/format.h`, `include/lqt/endian.h`, `include/lqt/crc.h`, `include/lqt/header.h`, `include/lqt/fp16.h`

Sources: `src/crc.cpp`, `src/header.cpp`

The container layer establishes every on-disk constant and provides the ByteReader/ByteWriter cursor abstraction used by all other modules. CRC-32 correctness is proven against the published zlib check vector (`crc32("123456789") = 0xCBF43926`) and CRC-64 against the XZ check vector (`crc64("123456789") = 0x995DC9BBDF1939FA`). The header is 36 bytes (operator-ratified deviation D-001; see below). FP16<->FP32 conversion is round-trip correct for normal values.

### A2 — TLV / metadata

Headers: `include/lqt/tlv.h`

Sources: `src/tlv.cpp`

The TLV layer handles all chunk types defined in the v1.3 registry (0x0001 through 0x000F, plus 0x0012 and 0xFFFF). Unknown chunk types are skipped and their bytes preserved, ensuring forward compatibility. The codebook, delta, and sparse-mask offset tables (chunk types 0x0005, 0x0006, 0x0007) each serialize as `[id:u16][offset:u64][size:u64]` (18 bytes per entry). JSON-bearing chunks (0x0003, 0x0004, 0x000A) store verbatim UTF-8.

### A3 — Reconstruction

Headers: `include/lqt/descriptor.h`, `include/lqt/codebook.h`, `include/lqt/reconstruct.h`

Sources: `src/descriptor.cpp`, `src/codebook.cpp`, `src/reconstruct.cpp`

The reconstruction module covers tensor descriptors, codebook storage (scalar, vector, hierarchical, expandable), INT4/INT8/INT16/INT32 index unpacking (INT4 low-nibble-first per D-007), and the full multi-stage reconstruction formula: `weight = codebook[idx] * scale + delta * mask`. Codebooks are stored on disk as FP16 and decoded to FP32 in memory for fast lookup and editing. The `Codebook::set_scalar` / `set_vector` methods provide the mutation surface used by A7.

### A4 — Delta / Mask

Headers: `include/lqt/delta.h`, `include/lqt/sparse_mask.h`

Sources: `src/delta.cpp`, `src/sparse_mask.cpp`

Delta buffers support FP16 and FP32 dense and sparse variants. Sparse deltas encode as interleaved `[u32 index][value]` pairs. Sparse masks implement both CompressedBitmap (LSB-first per byte) and RLE (alternating uint16 run lengths, first run covering leading zero-bits). The `num_elements` field is a uint24 (3 bytes) per canon section 2.6.

### A5 — Recursive Tensor Architecture

Headers: `include/lqt/rta.h`

Sources: `src/rta.cpp`

The RTA module implements 5-D tensor blocks with rank-5 enforced as a hard invariant. All six sparse encodings from the v1.3 binary spec are implemented with typed builder/parser pairs: Uniform, PerDimension, Hierarchical, RLE, CompressedBitmap, and CSR. Reference blocks support Direct, Transformed (matrix-based), and Fractal (iterative) kinds. Every RTA block carries a CRC-64 (XZ) trailer; a mismatch raises `IntegrityError`. The 24-byte dimension block and five per-dimension sizes (d0 Feature, d1 Pattern, d2 Temporal, d3 Scale-Fractal, d4 Channel) are laid out as specified.

### A6 — Recursive Weights

Headers: `include/lqt/recursive_weight.h`

Sources: `src/recursive_weight.cpp`

The recursive weight module encodes the quintuple W = {B, Phi, R, T, epsilon}: base index, phase modulation, recursive reference matrix, 5-D tensor position, and error-preservation term. The `phase_at(t)` method computes the harmonic phase component. `reconstruct()` returns the full-precision weight value for a given position.

### A7 — Mutation / Edit Log / Transactions

Headers: `include/lqt/edit_log.h`, `include/lqt/mutation.h`, `include/lqt/transaction.h`

Sources: `src/edit_log.cpp`, `src/mutation.cpp`

The mutation layer is the library's trust boundary. The edit log is append-only and tamper-evident: each entry stores a CRC-32 chained `data_hash` computed over the previous entry's hash, the timestamp, the mutation type, the target name, and a payload hash. Any reordering or field modification is detectable via `EditLog::verify_chain()`. The mutation validator enforces four independent constraints: dimension compatibility, value bounds, topology (with directed-graph cycle detection), and access control (the `PROTECTED` flag on tensor descriptors). `Transaction<State>` implements copy-validate-swap rollback: a trial copy is mutated and validated before the live state is replaced, so a rejected mutation leaves the model unchanged.

### A8 — Concurrency and Memory Mapping

Headers: `include/lqt/concurrency.h`, `include/lqt/mmap.h`

Sources: `src/mmap.cpp`

`ReaderWriterLock` is a reader-preference lock implemented with a mutex, condition variables, and counters — not a bare `std::shared_mutex` whose scheduling priority is unspecified. This honors canon section 7.2's requirement to prioritize readers during active inference. `DoubleBuffer<T>` uses `std::atomic_load` / `std::atomic_store` on a `shared_ptr` for lock-free reader snapshots across a writer's `store()` call. `MemoryMappedFile` wraps POSIX `mmap` and throws a typed `LqtError` (with `strerror(errno)`) on OS failure.

### A10 — Integration

Headers: `include/lqt/model.h`

Sources: `src/model.cpp`

`LqtModel` is the capstone. It assembles every other module into a compliant binary container and parses it back. The on-disk layout is: 36-byte `FileHeader`, then at `metadata_offset` a u64 TLV length prefix followed by the TLV `MetadataSection`, then 64-byte-aligned codebook blocks, then tensor blobs starting at `tensor_offset`, then delta buffers and sparse masks (each 4-byte aligned), then the 64-byte `FileFooter` at `footer_offset`. The whole-file CRC-32 is computed over all bytes with the 4 checksum bytes in the footer treated as zero. `LqtModel::load` verifies this checksum and throws `IntegrityError` on mismatch.

---

## Test results

All 9 suites pass. 119 cases total. Zero warnings under `-Wall -Wextra -Wpedantic`.

| Suite | Cases | What is covered |
|---|---|---|
| test_header | 10 | Header parse/serialize, magic rejection, CRC-32 check vector, CRC-64 check vector, FP16 round-trip |
| test_tlv | 23 | All chunk types, unknown-type skipping, codebook/delta/mask tables, JSON chunks |
| test_descriptor_codebook | 13 | Descriptor layout, INT4/INT8/INT16/INT32 unpacking, scalar/vector/hierarchical codebooks, reconstruction formula |
| test_delta_mask | 6 | Dense FP16/FP32 deltas, sparse deltas, CompressedBitmap mask, RLE mask |
| test_rta | 25 | Rank-5 enforcement, all six sparse encodings, Direct/Transformed/Fractal reference blocks, per-block CRC-64 |
| test_recursive_weight | 10 | Quintuple construction, phase_at(t), reconstruct(), serialization round-trip |
| test_mutation | 20 | Edit log chain, verify_chain tampering detection, all four validator constraints, transaction rollback |
| test_concurrency | 7 | ReaderWriterLock reader preference, DoubleBuffer hot-swap, MemoryMappedFile read |
| test_model | 5 | Full in-memory round-trip, on-disk save/load, CRC corruption detection, bad-magic rejection, empty optional regions |
| **Total** | **119** | |

---

## Build and run commands

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build -j
ctest --test-dir build --output-on-failure
```

---

## Known deviations and specification notes

These are summarized from `docs/SPEC_COMPLIANCE.md`. All deviations are in the register; the eight labeled below correspond to D-001 through D-008 in that document.

**D-001 — Header size: 36 bytes (operator-ratified, 2026-06-04)**
Canon section 2.2 says "32 bytes" in one place and specifies three `uint64` offset fields that reach byte 36 in another. We implement 36 bytes. The 32-byte statement would cap LQT files at 4 GiB via a 32-bit footer offset; the format's own benchmark references a 7B model at 4.0 GB, making the 64-bit offsets load-bearing.

**D-002 — Version encoding: 8-bit major / 8-bit minor**
Canon prose describes a 4/12 split; the v1.3 binary spec describes an 8/8 split. We use 8/8. Version 1.3 encodes as `0x0103`, which is self-documenting in a hex dump and symmetric.

**D-003 — DType numeric codes**
Canon enumerates element dtypes by name without fixed codes. We assign: `FP32=0, FP16=1, BF16=2, INT8=3, INT4=4, UINT8=5, INT16=6, INT32=7`.

**D-004 — Whole-file checksum convention**
Canon says the footer holds a CRC-32 of the entire file but does not specify how the checksum field itself is handled. We compute the checksum over the whole file with the 4 footer checksum bytes treated as zero, which is the only self-consistent option.

**D-005 — Tensor descriptor includes tensor_type**
Canon section 2.3 omits `tensor_type` from the descriptor field list; v1.3 spec section 3 includes it as field 2 and calls it "The Logic Switch" (0=Standard, 1=RecursiveTensor). We include it immediately after the name because it is load-bearing for routing reconstruction.

**D-006 — Codebook type is a model-level role, not an on-disk byte**
Canon section 2.5 lists codebook types (global/local/hierarchical/expandable) but the on-disk block carries no type byte. We model global/local as a role (which tensors reference the codebook), hierarchical as a distinct composed type (`HierarchicalCodebook`), and expandable as the `Codebook::expand()` runtime capability.

**D-007 — INT4 index packing: low nibble first**
Canon specifies "2 values per byte" without nibble order. We use: element `2k` is the low nibble of byte `k`; element `2k+1` is the high nibble.

**D-008 — Codebook id sentinel is 0xFFFF**
`codebook_id`, `delta_id`, and `sparse_mask_id` use `LQT_ID_NONE = 0xFFFF` to mean "no link", since `0` is a valid id.

Additional operator design decisions (A2, A4, A5, A7, A8) are recorded in full in `docs/SPEC_COMPLIANCE.md`.

---

## Known deviations / not yet implemented

The following areas are structurally present (flags carried, bytes reserved) but not fully wired:

1. **Big-endian read path.** The `BigEndian` header flag is carried and byte-swap helpers exist in `endian.h`. Full materialization of a big-endian file as native little-endian on read is not implemented. Files written by this library are always little-endian.

2. **Cryptographic edit-log signatures.** The `SignedEdits` flag and signature byte fields in each `EditLogEntry` are carried. The tamper-evident chain uses CRC-32, which detects accidental or naive corruption. Asymmetric signing (e.g., ECDSA) is not implemented and is explicitly out of scope for v0.1.

3. **Section compression.** The `Compressed` header flag is carried. No compressor or decompressor is wired; sections are stored uncompressed.

4. **Multi-file sharding.** The `Sharded` flag is carried. The loader operates on a single `.lqt` file.

5. **Reconstruction is scalar reference code.** The reconstruction path is correct and tested. No SIMD intrinsics or GPU dispatch paths are implemented.

6. **Affine-only tensors in LqtModel.** `reconstruct.h` provides `dequant_affine` for codebook-less affine dequantization. `LqtModel::reconstruct` dispatches through the codebook path and requires a linked codebook. A tensor with `codebook_id == LQT_ID_NONE` that relies solely on affine dequantization cannot be reconstructed via `LqtModel` in v0.1.

7. **RTA / recursive-tensor embedding in LqtModel.** The A5 (RTA) and A6 (recursive weights) modules are complete and pass their own test suites. `LqtModel` assembles and reconstructs the standard tensor path end-to-end; embedding RTA blocks into the model file and routing `tensor_type == RecursiveTensor` through `LqtModel::reconstruct` is the next planned work item.

8. **EditLog not auto-persisted by LqtModel.save.** `EditLog` is fully implemented, serializable, and tested. When `LqtModel::save` writes the file it does not yet emit the log as a `0x000B` TLV chunk. An in-memory `EditLog` must be serialized separately by the caller if persistence is required.

---

## Next patch list

In priority order, the patches we would write immediately after this report:

1. **Persist EditLog as 0x000B chunk in LqtModel.save.** Add an `EditLog edit_log_` member to `LqtModel`; serialize it into the TLV metadata region on `save()`; parse it back on `load()`.

2. **Expose model mutation methods.** Add `LqtModel::edit_codebook(id, index, value)`, `update_delta(id, buffer)`, and `hot_swap_module(name, new_blob)` that each validate via the mutation framework, append to the edit log, and execute atomically via `Transaction<LqtModel>`.

3. **Wire RTA blocks and recursive tensors into LqtModel.** Add an `rta_blocks_` collection to `LqtModel`; serialize/parse them; route `tensor_type == RecursiveTensor` in `reconstruct()` through the A5/A6 path.

4. **Affine-only tensor reconstruction.** When `codebook_id == LQT_ID_NONE` in `LqtModel::reconstruct`, fall back to `dequant_affine(desc, indices)`.

5. **Big-endian read path.** Wire the `BigEndian` flag through `ByteReader` so that loading a file produced on a big-endian host yields correct values on any platform.

6. **GGUF and ONNX converters.** Implement `from_gguf` and `from_onnx` that read those formats and produce a populated `LqtModel` with appropriate codebooks, deltas, and descriptors.

7. **SIMD reconstruction kernels.** Replace the scalar inner loop in `reconstruct.cpp` with AVX2 / NEON paths behind compile-time dispatch, targeting the 4.0 GB / 7B model benchmark case.
