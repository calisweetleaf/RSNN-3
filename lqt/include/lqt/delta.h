// lqt/delta.h — Delta buffer: per-element residual corrections applied after
//               codebook reconstruction.
//
// Council module: A4 (delta buffers and sparse masks).
// Canon: lqt.md §2.6 (Delta Buffers), §3.1 (reconstruction formula).
//
// DESIGN DECISION A4-DD-1: delta datatype byte codes.
//   On-disk datatype field (uint8) in the delta block header:
//     0x00 = FP16 (half-precision, 2 bytes/element)
//     0x01 = FP32 (single-precision, 4 bytes/element)
//   These codes occupy the low 6 bits. The high two bits are flag bits:
//     bit 7 (0x80) = SPARSE flag. When set, values section stores [u32 index][f16|f32 value]
//                    interleaved pairs instead of a flat value array.
//   Canon §2.6 does not assign explicit datatype codes for delta; this mapping
//   is chosen to match the DType enum (DType::FP16=1, DType::FP32=0) but note
//   that the on-disk delta datatype byte uses its OWN numbering (0=FP16, 1=FP32)
//   to keep the on-disk block as compact as possible (FP16 is the common case).
//
// DESIGN DECISION A4-DD-2: sparse delta layout.
//   Canon §2.6 specifies the header but does not prescribe sparse storage.
//   We encode sparse deltas by setting bit 7 of the datatype byte (SPARSE flag).
//   After the 4-byte-aligned header, the data section contains `num_elements`
//   [u32 index, fp16|fp32 value] pairs (index first, then value, no alignment
//   padding between pairs within the section). Total count of pairs equals
//   num_elements. The 4-byte alignment of the whole block is achieved by
//   pad_to(LQT_ALIGN_DELTA) after all pairs are written.
//
// Reconstruction formula (canon §3.1):
//   weight[i] = codebook[idx]*scale + delta[i]    (dense)
//   weight[indices[k]] += values[k]               (sparse, k in [0, values.size()) )

#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ---------------------------------------------------------------------------
// DeltaBuffer
// ---------------------------------------------------------------------------
// Stores residual delta corrections for a tensor. Internally, all values are
// kept as float (fp32). Serialization converts to the chosen on-disk dtype.
struct DeltaBuffer {
    uint16_t             delta_id{0};
    DType                dtype{DType::FP16};  // FP16 or FP32 on disk
    bool                 sparse{false};

    // Dense mode: values[i] is the correction for weight element i.
    // Sparse mode: values[k] is the correction for weight element indices[k].
    std::vector<float>    values;
    std::vector<uint32_t> indices;  // only meaningful when sparse == true

    // Serialize this delta block into w. Pads to LQT_ALIGN_DELTA.
    void serialize(ByteWriter& w) const;

    // Parse a delta block from r. Reads exactly the bytes written by serialize().
    static DeltaBuffer parse(ByteReader& r);

    // Apply corrections to a weight array of length n.
    //   Dense:  weights[i] += values[i]  for i in [0, n)
    //   Sparse: weights[indices[k]] += values[k]  for k in [0, values.size())
    // Throws ValidationError if any index >= n, or if dense and values.size() != n.
    void apply(float* weights, size_t n) const;
};

} // namespace lqt
