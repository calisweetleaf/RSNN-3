// lqt/fp16.h — IEEE 754 half-precision <-> single-precision conversion.
//
// Council module: A1 foundation (shared by A3 codebooks and A4 deltas).
// Canon: lqt.md §2.5 (codebooks stored FP16), §2.6 (delta buffers FP16/FP32).
//
// Round-to-nearest-even on narrowing. Handles zero, subnormal, inf, NaN.
// Header-only.
#pragma once

#include <cstdint>
#include <cstring>

namespace lqt {

inline float fp16_to_fp32(uint16_t h) {
    const uint32_t sign = static_cast<uint32_t>(h & 0x8000u) << 16;
    uint32_t exp  = (h & 0x7C00u) >> 10;
    uint32_t mant = (h & 0x03FFu);
    uint32_t f;
    if (exp == 0) {
        if (mant == 0) {
            f = sign; // +/- zero
        } else {
            // subnormal half -> normalized single
            exp = 1;
            while ((mant & 0x0400u) == 0) { mant <<= 1; --exp; }
            mant &= 0x03FFu;
            f = sign | ((exp + (127 - 15)) << 23) | (mant << 13);
        }
    } else if (exp == 0x1F) {
        f = sign | 0x7F800000u | (mant << 13); // inf / NaN
    } else {
        f = sign | ((exp + (127 - 15)) << 23) | (mant << 13);
    }
    float out;
    std::memcpy(&out, &f, sizeof(out));
    return out;
}

inline uint16_t fp32_to_fp16(float value) {
    uint32_t f;
    std::memcpy(&f, &value, sizeof(f));
    const uint16_t sign = static_cast<uint16_t>((f >> 16) & 0x8000u);
    const uint32_t f_exp = (f >> 23) & 0xFFu;
    uint32_t mant = f & 0x007FFFFFu;

    if (f_exp == 0xFF) { // inf / NaN
        return static_cast<uint16_t>(sign | 0x7C00u | (mant ? 0x0200u : 0u));
    }

    int32_t exp = static_cast<int32_t>(f_exp) - 127 + 15;
    if (exp >= 0x1F) {
        return static_cast<uint16_t>(sign | 0x7C00u); // overflow -> inf
    }
    if (exp <= 0) {
        if (exp < -10) {
            return sign; // underflow -> +/- zero
        }
        // subnormal half
        mant |= 0x00800000u; // restore implicit 1
        const int shift = 14 - exp; // shift in [14, 24]
        uint32_t half = mant >> shift;
        const uint32_t remainder = mant & ((1u << shift) - 1u);
        const uint32_t halfway = 1u << (shift - 1);
        if (remainder > halfway || (remainder == halfway && (half & 1u))) {
            ++half; // round to nearest even
        }
        return static_cast<uint16_t>(sign | half);
    }

    // normal half
    uint16_t out = static_cast<uint16_t>(sign | (static_cast<uint16_t>(exp) << 10) |
                                         static_cast<uint16_t>(mant >> 13));
    const uint32_t remainder = mant & 0x00001FFFu;
    const uint32_t halfway = 0x00001000u;
    if (remainder > halfway || (remainder == halfway && (out & 1u))) {
        ++out; // round-to-nearest-even; carry propagates mantissa -> exponent
    }
    return out;
}

} // namespace lqt
