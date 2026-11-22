// lqt/src/crc.cpp — table-driven CRC-32 (zlib) and CRC-64/XZ.
//
// Tables are built once on first use (thread-safe via function-local static).
#include "lqt/crc.h"

#include <array>

namespace lqt {
namespace {

// --- CRC-32 (reflected, poly 0xEDB88320) ---
const std::array<uint32_t, 256>& crc32_table() {
    static const std::array<uint32_t, 256> table = [] {
        std::array<uint32_t, 256> t{};
        for (uint32_t i = 0; i < 256; ++i) {
            uint32_t c = i;
            for (int k = 0; k < 8; ++k) {
                c = (c & 1u) ? (0xEDB88320u ^ (c >> 1)) : (c >> 1);
            }
            t[i] = c;
        }
        return t;
    }();
    return table;
}

// --- CRC-64/XZ (reflected, poly 0xC96C5795D7870F42) ---
const std::array<uint64_t, 256>& crc64_table() {
    static const std::array<uint64_t, 256> table = [] {
        std::array<uint64_t, 256> t{};
        for (uint32_t i = 0; i < 256; ++i) {
            uint64_t c = i;
            for (int k = 0; k < 8; ++k) {
                c = (c & 1ull) ? (0xC96C5795D7870F42ull ^ (c >> 1)) : (c >> 1);
            }
            t[i] = c;
        }
        return t;
    }();
    return table;
}

} // namespace

uint32_t crc32_update(uint32_t crc, const void* data, size_t len) {
    const auto& table = crc32_table();
    const uint8_t* p = static_cast<const uint8_t*>(data);
    crc = ~crc; // resume reflected running value
    for (size_t i = 0; i < len; ++i) {
        crc = table[(crc ^ p[i]) & 0xFFu] ^ (crc >> 8);
    }
    return ~crc;
}

uint64_t crc64_update(uint64_t crc, const void* data, size_t len) {
    const auto& table = crc64_table();
    const uint8_t* p = static_cast<const uint8_t*>(data);
    crc = ~crc;
    for (size_t i = 0; i < len; ++i) {
        crc = table[(crc ^ p[i]) & 0xFFull] ^ (crc >> 8);
    }
    return ~crc;
}

uint32_t crc32(const void* data, size_t len) { return crc32_update(0u, data, len); }
uint64_t crc64(const void* data, size_t len) { return crc64_update(0ull, data, len); }

} // namespace lqt
