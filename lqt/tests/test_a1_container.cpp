// tests/test_a1_container.cpp — A1 council: binary container layer tests.
//
// Covers: CRC-32 check-vector, CRC-64 check-vector, ByteWriter/ByteReader
// round-trip, FileHeader serialize/parse/validate, FileFooter serialize/parse/
// validate, compute_file_checksum, corruption rejection, flag helpers,
// version encoding helpers.
//
// CRC check vectors (authoritative per polynomial specs):
//   crc32("123456789") == 0xCBF43926
//   crc64("123456789") == 0x995DC9BBDF1939FA

#include "test_framework.h"
#include "lqt/crc.h"
#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/header.h"
#include "lqt/version.h"

#include <cstring>
#include <vector>

using namespace lqt;
using namespace lqttest;

// ============================================================ CRC-32 tests ==

TEST_CASE(crc32_check_vector) {
    // IEEE 802.3 standard check value: crc32("123456789") == 0xCBF43926
    const char* input = "123456789";
    uint32_t got = crc32(input, 9);
    CHECK_MSG(got == 0xCBF43926u,
        "CRC-32 check vector failed: expected 0xCBF43926");
}

TEST_CASE(crc32_empty) {
    // crc32("") == 0x00000000 for initial CRC 0
    uint32_t got = crc32(nullptr, 0);
    // Standard: crc32 of empty is ~(~0) = 0x00000000
    // With our implementation: ~0u XOR ~0u -> 0
    CHECK_EQ(got, 0x00000000u);
}

TEST_CASE(crc32_incremental) {
    const char* input = "123456789";
    // Split "12345" then "6789"
    uint32_t incremental = crc32_update(0u, input, 5);
    incremental = crc32_update(incremental, input + 5, 4);
    uint32_t full = crc32(input, 9);
    CHECK_EQ(incremental, full);
}

// ============================================================ CRC-64 tests ==

TEST_CASE(crc64_check_vector) {
    // CRC-64/XZ standard check value: crc64("123456789") == 0x995DC9BBDF1939FA
    const char* input = "123456789";
    uint64_t got = crc64(input, 9);
    CHECK_MSG(got == 0x995DC9BBDF1939FAull,
        "CRC-64 check vector failed: expected 0x995DC9BBDF1939FA");
}

TEST_CASE(crc64_incremental) {
    const char* input = "123456789";
    uint64_t incremental = crc64_update(0ull, input, 5);
    incremental = crc64_update(incremental, input + 5, 4);
    uint64_t full = crc64(input, 9);
    CHECK_EQ(incremental, full);
}

// =========================================== ByteWriter / ByteReader tests ==

TEST_CASE(bytewriter_reader_primitives) {
    ByteWriter w;
    w.put_u8(0xAB);
    w.put_u16(0x1234);
    w.put_u32(0xDEADBEEFu);
    w.put_u64(0xCAFEBABE12345678ull);
    w.put_i8(-42);
    w.put_i16(-1000);
    w.put_i32(-100000);

    ByteReader r(w.bytes());
    CHECK_EQ(r.get_u8(), 0xABu);
    CHECK_EQ(r.get_u16(), 0x1234u);
    CHECK_EQ(r.get_u32(), 0xDEADBEEFu);
    CHECK_EQ(r.get_u64(), 0xCAFEBABE12345678ull);
    CHECK_EQ(r.get_i8(), (int8_t)-42);
    CHECK_EQ(r.get_i16(), (int16_t)-1000);
    CHECK_EQ(r.get_i32(), (int32_t)-100000);
    CHECK_EQ(r.remaining(), (size_t)0);
}

TEST_CASE(bytewriter_reader_float) {
    ByteWriter w;
    w.put_f32(3.14159f);
    w.put_f64(2.718281828459045);
    ByteReader r(w.bytes());
    CHECK_NEAR(r.get_f32(), 3.14159f, 1e-5);
    CHECK_NEAR(r.get_f64(), 2.718281828459045, 1e-12);
}

TEST_CASE(bytewriter_reader_string) {
    ByteWriter w;
    w.put_string("hello, LQT");
    ByteReader r(w.bytes());
    CHECK_EQ(r.get_string(), std::string("hello, LQT"));
}

TEST_CASE(bytewriter_pad_alignment) {
    ByteWriter w;
    w.put_u8(0x01); // pos=1
    w.pad_to(4);    // should add 3 bytes padding -> pos=4
    CHECK_EQ(w.size(), (size_t)4);
    w.put_u32(0xDEADBEEFu);
    CHECK_EQ(w.size(), (size_t)8);
}

TEST_CASE(bytewriter_patch_u64) {
    ByteWriter w;
    w.put_u64(0ull);         // reserve 8 bytes at position 0
    w.put_u32(0xDEADBEEFu);  // put something after
    w.patch_u64(0, 0x1122334455667788ull);
    ByteReader r(w.bytes());
    CHECK_EQ(r.get_u64(), 0x1122334455667788ull);
    CHECK_EQ(r.get_u32(), 0xDEADBEEFu);
}

TEST_CASE(bytereader_bounds_check) {
    std::vector<uint8_t> buf = {0x01, 0x02};
    ByteReader r(buf.data(), buf.size());
    r.get_u8(); r.get_u8(); // consume both bytes
    CHECK_THROWS_AS(r.get_u8(), FormatError);
}

TEST_CASE(bytereader_seek_and_skip) {
    ByteWriter w;
    for (int i = 0; i < 16; ++i) w.put_u8(static_cast<uint8_t>(i));
    ByteReader r(w.bytes());
    r.seek(8);
    CHECK_EQ(r.get_u8(), 8u);
    r.skip(2); // skip 9, 10
    CHECK_EQ(r.get_u8(), 11u);
    CHECK_THROWS_AS(r.seek(100), FormatError);
}

TEST_CASE(bytewriter_put_u24_roundtrip) {
    ByteWriter w;
    w.put_u24(0xABCDEFu);
    ByteReader r(w.bytes());
    CHECK_EQ(w.size(), (size_t)3);
    CHECK_EQ(r.get_u24(), 0xABCDEFu);
}

// ===================================================== version helpers =====

TEST_CASE(version_encoding) {
    // D-002: 8-bit major | 8-bit minor, v1.3 -> 0x0103
    uint16_t v = lqt_make_version(1, 3);
    CHECK_EQ(v, 0x0103u);
    CHECK_EQ(lqt_version_major(v), 1u);
    CHECK_EQ(lqt_version_minor(v), 3u);
    // Global constant
    CHECK_EQ(LQT_FORMAT_VERSION, 0x0103u);
}

// ================================================== FileHeader tests ========

TEST_CASE(file_header_serialize_size) {
    FileHeader h;
    ByteWriter w;
    h.serialize(w);
    CHECK_EQ(w.size(), (size_t)LQT_HEADER_SIZE); // D-001: 36 bytes
}

TEST_CASE(file_header_round_trip) {
    FileHeader orig;
    orig.metadata_offset = 36;
    orig.tensor_offset   = 2048;
    orig.footer_offset   = 65536;
    orig.set_flag(HeaderFlag::HasDeltas);
    orig.set_flag(HeaderFlag::Align64);

    ByteWriter w;
    orig.serialize(w);

    ByteReader r(w.bytes());
    FileHeader parsed = FileHeader::parse(r);

    CHECK_EQ(parsed.magic,           LQT_HEADER_MAGIC);
    CHECK_EQ(parsed.version,         LQT_FORMAT_VERSION);
    CHECK_EQ(parsed.header_size,     LQT_HEADER_SIZE);
    CHECK_EQ(parsed.metadata_offset, (uint64_t)36);
    CHECK_EQ(parsed.tensor_offset,   (uint64_t)2048);
    CHECK_EQ(parsed.footer_offset,   (uint64_t)65536);
    CHECK(parsed.has_flag(HeaderFlag::HasDeltas));
    CHECK(parsed.has_flag(HeaderFlag::Align64));
    CHECK(!parsed.has_flag(HeaderFlag::BigEndian));
    CHECK_EQ(parsed.version_major(), (uint8_t)1);
    CHECK_EQ(parsed.version_minor(), (uint8_t)3);
}

TEST_CASE(file_header_bad_magic_rejected) {
    FileHeader h;
    ByteWriter w;
    h.serialize(w);
    // Corrupt the magic
    auto& buf = const_cast<std::vector<uint8_t>&>(w.bytes());
    buf[0] = 0xFF;
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(FileHeader::parse(r), FormatError);
}

TEST_CASE(file_header_bad_header_size_rejected) {
    FileHeader h;
    ByteWriter w;
    h.serialize(w);
    // Overwrite header_size field (bytes 8-11 LE) with 32 instead of 36
    auto& buf = const_cast<std::vector<uint8_t>&>(w.bytes());
    buf[8]  = 32; buf[9]  = 0; buf[10] = 0; buf[11] = 0;
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(FileHeader::parse(r), FormatError);
}

// =================================================== FileFooter tests ======

TEST_CASE(file_footer_serialize_size) {
    FileFooter f;
    ByteWriter w;
    f.serialize(w);
    CHECK_EQ(w.size(), (size_t)LQT_FOOTER_SIZE); // 64 bytes
}

TEST_CASE(file_footer_round_trip) {
    FileFooter orig;
    orig.checksum        = 0xABCDABCDu;
    orig.edit_log_offset = 0x123456789ABCull;
    orig.timestamp_ns    = 1748000000000000000ull;

    ByteWriter w;
    orig.serialize(w);

    ByteReader r(w.bytes());
    FileFooter parsed = FileFooter::parse(r);

    CHECK_EQ(parsed.magic,           LQT_FOOTER_MAGIC);
    CHECK_EQ(parsed.checksum,        0xABCDABCDu);
    CHECK_EQ(parsed.edit_log_offset, 0x123456789ABCull);
    CHECK_EQ(parsed.timestamp_ns,    1748000000000000000ull);
}

TEST_CASE(file_footer_bad_magic_rejected) {
    FileFooter f;
    ByteWriter w;
    f.serialize(w);
    auto& buf = const_cast<std::vector<uint8_t>&>(w.bytes());
    buf[0] = 0xAA;
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(FileFooter::parse(r), FormatError);
}

TEST_CASE(file_footer_reserved_bytes_zero) {
    FileFooter f;
    ByteWriter w;
    f.serialize(w);
    // Bytes 0x18..0x3F should be zero
    const auto& buf = w.bytes();
    for (size_t i = 0x18; i < LQT_FOOTER_SIZE; ++i) {
        CHECK_EQ(buf[i], 0u);
    }
}

// ============================================= compute_file_checksum test ===

TEST_CASE(file_checksum_stability) {
    // Build a minimal valid file: header + 1 byte + footer.
    FileHeader hdr;
    hdr.metadata_offset = LQT_HEADER_SIZE;
    hdr.tensor_offset   = LQT_HEADER_SIZE;
    hdr.footer_offset   = LQT_HEADER_SIZE + 1; // immediately after 1-byte payload

    FileFooter ftr;

    ByteWriter w;
    hdr.serialize(w);
    w.put_u8(0xFF); // payload byte

    const uint64_t footer_pos = static_cast<uint64_t>(w.size());
    ftr.edit_log_offset  = 0;
    ftr.timestamp_ns     = 12345678ull;
    ftr.serialize(w);

    // Compute checksum with zeroed checksum field.
    const std::vector<uint8_t>& buf = w.bytes();
    uint32_t cs1 = compute_file_checksum(buf.data(), buf.size(), footer_pos);
    // Applying checksum then re-computing must yield a stable result.
    // Patch checksum into the footer checksum field (offset +4 in footer).
    std::vector<uint8_t> buf2 = buf;
    buf2[footer_pos + 4] = static_cast<uint8_t>(cs1 & 0xFF);
    buf2[footer_pos + 5] = static_cast<uint8_t>((cs1 >> 8) & 0xFF);
    buf2[footer_pos + 6] = static_cast<uint8_t>((cs1 >> 16) & 0xFF);
    buf2[footer_pos + 7] = static_cast<uint8_t>((cs1 >> 24) & 0xFF);
    // Re-computing over the patched file should give same value (checksum
    // field is excluded from computation, so it is always treated as zero).
    uint32_t cs2 = compute_file_checksum(buf2.data(), buf2.size(), footer_pos);
    CHECK_EQ(cs1, cs2);
}

TEST_CASE(file_checksum_detects_corruption) {
    // Build the same minimal file as above.
    FileHeader hdr;
    hdr.metadata_offset = LQT_HEADER_SIZE;
    hdr.tensor_offset   = LQT_HEADER_SIZE;
    hdr.footer_offset   = LQT_HEADER_SIZE + 4;

    FileFooter ftr;
    ByteWriter w;
    hdr.serialize(w);
    w.put_u32(0x12345678u);
    const uint64_t footer_pos = static_cast<uint64_t>(w.size());
    ftr.serialize(w);

    const std::vector<uint8_t>& buf = w.bytes();
    uint32_t original_cs = compute_file_checksum(buf.data(), buf.size(), footer_pos);

    // Flip a bit in the payload.
    std::vector<uint8_t> corrupted = buf;
    corrupted[LQT_HEADER_SIZE] ^= 0x01u;
    uint32_t corrupted_cs = compute_file_checksum(corrupted.data(), corrupted.size(), footer_pos);

    CHECK_MSG(original_cs != corrupted_cs,
        "checksum should differ for corrupted data");
}

// ============================================================ entry point ==

int main() { return lqttest::run_all(); }
