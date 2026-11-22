// lqt/rw_cache.h — Tiered L1/L2 LRU cache + PerformanceTracker.
// Ports TieredCacheManager and PerformanceTracker from recursive_weights_core.py.
// Council: Baldur (Patch 4).
#pragma once
#include <chrono>
#include <cstdint>
#include <list>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>
#include "lqt/error.h"

namespace lqt {

// ── LRU cache (single tier) ─────────────────────────────────────────────────
// Generic LRU eviction: entries evicted when capacity exceeded.
class LruCache {
public:
    explicit LruCache(size_t capacity);
    bool        get(const std::string& key, std::vector<float>& out) const;
    void        put(const std::string& key, std::vector<float> value);
    bool        contains(const std::string& key) const;
    size_t      size() const;
    size_t      capacity() const;
    void        clear();

    // Peek at the least-recently-used entry without removing it. Returns
    // false if the cache is empty. Used by TieredCacheManager to demote
    // an L1 entry into L2 before inserting a new L1 value.
    bool        back_key_value(std::string& k, std::vector<float>& v) const;

private:
    size_t capacity_;
    mutable std::list<std::pair<std::string, std::vector<float>>> order_; // MRU front
    mutable std::unordered_map<std::string, decltype(order_)::iterator>  index_;
    void evict_lru();
};

// ── TieredCacheManager (L1 + L2) ───────────────────────────────────────────
// L1: small, fast (default 256 entries). L2: larger (default 1024 entries).
// get(): check L1 first, then L2 (promote to L1 on L2 hit).
// put(): insert into L1; if L1 evicts an entry, demote it to L2.
class TieredCacheManager {
public:
    explicit TieredCacheManager(size_t l1_size = 256, size_t l2_size = 1024);

    // Retrieve value. Returns false if not found in either tier.
    bool get(const std::string& key, std::vector<float>& out);

    // Insert value. Inserts into L1; promotes evicted L1 entries to L2.
    void put(const std::string& key, std::vector<float> value);

    // Cache statistics.
    size_t l1_size() const;
    size_t l2_size() const;
    uint64_t hits()   const;
    uint64_t misses() const;
    float    hit_rate() const;  // hits / (hits + misses)

    void clear();

private:
    LruCache  l1_;
    LruCache  l2_;
    uint64_t  hits_   = 0;
    uint64_t  misses_ = 0;
    // We need to know when L1 evicts — we'll use a custom approach:
    // Before putting into L1, if L1 is at capacity, manually demote the LRU L1 entry to L2.
    void promote_to_l1(const std::string& key, std::vector<float> value);
};

// ── PerformanceTracker ──────────────────────────────────────────────────────
// Tracks operation timing and memory usage.
// Ports PerformanceTracker from recursive_weights_core.py.
struct OpStats {
    uint64_t count      = 0;
    double   total_ms   = 0.0;
    double   min_ms     = 1e18;
    double   max_ms     = 0.0;
    double   mean_ms()  const { return count > 0 ? total_ms / count : 0.0; }
};

class PerformanceTracker {
public:
    PerformanceTracker() = default;

    // Start timing an operation.
    void start_timer(const std::string& op);

    // End timing; returns elapsed milliseconds.
    double end_timer(const std::string& op);

    // Record an external duration (for benchmarking wrappers).
    void record(const std::string& op, double ms);

    // Returns stats for a named operation. Returns default-zero if op unknown.
    OpStats stats(const std::string& op) const;

    // Human-readable summary string.
    std::string summary() const;

    // Reset all counters.
    void reset();

private:
    using Clock = std::chrono::steady_clock;
    using TimePoint = Clock::time_point;
    std::unordered_map<std::string, TimePoint> active_;
    std::unordered_map<std::string, OpStats>   stats_;
};

} // namespace lqt
