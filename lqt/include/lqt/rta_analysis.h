// lqt/rta_analysis.h — RTA analysis operations.
// Ported from recursive_tensor.py: fractal_iteration, compute_entropy,
//   normalize, apply_function, compute_density_function.
// Council: Thor (Patch 4).
#pragma once
#include <cstdint>
#include <functional>
#include <vector>
#include "lqt/error.h"

namespace lqt {

// ── Normalization type ──────────────────────────────────────────────────────
enum class NormType { L1, L2, Inf, Frobenius };

// ── Fractal iteration on a flat vector of values ───────────────────────────
// Port of RecursiveTensor.fractal_iteration(c_function, max_iter).
// Each value z is iterated: z = z² + c until |z| > escape_radius or max_iter reached.
// c_func: returns the 'c' constant for each element given (index, current_z).
// Iteration stops element-wise when |z| > escape_radius.
// Returns the final z values after iteration.
std::vector<float> rta_fractal_iterate(
    const std::vector<float>& data,
    std::function<float(size_t, float)> c_func,
    uint32_t max_iter = 10,
    float escape_radius = 2.0f);

// ── Shannon entropy ─────────────────────────────────────────────────────────
// Port of RecursiveTensor.compute_entropy().
// Treats absolute values as unnormalized probabilities, computes -Σ p_i * log(p_i + ε).
// Only positive values are included; returns 0.0 for empty or all-zero input.
float rta_entropy(const std::vector<float>& values);

// ── Normalization ────────────────────────────────────────────────────────────
// Port of RecursiveTensor.normalize(norm_type).
// Returns normalized copy; if norm == 0 returns unchanged copy.
std::vector<float> rta_normalize(const std::vector<float>& data, NormType norm = NormType::L2);

// ── Element-wise function application ────────────────────────────────────────
// Port of RecursiveTensor.apply_function(func, threshold).
// Applies func to each element. If threshold >= 0, zeroes elements below threshold.
std::vector<float> rta_apply_function(
    const std::vector<float>& data,
    std::function<float(float)> func,
    float threshold = -1.0f);    // negative = no threshold

// ── Density function (histogram) ─────────────────────────────────────────────
// Port of RecursiveTensor.compute_density_function(resolution, threshold).
// Returns (bin_edges, histogram_counts) as two vectors.
// bin_edges has resolution+1 elements; histogram has resolution elements.
struct DensityResult { std::vector<float> bin_edges; std::vector<float> counts; };
DensityResult rta_density(
    const std::vector<float>& values,
    uint32_t resolution = 50,
    float threshold = 0.01f);

// ── Recursive fixed-point check ────────────────────────────────────────────
// From whitepaper Theorem 2: for recursive tensor with contractive mapping f,
// iterate f(v) until ||f(v) - v||₂ < tol or max_iter reached.
// Returns {converged, final_value, iterations_taken}.
struct FixedPointResult { bool converged; std::vector<float> value; uint32_t iters; };
FixedPointResult rta_find_fixed_point(
    const std::vector<float>& initial,
    std::function<std::vector<float>(const std::vector<float>&)> f,
    float tol = 1e-6f,
    uint32_t max_iter = 256);

} // namespace lqt
