// lqt/simd.h — Compile-time SIMD dispatch for reconstruction kernels.
//
// Council module: A3 (reconstruction), SIMD extension.
// Canon: docs/AGENT_REPORT.md gap #7 (SIMD reconstruction kernels).
//
// Usage: #include "lqt/simd.h"  then call lqt::simd::dequant_fp16_to_fp32(...)
//
// Dispatch priority: AVX2 > NEON > scalar.
// To force scalar: compile with -DLQT_FORCE_SCALAR=1
#pragma once
#include <cstdint>
#include <cstddef>

// ---------------------------------------------------------------------------
// Detect SIMD capability
// ---------------------------------------------------------------------------
#if !defined(LQT_FORCE_SCALAR)
#  if defined(__AVX2__)
#    define LQT_HAS_AVX2 1
#    include <immintrin.h>
#  elif defined(__ARM_NEON) || defined(__aarch64__)
#    define LQT_HAS_NEON 1
#    include <arm_neon.h>
#  endif
#endif

namespace lqt {
namespace simd {

// ---------------------------------------------------------------------------
// fp16_to_fp32
// ---------------------------------------------------------------------------
// Convert n FP16 values (uint16_t) to FP32.
// dst must have capacity for n floats; src must have n uint16_t values.
//
// Fast-path priority:
//   AVX2  — _mm256_cvtph_ps (F16C instruction; 16 elements/iteration)
//   NEON  — vcvt_f32_f16     (8 elements/iteration)
//   scalar — lqt::fp16_to_fp32 loop
void fp16_to_fp32(float* dst, const uint16_t* src, size_t n);

// ---------------------------------------------------------------------------
// dequant_int8
// ---------------------------------------------------------------------------
// Vectorized zero-point affine dequantization for INT8 indices:
// dst[i] = (float(src[i]) - zero_point) * scale.
//
// Fast-path priority:
//   AVX2  — _mm256_cvtepi8_epi32 + fused multiply-add (8 elements/iteration)
//   NEON  — vmovl_s8 + vcvtq_f32_s32 (8 elements/iteration)
//   scalar — cast and affine loop
void dequant_int8(float* dst, const int8_t* src, size_t n, float scale, float zero_point);

// ---------------------------------------------------------------------------
// dequant_int4
// ---------------------------------------------------------------------------
// Vectorized affine dequantization for INT4 (packed 2/byte, low-nibble first).
// n is the number of elements (not bytes). Uses ceil(n/2) source bytes.
//
// Packing convention (DESIGN DECISION D-007):
//   element 2k   = low  nibble of src[k]
//   element 2k+1 = high nibble of src[k]
// Affine convention: dst[i] = (float(nib_i) - zero_point) * scale
// (nibbles are unsigned 0..15 per D-007; zero_point shifts the zero).
//
// Fast-path priority:
//   AVX2  — unpack nibbles via shift/mask, then _mm256_cvtepi32_ps + FMA
//   NEON  — unpack nibbles via vshrq_n_u8/vandq_u8, then vcvtq_f32_s32
//   scalar — manual nibble unpack + affine loop
void dequant_int4(float* dst, const uint8_t* src, size_t n, float scale, float zero_point);

} // namespace simd
} // namespace lqt
