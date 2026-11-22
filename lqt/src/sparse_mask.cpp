// src/sparse_mask.cpp — Implementation of SparseMask serialization, parsing,
//                       bit access, density, and weight application.
//
// Council module: A4 (delta buffers and sparse masks).
// Canon: lqt.md §2.4 (Tensor Data), §3.1 (reconstruction); v1.3 §4 (encodings).
//
// Supported encodings:
//   CompressedBitmap (0x04): 1 bit/element, LSB-first per byte.
//   RLE (0x03): alternating uint16 run-lengths, first run = count of 0-bits.
//
// On-disk block layout:
//   mask_id (u16) | encoding_type (u8) | element_count (u32) | pad_to(4)
//   | encoding data | pad_to(4)

#include "lqt/sparse_mask.h"

#include <algorithm>
#include <numeric>
#include <sstream>

namespace lqt {

// ---------------------------------------------------------------------------
// Construction helpers
// ---------------------------------------------------------------------------

SparseMask::SparseMask(uint16_t id, SparseEncoding enc, std::vector<bool> b)
    : mask_id(id),
      encoding(enc),
      element_count(static_cast<uint32_t>(b.size())),
      bits(std::move(b))
{
    if (encoding != SparseEncoding::CompressedBitmap &&
        encoding != SparseEncoding::RLE) {
        throw ValidationError("SparseMask: only CompressedBitmap and RLE encodings are supported");
    }
}

SparseMask SparseMask::from_bitfield(uint16_t id, SparseEncoding enc,
                                      const uint8_t* data, uint32_t element_count) {
    SparseMask sm;
    sm.mask_id       = id;
    sm.encoding      = enc;
    sm.element_count = element_count;
    sm.bits          = decode_bitmap(data,
                                     (static_cast<size_t>(element_count) + 7) / 8,
                                     element_count);
    if (sm.encoding != SparseEncoding::CompressedBitmap &&
        sm.encoding != SparseEncoding::RLE) {
        throw ValidationError("SparseMask: only CompressedBitmap and RLE encodings are supported");
    }
    return sm;
}

// ---------------------------------------------------------------------------
// Internal encode helpers
// ---------------------------------------------------------------------------

std::vector<uint8_t> SparseMask::encode_bitmap() const {
    const size_t byte_len = (element_count + 7) / 8;
    std::vector<uint8_t> out(byte_len, 0);
    for (uint32_t i = 0; i < element_count; ++i) {
        if (bits[i]) {
            out[i / 8] |= static_cast<uint8_t>(1u << (i % 8));
        }
    }
    return out;
}

std::vector<uint16_t> SparseMask::encode_rle() const {
    // DESIGN DECISION A4-DD-5: alternating runs starting with a run of 0-bits.
    // First entry = number of leading 0-bits (may be 0 if first bit is 1).
    std::vector<uint16_t> runs;
    if (element_count == 0) {
        return runs;
    }

    bool current_val = false;  // start counting 0-bits
    uint16_t run_len = 0;

    for (uint32_t i = 0; i < element_count; ++i) {
        bool b = bits[i];
        if (b == current_val) {
            // Overflow protection: uint16 max is 65535
            if (run_len == 65535u) {
                // DESIGN DECISION A4-DD-6: when a run exceeds uint16 max, we
                // split it by emitting the saturated run and a zero-length run
                // of the opposite polarity, then continuing.
                runs.push_back(65535u);
                runs.push_back(0u);
                run_len = 1u;
                // current_val stays the same (we just emitted a zero opposite run)
            } else {
                ++run_len;
            }
        } else {
            runs.push_back(run_len);
            run_len = 1u;
            current_val = !current_val;
        }
    }
    runs.push_back(run_len);
    return runs;
}

// ---------------------------------------------------------------------------
// Internal decode helpers
// ---------------------------------------------------------------------------

std::vector<bool> SparseMask::decode_bitmap(const uint8_t* data, size_t data_len,
                                             uint32_t element_count) {
    const size_t required_bytes = (static_cast<size_t>(element_count) + 7) / 8;
    if (data_len < required_bytes) {
        std::ostringstream oss;
        oss << "SparseMask::decode_bitmap: need " << required_bytes
            << " bytes for " << element_count << " elements, got " << data_len;
        throw FormatError(oss.str());
    }
    std::vector<bool> bits(element_count);
    for (uint32_t i = 0; i < element_count; ++i) {
        bits[i] = ((data[i / 8] >> (i % 8)) & 1u) != 0;
    }
    return bits;
}

std::vector<bool> SparseMask::decode_rle(const uint16_t* runs, size_t num_runs,
                                          uint32_t element_count) {
    std::vector<bool> bits(element_count, false);
    uint32_t pos = 0;
    bool val = false;  // first run is always 0-bits
    for (size_t r = 0; r < num_runs && pos < element_count; ++r) {
        uint16_t run_len = runs[r];
        uint32_t end = std::min(static_cast<uint32_t>(pos + run_len), element_count);
        for (uint32_t i = pos; i < end; ++i) {
            bits[i] = val;
        }
        pos += run_len;
        val = !val;
    }
    if (pos != element_count) {
        // If runs don't cover element_count exactly, remaining bits stay false.
        // Only raise an error if we consumed MORE bits than element_count.
        // (Trailing zero run may be omitted per design; see A4-DD-5.)
    }
    return bits;
}

// ---------------------------------------------------------------------------
// serialize
// ---------------------------------------------------------------------------

void SparseMask::serialize(ByteWriter& w) const {
    if (bits.size() != element_count) {
        throw ValidationError("SparseMask::serialize: bits.size() != element_count");
    }
    if (encoding != SparseEncoding::CompressedBitmap &&
        encoding != SparseEncoding::RLE) {
        throw ValidationError("SparseMask::serialize: unsupported encoding");
    }

    // Header: mask_id (u16) + encoding_type (u8) + element_count (u32) = 7 bytes
    w.put_u16(mask_id);
    w.put_u8(static_cast<uint8_t>(encoding));
    w.put_u32(element_count);
    // Pad header to 4-byte alignment (7 bytes -> 1 byte pad -> 8 bytes total)
    w.pad_to(LQT_ALIGN_DELTA);

    // Data section
    if (encoding == SparseEncoding::CompressedBitmap) {
        std::vector<uint8_t> bm = encode_bitmap();
        w.put_bytes(bm.data(), bm.size());
    } else {
        // RLE
        std::vector<uint16_t> runs = encode_rle();
        for (uint16_t r : runs) {
            w.put_u16(r);
        }
    }

    // Pad end of data to 4-byte alignment
    w.pad_to(LQT_ALIGN_DELTA);
}

// ---------------------------------------------------------------------------
// parse
// ---------------------------------------------------------------------------

SparseMask SparseMask::parse(ByteReader& r) {
    SparseMask sm;

    sm.mask_id = r.get_u16();
    sm.encoding = static_cast<SparseEncoding>(r.get_u8());
    sm.element_count = r.get_u32();

    // Skip header alignment padding (7 bytes -> 4-byte boundary)
    r.align_to(LQT_ALIGN_DELTA);

    if (sm.encoding == SparseEncoding::CompressedBitmap) {
        const size_t byte_len = (static_cast<size_t>(sm.element_count) + 7) / 8;
        r.require(byte_len);
        sm.bits = decode_bitmap(r.current(), byte_len, sm.element_count);
        r.skip(byte_len);
        // Consume alignment padding after bitmap data
        r.align_to(LQT_ALIGN_DELTA);
    } else if (sm.encoding == SparseEncoding::RLE) {
        // We need to read until we've reconstructed element_count bits.
        // But we don't know ahead of time how many runs there are; we read
        // until we have all bits or the reader is exhausted.
        // DESIGN DECISION A4-DD-7: on parse, we determine num_runs by
        // decoding runs until the accumulated bit count reaches element_count.
        // The serialized block is padded to 4 bytes; we stop reading uint16
        // values when our decoded bit count reaches element_count.
        std::vector<uint16_t> runs;
        uint32_t total_bits = 0;
        const size_t saved_pos = r.position();
        while (total_bits < sm.element_count && r.remaining() >= 2) {
            uint16_t rlen = r.get_u16();
            runs.push_back(rlen);
            total_bits += rlen;
            // After reading each run: if total_bits >= element_count, stop.
            if (total_bits >= sm.element_count) break;
        }
        sm.bits = decode_rle(runs.data(), runs.size(), sm.element_count);
        // Advance to 4-byte alignment
        r.align_to(LQT_ALIGN_DELTA);
        (void)saved_pos;
    } else {
        std::ostringstream oss;
        oss << "SparseMask::parse: unsupported encoding 0x"
            << std::hex << static_cast<unsigned>(sm.encoding);
        throw FormatError(oss.str());
    }

    return sm;
}

// ---------------------------------------------------------------------------
// bit access
// ---------------------------------------------------------------------------

bool SparseMask::bit(size_t i) const {
    if (i >= element_count) {
        std::ostringstream oss;
        oss << "SparseMask::bit: index " << i << " >= element_count=" << element_count;
        throw FormatError(oss.str());
    }
    return bits[i];
}

// ---------------------------------------------------------------------------
// density
// ---------------------------------------------------------------------------

double SparseMask::density() const {
    if (element_count == 0) return 0.0;
    size_t count = 0;
    for (uint32_t i = 0; i < element_count; ++i) {
        if (bits[i]) ++count;
    }
    return static_cast<double>(count) / static_cast<double>(element_count);
}

// ---------------------------------------------------------------------------
// apply
// ---------------------------------------------------------------------------

void SparseMask::apply(float* weights, size_t n) const {
    if (n != element_count) {
        std::ostringstream oss;
        oss << "SparseMask::apply: n=" << n << " != element_count=" << element_count;
        throw ValidationError(oss.str());
    }
    for (uint32_t i = 0; i < element_count; ++i) {
        if (!bits[i]) {
            weights[i] = 0.0f;
        }
    }
}

} // namespace lqt
