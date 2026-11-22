// tests/test_tlv.cpp — TLV metadata system tests (A2).
//
// Council module: A2 (TLV metadata).
// Canon: lqt.md §2.3; Binary Spec v1.3 §3.
//
// Test coverage:
//   - Round-trip a MetadataSection with several known chunks + unknown type
//   - Unknown entry survives byte-identical across serialize/parse
//   - Each entry's serialized start is 4-byte aligned
//   - Padding bytes are NOT counted in the Length field
//   - TableEntry encode/decode round-trip
//   - Hyperparameter encode/decode round-trip
//   - find() returns nullptr for absent type
//   - Truncated buffer raises FormatError
//   - JSON helpers set_json / get_json round-trip
//   - JSON absent returns empty string
//   - JSON upsert replaces existing entry

#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/tlv.h"
#include "test_framework.h"

using namespace lqt;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
static std::vector<uint8_t> make_blob(std::initializer_list<uint8_t> il) {
    return std::vector<uint8_t>(il);
}

// ---------------------------------------------------------------------------
// Full round-trip: known chunks + unknown type preserved byte-identical.
// Also verifies alignment and Length-excludes-padding invariants.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_roundtrip_known_and_unknown) {
    MetadataSection sec;

    // 0x0001 Hyperparameters — 5-byte value (Length=5, 3-byte pad to reach 6+5+pad=16 total wire)
    std::vector<uint8_t> hp_blob = make_blob({0x01, 0x02, 0x03, 0x04, 0x05});
    sec.add(ChunkType::ModelHyperparameters, hp_blob);

    // 0x0003 ModuleDefinitions — 8-byte value (already 4-byte aligned, no pad)
    std::vector<uint8_t> mod_blob = make_blob({0xAA, 0xBB, 0xCC, 0xDD, 0x11, 0x22, 0x33, 0x44});
    sec.add(ChunkType::ModuleDefinitions, mod_blob);

    // 0xABCD — unknown type, 7-byte value (1-byte pad)
    constexpr uint16_t UNKNOWN_TYPE = 0xABCD;
    std::vector<uint8_t> unk_blob = make_blob({0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE, 0xFF});
    sec.add_raw(UNKNOWN_TYPE, unk_blob);

    // Serialize
    ByteWriter w;
    sec.serialize(w);
    const std::vector<uint8_t>& raw = w.bytes();

    // ---------- Verify alignment of each entry start ----------
    // Entry 0 starts at offset 0  (always 4-byte aligned)
    // Wire: [u16 type=2][u32 len=5][5 bytes value][3 bytes pad] = 14 bytes
    CHECK_EQ(raw.size() % LQT_ALIGN_TLV, static_cast<size_t>(0));

    // Manually walk the wire layout to check each entry's start offset.
    {
        ByteReader r(raw);
        size_t entry_start = 0;

        // Entry 0
        CHECK_EQ(r.position() % LQT_ALIGN_TLV, static_cast<size_t>(0));
        CHECK_EQ(r.get_u16(), to_u16(ChunkType::ModelHyperparameters));
        uint32_t len0 = r.get_u32();
        CHECK_EQ(len0, static_cast<uint32_t>(5));   // Length excludes padding
        r.skip(len0);
        r.align_to(LQT_ALIGN_TLV);
        entry_start = r.position();

        // Entry 1
        CHECK_EQ(entry_start % LQT_ALIGN_TLV, static_cast<size_t>(0));
        CHECK_EQ(r.get_u16(), to_u16(ChunkType::ModuleDefinitions));
        uint32_t len1 = r.get_u32();
        CHECK_EQ(len1, static_cast<uint32_t>(8));   // No padding needed
        r.skip(len1);
        r.align_to(LQT_ALIGN_TLV);
        entry_start = r.position();

        // Entry 2 (unknown)
        CHECK_EQ(entry_start % LQT_ALIGN_TLV, static_cast<size_t>(0));
        CHECK_EQ(r.get_u16(), UNKNOWN_TYPE);
        uint32_t len2 = r.get_u32();
        CHECK_EQ(len2, static_cast<uint32_t>(7));   // Length excludes 1-byte pad
        r.skip(len2);
        r.align_to(LQT_ALIGN_TLV);
    }

    // ---------- Parse back ----------
    ByteReader pr(raw);
    MetadataSection sec2 = MetadataSection::parse(pr, raw.size());

    const auto& entries = sec2.entries();
    CHECK_EQ(entries.size(), static_cast<size_t>(3));

    // Entry 0: known chunk, value bytes intact
    CHECK_EQ(entries[0].type, to_u16(ChunkType::ModelHyperparameters));
    CHECK_EQ(entries[0].value, hp_blob);

    // Entry 1: known chunk
    CHECK_EQ(entries[1].type, to_u16(ChunkType::ModuleDefinitions));
    CHECK_EQ(entries[1].value, mod_blob);

    // Entry 2: unknown type survives byte-identical
    CHECK_EQ(entries[2].type, UNKNOWN_TYPE);
    CHECK_EQ(entries[2].value, unk_blob);
}

// ---------------------------------------------------------------------------
// find() returns nullptr for absent type.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_find_absent_returns_nullptr) {
    MetadataSection sec;
    sec.add(ChunkType::ModelHyperparameters, make_blob({0x00}));

    CHECK(sec.find(ChunkType::TensorDescriptors) == nullptr);
    CHECK(sec.find(ChunkType::CodebookTable)      == nullptr);
}

// ---------------------------------------------------------------------------
// find() returns the correct entry when present.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_find_returns_entry_when_present) {
    MetadataSection sec;
    auto blob = make_blob({0x11, 0x22, 0x33});
    sec.add(ChunkType::CodebookTable, blob);

    const TlvEntry* e = sec.find(ChunkType::CodebookTable);
    CHECK(e != nullptr);
    CHECK_EQ(e->type, to_u16(ChunkType::CodebookTable));
    CHECK_EQ(e->value, blob);
}

// ---------------------------------------------------------------------------
// find_all() returns all matching entries for duplicate raw types.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_find_all_multiple_entries) {
    MetadataSection sec;
    sec.add_raw(0x1234, make_blob({0xAA}));
    sec.add_raw(0x5678, make_blob({0xBB}));
    sec.add_raw(0x1234, make_blob({0xCC}));

    auto results = sec.find_all(0x1234);
    CHECK_EQ(results.size(), static_cast<size_t>(2));
    CHECK_EQ(results[0]->value[0], static_cast<uint8_t>(0xAA));
    CHECK_EQ(results[1]->value[0], static_cast<uint8_t>(0xCC));

    auto none = sec.find_all(0xFFFF);
    CHECK_EQ(none.size(), static_cast<size_t>(0));
}

// ---------------------------------------------------------------------------
// Empty section serializes to zero bytes and parses to empty section.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_empty_section_roundtrip) {
    MetadataSection sec;
    ByteWriter w;
    sec.serialize(w);
    CHECK_EQ(w.size(), static_cast<size_t>(0));

    ByteReader r(w.bytes());
    MetadataSection sec2 = MetadataSection::parse(r, 0);
    CHECK_EQ(sec2.entries().size(), static_cast<size_t>(0));
}

// ---------------------------------------------------------------------------
// TableEntry encode/decode round-trip.
// ---------------------------------------------------------------------------
TEST_CASE(table_encode_decode_roundtrip) {
    std::vector<TableEntry> entries = {
        {0x0001, 0x000000001000, 0x0000000000800},
        {0x0002, 0x000000002000, 0x0000000001000},
        {0x0003, 0xFFFFFFFFFFFF, 0x0000000000001},
    };

    std::vector<uint8_t> blob = encode_table(entries);
    // Each entry = 2 + 8 + 8 = 18 bytes.
    CHECK_EQ(blob.size(), static_cast<size_t>(3 * 18));

    std::vector<TableEntry> decoded = decode_table(blob);
    CHECK_EQ(decoded.size(), entries.size());
    for (size_t i = 0; i < entries.size(); ++i) {
        CHECK_EQ(decoded[i].id,     entries[i].id);
        CHECK_EQ(decoded[i].offset, entries[i].offset);
        CHECK_EQ(decoded[i].size,   entries[i].size);
    }
}

// ---------------------------------------------------------------------------
// decode_table rejects blob with non-multiple-of-18 length.
// ---------------------------------------------------------------------------
TEST_CASE(table_decode_bad_length_throws) {
    std::vector<uint8_t> bad(17, 0x00);  // 17 is not a multiple of 18
    CHECK_THROWS_AS(decode_table(bad), FormatError);
}

// ---------------------------------------------------------------------------
// TableEntry round-trip inside a MetadataSection (full pipeline).
// ---------------------------------------------------------------------------
TEST_CASE(table_roundtrip_in_section) {
    std::vector<TableEntry> cb_entries = {
        {0x0010, 0x1000, 0x200},
        {0x0011, 0x1200, 0x400},
    };
    MetadataSection sec;
    sec.add(ChunkType::CodebookTable, encode_table(cb_entries));

    ByteWriter w;
    sec.serialize(w);
    ByteReader r(w.bytes());
    MetadataSection sec2 = MetadataSection::parse(r, w.size());

    const TlvEntry* e = sec2.find(ChunkType::CodebookTable);
    CHECK(e != nullptr);
    auto decoded = decode_table(e->value);
    CHECK_EQ(decoded.size(), cb_entries.size());
    CHECK_EQ(decoded[0].id, cb_entries[0].id);
    CHECK_EQ(decoded[1].offset, cb_entries[1].offset);
}

// ---------------------------------------------------------------------------
// Hyperparameter encode/decode round-trip.
// ---------------------------------------------------------------------------
TEST_CASE(hyperparams_encode_decode_roundtrip) {
    std::vector<std::pair<std::string, float>> params = {
        {"learning_rate", 0.001f},
        {"dropout",       0.1f},
        {"temperature",   0.8f},
        {"num_heads",     32.0f},
    };

    auto blob = encode_hyperparams(params);
    auto decoded = decode_hyperparams(blob);

    CHECK_EQ(decoded.size(), params.size());
    for (size_t i = 0; i < params.size(); ++i) {
        CHECK_EQ(decoded[i].first, params[i].first);
        // Float round-trip through IEEE 754 is exact for these values.
        CHECK(std::fabs(decoded[i].second - params[i].second) < 1e-6f);
    }
}

// ---------------------------------------------------------------------------
// Hyperparameter empty list round-trips to empty list.
// ---------------------------------------------------------------------------
TEST_CASE(hyperparams_empty_roundtrip) {
    auto blob = encode_hyperparams({});
    CHECK_EQ(blob.size(), static_cast<size_t>(0));
    auto decoded = decode_hyperparams(blob);
    CHECK_EQ(decoded.size(), static_cast<size_t>(0));
}

// ---------------------------------------------------------------------------
// Hyperparameter decode truncated blob throws FormatError.
// ---------------------------------------------------------------------------
TEST_CASE(hyperparams_decode_truncated_throws) {
    // Encode a valid pair and then truncate it.
    auto blob = encode_hyperparams({{"x", 1.0f}});
    CHECK(blob.size() >= 4);
    blob.resize(3);  // Truncate within the string length prefix
    CHECK_THROWS_AS(decode_hyperparams(blob), FormatError);
}

// ---------------------------------------------------------------------------
// Hyperparameters inside MetadataSection full pipeline.
// ---------------------------------------------------------------------------
TEST_CASE(hyperparams_roundtrip_in_section) {
    std::vector<std::pair<std::string, float>> params = {
        {"embed_dim", 512.0f},
        {"vocab_size", 32000.0f},
    };
    MetadataSection sec;
    sec.add(ChunkType::ModelHyperparameters, encode_hyperparams(params));

    ByteWriter w;
    sec.serialize(w);
    ByteReader r(w.bytes());
    MetadataSection sec2 = MetadataSection::parse(r, w.size());

    const TlvEntry* e = sec2.find(ChunkType::ModelHyperparameters);
    CHECK(e != nullptr);
    auto decoded = decode_hyperparams(e->value);
    CHECK_EQ(decoded.size(), params.size());
    CHECK_EQ(decoded[0].first, "embed_dim");
    CHECK(std::fabs(decoded[1].second - 32000.0f) < 1.0f);
}

// ---------------------------------------------------------------------------
// Truncated buffer raises FormatError.
// ---------------------------------------------------------------------------
TEST_CASE(parse_truncated_buffer_throws_format_error) {
    // Build a valid section and then truncate it in the middle of a value.
    MetadataSection sec;
    sec.add(ChunkType::ModelHyperparameters, make_blob({0x01, 0x02, 0x03, 0x04}));

    ByteWriter w;
    sec.serialize(w);
    auto raw = w.bytes();

    // Keep only the type+length header (6 bytes) but not the value.
    raw.resize(6);

    ByteReader r(raw);
    CHECK_THROWS_AS(MetadataSection::parse(r, raw.size()), FormatError);
}

// ---------------------------------------------------------------------------
// Truncated within type/length header raises FormatError.
// ---------------------------------------------------------------------------
TEST_CASE(parse_partial_header_throws_format_error) {
    // Write only 3 bytes — less than a TLV header (6 bytes).
    std::vector<uint8_t> buf = {0x01, 0x00, 0x01};
    ByteReader r(buf);
    CHECK_THROWS_AS(MetadataSection::parse(r, buf.size()), FormatError);
}

// ---------------------------------------------------------------------------
// Region extends past buffer raises FormatError.
// ---------------------------------------------------------------------------
TEST_CASE(parse_region_past_buffer_throws_format_error) {
    std::vector<uint8_t> buf(20, 0x00);
    ByteReader r(buf);
    CHECK_THROWS_AS(MetadataSection::parse(r, 100), FormatError);
}

// ---------------------------------------------------------------------------
// JSON helpers: set_json / get_json round-trip.
// ---------------------------------------------------------------------------
TEST_CASE(json_helpers_set_and_get_roundtrip) {
    MetadataSection sec;
    const std::string json_str = R"({"modules":[],"connections":[]})";
    set_json(sec, ChunkType::ModuleDefinitions, json_str);

    std::string back = get_json(sec, ChunkType::ModuleDefinitions);
    CHECK_EQ(back, json_str);
}

// ---------------------------------------------------------------------------
// get_json returns empty string for absent chunk.
// ---------------------------------------------------------------------------
TEST_CASE(json_get_absent_returns_empty) {
    MetadataSection sec;
    CHECK_EQ(get_json(sec, ChunkType::MutationRules), std::string{});
}

// ---------------------------------------------------------------------------
// set_json upserts: second call replaces instead of appending.
// ---------------------------------------------------------------------------
TEST_CASE(json_set_upserts_existing_entry) {
    MetadataSection sec;
    set_json(sec, ChunkType::SelfModificationRules, R"({"version":1})");
    set_json(sec, ChunkType::SelfModificationRules, R"({"version":2})");

    // Only one entry for this type.
    auto all = sec.find_all(to_u16(ChunkType::SelfModificationRules));
    CHECK_EQ(all.size(), static_cast<size_t>(1));
    CHECK_EQ(get_json(sec, ChunkType::SelfModificationRules), std::string{R"({"version":2})"});
}

// ---------------------------------------------------------------------------
// set_json rejects non-JSON bearer types.
// ---------------------------------------------------------------------------
TEST_CASE(json_set_wrong_type_throws_validation_error) {
    MetadataSection sec;
    CHECK_THROWS_AS(
        set_json(sec, ChunkType::CodebookTable, "{}"),
        ValidationError);
}

// ---------------------------------------------------------------------------
// JSON survives MetadataSection serialize/parse round-trip.
// ---------------------------------------------------------------------------
TEST_CASE(json_survives_section_roundtrip) {
    const std::string dag = R"({"modules":["attn"]})";
    MetadataSection sec;
    set_json(sec, ChunkType::ModuleDefinitions, dag);

    ByteWriter w;
    sec.serialize(w);
    ByteReader r(w.bytes());
    MetadataSection sec2 = MetadataSection::parse(r, w.size());

    CHECK_EQ(get_json(sec2, ChunkType::ModuleDefinitions), dag);
}

// ---------------------------------------------------------------------------
// Multiple different chunks together: order preserved through round-trip.
// ---------------------------------------------------------------------------
TEST_CASE(tlv_order_preserved_roundtrip) {
    MetadataSection sec;
    sec.add(ChunkType::ModelHyperparameters, make_blob({0x01}));
    sec.add(ChunkType::CodebookTable,        make_blob({0x02, 0x03}));
    sec.add(ChunkType::DeltaTable,           make_blob({0x04, 0x05, 0x06}));
    sec.add_raw(0x9999,                      make_blob({0x07}));
    sec.add(ChunkType::SparseMaskTable,      make_blob({0x08, 0x09, 0x0A, 0x0B}));

    ByteWriter w;
    sec.serialize(w);
    ByteReader r(w.bytes());
    MetadataSection sec2 = MetadataSection::parse(r, w.size());

    const auto& e = sec2.entries();
    CHECK_EQ(e.size(), static_cast<size_t>(5));
    CHECK_EQ(e[0].type, to_u16(ChunkType::ModelHyperparameters));
    CHECK_EQ(e[1].type, to_u16(ChunkType::CodebookTable));
    CHECK_EQ(e[2].type, to_u16(ChunkType::DeltaTable));
    CHECK_EQ(e[3].type, static_cast<uint16_t>(0x9999));
    CHECK_EQ(e[4].type, to_u16(ChunkType::SparseMaskTable));
    // Unknown type value byte-identical
    CHECK_EQ(e[3].value, make_blob({0x07}));
}

// ---------------------------------------------------------------------------
// Padding is NOT counted in Length field (explicit wire-level verification).
//
// Wire layout for a single 1-byte value entry:
//   [u16 type=0x0001][u32 len=0x00000001][u8 value=0xAB][u8 pad=0x00]
//   Offsets: 0-1 type, 2-5 length, 6 value, 7 pad.
//   Total = 8 bytes (7 rounded up to next multiple of 4 = 8; pad = 1 byte).
//   Length field is 1, not 2 (pad not counted).
// ---------------------------------------------------------------------------
TEST_CASE(padding_excluded_from_length_field) {
    MetadataSection sec;
    sec.add(ChunkType::ModelHyperparameters, make_blob({0xAB})); // 1 byte value

    ByteWriter w;
    sec.serialize(w);
    const auto& raw = w.bytes();

    // After type(2)+length(4)+value(1) = position 7.
    // pad_to(4): 7 % 4 = 3, pad = 4-3 = 1. Total = 8.
    CHECK_EQ(raw.size(), static_cast<size_t>(8));

    ByteReader r(raw);
    CHECK_EQ(r.get_u16(), to_u16(ChunkType::ModelHyperparameters));
    uint32_t len = r.get_u32();
    CHECK_EQ(len, static_cast<uint32_t>(1)); // Length==1, not padded to 4
    CHECK_EQ(r.get_u8(), static_cast<uint8_t>(0xAB));
    // 1 padding byte follows.
    CHECK_EQ(r.remaining(), static_cast<size_t>(1));
    CHECK_EQ(r.get_u8(), static_cast<uint8_t>(0x00));
}

// ---------------------------------------------------------------------------
// Verify total wire size for a 2-byte value entry (needs 2 bytes padding).
// After type(2)+length(4)+value(2) = position 8.
// 8 % 4 = 0 — already aligned, no padding. Total = 8.
// ---------------------------------------------------------------------------
TEST_CASE(no_padding_when_already_aligned) {
    MetadataSection sec;
    // 2-byte value: after header(6)+value(2) = position 8, already 4-aligned.
    sec.add(ChunkType::CodebookTable, make_blob({0x01, 0x02}));

    ByteWriter w;
    sec.serialize(w);
    // Wire: 2 (type) + 4 (length) + 2 (value) + 0 (pad) = 8 bytes.
    CHECK_EQ(w.size(), static_cast<size_t>(8));
}

int main() { return lqttest::run_all(); }
