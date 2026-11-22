# LQT/LQF Authority Compliance Matrix

**Classification:** INTERNAL
**Version:** 1.0
**Date:** 2026-09-21
**Origin:** Authority-intake documentation pass (packet LQT-001 follow-on)
**Status:** OPERATIONAL EVIDENCE RECORD

---

## 1. Executive Summary

This document maps the material clauses of the four canonical whitepapers under
`whitepaper/` onto the current C++17 implementation, the operator's Python
reference under `original-py-code/`, and the autodidactic substrate. Every
clause is classified IMPLEMENTED, PARTIAL, ABSENT, CONTRADICTED, or NOT
VERIFIABLE, with a file:line or test-name citation for each ruling. The single
most consequential structural finding: the RTA whitepaper (`recursive-tensor-whitepaper.md` §3.1)
specifies an `RTNZ` binary layout that no artifact in this repository
implements — the shipped wire format is the v1.3 Binary Spec `RTATNSR\0`
layout, which the whitepaper contradicts on magic, section order, index
encoding set, and index width. Whitepaper performance claims are entirely
unreproduced and are quarantined as NOT VERIFIABLE.

## 2. Authority Order Applied

Per repo AGENTS.md and the operator instruction for this pass:

1. **Current operator instruction** (this task packet).
2. **Canonical whitepapers** under `whitepaper/` (4 documents; binding on
   conflict).
3. **Executable behavior and tests** in this repository.
4. **Historical records** — `docs/SPEC_COMPLIANCE.md`, `docs/AGENT_REPORT.md`,
   `docs/authority/*` (provenance only; superseded where they disagree with
   the whitepapers).

Where the whitepapers contradict each other (they do; see §5-E1), the operator
previously ratified the v1.3 Binary Spec readings in
`docs/SPEC_COMPLIANCE.md` D-001..D-011. Those rulings are preserved here and
the contradictions are recorded, not overwritten.

A note on whitepaper provenance I verified myself: the main LQT whitepaper has
a structural numbering defect. It runs `## 1` through `## 9.1` (mutation,
self-modification, threading, security sections), then restarts numbering at
`## 2. LQT Format Specification` (line 9243). Worse, the first part jumps from
`### 1.3` (line 43) directly into `#### 5.1.2` (line 287) with no `## 5`
parent heading. I cite the second-half numbering for format clauses (§2.x–§5.x
at lines 9243–9700) and the first-part numbering for mutation mechanics
(§5.1.2–§5.6 at lines 287–2692), and flag the defect here once rather than
per-row.

## 3. Classification Legend

| Status | Meaning |
|---|---|
| IMPLEMENTED | Mechanism present in C++ and exercised by at least one named passing test, with semantics matching the clause. |
| PARTIAL | Mechanism present but bounded, structural-only, or missing sub-clauses; gap stated explicitly. |
| ABSENT | No implementation exists. Known gap; recorded, not concealed. |
| CONTRADICTED | Implementation or operator Python reference behaves differently from the clause, or two authorities conflict irreconcilably. |
| NOT VERIFIABLE | Claim exists only in authority prose; no test, benchmark, or artifact in this repo can confirm or deny it. |

## 4. Test Inventory Basis

237 individual cases across 21 binaries were reported passing by the gate as
of 2026-09-20 (CONTEXT.md). Every IMPLEMENTED ruling below names its evidence
test(s). Gate reproduction: `./scripts/gate.sh` (CMake/CTest when `cmake` is
installed; direct GCC fallback otherwise — the fallback is not CMake/CTest
validation and is labeled as such in gate output).

---

## 5. Clause Matrix

### 5-A. Container format (whitepaper §2.1–§2.8, lines 9243–9465)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| A1 | File magic `LQT1` header / `LQTF` footer, little-endian | §2.2 L9271, §2.8 L9460 | IMPLEMENTED | `include/lqt/format.h:18-19`; tests `file_header_bad_magic_rejected`, `file_footer_bad_magic_rejected` |
| A2 | Header 32 bytes fixed | §2.2 L9267/L9274 | CONTRADICTED (resolved by deviation) | Whitepaper self-contradiction: three `uint64` offsets at 0x0C/0x14/0x1C end at byte 36. Operator ruling D-001: 36-byte header. `include/lqt/format.h:29`; test `header_roundtrip_is_36_bytes`. Also contradicted by operator Python: `original-py-code/lqt_library.py:29` sets `LQT_HEADER_SIZE = 32` |
| A3 | Version word encoding | §2.2 L9272 | CONTRADICTED (resolved by deviation) | Whitepaper prose "4 bits major + 12 bits minor"; operator ruling D-002 uses 8/8 = `0x0103`. `include/lqt/version.h`; tests `version_encoding`, `version_encoding_8_8` |
| A4 | Header flags bitmask (bits 0–7: HAS_DELTAS … SHARDED) | §2.2 L9279–9288 | IMPLEMENTED | `include/lqt/format.h:43-52` (all 8 flags); test `file_header_round_trip`. Flag *semantics* vary: see A12, D-crypto, D-compression rows |
| A5 | TLV chunk framing: 2B type, 4B length, value 4B-aligned | §2.3 L9290–9301 | IMPLEMENTED | `include/lqt/tlv.h`, `src/tlv.cpp`; tests `tlv_roundtrip_known_and_unknown`, `padding_excluded_from_length_field`, `tlv_order_preserved_roundtrip`. Deviation noted in SPEC_COMPLIANCE A2: length counts value bytes only |
| A6 | Chunk type registry 0x0001–0x0010 + 0xFFFF | §2.3 L9304–9324 | IMPLEMENTED | `include/lqt/format.h:57-76` (full registry incl. 0x0012 RTA meta from v1.3 spec); test `tlv_roundtrip_known_and_unknown` |
| A7 | Tensor descriptor field list | §2.3 L9326–9338 | CONTRADICTED (resolved by deviation D-005) | Whitepaper omits `tensor_type`; v1.3 spec and both implementations carry it. `include/lqt/descriptor.h`; `original-py-code/lqt_library.py:78`; test `descriptor_roundtrip` |
| A8 | Descriptor flag bits 0–5 (TRAINABLE…CHECKPOINT) | §2.3 L9340–9347 | IMPLEMENTED | `include/lqt/format.h:116-123`; exercised via `validator_rejects_protected_tensor_no_auth`, `validator_allows_protected_tensor_with_auth` |
| A9 | Tensor blob `[codebook_id:u16][delta_id:u16][sparse_mask_id:u16][indices…]` | §2.4 L9349–9361 | IMPLEMENTED with framing deviation D-009 | `include/lqt/model.h:17-22` (D-009 framing), `src/model.cpp` save/parse; tests `model_full_roundtrip_reconstruct`, `end_to_end_int4_reconstruct` |
| A10 | INT4 packing (2 values/byte) | §2.4 L9364 | IMPLEMENTED with nibble-order deviation D-007 | `include/lqt/format.h:86`, `src/reconstruct.cpp` unpack; tests `unpack_int4_low_nibble_first`, `end_to_end_int4_reconstruct` |
| A11 | Codebook block `[id:u16][num_vectors:u16][vector_dim:u16][FP16 data]` | §2.5 L9369–9387 | IMPLEMENTED | `include/lqt/codebook.h`, `src/codebook.cpp`; tests `codebook_vector_roundtrip`, `codebook_scalar_roundtrip_and_edit`, `reconstruct_vector_codebook` |
| A12 | Codebook variants: global/local/hierarchical/expandable | §2.5 L9383–9387 | PARTIAL | Hierarchical implemented (`reconstruct_hierarchical_codebook` test, `src/reconstruct.cpp`); expandable implemented (`codebook_expand` test, `Codebook::expand()`); global/local are model-level roles only (deviation D-006) — no on-disk discriminator byte exists |
| A13 | Delta buffer block `[delta_id:u16][datatype:u8][num_elements:u24][values]` | §2.6 L9389–9407 | IMPLEMENTED with codes deviation A4-DD-1 | `include/lqt/delta.h:14-45` (on-disk codes 0=FP16, 1=FP32 — independent of DType enum; whitepaper assigns no codes); tests `delta_fp16_roundtrip_apply`, `delta_fp32_roundtrip_apply`, `delta_num_elements_uint24` |
| A14 | Sparse deltas | §2.6 L9404 | IMPLEMENTED with framing deviation A4-DD-2 | Sparse flag = bit 7 of datatype byte, interleaved `[u32 index][value]` pairs. `include/lqt/delta.h:20-27`; tests `delta_sparse_roundtrip_apply`, `reconstruct_with_delta_and_mask`. Whitepaper specifies the *capability* but no wire format; the framing is a lead decision |
| A15 | Module graph JSON as TLV chunk 0x0003 (DAG, hot-swap, topology validation) | §2.7 L9409–9454 | PARTIAL | JSON carried verbatim (`model.h:82`, `json_survives_section_roundtrip` test); topology cycle detection implemented (`validator_detects_cycle_in_module_graph`, `validator_rejects_unresolved_edge`). The whitepaper's per-module `mutation_hooks` structure is storage-only — no runtime consumes hooks. Not load-bearing yet |
| A16 | Footer 64 bytes: magic, CRC32 of whole file, edit-log offset, timestamp, 40B reserved | §2.8 L9456–9464 | IMPLEMENTED with checksum-convention deviation D-004 | `include/lqt/header.h` (footer), `src/crc.cpp`; tests `footer_roundtrip_is_64_bytes`, `file_checksum_detects_corruption`, `file_checksum_excludes_field_and_detects_corruption`, `file_footer_reserved_bytes_zero` |
| A17 | Reconstruction formula `w = codebook[idx]*scale + delta`, then `*= mask` | §3.1 L9470–9487 | IMPLEMENTED | `src/reconstruct.cpp` (`reconstruct_standard`), `src/model.cpp:424-428`; tests `model_full_roundtrip_reconstruct`, `reconstruct_with_delta_and_mask`, `changing_codebook_changes_reconstruct`, `affine_dequant_formula` (D-015 no-codebook path) |
| A18 | Hierarchical codebook reconstruction `primary + residual*scale` | §3.2 L9489–9498 | IMPLEMENTED | `src/reconstruct.cpp` hierarchical path; test `reconstruct_hierarchical_codebook` |
| A19 | Big-endian support (header flag bit 3) | §2.2 L9283 | PARTIAL | Read path only: `BigEndianByteReader` in `include/lqt/endian.h` (deviation D-016); tests `big_endian_flag_detection`, `big_endian_reader_byteswap`. Writers are little-endian only; full BE materialization absent. Known gap |
| A20 | Metadata chunk types 0x0008–0x0010 (vocabulary, KV-cache, ACL, metrics, …) | §2.3 L9315–9323 | PARTIAL | Registry entries and skip/preserve behavior exist (`tlv_roundtrip_known_and_unknown`); no producer or consumer for 0x0008/0x0009/0x000C–0x0010 payloads. Storage-level only |

### 5-B. Mutation subsystem (whitepaper §4.1–§4.2 L9520–9556; §5.1.2–§5.6 L287–2692)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| B1 | Mutation type 1: Codebook editing | §4.1 L9524–9527 | IMPLEMENTED | `src/model.cpp` `edit_codebook` (model.h:129-132); tests `model_edit_codebook_changes_reconstruction`, `codebook_scalar_roundtrip_and_edit`, `changing_codebook_changes_reconstruct` |
| B2 | Mutation type 2: Delta injection | §4.1 L9529–9532 | PARTIAL | Whole-buffer replacement implemented: `LqtModel::update_delta` (`src/model.cpp:505-511`); test `model_update_delta_replaces_buffer_in_reconstruction`. Whitepaper §5.1.2 additionally specifies element-wise sparse `update_delta_sparse`, mutability flags (`DELTA_FLAG_MUTABLE`), `make_delta_writeable` page-protection semantics, and create-or-replace-by-tensor — none of those exist. Known gap |
| B3 | Mutation type 3: Module hot-swapping | §4.1 L9534–9536, §5.1.3 L663–914 | PARTIAL | Blob/tensor replacement with rollback snapshot implemented: `src/model.cpp:513-551`; tests `model_hot_swap_module_replaces_blob`, `rollback_one_after_codebook_edit_restores_value` (module path), `double_buffer_basic/stress` (concurrent read safety). Missing per §5.1.3: `MODULE_FLAG_HOT_SWAPPABLE` gate, interface-compatibility check, parse-and-validate replacement modules — `hot_swap_module` accepts any bytes without validation. Do not claim O(1) hot swapping from storage alone (LQT_AUTHORITY_MATRIX precedent stands) |
| B4 | Mutation type 4: Sparse mask updates | §4.1 L9539–9542, §5.1.4 L916–1238 | PARTIAL | Mask replacement via builder + reconstruction applies mask (`include/lqt/sparse_mask.h:51+`; tests `mask_bitmap_roundtrip_apply`, `mask_rle_roundtrip_equals_bitmap`, `reconstruct_with_delta_and_mask`). No in-place `update_mask` API, no `MASK_FLAG_MUTABLE`, no density-statistics recomputation (§5.1.4 L1074-1084). Known gap |
| B5 | Mutation type 5: Hyperparameter tuning | §4.1 L9544–9547 | PARTIAL | Model-level hyperparams only (`set_hyperparam`, tests `hyperparams_encode_decode_roundtrip`, `hyperparams_roundtrip_in_section`). Whitepaper's per-module scoping (`model.set_hyperparameter("attention_1", …)`) has no consumer. Known gap |
| B6 | Four validation constraints: dimensions, value bounds, topology, access control | §4.2 L9549–9555; §5.2 L1240+ | IMPLEMENTED | `include/lqt/mutation.h:46` `MutationValidator`; tests `validator_rejects_dimension_mismatch`, `validator_rejects_over_bound`, `validator_rejects_under_bound`, `validator_rejects_nan`, `validator_rejects_inf`, `validator_detects_cycle_in_module_graph`, `validator_rejects_protected_tensor_no_auth`, `validator_accepts_valid_edit` |
| B7 | Append-only edit log with rollback to entry | §5.3 L1751–2180; §4.4 L9582–9596 | IMPLEMENTED with mechanism deviation | Chained CRC-32 tamper evidence (`include/lqt/edit_log.h:50-90` `make_entry` chain hash); full undo stack with `rollback(n)` (`model.h:146-147`). Deviation: whitepaper §5.3 stores entries in a footer-offset file region; implementation persists the log as TLV chunk 0x000B (deviation D-012). Tests: `editlog_verify_chain_intact`, `editlog_verify_chain_detects_tamper`, `editlog_tamper_detected_after_mutation`, `editlog_persists_through_save_reload_cycle`, `rollback_reduces_edit_log_size_by_n`, `rollback_chain_remains_valid_after_remutation` |
| B8 | Batch mutation system (multi-op atomic application) | §5.5 L2332–2561 | PARTIAL | `Transaction<State>` copy-validate-swap covers atomic multi-op semantics (`include/lqt/transaction.h:42+`; tests `transaction_commits_three_op_batch`, `transaction_abort_prevents_commit`, `transaction_rollback_on_op_exception`, `transaction_rollback_on_validation_failure`). The dedicated BatchMutationManager facade of §5.5 is not implemented |
| B9 | Mutation API facade (DeltaEditor / ModuleSwapper / SparseMaskEditor classes) | §5.4 L2181–2331 | ABSENT | No such facade classes exist; mutation surface is direct `LqtModel` methods (D-013). Deliberate simplification, documented here as a gap |
| B10 | Self-modification framework (interface, optimizer, security manager, audit) | §6 L2692–4617 | ABSENT | Chunk type 0x000A (SelfModificationRules) is defined and skippable (`format.h:67`) but nothing produces, parses as objects, or enforces it. No self-optimization or audit subsystem in C++. Largest whitepaper section (≈2000 lines) with zero implementation surface — recorded as a known gap, not a roadmap promise |
| B11 | Mutation quotas / rate limiting | §5.2 (stability sub-clauses); SPEC checklist | PARTIAL | PROTECTED flag + access check implemented (B6); quota policy absent — matches SPEC_COMPLIANCE A7 checklist "[~]" entry |

### 5-C. Concurrency and memory (whitepaper §3.4 L9508–9516; §7 L4618–6060)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| C1 | Reader-writer lock prioritizing readers | §3.4, §7.2 L4828–5143 | IMPLEMENTED | `include/lqt/concurrency.h` `ReaderWriterLock` (mutex + condvars + counters, reader-preference per SPEC_COMPLIANCE A8); tests `rwlock_basic`, `rwlock_try`, `rwlock_stress` (post-deadlock-repair, commit `4ad12d1`) |
| C2 | Double-buffering for hot-swap-safe reads | §3.4, §7.1 | IMPLEMENTED | `include/lqt/concurrency.h` `DoubleBuffer<T>` (atomic `shared_ptr` swap); tests `double_buffer_basic`, `double_buffer_stress` |
| C3 | mmap zero-copy access | §5.1 L9599–9611, §7.x | IMPLEMENTED (POSIX only) | `include/lqt/mmap.h`, `src/mmap.cpp`; tests `mmap_create_write_read`, `mmap_nonexistent`. Windows path absent |
| C4 | Thread pool | §7.4 L5322–5422 | ABSENT | No thread pool in the C++ tree. Known gap |
| C5 | Parallel reconstruction | §7.5 L5423–5587 | ABSENT | Reconstruction is single-threaded. Known gap |
| C6 | Wait-free / lock-free operations beyond `DoubleBuffer` | §7.6 L5588–5727 | ABSENT | Only the `shared_ptr` atomic snapshot exists (C2). No hazard pointers, no lock-free counters. Known gap |
| C7 | Cross-process synchronization | §7.7 L5728–6060 | ABSENT | Nothing implemented. Known gap |
| C8 | Tiered caching of reconstructed values | §5.2 L9612–9620 | PARTIAL | `TieredCacheManager` ported (single-threaded, D-023) in `include/lqt/rw_cache.h`; tests `cache_tiered_l1_hit`, `cache_tiered_l2_promotion`, `cache_lru_eviction`, `cache_performance_tracker`. Not wired into the standard reconstruct path — it serves the RW subsystem |

### 5-D. Security and integrity (whitepaper §8 L6061–7804; §2.2 flag semantics)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| D1 | Whole-file CRC-32 integrity verification | §2.8, §8.3 L6564+ | IMPLEMENTED | `src/crc.cpp`; tests `file_checksum_detects_corruption`, `integration_crc_corruption_detected`, `model_crc_detects_corruption` |
| D2 | Per-RTA-block CRC-64 integrity | v1.3 spec §4 (via briefing); RTA blocks carry trailer | IMPLEMENTED | `include/lqt/rta.h:139-143` (DD-07, CRC-64/XZ coverage); tests `rta_crc64_clean_block_passes`, `rta_crc64_detects_corruption` |
| D3 | Cryptographically signed edit logs (SIGNED_EDITS bit 5) | §2.2 L9285, §8.1 L6065–6280 | ABSENT (structural only) | `SIGNED_EDITS` flag exists and `EditLogEntry.signature` carries opaque bytes (`edit_log.h:56`), but no key policy, signing, or verification. Matches SPEC_COMPLIANCE checklist "[ ] crypto out of scope for v0.1". Known gap |
| D4 | Access control system (ACL chunk, per-tensor auth) | §8.2 L6281–6563; §2.3 0x000F | PARTIAL | Tensor-level PROTECTED + authorization token in validator (tests `validator_rejects_protected_tensor_no_auth`, `validator_allows_protected_tensor_with_auth`). The 0x000F ACL chunk has no parser/producer. Module-level ACL absent |
| D5 | Compressed sections (COMPRESSED bit 6, compression dictionary 0x000D) | §2.2 L9286; §2.3 L9320 | ABSENT | Flag and chunk types defined; no codec. Deliberate, documented (LQT_AUTHORITY_MATRIX precedent) |
| D6 | Sharded models (SHARDED bit 7, 0x000C chunk) | §2.2 L9287; §5.4 L9630–9639 | ABSENT | Flag and chunk type defined; no sharding logic. Known gap |
| D7 | Secure operation modes / secure storage | §8.4 L7284+, §8.5 L7566+ | ABSENT | No implementation. Known gap |

### 5-E. RTA whitepaper clauses (`recursive-tensor-whitepaper.md`)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| E1 | RTA binary format: magic `RTNZ` (4B), version, dimension size, rank byte, sparsity f32, distribution byte, index block (N:u64 + encoding enum), value block, reference block | §3.1 L205–242 | CONTRADICTED | No artifact implements this layout. The shipped format is the v1.3 Binary Spec layout: magic `RTATNSR\0` (8B) → metadata KV → 24B dimension block → 5×u32 dim sizes → sparse section (tag+len+payload) → reference block → CRC-64. `include/lqt/rta.h:22` (`LQT_RTA_MAGIC`), DD-06 layout at `rta.h:128-137`. The operator's Python reference implements **neither** layout — `RecursiveTensor.serialize()` emits a JSON dict (`original-py-code/recursive_tensor.py:1510-1558`). Three authorities, three formats. The v1.3 wire format is the operator-ratified one; the whitepaper §3.1 layout is a specification orphan |
| E2 | Index encodings `{COORDINATE=0, CSR=1, CSC=2, COO=3, CUSTOM=4}` | §3.1 L222 | CONTRADICTED (resolved) | Implemented encodings are the v1.3 set `{Uniform=0, PerDimension=1, Hierarchical=2, RLE=3, CompressedBitmap=4, CsrCscCsf=5}` — different names, different codes, different payloads. `include/lqt/format.h:127-134`; all six exercised: tests `rta_sparse_uniform_roundtrip`, `rta_sparse_per_dimension_roundtrip`, `rta_sparse_hierarchical_roundtrip`, `rta_sparse_rle_roundtrip`, `rta_sparse_compressed_bitmap_roundtrip`, `rta_sparse_csr_roundtrip` |
| E3 | Rank-5 invariant (rank byte "always 5") | §3.1 L214; §2.1 L70 | IMPLEMENTED | `include/lqt/format.h:155` (`LQT_RTA_RANK = 5`), enforced in `RtaDimensionBlock::validate` (`rta.h:185`); tests `rta_rank_not_5_rejected`, `rta_validate_rank_enforced`, `descriptor_recursive_requires_rank5`. Note: operator Python `RecursiveTensor.__init__` defaults `rank=4` (`recursive_tensor.py:97`) — see §7 finding W-2 |
| E4 | Dimensional semantics d1 Feature / d2 Pattern / d3 Temporal / d4 Scale / d5 Channel | §2.2 L86–114 | IMPLEMENTED (as d0..d4) | `include/lqt/rta.h:40-45` (DD-02 semantic mapping); test `rta_dimension_block_flags_at_offset_17`, `rta_dimension_block_exact_size`. One-indexed whitepaper vs zero-indexed C++ is cosmetic; semantics align |
| E5 | Sparsity factor σ stored and meaningful | §2.1 L77, §2.3 L157–172, §3.1 L215 | CONTRADICTED | The v1.3 wire format has no sparsity field — density is expressed structurally per encoding (density maps, bitmap words). `RtaDimensionBlock` (`rta.h:162-166`) carries rank/distribution/flags/dim_sizes only; there is no σ anywhere in the C++ block, the descriptor, or the operator Python RTA serialization. The whitepaper's σ-as-first-class-field semantics are orphaned |
| E6 | Recursive property: self-reference function S: T→T with fixed-point substructure (Banach) | §2.4 L174–186 | PARTIAL | Fixed-point machinery exists one level up, in the recursive-weight quintuple: `rw_compute.h` (Theorem 1.2.1 fixed-point convergence), `rw_dynamics.h` `fixed_point_convergence`, `convergence_value()` (`recursive_weight.h:140`); tests `dynamics_fixed_point_convergence_basic`, `dynamics_fixed_point_alpha_too_large_throws`, `rta_fixed_point_constant`, `rta_fixed_point_contractive`. But `RtaBlock` references are never *resolved* — see E7. The tensor-level self-reference function of §2.4 is not evaluated anywhere |
| E7 | Recursive reference resolution (DIRECT/TRANSFORM/FRACTAL entries evaluated during reconstruction or operations) | §3.1 L233–239; §3.2.3 L287–303 | PARTIAL / known gap | References serialize, round-trip, and validate structurally: `RtaReference` (`rta.h:189-206`, DD-05 wire format), tests `rta_reference_direct_roundtrip`, `rta_reference_transformed_roundtrip`, `rta_reference_fractal_roundtrip`, `rta_reference_multiple_mixed_kinds`, `rta_zero_references_roundtrip`. **No engine evaluates references**: neither `reconstruct_standard` nor `LqtModel::reconstruct` consumes them, and no operation applies a reference's transform matrix or iteration parameters to tensor values. This is the deepest RTA semantic gap in the repo |
| E8 | Fractal iteration `z → z² + c` with escape threshold | §4.3.1 L515–532 | IMPLEMENTED with dtype narrowing | `include/lqt/rta_analysis.h:20-30` `rta_fractal_iterate`; tests `rta_fractal_iterate_escape`, `rta_fractal_iterate_bound_zero`. Deviation: operator Python iterates complex values (`recursive_tensor.py:1042-1090` supports `complex64`); C++ is `float`-only, and `c_func` returns a real `c`. Complex-domain fractal iteration absent |
| E9 | Scale transform / multi-scale aggregation (`scale_transform`, `scale_aggregate`) | §4.3.2 L556–573 | ABSENT | No C++ or Python implementation of either method (verified by symbol search across `include/`, `src/`, and `recursive_tensor.py`). The whitepaper clause has no reference implementation anywhere in the archive. Known gap |
| E10 | Pattern matching (`match_pattern`, `self_similarity` on tensors) | §4.4.1 L579–595 | ABSENT | No tensor-level pattern matching in C++ (`include/` and `src/` contain only `rw_dynamics::self_similarity_metric` for RW reference matrices — different semantics) or in the operator Python (no such methods on `RecursiveTensor`). The whitepaper §7.1.2 `detect_patterns` pseudocode was never realized. Known gap |
| E11 | Pattern extraction / replacement (`extract_patterns`, `replace_pattern`) | §4.4.2 L626–642 | ABSENT | Same status as E10; no implementation in either language. Known gap |
| E12 | Project / contract / expand operations | §4.2.1–§4.2.2 L487–509 | IMPLEMENTED | Direct ports per D-020: `include/lqt/rta_ops.h` (`rta_project`, `rta_contract`, `rta_contract_sparse`, `rta_expand`); tests `rta_apply_function_square`, plus the full `test_rta_ops.cpp` surface (13 cases incl. sparse contract and basis normalization). Numerical cross-language fixture against Python still open (LQT_AUTHORITY_MATRIX disposition stands) |
| E13 | Entropy, normalization, function application, density function | RTA ops surface | IMPLEMENTED | `include/lqt/rta_analysis.h` (`rta_entropy`, `rta_normalize`, `rta_apply_function`, `rta_density`); tests `rta_entropy_uniform`, `rta_entropy_single`, `rta_entropy_empty`, `rta_normalize_l1/l2/zero_input`, `rta_apply_function_square/threshold`, `rta_density_basic` |
| E14 | Distribution types {NORMAL, UNIFORM, EXPONENTIAL, CUSTOM} | §2.5 L188–199; §3.1 L216 | IMPLEMENTED (as stored enum) | `include/lqt/format.h:138-143` `RtaDistribution`; test `rta_all_distributions_roundtrip`. Caveat: this is the *wire* representation; the C++ layer never samples from these distributions (initialization is a Python-side concern in the reference) |
| E15 | Multi-stage reconstruction of RTA values through codebook machinery | v1.3 spec (via briefing); SPEC checklist | PARTIAL | `model_rta_reconstruction_path` test exercises the routing, but the path returns the dimension envelope (`src/model.cpp:386-403`); full RTA value reconstruction is the documented open gap (TASK.md invariant: do not call the RTA model path complete) |
| E16 | RTA performance/complexity claims (memory tables, OOM benchmarks, 50–90% pattern compression) | §6 L844–916 | NOT VERIFIABLE | No benchmark artifact, harness, or dataset in the repo reproduces any number in §6.1.2/§6.2. Do not cite these as achieved results |

### 5-F. Recursive weights quintuple {B, Φ, R, T, ε} (briefing §3; `docs/specs/recursive_weights*.md`; operator Python `recursive_weights_core.py`)

Note: the main LQT whitepaper contains **no** recursive-weight clause (verified
by full-text search). RW authority is the briefing + the recursive-weights
specifications under `docs/specs/` + the operator Python. Classified here
because the triaxial integration clause (5-G) depends on RWA as the weight
axis.

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| F1 | Quintuple structure B/Φ/R/T/ε with T mapping RTA dims d0..d4 | briefing §3; `recursive_weights_core.py:2367+` | IMPLEMENTED | `include/lqt/recursive_weight.h:83-104` (B u32, Φ vector, R k×d×d, T `array<float,5>`, ε vector); tests `validate_passes_for_valid_weight`, `validate_throws_on_bad_reference_size`, `validate_throws_on_dim_mismatch` |
| F2 | Effective value recurrence `W_eff(i,t) = B + α·W_eff(i-1,t) + ΣR_j·W_ref + Φ(t) + ε` | `recursive_weights_core.py` `compute_effective_value`; spec Theorem 1.2.1 | IMPLEMENTED with documented deviations D-021 | `include/lqt/rw_compute.h` (depth cap 32 = `RW_MAX_RECURSION_DEPTH`; threading removed; PatternLibrary lookup simplified); tests `reconstruct_finite_and_nontrivial`, `reconstruct_scalar_codebook_scale`, `reconstruct_vector_codebook` |
| F3 | Phase modulation Φ(t) harmonic series | spec §3.1 formula; briefing | IMPLEMENTED with formula-selection note | `include/lqt/recursive_weight.h:36-51` (documented formula choice — canon underspecified the operator); tests `phase_at_zero_is_zero`, `phase_at_finite_bounded_varying` |
| F4 | Dynamical-systems theorems (fixed point, Lyapunov, attractor dimension, capacity, Kolmogorov, spectral radius, error bounds) | `recursive_weights_core.py:188-343` `DynamicalSystemsAnalyzer`; spec Theorems 1.2.x–1.7.x | IMPLEMENTED with deviations D-021/D-022 | `include/lqt/rw_dynamics.h` (all theorem functions; power iteration replaces exact eigvals — dominant eigenvalue only); tests `dynamics_lyapunov_stable_small_matrices`, `dynamics_lyapunov_unstable_large_matrix`, `dynamics_attractor_*` (via `dynamics_frobenius_norm_identity`, `dynamics_spectral_radius_scaled_identity`), `dynamics_convergence_rate_basic`, `dynamics_error_accumulation_decay`, `dynamics_self_similarity_identity_matrices` |
| F5 | Evolution engine + pattern library | `recursive_weights_core.py:659, 516` | IMPLEMENTED with simplification | `include/lqt/rw_evolution.h` `PatternLibrary`/`EvolutionEngine`; `test_recursive_weight.cpp` + `test_rw_reference.cpp` (17 cases) exercise registration, lookup, evolution steps |
| F6 | `.rw` standalone file format (`RecursiveWeightHeader`, `RecursiveWeightMetadataChunk`, `LQFVersionInfo`) | `recursive_weights_core.py:82-186` | ABSENT | `RecursiveWeight::serialize/parse` exists for block-level I/O (`recursive_weight.h:108-109`), but no `.rw` container header/version/chunk format is implemented in C++. The autodidactic substrate README lists the same gap ("native `.rw` serializer/loader contract … registry-only fallback"). Known gap on both sides |
| F7 | GPU kernels / SIMD ops / memory pool for RW | `recursive_weights_core.py:1644-1804` | PARTIAL | SIMD scalar/AVX2/NEON dispatch exists for dequant paths (`include/lqt/simd.h`, D-017; tests `simd_dequant_int8_scalar_agreement_64`, `simd_fp16_to_fp32_known_values`, `test_simd_avx2.cpp` 9 cases) but there is no RW-specific GPU kernel or memory pool. CUDA/GPU surfaces entirely absent |

### 5-G. Triaxial integration (triaxial paper §2.1, §2.10, §3.8; metacognitive paper §2.1, §3.1)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| G1 | Three-axis manifold Ψ = ⟨T_R, T_E, T_M⟩ with triaxial integration operator `tanh(W_R·T_R + W_E·T_E + W_M·T_M)` | triaxial §2.1 L40–55, §3.8 L300–311 | ABSENT (C++) / PARTIAL (Python) | No C++ triaxial operator exists. The substrate implements axis *roles* — RTA attention selection (`autodidactic_learning.py:936-952` `RTAAttention.select`), RWA weight registry (`LocalRWAWeight`/`LocalRWARegistry`, lines 342-384), metacognitive monitoring (`MetacognitiveMonitor`, lines 499-556) — but no `tanh`-projection integration operator with learned W_R/W_E/W_M. The `compute_triaxial_integration_score` in `metacognitive_tensor.py:1367` is a weighted-average heuristic, not the §3.8 operator. Known gap in both trees |
| G2 | RTA as structural attention (selects which entities receive computation) | substrate README boundary table; triaxial §2.2 | PARTIAL | Substrate-level: `RTAAttention.select` over knowledge entities (Python only). C++ RTA provides structure + ops but no attention selector. The C++↔Python boundary contract (RTA selects, RWA stores, LQT contains) is honored by convention, not by code |
| G3 | RWA as recursive weight/state storage ("buckets of knowledge") | substrate README; recursive-weights specs | PARTIAL | C++ RW quintuple + evolution + cache surfaces exist (F1–F5). The substrate's "buckets of knowledge" live in `LocalRWARegistry` in Python memory with a registry-only fallback — the native `.rw` persistence contract is unimplemented (F6). Weights-in-LQT-containers is architecturally asserted; no code path today serializes a trained substrate weight into an `.lqt` file |
| G4 | Ethical Tensor axis: 5 ethical dimensions, breath-phase modulation | triaxial §2.3 L99–111; `ethical_tensor.py:17` | ABSENT (C++) / IMPLEMENTED (Python reference) | The five dimensions (`good_harm, truth_deception, fairness_bias, liberty_constraint, care_harm`) and `QuantumBreathAdapter` modulation exist only in `original-py-code/ethical_tensor.py:17-197` and re-derived in the substrate (`EthicalLearningFilter`, lines 218-341). No C++ surface. See `docs/PY_TO_CPP_CONVERSION_CONTRACT.md` for the conversion obligations |
| G5 | Metacognitive Tensor axis: 15-component MetacognitiveState, five component engines + three integration engines | metacognitive paper §2.1 L48–67; `metacognitive_tensor.py:22-42` | ABSENT (C++) / IMPLEMENTED (Python reference) | Full Python reference exists (`metacognitive_tensor.py`: ContradictionDepthField, CoherenceTraceMap, ReflectiveIndexLayer, FeedbackEntropyVector, IdentityCoherenceTensor, MetacognitiveTensor, plus AdvancedMetacognitiveTensor with TemporalEigenstateEngine, RecursiveLoopInterceptor, EigenrecursiveBayesianCore). No C++ surface. Conversion obligations in the contract doc |
| G6 | Breath-phase taxonomy | `ethical_tensor.py:24-29` (4 phases) vs substrate fallback enum (7 phases, `autodidactic_learning.py:183-191` importing `sacred_harmonic_ratio.BreathPhase`) | CONTRADICTED | Two incompatible BreathPhase enums coexist: the operator reference defines {INHALE, HOLD_IN, EXHALE, HOLD_OUT}; the substrate expects {INHALE, PAUSE_RISING, HOLD, EXHALE, PAUSE_FALLING, REST, DREAM} and degrades to `BREATH_SYSTEM_AVAILABLE = False` when its import is missing. Any py→cpp conversion must rule which taxonomy is canonical. Recorded; ruling deferred to operator |
| G7 | Consciousness emergence criteria / verification protocol | triaxial §3.9, §3.11; metacognitive paper §5 | NOT VERIFIABLE | No test, benchmark, or artifact in the repo evaluates any emergence criterion (ethical coherence over synthetic dilemmas, identity stress tests, temporal invariance, basin-of-attraction analysis). These are theory claims, not implementation claims |

### 5-H. Published performance claims (whitepaper §11; RTA §6)

| # | Clause | Authority locus | Status | Evidence |
|---|---|---|---|---|
| H1 | Memory efficiency tables (7B model 4.0 GB etc.) | §11.1 L10006–10018 | NOT VERIFIABLE | No benchmark artifact in repo. (The 4 GB figure was previously cited as motivation for the D-001 uint64 footer-offset ruling; that motivational use stands, the number itself remains unreproduced) |
| H2 | Inference speed claims | §11.2 L10019–10036 | NOT VERIFIABLE | No benchmark harness exists |
| H3 | Quantization quality (perplexity deltas) | §11.3 L10037–10047 | NOT VERIFIABLE | No eval harness exists |
| H4 | RTA empirical benchmark table (§6.1.2) | RTA §6.1.2 L866–879 | NOT VERIFIABLE | See E16 |

---

## 6. Status Tallies

Counted per row across §5-A through §5-H (80 clauses total):

| Status | Count | Clause IDs |
|---|---|---|
| IMPLEMENTED | 32 | A1, A4, A5, A6, A8, A9, A10, A11, A13, A14, A16, A17, A18, B1, B6, B7, C1, C2, C3, D1, D2, E3, E4, E8, E12, E13, E14, F1, F2, F3, F4, F5 |
| PARTIAL | 18 | A12, A15, A19, A20, B2, B3, B4, B5, B8, B11, C8, D4, E6, E7, E15, F7, G2, G3 |
| ABSENT | 17 | B9, B10, C4, C5, C6, C7, D3, D5, D6, D7, E9, E10, E11, F6, G1 (C++), G4 (C++), G5 (C++) |
| CONTRADICTED | 7 | A2, A3, A7, E1, E2, E5, G6 |
| NOT VERIFIABLE | 6 | E16, G7, H1, H2, H3, H4 |

Tally notes:
- Rows carrying an operator-ratified deviation (e.g. A2, A3, A7, B7, E8)
  remain in their primary bucket; a recorded ruling is not a demotion, but
  the contradiction stays on the record for audit.
- F6 is counted once under ABSENT: block-level `RecursiveWeight`
  serialize/parse exists (credited to F1–F5 surfaces), but the clause as
  written — the `.rw` versioned container format — has no implementation on
  either the C++ or substrate side.
- G1/G4/G5 are counted under ABSENT with the parenthetical qualifier because
  the Python reference side of those clauses is implemented; only the C++
  surface is absent. The qualification is load-bearing for the py→cpp
  conversion effort (`docs/PY_TO_CPP_CONVERSION_CONTRACT.md`).
- The CONTRADICTED bucket splits into closed items resolved by operator
  ruling (A2, A3, A7) and open items requiring a ruling (E1, E2, E5, G6).

## 7. Most Consequential Findings (top five)

1. **E1 — RTA binary format is triply inconsistent.** The RTA whitepaper
   specifies `RTNZ` magic with a header/index/value/reference layout
   (§3.1); the implementation ships the v1.3 `RTATNSR\0` layout with a
   completely different section order and encoding set; the operator Python
   reference implements neither and serializes JSON. Anyone writing an RTA
   interoperability claim must first obtain an operator ruling on which wire
   format is canonical. This matrix records the v1.3 layout as the de facto
   standard because it is the only one with executable proof.
2. **E7 — Recursive references are structural only.** RTA reference blocks
   round-trip with CRC protection but are never evaluated: no code resolves a
   Direct/Transformed/Fractal reference during reconstruction or operations.
   Combined with E15 (the `RecursiveTensor` reconstruct path returns a
   dimension envelope, `src/model.cpp:386-403`), the RTA runtime is a
   structure-and-operations layer, not a self-referential value system yet.
3. **B10 — The whitepaper's largest section has zero implementation surface.**
   Self-modification framework §6 (~1900 lines of authority text: interface,
   self-optimizer, security manager, audit system) maps to nothing beyond a
   skippable TLV chunk type. Any completion claim covering "the LQT
   whitepaper" as a whole is unsupportable while this stands.
4. **E10/E11/E9 — The pattern subsystem the RTA theory leans on does not
   exist.** Pattern matching, pattern extraction/replacement, and scale
   transforms are absent in C++ **and** in the operator's own Python
   reference. The whitepaper presents them as core RTA capabilities; they
   have no reference implementation anywhere in the archive.
5. **D3 — Signed edit logs are structural theater.** The SIGNED_EDITS flag
   and signature bytes exist, tests exercise the CRC chain, but no
   cryptographic signing or verification exists. For a format whose
   self-modification story depends on tamper-evident audit, this is the
   security gap most likely to be mistaken for coverage.

## 8. Whitepaper vs. Operator Python Reference — Recorded Contradictions

| ID | Whitepaper clause | Operator Python behavior | Disposition |
|---|---|---|---|
| W-1 | Main whitepaper §2.2: header 32 bytes | `lqt_library.py:29` `LQT_HEADER_SIZE = 32` (with the same three-uint64-offset contradiction latent in its own struct writes) | Implementation follows ruling D-001 (36). Python writer is internally inconsistent; do not use it as the wire authority |
| W-2 | RTA whitepaper §3.1: "Rank (1 byte): always 5" | `recursive_tensor.py:97` defaults `rank=4`; rank is parameterized | C++ enforces 5 per spec. Python's rank-4 default is a reference-flexibility choice, not a wire statement; flag to operator if cross-language fixtures ever serialize rank |
| W-3 | RTA whitepaper §4.4: pattern matching/extraction as native operations | No such methods exist on `RecursiveTensor` (verified by symbol search) | Whitepaper overstates the reference; E10/E11 stand as absent in both |
| W-4 | RTA whitepaper §3.1 `RTNZ` binary format | `RecursiveTensor.serialize()` emits versioned JSON dicts (`recursive_tensor.py:1510-1558`) | The RTA binary spec has no reference implementation at all; only the C++ v1.3 layout is executable proof |
| W-5 | Whitepaper descriptor omits `tensor_type` | `lqt_library.py:78` includes `tensor_type: int` with the 0/1 logic switch | Whitepaper prose loses to both implementations; D-005 stands |

## 9. What This Matrix Does Not Claim

- No clause classified IMPLEMENTED is claimed complete beyond the specific
  sub-clauses named in its evidence cell.
- The substrate (`autodidactic-learning-substrate/`, byte-identically twinned
  at `iala/` — see `docs/TRIAXIAL_ARCHITECTURE.md` §7 for the duplication
  ruling) is classified only where triaxial integration clauses demand it;
  its internal theorem pipeline has its own evidence surface and is not
  re-audited here.
- Whitepaper benchmark numbers are quoted nowhere as results.

## 10. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-21 | Initial clause matrix from whitepaper intake. 80 clauses classified. |
