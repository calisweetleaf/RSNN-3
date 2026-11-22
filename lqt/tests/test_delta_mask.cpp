// tests/test_delta_mask.cpp — Tests for DeltaBuffer and SparseMask.
//
// Council module: A4 (delta buffers and sparse masks).
// Canon: lqt.md §2.6 (delta), §2.4 (sparse mask), §3.1 (reconstruction).
//
// Tests:
//   1. delta_fp16_roundtrip_apply    — FP16 dense round-trip + apply (CHECK_NEAR fp16 precision)
//   2. delta_fp32_roundtrip_apply    — FP32 dense exact round-trip + apply
//   3. delta_sparse_roundtrip_apply  — Sparse delta round-trip, apply, bounds check
//   4. delta_num_elements_uint24     — num_elements > 65535 proves uint24 works
//   5. mask_bitmap_roundtrip_apply   — CompressedBitmap round-trip, apply zeros pruned, density
//   6. mask_rle_roundtrip_equals_bitmap — RLE round-trip matches bitmap semantics

#include "test_framework.h"
#include "lqt/delta.h"
#include "lqt/sparse_mask.h"
#include "lqt/endian.h"
#include "lqt/error.h"

#include <cstdlib>
#include <vector>

using namespace lqt;

// ---------------------------------------------------------------------------
// Test 1: delta FP16 dense round-trip and apply
// ---------------------------------------------------------------------------
TEST_CASE(delta_fp16_roundtrip_apply) {
    DeltaBuffer db;
    db.delta_id = 42;
    db.dtype    = DType::FP16;
    db.sparse   = false;
    // Use values that are exactly representable in FP16
    db.values   = { 1.0f, -0.5f, 0.25f, 2.0f, -1.0f };

    // Serialize
    ByteWriter w;
    db.serialize(w);

    // Parse back
    ByteReader r(w.bytes());
    DeltaBuffer db2 = DeltaBuffer::parse(r);

    // Check fields
    CHECK_EQ(db2.delta_id, uint16_t{42});
    CHECK_EQ(db2.dtype, DType::FP16);
    CHECK_EQ(db2.sparse, false);
    CHECK_EQ(db2.values.size(), db.values.size());

    // FP16 has ~3 decimal digits of precision; tolerance = 0.001
    const float tol = 0.001f;
    for (size_t i = 0; i < db.values.size(); ++i) {
        CHECK_NEAR(db2.values[i], db.values[i], tol);
    }

    // Apply: weights[i] += delta[i]
    std::vector<float> weights = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
    db2.apply(weights.data(), weights.size());

    CHECK_NEAR(weights[0],  1.0f, tol);
    CHECK_NEAR(weights[1], -0.5f, tol);
    CHECK_NEAR(weights[2],  0.25f, tol);
    CHECK_NEAR(weights[3],  2.0f, tol);
    CHECK_NEAR(weights[4], -1.0f, tol);
}

// ---------------------------------------------------------------------------
// Test 2: delta FP32 exact round-trip and apply
// ---------------------------------------------------------------------------
TEST_CASE(delta_fp32_roundtrip_apply) {
    DeltaBuffer db;
    db.delta_id = 7;
    db.dtype    = DType::FP32;
    db.sparse   = false;
    db.values   = { 3.14159f, -2.71828f, 1.41421f };

    ByteWriter w;
    db.serialize(w);

    ByteReader r(w.bytes());
    DeltaBuffer db2 = DeltaBuffer::parse(r);

    CHECK_EQ(db2.delta_id, uint16_t{7});
    CHECK_EQ(db2.dtype, DType::FP32);
    CHECK_EQ(db2.sparse, false);
    CHECK_EQ(db2.values.size(), size_t{3});

    // FP32 is bit-exact through the round trip
    CHECK_EQ(db2.values[0], 3.14159f);
    CHECK_EQ(db2.values[1], -2.71828f);
    CHECK_EQ(db2.values[2], 1.41421f);

    // Apply and verify
    std::vector<float> weights = { 10.0f, 10.0f, 10.0f };
    db2.apply(weights.data(), weights.size());
    CHECK_EQ(weights[0], 10.0f + 3.14159f);
    CHECK_EQ(weights[1], 10.0f - 2.71828f);
    CHECK_EQ(weights[2], 10.0f + 1.41421f);
}

// ---------------------------------------------------------------------------
// Test 3: sparse delta round-trip, apply, and bounds-check
// ---------------------------------------------------------------------------
TEST_CASE(delta_sparse_roundtrip_apply) {
    DeltaBuffer db;
    db.delta_id = 100;
    db.dtype    = DType::FP32;
    db.sparse   = true;
    // Sparse: only elements at indices 2, 5, 9 are updated
    db.indices  = { 2u, 5u, 9u };
    db.values   = { 0.1f, -0.2f, 0.3f };

    ByteWriter w;
    db.serialize(w);

    ByteReader r(w.bytes());
    DeltaBuffer db2 = DeltaBuffer::parse(r);

    CHECK_EQ(db2.delta_id, uint16_t{100});
    CHECK_EQ(db2.dtype, DType::FP32);
    CHECK(db2.sparse);
    CHECK_EQ(db2.values.size(), size_t{3});
    CHECK_EQ(db2.indices.size(), size_t{3});
    CHECK_EQ(db2.indices[0], 2u);
    CHECK_EQ(db2.indices[1], 5u);
    CHECK_EQ(db2.indices[2], 9u);
    CHECK_EQ(db2.values[0],  0.1f);
    CHECK_EQ(db2.values[1], -0.2f);
    CHECK_EQ(db2.values[2],  0.3f);

    // Apply
    std::vector<float> weights(10, 1.0f);
    db2.apply(weights.data(), weights.size());
    CHECK_EQ(weights[2], 1.0f + 0.1f);
    CHECK_EQ(weights[5], 1.0f - 0.2f);
    CHECK_EQ(weights[9], 1.0f + 0.3f);
    // Unmodified elements
    CHECK_EQ(weights[0], 1.0f);
    CHECK_EQ(weights[1], 1.0f);

    // Bounds check: index out of range
    DeltaBuffer bad;
    bad.sparse  = true;
    bad.dtype   = DType::FP32;
    bad.indices = { 100u };  // out of range for n=10
    bad.values  = { 1.0f };
    std::vector<float> w2(10, 0.0f);
    CHECK_THROWS_AS(bad.apply(w2.data(), w2.size()), ValidationError);
}

// ---------------------------------------------------------------------------
// Test 4: num_elements > 65535 (uint24 range)
// ---------------------------------------------------------------------------
TEST_CASE(delta_num_elements_uint24) {
    // 70000 elements fits in uint24 (max ~16M) but not uint16 (max 65535)
    const size_t N = 70000;
    DeltaBuffer db;
    db.delta_id = 1;
    db.dtype    = DType::FP32;
    db.sparse   = false;
    db.values.assign(N, 0.5f);

    ByteWriter w;
    db.serialize(w);

    ByteReader r(w.bytes());
    DeltaBuffer db2 = DeltaBuffer::parse(r);

    CHECK_EQ(db2.values.size(), N);
    CHECK_EQ(db2.values[0],    0.5f);
    CHECK_EQ(db2.values[N - 1], 0.5f);
}

// ---------------------------------------------------------------------------
// Test 5: SparseMask CompressedBitmap round-trip, apply, and density
// ---------------------------------------------------------------------------
TEST_CASE(mask_bitmap_roundtrip_apply) {
    // Pattern: 10 elements, bits = [1,0,1,1,0,0,1,0,1,1]
    // 1-bits at indices: 0,2,3,6,8,9  -> 6 out of 10 -> density = 0.6
    std::vector<bool> pattern = { true, false, true, true, false, false, true, false, true, true };

    SparseMask sm(99, SparseEncoding::CompressedBitmap, pattern);

    CHECK_EQ(sm.element_count, 10u);
    CHECK_NEAR(sm.density(), 0.6, 1e-9);

    // Serialize
    ByteWriter w;
    sm.serialize(w);

    // Parse back
    ByteReader r(w.bytes());
    SparseMask sm2 = SparseMask::parse(r);

    CHECK_EQ(sm2.mask_id, uint16_t{99});
    CHECK_EQ(sm2.element_count, 10u);
    CHECK_EQ(sm2.encoding, SparseEncoding::CompressedBitmap);

    // Verify all bits match
    for (size_t i = 0; i < 10; ++i) {
        CHECK_EQ(sm2.bit(i), pattern[i]);
    }
    CHECK_NEAR(sm2.density(), 0.6, 1e-9);

    // Apply: weights at 0-positions should become 0
    std::vector<float> weights(10, 2.5f);
    sm2.apply(weights.data(), weights.size());

    // 1-bit positions: untouched (2.5)
    CHECK_EQ(weights[0], 2.5f);  // bit=1
    CHECK_EQ(weights[2], 2.5f);  // bit=1
    CHECK_EQ(weights[3], 2.5f);  // bit=1
    CHECK_EQ(weights[6], 2.5f);  // bit=1
    CHECK_EQ(weights[8], 2.5f);  // bit=1
    CHECK_EQ(weights[9], 2.5f);  // bit=1

    // 0-bit positions: zeroed
    CHECK_EQ(weights[1], 0.0f);  // bit=0
    CHECK_EQ(weights[4], 0.0f);  // bit=0
    CHECK_EQ(weights[5], 0.0f);  // bit=0
    CHECK_EQ(weights[7], 0.0f);  // bit=0

    // density unchanged
    CHECK_NEAR(sm2.density(), 0.6, 1e-9);

    // bit() out-of-bounds
    CHECK_THROWS_AS(sm2.bit(10), FormatError);
}

// ---------------------------------------------------------------------------
// Test 6: SparseMask RLE round-trip equals Bitmap semantics
// ---------------------------------------------------------------------------
TEST_CASE(mask_rle_roundtrip_equals_bitmap) {
    // Same pattern as test 5 but encoded as RLE
    // bits = [1,0,1,1,0,0,1,0,1,1]
    // Runs starting at 0-bits: [0, 1, 2, 2, 1, 1, 2]
    //   run0 (0-bits) = 0   (no leading zeros; first bit is 1)
    //   run1 (1-bits) = 1   -> [1]
    //   run2 (0-bits) = 1   -> [0]
    //   run3 (1-bits) = 2   -> [1,1]
    //   run4 (0-bits) = 2   -> [0,0]
    //   run5 (1-bits) = 1   -> [1]
    //   run6 (0-bits) = 1   -> [0]
    //   run7 (1-bits) = 2   -> [1,1]
    std::vector<bool> pattern = { true, false, true, true, false, false, true, false, true, true };

    SparseMask sm_rle(55, SparseEncoding::RLE, pattern);
    SparseMask sm_bm(55, SparseEncoding::CompressedBitmap, pattern);

    // Serialize RLE
    ByteWriter wr;
    sm_rle.serialize(wr);

    // Parse back
    ByteReader rr(wr.bytes());
    SparseMask sm_rle2 = SparseMask::parse(rr);

    CHECK_EQ(sm_rle2.mask_id, uint16_t{55});
    CHECK_EQ(sm_rle2.element_count, 10u);
    CHECK_EQ(sm_rle2.encoding, SparseEncoding::RLE);

    // Verify bits match bitmap reference
    for (size_t i = 0; i < 10; ++i) {
        CHECK_EQ(sm_rle2.bit(i), sm_bm.bit(i));
    }

    // Densities should match
    CHECK_NEAR(sm_rle2.density(), sm_bm.density(), 1e-9);

    // Apply weights with RLE mask, compare with bitmap mask apply
    std::vector<float> w_rle(10, 3.0f);
    std::vector<float> w_bm(10, 3.0f);
    sm_rle2.apply(w_rle.data(), w_rle.size());
    sm_bm.apply(w_bm.data(), w_bm.size());

    for (size_t i = 0; i < 10; ++i) {
        CHECK_EQ(w_rle[i], w_bm[i]);
    }

    // Test with all-zeros pattern (all weights pruned)
    std::vector<bool> all_zero(8, false);
    SparseMask sm_zero(1, SparseEncoding::RLE, all_zero);
    ByteWriter wz;
    sm_zero.serialize(wz);
    ByteReader rz(wz.bytes());
    SparseMask sm_zero2 = SparseMask::parse(rz);
    CHECK_NEAR(sm_zero2.density(), 0.0, 1e-9);

    // Test with all-ones pattern (no weights pruned)
    std::vector<bool> all_one(8, true);
    SparseMask sm_one(2, SparseEncoding::RLE, all_one);
    ByteWriter wo;
    sm_one.serialize(wo);
    ByteReader ro(wo.bytes());
    SparseMask sm_one2 = SparseMask::parse(ro);
    CHECK_NEAR(sm_one2.density(), 1.0, 1e-9);
}

int main() {
    return lqttest::run_all();
}
