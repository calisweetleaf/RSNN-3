// tests/test_rta.cpp — RTA (Agent A5) round-trip and integrity tests.
//
// Covers per the spec:
//   - Magic round-trip (writes + parses, confirms magic verified)
//   - rank != 5 raises FormatError
//   - All 6 sparse encodings round-trip a known pattern
//   - All 3 reference kinds round-trip (Direct, Transformed, Fractal)
//   - Dimension flags + distribution round-trip
//   - Corrupting one body byte causes IntegrityError (CRC-64)
//   - Metadata KV round-trip
//   - Dimension sizes round-trip
//   - Empty metadata + empty references (minimal block)

#include <cstdint>
#include <cstring>
#include <vector>
#include <string>

#include "lqt/crc.h"
#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/rta.h"
#include "test_framework.h"

using namespace lqt;

// ============================================================================
// Helper: serialize a block, then parse it back.
// ============================================================================
static RtaBlock roundtrip(const RtaBlock& blk) {
    ByteWriter w;
    blk.serialize(w);
    ByteReader r(w.bytes());
    return RtaBlock::parse(r);
}

// ============================================================================
// Magic round-trip
// ============================================================================
TEST_CASE(rta_magic_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 4;
    blk.dims.dim_sizes[1] = 4;
    blk.dims.dim_sizes[2] = 4;
    blk.dims.dim_sizes[3] = 4;
    blk.dims.dim_sizes[4] = 4;
    blk.sparse_payload = sparse_build_uniform(4 * 4 * 4 * 4 * 4);

    ByteWriter w;
    blk.serialize(w);

    // First 8 bytes must be LQT_RTA_MAGIC.
    const auto& bytes = w.bytes();
    CHECK(bytes.size() >= 8);
    CHECK(std::memcmp(bytes.data(), LQT_RTA_MAGIC, 8) == 0);

    // Parse succeeds.
    ByteReader r(bytes);
    RtaBlock back = RtaBlock::parse(r);
    CHECK_EQ(back.dims.rank, static_cast<uint8_t>(5));
}

// ============================================================================
// Bad magic is rejected with FormatError
// ============================================================================
TEST_CASE(rta_bad_magic_rejected) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    ByteWriter w;
    blk.serialize(w);
    auto bytes = w.take();

    // Corrupt the magic.
    bytes[0] ^= 0xFF;

    ByteReader r(bytes);
    CHECK_THROWS_AS(RtaBlock::parse(r), FormatError);
}

// ============================================================================
// rank != 5 raises FormatError
// ============================================================================
TEST_CASE(rta_rank_not_5_rejected) {
    // Build a valid block, then manually corrupt the rank byte in the
    // serialised output (the 24-byte dimension block starts after the 8-byte
    // magic and the 2-byte metadata count with 0 entries; rank is at offset 0
    // within the dimension block).
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 2;
    blk.dims.dim_sizes[1] = 2;
    blk.dims.dim_sizes[2] = 2;
    blk.dims.dim_sizes[3] = 2;
    blk.dims.dim_sizes[4] = 2;
    blk.sparse_payload = sparse_build_uniform(32);

    ByteWriter w;
    blk.serialize(w);
    auto bytes = w.take();

    // Locate rank byte: offset 10 in the block (8 magic + 2 empty KV count).
    // Write rank = 3.
    bytes[10] = 3;

    // The CRC will also be wrong, but rank check happens before CRC, so we
    // expect FormatError specifically (not IntegrityError).
    ByteReader r(bytes);
    CHECK_THROWS_AS(RtaBlock::parse(r), FormatError);
}

// ============================================================================
// validate() throws FormatError if rank set to non-5
// ============================================================================
TEST_CASE(rta_validate_rank_enforced) {
    RtaDimensionBlock d;
    d.rank = 3; // wrong
    CHECK_THROWS_AS(d.validate(), FormatError);
}

// ============================================================================
// Dimension flags + distribution round-trip
// ============================================================================
TEST_CASE(rta_dim_flags_distribution_roundtrip) {
    RtaBlock blk;
    blk.dims.distribution = RtaDistribution::Exponential;
    blk.dims.set_flag(RtaDimFlag::Fractal, true);
    blk.dims.set_flag(RtaDimFlag::Quantized, true);
    blk.dims.set_flag(RtaDimFlag::DoublePrecision, false);
    blk.dims.dim_sizes[0] = 8;
    blk.dims.dim_sizes[1] = 16;
    blk.dims.dim_sizes[2] = 4;
    blk.dims.dim_sizes[3] = 2;
    blk.dims.dim_sizes[4] = 32;
    blk.sparse_payload = sparse_build_uniform(8 * 16 * 4 * 2 * 32);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint32_t>(back.dims.distribution),
             static_cast<uint32_t>(RtaDistribution::Exponential));
    CHECK(back.dims.has_flag(RtaDimFlag::Fractal));
    CHECK(back.dims.has_flag(RtaDimFlag::Quantized));
    CHECK(!back.dims.has_flag(RtaDimFlag::DoublePrecision));
    CHECK_EQ(back.dims.dim_sizes[0], 8u);
    CHECK_EQ(back.dims.dim_sizes[1], 16u);
    CHECK_EQ(back.dims.dim_sizes[2], 4u);
    CHECK_EQ(back.dims.dim_sizes[3], 2u);
    CHECK_EQ(back.dims.dim_sizes[4], 32u);
}

// ============================================================================
// Metadata KV round-trip
// ============================================================================
TEST_CASE(rta_metadata_kv_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.metadata.push_back({"layer_name",  "transformer.attn"});
    blk.metadata.push_back({"precision",   "int4"});
    blk.metadata.push_back({"sparsity",    "0.9"});
    blk.sparse_payload = sparse_build_uniform(1);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.metadata.size(), static_cast<size_t>(3));
    CHECK_EQ(back.metadata[0].first,  std::string("layer_name"));
    CHECK_EQ(back.metadata[0].second, std::string("transformer.attn"));
    CHECK_EQ(back.metadata[1].first,  std::string("precision"));
    CHECK_EQ(back.metadata[1].second, std::string("int4"));
    CHECK_EQ(back.metadata[2].first,  std::string("sparsity"));
    CHECK_EQ(back.metadata[2].second, std::string("0.9"));
}

// ============================================================================
// Metadata empty (minimal block)
// ============================================================================
TEST_CASE(rta_empty_metadata_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    RtaBlock back = roundtrip(blk);
    CHECK(back.metadata.empty());
    CHECK(back.references.empty());
}

// ============================================================================
// Sparse encoding 0x00 Uniform round-trip
// ============================================================================
TEST_CASE(rta_sparse_uniform_roundtrip) {
    const uint32_t N = 1024u;
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 4;
    blk.dims.dim_sizes[1] = 4;
    blk.dims.dim_sizes[2] = 4;
    blk.dims.dim_sizes[3] = 4;
    blk.dims.dim_sizes[4] = 4;
    blk.sparse_encoding  = SparseEncoding::Uniform;
    blk.sparse_payload   = sparse_build_uniform(N);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::Uniform));
    const uint32_t elem = sparse_parse_uniform(back.sparse_payload);
    CHECK_EQ(elem, N);
}

// ============================================================================
// Sparse encoding 0x01 PerDimension round-trip
// ============================================================================
TEST_CASE(rta_sparse_per_dimension_roundtrip) {
    PerDimMap maps(5);
    maps[0] = {{0, 0.8f}, {2, 0.5f}, {7, 0.1f}};
    maps[1] = {{1, 1.0f}};
    maps[2] = {};
    maps[3] = {{0, 0.3f}, {1, 0.3f}};
    maps[4] = {{3, 0.9f}};

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 8;
    blk.dims.dim_sizes[1] = 8;
    blk.dims.dim_sizes[2] = 8;
    blk.dims.dim_sizes[3] = 8;
    blk.dims.dim_sizes[4] = 8;
    blk.sparse_encoding = SparseEncoding::PerDimension;
    blk.sparse_payload  = sparse_build_per_dimension(maps);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::PerDimension));

    PerDimMap recovered = sparse_parse_per_dimension(back.sparse_payload);
    CHECK_EQ(recovered.size(), static_cast<size_t>(5));
    CHECK_EQ(recovered[0].size(), static_cast<size_t>(3));
    CHECK_EQ(recovered[0][0].slice_index, 0u);
    CHECK_NEAR(recovered[0][0].density, 0.8f, 1e-6f);
    CHECK_EQ(recovered[0][2].slice_index, 7u);
    CHECK_EQ(recovered[1].size(), static_cast<size_t>(1));
    CHECK_NEAR(recovered[1][0].density, 1.0f, 1e-6f);
    CHECK_EQ(recovered[2].size(), static_cast<size_t>(0));
    CHECK_EQ(recovered[3].size(), static_cast<size_t>(2));
    CHECK_EQ(recovered[4].size(), static_cast<size_t>(1));
}

// ============================================================================
// Sparse encoding 0x02 Hierarchical round-trip
// ============================================================================
TEST_CASE(rta_sparse_hierarchical_roundtrip) {
    HierarchicalSparse h;
    h.block_size     = 64;
    h.total_elements = 512;
    // Set bits 0, 3, 7 in the L0 word (positions 0, 3, 7 of the flat index).
    h.l0_words = { (1ull << 0) | (1ull << 3) | (1ull << 7) };
    // L1: non-zero flat indices within those blocks.
    h.l1_indices = {0, 3, 192, 193, 448, 449, 450};

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 8;
    blk.dims.dim_sizes[1] = 8;
    blk.dims.dim_sizes[2] = 8;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::Hierarchical;
    blk.sparse_payload  = sparse_build_hierarchical(h);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::Hierarchical));

    HierarchicalSparse rec = sparse_parse_hierarchical(back.sparse_payload);
    CHECK_EQ(rec.block_size,     64u);
    CHECK_EQ(rec.total_elements, 512u);
    CHECK_EQ(rec.l0_words.size(), static_cast<size_t>(1));
    CHECK_EQ(rec.l0_words[0],
             (1ull << 0) | (1ull << 3) | (1ull << 7));
    CHECK_EQ(rec.l1_indices.size(), static_cast<size_t>(7));
    CHECK_EQ(rec.l1_indices[0], 0u);
    CHECK_EQ(rec.l1_indices[6], 450u);
}

// ============================================================================
// Sparse encoding 0x03 RLE round-trip
// ============================================================================
TEST_CASE(rta_sparse_rle_roundtrip) {
    std::vector<RleRun> runs = {
        {0,   16, 1.0f},
        {64,  4,  0.5f},
        {200, 1,  -0.25f},
    };

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 8;
    blk.dims.dim_sizes[1] = 8;
    blk.dims.dim_sizes[2] = 8;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::RLE;
    blk.sparse_payload  = sparse_build_rle(runs);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::RLE));

    std::vector<RleRun> rec = sparse_parse_rle(back.sparse_payload);
    CHECK_EQ(rec.size(), static_cast<size_t>(3));
    CHECK_EQ(rec[0].start, 0u);
    CHECK_EQ(rec[0].length, 16u);
    CHECK_NEAR(rec[0].value, 1.0f, 1e-6f);
    CHECK_EQ(rec[1].start, 64u);
    CHECK_EQ(rec[1].length, 4u);
    CHECK_NEAR(rec[1].value, 0.5f, 1e-6f);
    CHECK_EQ(rec[2].start, 200u);
    CHECK_NEAR(rec[2].value, -0.25f, 1e-6f);
}

// ============================================================================
// Sparse encoding 0x04 CompressedBitmap round-trip
// ============================================================================
TEST_CASE(rta_sparse_compressed_bitmap_roundtrip) {
    // 128 elements, first word has bits 0, 3, 7 set; second word all zeros.
    const uint32_t num_elements = 128;
    std::vector<uint64_t> words = {
        (1ull << 0) | (1ull << 3) | (1ull << 7),
        0ull
    };

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 2;
    blk.dims.dim_sizes[1] = 8;
    blk.dims.dim_sizes[2] = 8;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::CompressedBitmap;
    blk.sparse_payload  = sparse_build_bitmap(num_elements, words);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::CompressedBitmap));

    BitmapSparse rec = sparse_parse_bitmap(back.sparse_payload);
    CHECK_EQ(rec.num_elements, 128u);
    CHECK_EQ(rec.words.size(), static_cast<size_t>(2));
    CHECK_EQ(rec.words[0], (1ull << 0) | (1ull << 3) | (1ull << 7));
    CHECK_EQ(rec.words[1], 0ull);
}

// ============================================================================
// Sparse encoding 0x05 CSR round-trip
// ============================================================================
TEST_CASE(rta_sparse_csr_roundtrip) {
    // 3x4 sparse matrix: row 0 = {col1=1.5}, row1 = {col0=2.0, col3=-1.0},
    //                    row2 = {}
    CsrSparse csr;
    csr.nrows   = 3;
    csr.row_ptr = {0, 1, 3, 3};
    csr.col_idx = {1, 0, 3};
    csr.values  = {1.5f, 2.0f, -1.0f};

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 3;
    blk.dims.dim_sizes[1] = 4;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::CsrCscCsf;
    blk.sparse_payload  = sparse_build_csr(csr);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(static_cast<uint8_t>(back.sparse_encoding),
             static_cast<uint8_t>(SparseEncoding::CsrCscCsf));

    CsrSparse rec = sparse_parse_csr(back.sparse_payload);
    CHECK_EQ(rec.nrows, 3u);
    CHECK_EQ(rec.row_ptr.size(), static_cast<size_t>(4));
    CHECK_EQ(rec.row_ptr[0], 0u);
    CHECK_EQ(rec.row_ptr[1], 1u);
    CHECK_EQ(rec.row_ptr[2], 3u);
    CHECK_EQ(rec.row_ptr[3], 3u);
    CHECK_EQ(rec.col_idx.size(), static_cast<size_t>(3));
    CHECK_EQ(rec.col_idx[0], 1u);
    CHECK_EQ(rec.col_idx[1], 0u);
    CHECK_EQ(rec.col_idx[2], 3u);
    CHECK_EQ(rec.values.size(), static_cast<size_t>(3));
    CHECK_NEAR(rec.values[0], 1.5f, 1e-6f);
    CHECK_NEAR(rec.values[1], 2.0f, 1e-6f);
    CHECK_NEAR(rec.values[2], -1.0f, 1e-6f);
}

// ============================================================================
// Reference kind Direct round-trip
// ============================================================================
TEST_CASE(rta_reference_direct_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    RtaReference ref;
    ref.kind   = ReferenceKind::Direct;
    ref.target = 42;
    blk.references.push_back(ref);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.references.size(), static_cast<size_t>(1));
    CHECK_EQ(static_cast<uint8_t>(back.references[0].kind),
             static_cast<uint8_t>(ReferenceKind::Direct));
    CHECK_EQ(back.references[0].target, 42u);
}

// ============================================================================
// Reference kind Transformed (matrix) round-trip
// ============================================================================
TEST_CASE(rta_reference_transformed_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    RtaReference ref;
    ref.kind     = ReferenceKind::Transformed;
    ref.target   = 7;
    ref.mat_rows = 2;
    ref.mat_cols = 3;
    // 2x3 row-major: [1.0, 2.0, 3.0; 4.0, 5.0, 6.0]
    ref.matrix   = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f};
    blk.references.push_back(ref);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.references.size(), static_cast<size_t>(1));
    const auto& r0 = back.references[0];
    CHECK_EQ(static_cast<uint8_t>(r0.kind),
             static_cast<uint8_t>(ReferenceKind::Transformed));
    CHECK_EQ(r0.target, 7u);
    CHECK_EQ(r0.mat_rows, 2u);
    CHECK_EQ(r0.mat_cols, 3u);
    CHECK_EQ(r0.matrix.size(), static_cast<size_t>(6));
    CHECK_NEAR(r0.matrix[0], 1.0f, 1e-6f);
    CHECK_NEAR(r0.matrix[4], 5.0f, 1e-6f);
    CHECK_NEAR(r0.matrix[5], 6.0f, 1e-6f);
}

// ============================================================================
// Reference kind Fractal (iterative + params) round-trip
// ============================================================================
TEST_CASE(rta_reference_fractal_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    RtaReference ref;
    ref.kind       = ReferenceKind::Fractal;
    ref.target     = 99;
    ref.iterations = 7;
    ref.params     = {0.5f, -0.25f, 1.414f, 3.14159f};
    blk.references.push_back(ref);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.references.size(), static_cast<size_t>(1));
    const auto& r0 = back.references[0];
    CHECK_EQ(static_cast<uint8_t>(r0.kind),
             static_cast<uint8_t>(ReferenceKind::Fractal));
    CHECK_EQ(r0.target, 99u);
    CHECK_EQ(r0.iterations, 7u);
    CHECK_EQ(r0.params.size(), static_cast<size_t>(4));
    CHECK_NEAR(r0.params[0], 0.5f, 1e-5f);
    CHECK_NEAR(r0.params[1], -0.25f, 1e-5f);
    CHECK_NEAR(r0.params[2], 1.414f, 1e-4f);
    CHECK_NEAR(r0.params[3], 3.14159f, 1e-4f);
}

// ============================================================================
// Multiple references of mixed kinds in a single block
// ============================================================================
TEST_CASE(rta_reference_multiple_mixed_kinds) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 2;
    blk.dims.dim_sizes[1] = 2;
    blk.dims.dim_sizes[2] = 2;
    blk.dims.dim_sizes[3] = 2;
    blk.dims.dim_sizes[4] = 2;
    blk.sparse_payload = sparse_build_uniform(32);

    RtaReference r0;
    r0.kind = ReferenceKind::Direct; r0.target = 10;

    RtaReference r1;
    r1.kind = ReferenceKind::Transformed; r1.target = 20;
    r1.mat_rows = 1; r1.mat_cols = 2; r1.matrix = {0.0f, 1.0f};

    RtaReference r2;
    r2.kind = ReferenceKind::Fractal; r2.target = 30;
    r2.iterations = 3; r2.params = {0.1f, 0.2f};

    blk.references = {r0, r1, r2};

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.references.size(), static_cast<size_t>(3));
    CHECK_EQ(back.references[0].target, 10u);
    CHECK_EQ(static_cast<uint8_t>(back.references[0].kind),
             static_cast<uint8_t>(ReferenceKind::Direct));
    CHECK_EQ(back.references[1].target, 20u);
    CHECK_EQ(back.references[1].mat_rows, 1u);
    CHECK_NEAR(back.references[1].matrix[1], 1.0f, 1e-6f);
    CHECK_EQ(back.references[2].target, 30u);
    CHECK_EQ(back.references[2].iterations, 3u);
    CHECK_NEAR(back.references[2].params[1], 0.2f, 1e-6f);
}

// ============================================================================
// CRC-64: corrupting one body byte raises IntegrityError
// ============================================================================
TEST_CASE(rta_crc64_detects_corruption) {
    RtaBlock blk;
    blk.dims.distribution = RtaDistribution::Normal;
    blk.dims.dim_sizes[0] = 4;
    blk.dims.dim_sizes[1] = 4;
    blk.dims.dim_sizes[2] = 4;
    blk.dims.dim_sizes[3] = 4;
    blk.dims.dim_sizes[4] = 4;
    blk.metadata.push_back({"key", "value"});
    blk.sparse_payload = sparse_build_uniform(1024);

    ByteWriter w;
    blk.serialize(w);
    auto bytes = w.take();

    // Corrupt byte at index 20 (inside the body, before the CRC).
    bytes[20] ^= 0x01;

    ByteReader r(bytes);
    CHECK_THROWS_AS(RtaBlock::parse(r), IntegrityError);
}

// ============================================================================
// CRC-64: valid block parses cleanly (no corruption)
// ============================================================================
TEST_CASE(rta_crc64_clean_block_passes) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_payload = sparse_build_uniform(1);

    // This should NOT throw.
    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.dims.rank, static_cast<uint8_t>(5));
}

// ============================================================================
// Dimension block serializes to exactly 44 bytes (24 + 5*4) within larger block
// ============================================================================
TEST_CASE(rta_dimension_block_exact_size) {
    RtaDimensionBlock d;
    d.rank = 5;
    d.distribution = RtaDistribution::Uniform;
    d.flags = 0;
    for (int i = 0; i < 5; ++i) d.dim_sizes[i] = static_cast<uint32_t>(i + 1);

    ByteWriter w;
    d.serialize(w);
    CHECK_EQ(w.size(), static_cast<size_t>(44)); // 24-byte block + 5*4 dim_sizes
}

// ============================================================================
// Dimension block flags byte is at byte offset 17 within the 24-byte region
// ============================================================================
TEST_CASE(rta_dimension_block_flags_at_offset_17) {
    RtaDimensionBlock d;
    d.rank = 5;
    d.distribution = RtaDistribution::Normal;
    d.flags = static_cast<uint8_t>(RtaDimFlag::SelfReferential) |
              static_cast<uint8_t>(RtaDimFlag::Fractal);
    for (int i = 0; i < 5; ++i) d.dim_sizes[i] = 1;

    ByteWriter w;
    d.serialize(w);
    const auto& bytes = w.bytes();

    // Offset 17 within the 44-byte output must equal our flags value.
    CHECK_EQ(bytes[17], d.flags);
    // Offset 0 must be rank.
    CHECK_EQ(bytes[0], static_cast<uint8_t>(5));
}

// ============================================================================
// All distributions round-trip correctly
// ============================================================================
TEST_CASE(rta_all_distributions_roundtrip) {
    const RtaDistribution dists[] = {
        RtaDistribution::Normal,
        RtaDistribution::Uniform,
        RtaDistribution::Exponential,
        RtaDistribution::Custom,
    };
    for (auto dist : dists) {
        RtaBlock blk;
        blk.dims.distribution = dist;
        blk.dims.dim_sizes[0] = 1;
        blk.dims.dim_sizes[1] = 1;
        blk.dims.dim_sizes[2] = 1;
        blk.dims.dim_sizes[3] = 1;
        blk.dims.dim_sizes[4] = 1;
        blk.sparse_payload = sparse_build_uniform(1);

        RtaBlock back = roundtrip(blk);
        CHECK_EQ(static_cast<uint32_t>(back.dims.distribution),
                 static_cast<uint32_t>(dist));
    }
}

// ============================================================================
// Block with zero references serializes and parses correctly
// ============================================================================
TEST_CASE(rta_zero_references_roundtrip) {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 3;
    blk.dims.dim_sizes[1] = 3;
    blk.dims.dim_sizes[2] = 3;
    blk.dims.dim_sizes[3] = 3;
    blk.dims.dim_sizes[4] = 3;
    blk.sparse_payload = sparse_build_uniform(243);

    RtaBlock back = roundtrip(blk);
    CHECK(back.references.empty());
}

// ============================================================================
// CSR with zero non-zeros (empty sparse) round-trips
// ============================================================================
TEST_CASE(rta_csr_empty_sparse) {
    CsrSparse csr;
    csr.nrows   = 4;
    csr.row_ptr = {0, 0, 0, 0, 0}; // all rows empty
    // col_idx and values are empty vectors

    RtaBlock blk;
    blk.dims.dim_sizes[0] = 4;
    blk.dims.dim_sizes[1] = 4;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::CsrCscCsf;
    blk.sparse_payload  = sparse_build_csr(csr);

    RtaBlock back = roundtrip(blk);
    CsrSparse rec = sparse_parse_csr(back.sparse_payload);
    CHECK_EQ(rec.nrows, 4u);
    CHECK_EQ(rec.row_ptr.size(), static_cast<size_t>(5));
    CHECK(rec.col_idx.empty());
    CHECK(rec.values.empty());
}

// ============================================================================
// Large metadata value round-trip
// ============================================================================
TEST_CASE(rta_large_metadata_value_roundtrip) {
    std::string big_val(1024, 'X');  // 1 KiB value
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.metadata.push_back({"big_json", big_val});
    blk.sparse_payload = sparse_build_uniform(1);

    RtaBlock back = roundtrip(blk);
    CHECK_EQ(back.metadata.size(), static_cast<size_t>(1));
    CHECK_EQ(back.metadata[0].first, std::string("big_json"));
    CHECK_EQ(back.metadata[0].second.size(), static_cast<size_t>(1024));
    CHECK_EQ(back.metadata[0].second, big_val);
}

int main() { return lqttest::run_all(); }
