// lqt/rw_dynamics.h — Dynamical systems analysis for Recursive Weights.
// Ports DynamicalSystemsAnalyzer from recursive_weights_core.py.
// Theorems 1.2.1 through 1.7.3 of the specification.
// Council: Freya (Patch 4).
#pragma once
#include <cstdint>
#include <utility>
#include <vector>
#include "lqt/error.h"

namespace lqt {
namespace dynamics {

// ── Theorem 1.2.1: Fixed-Point Convergence ─────────────────────────────────
// Computes lim_{i→∞} W_eff = base / (1 - alpha)
// Throws ValidationError if |alpha| >= 1.0.
std::vector<float> fixed_point_convergence(float alpha,
                                           const std::vector<float>& base_components);

// ── Theorem 1.2.2: Lyapunov Stability ──────────────────────────────────────
// Returns true if ||R_i||_F < 1/k for all k reference matrices.
// Each matrix is d×d stored row-major (size d*d).
bool lyapunov_stable(const std::vector<std::vector<float>>& reference_matrices, uint32_t d);

// ── Theorem 1.2.3: Attractor Dimension ─────────────────────────────────────
// D_attr = min(d, Σlog(||R_i||) / log(max_eigenvalue))
// Uses power iteration to approximate max |eigenvalue|.
float attractor_dimension(const std::vector<std::vector<float>>& reference_matrices, uint32_t d);

// ── Theorem 1.3.1: Capacity Amplification ──────────────────────────────────
// C = 2^b_base * Π (2^b_i)^m_i
double capacity_amplification(uint32_t b_base,
                              const std::vector<uint32_t>& reference_precisions,
                              const std::vector<float>& multiplicity_factors);

// ── Theorem 1.3.2: Universal Approximation ─────────────────────────────────
bool universal_approximation(uint32_t dimension, uint32_t num_refs, uint32_t recursion_depth);

// ── Theorem 1.3.3: Kolmogorov Complexity Reduction ─────────────────────────
double kolmogorov_complexity_reduction(uint32_t K_full);

// ── Theorem 1.4.1: Uniform Convergence Bound ───────────────────────────────
// Bound = C * gamma^i / (1 - gamma). Throws if gamma >= 1.
double uniform_convergence_bound(float gamma, float C, uint32_t iterations);

// ── Theorem 1.4.2: Convergence Rate ────────────────────────────────────────
// i_min = ceil(log(eps*(1-gamma)/C) / log(gamma))
uint32_t convergence_rate(float epsilon, float gamma, float C);

// ── Theorem 1.4.3: Computational Complexity ────────────────────────────────
// T = O(n*d^2 + d^3*log(1/eps))
double computational_complexity(uint32_t n, uint32_t d, float epsilon);

// ── Theorem 1.5.1: Error Accumulation Bound ────────────────────────────────
// ||eps_n|| <= ||eps_0|| + Σ eta_i * (1-beta)^(n-i)
double error_accumulation_bound(float initial_error,
                                const std::vector<float>& step_errors,
                                float decay_factor);

// ── Theorem 1.5.2: Spectral Radius ─────────────────────────────────────────
// Approximates max |eigenvalue| via power iteration. Matrix is d×d row-major.
float spectral_radius(const std::vector<float>& matrix, uint32_t d,
                      uint32_t max_iter = 100, float tol = 1e-6f);

// ── Theorem 1.5.3: Error Correction Capacity ───────────────────────────────
double error_correction_capacity(float gamma, float epsilon_max);

// ── Theorem 1.6.1: Weight Space Dimension ──────────────────────────────────
double weight_space_dimension(uint32_t base_dim,
                              const std::vector<uint32_t>& ref_dims,
                              const std::vector<float>& scaling_factors);

// ── Theorem 1.6.2: Self-Similarity Metric ──────────────────────────────────
// S = (1/k) Σ tr(R_i^T R_i) / ||R_i||_F^2
float self_similarity_metric(const std::vector<std::vector<float>>& reference_matrices, uint32_t d);

// ── Theorem 1.6.3: Multiscale Efficiency ───────────────────────────────────
double multiscale_efficiency(uint32_t N_full, uint32_t N_base,
                             const std::vector<std::pair<uint32_t,float>>& scale_params,
                             float fractal_dimension);

// ── Theorem 1.7.1: Minimum Description Length ──────────────────────────────
double minimum_description_length(const std::vector<float>& entropies, double mutual_information);

// ── Theorem 1.7.2: Information Capacity ────────────────────────────────────
double information_capacity(uint32_t base_bits,
                            const std::vector<uint32_t>& reference_bits,
                            const std::vector<float>& preservation_factors);

// ── Theorem 1.7.3: Compression Efficiency ──────────────────────────────────
double compression_efficiency(uint32_t N, uint32_t b_quant,
                              uint32_t N_patterns, uint32_t b_pattern,
                              uint32_t N_refs, uint32_t b_ref,
                              uint32_t N_base, uint32_t b_base);

// ── Power iteration (internal helper, also exported for testing) ────────────
// Approximates dominant eigenvalue of d×d matrix (row-major float vector).
float power_iteration(const std::vector<float>& matrix, uint32_t d,
                      uint32_t max_iter = 100, float tol = 1e-6f);

// ── Frobenius norm helper ────────────────────────────────────────────────────
float frobenius_norm(const std::vector<float>& matrix);

// ── Trace of M^T * M (= ||M||_F^2) ─────────────────────────────────────────
float trace_mtm(const std::vector<float>& matrix, uint32_t d);

} // namespace dynamics
} // namespace lqt
