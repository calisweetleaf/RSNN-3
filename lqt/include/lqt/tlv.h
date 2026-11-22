// lqt/tlv.h — TLV metadata system and chunk-type registry.
//
// Council module: A2 (TLV metadata).
// Canon: lqt.md §2.3 "Metadata Chunks (TLV Format)"; Binary Spec v1.3 §3.
//
// DESIGN DECISION 1 (parse region boundary):
//   MetadataSection::parse() consumes exactly `region_bytes` from the reader.
//   The metadata region is bounded by [header.metadata_offset, tensor_offset).
//   Reading proceeds entry-by-entry until all region_bytes are exhausted.
//   Entries with unknown Type values are preserved verbatim (forward compat).
//   A partial header (< 6 bytes remaining) at end-of-region is an error.
//
// DESIGN DECISION 2 (padding excluded from Length):
//   Length encodes only the raw value byte count, NOT the trailing zero-padding.
//   Padding bytes (to reach LQT_ALIGN_TLV=4 boundary) follow the value silently.
//   This matches canon §2.3 diagram: "padded to 4-byte alignment" is distinct
//   from the Length field. pad_to() is used on the ByteWriter after each value.
//
// DESIGN DECISION 3 (hyperparameters key encoding):
//   Keys use put_string() / get_string() (uint32 length-prefix + UTF-8 bytes),
//   matching the canonical format description "[key:str][value:float32] pairs"
//   and the existing foundation ByteWriter::put_string convention.
//
// DESIGN DECISION 4 (table layout byte order):
//   TableEntry wire layout is [id:u16][offset:u64][size:u64] = 18 bytes/entry.
//   All fields little-endian (canonical file byte order). No intra-entry padding
//   is inserted; entries are packed contiguously. This is consistent with canon
//   §2.3 table spec and the foundation's ByteWriter little-endian convention.
#pragma once

#include <cstdint>
#include <string>
#include <utility>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ---------------------------------------------------------------------------
// TlvEntry — a single on-disk TLV record (type + raw value bytes).
// The value does NOT include padding bytes; padding is an on-wire artifact.
// ---------------------------------------------------------------------------
struct TlvEntry {
    uint16_t             type;   // raw type code (may be unknown)
    std::vector<uint8_t> value;  // exact value bytes (Length == value.size())
};

// ---------------------------------------------------------------------------
// MetadataSection — ordered list of TlvEntry items with serialise/parse.
// ---------------------------------------------------------------------------
class MetadataSection {
public:
    MetadataSection() = default;

    // Append a known chunk type with its value blob.
    void add(ChunkType ct, std::vector<uint8_t> value) {
        entries_.push_back(TlvEntry{to_u16(ct), std::move(value)});
    }

    // Append a raw (potentially unknown) type with its value blob.
    void add_raw(uint16_t type, std::vector<uint8_t> value) {
        entries_.push_back(TlvEntry{type, std::move(value)});
    }

    // First entry matching the given chunk type, or nullptr if absent.
    const TlvEntry* find(ChunkType ct) const {
        const uint16_t t = to_u16(ct);
        for (const auto& e : entries_) {
            if (e.type == t) return &e;
        }
        return nullptr;
    }

    // All entries matching the given raw type code.
    std::vector<const TlvEntry*> find_all(uint16_t type) const {
        std::vector<const TlvEntry*> out;
        for (const auto& e : entries_) {
            if (e.type == type) out.push_back(&e);
        }
        return out;
    }

    // Write every entry in order: [Type:u16][Length:u32][Value][padding].
    // padding is zero bytes to the next LQT_ALIGN_TLV=4 boundary.
    // The Length field encodes only the value byte count, not the padding.
    void serialize(ByteWriter& w) const {
        for (const auto& e : entries_) {
            w.put_u16(e.type);
            w.put_u32(static_cast<uint32_t>(e.value.size()));
            w.put_bytes(e.value.data(), e.value.size());
            w.pad_to(LQT_ALIGN_TLV);
        }
    }

    // Parse exactly region_bytes from the reader, collecting all TLV entries.
    // Unknown types are preserved verbatim for forward compatibility.
    // Throws FormatError on truncation or a partial entry header.
    static MetadataSection parse(ByteReader& r, size_t region_bytes) {
        MetadataSection sec;
        const size_t start = r.position();
        const size_t end   = start + region_bytes;

        if (r.size() < end) {
            throw FormatError("MetadataSection::parse: region extends past buffer");
        }

        while (r.position() < end) {
            const size_t remaining_region = end - r.position();
            // Minimum entry header is 6 bytes (u16 type + u32 length).
            if (remaining_region < 6) {
                throw FormatError(
                    "MetadataSection::parse: partial TLV header at end of region");
            }

            const uint16_t type = r.get_u16();
            const uint32_t len  = r.get_u32();

            // Value bytes must fit within the region.
            const size_t after_value = r.position() + len;
            if (after_value > end) {
                throw FormatError(
                    "MetadataSection::parse: TLV value overruns region boundary");
            }

            std::vector<uint8_t> val(len);
            if (len > 0) r.get_bytes(val.data(), len);

            // Skip padding bytes (not part of Length, but consume from region).
            // Padding is computed from CURRENT reader position (absolute), not
            // from len alone — the 6-byte header shifts alignment.
            const size_t cur = r.position();
            const size_t pad = (LQT_ALIGN_TLV - (cur % LQT_ALIGN_TLV)) % LQT_ALIGN_TLV;
            if (pad > 0) {
                if (r.position() + pad > end) {
                    // Padding would cross region boundary — stop at end.
                    // Per DESIGN DECISION 1 we do NOT error here.
                    r.seek(end);
                } else {
                    r.skip(pad);
                }
            }

            sec.entries_.push_back(TlvEntry{type, std::move(val)});
        }

        return sec;
    }

    const std::vector<TlvEntry>& entries() const { return entries_; }

    // Replace the first entry matching `type`, or append a new one.
    // Used by set_json and any other helpers that upsert by type.
    void replace_or_add(uint16_t type, std::vector<uint8_t> value) {
        for (auto& e : entries_) {
            if (e.type == type) {
                e.value = std::move(value);
                return;
            }
        }
        entries_.push_back(TlvEntry{type, std::move(value)});
    }

private:
    std::vector<TlvEntry> entries_;
};

// ---------------------------------------------------------------------------
// TableEntry — on-disk record for Codebook/Delta/SparseMask tables (§2.3).
// Wire layout per entry: [id:u16][offset:u64][size:u64] = 18 bytes.
// ---------------------------------------------------------------------------
struct TableEntry {
    uint16_t id;
    uint64_t offset;
    uint64_t size;
};

// Encode a vector of TableEntry into a value-blob suitable for a TLV entry.
inline std::vector<uint8_t> encode_table(const std::vector<TableEntry>& entries) {
    ByteWriter w;
    for (const auto& e : entries) {
        w.put_u16(e.id);
        w.put_u64(e.offset);
        w.put_u64(e.size);
    }
    return w.take();
}

// Decode a value-blob into a vector of TableEntry.
// Throws FormatError if the blob length is not a multiple of 18 bytes.
inline std::vector<TableEntry> decode_table(const std::vector<uint8_t>& blob) {
    constexpr size_t ENTRY_SIZE = sizeof(uint16_t) + sizeof(uint64_t) + sizeof(uint64_t);
    if (blob.size() % ENTRY_SIZE != 0) {
        throw FormatError("decode_table: blob size is not a multiple of 18 bytes");
    }
    ByteReader r(blob);
    std::vector<TableEntry> out;
    out.reserve(blob.size() / ENTRY_SIZE);
    while (r.remaining() >= ENTRY_SIZE) {
        TableEntry e;
        e.id     = r.get_u16();
        e.offset = r.get_u64();
        e.size   = r.get_u64();
        out.push_back(e);
    }
    return out;
}

// ---------------------------------------------------------------------------
// Hyperparameters helpers (chunk 0x0001).
// Wire layout: sequence of [key:put_string][value:float32] pairs.
// put_string emits a uint32 length-prefix followed by raw UTF-8 bytes.
// ---------------------------------------------------------------------------
inline std::vector<uint8_t> encode_hyperparams(
    const std::vector<std::pair<std::string, float>>& params)
{
    ByteWriter w;
    for (const auto& p : params) {
        w.put_string(p.first);
        w.put_f32(p.second);
    }
    return w.take();
}

inline std::vector<std::pair<std::string, float>> decode_hyperparams(
    const std::vector<uint8_t>& blob)
{
    ByteReader r(blob);
    std::vector<std::pair<std::string, float>> out;
    while (r.remaining() > 0) {
        // Minimum: 4-byte string length prefix + 4-byte float = 8 bytes.
        // For an empty key: 4 + 0 + 4 = 8 bytes.
        if (r.remaining() < 8) {
            throw FormatError("decode_hyperparams: truncated pair entry");
        }
        std::string key = r.get_string();
        if (r.remaining() < 4) {
            throw FormatError("decode_hyperparams: truncated float value");
        }
        float val = r.get_f32();
        out.emplace_back(std::move(key), val);
    }
    return out;
}

// ---------------------------------------------------------------------------
// JSON-bearing chunk helpers (0x0003 ModuleDefinitions, 0x0004 MutationRules,
// 0x000A SelfModificationRules).
// The JSON is stored as raw UTF-8 bytes (no length prefix; the TLV Length
// field already encodes the byte count).
//
// DESIGN DECISION 5 (JSON storage):
//   JSON bytes are stored verbatim as the TLV value — no BOM, no null
//   terminator, no additional framing. This matches canon §2.3 which says
//   these chunks contain "JSON defining X". The caller is responsible for
//   valid UTF-8; we do not parse or validate JSON content.
// ---------------------------------------------------------------------------

// Helper: only ModuleDefinitions, MutationRules, SelfModificationRules
// are valid JSON bearer chunks. Enforce at runtime.
inline void check_json_chunk_type(ChunkType ct) {
    if (ct != ChunkType::ModuleDefinitions  &&
        ct != ChunkType::MutationRules       &&
        ct != ChunkType::SelfModificationRules)
    {
        throw ValidationError("set_json/get_json: chunk type is not a JSON bearer");
    }
}

// Upsert a JSON string into the section. If a matching entry already exists
// it is replaced; otherwise a new one is appended.
inline void set_json(MetadataSection& sec, ChunkType ct, const std::string& json) {
    check_json_chunk_type(ct);
    std::vector<uint8_t> blob(json.begin(), json.end());
    sec.replace_or_add(to_u16(ct), std::move(blob));
}

// Retrieve the JSON string for a JSON bearer chunk type.
// Returns an empty string if the chunk is absent (caller may also use find()).
inline std::string get_json(const MetadataSection& sec, ChunkType ct) {
    check_json_chunk_type(ct);
    const TlvEntry* e = sec.find(ct);
    if (!e) return {};
    return std::string(e->value.begin(), e->value.end());
}

} // namespace lqt
