// tests/test_rta_ops.cpp — RTA analysis function tests (Patch 4).
// Covers: rta_entropy, rta_normalize (NormType::L1/L2), rta_apply_function,
//         rta_fractal_iterate, rta_density (DensityResult), rta_find_fixed_point.
// All API names match the actual rta_analysis.h surface from Thor (Patch 4).

#include <cmath>
#include <cstdint>
#include <vector>

#include "lqt/rta_analysis.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqttest;

// ─── Entropy ─────────────────────────────────────────────────────────────────

TEST_CASE(rta_entropy_uniform) {
    // Uniform values → max entropy ≈ log(N) = log(8)
    std::vector<float> v(8, 0.25f);
    const float e = rta_entropy(v);
    const float expected = static_cast<float>(std::log(8.0));
    CHECK(std::isfinite(e));
    CHECK_NEAR(e, expected, 1e-4);
}

TEST_CASE(rta_entropy_empty) {
    std::vector<float> v;
    CHECK_NEAR(rta_entropy(v), 0.0f, 1e-9);
}

TEST_CASE(rta_entropy_single) {
    // p = 1 → -1*log(1) = 0 (uses log(p+1e-10) so result ≈ 0 not exactly 0)
    std::vector<float> v = {5.0f};
    CHECK_NEAR(rta_entropy(v), 0.0f, 0.01f);
}

// ─── Normalization ─────────────────────────────────────────────────────────

TEST_CASE(rta_normalize_l2) {
    std::vector<float> v = {3.0f, 4.0f, 0.0f, 0.0f}; // ||v||_2 = 5
    std::vector<float> n = rta_normalize(v, NormType::L2);
    double sq = 0.0;
    for (float x : n) sq += double(x) * double(x);
    CHECK_NEAR(std::sqrt(sq), 1.0, 1e-5);
}

TEST_CASE(rta_normalize_zero_input) {
    std::vector<float> v = {0.0f, 0.0f, 0.0f};
    std::vector<float> n = rta_normalize(v, NormType::L2);
    CHECK_EQ(n.size(), v.size());
    for (size_t i = 0; i < n.size(); ++i) CHECK_NEAR(n[i], 0.0f, 1e-9);
}

TEST_CASE(rta_normalize_l1) {
    std::vector<float> v = {1.0f, 2.0f, 3.0f, 4.0f};
    std::vector<float> n = rta_normalize(v, NormType::L1);
    double s = 0.0;
    for (float x : n) s += std::fabs(double(x));
    CHECK_NEAR(s, 1.0, 1e-5);
}

// ─── apply_function ──────────────────────────────────────────────────────────

TEST_CASE(rta_apply_function_square) {
    std::vector<float> v = {1.0f, 2.0f, 3.0f};
    auto sq = [](float x) { return x * x; };
    std::vector<float> r = rta_apply_function(v, sq);
    CHECK_EQ(r.size(), static_cast<size_t>(3));
    CHECK_NEAR(r[0], 1.0f, 1e-6);
    CHECK_NEAR(r[1], 4.0f, 1e-6);
    CHECK_NEAR(r[2], 9.0f, 1e-6);
}

TEST_CASE(rta_apply_function_threshold) {
    // Identity function + threshold 2.0 → zeroes values with |r| <= 2
    std::vector<float> v = {1.0f, 2.0f, 3.0f, 4.0f};
    auto identity = [](float x) { return x; };
    std::vector<float> r = rta_apply_function(v, identity, 2.0f);
    CHECK_EQ(r.size(), static_cast<size_t>(4));
    CHECK_NEAR(r[0], 0.0f, 1e-6); // |1| <= 2 → zeroed
    CHECK_NEAR(r[1], 0.0f, 1e-6); // |2| <= 2 → zeroed
    CHECK(r[2] > 0.0f);           // |3| > 2 → kept
    CHECK(r[3] > 0.0f);           // |4| > 2 → kept
}

// ─── Fractal iteration ────────────────────────────────────────────────────────

TEST_CASE(rta_fractal_iterate_escape) {
    // z0 = 10, c = 0: first step z = 100 + 0 = 100 → |z| >> 2.0 → escaped
    std::vector<float> z0 = {10.0f};
    auto c_zero = [](size_t, float) { return 0.0f; };
    std::vector<float> result = rta_fractal_iterate(z0, c_zero, 50, 2.0f);
    CHECK_EQ(result.size(), static_cast<size_t>(1));
    // After iteration the absolute value should be large (escaped)
    CHECK(std::fabs(result[0]) > 2.0f);
}

TEST_CASE(rta_fractal_iterate_bound_zero) {
    // z0 = 0, c = 0: z_n = 0 for all n → |z| = 0 ≤ 2 → never escapes
    std::vector<float> z0 = {0.0f};
    auto c_zero = [](size_t, float) { return 0.0f; };
    std::vector<float> result = rta_fractal_iterate(z0, c_zero, 50, 2.0f);
    CHECK_EQ(result.size(), static_cast<size_t>(1));
    CHECK_NEAR(result[0], 0.0f, 1e-6);
}

// ─── Density estimation ───────────────────────────────────────────────────────

TEST_CASE(rta_density_basic) {
    std::vector<float> v = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f};
    DensityResult res = rta_density(v, 5, 0.0f); // threshold=0 to include all
    CHECK_EQ(res.counts.size(), static_cast<size_t>(5));
    CHECK_EQ(res.bin_edges.size(), static_cast<size_t>(6)); // resolution+1
    bool any_nonzero = false;
    for (float c : res.counts) if (c > 0.0f) { any_nonzero = true; break; }
    CHECK(any_nonzero);
}

// ─── Fixed-point iteration ────────────────────────────────────────────────────

TEST_CASE(rta_fixed_point_constant) {
    // f(v) = v → converges immediately
    std::vector<float> v0 = {1.0f, 2.0f, 3.0f};
    auto identity = [](const std::vector<float>& x) { return x; };
    FixedPointResult fp = rta_find_fixed_point(v0, identity, 1e-6f, 100);
    CHECK_EQ(fp.value.size(), v0.size());
    CHECK(fp.converged);
    for (size_t i = 0; i < v0.size(); ++i) CHECK_NEAR(fp.value[i], v0[i], 1e-5);
}

TEST_CASE(rta_fixed_point_contractive) {
    // f(v) = 0.5*v → converges to zero
    std::vector<float> v0 = {4.0f, -4.0f, 8.0f};
    auto half = [](const std::vector<float>& x) {
        std::vector<float> out(x.size());
        for (size_t i = 0; i < x.size(); ++i) out[i] = x[i] * 0.5f;
        return out;
    };
    FixedPointResult fp = rta_find_fixed_point(v0, half, 1e-6f, 200);
    CHECK_EQ(fp.value.size(), v0.size());
    for (size_t i = 0; i < fp.value.size(); ++i) CHECK_NEAR(fp.value[i], 0.0f, 1e-3);
}

int main() { return lqttest::run_all(); }
