// tests/test_header.cpp — A1 container: CRC, header/footer, fp16 proving tests.
#include <cstdint>
#include <vector>

#include "lqt/crc.h"
#include "lqt/fp16.h"
#include "lqt/header.h"
#include "lqt/version.h"
#include "test_framework.h"

using namespace lqt;

// --- CRC engines proven against published check values ----------------------
TEST_CASE(crc32_zlib_check_vector) {
    const char* s = "123456789";
    CHECK_EQ(crc32(s, 9), 0xCBF43926u); // canonical CRC-32/ISO-HDLC check
}

TEST_CASE(crc64_xz_check_vector) {
    const char* s = "123456789";
    CHECK_EQ(crc64(s, 9), 0x995DC9BBDF1939FAull); // canonical CRC-64/XZ check
}

TEST_CASE(crc32_incremental_matches_oneshot) {
    const char* s = "123456789";
    uint32_t c = crc32_update(0u, s, 4);
    c = crc32_update(c, s + 4, 5);
    CHECK_EQ(c, crc32(s, 9));
}

// --- Version field encoding (DEVIATION D-002: 8+8 -> 0x0103) ---------------
TEST_CASE(version_encoding_8_8) {
    CHECK_EQ(LQT_FORMAT_VERSION, static_cast<uint16_t>(0x0103));
    CHECK_EQ(lqt_version_major(0x0103), static_cast<uint8_t>(1));
    CHECK_EQ(lqt_version_minor(0x0103), static_cast<uint8_t>(3));
}

// --- Header: 36 bytes, uint64 offsets (DEVIATION D-001) --------------------
TEST_CASE(header_roundtrip_is_36_bytes) {
    FileHeader h;
    h.set_flag(HeaderFlag::HasDeltas, true);
    h.set_flag(HeaderFlag::SelfModifying, true);
    h.metadata_offset = 36;
    h.tensor_offset = 4096;
    h.footer_offset = (1ull << 33); // > 4 GiB: proves uint64 offset

    ByteWriter w;
    h.serialize(w);
    CHECK_EQ(w.size(), static_cast<size_t>(LQT_HEADER_SIZE));
    CHECK_EQ(w.size(), static_cast<size_t>(36));

    ByteReader r(w.bytes());
    FileHeader h2 = FileHeader::parse(r);
    CHECK_EQ(h2.magic, LQT_HEADER_MAGIC);
    CHECK_EQ(h2.version, h.version);
    CHECK(h2.has_flag(HeaderFlag::HasDeltas));
    CHECK(h2.has_flag(HeaderFlag::SelfModifying));
    CHECK(!h2.has_flag(HeaderFlag::Sharded));
    CHECK_EQ(h2.metadata_offset, h.metadata_offset);
    CHECK_EQ(h2.tensor_offset, h.tensor_offset);
    CHECK_EQ(h2.footer_offset, h.footer_offset);
    CHECK_EQ(r.position(), static_cast<size_t>(36));
}

TEST_CASE(footer_roundtrip_is_64_bytes) {
    FileFooter f;
    f.checksum = 0xDEADBEEFu;
    f.edit_log_offset = 0x1122334455667788ull;
    f.timestamp_ns = now_unix_nanos();

    ByteWriter w;
    f.serialize(w);
    CHECK_EQ(w.size(), static_cast<size_t>(64));

    ByteReader r(w.bytes());
    FileFooter f2 = FileFooter::parse(r);
    CHECK_EQ(f2.magic, LQT_FOOTER_MAGIC);
    CHECK_EQ(f2.checksum, f.checksum);
    CHECK_EQ(f2.edit_log_offset, f.edit_log_offset);
    CHECK_EQ(f2.timestamp_ns, f.timestamp_ns);
    CHECK_EQ(r.position(), static_cast<size_t>(64));
}

TEST_CASE(header_bad_magic_rejected) {
    ByteWriter w;
    w.put_u32(0x12345678u); // wrong magic
    w.put_u16(0x0103);
    w.put_u16(0);
    w.put_u32(36);
    w.put_u64(36);
    w.put_u64(0);
    w.put_u64(0);
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(FileHeader::parse(r), FormatError);
}

TEST_CASE(header_truncated_buffer_rejected) {
    ByteWriter w;
    w.put_u32(LQT_HEADER_MAGIC);
    w.put_u16(0x0103); // only 6 bytes total — truncated
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(FileHeader::parse(r), FormatError);
}

// --- Whole-file checksum: field excluded, corruption detected ---------------
TEST_CASE(file_checksum_excludes_field_and_detects_corruption) {
    std::vector<uint8_t> file(128, 0);
    for (size_t i = 0; i < file.size(); ++i) file[i] = static_cast<uint8_t>(i * 7 + 1);
    const uint64_t footer_off = 64;

    const uint32_t c1 = compute_file_checksum(file.data(), file.size(), footer_off);
    // Write c1 into the footer checksum field [footer_off+4, footer_off+8).
    for (int i = 0; i < 4; ++i) file[footer_off + 4 + i] = static_cast<uint8_t>((c1 >> (8 * i)) & 0xFF);
    const uint32_t c2 = compute_file_checksum(file.data(), file.size(), footer_off);
    CHECK_EQ(c1, c2); // idempotent: checksum field is excluded from CRC

    file[10] ^= 0xFFu; // corrupt a data byte
    const uint32_t c3 = compute_file_checksum(file.data(), file.size(), footer_off);
    CHECK(c3 != c1);
}

// --- fp16 conversion --------------------------------------------------------
TEST_CASE(fp16_roundtrip_and_known_value) {
    const float vals[] = {0.0f, 1.0f, -1.0f, 0.5f, -2.0f, 3.5f, 100.0f, 0.125f};
    for (float v : vals) {
        const uint16_t h = fp32_to_fp16(v);
        const float back = fp16_to_fp32(h);
        CHECK_NEAR(back, v, 0.01);
    }
    CHECK_EQ(fp32_to_fp16(1.0f), static_cast<uint16_t>(0x3C00)); // 1.0 in half
    CHECK_NEAR(fp16_to_fp32(0x3C00), 1.0f, 1e-6);
}

TEST_CASE(big_endian_flag_detection) {
    FileHeader h;
    h.set_flag(HeaderFlag::BigEndian);
    CHECK(h.is_big_endian());
    h.set_flag(HeaderFlag::BigEndian, false);
    CHECK(!h.is_big_endian());
}

TEST_CASE(big_endian_reader_byteswap) {
    // Write a uint32 in little-endian, read it as big-endian — should be swapped.
    ByteWriter w;
    w.put_u32(0x12345678u); // LE bytes: 78 56 34 12
    BigEndianByteReader r(w.bytes());
    // Reading as big-endian: bytes 78 56 34 12 interpreted as 0x78563412
    CHECK_EQ(r.get_u32(), 0x78563412u);
}

int main() { return lqttest::run_all(); }
