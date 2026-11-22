// lqt/rw_dynamics.cpp — Dynamical systems analysis implementation.
// Ports DynamicalSystemsAnalyzer from recursive_weights_core.py (theorems 1.2.1–1.7.3).
// Council: Freya (Patch 4).
//
// Implementation notes:
//   - No external linear-algebra dependency. Eigenvalue magnitudes are
//     approximated via power iteration (dominant eigenvalue only).
//   - All matrices are stored as std::vector<float> in row-major layout
//     with size d*d.
//   - Functions raise lqt::ValidationError for inputs that violate the
//     mathematical preconditions of the underlying theorem.
#include "lqt/rw_dynamics.h"

#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstddef>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>

namespace lqt {
namespace dynamics {

// ── Helpers ──────────────────────────────────────────────────────────────────

float frobenius_norm(const std::vector<float>& matrix) {
    double sum_sq = 0.0;
    for (float v : matrix) {
        sum_sq += static_cast<double>(v) * static_cast<double>(v);
    }
    return static_cast<float>(std::sqrt(sum_sq));
}

float trace_mtm(const std::vector<float>& matrix, uint32_t d) {
    // tr(M^T M) = Σ_{i,j} M[i][j]^2  (independent of d when matrix is flat,
    // but we accept d for API symmetry and to validate the size).
    assert(matrix.size() == static_cast<std::size_t>(d) * static_cast<std::size_t>(d));
    (void)d;
    double sum_sq = 0.0;
    for (float v : matrix) {
        sum_sq += static_cast<double>(v) * static_cast<double>(v);
    }
    return static_cast<float>(sum_sq);
}

// Multiply d×d matrix (row-major) by length-d vector. out has length d.
static void matvec(const std::vector<float>& M, uint32_t d,
                   const std::vector<float>& x, std::vector<float>& out) {
    out.assign(d, 0.0f);
    for (uint32_t i = 0; i < d; ++i) {
        double acc = 0.0;
        const float* row = M.data() + static_cast<std::size_t>(i) * d;
        for (uint32_t j = 0; j < d; ++j) {
            acc += static_cast<double>(row[j]) * static_cast<double>(x[j]);
        }
        out[i] = static_cast<float>(acc);
    }
}

static float vec_norm(const std::vector<float>& v) {
    double s = 0.0;
    for (float x : v) s += static_cast<double>(x) * static_cast<double>(x);
    return static_cast<float>(std::sqrt(s));
}

static float vec_dot(const std::vector<float>& a, const std::vector<float>& b) {
    double s = 0.0;
    const std::size_t n = std::min(a.size(), b.size());
    for (std::size_t i = 0; i < n; ++i) {
        s += static_cast<double>(a[i]) * static_cast<double>(b[i]);
    }
    return static_cast<float>(s);
}

// Power iteration: approximates the dominant eigenvalue of a square matrix.
// Initialises with a deterministic non-zero vector (1/sqrt(d) on every entry)
// so behaviour is reproducible without an RNG dependency.
float power_iteration(const std::vector<float>& matrix, uint32_t d,
                      uint32_t max_iter, float tol) {
    if (d == 0) return 0.0f;
    if (matrix.size() != static_cast<std::size_t>(d) * static_cast<std::size_t>(d)) {
        throw ValidationError("power_iteration: matrix size != d*d");
    }

    std::vector<float> v(d, 1.0f / std::sqrt(static_cast<float>(d)));
    std::vector<float> w(d, 0.0f);

    float prev_eigen = 0.0f;
    float eigen = 0.0f;
    for (uint32_t it = 0; it < max_iter; ++it) {
        matvec(matrix, d, v, w);
        float n = vec_norm(w);
        if (n <= 1e-30f) {
            return 0.0f;  // Matrix maps v to zero; dominant eigenvalue ≈ 0.
        }
        for (uint32_t i = 0; i < d; ++i) {
            v[i] = w[i] / n;
        }
        // Rayleigh quotient: v^T M v / v^T v, and v is unit-norm so denom = 1.
        matvec(matrix, d, v, w);
        eigen = vec_dot(v, w);
        if (std::fabs(eigen - prev_eigen) < tol) {
            break;
        }
        prev_eigen = eigen;
    }
    return eigen;
}

// ── Theorem 1.2.1: Fixed-Point Convergence ─────────────────────────────────
std::vector<float> fixed_point_convergence(float alpha,
                                           const std::vector<float>& base_components) {
    if (std::fabs(alpha) >= 1.0f) {
        throw ValidationError("Alpha " + std::to_string(alpha) +
                              " >= 1.0, convergence not guaranteed");
    }
    const float denom = 1.0f - alpha;
    std::vector<float> out(base_components.size(), 0.0f);
    for (std::size_t i = 0; i < base_components.size(); ++i) {
        out[i] = base_components[i] / denom;
    }
    return out;
}

// ── Theorem 1.2.2: Lyapunov Stability ──────────────────────────────────────
bool lyapunov_stable(const std::vector<std::vector<float>>& reference_matrices, uint32_t d) {
    const std::size_t k = reference_matrices.size();
    if (k == 0) return true;  // Vacuously stable: no references => no recursion.
    const float bound = 1.0f / static_cast<float>(k);
    for (const auto& R : reference_matrices) {
        if (R.size() != static_cast<std::size_t>(d) * static_cast<std::size_t>(d)) {
            throw ValidationError("lyapunov_stable: matrix size != d*d");
        }
        if (frobenius_norm(R) >= bound) {
            return false;
        }
    }
    return true;
}

// ── Theorem 1.2.3: Attractor Dimension ─────────────────────────────────────
float attractor_dimension(const std::vector<std::vector<float>>& reference_matrices, uint32_t d) {
    if (reference_matrices.empty()) {
        return static_cast<float>(d);
    }

    double sum_log_norms = 0.0;
    for (const auto& R : reference_matrices) {
        if (R.size() != static_cast<std::size_t>(d) * static_cast<std::size_t>(d)) {
            throw ValidationError("attractor_dimension: matrix size != d*d");
        }
        const double n = static_cast<double>(frobenius_norm(R));
        sum_log_norms += std::log(n + 1e-8);
    }

    float max_eigenvalue = 0.0f;
    for (const auto& R : reference_matrices) {
        const float ev = power_iteration(R, d);
        if (ev > max_eigenvalue) {
            max_eigenvalue = ev;
        }
    }

    if (max_eigenvalue <= 0.0f) {
        return static_cast<float>(d);
    }

    const double log_max = std::log(static_cast<double>(max_eigenvalue));
    const double ratio = sum_log_norms / log_max;
    const double bounded = std::min(static_cast<double>(d), ratio);
    return static_cast<float>(std::max(0.0, bounded));
}

// ── Theorem 1.3.1: Capacity Amplification ──────────────────────────────────
double capacity_amplification(uint32_t b_base,
                              const std::vector<uint32_t>& reference_precisions,
                              const std::vector<float>& multiplicity_factors) {
    const double base_capacity = std::pow(2.0, static_cast<double>(b_base));
    double reference_capacity = 1.0;
    const std::size_t n = std::min(reference_precisions.size(), multiplicity_factors.size());
    for (std::size_t i = 0; i < n; ++i) {
        const double base_i = std::pow(2.0, static_cast<double>(reference_precisions[i]));
        reference_capacity *= std::pow(base_i, static_cast<double>(multiplicity_factors[i]));
    }
    return base_capacity * reference_capacity;
}

// ── Theorem 1.3.2: Universal Approximation ─────────────────────────────────
bool universal_approximation(uint32_t dimension, uint32_t num_refs, uint32_t recursion_depth) {
    // Use 64-bit arithmetic to avoid overflow for moderate sizes.
    const uint64_t d = static_cast<uint64_t>(dimension);
    const uint64_t k = static_cast<uint64_t>(num_refs);
    const uint64_t depth = static_cast<uint64_t>(recursion_depth);

    const uint64_t min_parameters = d * (d + 1ULL);                 // d*(d+1)
    const uint64_t available_parameters = d + (k * d * d * depth);  // d + k·d²·depth
    return available_parameters >= min_parameters;
}

// ── Theorem 1.3.3: Kolmogorov Complexity Reduction ─────────────────────────
double kolmogorov_complexity_reduction(uint32_t K_full) {
    if (K_full <= 1) return 1.0;
    return static_cast<double>(K_full) * std::log(static_cast<double>(K_full));
}

// ── Theorem 1.4.1: Uniform Convergence Bound ───────────────────────────────
double uniform_convergence_bound(float gamma, float C, uint32_t iterations) {
    if (gamma >= 1.0f) {
        throw ValidationError("Gamma " + std::to_string(gamma) + " >= 1.0, bound invalid");
    }
    const double g = static_cast<double>(gamma);
    const double c = static_cast<double>(C);
    return (c * std::pow(g, static_cast<double>(iterations))) / (1.0 - g);
}

// ── Theorem 1.4.2: Convergence Rate ────────────────────────────────────────
uint32_t convergence_rate(float epsilon, float gamma, float C) {
    if (gamma >= 1.0f || epsilon <= 0.0f) {
        throw ValidationError("Invalid parameters for convergence rate computation");
    }
    const double e = static_cast<double>(epsilon);
    const double g = static_cast<double>(gamma);
    const double c = static_cast<double>(C);
    const double numerator = std::log(e * (1.0 - g) / c);
    const double denominator = std::log(g);
    // gamma < 1 so log(gamma) is negative; numerator may be negative as well.
    const double ratio = numerator / denominator;
    const double ceiled = std::ceil(ratio);
    if (!std::isfinite(ceiled) || ceiled < 1.0) {
        return 1U;
    }
    return static_cast<uint32_t>(ceiled);
}

// ── Theorem 1.4.3: Computational Complexity ────────────────────────────────
double computational_complexity(uint32_t n, uint32_t d, float epsilon) {
    double eps = static_cast<double>(epsilon);
    if (eps <= 0.0) {
        eps = 1e-6;
    }
    const double dd = static_cast<double>(d);
    const double nn = static_cast<double>(n);
    return nn * (dd * dd) + (dd * dd * dd) * std::log(1.0 / eps);
}

// ── Theorem 1.5.1: Error Accumulation Bound ────────────────────────────────
double error_accumulation_bound(float initial_error,
                                const std::vector<float>& step_errors,
                                float decay_factor) {
    const std::size_t n = step_errors.size();
    double accumulated = static_cast<double>(initial_error);
    const double base = 1.0 - static_cast<double>(decay_factor);
    for (std::size_t i = 0; i < n; ++i) {
        // exponent matches Python: (n - i - 1)
        const double exponent = static_cast<double>(n - i - 1);
        accumulated += static_cast<double>(step_errors[i]) * std::pow(base, exponent);
    }
    return accumulated;
}

// ── Theorem 1.5.2: Spectral Radius ─────────────────────────────────────────
float spectral_radius(const std::vector<float>& matrix, uint32_t d,
                      uint32_t max_iter, float tol) {
    // The Python implementation takes max over |eigenvalues|. Without a
    // full eigendecomposition we use |dominant eigenvalue| from power iteration.
    return std::fabs(power_iteration(matrix, d, max_iter, tol));
}

// ── Theorem 1.5.3: Error Correction Capacity ───────────────────────────────
double error_correction_capacity(float gamma, float epsilon_max) {
    if (gamma >= 1.0f) {
        throw ValidationError("Gamma must be < 1 for stability");
    }
    const double g = static_cast<double>(gamma);
    return ((1.0 - g) * static_cast<double>(epsilon_max)) / (1.0 + g);
}

// ── Theorem 1.6.1: Weight Space Dimension ──────────────────────────────────
double weight_space_dimension(uint32_t base_dim,
                              const std::vector<uint32_t>& ref_dims,
                              const std::vector<float>& scaling_factors) {
    double effective = static_cast<double>(base_dim);
    const std::size_t n = std::min(ref_dims.size(), scaling_factors.size());
    for (std::size_t i = 0; i < n; ++i) {
        const double lam = static_cast<double>(scaling_factors[i]);
        const double one_plus_lam = 1.0 + lam;
        effective += static_cast<double>(ref_dims[i]) / (one_plus_lam * one_plus_lam);
    }
    return effective;
}

// ── Theorem 1.6.2: Self-Similarity Metric ──────────────────────────────────
float self_similarity_metric(const std::vector<std::vector<float>>& reference_matrices, uint32_t d) {
    const std::size_t k = reference_matrices.size();
    if (k == 0) return 0.0f;

    double similarity_sum = 0.0;
    for (const auto& R : reference_matrices) {
        if (R.size() != static_cast<std::size_t>(d) * static_cast<std::size_t>(d)) {
            throw ValidationError("self_similarity_metric: matrix size != d*d");
        }
        const double trace_term = static_cast<double>(trace_mtm(R, d));
        const double fnorm = static_cast<double>(frobenius_norm(R));
        const double fnorm_sq = fnorm * fnorm;
        if (fnorm_sq > 1e-8) {
            similarity_sum += trace_term / fnorm_sq;
        }
    }
    return static_cast<float>(similarity_sum / static_cast<double>(k));
}

// ── Theorem 1.6.3: Multiscale Efficiency ───────────────────────────────────
double multiscale_efficiency(uint32_t N_full, uint32_t N_base,
                             const std::vector<std::pair<uint32_t,float>>& scale_params,
                             float fractal_dimension) {
    double denominator = static_cast<double>(N_base);
    const double D = static_cast<double>(fractal_dimension);
    for (const auto& sp : scale_params) {
        const uint32_t N_i = sp.first;
        const float s_i = sp.second;
        if (s_i > 0.0f) {
            denominator += static_cast<double>(N_i) *
                           std::pow(static_cast<double>(s_i), -D);
        }
    }
    if (denominator == 0.0) {
        return std::numeric_limits<double>::infinity();
    }
    return static_cast<double>(N_full) / denominator;
}

// ── Theorem 1.7.1: Minimum Description Length ──────────────────────────────
double minimum_description_length(const std::vector<float>& entropies, double mutual_information) {
    double total = 0.0;
    for (float h : entropies) total += static_cast<double>(h);
    return total + mutual_information;
}

// ── Theorem 1.7.2: Information Capacity ────────────────────────────────────
double information_capacity(uint32_t base_bits,
                            const std::vector<uint32_t>& reference_bits,
                            const std::vector<float>& preservation_factors) {
    double capacity = static_cast<double>(base_bits);
    const std::size_t n = std::min(reference_bits.size(), preservation_factors.size());
    for (std::size_t i = 0; i < n; ++i) {
        const double alpha_i = static_cast<double>(preservation_factors[i]);
        // Python: alpha_i ** (i + 1)
        capacity += static_cast<double>(reference_bits[i]) *
                    std::pow(alpha_i, static_cast<double>(i + 1));
    }
    return capacity;
}

// ── Theorem 1.7.3: Compression Efficiency ──────────────────────────────────
double compression_efficiency(uint32_t N, uint32_t b_quant,
                              uint32_t N_patterns, uint32_t b_pattern,
                              uint32_t N_refs, uint32_t b_ref,
                              uint32_t N_base, uint32_t b_base) {
    const double numerator = static_cast<double>(N) * static_cast<double>(b_quant);
    const double denominator =
        static_cast<double>(N_patterns) * static_cast<double>(b_pattern) +
        static_cast<double>(N_refs)     * static_cast<double>(b_ref)     +
        static_cast<double>(N_base)     * static_cast<double>(b_base);
    if (denominator == 0.0) {
        return std::numeric_limits<double>::infinity();
    }
    return numerator / denominator;
}

} // namespace dynamics
} // namespace lqt
