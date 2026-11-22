// lqt/src/simd.cpp — dequantization/reconstruction kernels.
//
// Council module: A3 (reconstruction), SIMD extension.
// Canon: docs/AGENT_REPORT.md gap #7 (SIMD reconstruction kernels).
//
// REAL AVX2 and NEON fast paths are compiled when the target ISA is enabled
// (see simd.h detection; -DLQT_FORCE_SCALAR=1 disables them). Scalar paths are
// always compiled and used for tails.
//
// Dispatch priority: AVX2 > NEON > scalar.
// To force scalar: compile with -DLQT_FORCE_SCALAR=1
//
// AFFINE CONVENTION (ruling 2026-09-21): every dequant_* kernel implements the
// standard zero-point dequantization
//     out[i] = (q[i] - zero_point) * scale
// matching dequant_affine() (lqt/reconstruct.h), the TensorDescriptor
// zero_point field semantics, and the LqtModel codebook-less reconstruction
// contract (tests: model_affine_only_reconstruction). The kernels previously
// computed q*scale + zero_point, which is NOT zero-point dequantization and
// disagreed with the model-level contract; that form is fixed here.

#include "lqt/simd.h"
#include "lqt/fp16.h"

namespace lqt {
namespace simd {

// ---------------------------------------------------------------------------
// fp16_to_fp32
// ---------------------------------------------------------------------------
void fp16_to_fp32(float* dst, const uint16_t* src, size_t n) {
#if defined(LQT_HAS_AVX2) && defined(__F16C__)
    // AVX2 + F16C fast path: _mm256_cvtph_ps converts 8 x fp16 → 8 x fp32.
    // Requires -mavx2 -mf16c on x86-64. CPU confirmed: avx2+f16c present.
    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m128i h8 = _mm_loadu_si128(
            reinterpret_cast<const __m128i*>(src + i));
        __m256  f8 = _mm256_cvtph_ps(h8);
        _mm256_storeu_ps(dst + i, f8);
    }
    for (; i < n; ++i)
        dst[i] = lqt::fp16_to_fp32(src[i]);
#elif defined(LQT_HAS_NEON)
    // NEON fast path: vcvt_f32_f16 converts 4 x fp16 → 4 x fp32.
    size_t i = 0;
    for (; i + 4 <= n; i += 4) {
        float16x4_t h4 = vld1_f16(
            reinterpret_cast<const __fp16*>(src + i));
        float32x4_t f4 = vcvt_f32_f16(h4);
        vst1q_f32(dst + i, f4);
    }
    for (; i < n; ++i)
        dst[i] = lqt::fp16_to_fp32(src[i]);
#else
    // Scalar path — always correct, always compiled.
    for (size_t i = 0; i < n; ++i) {
        dst[i] = lqt::fp16_to_fp32(src[i]);
    }
#endif
}

// ---------------------------------------------------------------------------
// dequant_int8
// ---------------------------------------------------------------------------
void dequant_int8(float* dst, const int8_t* src, size_t n,
                  float scale, float zero_point) {
#if defined(LQT_HAS_AVX2)
    // AVX2 fast path: 8 x int8 → 8 x float per iteration.
    // _mm256_cvtepi8_epi32: sign-extends 8 x i8 (low 8 bytes of __m128i) → 8 x i32.
    // _mm256_cvtepi32_ps: 8 x i32 → 8 x f32.
    // Affine: out = (f32 - zero_point) * scale.
    // Requires -mavx2. CPU confirmed: avx2+fma present.
    {
        const __m256 vscale = _mm256_set1_ps(scale);
        const __m256 vzero  = _mm256_set1_ps(zero_point);
        size_t i = 0;
        for (; i + 8 <= n; i += 8) {
            __m128i s8  = _mm_loadl_epi64(
                reinterpret_cast<const __m128i*>(src + i));
            __m256i i32 = _mm256_cvtepi8_epi32(s8);
            __m256  f32 = _mm256_cvtepi32_ps(i32);
            __m256  out = _mm256_mul_ps(_mm256_sub_ps(f32, vzero), vscale);
            _mm256_storeu_ps(dst + i, out);
        }
        for (; i < n; ++i)
            dst[i] = (static_cast<float>(src[i]) - zero_point) * scale;
    }
#elif defined(LQT_HAS_NEON)
    // NEON fast path: 8 x int8 → 8 x float per iteration.
    {
        const float32x4_t vscale = vdupq_n_f32(scale);
        const float32x4_t vzero  = vdupq_n_f32(zero_point);
        size_t i = 0;
        for (; i + 8 <= n; i += 8) {
            int8x8_t    s8   = vld1_s8(src + i);
            int16x8_t   s16  = vmovl_s8(s8);
            int32x4_t   s32l = vmovl_s16(vget_low_s16(s16));
            int32x4_t   s32h = vmovl_s16(vget_high_s16(s16));
            float32x4_t fl   = vmulq_f32(vsubq_f32(vcvtq_f32_s32(s32l), vzero), vscale);
            float32x4_t fh   = vmulq_f32(vsubq_f32(vcvtq_f32_s32(s32h), vzero), vscale);
            vst1q_f32(dst + i,     fl);
            vst1q_f32(dst + i + 4, fh);
        }
        for (; i < n; ++i)
            dst[i] = (static_cast<float>(src[i]) - zero_point) * scale;
    }
#else
    // Scalar path: dst[i] = (float(src[i]) - zero_point) * scale
    for (size_t i = 0; i < n; ++i) {
        dst[i] = (static_cast<float>(src[i]) - zero_point) * scale;
    }
#endif
}

// ---------------------------------------------------------------------------
// dequant_int4
// ---------------------------------------------------------------------------
void dequant_int4(float* dst, const uint8_t* src, size_t n,
                  float scale, float zero_point) {
#if defined(LQT_HAS_AVX2)
    // AVX2 fast path: unpack 16 INT4 nibbles (8 bytes) per iteration (D-007).
    // Each byte holds: low nibble = element 2k, high nibble = element 2k+1.
    // Strategy: separate lo/hi nibbles, interleave, widen to int32, convert to
    // float, then apply the affine convention out = (q - zero_point) * scale.
    {
        const __m256    vscale = _mm256_set1_ps(scale);
        const __m256    vzero  = _mm256_set1_ps(zero_point);
        const __m128i   mask4  = _mm_set1_epi8(0x0F);
        size_t i = 0;
        for (; i + 16 <= n; i += 16) {
            // Load 8 packed bytes covering 16 nibbles.
            __m128i packed = _mm_loadl_epi64(
                reinterpret_cast<const __m128i*>(src + i / 2));
            // Low nibbles (elements i+0, i+2, ...): mask low 4 bits.
            __m128i lo4 = _mm_and_si128(packed, mask4);
            // High nibbles (elements i+1, i+3, ...): shift right 4.
            __m128i hi4 = _mm_and_si128(_mm_srli_epi16(packed, 4), mask4);
            // Interleave lo and hi nibbles in byte order: lo0,hi0,lo1,hi1,...
            __m128i inter_lo = _mm_unpacklo_epi8(lo4, hi4);
            // First 8 elements (lo0,hi0,lo1,hi1,lo2,hi2,lo3,hi3): zero-extend each
            // byte to 32-bit int and convert to float.
            __m256i i32_a = _mm256_cvtepu8_epi32(inter_lo);
            __m256  f32_a = _mm256_cvtepi32_ps(i32_a);
            __m256  res_a = _mm256_mul_ps(_mm256_sub_ps(f32_a, vzero), vscale);
            _mm256_storeu_ps(dst + i, res_a);
            // Next 8 elements: shift the interleaved bytes right by 8 bytes.
            __m128i inter_hi = _mm_bsrli_si128(inter_lo, 8);
            __m256i i32_b    = _mm256_cvtepu8_epi32(inter_hi);
            __m256  f32_b    = _mm256_cvtepi32_ps(i32_b);
            __m256  res_b    = _mm256_mul_ps(_mm256_sub_ps(f32_b, vzero), vscale);
            _mm256_storeu_ps(dst + i + 8, res_b);
        }
        // Scalar tail.
        for (; i < n; ++i) {
            const uint8_t byte = src[i >> 1];
            const uint8_t nib  = (i & 1u) ? (byte >> 4) : (byte & 0x0Fu);
            dst[i] = (static_cast<float>(nib) - zero_point) * scale;
        }
    }
#elif defined(LQT_HAS_NEON)
    // NEON fast path: unpack 16 INT4 nibbles per iteration.
    {
        const float32x4_t vscale = vdupq_n_f32(scale);
        const float32x4_t vzero  = vdupq_n_f32(zero_point);
        const uint8x8_t   vmask  = vdup_n_u8(0x0F);
        size_t i = 0;
        for (; i + 16 <= n; i += 16) {
            uint8x8_t packed = vld1_u8(src + i / 2);
            uint8x8_t lo = vand_u8(packed, vmask);
            uint8x8_t hi = vand_u8(vshr_n_u8(packed, 4), vmask);
            uint8x8_t inter = vzip1_u8(lo, hi); // interleave lo/hi
            uint16x8_t s16 = vmovl_u8(inter);
            uint32x4_t s32l = vmovl_u16(vget_low_u16(s16));
            uint32x4_t s32h = vmovl_u16(vget_high_u16(s16));
            float32x4_t fl = vmulq_f32(vsubq_f32(vcvtq_f32_u32(s32l), vzero), vscale);
            float32x4_t fh = vmulq_f32(vsubq_f32(vcvtq_f32_u32(s32h), vzero), vscale);
            vst1q_f32(dst + i,     fl);
            vst1q_f32(dst + i + 4, fh);
            // Second 8 nibbles.
            uint8x8_t inter2 = vzip2_u8(lo, hi);
            uint16x8_t s16_2 = vmovl_u8(inter2);
            uint32x4_t s32l2 = vmovl_u16(vget_low_u16(s16_2));
            uint32x4_t s32h2 = vmovl_u16(vget_high_u16(s16_2));
            float32x4_t fl2 = vmulq_f32(vsubq_f32(vcvtq_f32_u32(s32l2), vzero), vscale);
            float32x4_t fh2 = vmulq_f32(vsubq_f32(vcvtq_f32_u32(s32h2), vzero), vscale);
            vst1q_f32(dst + i + 8,  fl2);
            vst1q_f32(dst + i + 12, fh2);
        }
        for (; i < n; ++i) {
            const uint8_t byte = src[i >> 1];
            const uint8_t nib  = (i & 1u) ? (byte >> 4) : (byte & 0x0Fu);
            dst[i] = (static_cast<float>(nib) - zero_point) * scale;
        }
    }
#else
    // Scalar path: unpack low nibble first (D-007), then high nibble.
    // element 2k   = low  nibble of src[k]
    // element 2k+1 = high nibble of src[k]
    for (size_t i = 0; i < n; ++i) {
        const uint8_t byte = src[i >> 1];
        const uint8_t nib  = (i & 1u) ? (byte >> 4) : (byte & 0x0Fu);
        dst[i] = (static_cast<float>(nib) - zero_point) * scale;
    }
#endif
}

} // namespace simd
} // namespace lqt
