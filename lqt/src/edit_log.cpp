// src/edit_log.cpp — Append-only edit log implementation.
//
// Council module: A7 (mutation safety layer).
// Canon: lqt.md §4.4, §5.3, §8.
#include "lqt/edit_log.h"

#include <chrono>
#include <stdexcept>

#include "lqt/crc.h"

namespace lqt {

// ---------------------------------------------------------------------------
// Helper: extract stored payload_hash from signature bytes[0..3].
// Returns 0 if signature has fewer than 4 bytes.
static uint32_t extract_payload_hash(const std::vector<uint8_t>& sig) {
    if (sig.size() < 4) return 0;
    return (static_cast<uint32_t>(sig[0])      ) |
           (static_cast<uint32_t>(sig[1]) <<  8) |
           (static_cast<uint32_t>(sig[2]) << 16) |
           (static_cast<uint32_t>(sig[3]) << 24);
}

// ---------------------------------------------------------------------------
// EditLogEntry — serialisation
// ---------------------------------------------------------------------------

void EditLogEntry::serialize(ByteWriter& w) const {
    w.put_u64(timestamp_ns);
    w.put_u8(static_cast<uint8_t>(type));
    w.put_string(target);
    w.put_u32(data_hash);
    w.put_u32(static_cast<uint32_t>(signature.size()));
    if (!signature.empty()) {
        w.put_bytes(signature.data(), signature.size());
    }
}

EditLogEntry EditLogEntry::parse(ByteReader& r) {
    EditLogEntry e;
    e.timestamp_ns = r.get_u64();
    uint8_t raw_type = r.get_u8();
    if (raw_type > static_cast<uint8_t>(MutationType::TensorDetach)) {
        throw FormatError("EditLogEntry: unknown mutation type byte");
    }
    e.type = static_cast<MutationType>(raw_type);
    e.target    = r.get_string();
    e.data_hash = r.get_u32();
    uint32_t sig_len = r.get_u32();
    e.signature.resize(sig_len);
    if (sig_len > 0) {
        r.get_bytes(e.signature.data(), sig_len);
    }
    return e;
}

// ---------------------------------------------------------------------------
// make_entry
// ---------------------------------------------------------------------------
EditLogEntry make_entry(
    MutationType            type,
    const std::string&      target,
    const void*             payload,
    size_t                  payload_len,
    uint32_t                prev_hash,
    uint64_t                timestamp_ns,
    std::vector<uint8_t>    signature)
{
    // Auto-timestamp.
    if (timestamp_ns == 0) {
        timestamp_ns = static_cast<uint64_t>(
            std::chrono::duration_cast<std::chrono::nanoseconds>(
                std::chrono::system_clock::now().time_since_epoch()
            ).count()
        );
    }

    // Step 1: compute payload_hash.
    uint32_t payload_hash = 0;
    if (payload != nullptr && payload_len > 0) {
        payload_hash = crc32(payload, payload_len);
    }

    // Step 2: build the chain input buffer and compute data_hash.
    //   chain_input = [prev_hash:4 LE][timestamp_ns:8 LE][type:1]
    //                 [target raw UTF-8 bytes][payload_hash:4 LE]
    ByteWriter chain_buf;
    chain_buf.put_u32(prev_hash);
    chain_buf.put_u64(timestamp_ns);
    chain_buf.put_u8(static_cast<uint8_t>(type));
    if (!target.empty()) {
        chain_buf.put_bytes(target.data(), target.size());
    }
    chain_buf.put_u32(payload_hash);

    const auto& cb = chain_buf.bytes();
    uint32_t data_hash = crc32(cb.data(), cb.size());

    // Step 3: build the signature storage: [payload_hash:4 LE][caller sig bytes].
    //   We always prepend payload_hash so that verify_chain() can retrieve it.
    std::vector<uint8_t> sig_storage;
    sig_storage.reserve(4 + signature.size());
    sig_storage.push_back(static_cast<uint8_t>(payload_hash & 0xFF));
    sig_storage.push_back(static_cast<uint8_t>((payload_hash >>  8) & 0xFF));
    sig_storage.push_back(static_cast<uint8_t>((payload_hash >> 16) & 0xFF));
    sig_storage.push_back(static_cast<uint8_t>((payload_hash >> 24) & 0xFF));
    sig_storage.insert(sig_storage.end(), signature.begin(), signature.end());

    EditLogEntry e;
    e.timestamp_ns = timestamp_ns;
    e.type         = type;
    e.target       = target;
    e.data_hash    = data_hash;
    e.signature    = std::move(sig_storage);
    return e;
}

// ---------------------------------------------------------------------------
// EditLog
// ---------------------------------------------------------------------------

void EditLog::append(EditLogEntry entry) {
    entries_.push_back(std::move(entry));
}

const EditLogEntry& EditLog::at(size_t idx) const {
    return entries_.at(idx);
}

size_t EditLog::size() const noexcept {
    return entries_.size();
}

uint32_t EditLog::tail_hash() const noexcept {
    if (entries_.empty()) return 0;
    return entries_.back().data_hash;
}

void EditLog::serialize(ByteWriter& w) const {
    w.put_u32(static_cast<uint32_t>(entries_.size()));
    for (const auto& e : entries_) {
        e.serialize(w);
    }
}

EditLog EditLog::parse(ByteReader& r) {
    EditLog log;
    uint32_t count = r.get_u32();
    log.entries_.reserve(count);
    for (uint32_t i = 0; i < count; ++i) {
        log.entries_.push_back(EditLogEntry::parse(r));
    }
    return log;
}

bool EditLog::verify_chain() const {
    uint32_t running_prev = 0;
    for (const auto& e : entries_) {
        // Recover payload_hash from signature[0..3].
        uint32_t payload_hash = extract_payload_hash(e.signature);

        // Rebuild the same chain_input that make_entry() would have used.
        ByteWriter chain_buf;
        chain_buf.put_u32(running_prev);
        chain_buf.put_u64(e.timestamp_ns);
        chain_buf.put_u8(static_cast<uint8_t>(e.type));
        if (!e.target.empty()) {
            chain_buf.put_bytes(e.target.data(), e.target.size());
        }
        chain_buf.put_u32(payload_hash);

        const auto& cb = chain_buf.bytes();
        uint32_t expected = crc32(cb.data(), cb.size());

        if (expected != e.data_hash) {
            return false;
        }
        running_prev = e.data_hash;
    }
    return true;
}

void EditLog::truncate(size_t last_n) {
    if (last_n == 0) return;
    if (last_n > entries_.size()) {
        throw std::out_of_range("EditLog::truncate: last_n exceeds log size");
    }
    entries_.resize(entries_.size() - last_n);
}

} // namespace lqt
