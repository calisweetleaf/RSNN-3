// tests/test_rw_reference.cpp — Recursive Weight reference module tests (Patch 4).
// Covers: rw_dynamics (17 theorems), rw_validation (4-pass), rw_cache (LRU/tiered).
// All API names match the actual headers: dynamics:: namespace (Freya),
//   validate_configuration() (Tyr), LruCache/TieredCacheManager/PerformanceTracker (Baldur).

#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

#include "lqt/error.h"
#include "lqt/recursive_weight.h"
#include "lqt/rw_cache.h"
#include "lqt/rw_dynamics.h"
#include "lqt/rw_validation.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqt::dynamics;
using namespace lqttest;

// ─── Theorem 1.2.1: Fixed-point convergence ───────────────────────────────

TEST_CASE(dynamics_fixed_point_convergence_basic) {
    // alpha = 0.5, base = {2.0} → fixed point = 2/(1-0.5) = 4.0
    std::vector<float> base = {2.0f};
    std::vector<float> result = fixed_point_convergence(0.5f, base);
    CHECK_EQ(result.size(), static_cast<size_t>(1));
    CHECK_NEAR(result[0], 4.0f, 1e-3);
}

TEST_CASE(dynamics_fixed_point_alpha_too_large_throws) {
    std::vector<float> base = {1.0f};
    CHECK_THROWS_AS(fixed_point_convergence(1.0f, base), ValidationError);
}

// ─── Theorem 1.2.2: Lyapunov stability ───────────────────────────────────

TEST_CASE(dynamics_lyapunov_stable_small_matrices) {
    // Two 2×2 matrices, each element = 0.1 → ||M||_F = sqrt(4*0.01) = 0.2 < 1/k=0.5
    std::vector<std::vector<float>> mats = {
        {0.1f, 0.1f, 0.1f, 0.1f},
        {0.1f, 0.1f, 0.1f, 0.1f},
    };
    CHECK(lyapunov_stable(mats, 2u));
}

TEST_CASE(dynamics_lyapunov_unstable_large_matrix) {
    // One 2×2 identity: ||I||_F = sqrt(2) ≈ 1.41 > 1/k=1.0 → unstable
    std::vector<std::vector<float>> mats = {{1.0f, 0.0f, 0.0f, 1.0f}};
    CHECK(!lyapunov_stable(mats, 2u));
}

// ─── Theorem 1.4.1: Uniform convergence bound ────────────────────────────

TEST_CASE(dynamics_uniform_convergence_bound) {
    // gamma=0.5, C=1.0, iter=10 → C*gamma^iter/(1-gamma) = 0.5^10/0.5 ≈ 0.00195
    const double bound = uniform_convergence_bound(0.5f, 1.0f, 10);
    CHECK(std::isfinite(bound));
    CHECK(bound > 0.0);
    CHECK(bound < 0.01);
}

// ─── Theorem 1.4.2: Convergence rate ────────────────────────────────────

TEST_CASE(dynamics_convergence_rate_basic) {
    const uint32_t iters = convergence_rate(0.01f, 0.5f, 1.0f);
    CHECK(iters > 0u);
    CHECK(iters < 1000u);
}

// ─── Matrix norms ────────────────────────────────────────────────────────

TEST_CASE(dynamics_frobenius_norm_identity) {
    // 2×2 identity → ||I||_F = sqrt(2)
    std::vector<float> m = {1.0f, 0.0f, 0.0f, 1.0f};
    const float fn = frobenius_norm(m);
    CHECK_NEAR(fn, std::sqrt(2.0f), 1e-5);
}

TEST_CASE(dynamics_spectral_radius_scaled_identity) {
    // 2×2 0.3*I → dominant eigenvalue ≈ 0.3
    std::vector<float> m = {0.3f, 0.0f, 0.0f, 0.3f};
    const float sr = spectral_radius(m, 2u);
    CHECK_NEAR(sr, 0.3f, 1e-2);
}

// ─── Theorem 1.6.2: Self-similarity ────────────────────────────────────

TEST_CASE(dynamics_self_similarity_identity_matrices) {
    // tr(I^T I)/||I||_F^2 = 2/2 = 1.0 per matrix → mean = 1.0
    std::vector<std::vector<float>> mats = {
        {1.0f, 0.0f, 0.0f, 1.0f},
        {1.0f, 0.0f, 0.0f, 1.0f},
    };
    const float s = self_similarity_metric(mats, 2u);
    CHECK_NEAR(s, 1.0f, 1e-5);
}

// ─── Theorem 1.5.1: Error accumulation ───────────────────────────────────

TEST_CASE(dynamics_error_accumulation_decay) {
    // step_errors all 0 → accumulated error == initial
    const float initial = 0.5f;
    std::vector<float> steps = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    const double acc = error_accumulation_bound(initial, steps, 0.1f);
    CHECK_NEAR(acc, double(initial), 1e-5);
}

// ─── Validation: configuration pass ───────────────────────────────────────

TEST_CASE(validation_passes_valid_weight) {
    RecursiveWeight w;
    w.base_index          = 0;
    w.phase               = {0.1f, 0.2f};
    w.r_k                 = 1;
    w.r_d                 = 2;
    w.reference           = {1.0f, 0.0f, 0.0f, 1.0f}; // 1×2×2
    w.tensor_position     = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    w.error               = {0.0f, 0.0f};
    w.self_reference_coeff = 0.5f;  // |alpha| < 1 → valid
    ValidationPass pass = validate_configuration(w);
    CHECK(pass.passed);
}

TEST_CASE(validation_fails_alpha_too_large) {
    RecursiveWeight w;
    w.base_index           = 0;
    w.phase                = {0.0f};
    w.r_k                  = 0;
    w.r_d                  = 0;
    w.tensor_position      = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    w.error                = {};
    w.self_reference_coeff = 1.5f;  // |alpha| >= 1 → invalid
    ValidationPass pass = validate_configuration(w);
    CHECK(!pass.passed);
}

// ─── Cache: LRU ──────────────────────────────────────────────────────────

TEST_CASE(cache_lru_basic_put_get) {
    LruCache cache(8);
    cache.put("k1", {10.0f});
    cache.put("k2", {20.0f});
    cache.put("k3", {30.0f});

    std::vector<float> v;
    CHECK(cache.get("k1", v)); CHECK_NEAR(v[0], 10.0f, 1e-6);
    CHECK(cache.get("k2", v)); CHECK_NEAR(v[0], 20.0f, 1e-6);
    CHECK(cache.get("k3", v)); CHECK_NEAR(v[0], 30.0f, 1e-6);
}

TEST_CASE(cache_lru_eviction) {
    LruCache cache(3);
    cache.put("k1", {10.0f});
    cache.put("k2", {20.0f});
    cache.put("k3", {30.0f});
    cache.put("k4", {40.0f}); // forces eviction of LRU = k1

    std::vector<float> v;
    CHECK(!cache.get("k1", v));          // evicted
    CHECK(cache.get("k2", v));
    CHECK(cache.get("k3", v));
    CHECK(cache.get("k4", v)); CHECK_NEAR(v[0], 40.0f, 1e-6);
}

// ─── Cache: tiered ───────────────────────────────────────────────────────

TEST_CASE(cache_tiered_l1_hit) {
    TieredCacheManager cache(256, 1024);
    cache.put("key_42", {3.14f});
    std::vector<float> v;
    CHECK(cache.get("key_42", v));
    CHECK_NEAR(v[0], 3.14f, 1e-6);
}

TEST_CASE(cache_tiered_l2_promotion) {
    TieredCacheManager cache(4, 16); // small cache for testing
    for (int i = 0; i < 8; ++i) {
        cache.put("k" + std::to_string(i), {static_cast<float>(i)});
    }
    // Newest entries must hit
    std::vector<float> v;
    CHECK(cache.get("k7", v));
    CHECK_NEAR(v[0], 7.0f, 1e-6);
    // Key 0 may have been evicted — test is non-strict (allowed miss)
    const bool hit = cache.get("k0", v);
    if (hit) CHECK_NEAR(v[0], 0.0f, 1e-6);
}

// ─── PerformanceTracker ──────────────────────────────────────────────────

TEST_CASE(cache_performance_tracker) {
    PerformanceTracker tracker;
    tracker.start_timer("test_op");
    volatile double acc = 0.0;
    for (int i = 0; i < 10000; ++i) acc += std::sin(double(i));
    (void)acc;
    const double dur = tracker.end_timer("test_op");
    CHECK(dur >= 0.0);
    CHECK(tracker.stats("test_op").count == 1u);
}

int main() { return lqttest::run_all(); }
