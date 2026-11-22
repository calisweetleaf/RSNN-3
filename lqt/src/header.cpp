// lqt/src/header.cpp — header/footer (de)serialization, validation, checksum.
#include "lqt/header.h"

#include <chrono>

#include "lqt/crc.h"

namespace lqt {

// ------------------------------- FileHeader ---------------------------------
void FileHeader::serialize(ByteWriter& w) const {
    const size_t start = w.size();
    w.put_u32(magic);
    w.put_u16(version);
    w.put_u16(flags);
    w.put_u32(header_size);
    w.put_u64(metadata_offset);
    w.put_u64(tensor_offset);
    w.put_u64(footer_offset);
    // Guarantee the on-disk header is exactly LQT_HEADER_SIZE bytes.
    if (w.size() - start != LQT_HEADER_SIZE) {
        throw FormatError("FileHeader::serialize produced wrong size");
    }
}

FileHeader FileHeader::parse(ByteReader& r) {
    FileHeader h;
    h.magic           = r.get_u32();
    h.version         = r.get_u16();
    h.flags           = r.get_u16();
    h.header_size     = r.get_u32();
    h.metadata_offset = r.get_u64();
    h.tensor_offset   = r.get_u64();
    h.footer_offset   = r.get_u64();
    h.validate();
    return h;
}

void FileHeader::validate() const {
    if (magic != LQT_HEADER_MAGIC) {
        throw FormatError("FileHeader: bad magic (expected 'LQT1')");
    }
    if (header_size != LQT_HEADER_SIZE) {
        throw FormatError("FileHeader: header_size != 36");
    }
    if (version_major() != LQT_FORMAT_VERSION_MAJOR) {
        throw FormatError("FileHeader: unsupported major version");
    }
    // Big-endian files are flagged but not natively materialized by this build's
    // higher layers yet; the flag itself is legal to carry.
    // Offsets are validated against file size by the container/loader layer.
}

bool FileHeader::is_big_endian() const {
    return flag_set(flags, HeaderFlag::BigEndian);
}

// ------------------------------- FileFooter ---------------------------------
void FileFooter::serialize(ByteWriter& w) const {
    const size_t start = w.size();
    w.put_u32(magic);
    w.put_u32(checksum);
    w.put_u64(edit_log_offset);
    w.put_u64(timestamp_ns);
    w.put_zeros(LQT_FOOTER_RESERVED); // 40 reserved bytes
    if (w.size() - start != LQT_FOOTER_SIZE) {
        throw FormatError("FileFooter::serialize produced wrong size");
    }
}

FileFooter FileFooter::parse(ByteReader& r) {
    FileFooter f;
    f.magic           = r.get_u32();
    f.checksum        = r.get_u32();
    f.edit_log_offset = r.get_u64();
    f.timestamp_ns    = r.get_u64();
    r.skip(LQT_FOOTER_RESERVED);
    f.validate();
    return f;
}

void FileFooter::validate() const {
    if (magic != LQT_FOOTER_MAGIC) {
        throw FormatError("FileFooter: bad magic (expected 'LQTF')");
    }
}

// ------------------------------- Checksum -----------------------------------
uint32_t compute_file_checksum(const uint8_t* data, size_t size, uint64_t footer_offset) {
    if (footer_offset + LQT_FOOTER_SIZE > size) {
        throw FormatError("compute_file_checksum: footer offset past end of buffer");
    }
    // CRC over [0, footer_offset+4), skip 4 checksum bytes, resume to end.
    const size_t checksum_pos = static_cast<size_t>(footer_offset) + 4;
    uint32_t crc = crc32_update(0u, data, checksum_pos);
    const size_t after = checksum_pos + 4;
    crc = crc32_update(crc, data + after, size - after);
    return crc;
}

uint64_t now_unix_nanos() {
    using namespace std::chrono;
    return static_cast<uint64_t>(
        duration_cast<nanoseconds>(system_clock::now().time_since_epoch()).count());
}

} // namespace lqt
