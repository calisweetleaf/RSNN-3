# LQT — Liquid Quantized Format, Reference Library

LQT is a post-quantization editable container format: once a model is quantized and packed into an LQT file, codebooks can be revised, delta buffers injected, modules hot-swapped, and sparsity masks updated — all without decompressing and re-quantizing the entire model. Every mutation is validated, logged to a tamper-evident append-only edit log, and executed atomically. This is our v0.1 C++17 reference implementation of the LQT v1.3 binary format.

Compare to GGUF and ONNX: they offer no post-quantization edits, no hot-swap infrastructure, no audit trail. LQT fills that gap with native mutation safety, reader-preference concurrency, and a 5-D Recursive Tensor Architecture for complex model topologies.

---

## Architecture

We organized the reference library into ten modules (A1–A10):

- **A1 Container**: Header/footer parsing, whole-file CRC-32, little-endian byte cursors, FP16↔FP32 conversion.
- **A2 TLV Metadata**: Type-Length-Value chunk registry, unknown-type forward-skip, codebook/delta/mask tables, JSON hyperparams.
- **A3 Reconstruction**: Tensor descriptors, FP16 codebooks (scalar/vector/hierarchical/expandable), INT4/8/16/32 unpacking, multi-stage formula.
- **A4 Delta & Mask**: FP16/FP32 dense and sparse deltas, bitmap and RLE sparse masks with bitmap-first layout.
- **A5 RTA**: 5-D Recursive Tensor Architecture, rank-5 enforced, all six sparse encodings, per-block CRC-64 integrity.
- **A6 Recursive Weights**: Quintuple {B, Phi, R, T, epsilon}, harmonic phase computation, full-precision reconstruction.
- **A7 Mutation**: CRC-32–chained edit log, 4-constraint validator (dimensions/bounds/topology/access), atomic Transaction with rollback.
- **A8 Concurrency**: Reader-preference ReaderWriterLock, lock-free DoubleBuffer hot-swap, POSIX mmap zero-copy.
- **A10 Integration**: LqtModel: container assembly, parsing, whole-file CRC-32 verification, tensor reconstruction by name.

---

## Binary Format at a Glance

| Region | Size | Contents |
|---|---|---|
| FileHeader | 36 bytes | Magic, version 0x0103, offsets (uint64 × 3), flags, CRC-32 space |
| TLV Metadata | Variable | Self-delimiting length + chunks (hyperparams, module graph, tables) |
| Codebooks | 64B-aligned | Scalar/vector/hierarchical codebooks, FP16 storage, mutable in-place |
| Tensors | Variable | Packed quantized indices (dtype-dependent), contiguous from tensor_offset |
| Deltas | 4B-aligned | FP16/FP32 dense/sparse buffers, per-tensor linked by delta_id |
| Sparse Masks | 4B-aligned | Bitmap (LSB-first) or RLE (uint16 run lengths) per-tensor masks |
| FileFooter | 64 bytes | Offsets, CRC-32 checksum (whole-file with footer bytes zeroed), reserved |

---

## Quick Start

### Repository operator entrypoint

For an arriving implementation agent, read `AGENTS.md`, `TASK.md`,
`CONTEXT.md`, and `filetree.md`, then run:

```sh
./scripts/gate.sh
```

The gate uses CMake/CTest when available and falls back to the documented GCC
static-library pattern when CMake is unavailable. It must be treated as the
current evidence source; the historical reports below are not a substitute for
running it.

**Build the library:**
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build -j
```

**Run tests:**
```sh
ctest --test-dir build --output-on-failure
```

The supplied archive's historical reports say 119 cases pass. The current
source tree contains 237 registered tests across 21 test binaries; after a
reader-writer lost-wakeup repair, the 2026-09-20 manual gate passed all 237.
See `docs/REPO_AUDIT_2026-09-20.md` for the evidence boundary.

---

## Usage Examples

**Write and save a model:**
```cpp
LqtModel m;
m.set_hyperparam("hidden_size", 768.0f);

Codebook cb(0, 256, 1);
for (int i = 0; i < 256; ++i) cb.set_scalar(i, i * 0.01f);
m.add_codebook(cb);

TensorDescriptor d;
d.name = "layer0.weight";
d.dtype = DType::INT8;
d.shape = {4, 4};
d.codebook_id = 0;
d.scale = 1.0f;
std::vector<uint8_t> indices(16);
for (int i = 0; i < 16; ++i) indices[i] = i * 16;

m.add_tensor(std::move(d), std::move(indices));
m.save("/tmp/demo.lqt");
```

**Load and reconstruct:**
```cpp
LqtModel m = LqtModel::load("/tmp/demo.lqt");
std::vector<float> weights = m.reconstruct("layer0.weight");
// weights[i] = codebook[indices[i]] * scale
```

**Mutate with validation and edit log:**
```cpp
LqtModel m = LqtModel::load("/tmp/example.lqt");
Codebook* cb = m.codebook_mut(0);

MutationValidator validator(-8.0f, 8.0f);
ValidationResult vb = validator.check_value_bounds(&new_value, 1);
if (vb.ok) {
    cb->set_scalar(0, new_value);
    EditLog log;
    EditLogEntry e = make_entry(MutationType::CodebookEdit, "codebook[0][0]",
                                &new_value, sizeof(new_value), log.tail_hash());
    log.append(e);
    m.save("/tmp/mutated.lqt");
}
```

---

## Implemented

- Binary container layout (header, footer, TLV metadata, aligned codebook/tensor/delta/mask regions)
- All standard reconstruction paths (INT4/8/16/32 unpacking, codebook lookup, scale, delta, mask)
- 5-D RTA standalone modules with all six sparse encodings and per-block CRC-64
- Recursive weight quintuple and harmonic phase computation
- Full edit-log framework: tamper-evident chaining, 4-constraint validator, atomic transactions
- Concurrency: reader-preference RWLock, lock-free DoubleBuffer, mmap zero-copy
- Complete in-memory and on-disk round-trip with CRC-32/CRC-64 verification
- **237 test cases across 21 binaries, all passing in the current manual gate**

---

## Known Gaps in v0.1

- **Big-endian write path**: byte-swap helpers exist; full BE materialization on read is not wired.
- **Edit-log crypto signatures**: SIGNED_EDITS flag and signature bytes are carried; asymmetric signing is out of scope.
- **Section compression**: COMPRESSED flag is carried; decompression is not implemented.
- **Multi-file sharding**: SHARDED flag is carried; single-file loader only.
- **RTA embedding in LqtModel**: A5/A6 modules complete and tested standalone; integration into model reconstruction is next.
- **EditLog persistence**: fully implemented; not yet written as 0x000B chunk by LqtModel.save.
- **Affine-only tensors**: dequant_affine helper exists; model.reconstruct requires a linked codebook.
- **SIMD reconstruction**: reference scalar implementation only; no AVX2/NEON paths.

---

## Deviation Register

| ID | Summary | Rationale |
|---|---|---|
| D-001 | Header size 36 bytes | Canon contradicts itself (32 vs. 36); uint64 offsets run to byte 36; files >4 GiB are real (7B model = 4.0 GB) |
| D-002 | Version 0x0103 (8-bit/8-bit major/minor) | Self-documenting in hex dump; symmetric; avoids 16-major-version ceiling |
| D-003 | DType codes FP32=0…INT32=7 | Canon lists no codes; assignment is conventional |
| D-004 | Whole-file CRC-32 with footer bytes zeroed | Canon gives no checksum-field treatment; only self-consistent option |
| D-005 | Tensor descriptor includes tensor_type field | Canon omits it; v1.3 spec includes it as "Logic Switch"; load-bearing for routing |
| D-006 | Codebook type is model-level role, not on-disk byte | Canon lists types but block carries no byte; modeled as role + composed types |
| D-007 | INT4 packing: low nibble first | Canon silent on nibble order; element 2k = low nibble of byte k |
| D-008 | Codebook id sentinel 0xFFFF | Disambiguates "no link" from valid id 0 |
| D-009 | Tensor blobs contiguous from tensor_offset | Canon defines no offset table; walked sequentially in descriptor order |
| D-010 | TensorDescriptors chunk framed with count | Canon gives no multi-descriptor framing; count prefix required |
| D-011 | Metadata region self-delimiting (u64 length prefix) | Header carries only region offsets; codebooks sit between metadata and tensors |
| D-012 | Delta datatype codes 0=FP16, 1=FP32 | Independent of DType enum; canon specifies only FP16/FP32 for deltas |
| D-013 | Sparse-delta flag = bit 7 (0x80) of datatype byte | Leaves room for other flags in bits 0–6 |
| D-014 | num_elements is uint24 (3 bytes) | Per canon section 2.6 |
| D-015 | Sparse mask: CompressedBitmap LSB-first per byte | Aligns with common hardware bitmap conventions |
| D-016 | RTA dimension block 24 bytes + five uint32 sizes (44 total) | Spec mandate + documented extension; five sizes = d0…d4 |
| D-017 | RTA reference block: Direct/Transformed/Fractal kinds | Spec-defined; Transformed appends matrix; Fractal appends iteration params |
| D-018 | Per-block CRC-64 (XZ) over all preceding block bytes | Integrity check before unpacking |

---

## License

LQT Reference Implementation is released under the MIT License.
