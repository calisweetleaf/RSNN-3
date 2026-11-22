// lqt/src/reconstruct.cpp — multi-stage reconstruction implementation.
#include "lqt/reconstruct.h"

#include "lqt/error.h"
#include "lqt/simd.h"

namespace lqt {

std::vector<uint8_t> pack_indices(const std::vector<uint32_t>& indices, DType index_dtype) {
    std::vector<uint8_t> out;
    auto check_max = [&](uint32_t maxv, const char* what) {
        for (uint32_t v : indices) {
            if (v > maxv) throw ValidationError(std::string("pack_indices: index exceeds ") + what + " range");
        }
    };
    switch (index_dtype) {
        case DType::INT4: {
            check_max(0x0Fu, "INT4");
            out.assign((indices.size() + 1) / 2, 0);
            for (size_t i = 0; i < indices.size(); ++i) {
                const uint8_t nib = static_cast<uint8_t>(indices[i] & 0x0Fu);
                out[i >> 1] = static_cast<uint8_t>(out[i >> 1] | ((i & 1u) ? (nib << 4) : nib));
            }
            break;
        }
        case DType::INT8:
        case DType::UINT8: {
            check_max(0xFFu, "INT8/UINT8");
            out.reserve(indices.size());
            for (uint32_t v : indices) out.push_back(static_cast<uint8_t>(v));
            break;
        }
        case DType::INT16: {
            check_max(0xFFFFu, "INT16");
            out.reserve(indices.size() * 2);
            for (uint32_t v : indices) {
                out.push_back(static_cast<uint8_t>(v & 0xFFu));
                out.push_back(static_cast<uint8_t>((v >> 8) & 0xFFu));
            }
            break;
        }
        case DType::INT32: {
            out.reserve(indices.size() * 4);
            for (uint32_t v : indices) {
                for (int b = 0; b < 4; ++b) out.push_back(static_cast<uint8_t>((v >> (8 * b)) & 0xFFu));
            }
            break;
        }
        default:
            throw FormatError("pack_indices: dtype is not an index type");
    }
    return out;
}

std::vector<uint32_t> unpack_indices(const uint8_t* data, size_t data_len,
                                     size_t count, DType index_dtype) {
    std::vector<uint32_t> out;
    out.reserve(count);
    switch (index_dtype) {
        case DType::INT4: {
            const size_t need_bytes = (count + 1) / 2;
            if (data_len < need_bytes) throw FormatError("unpack_indices: INT4 buffer too small");
            for (size_t i = 0; i < count; ++i) {
                const uint8_t byte = data[i >> 1];
                const uint8_t nib = (i & 1u) ? (byte >> 4) : (byte & 0x0F); // low nibble first
                out.push_back(nib);
            }
            break;
        }
        case DType::INT8:
        case DType::UINT8: {
            if (data_len < count) throw FormatError("unpack_indices: INT8 buffer too small");
            for (size_t i = 0; i < count; ++i) out.push_back(data[i]);
            break;
        }
        case DType::INT16: {
            if (data_len < count * 2) throw FormatError("unpack_indices: INT16 buffer too small");
            for (size_t i = 0; i < count; ++i) {
                out.push_back(static_cast<uint32_t>(data[i * 2]) |
                              (static_cast<uint32_t>(data[i * 2 + 1]) << 8));
            }
            break;
        }
        case DType::INT32: {
            if (data_len < count * 4) throw FormatError("unpack_indices: INT32 buffer too small");
            for (size_t i = 0; i < count; ++i) {
                uint32_t v = 0;
                for (int b = 0; b < 4; ++b) v |= static_cast<uint32_t>(data[i * 4 + b]) << (8 * b);
                out.push_back(v);
            }
            break;
        }
        default:
            throw FormatError("unpack_indices: dtype is not an index type");
    }
    return out;
}

std::vector<float> reconstruct_standard(const Codebook& cb,
                                        const std::vector<uint32_t>& indices,
                                        float scale,
                                        const float* delta,
                                        const uint8_t* mask_bits) {
    const uint16_t vd = cb.vector_dim();
    std::vector<float> out;
    out.resize(indices.size() * vd);

    size_t k = 0;
    for (uint32_t idx : indices) {
        const float* vec = cb.vector(idx); // bounds-checked
        for (uint16_t j = 0; j < vd; ++j, ++k) {
            float w = vec[j] * scale;
            if (delta) w += delta[k];
            if (mask_bits && !mask_bit(mask_bits, k)) w = 0.0f;
            out[k] = w;
        }
    }
    return out;
}

std::vector<float> reconstruct_hierarchical(const HierarchicalCodebook& hcb,
                                            const std::vector<uint32_t>& primary_idx,
                                            const std::vector<uint32_t>& residual_idx,
                                            float scale,
                                            const float* delta,
                                            const uint8_t* mask_bits) {
    if (primary_idx.size() != residual_idx.size()) {
        throw FormatError("reconstruct_hierarchical: index count mismatch");
    }
    std::vector<float> out;
    out.resize(primary_idx.size());
    for (size_t i = 0; i < primary_idx.size(); ++i) {
        float w = hcb.value(primary_idx[i], residual_idx[i]) * scale;
        if (delta) w += delta[i];
        if (mask_bits && !mask_bit(mask_bits, i)) w = 0.0f;
        out[i] = w;
    }
    return out;
}

std::vector<float> dequant_affine(const TensorDescriptor& desc,
                                   const std::vector<uint8_t>& indices) {
    const size_t n = static_cast<size_t>(desc.element_count());
    std::vector<float> out(n);
    const float scale       = desc.scale;
    const float zero_point  = static_cast<float>(desc.zero_point);
    if (desc.dtype == DType::INT4) {
        simd::dequant_int4(out.data(), indices.data(), n, scale, zero_point);
    } else if (desc.dtype == DType::INT8) {
        simd::dequant_int8(out.data(),
                           reinterpret_cast<const int8_t*>(indices.data()),
                           n, scale, zero_point);
    } else {
        // FP32/FP16 stored as raw bytes — apply affine scale per byte.
        for (size_t i = 0; i < n; ++i) {
            out[i] = static_cast<float>(indices[i]) * scale + zero_point;
        }
    }
    return out;
}

} // namespace lqt
