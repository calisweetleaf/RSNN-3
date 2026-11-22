// lqt/rta.h — Recursive Tensor Architecture (RTA) 5-dimensional block.
//
// Council module: A5 (RTA blocks).
// Spec: LQT Binary File Format Specification v1.3 §4 "Recursive Tensor
//       Architecture (RTA) Block Specifications" and §5 "Five-Dimensional
//       Semantic Logic and Recursive Operations".
// Briefing: §2 "5D Semantic Structure".
//
// ============================================================================
// DESIGN DECISIONS
// ============================================================================
//
// DD-01: 24-BYTE DIMENSION BLOCK LAYOUT
//   The spec pins rank (u8) at offset 0, distribution (u32) starting somewhere,
//   and flags (u8) exactly at offset 17, but does not fully pin every byte.
//   We define the following concrete 24-byte layout (all fields little-endian):
//
//   Offset  Size  Field
//   ------  ----  -----
//    0       1    rank            (u8, must equal LQT_RTA_RANK == 5)
//    1       4    distribution    (u32, RtaDistribution)
//    5      11    reserved_a      (11 bytes, written as 0, ignored on parse)
//   16       1    reserved_b      (1 byte, written as 0, ignored on parse)
//   17       1    flags           (u8, RtaDimFlag bitmask)
//   18       6    reserved_c      (6 bytes, written as 0, ignored on parse)
//   Total:  24 bytes
//
//   Rationale: rank at 0 allows an immediate validity check; distribution
//   immediately follows at 1 (natural packing); flags at exactly 17 as
//   required by spec; remaining 11 bytes are zero-reserved for forward
//   compatibility.
//
// DD-02: DIMENSION SIZES IMMEDIATELY FOLLOW THE 24-BYTE DIMENSION BLOCK
//   The spec says the five per-dimension sizes (d0..d4) are part of the block
//   structure. We serialize them as 5 x uint32_t (20 bytes) immediately after
//   the 24-byte dimension block (at block-relative offset 24). They are NOT
//   part of the 24-byte spec-mandated block; they extend it. Total dimension
//   section: 44 bytes.
//
//   Dimension semantics (§5):
//     dim_sizes[0] = d0  Feature / embedding dimension
//     dim_sizes[1] = d1  Pattern / template dimension
//     dim_sizes[2] = d2  Temporal / sequential dimension
//     dim_sizes[3] = d3  Scale / fractal dimension
//     dim_sizes[4] = d4  Channel / multimodal dimension
//
// DD-03: INTERNAL METADATA TLV FORMAT
//   The spec calls for "internal TLV block for tensor-local metadata
//   (key-value pairs, UTF-8)". We define a simple KV wire format:
//
//     [u16 count]
//     count x {
//       [u16 key_len]   [key_len bytes of UTF-8 key]
//       [u32 val_len]   [val_len bytes of UTF-8 value]
//     }
//
//   Rationale: u16 key length caps keys at 65535 bytes (ample); u32 value
//   length supports large JSON blobs. No alignment padding is applied since
//   the metadata block is consumed sequentially. An empty metadata block
//   is encoded as a single u16 == 0 (2 bytes).
//
// DD-04: SPARSE SECTION WIRE FORMAT
//   Each sparse section starts with a single u8 encoding tag (matching
//   SparseEncoding enum), followed immediately by a u32 payload_length,
//   then payload_length bytes of payload. This allows unknown encodings to
//   be skipped by a reader that does not support them.
//
//   Per-encoding payload layouts:
//
//   0x00 UNIFORM:
//     No density map is required (all elements present at uniform density).
//     Payload: [u32 element_count] — total number of logical elements.
//     Length: 4 bytes.
//
//   0x01 PER_DIMENSION:
//     One density map per axis. Each map is a list of (index, density) pairs
//     that record which slices along that axis are non-empty.
//     Payload: [u8 ndim] then for each dim: [u32 num_entries]
//              then num_entries x [u32 slice_index][f32 density_value].
//     A density of 0.0 means the slice is empty; 1.0 means fully dense.
//
//   0x02 HIERARCHICAL:
//     Multi-level density maps encoded as a 2-level tree.
//     Level-0 (coarse): block_size-aligned bitmask over the flat index space.
//     Level-1 (fine):   per-set-bit entries listing the actual non-zero
//                       flat indices within that block.
//     Payload: [u32 block_size][u32 total_elements]
//              [u32 L0_word_count] [L0_word_count x u64 bitmask words]
//              [u32 L1_entry_count] [L1_entry_count x u32 flat_index]
//     Each set bit i in L0 means block i*block_size..(i+1)*block_size-1
//     contains at least one non-zero element; L1 then lists every non-zero
//     flat index in those blocks.
//
//   0x03 RLE:
//     Run-length encoding for contiguous spans.
//     Each run: [u32 start_index][u32 run_length][f32 value]
//     Payload: [u32 num_runs] then num_runs x {u32, u32, f32} = 12 bytes each.
//
//   0x04 COMPRESSED_BITMAP:
//     A flat bit-array over the linearised index space: bit i is set if
//     element i is non-zero.
//     Payload: [u32 num_elements][u32 word_count]
//              [word_count x u64 little-endian bitmap words]
//     Bit packing: element i is in word[i/64], bit (i%64) (LSB = index 0).
//
//   0x05 CSR_CSC_CSF:
//     Compressed Sparse Row / Column / Fiber encoding (generalised to 5D).
//     We implement CSR semantics: row pointers + column indices + values.
//     Payload: [u32 nrows][u32 nnz]
//              [nrows+1 x u32 row_ptr]   -- cumulative nnz per row
//              [nnz x u32 col_idx]       -- column (or fibre) indices
//              [nnz x f32 values]        -- non-zero float values
//
// DD-05: REFERENCE BLOCK WIRE FORMAT
//   The reference section begins with [u32 num_references]. Each reference
//   entry is serialised as:
//     [u8  kind]         (ReferenceKind: 0=Direct, 1=Transformed, 2=Fractal)
//     [u32 target]       (target node index, always present)
//     kind==0 (Direct):  no further fields.
//     kind==1 (Transformed):
//       [u32 mat_rows][u32 mat_cols]
//       [mat_rows*mat_cols x f32] transform matrix, row-major
//     kind==2 (Fractal):
//       [u32 iterations]
//       [u32 param_count]
//       [param_count x f32] iteration parameters
//
// DD-06: OVERALL RTA BLOCK WIRE FORMAT
//   All multi-byte integers are little-endian. The full layout is:
//     [8  bytes] magic            LQT_RTA_MAGIC ("RTATNSR\0")
//     [variable] metadata KV      DD-03 format
//     [24 bytes] dimension block  DD-01 format (rank, distribution, flags)
//     [20 bytes] dim_sizes        DD-02 format (5 x u32)
//     [variable] sparse section   DD-04 format (tag + length + payload)
//     [variable] reference block  DD-05 format
//     [8  bytes] CRC-64           crc64 over all preceding bytes of this block
//                                 (starting at magic, ending before crc field)
//
// DD-07: CRC-64 COVERAGE
//   The CRC-64 (CRC-64/XZ per crc.h) covers every byte from the start of the
//   magic through the last byte before the 8-byte CRC field itself. On parse,
//   the stored CRC is read, the body bytes are re-hashed, and a mismatch
//   throws IntegrityError.
//
// ============================================================================
#pragma once

#include <cstdint>
#include <string>
#include <utility>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ============================================================================
// RtaDimensionBlock — the 24-byte fixed region + 5 dim_sizes (DD-01 / DD-02)
// ============================================================================
struct RtaDimensionBlock {
    uint8_t          rank         = LQT_RTA_RANK;     // must equal 5
    RtaDistribution  distribution = RtaDistribution::Normal;
    uint8_t          flags        = 0;                // RtaDimFlag bitmask
    uint32_t         dim_sizes[5] = {1, 1, 1, 1, 1}; // d0..d4 (DD-02)

    // Check flag bit.
    bool has_flag(RtaDimFlag f) const {
        return (flags & static_cast<uint8_t>(f)) != 0;
    }
    void set_flag(RtaDimFlag f, bool on) {
        if (on) flags |= static_cast<uint8_t>(f);
        else    flags &= static_cast<uint8_t>(~static_cast<uint8_t>(f));
    }

    // Serialize: 24-byte block (DD-01) then 5 x u32 dim_sizes (DD-02).
    // Total: 44 bytes.
    void serialize(ByteWriter& w) const;

    // Parse the 24-byte block + 5 x u32 dim_sizes.
    static RtaDimensionBlock parse(ByteReader& r);

    // Throw FormatError if rank != LQT_RTA_RANK.
    void validate() const;
};

// ============================================================================
// RtaReference — one entry in the Reference Block (DD-05)
// ============================================================================
struct RtaReference {
    ReferenceKind         kind       = ReferenceKind::Direct;
    uint32_t              target     = 0;     // target node index (all kinds)

    // Transformed: row-major transform matrix
    uint32_t              mat_rows   = 0;
    uint32_t              mat_cols   = 0;
    std::vector<float>    matrix;            // mat_rows * mat_cols elements

    // Fractal: iterative parameters
    uint32_t              iterations = 0;
    std::vector<float>    params;

    void serialize(ByteWriter& w) const;
    static RtaReference parse(ByteReader& r);
};

// ============================================================================
// RtaBlock — the top-level 5D RTA block (DD-06)
// ============================================================================
struct RtaBlock {
    // Tensor-local metadata KV pairs (UTF-8 keys and values, DD-03).
    std::vector<std::pair<std::string, std::string>> metadata;

    // Dimension information (rank + distribution + flags + 5 dim_sizes).
    RtaDimensionBlock dims;

    // Sparse section (DD-04).
    SparseEncoding           sparse_encoding = SparseEncoding::Uniform;
    std::vector<uint8_t>     sparse_payload; // raw bytes of the payload region

    // Reference block (DD-05).
    std::vector<RtaReference> references;

    // Serialize the full RTA block into w (DD-06 layout, CRC-64 appended).
    void serialize(ByteWriter& w) const;

    // Parse a complete RTA block from r; verifies magic, rank, and CRC-64.
    static RtaBlock parse(ByteReader& r);

    // Validate structural invariants; throws FormatError / ValidationError.
    void validate() const;
};

// ============================================================================
// Sparse payload builder helpers
// (These functions build the typed payload bytes for each SparseEncoding.
//  Call the appropriate builder, then assign sparse_encoding + sparse_payload
//  on the RtaBlock.)
// ============================================================================

// 0x00 Uniform: element_count only.
std::vector<uint8_t> sparse_build_uniform(uint32_t element_count);
uint32_t             sparse_parse_uniform(const std::vector<uint8_t>& payload);

// 0x01 PerDimension: per-axis (slice_index, density) entry lists.
struct PerDimEntry  { uint32_t slice_index; float density; };
using  PerDimMap    = std::vector<std::vector<PerDimEntry>>; // one vec per dim
std::vector<uint8_t> sparse_build_per_dimension(const PerDimMap& maps);
PerDimMap            sparse_parse_per_dimension(const std::vector<uint8_t>& payload);

// 0x02 Hierarchical: 2-level block bitmask + L1 flat indices.
struct HierarchicalSparse {
    uint32_t              block_size      = 64;
    uint32_t              total_elements  = 0;
    std::vector<uint64_t> l0_words;    // coarse bitmask
    std::vector<uint32_t> l1_indices;  // fine non-zero flat indices
};
std::vector<uint8_t>  sparse_build_hierarchical(const HierarchicalSparse& h);
HierarchicalSparse    sparse_parse_hierarchical(const std::vector<uint8_t>& payload);

// 0x03 RLE: runs of (start_index, run_length, value).
struct RleRun { uint32_t start; uint32_t length; float value; };
std::vector<uint8_t> sparse_build_rle(const std::vector<RleRun>& runs);
std::vector<RleRun>  sparse_parse_rle(const std::vector<uint8_t>& payload);

// 0x04 CompressedBitmap: flat bit array over linearised index space.
std::vector<uint8_t>  sparse_build_bitmap(uint32_t num_elements,
                                          const std::vector<uint64_t>& words);
struct BitmapSparse { uint32_t num_elements; std::vector<uint64_t> words; };
BitmapSparse          sparse_parse_bitmap(const std::vector<uint8_t>& payload);

// 0x05 CSR/CSC/CSF: row_ptr + col_idx + values.
struct CsrSparse {
    uint32_t              nrows = 0;
    std::vector<uint32_t> row_ptr;  // nrows+1 entries
    std::vector<uint32_t> col_idx;  // nnz entries
    std::vector<float>    values;   // nnz entries
};
std::vector<uint8_t> sparse_build_csr(const CsrSparse& csr);
CsrSparse            sparse_parse_csr(const std::vector<uint8_t>& payload);

} // namespace lqt
