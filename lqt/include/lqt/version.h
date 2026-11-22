// lqt/version.h — LQT binary format version + library version.
//
// Council module: A1 (container).
// Canon: lqt.md §2.2 (Header), Binary Spec v1.3 §2.
//
// VERSION FIELD ENCODING (DEVIATION D-002, operator-ratified 2026-06-04):
//   Canon §2.2 prose says "Major (4 bits) + Minor (12 bits)"; the v1.3 binary
//   spec says "(1<<8)|3" = 0x0103 (8 + 8). These conflict. Per the operator's
//   "most architecturally mature SOTA++" directive we adopt the 8-bit major /
//   8-bit minor split:
//     * self-documenting in a hex dump (0x0103 reads as "1.3"),
//     * symmetric and conventional for a uint16 version word,
//     * avoids the 16-major-version ceiling imposed by a 4-bit major field.
//   See docs/SPEC_COMPLIANCE.md D-002.
#pragma once

#include <cstdint>

namespace lqt {

// --- On-disk binary format version (stored in the file header @0x04). ---
inline constexpr uint8_t  LQT_FORMAT_VERSION_MAJOR = 1;
inline constexpr uint8_t  LQT_FORMAT_VERSION_MINOR = 3;

// Compose / decompose the uint16 version word (8-bit major | 8-bit minor).
constexpr uint16_t lqt_make_version(uint8_t major, uint8_t minor) {
    return static_cast<uint16_t>((static_cast<uint16_t>(major) << 8) |
                                 static_cast<uint16_t>(minor));
}
constexpr uint8_t lqt_version_major(uint16_t v) { return static_cast<uint8_t>(v >> 8); }
constexpr uint8_t lqt_version_minor(uint16_t v) { return static_cast<uint8_t>(v & 0xFF); }

// The format version this build reads/writes natively: v1.3 -> 0x0103.
inline constexpr uint16_t LQT_FORMAT_VERSION =
    lqt_make_version(LQT_FORMAT_VERSION_MAJOR, LQT_FORMAT_VERSION_MINOR);

// --- Library (implementation) semantic version, independent of the format. ---
inline constexpr int LQT_LIB_VERSION_MAJOR = 0;
inline constexpr int LQT_LIB_VERSION_MINOR = 1;
inline constexpr int LQT_LIB_VERSION_PATCH = 0;
inline constexpr const char* LQT_LIB_VERSION_STRING = "0.1.0";

} // namespace lqt
