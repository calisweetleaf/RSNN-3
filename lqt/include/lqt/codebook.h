// lqt/codebook.h — Vector-quantization codebooks (FP16 storage).
//
// Council module: A3 (descriptors + codebooks + reconstruction), LEAD.
// Canon: lqt.md §2.5 (Codebooks), §3.2 (Hierarchical Codebooks).
//
// On-disk block (canon §2.5):
//   codebook_id (u16) | num_vectors (u16) | vector_dim (u16)
//   | float16[num_vectors * vector_dim]  (4-byte aligned within the block)
//
// In memory we hold decoded FP32 for fast lookup and editing; serialization
// re-encodes to FP16.
//
// DESIGN DECISION D-006: canon §2.5 lists codebook "types" (global / local /
// hierarchical / expandable) but the block layout stores no type byte. We treat
// global/local as a model-level role (which tensors reference the codebook),
// hierarchical as a distinct composed type (HierarchicalCodebook below), and
// "expandable" as the ability to grow num_vectors at runtime (expand()).
#pragma once

#include <cstdint>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

class Codebook {
public:
    Codebook() = default;
    Codebook(uint16_t id, uint16_t num_vectors, uint16_t vector_dim)
        : id_(id), num_vectors_(num_vectors), vector_dim_(vector_dim),
          data_(static_cast<size_t>(num_vectors) * vector_dim, 0.0f) {}

    uint16_t id() const { return id_; }
    uint16_t num_vectors() const { return num_vectors_; }
    uint16_t vector_dim() const { return vector_dim_; }
    bool is_scalar() const { return vector_dim_ == 1; }

    const std::vector<float>& data() const { return data_; }
    std::vector<float>& data() { return data_; }

    // Pointer to the vector_dim floats for entry `index` (bounds-checked).
    const float* vector(uint32_t index) const {
        if (index >= num_vectors_) throw FormatError("Codebook::vector index out of range");
        return data_.data() + static_cast<size_t>(index) * vector_dim_;
    }
    // Scalar value of entry `index` (requires vector_dim == 1).
    float scalar(uint32_t index) const {
        if (vector_dim_ != 1) throw FormatError("Codebook::scalar on non-scalar codebook");
        return *vector(index);
    }

    // Mutation: overwrite entry `index` with vector_dim floats (codebook edit).
    void set_vector(uint32_t index, const float* vec) {
        if (index >= num_vectors_) throw ValidationError("Codebook::set_vector index out of range");
        float* dst = data_.data() + static_cast<size_t>(index) * vector_dim_;
        for (uint16_t j = 0; j < vector_dim_; ++j) dst[j] = vec[j];
    }
    void set_scalar(uint32_t index, float value) { set_vector(index, &value); }

    // Expandable codebook: append `added` zero-initialized entries.
    void expand(uint16_t added) {
        const uint32_t total = static_cast<uint32_t>(num_vectors_) + added;
        if (total > 0xFFFFu) throw ValidationError("Codebook::expand exceeds u16 capacity");
        num_vectors_ = static_cast<uint16_t>(total);
        data_.resize(static_cast<size_t>(num_vectors_) * vector_dim_, 0.0f);
    }

    void serialize(ByteWriter& w) const;            // emits FP16, 4B-aligned data
    static Codebook parse(ByteReader& r);            // throws FormatError

private:
    uint16_t id_ = 0;
    uint16_t num_vectors_ = 0;
    uint16_t vector_dim_ = 1;
    std::vector<float> data_; // size = num_vectors_ * vector_dim_
};

// Hierarchical codebook (canon §3.2): weight = primary[i_p] + residual[i_r]*rs.
struct HierarchicalCodebook {
    Codebook primary;
    Codebook residual;
    float residual_scale = 1.0f;

    // Reconstruct one scalar from a primary + residual index pair.
    float value(uint32_t primary_index, uint32_t residual_index) const {
        return primary.scalar(primary_index) +
               residual.scalar(residual_index) * residual_scale;
    }
};

} // namespace lqt
