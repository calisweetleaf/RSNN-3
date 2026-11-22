// lqt/crc.h — CRC-32 (file footer) and CRC-64 (per-RTA-block) integrity.
//
// Council module: A1 (container) / A5 (RTA).
// Canon: lqt.md §2.8 (footer CRC32), §8.1 (cryptographic verification);
//        Transitioning doc §4 (CRC-64 per RTA block + CRC-32 footer).
//
// CRC-32: IEEE 802.3 / zlib (reflected poly 0xEDB88320, init/xorout 0xFFFFFFFF).
//   Verified check value: crc32("123456789") == 0xCBF43926.
// CRC-64: CRC-64/XZ (reflected poly 0xC96C5795D7870F42, init/xorout all-ones).
//   Verified check value: crc64("123456789") == 0x995DC9BBDF1939FA.
#pragma once

#include <cstddef>
#include <cstdint>

namespace lqt {

// One-shot helpers.
uint32_t crc32(const void* data, size_t len);
uint64_t crc64(const void* data, size_t len);

// Incremental variants (seed with 0 on the first call).
uint32_t crc32_update(uint32_t crc, const void* data, size_t len);
uint64_t crc64_update(uint64_t crc, const void* data, size_t len);

} // namespace lqt
