// lqt/sparse_mask.h — SparseMask: binary weight mask for structural sparsity.
//
// Council module: A4 (delta buffers and sparse masks).
// Canon: lqt.md §2.4 (Tensor Data, sparse_mask_id), §3.1 (reconstruction:
//        weight[i] *= mask[i]); Binary Spec v1.3 §4 (sparse encodings).
//
// On-disk layout (§2.4 + v1.3 §4):
//   mask_id       : uint16
//   encoding_type : uint8  (SparseEncoding enum)
//   element_count : uint32
//   <pad to 4-byte alignment>
//   data          : encoding-specific (see below), padded to 4 bytes
//
// Supported encodings:
//
//   CompressedBitmap (SparseEncoding::CompressedBitmap, code 0x04):
//     Bits packed LSB-first within each byte.
//     Element i is in byte (i/8), bit (i%8).
//     Data length: ceil(element_count / 8) bytes, then pad_to(4).
//
//   RLE (SparseEncoding::RLE, code 0x03):
//     DESIGN DECISION A4-DD-5: RLE format.
//     Stores alternating run lengths as uint16 values, starting with a run
//     of 0-bits (zeros). Each uint16 gives the count of consecutive bits of
//     the current polarity. The first run may be zero (meaning the bit sequence
//     starts with a 1).  Runs continue alternating 0,1,0,1,... until
//     element_count bits have been described. A trailing run of the current
//     polarity may be omitted if its length is zero.
//     Example: bits = [0,0,1,1,1,0] -> runs = [2, 3, 1]
//              bits = [1,1,0]        -> runs = [0, 2, 1]
//     Data length: num_runs * sizeof(uint16), then pad_to(4).
//
// Reconstruction (canon §3.1):
//   weight[i] *= (bit(i) ? 1.0f : 0.0f)

#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ---------------------------------------------------------------------------
// SparseMask
// ---------------------------------------------------------------------------
struct SparseMask {
    uint16_t       mask_id{0};
    SparseEncoding encoding{SparseEncoding::CompressedBitmap};
    uint32_t       element_count{0};

    // Internal canonical storage: one bool per element (true = weight kept).
    // Constructed from std::vector<bool>, a raw bitfield, or via parse().
    std::vector<bool> bits;

    // Construct from a std::vector<bool>. encoding selects the on-disk format.
    // Only SparseEncoding::CompressedBitmap and SparseEncoding::RLE are supported.
    SparseMask() = default;
    SparseMask(uint16_t id, SparseEncoding enc, std::vector<bool> b);

    // Construct from a packed bitfield (LSB-first). element_count is the
    // number of valid bits; bytes = ceil(element_count/8).
    static SparseMask from_bitfield(uint16_t id, SparseEncoding enc,
                                    const uint8_t* data, uint32_t element_count);

    // Serialize to w. Pads to LQT_ALIGN_DELTA.
    void serialize(ByteWriter& w) const;

    // Parse from r.
    static SparseMask parse(ByteReader& r);

    // Return the value of bit i. Throws FormatError if i >= element_count.
    bool bit(size_t i) const;

    // Fraction of 1-bits in [0.0, 1.0].
    double density() const;

    // Apply mask to weights: weights[i] *= (bit(i) ? 1.0f : 0.0f).
    // n must equal element_count; throws ValidationError otherwise.
    void apply(float* weights, size_t n) const;

private:
    // Encode bits as a flat byte vector (LSB-first bitmap).
    std::vector<uint8_t> encode_bitmap() const;

    // Encode bits as RLE run-length sequence (uint16 run lengths).
    std::vector<uint16_t> encode_rle() const;

    // Decode a bitmap byte vector into bits_.
    static std::vector<bool> decode_bitmap(const uint8_t* data, size_t data_len,
                                           uint32_t element_count);

    // Decode RLE run-length sequence into bits_.
    static std::vector<bool> decode_rle(const uint16_t* runs, size_t num_runs,
                                        uint32_t element_count);
};

} // namespace lqt
