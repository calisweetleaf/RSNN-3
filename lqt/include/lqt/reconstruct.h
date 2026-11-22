// lqt/reconstruct.h — multi-stage quantized weight reconstruction.
//
// Council module: A3 (descriptors + codebooks + reconstruction), LEAD.
// Canon: lqt.md §3.1 (Quantized Weight Reconstruction), §3.2 (Hierarchical),
//        §2.4 (index storage: INT4 2/byte, INT8 1/byte).
//
// Canonical formula (§3.1):
//   weight[i] = codebook[codebook_id][indices[i]] * scale + delta[delta_id][i]
//   if sparse mask present:  weight[i] *= mask[i]
//
// Delta and mask are passed as raw pointers so this module stays independent of
// the delta/sparse-mask module (built concurrently by operator MASON); the
// model-integration layer wires DeltaBuffer::apply / SparseMask::apply on top.
#pragma once

#include <cstdint>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/descriptor.h"
#include "lqt/format.h"

namespace lqt {

// Unpack packed quantized indices into u32 index values.
//   INT4  -> 2 indices/byte, low nibble first (DESIGN DECISION D-007).
//   INT8/UINT8 -> 1 byte each; INT16 -> 2 bytes LE; INT32 -> 4 bytes LE.
// `count` is the number of indices to produce.
std::vector<uint32_t> unpack_indices(const uint8_t* data, size_t data_len,
                                     size_t count, DType index_dtype);

// Exact inverse of unpack_indices: pack u32 indices into the on-disk index
// layout for `index_dtype` (INT4 low nibble first, odd tail's high nibble 0;
// INT8/UINT8 1 byte; INT16/INT32 little-endian). Throws ValidationError if an
// index does not fit the dtype, FormatError if the dtype is not an index type.
std::vector<uint8_t> pack_indices(const std::vector<uint32_t>& indices, DType index_dtype);

// Standard reconstruction. Output length = indices.size() * codebook.vector_dim.
// `delta`     : optional, length == output length (per-weight additive); may be null.
// `mask_bits` : optional, LSB-first bitfield length >= output length; may be null.
std::vector<float> reconstruct_standard(const Codebook& cb,
                                        const std::vector<uint32_t>& indices,
                                        float scale,
                                        const float* delta = nullptr,
                                        const uint8_t* mask_bits = nullptr);

// Hierarchical reconstruction (§3.2): primary[i_p] + residual[i_r]*residual_scale,
// then * scale, + optional delta, * optional mask. Scalar codebooks only.
std::vector<float> reconstruct_hierarchical(const HierarchicalCodebook& hcb,
                                            const std::vector<uint32_t>& primary_idx,
                                            const std::vector<uint32_t>& residual_idx,
                                            float scale,
                                            const float* delta = nullptr,
                                            const uint8_t* mask_bits = nullptr);

// Affine dequantization for codebook-less INT tensors: (q - zero_point) * scale.
inline float dequant_affine(int64_t q, float scale, int32_t zero_point) {
    return static_cast<float>(q - zero_point) * scale;
}

// Bulk affine dequantization dispatched through SIMD kernels (see lqt/simd.h).
// Reads desc.dtype, desc.scale, and desc.zero_point; routes INT4/INT8 through
// simd::dequant_int4 / simd::dequant_int8 respectively.
// `indices` must hold the packed on-disk bytes (INT4: 2/byte, INT8: 1/byte).
// Returns a vector of desc.element_count() floats.
std::vector<float> dequant_affine(const TensorDescriptor& desc,
                                   const std::vector<uint8_t>& indices);

// Read bit `i` from an LSB-first bitfield.
inline bool mask_bit(const uint8_t* bits, size_t i) {
    return (bits[i >> 3] >> (i & 7u)) & 1u;
}

} // namespace lqt
