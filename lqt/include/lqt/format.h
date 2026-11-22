// lqt/format.h — Canonical LQT binary constants, magic values, enums, flags.
//
// Council module: A1/A2 (container + metadata).
// Canon: lqt.md §2 (Format Specification), Binary Spec v1.3.
//
// This header is the single source of truth for on-disk constants. Every other
// module derives layout from here so there is no silent format drift.
#pragma once

#include <cstdint>
#include "lqt/version.h"

namespace lqt {

// ------------------------------ Magic values --------------------------------
// Stored little-endian on disk. "LQT1" / "LQTF" as ASCII -> these uint32s when
// the first character occupies the least-significant byte.
inline constexpr uint32_t LQT_HEADER_MAGIC = 0x4C515431u; // "LQT1"
inline constexpr uint32_t LQT_FOOTER_MAGIC = 0x4C515446u; // "LQTF"

// RTA block sentinel: 8 bytes, ASCII "RTATNSR\0".
inline constexpr char     LQT_RTA_MAGIC[8] = {'R', 'T', 'A', 'T', 'N', 'S', 'R', '\0'};

// ------------------------------ Fixed sizes ---------------------------------
// DEVIATION D-001 (operator-ratified 2026-06-04): canon labels the header
// "32 bytes" yet specifies three uint64 offsets at 0x0C/0x14/0x1C (-> 36 bytes).
// We honor the uint64 offset fields (required for >4GB models) and fix the
// header at 36 bytes. See docs/SPEC_COMPLIANCE.md D-001.
inline constexpr uint32_t LQT_HEADER_SIZE = 36;
inline constexpr uint32_t LQT_FOOTER_SIZE = 64;
inline constexpr uint32_t LQT_FOOTER_RESERVED = 40; // footer reserved tail bytes

// ------------------------------ Alignment -----------------------------------
// Canon §2 / §B.1: codebooks on 64B cache lines, tensor indices on 16B,
// delta buffers on 4B; TLV values padded to 4B.
inline constexpr uint32_t LQT_ALIGN_CODEBOOK = 64;
inline constexpr uint32_t LQT_ALIGN_INDEX    = 16;
inline constexpr uint32_t LQT_ALIGN_DELTA    = 4;
inline constexpr uint32_t LQT_ALIGN_TLV      = 4;

// --------------------------- Header flag bitmask ----------------------------
// Canon §2.2 Flags (uint16). Bits 8-15 reserved.
enum class HeaderFlag : uint16_t {
    HasDeltas      = 1u << 0,
    HasSparseMasks = 1u << 1,
    Align64        = 1u << 2,
    BigEndian      = 1u << 3,
    SelfModifying  = 1u << 4,
    SignedEdits    = 1u << 5,
    Compressed     = 1u << 6,
    Sharded        = 1u << 7,
};

// ----------------------------- TLV chunk types ------------------------------
// Canon §2.3 Core Chunk Types. 0x0012 (Recursive Weight Metadata) from the
// v1.3 binary spec is included alongside the canon registry.
enum class ChunkType : uint16_t {
    ModelHyperparameters = 0x0001,
    TensorDescriptors    = 0x0002,
    ModuleDefinitions    = 0x0003, // JSON DAG
    MutationRules        = 0x0004, // JSON
    CodebookTable        = 0x0005,
    DeltaTable           = 0x0006,
    SparseMaskTable      = 0x0007,
    Vocabulary           = 0x0008,
    KvCacheConfig        = 0x0009,
    SelfModificationRules= 0x000A, // JSON
    EditLog              = 0x000B,
    ShardingInfo         = 0x000C,
    CompressionDict      = 0x000D,
    MemoryMappingHints   = 0x000E,
    AccessControlList    = 0x000F,
    PerformanceMetrics   = 0x0010,
    // DEVIATION D-024: 0x0011 was unused in the v1.3 registry. RecursiveWeightMeta
    // (0x0012) is RtaBlock structural data only (see rta.h); it never carried an
    // actual RecursiveWeight quintuple despite the name. This chunk carries the
    // real per-tensor RecursiveWeight (W={B,Phi,R,T,epsilon}) table consumed by
    // LqtModel::reconstruct() for TensorType::RecursiveTensor. See
    // docs/SPEC_COMPLIANCE.md D-024.
    RecursiveWeightTable = 0x0011,
    RecursiveWeightMeta  = 0x0012, // RTA-specific (v1.3 spec §3 registry)
    ExtensionBlock       = 0xFFFF,
};

// --------------------------- Tensor element dtype ---------------------------
// Canon enumerates "FP16, INT8, etc." without fixed codes. DEVIATION D-003:
// we assign canonical dtype codes (documented in SPEC_COMPLIANCE.md D-003).
enum class DType : uint8_t {
    FP32 = 0,
    FP16 = 1,
    BF16 = 2,
    INT8 = 3,
    INT4 = 4, // packed: 2 values per byte, low nibble first
    UINT8 = 5,
    INT16 = 6,
    INT32 = 7,
};

// Size in bits of a single element of the given dtype.
constexpr uint32_t dtype_bits(DType d) {
    switch (d) {
        case DType::FP32:  return 32;
        case DType::FP16:  return 16;
        case DType::BF16:  return 16;
        case DType::INT8:  return 8;
        case DType::INT4:  return 4;
        case DType::UINT8: return 8;
        case DType::INT16: return 16;
        case DType::INT32: return 32;
    }
    return 0;
}

// --------------------------- Tensor descriptor type -------------------------
// Canon §2.3 Tensor Descriptor tensor_type switch.
enum class TensorType : uint8_t {
    Standard        = 0,
    RecursiveTensor = 1, // RTA
};

// --------------------------- Tensor descriptor flags ------------------------
// Canon §2.3 descriptor flags (uint16). Bits 6-15 reserved.
enum class TensorFlag : uint16_t {
    Trainable    = 1u << 0,
    Protected    = 1u << 1,
    Shared       = 1u << 2,
    HotSwappable = 1u << 3,
    Cached       = 1u << 4,
    Checkpoint   = 1u << 5,
};

// ------------------------- RTA sparse encoding methods ----------------------
// Binary Spec v1.3 §4 (offsets 0x00-0x05).
enum class SparseEncoding : uint8_t {
    Uniform         = 0x00,
    PerDimension    = 0x01,
    Hierarchical    = 0x02,
    RLE             = 0x03,
    CompressedBitmap= 0x04,
    CsrCscCsf       = 0x05,
};

// ------------------------- RTA distribution / dim flags ---------------------
// Binary Spec v1.3 §4 Dimension Block.
enum class RtaDistribution : uint32_t {
    Normal      = 0,
    Uniform     = 1,
    Exponential = 2,
    Custom      = 3,
};

enum class RtaDimFlag : uint8_t {
    CustomDistribution = 1u << 0,
    PatternComp        = 1u << 1,
    Quantized          = 1u << 2,
    SelfReferential    = 1u << 3,
    Fractal            = 1u << 4,
    DoublePrecision    = 1u << 5,
};

// RTA fixed rank (canon: "Rank: Fixed at 5"). Load-bearing invariant.
inline constexpr uint8_t LQT_RTA_RANK = 5;

// --------------------------- Mutation operation type ------------------------
// Canon §4.4 edit-log mutation_type (uint8). 0/1/2 match the archaeological
// writer's operation_type; extended for the full canon §4.1 mutation set.
enum class MutationType : uint8_t {
    CodebookEdit    = 0,
    DeltaUpdate     = 1,
    ModuleSwap      = 2,
    SparseMaskUpdate= 3,
    Hyperparameter  = 4,
    CodebookExpand  = 5,
    // D-025 (additive): logged RecursiveWeight bucket edits and logged
    // RecursiveTensor attach/detach, so a live model whose values are
    // RecursiveWeight buckets can be edited, hash-chained and rolled back.
    RecursiveWeightEdit = 6,
    TensorAttach        = 7,
    TensorDetach        = 8,
};

// ----------------------------- Reference kinds ------------------------------
// Binary Spec v1.3 §4 Reference Block (Direct / Transformed / Fractal).
enum class ReferenceKind : uint8_t {
    Direct      = 0,
    Transformed = 1, // matrix-based
    Fractal     = 2, // iterative
};

// ------------------------------ Flag helpers --------------------------------
template <typename E>
constexpr uint16_t to_u16(E e) { return static_cast<uint16_t>(e); }

inline bool flag_set(uint16_t bits, HeaderFlag f) { return (bits & to_u16(f)) != 0; }
inline bool flag_set(uint16_t bits, TensorFlag f) { return (bits & to_u16(f)) != 0; }
inline void flag_assign(uint16_t& bits, HeaderFlag f, bool on) {
    if (on) bits |= to_u16(f); else bits &= static_cast<uint16_t>(~to_u16(f));
}
inline void flag_assign(uint16_t& bits, TensorFlag f, bool on) {
    if (on) bits |= to_u16(f); else bits &= static_cast<uint16_t>(~to_u16(f));
}

} // namespace lqt
