// lqt/src/descriptor.cpp — Tensor Descriptor (de)serialization + validation.
#include "lqt/descriptor.h"

namespace lqt {

uint64_t TensorDescriptor::element_count() const {
    if (shape.empty()) return 0;
    uint64_t n = 1;
    for (uint32_t d : shape) n *= static_cast<uint64_t>(d);
    return n;
}

void TensorDescriptor::serialize(ByteWriter& w) const {
    if (shape.size() > 0xFF) {
        throw FormatError("TensorDescriptor: ndim exceeds 255");
    }
    w.put_string(name);
    w.put_u8(static_cast<uint8_t>(tensor_type));
    w.put_u8(static_cast<uint8_t>(dtype));
    w.put_u8(static_cast<uint8_t>(shape.size()));
    for (uint32_t d : shape) w.put_u32(d);
    w.put_u16(codebook_id);
    w.put_u16(delta_id);
    w.put_u16(sparse_mask_id);
    w.put_f32(scale);
    w.put_i32(zero_point);
    w.put_u16(flags);
}

TensorDescriptor TensorDescriptor::parse(ByteReader& r) {
    TensorDescriptor d;
    d.name        = r.get_string();
    d.tensor_type = static_cast<TensorType>(r.get_u8());
    d.dtype       = static_cast<DType>(r.get_u8());
    const uint8_t ndim = r.get_u8();
    d.shape.resize(ndim);
    for (uint8_t i = 0; i < ndim; ++i) d.shape[i] = r.get_u32();
    d.codebook_id    = r.get_u16();
    d.delta_id       = r.get_u16();
    d.sparse_mask_id = r.get_u16();
    d.scale          = r.get_f32();
    d.zero_point     = r.get_i32();
    d.flags          = r.get_u16();
    d.validate();
    return d;
}

void TensorDescriptor::validate() const {
    if (tensor_type != TensorType::Standard &&
        tensor_type != TensorType::RecursiveTensor) {
        throw FormatError("TensorDescriptor: invalid tensor_type");
    }
    // Recursive tensors carry rank-5 semantics in the linked RTA block; the
    // descriptor shape for a recursive tensor must therefore be rank 5.
    if (tensor_type == TensorType::RecursiveTensor && shape.size() != LQT_RTA_RANK) {
        throw FormatError("TensorDescriptor: RecursiveTensor must have rank 5");
    }
}

} // namespace lqt
