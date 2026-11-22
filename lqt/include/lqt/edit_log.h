// lqt/edit_log.h — Append-only edit log with tamper-evident chain hashing.
//
// Council module: A7 (mutation safety layer).
// Canon: lqt.md §4.4 (edit-log entry format), §8 (tamper-evident logs),
//        §5.3 (Edit Log Management).
//
// DESIGN DECISION (chaining formula, canon §8):
//   The log is tamper-evident via a blockchain-style CRC-32 chain.
//   make_entry() stores data_hash computed as:
//
//     chain_input = [prev_hash : 4 bytes LE]
//                 | [timestamp_ns : 8 bytes LE]
//                 | [type : 1 byte]
//                 | [target : raw UTF-8 bytes (no length prefix)]
//                 | [payload_hash : 4 bytes LE]
//     payload_hash  = crc32(payload, payload_len)
//     data_hash     = crc32(chain_input)
//
//   The payload_hash is stored in signature[0..3] (little-endian u32) when
//   no caller-supplied signature is present, so that verify_chain() can
//   reconstruct the exact same chain_input and detect any mutation to any
//   field (timestamp, type, target, payload, or chain order).
//   When the caller supplies a non-empty signature, the payload_hash is
//   prepended as the first 4 bytes of the signature storage.
//
// On-disk wire format for one entry (canon §4.4):
//   [timestamp_ns : u64 LE]
//   [type         : u8]
//   [target       : u32-length-prefixed UTF-8 string]
//   [data_hash    : u32 LE]
//   [signature    : u32-length-prefixed bytes]
//
// EditLog wire format (§5.3):
//   [count : u32 LE] then count serialised entries.
#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ---------------------------------------------------------------------------
// EditLogEntry — one immutable record in the append-only log
// ---------------------------------------------------------------------------
struct EditLogEntry {
    uint64_t             timestamp_ns = 0;
    MutationType         type         = MutationType::CodebookEdit;
    std::string          target;
    uint32_t             data_hash    = 0;  // chained CRC-32 (see DESIGN DECISION)
    std::vector<uint8_t> signature;         // [payload_hash:4 LE][optional sig bytes]

    // Serialise to a ByteWriter (canon §4.4 wire layout).
    void serialize(ByteWriter& w) const;

    // Deserialise one entry from a ByteReader; throws FormatError on bad data.
    static EditLogEntry parse(ByteReader& r);
};

// ---------------------------------------------------------------------------
// make_entry — convenience factory that computes the chained data_hash.
//
// Arguments:
//   type         — mutation category
//   target       — name of the mutated component
//   payload      — pointer to raw bytes of the mutation payload (may be null if len==0)
//   payload_len  — byte count of payload (may be 0)
//   prev_hash    — data_hash of the immediately preceding entry (0 for first entry)
//   timestamp_ns — nanoseconds since Unix epoch; 0 -> auto-fill from system clock
//   signature    — optional opaque signature blob appended after payload_hash
//
// The resulting entry has:
//   signature[0..3] = payload_hash (LE u32)
//   signature[4..]  = caller-supplied signature bytes (if any)
//   data_hash       = crc32([prev_hash:4][timestamp_ns:8][type:1][target bytes][payload_hash:4])
// ---------------------------------------------------------------------------
EditLogEntry make_entry(
    MutationType            type,
    const std::string&      target,
    const void*             payload,
    size_t                  payload_len,
    uint32_t                prev_hash    = 0,
    uint64_t                timestamp_ns = 0,
    std::vector<uint8_t>    signature    = {}
);

// ---------------------------------------------------------------------------
// EditLog — ordered, append-only collection of EditLogEntry objects
// ---------------------------------------------------------------------------
class EditLog {
public:
    EditLog() = default;

    // Append an already-constructed entry.  Use make_entry() to guarantee
    // correct chaining.
    void append(EditLogEntry entry);

    // Random-access read; throws std::out_of_range if idx >= size().
    const EditLogEntry& at(size_t idx) const;

    // Number of entries currently stored.
    size_t size() const noexcept;

    // data_hash of the last entry (0 if empty).
    uint32_t tail_hash() const noexcept;

    // Serialise the entire log ([u32 count][entries...]).
    void serialize(ByteWriter& w) const;

    // Deserialise from a ByteReader; throws FormatError on bad data.
    static EditLog parse(ByteReader& r);

    // Verify tamper-evidence: recompute every entry's expected chain hash
    // (using the payload_hash stored in signature[0..3]) and compare it
    // against the stored data_hash.  Returns false if any mismatch is found.
    bool verify_chain() const;

    // Remove the last `last_n` entries from the log.
    // Used by LqtModel::rollback(n) to keep the log consistent with undone mutations.
    // No-op if last_n == 0. Throws std::out_of_range if last_n > size().
    void truncate(size_t last_n);

private:
    std::vector<EditLogEntry> entries_;
};

} // namespace lqt
