// lqt/rw_cache.cpp — Tiered L1/L2 LRU cache + PerformanceTracker.
// Council: Baldur (Patch 4).
#include "lqt/rw_cache.h"

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <utility>

namespace lqt {

// ── LruCache ────────────────────────────────────────────────────────────────

LruCache::LruCache(size_t capacity) : capacity_(capacity) {}

bool LruCache::get(const std::string& key, std::vector<float>& out) const {
    auto it = index_.find(key);
    if (it == index_.end()) {
        return false;
    }
    // Promote to MRU front (O(1) splice on std::list).
    order_.splice(order_.begin(), order_, it->second);
    out = it->second->second;
    return true;
}

void LruCache::put(const std::string& key, std::vector<float> value) {
    auto it = index_.find(key);
    if (it != index_.end()) {
        // Update existing entry's value and promote to MRU.
        it->second->second = std::move(value);
        order_.splice(order_.begin(), order_, it->second);
        return;
    }
    // Insert as MRU front, then evict if over capacity.
    order_.emplace_front(key, std::move(value));
    index_[key] = order_.begin();
    if (index_.size() > capacity_) {
        evict_lru();
    }
}

bool LruCache::contains(const std::string& key) const {
    return index_.find(key) != index_.end();
}

size_t LruCache::size() const {
    return index_.size();
}

size_t LruCache::capacity() const {
    return capacity_;
}

void LruCache::clear() {
    order_.clear();
    index_.clear();
}

bool LruCache::back_key_value(std::string& k, std::vector<float>& v) const {
    if (order_.empty()) {
        return false;
    }
    const auto& back = order_.back();
    k = back.first;
    v = back.second;
    return true;
}

void LruCache::evict_lru() {
    if (order_.empty()) {
        return;
    }
    const std::string& victim_key = order_.back().first;
    index_.erase(victim_key);
    order_.pop_back();
}

// ── TieredCacheManager ──────────────────────────────────────────────────────

TieredCacheManager::TieredCacheManager(size_t l1_size, size_t l2_size)
    : l1_(l1_size), l2_(l2_size) {}

bool TieredCacheManager::get(const std::string& key, std::vector<float>& out) {
    // Check L1 first.
    if (l1_.get(key, out)) {
        ++hits_;
        return true;
    }
    // Check L2; on hit, promote to L1.
    std::vector<float> tmp;
    if (l2_.get(key, tmp)) {
        ++hits_;
        out = tmp;
        // Promote a copy into L1 (demoting an L1 LRU entry into L2 if needed).
        promote_to_l1(key, std::move(tmp));
        return true;
    }
    ++misses_;
    return false;
}

void TieredCacheManager::put(const std::string& key, std::vector<float> value) {
    // Insert into L1. If L1 is already at capacity and the key is new,
    // demote the current LRU L1 entry to L2 first to avoid losing it.
    if (!l1_.contains(key) && l1_.size() >= l1_.capacity()) {
        std::string victim_k;
        std::vector<float> victim_v;
        if (l1_.back_key_value(victim_k, victim_v)) {
            l2_.put(victim_k, std::move(victim_v));
        }
    }
    l1_.put(key, std::move(value));
}

void TieredCacheManager::promote_to_l1(const std::string& key,
                                       std::vector<float> value) {
    // Same demotion logic as put(), kept separate for clarity at call sites.
    if (!l1_.contains(key) && l1_.size() >= l1_.capacity()) {
        std::string victim_k;
        std::vector<float> victim_v;
        if (l1_.back_key_value(victim_k, victim_v)) {
            l2_.put(victim_k, std::move(victim_v));
        }
    }
    l1_.put(key, std::move(value));
}

size_t TieredCacheManager::l1_size() const {
    return l1_.size();
}

size_t TieredCacheManager::l2_size() const {
    return l2_.size();
}

uint64_t TieredCacheManager::hits() const {
    return hits_;
}

uint64_t TieredCacheManager::misses() const {
    return misses_;
}

float TieredCacheManager::hit_rate() const {
    const uint64_t total = hits_ + misses_;
    if (total == 0) {
        return 0.0f;
    }
    return static_cast<float>(hits_) / static_cast<float>(total);
}

void TieredCacheManager::clear() {
    l1_.clear();
    l2_.clear();
    hits_ = 0;
    misses_ = 0;
}

// ── PerformanceTracker ──────────────────────────────────────────────────────

void PerformanceTracker::start_timer(const std::string& op) {
    active_[op] = Clock::now();
}

double PerformanceTracker::end_timer(const std::string& op) {
    auto it = active_.find(op);
    if (it == active_.end()) {
        return 0.0;
    }
    const TimePoint now = Clock::now();
    const auto us = std::chrono::duration_cast<std::chrono::microseconds>(
        now - it->second).count();
    const double ms = static_cast<double>(us) / 1000.0;
    active_.erase(it);
    record(op, ms);
    return ms;
}

void PerformanceTracker::record(const std::string& op, double ms) {
    OpStats& s = stats_[op];
    s.count += 1;
    s.total_ms += ms;
    if (ms < s.min_ms) {
        s.min_ms = ms;
    }
    if (ms > s.max_ms) {
        s.max_ms = ms;
    }
}

OpStats PerformanceTracker::stats(const std::string& op) const {
    auto it = stats_.find(op);
    if (it == stats_.end()) {
        OpStats empty;
        empty.min_ms = 0.0;  // present a friendly zero for never-recorded ops
        return empty;
    }
    return it->second;
}

std::string PerformanceTracker::summary() const {
    // Sort by operation name for deterministic output.
    std::vector<std::string> names;
    names.reserve(stats_.size());
    for (const auto& kv : stats_) {
        names.push_back(kv.first);
    }
    std::sort(names.begin(), names.end());

    std::ostringstream os;
    os << std::fixed << std::setprecision(3);
    for (const auto& name : names) {
        const OpStats& s = stats_.at(name);
        const double min_display = (s.count > 0) ? s.min_ms : 0.0;
        os << name
           << ": count=" << s.count
           << " mean=" << s.mean_ms() << "ms"
           << " min=" << min_display << "ms"
           << " max=" << s.max_ms << "ms"
           << "\n";
    }
    return os.str();
}

void PerformanceTracker::reset() {
    active_.clear();
    stats_.clear();
}

} // namespace lqt
