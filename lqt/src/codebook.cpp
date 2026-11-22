// lqt/src/codebook.cpp — codebook FP16 (de)serialization.
#include "lqt/codebook.h"

#include "lqt/fp16.h"

namespace lqt {

void Codebook::serialize(ByteWriter& w) const {
    const size_t start = w.size();
    w.put_u16(id_);
    w.put_u16(num_vectors_);
    w.put_u16(vector_dim_);
    // 4-byte align the FP16 vector data relative to the block start.
    const size_t header_bytes = w.size() - start; // == 6
    const size_t pad = (LQT_ALIGN_DELTA - (header_bytes % LQT_ALIGN_DELTA)) % LQT_ALIGN_DELTA;
    w.put_zeros(pad);
    for (float v : data_) {
        w.put_u16(fp32_to_fp16(v));
    }
}

Codebook Codebook::parse(ByteReader& r) {
    const size_t start = r.position();
    const uint16_t id = r.get_u16();
    const uint16_t num_vectors = r.get_u16();
    const uint16_t vector_dim = r.get_u16();
    // Mirror the writer's 4-byte alignment of the data section.
    const size_t header_bytes = r.position() - start; // == 6
    const size_t pad = (LQT_ALIGN_DELTA - (header_bytes % LQT_ALIGN_DELTA)) % LQT_ALIGN_DELTA;
    r.skip(pad);

    Codebook cb(id, num_vectors, vector_dim);
    const size_t n = static_cast<size_t>(num_vectors) * vector_dim;
    for (size_t i = 0; i < n; ++i) {
        cb.data_[i] = fp16_to_fp32(r.get_u16());
    }
    return cb;
}

} // namespace lqt
