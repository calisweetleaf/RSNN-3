// lqt/header.h — 36-byte file header and 64-byte file footer.
//
// Council module: A1 (container).
// Canon: lqt.md §2.2 (Header), §2.8 (Footer); Binary Spec v1.3 §2, §8.
//
// Header layout (36 bytes, DEVIATION D-001):
//   0x00 magic           uint32   "LQT1"
//   0x04 version         uint16   0x0103 (8-bit major | 8-bit minor)
//   0x06 flags           uint16   HeaderFlag bitmask
//   0x08 header_size      uint32   == LQT_HEADER_SIZE (36)
//   0x0C metadata_offset uint64
//   0x14 tensor_offset   uint64
//   0x1C footer_offset   uint64
//
// Footer layout (64 bytes):
//   0x00 magic           uint32   "LQTF"
//   0x04 checksum        uint32   CRC32 of entire file (checksum field zeroed)
//   0x08 edit_log_offset uint64
//   0x10 timestamp_ns    uint64   Unix epoch nanoseconds
//   0x18 reserved        uint8[40] zero
#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/version.h"

namespace lqt {

struct FileHeader {
    uint32_t magic           = LQT_HEADER_MAGIC;
    uint16_t version         = LQT_FORMAT_VERSION;
    uint16_t flags           = 0;
    uint32_t header_size     = LQT_HEADER_SIZE;
    uint64_t metadata_offset = 0;
    uint64_t tensor_offset   = 0;
    uint64_t footer_offset   = 0;

    void serialize(ByteWriter& w) const;            // emits exactly 36 bytes
    static FileHeader parse(ByteReader& r);          // throws FormatError
    void validate() const;                           // throws FormatError

    bool has_flag(HeaderFlag f) const { return flag_set(flags, f); }
    void set_flag(HeaderFlag f, bool on = true) { flag_assign(flags, f, on); }
    bool is_big_endian() const;

    uint8_t version_major() const { return lqt_version_major(version); }
    uint8_t version_minor() const { return lqt_version_minor(version); }
};

struct FileFooter {
    uint32_t magic           = LQT_FOOTER_MAGIC;
    uint32_t checksum        = 0;
    uint64_t edit_log_offset = 0;
    uint64_t timestamp_ns    = 0;
    // 40 reserved bytes are always serialized as zero.

    void serialize(ByteWriter& w) const;            // emits exactly 64 bytes
    static FileFooter parse(ByteReader& r);          // throws FormatError
    void validate() const;                           // throws FormatError
};

// Compute the canonical whole-file CRC32 with the footer checksum field treated
// as zero. `footer_offset` must point at the footer's first byte; the four
// checksum bytes at footer_offset+4 are excluded from the running CRC.
//
// DEVIATION D-004: canon says "CRC32 of entire file" without stating how the
// checksum field itself is handled. Zeroing it is the only self-consistent
// convention. See docs/SPEC_COMPLIANCE.md D-004.
uint32_t compute_file_checksum(const uint8_t* data, size_t size, uint64_t footer_offset);

// Wall-clock helper: current Unix epoch in nanoseconds (for footer timestamp).
uint64_t now_unix_nanos();

} // namespace lqt
