// tests/test_simd_avx2.cpp — SIMD fast path accuracy tests (Patch 7).
//
// Verifies that the AVX2/F16C/NEON fast paths in lqt::simd produce the same
// results as the scalar reference paths. The test runs regardless of whether
// the SIMD path is compiled in — the simd:: functions dispatch to the best
// available path so we are testing the actual dispatch result.
//
// Key correctness property: for integer → float conversions there should be no
// rounding difference from the scalar reference (same mathematical operation).

#include <cmath>
#include <cstdint>
#include <vector>

#include "lqt/fp16.h"
#include "lqt/simd.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqt::simd;
using namespace lqttest;

// ── fp16_to_fp32 ──────────────────────────────────────────────────────────────

TEST_CASE(simd_fp16_to_fp32_known_values) {
    // IEEE 754 half-precision constants: 1.0=0x3C00, 2.0=0x4000, 0.0=0x0000, -1.0=0xBC00
    const uint16_t src[4] = {0x3C00, 0x4000, 0x0000, 0xBC00};
    float dst[4] = {};
    fp16_to_fp32(dst, src, 4);
    CHECK_NEAR(dst[0],  1.0f, 1e-3f);
    CHECK_NEAR(dst[1],  2.0f, 1e-3f);
    CHECK_NEAR(dst[2],  0.0f, 1e-6f);
    CHECK_NEAR(dst[3], -1.0f, 1e-3f);
}

TEST_CASE(simd_fp16_to_fp32_large_batch_scalar_agreement) {
    // 128 half-precision values, compare simd path against scalar reference.
    std::vector<uint16_t> src(128);
    for (size_t i = 0; i < 128; ++i) {
        // Construct a variety of normal fp16 values (avoid inf/nan for simplicity).
        float f = static_cast<float>(i) * 0.125f;
        src[i] = lqt::fp32_to_fp16(f);
    }

    std::vector<float> simd_out(128, 0.0f);
    std::vector<float> ref_out(128, 0.0f);

    fp16_to_fp32(simd_out.data(), src.data(), 128);
    for (size_t i = 0; i < 128; ++i)
        ref_out[i] = lqt::fp16_to_fp32(src[i]);

    for (size_t i = 0; i < 128; ++i) {
        CHECK_NEAR(simd_out[i], ref_out[i], 1e-3f);
    }
}

TEST_CASE(simd_fp16_to_fp32_empty) {
    fp16_to_fp32(nullptr, nullptr, 0); // must not crash
}

// ── dequant_int8 ──────────────────────────────────────────────────────────────

TEST_CASE(simd_dequant_int8_scalar_agreement_64) {
    std::vector<int8_t> src(64);
    for (int i = 0; i < 64; ++i) src[i] = static_cast<int8_t>(i - 32); // -32..31

    const float scale = 0.1f, zero = 5.0f;
    std::vector<float> simd_out(64), ref_out(64);

    dequant_int8(simd_out.data(), src.data(), 64, scale, zero);
    for (size_t i = 0; i < 64; ++i)
        ref_out[i] = static_cast<float>(src[i]) * scale + zero;

    for (size_t i = 0; i < 64; ++i)
        CHECK_NEAR(simd_out[i], ref_out[i], 1e-5f);
}

TEST_CASE(simd_dequant_int8_non_multiple_of_8) {
    // n=13 exercises the scalar tail path (13 = 1*8 + 5).
    std::vector<int8_t> src(13);
    for (int i = 0; i < 13; ++i) src[i] = static_cast<int8_t>(i * 10 - 60);

    const float scale = 0.5f, zero = 1.0f;
    std::vector<float> simd_out(13), ref_out(13);

    dequant_int8(simd_out.data(), src.data(), 13, scale, zero);
    for (size_t i = 0; i < 13; ++i)
        ref_out[i] = static_cast<float>(src[i]) * scale + zero;

    for (size_t i = 0; i < 13; ++i)
        CHECK_NEAR(simd_out[i], ref_out[i], 1e-5f);
}

TEST_CASE(simd_dequant_int8_empty) {
    dequant_int8(nullptr, nullptr, 0, 1.0f, 0.0f);
}

// ── dequant_int4 ──────────────────────────────────────────────────────────────

TEST_CASE(simd_dequant_int4_scalar_agreement_32) {
    // 32 INT4 elements packed as 16 bytes. Nibble pattern: 0x01, 0x23, ..., 0xEF.
    // Byte k = lo nibble is element 2k, hi nibble is element 2k+1 (D-007).
    std::vector<uint8_t> src(16);
    for (size_t i = 0; i < 16; ++i)
        src[i] = static_cast<uint8_t>((i & 0x0Fu) | ((((i + 1) & 0x0Fu)) << 4));

    const float scale = 0.5f, zero = 0.0f;
    std::vector<float> simd_out(32), ref_out(32);

    dequant_int4(simd_out.data(), src.data(), 32, scale, zero);
    for (size_t i = 0; i < 32; ++i) {
        const uint8_t byte = src[i >> 1];
        const uint8_t nib  = (i & 1u) ? (byte >> 4) : (byte & 0x0Fu);
        ref_out[i] = static_cast<float>(nib) * scale + zero;
    }

    for (size_t i = 0; i < 32; ++i)
        CHECK_NEAR(simd_out[i], ref_out[i], 1e-5f);
}

TEST_CASE(simd_dequant_int4_non_multiple_of_16) {
    // n=17 exercises the scalar tail path (17 = 1*16 + 1).
    std::vector<uint8_t> src(9, 0x00); // 9 packed bytes → 18 nibbles; use first 17
    for (size_t i = 0; i < 9; ++i) src[i] = static_cast<uint8_t>(i * 17u);

    const float scale = 1.0f, zero = 0.5f;
    std::vector<float> simd_out(17), ref_out(17);

    dequant_int4(simd_out.data(), src.data(), 17, scale, zero);
    for (size_t i = 0; i < 17; ++i) {
        const uint8_t byte = src[i >> 1];
        const uint8_t nib  = (i & 1u) ? (byte >> 4) : (byte & 0x0Fu);
        ref_out[i] = static_cast<float>(nib) * scale + zero;
    }

    for (size_t i = 0; i < 17; ++i)
        CHECK_NEAR(simd_out[i], ref_out[i], 1e-5f);
}

TEST_CASE(simd_dequant_int4_empty) {
    dequant_int4(nullptr, nullptr, 0, 1.0f, 0.0f);
}

int main() { return lqttest::run_all(); }
