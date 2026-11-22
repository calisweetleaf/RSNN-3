// tests/test_pack_indices.cpp — pack_indices (inverse of unpack_indices) and
// the ByteReader polymorphic-destruction contract.
//
// Added 2026-11-21 (lane lqt-bindings): the Python bindings build tensors from
// u32 codebook indices, which needs the exact inverse of unpack_indices
// (D-007 INT4 low-nibble-first; INT8/UINT8 1 byte; INT16/INT32 LE). Also
// regression for make_reader(): it returns unique_ptr<ByteReader> holding a
// BigEndianByteReader, so ByteReader must have a virtual destructor.

#include <cstdint>
#include <memory>
#include <type_traits>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/reconstruct.h"
#include "test_framework.h"

using namespace lqt;

static void roundtrip(DType dt, const std::vector<uint32_t>& idx) {
    const std::vector<uint8_t> packed = pack_indices(idx, dt);
    const std::vector<uint32_t> back = unpack_indices(packed.data(), packed.size(), idx.size(), dt);
    CHECK_EQ(back.size(), idx.size());
    for (size_t i = 0; i < idx.size(); ++i) CHECK_EQ(back[i], idx[i]);
}

TEST_CASE(pack_int4_matches_d007_layout) {
    // Same bytes as examples/write_lqt.cpp: {0,1,2,3,3,2,1,0} -> 10 32 23 01.
    const std::vector<uint8_t> p = pack_indices({0, 1, 2, 3, 3, 2, 1, 0}, DType::INT4);
    CHECK_EQ(p.size(), static_cast<size_t>(4));
    CHECK_EQ(p[0], 0x10); CHECK_EQ(p[1], 0x32); CHECK_EQ(p[2], 0x23); CHECK_EQ(p[3], 0x01);
}

TEST_CASE(pack_int4_odd_count_pads_high_nibble_zero) {
    const std::vector<uint8_t> p = pack_indices({15, 7, 9}, DType::INT4);
    CHECK_EQ(p.size(), static_cast<size_t>(2));
    CHECK_EQ(p[0], 0x7F); CHECK_EQ(p[1], 0x09);
    roundtrip(DType::INT4, {15, 7, 9});
}

TEST_CASE(pack_roundtrip_all_index_dtypes) {
    roundtrip(DType::INT8, {0, 1, 127, 255, 42});
    roundtrip(DType::UINT8, {255, 0, 128});
    roundtrip(DType::INT16, {0, 1, 65535, 300, 4096});
    roundtrip(DType::INT32, {0, 1, 0xFFFFFFFFu, 70000, 123456789u});
}

TEST_CASE(pack_int16_is_little_endian) {
    const std::vector<uint8_t> p = pack_indices({0x1234}, DType::INT16);
    CHECK_EQ(p[0], 0x34); CHECK_EQ(p[1], 0x12);
}

TEST_CASE(pack_rejects_out_of_range_and_non_index_dtype) {
    CHECK_THROWS_AS(pack_indices({16}, DType::INT4), ValidationError);
    CHECK_THROWS_AS(pack_indices({256}, DType::INT8), ValidationError);
    CHECK_THROWS_AS(pack_indices({65536}, DType::INT16), ValidationError);
    CHECK_THROWS_AS(pack_indices({0}, DType::FP32), FormatError);
}

TEST_CASE(byte_reader_destroys_polymorphically) {
    static_assert(std::has_virtual_destructor<ByteReader>::value,
                  "make_reader returns unique_ptr<ByteReader> owning a BigEndianByteReader");
    const uint8_t buf[4] = {0x00, 0x00, 0x01, 0x02};
    std::unique_ptr<ByteReader> r = make_reader(buf, sizeof(buf), true);
    CHECK_EQ(r->get_u32(), static_cast<uint32_t>(0x00000102));
    r.reset();  // must run ~BigEndianByteReader via the base pointer
    CHECK(true);
}

int main() { return lqttest::run_all(); }
