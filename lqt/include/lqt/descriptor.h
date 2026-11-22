// lqt/descriptor.h — Tensor Descriptor (the reconstruction logic switch).
//
// Council module: A3 (descriptors + codebooks + reconstruction), LEAD.
// Canon: lqt.md §2.3 (Tensor Descriptor Format) + v1.3 spec §3 (Tensor Descriptor).
//
// DESIGN DECISION D-005: canon §2.3's descriptor field list omits tensor_type,
// but the v1.3 spec §3 lists it as field #2 (right after name) and calls it
// "The Logic Switch" (0 = Standard, 1 = RecursiveTensor). tensor_type is
// load-bearing — it routes reconstruction between the standard codebook path
// and the RTA path — so we INCLUDE it immediately after the name. Full on-disk
// descriptor layout (see SPEC_COMPLIANCE.md D-005):
//   [name:str][tensor_type:u8][dtype:u8][ndim:u8][shape:u32*ndim]
//   [codebook_id:u16][delta_id:u16][sparse_mask_id:u16]
//   [scale:f32][zero_point:i32][flags:u16]
#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// Sentinel meaning "no linked codebook/delta/mask" for the u16 id fields.
inline constexpr uint16_t LQT_ID_NONE = 0xFFFFu;

struct TensorDescriptor {
    std::string           name;
    TensorType            tensor_type    = TensorType::Standard;
    DType                 dtype          = DType::INT8;
    std::vector<uint32_t> shape;                       // ndim == shape.size()
    uint16_t              codebook_id    = LQT_ID_NONE;
    uint16_t              delta_id       = LQT_ID_NONE;
    uint16_t              sparse_mask_id = LQT_ID_NONE;
    float                 scale          = 1.0f;
    int32_t               zero_point     = 0;
    uint16_t              flags          = 0;

    // Number of logical elements (product of shape dims; 0 if shape empty).
    uint64_t element_count() const;

    bool is_recursive()  const { return tensor_type == TensorType::RecursiveTensor; }
    bool has_codebook()  const { return codebook_id    != LQT_ID_NONE; }
    bool has_delta()     const { return delta_id       != LQT_ID_NONE; }
    bool has_mask()      const { return sparse_mask_id != LQT_ID_NONE; }

    bool has_flag(TensorFlag f) const { return flag_set(flags, f); }
    void set_flag(TensorFlag f, bool on = true) { flag_assign(flags, f, on); }

    void serialize(ByteWriter& w) const;
    static TensorDescriptor parse(ByteReader& r);   // throws FormatError
    void validate() const;                          // throws FormatError
};

} // namespace lqt
