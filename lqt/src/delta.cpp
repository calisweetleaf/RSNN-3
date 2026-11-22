// src/delta.cpp — Implementation of DeltaBuffer serialization, parsing, and
//                 application.
//
// Council module: A4 (delta buffers and sparse masks).
// Canon: lqt.md §2.6 (Delta Buffers), §3.1 (reconstruction formula).
//
// On-disk layout (§2.6, little-endian):
//   delta_id     : uint16   — identifies the delta block
//   datatype     : uint8    — bits[5:0] dtype code (0=FP16, 1=FP32)
//                             bit 7 (0x80) = SPARSE flag (A4-DD-1, A4-DD-2)
//   num_elements : uint24   — number of elements (dense) or pairs (sparse)
//   <pad to LQT_ALIGN_DELTA=4 if header is not already aligned>
//   values data  : see below, 4-byte aligned
//
// Dense layout:  [fp16 or fp32] x num_elements, then pad_to(4).
// Sparse layout: ([u32 index][fp16 or fp32 value]) x num_elements, then pad_to(4).

#include "lqt/delta.h"
#include "lqt/fp16.h"

#include <sstream>

namespace lqt {

// On-disk dtype codes (A4-DD-1): different from DType enum values.
static constexpr uint8_t DELTA_DTYPE_FP16   = 0x00;
static constexpr uint8_t DELTA_DTYPE_FP32   = 0x01;
static constexpr uint8_t DELTA_SPARSE_FLAG  = 0x80;
static constexpr uint8_t DELTA_DTYPE_MASK   = 0x3F;  // bits[5:0]

// ---------------------------------------------------------------------------
void DeltaBuffer::serialize(ByteWriter& w) const {
    // Validate
    if (sparse && values.size() != indices.size()) {
        throw ValidationError("DeltaBuffer::serialize: values and indices must have the same size in sparse mode");
    }
    if (values.size() > 0x00FFFFFFu) {
        throw ValidationError("DeltaBuffer::serialize: num_elements exceeds uint24 maximum (16777215)");
    }

    // Determine on-disk dtype code
    uint8_t dtype_code;
    if (dtype == DType::FP16) {
        dtype_code = DELTA_DTYPE_FP16;
    } else if (dtype == DType::FP32) {
        dtype_code = DELTA_DTYPE_FP32;
    } else {
        // DESIGN DECISION A4-DD-3: only FP16 and FP32 are supported for delta
        // buffers. Canon §2.6 mentions only these two. Any other DType is an error.
        throw ValidationError("DeltaBuffer::serialize: unsupported dtype (only FP16 and FP32 supported)");
    }

    if (sparse) {
        dtype_code |= DELTA_SPARSE_FLAG;
    }

    // Header: delta_id (u16) + datatype (u8) + num_elements (u24) = 6 bytes
    w.put_u16(delta_id);
    w.put_u8(dtype_code);
    w.put_u24(static_cast<uint32_t>(values.size()));

    // Pad header to 4-byte alignment (6 bytes -> pad 2 bytes to reach 8)
    // Actually the spec says values are 4-byte aligned. Header is 6 bytes.
    // We pad to LQT_ALIGN_DELTA so values start at a 4-byte boundary.
    // Note: pad_to operates on the writer's current total size, which includes
    // bytes written before this delta block. The canon specifies alignment of
    // the delta block as a whole at LQT_ALIGN_DELTA; callers are expected to
    // pad_to(LQT_ALIGN_DELTA) before writing the block. Within the block, we
    // ensure the values section is 4-byte aligned relative to block start by
    // padding after the 6-byte header to reach a 4-byte boundary from the
    // writer's perspective.
    // DESIGN DECISION A4-DD-4: We pad after the header so the values section
    // begins at a buffer offset that is a multiple of 4. This matches the spirit
    // of LQT_ALIGN_DELTA and simplifies SIMD-friendly reads on the parse side.
    w.pad_to(LQT_ALIGN_DELTA);

    // Values (and optional indices for sparse)
    if (!sparse) {
        // Dense: flat value array
        for (float v : values) {
            if (dtype == DType::FP16) {
                w.put_u16(fp32_to_fp16(v));
            } else {
                w.put_f32(v);
            }
        }
    } else {
        // Sparse: interleaved [u32 index][f16|f32 value] pairs
        for (size_t k = 0; k < values.size(); ++k) {
            w.put_u32(indices[k]);
            if (dtype == DType::FP16) {
                w.put_u16(fp32_to_fp16(values[k]));
            } else {
                w.put_f32(values[k]);
            }
        }
    }

    // Pad end of data section to 4-byte alignment
    w.pad_to(LQT_ALIGN_DELTA);
}

// ---------------------------------------------------------------------------
DeltaBuffer DeltaBuffer::parse(ByteReader& r) {
    DeltaBuffer db;

    // Header
    db.delta_id = r.get_u16();
    uint8_t dtype_byte = r.get_u8();
    uint32_t num_elements = r.get_u24();

    // Decode dtype and sparse flag
    db.sparse = (dtype_byte & DELTA_SPARSE_FLAG) != 0;
    uint8_t dtype_code = dtype_byte & DELTA_DTYPE_MASK;

    if (dtype_code == DELTA_DTYPE_FP16) {
        db.dtype = DType::FP16;
    } else if (dtype_code == DELTA_DTYPE_FP32) {
        db.dtype = DType::FP32;
    } else {
        std::ostringstream oss;
        oss << "DeltaBuffer::parse: unknown dtype code 0x" << std::hex
            << static_cast<unsigned>(dtype_code);
        throw FormatError(oss.str());
    }

    // Skip alignment padding after 6-byte header
    r.align_to(LQT_ALIGN_DELTA);

    // Read values (and indices for sparse)
    db.values.resize(num_elements);
    if (db.sparse) {
        db.indices.resize(num_elements);
        for (uint32_t k = 0; k < num_elements; ++k) {
            db.indices[k] = r.get_u32();
            if (db.dtype == DType::FP16) {
                db.values[k] = fp16_to_fp32(r.get_u16());
            } else {
                db.values[k] = r.get_f32();
            }
        }
    } else {
        for (uint32_t i = 0; i < num_elements; ++i) {
            if (db.dtype == DType::FP16) {
                db.values[i] = fp16_to_fp32(r.get_u16());
            } else {
                db.values[i] = r.get_f32();
            }
        }
    }

    // Consume end-of-data alignment padding
    r.align_to(LQT_ALIGN_DELTA);

    return db;
}

// ---------------------------------------------------------------------------
void DeltaBuffer::apply(float* weights, size_t n) const {
    if (!sparse) {
        // Dense mode: values.size() must equal n
        if (values.size() != n) {
            std::ostringstream oss;
            oss << "DeltaBuffer::apply (dense): values.size()=" << values.size()
                << " != n=" << n;
            throw ValidationError(oss.str());
        }
        for (size_t i = 0; i < n; ++i) {
            weights[i] += values[i];
        }
    } else {
        // Sparse mode: apply only at the stored indices
        for (size_t k = 0; k < values.size(); ++k) {
            if (indices[k] >= static_cast<uint32_t>(n)) {
                std::ostringstream oss;
                oss << "DeltaBuffer::apply (sparse): index " << indices[k]
                    << " >= n=" << n;
                throw ValidationError(oss.str());
            }
            weights[indices[k]] += values[k];
        }
    }
}

} // namespace lqt
