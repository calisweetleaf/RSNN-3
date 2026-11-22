# LQT/RTA authority matrix

**Status:** initial source-grounded matrix, 2026-09-20

**Authority order:** the imported LQT documents in `docs/authority/` define the
format intent; the tested Python reference remains the mathematical authority
when available; this C++ tree is the production rewrite under review. A symbol
or comment alone is not implementation proof.

| Authority claim | Current evidence | Classification | Next disposition |
|---|---|---|---|
| `LQT1`/`LQTF` magic and v1.3 header/footer fields | `include/lqt/format.h`, `header.h`, header tests | Implemented with deviation | Preserve D-001: three 64-bit offsets require a 36-byte header although the authority also says 32 bytes. |
| Extensible TLV metadata with 4-byte value alignment | `include/lqt/tlv.h`, `src/tlv.cpp`, TLV/container tests | Implemented locally | Add byte-level fixtures against the reference. |
| Standard vs `RecursiveTensor` descriptor switch | `TensorType` and descriptor serialization | Implemented structurally | Keep recursive model semantics separate from descriptor routing. |
| Codebook + scale + delta + sparse-mask reconstruction | `reconstruct.cpp`, model mutation and round-trip tests | Implemented locally | Expand cross-language fixture proof. |
| Rank-5 RTA block with `RTATNSR\0`, dimensions, references, and CRC-64 | `rta.h`, `rta.cpp`, RTA tests | Implemented structurally | Verify exact Python wire compatibility, not only C++ round-trip. |
| All six RTA sparse encodings | RTA builders/parsers and `test_rta.cpp` | Implemented locally | Add malformed-input and cross-language cases. |
| Direct, transformed, and fractal reference blocks | `RtaReference`, parser/serializer, RTA tests | Implemented structurally | Establish whether references must be evaluated during reconstruction. |
| 5D project/contract/fractal operations | `rta_ops.*`, `test_rta_ops.cpp` | Implemented as separate operations | Compare numerical semantics with the Python reference. |
| Recursive-weight quintuple `{B, Φ, R, T, ε}` | `recursive_weight.*`, dedicated tests | Partial / formula selected by design | Reconcile scalar operator and recursion semantics against the authority. |
| `LqtModel::reconstruct()` for `RecursiveTensor` | `src/model.cpp:386-401` explicitly returns repeated dimension sizes | Partial, known gap | Replace with defined value reconstruction or formally make the API structural-only for RTA tensors. |
| Module DAG, hot swap, and zero-copy runtime evolution | JSON graph persistence, module mutation, transaction and concurrency tests | Partial | Prove executable DAG semantics and atomic runtime swap behavior; do not claim O(1) hot swapping from storage alone. |
| Four mutation constraints and sandboxed atomic trials | `mutation.*`, `transaction.h`, mutation/rollback tests | Implemented locally | Add quota policy only if required by the release boundary. |
| Reader-writer lock, double buffer, and mmap surface | `concurrency.h`, `mmap.h`, seven concurrency tests; repair in `4ad12d1` | Implemented locally | Compare fairness semantics to the authority and add file fixtures if required. |
| Big-endian portability | `BigEndianByteReader`; writer remains little-endian | Partial | Implement endian-aware writing/materialization or bound release to little-endian writers. |
| Cryptographic signed edit logs | `SIGNED_EDITS` flag and opaque signature bytes; CRC chain only | Partial / crypto absent | Keep out of v0.1 only with an explicit deviation, otherwise implement verification and key policy. |
| Compressed sections | `COMPRESSED` flag exists; no compressor/decompressor | Absent | Keep unsupported and documented, or implement the specified codec. |
| Published memory, speed, sparsity, and perplexity numbers | Authority documents only; no benchmark artifact in repo | Unverified | Do not repeat as implementation results until reproducible evidence exists. |

## Immediate next packet

1. Locate or materialize the tested Python LQT/RTA/RWA reference.
2. Build byte-level fixtures for the header, TLV, standard reconstruction, and
   RTA block formats.
3. Resolve the `RecursiveTensor` model contract before changing its code path.
4. Re-run the full gate and commit only proof-required changes.

The customizable LQT format remains primary. RTA remains a typed, distinct
subsystem; this matrix does not collapse the two lineages.
