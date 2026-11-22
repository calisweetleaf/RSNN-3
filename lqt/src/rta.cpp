// lqt/src/rta.cpp — Recursive Tensor Architecture (RTA) implementation.
//
// Council module: A5 (RTA blocks).
// Spec: LQT Binary File Format Specification v1.3 §4 and §5.
//
// Implements all design decisions defined in include/lqt/rta.h (DD-01..DD-07):
//   DD-01  24-byte dimension block concrete layout
//   DD-02  dim_sizes (5 x u32) immediately follow the dimension block
//   DD-03  Internal metadata KV wire format
//   DD-04  Sparse section: tag + u32 length + payload for all 6 encodings
//   DD-05  Reference block: Direct / Transformed / Fractal
//   DD-06  Full RTA block wire layout (magic → metadata → dims → sparse →
//          references → CRC-64)
//   DD-07  CRC-64 coverage (all bytes before the 8-byte trailing CRC field)

#include "lqt/rta.h"

#include <cstring>
#include <stdexcept>

#include "lqt/crc.h"
#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ============================================================================
// Internal helpers
// ============================================================================
namespace {

// Write the DD-03 metadata KV block to w.
void write_metadata(ByteWriter& w,
                    const std::vector<std::pair<std::string, std::string>>& kv)
{
    if (kv.size() > 0xFFFFu) {
        throw ValidationError("RTA metadata: too many KV pairs (> 65535)");
    }
    w.put_u16(static_cast<uint16_t>(kv.size()));
    for (const auto& p : kv) {
        if (p.first.size() > 0xFFFFu) {
            throw ValidationError("RTA metadata: key exceeds 65535 bytes");
        }
        w.put_u16(static_cast<uint16_t>(p.first.size()));
        w.put_bytes(p.first.data(), p.first.size());
        if (p.second.size() > 0xFFFFFFFFull) {
            throw ValidationError("RTA metadata: value exceeds 4 GiB");
        }
        w.put_u32(static_cast<uint32_t>(p.second.size()));
        w.put_bytes(p.second.data(), p.second.size());
    }
}

// Read the DD-03 metadata KV block from r.
std::vector<std::pair<std::string, std::string>> read_metadata(ByteReader& r) {
    std::vector<std::pair<std::string, std::string>> result;
    const uint16_t count = r.get_u16();
    result.reserve(count);
    for (uint16_t i = 0; i < count; ++i) {
        const uint16_t klen = r.get_u16();
        r.require(klen);
        std::string key(reinterpret_cast<const char*>(r.current()), klen);
        r.skip(klen);
        const uint32_t vlen = r.get_u32();
        r.require(vlen);
        std::string val(reinterpret_cast<const char*>(r.current()), vlen);
        r.skip(vlen);
        result.emplace_back(std::move(key), std::move(val));
    }
    return result;
}

} // namespace

// ============================================================================
// RtaDimensionBlock
// ============================================================================

void RtaDimensionBlock::validate() const {
    if (rank != LQT_RTA_RANK) {
        throw FormatError(
            std::string("RTA rank must be ") + std::to_string(LQT_RTA_RANK) +
            ", got " + std::to_string(rank));
    }
}

void RtaDimensionBlock::serialize(ByteWriter& w) const {
    // DD-01: 24-byte dimension block layout.
    //   offset  0: rank (u8)
    //   offset  1: distribution (u32)
    //   offset  5..15: reserved_a (11 bytes = 0)
    //   offset 16: reserved_b (1 byte = 0)
    //   offset 17: flags (u8)
    //   offset 18..23: reserved_c (6 bytes = 0)
    const size_t start = w.size();
    w.put_u8(rank);                                     //  0: 1 byte
    w.put_u32(static_cast<uint32_t>(distribution));    //  1: 4 bytes -> pos 5
    w.put_zeros(11);                                    //  5: 11 bytes -> pos 16
    w.put_zeros(1);                                     // 16: 1 byte  -> pos 17
    w.put_u8(flags);                                    // 17: 1 byte  -> pos 18
    w.put_zeros(6);                                     // 18: 6 bytes -> pos 24
    const size_t written = w.size() - start;
    // Compile-time invariant: layout produces exactly 24 bytes.
    if (written != 24) {
        throw FormatError("RtaDimensionBlock: serialized != 24 bytes (internal bug)");
    }

    // DD-02: 5 x u32 dim_sizes immediately after the 24-byte block.
    for (int i = 0; i < 5; ++i) {
        w.put_u32(dim_sizes[i]);
    }
    // Total dimension section: 44 bytes.
}

RtaDimensionBlock RtaDimensionBlock::parse(ByteReader& r) {
    // The reader must have at least 44 bytes (24 + 5*4) available.
    r.require(44);

    RtaDimensionBlock d;
    const size_t base = r.position();

    // offset 0: rank
    d.rank = r.get_u8();

    // offset 1: distribution (u32)
    d.distribution = static_cast<RtaDistribution>(r.get_u32());

    // offset 5..15: reserved_a (11 bytes) — skip
    r.skip(11);

    // offset 16: reserved_b (1 byte) — skip
    r.skip(1);

    // offset 17: flags (u8)
    d.flags = r.get_u8();

    // offset 18..23: reserved_c (6 bytes) — skip
    r.skip(6);

    // Verify we consumed exactly 24 bytes.
    if (r.position() - base != 24) {
        throw FormatError("RtaDimensionBlock: parse consumed != 24 bytes (internal bug)");
    }

    // DD-02: 5 x u32 dim_sizes.
    for (int i = 0; i < 5; ++i) {
        d.dim_sizes[i] = r.get_u32();
    }

    d.validate(); // throws FormatError if rank != 5
    return d;
}

// ============================================================================
// RtaReference
// ============================================================================

void RtaReference::serialize(ByteWriter& w) const {
    w.put_u8(static_cast<uint8_t>(kind));
    w.put_u32(target);

    switch (kind) {
        case ReferenceKind::Direct:
            // No additional fields.
            break;

        case ReferenceKind::Transformed:
            w.put_u32(mat_rows);
            w.put_u32(mat_cols);
            {
                const uint64_t expected = static_cast<uint64_t>(mat_rows) * mat_cols;
                if (matrix.size() != expected) {
                    throw ValidationError(
                        "RtaReference: matrix size mismatch with mat_rows * mat_cols");
                }
                for (float v : matrix) w.put_f32(v);
            }
            break;

        case ReferenceKind::Fractal:
            w.put_u32(iterations);
            w.put_u32(static_cast<uint32_t>(params.size()));
            for (float p : params) w.put_f32(p);
            break;
    }
}

RtaReference RtaReference::parse(ByteReader& r) {
    RtaReference ref;
    const uint8_t k = r.get_u8();
    if (k > 2) {
        throw FormatError(
            std::string("RtaReference: unknown kind ") + std::to_string(k));
    }
    ref.kind   = static_cast<ReferenceKind>(k);
    ref.target = r.get_u32();

    switch (ref.kind) {
        case ReferenceKind::Direct:
            break;

        case ReferenceKind::Transformed: {
            ref.mat_rows = r.get_u32();
            ref.mat_cols = r.get_u32();
            const uint64_t n = static_cast<uint64_t>(ref.mat_rows) * ref.mat_cols;
            ref.matrix.resize(n);
            for (uint64_t i = 0; i < n; ++i) ref.matrix[i] = r.get_f32();
            break;
        }

        case ReferenceKind::Fractal: {
            ref.iterations = r.get_u32();
            const uint32_t np = r.get_u32();
            ref.params.resize(np);
            for (uint32_t i = 0; i < np; ++i) ref.params[i] = r.get_f32();
            break;
        }
    }

    return ref;
}

// ============================================================================
// Sparse payload builders / parsers
// ============================================================================

// --- 0x00 Uniform -----------------------------------------------------------
std::vector<uint8_t> sparse_build_uniform(uint32_t element_count) {
    ByteWriter w;
    w.put_u32(element_count);
    return w.take();
}

uint32_t sparse_parse_uniform(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    return r.get_u32();
}

// --- 0x01 PerDimension ------------------------------------------------------
std::vector<uint8_t> sparse_build_per_dimension(const PerDimMap& maps) {
    ByteWriter w;
    if (maps.size() > 255) {
        throw ValidationError("sparse_build_per_dimension: ndim > 255");
    }
    w.put_u8(static_cast<uint8_t>(maps.size()));
    for (const auto& entries : maps) {
        w.put_u32(static_cast<uint32_t>(entries.size()));
        for (const auto& e : entries) {
            w.put_u32(e.slice_index);
            w.put_f32(e.density);
        }
    }
    return w.take();
}

PerDimMap sparse_parse_per_dimension(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    const uint8_t ndim = r.get_u8();
    PerDimMap result(ndim);
    for (uint8_t d = 0; d < ndim; ++d) {
        const uint32_t count = r.get_u32();
        result[d].resize(count);
        for (uint32_t i = 0; i < count; ++i) {
            result[d][i].slice_index = r.get_u32();
            result[d][i].density     = r.get_f32();
        }
    }
    return result;
}

// --- 0x02 Hierarchical ------------------------------------------------------
std::vector<uint8_t> sparse_build_hierarchical(const HierarchicalSparse& h) {
    ByteWriter w;
    w.put_u32(h.block_size);
    w.put_u32(h.total_elements);
    w.put_u32(static_cast<uint32_t>(h.l0_words.size()));
    for (uint64_t word : h.l0_words) w.put_u64(word);
    w.put_u32(static_cast<uint32_t>(h.l1_indices.size()));
    for (uint32_t idx : h.l1_indices) w.put_u32(idx);
    return w.take();
}

HierarchicalSparse sparse_parse_hierarchical(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    HierarchicalSparse h;
    h.block_size     = r.get_u32();
    h.total_elements = r.get_u32();
    const uint32_t l0_count = r.get_u32();
    h.l0_words.resize(l0_count);
    for (uint32_t i = 0; i < l0_count; ++i) h.l0_words[i] = r.get_u64();
    const uint32_t l1_count = r.get_u32();
    h.l1_indices.resize(l1_count);
    for (uint32_t i = 0; i < l1_count; ++i) h.l1_indices[i] = r.get_u32();
    return h;
}

// --- 0x03 RLE ---------------------------------------------------------------
std::vector<uint8_t> sparse_build_rle(const std::vector<RleRun>& runs) {
    ByteWriter w;
    w.put_u32(static_cast<uint32_t>(runs.size()));
    for (const auto& run : runs) {
        w.put_u32(run.start);
        w.put_u32(run.length);
        w.put_f32(run.value);
    }
    return w.take();
}

std::vector<RleRun> sparse_parse_rle(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    const uint32_t count = r.get_u32();
    std::vector<RleRun> runs(count);
    for (uint32_t i = 0; i < count; ++i) {
        runs[i].start  = r.get_u32();
        runs[i].length = r.get_u32();
        runs[i].value  = r.get_f32();
    }
    return runs;
}

// --- 0x04 CompressedBitmap --------------------------------------------------
std::vector<uint8_t> sparse_build_bitmap(uint32_t num_elements,
                                          const std::vector<uint64_t>& words)
{
    ByteWriter w;
    w.put_u32(num_elements);
    w.put_u32(static_cast<uint32_t>(words.size()));
    for (uint64_t word : words) w.put_u64(word);
    return w.take();
}

BitmapSparse sparse_parse_bitmap(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    BitmapSparse b;
    b.num_elements = r.get_u32();
    const uint32_t wcount = r.get_u32();
    b.words.resize(wcount);
    for (uint32_t i = 0; i < wcount; ++i) b.words[i] = r.get_u64();
    return b;
}

// --- 0x05 CSR ---------------------------------------------------------------
std::vector<uint8_t> sparse_build_csr(const CsrSparse& csr) {
    const uint32_t nnz = static_cast<uint32_t>(csr.col_idx.size());
    if (csr.row_ptr.size() != static_cast<size_t>(csr.nrows) + 1) {
        throw ValidationError("sparse_build_csr: row_ptr.size() != nrows+1");
    }
    if (csr.values.size() != nnz) {
        throw ValidationError("sparse_build_csr: values.size() != nnz");
    }
    ByteWriter w;
    w.put_u32(csr.nrows);
    w.put_u32(nnz);
    for (uint32_t v : csr.row_ptr) w.put_u32(v);
    for (uint32_t c : csr.col_idx) w.put_u32(c);
    for (float   f : csr.values)   w.put_f32(f);
    return w.take();
}

CsrSparse sparse_parse_csr(const std::vector<uint8_t>& payload) {
    ByteReader r(payload);
    CsrSparse csr;
    csr.nrows = r.get_u32();
    const uint32_t nnz = r.get_u32();
    csr.row_ptr.resize(static_cast<size_t>(csr.nrows) + 1);
    for (auto& v : csr.row_ptr) v = r.get_u32();
    csr.col_idx.resize(nnz);
    for (auto& c : csr.col_idx)  c = r.get_u32();
    csr.values.resize(nnz);
    for (auto& f : csr.values)   f = r.get_f32();
    return csr;
}

// ============================================================================
// RtaBlock::validate
// ============================================================================

void RtaBlock::validate() const {
    dims.validate(); // rank == 5

    // Verify dim_sizes are non-zero (a 0-length dimension is meaningless).
    for (int i = 0; i < 5; ++i) {
        if (dims.dim_sizes[i] == 0) {
            throw ValidationError(
                std::string("RTA dim_sizes[") + std::to_string(i) + "] == 0");
        }
    }
}

// ============================================================================
// RtaBlock::serialize
// ============================================================================

void RtaBlock::serialize(ByteWriter& w) const {
    // We write the block body into a separate writer so we can CRC it,
    // then append to the caller's writer.
    ByteWriter body;

    // 1. Magic (8 bytes).
    body.put_bytes(LQT_RTA_MAGIC, 8);

    // 2. Metadata KV block (DD-03).
    write_metadata(body, metadata);

    // 3. Dimension block (24 bytes) + dim_sizes (20 bytes) (DD-01, DD-02).
    dims.serialize(body);

    // 4. Sparse section (DD-04): tag(u8) + length(u32) + payload.
    body.put_u8(static_cast<uint8_t>(sparse_encoding));
    body.put_u32(static_cast<uint32_t>(sparse_payload.size()));
    body.put_bytes(sparse_payload.data(), sparse_payload.size());

    // 5. Reference block (DD-05): count(u32) + entries.
    body.put_u32(static_cast<uint32_t>(references.size()));
    for (const auto& ref : references) {
        ref.serialize(body);
    }

    // 6. CRC-64 over all body bytes (DD-07).
    const std::vector<uint8_t>& body_bytes = body.bytes();
    const uint64_t crc = crc64(body_bytes.data(), body_bytes.size());

    // Append body + CRC to the caller's writer.
    w.put_bytes(body_bytes.data(), body_bytes.size());
    w.put_u64(crc);
}

// ============================================================================
// RtaBlock::parse
// ============================================================================

RtaBlock RtaBlock::parse(ByteReader& r) {
    // Record the start position so we can CRC the body.
    const size_t block_start = r.position();

    // 1. Verify magic (8 bytes).
    r.require(8);
    if (std::memcmp(r.current(), LQT_RTA_MAGIC, 8) != 0) {
        throw FormatError("RtaBlock: bad magic (expected \"RTATNSR\\0\")");
    }
    r.skip(8);

    // 2. Metadata KV block (DD-03).
    RtaBlock blk;
    blk.metadata = read_metadata(r);

    // 3. Dimension block + dim_sizes (DD-01, DD-02). validate() inside parse().
    blk.dims = RtaDimensionBlock::parse(r);

    // 4. Sparse section (DD-04).
    const uint8_t enc_tag = r.get_u8();
    if (enc_tag > 0x05) {
        throw FormatError(
            std::string("RtaBlock: unknown sparse encoding tag 0x") +
            std::to_string(enc_tag));
    }
    blk.sparse_encoding = static_cast<SparseEncoding>(enc_tag);
    const uint32_t payload_len = r.get_u32();
    r.require(payload_len);
    blk.sparse_payload.assign(r.current(), r.current() + payload_len);
    r.skip(payload_len);

    // 5. Reference block (DD-05).
    const uint32_t ref_count = r.get_u32();
    blk.references.reserve(ref_count);
    for (uint32_t i = 0; i < ref_count; ++i) {
        blk.references.push_back(RtaReference::parse(r));
    }

    // 6. CRC-64 check (DD-07).
    // Body = all bytes from block_start up to (but not including) the CRC field.
    const size_t body_end = r.position();
    const size_t body_len = body_end - block_start;
    // Re-read body bytes for hashing.
    const uint64_t computed_crc = crc64(r.current() - body_len, body_len);
    const uint64_t stored_crc   = r.get_u64();
    if (computed_crc != stored_crc) {
        throw IntegrityError(
            "RtaBlock: CRC-64 mismatch — block is corrupted or tampered");
    }

    return blk;
}

// ============================================================================
// Patch 4 additions (2026-06-04)
// ============================================================================
// rta_analysis wrappers will be wired here once rta_analysis.cpp is compiled.
// See rta_analysis.h. The intended surface is:
//
//   float RtaBlock::compute_entropy() const;
//   std::vector<float> RtaBlock::get_values() const;
//
// These will collect non-zero sparse values from sparse_payload (decoded via
// the appropriate sparse_parse_* helper for the active sparse_encoding) and
// delegate to rta_entropy() / return the flat value vector. Method
// declarations will be added to RtaBlock in include/lqt/rta.h once the
// rta_analysis header lands; no rta.h edit is performed in this patch
// because the implementation is not yet wired.

} // namespace lqt
