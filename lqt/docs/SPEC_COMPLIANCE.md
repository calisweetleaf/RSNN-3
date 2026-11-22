# LQT Reference Implementation — Specification Compliance & Deviation Register

This document records how the implementation maps to the canonical specification,
every place the source documents were ambiguous or self-contradictory, and the
resolution applied. It is the authoritative log of "known deviations" required by
the LQT Constitutional Prompt.

## Source authority order

1. `lqt.md` — canonical specification (binding).
2. `LQT Binary File Format Specification (v1.3)` — low-level binary contract.
3. `Liquid Quantized Format (LQT) ... Briefing` — architecture briefing.
4. `Transitioning to Adaptive LQT Systems` — integration/roadmap context.
5. Constitutional Prompt Framework — council governance.
6. `lqf_binary_read-writer_implement.cpp` — archaeological only (mined for intent;
   NOT a layout source — it uses an incompatible header and is explicitly drifted).

Conflicts are resolved in this order. Where canon contradicts **itself**, the
contradiction is surfaced to the operator (architect) and resolved by ruling +
engineering merit; those carry an operator-ratified note.

---

## Deviation register

### D-001 — Header size: 36 bytes (operator-ratified)
Canon §2.2 labels the header "32 bytes" / "Header Size: Always 32", yet specifies
three `uint64` offsets at 0x0C / 0x14 / 0x1C, which run to byte 36. The two
statements cannot both hold. **Resolution (operator ruling 2026-06-04): 36-byte
header, all three offsets `uint64`.** Rationale: `uint64` offsets are stated in
both canon and the v1.3 spec; a `uint32` footer offset would cap LQT files at
4 GiB, but the format's own benchmark cites a 7B model at 4.0 GB, so >4 GiB is a
real production case. `LQT_HEADER_SIZE = 36`; the `header_size` field stores 36.

### D-002 — Version encoding: 8-bit major / 8-bit minor → 0x0103 (operator-ratified)
Canon §2.2 prose says "Major (4 bits) + Minor (12 bits)" (→ 0x1003); the v1.3 spec
says "(1<<8)|3" = 0x0103 (8+8). **Resolution (operator directive "most mature
SOTA++"): 8/8 split, v1.3 = 0x0103.** Rationale: self-documenting in a hex dump
(`0x0103` reads as "1.3"), symmetric and conventional for a `uint16` version word,
and avoids the 16-major-version ceiling of a 4-bit major field.

### D-003 — DType numeric codes (lead)
Canon enumerates element dtypes ("FP16, INT8, etc.") without fixed codes. Assigned:
`FP32=0, FP16=1, BF16=2, INT8=3, INT4=4, UINT8=5, INT16=6, INT32=7` (`format.h`).

### D-004 — Whole-file checksum convention (lead)
Canon §2.8: footer holds "CRC32 of entire file" but does not state how the checksum
field itself is treated. The checksum is computed over the whole file with the
4 footer checksum bytes excluded (treated as zero). Only self-consistent option.

### D-005 — Tensor descriptor includes `tensor_type` (lead)
Canon §2.3's field list omits `tensor_type`; the v1.3 spec §3 includes it as field
#2 ("The Logic Switch", 0=Standard / 1=RecursiveTensor). It is load-bearing (routes
reconstruction). Included immediately after `name`. Full layout:
`[name:str][tensor_type:u8][dtype:u8][ndim:u8][shape:u32*ndim][codebook_id:u16][delta_id:u16][sparse_mask_id:u16][scale:f32][zero_point:i32][flags:u16]`.

### D-006 — Codebook "type" is a model-level role (lead)
Canon §2.5 lists codebook types (global/local/hierarchical/expandable) but the block
stores no type byte. global/local = a model-level role (which tensors reference it);
hierarchical = a distinct composed type (`HierarchicalCodebook`); expandable = the
runtime `Codebook::expand()` capability.

### D-007 — INT4 index packing: low nibble first (lead)
Canon §2.4: "INT4 indices (4 bits per weight, 2 values per byte)" without nibble
order. Element `2k` is the low nibble of byte `k`; element `2k+1` is the high nibble.

### D-008 — Codebook id sentinel (lead)
`codebook_id` / `delta_id` / `sparse_mask_id` use `0xFFFF` (`LQT_ID_NONE`) to mean
"no link", since `0` is a valid id.

### D-009 — Tensor blob layout and sequential walking (lead, integration)
Canon defines no tensor-data offset table. Tensor blobs are stored contiguously
from `header.tensor_offset` in TensorDescriptors order; each blob is
`[codebook_id:u16][delta_id:u16][sparse_mask_id:u16][indices...]` padded to
`LQT_ALIGN_INDEX` (16). Index byte length is derived from the descriptor
(`element_count × dtype_bits`, INT4 packs 2/byte), so no per-tensor offset is stored.

### D-010 — TensorDescriptors chunk framing (lead)
Chunk 0x0002 value = `[u32 count][descriptor...]`. Canon gives no multi-descriptor
framing; a count prefix is added so the loader knows how many descriptors follow.

### D-011 — Self-delimiting metadata region (lead)
The metadata region begins with a `u64` giving the TLV byte length, then the TLV
`MetadataSection`. The header carries only metadata/tensor/footer offsets, and
codebooks sit between metadata and `tensor_offset`, so an explicit length is
required to locate the codebook region without ordering tricks.

---

## Patch 2 design decisions

### D-012 — EditLog serialized as 0x000B TLV chunk
`LqtModel::save()` now emits the in-memory `EditLog` as a TLV chunk (type `0x000B`,
`ChunkType::EditLog`) inside the metadata section. On load, if this chunk is present
it is parsed back into `LqtModel::edit_log_`. If absent (e.g., a file written by v0.1),
the edit log is treated as empty. This matches the chunk registry in canon section 2.3.

### D-013 — Model mutation surface added to LqtModel
Three mutation methods added: `edit_codebook()`, `update_delta()`, `hot_swap_module()`.
Each validates via the existing `MutationValidator`, appends a tamper-evident
`EditLogEntry`, and executes atomically. This closes the gap noted in the v0.1 report
where mutation infrastructure existed but was not exposed through `LqtModel`.

### D-014 — RTA blocks serialized via 0x0012 chunk
`RtaBlock` instances are stored in `LqtModel::rta_blocks_` and serialized as a
`ChunkType::RecursiveWeightMeta` (0x0012) TLV chunk. Each entry in the chunk is
`[name:str][block_bytes...]` with a u32 count prefix. Reconstruction routes
`TensorType::RecursiveTensor` through the RTA block path.

**Superseded by D-024 below**: as originally written, "routes through the RTA
block path" was materially misleading — `LqtModel::reconstruct()` never
computed a real value for `RecursiveTensor`; it cycled `RtaBlock.dims.dim_sizes`
into the output vector regardless of tensor content. `RtaBlock` itself carries
no scalar-reconstruct method; it is purely structural (sparsity + reference
topology). D-024 documents the real reconstruction path that replaces this.

### D-015 — Affine-only reconstruction fallback
When `codebook_id == LQT_ID_NONE` (0xFFFF) and `tensor_type == Standard`,
`LqtModel::reconstruct()` falls back to `dequant_affine()` from `reconstruct.cpp`.
This matches canon section 3.1's formula `weight[i] = indices[i] * scale + zero_point`
for the no-codebook case.

### D-016 — Big-endian read path via BigEndianByteReader
`BigEndianByteReader` is added to `endian.h` as a subclass of `ByteReader` that
byte-swaps all multi-byte reads. A `make_reader()` factory returns the correct reader
type based on the `BigEndian` header flag. Writers always emit little-endian (see v0.1
report item 1).

### D-017 — SIMD dispatch via simd.h compile-time selection
`include/lqt/simd.h` provides a three-level dispatch: AVX2 > NEON > scalar. Scalar
fallbacks are always compiled. Fast paths are declared but require platform-specific
intrinsic implementations (behind `#ifdef LQT_HAS_AVX2` / `#ifdef LQT_HAS_NEON`).
Compile with `-DLQT_FORCE_SCALAR=1` to disable SIMD selection.

### D-018 — GGUF and ONNX conversion stubs
`converters.h` / `converters.cpp` implement `from_gguf()` and `from_onnx()`. GGUF:
parses header, kv pairs, and tensor metadata to produce correct `TensorDescriptor`
entries and affine codebooks; weight bytes are stubbed as zeros. ONNX: validates the
ModelProto magic byte; full initializer parsing requires a protobuf runtime (documented TODO).

---

## Operator design decisions (per module)

### A2 — TLV / metadata (KETTLE)
- TLV `Length` field counts value bytes only; 4-byte padding is excluded and applied
  via absolute buffer position.
- `MetadataSection::parse(reader, region_bytes)` consumes exactly the metadata region
  `[metadata_offset, tensor_offset)`; partial headers inside the region are a `FormatError`.
- Table chunks (0x0005/0x0006/0x0007): `[id:u16][offset:u64][size:u64]` (18 bytes/entry).
- JSON-bearing chunks (0x0003/0x0004/0x000A) store verbatim UTF-8; bearer-type enforced.

### A4 — Delta buffers & sparse masks (MASON)
- Delta on-disk datatype codes: `0=FP16, 1=FP32` (independent of the DType enum;
  canon §2.6 specifies only FP16/FP32 for deltas).
- Sparse-delta flag = bit 7 (0x80) of the datatype byte; sparse payload is interleaved
  `[u32 index][value]` pairs.
- `num_elements` is `uint24` (3 bytes) per canon §2.6.
- Sparse mask encodings implemented: CompressedBitmap (LSB-first per byte) and RLE
  (alternating `uint16` run lengths, first run = leading 0-bits).

### A5 — Recursive Tensor Architecture (LATTICE)
- 24-byte dimension block: `rank:u8 @0`, `distribution:u32 @1`, reserved `@5..16`,
  `flags:u8 @17` (per spec mandate), reserved `@18..23`.
- The five per-dimension sizes (`u32[5]`, d0 Feature / d1 Pattern / d2 Temporal /
  d3 Scale-Fractal / d4 Channel) are appended after the 24-byte block (documented
  extension; total dimension section = 44 bytes).
- Internal metadata KV: `[u16 count]` + per-entry `[u16 key_len][key][u32 val_len][val]`.
- All six sparse encodings implemented with typed builder/parser pairs (Uniform,
  PerDimension, Hierarchical, RLE, CompressedBitmap, CSR).
- Reference entry: `[u8 kind][u32 target]`; Transformed appends `[u32 rows][u32 cols][f32...]`;
  Fractal appends `[u32 iterations][u32 param_count][f32...]`.
- Per-block CRC-64 (XZ) trailer over all preceding block bytes; mismatch → `IntegrityError`.

### A8 — Concurrency & memory mapping (WARDEN)
- `ReaderWriterLock` is a reader-preference lock (mutex + condvars + counters), NOT a
  bare `std::shared_mutex` (whose priority is unspecified) — honors canon §7.2
  "prioritizes readers during active inference".
- `DoubleBuffer<T>` uses `std::atomic_load/atomic_store` on a `shared_ptr` (C++17) for
  lock-free reader snapshots safe across a writer's `store()` (canon §3.4, §7.1).
- `MemoryMappedFile` (POSIX mmap) throws `lqt::LqtError` with `strerror(errno)` on OS
  failure (distinct from FormatError/IntegrityError/AccessError).

### A7 — Mutation / edit log / transactions (LEDGER)
- Edit-log chaining (tamper-evidence, canon §8): each entry's `data_hash =
  crc32([prev_hash:4 LE][timestamp:8 LE][type:1][target bytes][payload_hash:4 LE])`
  where `payload_hash = crc32(payload)` (stored in `signature[0..3]`).
  `verify_chain()` recomputes the chain and detects any altered field.
- 4-constraint validator (canon §5.2): `check_dimensions`, `check_value_bounds`
  (finite AND within `[value_lo, value_hi]`), `check_topology` (DFS cycle detection
  over the module graph), `check_access` (PROTECTED flag + authorization).
- `Transaction<State>` (canon §5.6): copy-validate-swap. Copies State, applies
  staged ops to the copy, validates; on success move-assigns into the target; on
  any failure or exception the target is left byte-identical (sandboxed trial).

### A6 — Recursive weights {B,Φ,R,T,ε} (RELAY)
- `phase_at(t) = Σ_i phase[i]·sin((i+1)·2π·t)`: harmonic series, bounded by
  `||phase||₁`, genuinely time-varying (distinct frequency per harmonic).
- `reconstruct(cb, scale, t) = cb.scalar(base_index)·scale·(1 + phase_at(t)) +
  mean(ε)`: multiplicative phase modulation (base recoverable at t=0); the ε mean
  is folded back to cancel systematic drift across recursion.
- T is `std::array<float,5>` mapping RTA dims d0..d4; R is a `k×d×d` float tensor.

---

## Conformance checklist (v1.3 §9 + canon §9.4)

### Binary & structural
- [x] Parse 32/36-byte header and 64-byte footer (header is 36 per D-001).
- [x] TLV chunk skipping (unknown types preserved) and chunk registry.
- [x] Module Graph JSON carried as verbatim UTF-8 TLV chunk.
- [~] Big/Little endian: little-endian native; readers byte-swap on BIG_ENDIAN flag
      (swap helpers present; full BE materialization is a documented partial).
- [x] CRC32 footer checksum verified; CRC64 per RTA block verified.
- [ ] Edit-log cryptographic signatures: structural (SIGNED_EDITS flag + signature
      bytes carried); signature crypto is out of scope for v0.1 (documented).

### Reconstruction & RTA
- [x] 5D RTA blocks with rank-5 enforcement.
- [x] All 6 sparsity encodings (Uniform/PerDimension/Hierarchical/RLE/Bitmap/CSR).
- [x] Multi-stage reconstruction (base index + codebook · scale + delta, × mask).
- [x] Hierarchical codebooks (primary + residual·scale).
- [x] Fractal iteration / self-reference: RTA reference block (Direct/Transformed/
      Fractal, A5) + recursive-weight quintuple {B,Φ,R,T,ε} (A6) implemented & tested.
      Embedding recursive tensors into the assembled model file is a documented next step.

### Memory & optimization
- [x] 64B (codebook) / 16B (index) / 4B (delta) alignment constants enforced in layout.
- [x] Reader-writer locks + double-buffering for hot-swaps.
- [x] mmap zero-copy file access (MemoryMappedFile).

### Security & evolution
- [x] Sandboxed mutation trials (A7 `Transaction<State>` copy-validate-swap).
- [x] Append-only edit log (A7).
- [~] Mutation quotas / critical-path protection: PROTECTED flag + access check (A7);
      quota policy is a documented model-level hook.

Legend: [x] implemented & tested · [~] partial/structural · [ ] out of scope for v0.1.

---

## Patch 4 deviations

### D-020 — RTA operations ported from Python reference (no deviations)
`rta_contract()`, `rta_project()`, `rta_expand()`, `rta_fractal_iterate()`, `rta_entropy()`,
`rta_normalize()`, `rta_apply_function()` are direct ports from recursive_tensor.py with
dtype changed from numpy to std::vector<float>. Visualization methods (matplotlib) omitted.

### D-021 — RecursiveWeight effective value formula
Port of recursive_weights_core.py `RecursiveWeight.compute_effective_value()`. Depth capped
at 32 (RW_MAX_RECURSION_DEPTH). Threading removed (single-threaded C++ model). PatternLibrary
get_pattern_value simplified: element-wise multiplication of pattern data and context vector.

### D-022 — DynamicalSystemsAnalyzer: power iteration for eigenvalues
Torch.linalg.eigvals replaced with power iteration (max 100 iters, tol 1e-6). Provides
dominant eigenvalue approximation only — exact eigendecomposition not implemented.

### D-023 — TieredCacheManager: no thread safety
Python threading.RLock removed. TieredCacheManager is single-threaded. Callers must
synchronize externally when using from multiple threads.

---

## Patch 5 deviations

### D-024 — RecursiveTensor reconstruction: real math, explicitly bounded scope

Closes the gap left by D-014: `LqtModel::reconstruct()` for
`TensorType::RecursiveTensor` previously returned `RtaBlock.dims.dim_sizes`
cycled into the output vector — not a function of the tensor's actual
content. This decision replaces that with real computation and, where the
supplied canon genuinely does not define a mapping, an explicit thrown error
instead of a further guess.

**Doctrine (fixed by `docs/TRIAXIAL_ARCHITECTURE.md` §3 and the
autodidactic-learning-substrate README's RTA/RWA boundary): weights are
storage buckets, tensors are compute engines.** A `RecursiveWeight` is a
self-contained W={B,Phi,R,T,epsilon} unit — its own codebook index and its
own position in the tensor's 5D lattice (`T`, "exactly 5 floats mapping to
RTA dims d0..d4", `recursive_weight.h:83-104`). A `RecursiveTensor`
(`RtaBlock`: dims + sparsity) does not own or modulate a shared value; it is
the structure that selects *which lattice positions receive computation*.
Where a position has an attached bucket, that bucket's own B/Phi/epsilon
*is* the value there — not an additive nudge to something else. An earlier
draft of this decision got this backwards (one `RecursiveWeight` applied as
a uniform tensor-wide modulation); corrected same-session before any commit.

**New storage**: `LqtModel::recursive_weights_` is a name-keyed map of
**vectors** of `RecursiveWeight` (module A6's already-implemented and tested
quintuple) — a tensor name may have zero, one, or many buckets, one per
occupied lattice position, matching the "buckets of knowledge" framing.
Persisted as a new `ChunkType::RecursiveWeightTable` (0x0011) TLV chunk —
`[u32 bucket_count]{[name:str][RecursiveWeight bytes]}`, a name may repeat
across entries. 0x0011 was unused in the v1.3 registry. This is additive:
files without the chunk parse exactly as before (no buckets attached;
reconstruction runs on the base term only). Note the pre-existing naming
trap this corrects: `RecursiveWeightMeta` (0x0012) has never carried a
`RecursiveWeight` — it carries `RtaBlock` structural data only. The two
chunks now cleanly own: 0x0012 = RTA structure, 0x0011 = the actual
buckets.

**Reconstruction, `LqtModel::reconstruct()`, `TensorType::RecursiveTensor` branch**:

1. **Structural base term (real, not placeholder)**: for lattice positions
   with no attached bucket, reuses the tensor's own per-element codebook
   index array (same mechanism every other tensor type uses, D-009)
   dequantized via `codebook(d.codebook_id)` and `d.scale`
   (`reconstruct_standard`), or the affine fallback (D-015) when
   codebook-less. Delta buffers (D-006 chunk) apply as usual. This is a
   legitimate, valid case on its own: a purely structural `RecursiveTensor`
   with no RWA state behaves like a `Standard` tensor shaped by RTA
   sparsity — it does not error just for lacking buckets.
2. **Sparse structure (real for 5 of 6 encodings)**: the `RtaBlock`'s sparse
   section is decoded per its `sparse_encoding` (DD-04 in `rta.h`).
   `Uniform` is fully dense (no-op). `Hierarchical` and `CompressedBitmap`
   carry exact per-element presence; absent positions are zeroed, with a
   thrown `FormatError` if the block's element count disagrees with the
   descriptor's. `RLE` and `CsrCscCsf` carry literal `f32` values on the
   wire; those values are authoritative and override the base term for the
   positions they cover (CSR's row/column mapping to flat index uses
   `dim_sizes[1]` as the column count, matching `tests/test_rta.cpp`'s own
   CSR fixture).
3. **`PerDimension` sparse encoding — explicitly bounded**: this encoding
   records only aggregate per-axis density (a float in `[0,1]`), not exact
   element membership. There is no rule in any supplied source for turning a
   density value into a hard zero/nonzero decision per element.
   `reconstruct()` throws `FormatError` for this case rather than inventing
   a threshold.
4. **Bucket override (real, not placeholder), applied last**: for each
   `RecursiveWeight` attached to the tensor's name, its `tensor_position`
   (T) is rounded to the nearest integer coordinate and flattened row-major
   against `blk.dims.dim_sizes` (same convention as
   `DenseTensor5D::flat_index` in `rta_ops.h` and the CSR flattening in
   step 2). The resolved position's value is fully replaced by
   `codebook[bucket.base_index] * scale + bucket.phase_at(0.0) +
   mean(bucket.error)` — the bucket's *own* B, not the tensor's shared
   index array, and not a modulation of whatever step 1/2 computed there —
   per Theorem 1.2.1 in `docs/specs/recursive_weights_technical_specs.md`
   §1.1. `t=0` is the reconstruction default; the format has no per-tensor
   stored timestamp. Applied after the sparse-structure step so a bucket
   can legitimately override a position that structure alone marked absent.
   Bounded, thrown rather than guessed: a bucket whose T falls outside the
   tensor's own `dim_sizes`; two buckets resolving to the same position (no
   rule picks a winner); a bucket referencing a `base_index` the tensor's
   codebook doesn't have, or naming a tensor with no codebook at all.
5. **`RtaReference` (Direct/Transformed/Fractal) — explicitly bounded**: the
   v1.3 wire format's reference entries (DD-05) carry a `target` node index
   and, for `Transformed`/`Fractal`, block-level parameters, but no field
   ties a reference to a specific output element, another named tensor, or
   any other addressable entity. The canonical whitepaper's own resolution
   pseudocode (`whitepaper/recursive-tensor-whitepaper.md`, Appendix B.3 /
   §15.1.1) calls an undefined `_resolve_value(...)` that is never completed
   in that document, and no test in this repository exercises `target` as
   anything but an opaque round-tripped integer. A `RecursiveTensor` whose
   `RtaBlock` carries any `references` entries causes `reconstruct()` to
   throw `FormatError` naming this gap, rather than fabricate a resolution
   rule. This is the one part of the RecursiveTensor path this patch leaves
   open; closing it requires either an operator-supplied resolution
   specification or a deliberate new design decision, not a guess.

**Tests** (`tests/test_model_mutations.cpp`): `model_rta_reconstruction_path`
now pins the actual returned value instead of only checking vector length;
`model_rta_reconstruction_with_recursive_weight` pins two buckets overriding
their own positions (own B, own epsilon) while the remaining positions keep
the structural base value, proving buckets are per-position storage, not a
tensor-wide modulation; `model_rta_reconstruction_bounds_colliding_buckets`
and `model_rta_reconstruction_bounds_bucket_out_of_range` assert the new
bucket-placement bounds throw; `model_rta_reconstruction_bounds_references`
and `model_rta_reconstruction_bounds_per_dimension` assert the
sparse/reference explicit-bound paths throw `FormatError` rather than
silently returning a wrong value; `model_recursive_weight_table_roundtrip`
proves the new chunk survives `serialize_to_bytes()`/`parse()` byte-for-byte.

### D-025 — Logged RecursiveWeight bucket edits and logged RecursiveTensor attach/detach (2026-11-21, lane lqt-unify)

Additive. Operator correction (Daeron, 2026-11-21): LQT is not an archive or
checkpoint format; the RecursiveWeights are the base and every learnable tensor
of the cognitive stack quantizes into that base inside ONE live `.lqt` that the
loop computes from and edits. D-024 made a bucket authoritative for its lattice
position but left no logged way to change a bucket, so a live model could not
both carry buckets and be edited (board seq 58). This closes that.

- `MutationType` gains `RecursiveWeightEdit = 6`, `TensorAttach = 7`,
  `TensorDetach = 8`. `EditLogEntry::parse` accepts 0..8 (was 0..5). Files
  that contain none of the new types are byte-identical to before; a pre-D-025
  reader rejects a log containing them with its existing FormatError.
- `LqtModel::edit_recursive_weights(name, [(slot, RecursiveWeight)])` replaces
  whole quintuples (B, Phi, R, T, epsilon, alpha) as ONE mutation: one
  hash-chained entry (target `rw:<name>`, payload `[u32 n]{[u32 slot][RW bytes]}`)
  and one undo snapshot of the previous buckets. Validated before anything is
  applied: slot range, no slot twice, `RecursiveWeight::validate`, B inside the
  tensor's codebook, T inside the RTA dims, no two buckets of the name on one
  position — the D-024 reconstruction bounds enforced at mutation time
  (`ValidationError`).
- `LqtModel::attach_recursive_tensor(desc, index_bytes, RtaBlock, buckets)`
  adds or replaces one RecursiveTensor (descriptor + packed indices + block +
  buckets) as one mutation (target `tensor:<name>`, payload = descriptor, index
  bytes, block, buckets). Requires RecursiveTensor type, index length equal to
  `tensor_index_byte_length`, RTA dims equal to the descriptor shape, codebook
  and delta present when referenced. `detach_tensor(name)` removes all four.
  `rollback()` restores the previous tensor (same position in `tensors_`),
  block and buckets exactly.
- Not changed: the D-024 FormatError bounds (RtaReference, PerDimension,
  colliding / out-of-range buckets at reconstruct), the zero_point convention,
  the wire layout of every existing chunk. The undo stack stays in-memory only
  (D-019); the edit log persists.
- Evidence (operator rule 2026-11-21: no new test code; proof = running the
  system): `runtime/runs/2026-11-21_unified_seed0/` — 40-step seed-0 loop on one
  `model.lqt`, every update a logged edit, reload equal to live for every
  tensor, `verify_edit_log` true, rollback of 1 and of 4 further steps exact.
  Existing CTest suites rerun against the changed `model.cpp`/`edit_log.cpp`.
