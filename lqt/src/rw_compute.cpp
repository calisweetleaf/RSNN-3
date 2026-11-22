// lqt/src/rw_compute.cpp — RecursiveWeight full effective-value computation.
//
// Ports the Python reference RecursiveWeight.compute_effective_value() and
// its sub-components (base / phase / reference / error) to C++17.
//
// Canon: lqt.md §5; Briefing §3.1, §3.2.
// Reference: recursive_weights_core.py lines 1030-1370,
//            recursive-weights-comprehensive-reference.md §1, §3.2.
//
// Mathematical form (Theorem 1.2.1):
//   W_effective(i, t) = B(t) + α·W_effective(i-1, t)
//                     + Σ_j R_j·W_ref(j, t) + Φ(t) + ε(t)
// where for a scalar prev_value the Σ_j R_j·prev_value reduces to
//   Σ_i mean(R_slice_i) · prev_value.

#include "lqt/rw_compute.h"

#include <cassert>
#include <cmath>
#include <numeric>

namespace lqt {

// ────────────────────────────────────────────────────────────────────────────
// B component
// ────────────────────────────────────────────────────────────────────────────

float rw_base_value(const RecursiveWeight& w,
                    const std::vector<float>& codebook_values,
                    float scale) {
    if (static_cast<size_t>(w.base_index) >= codebook_values.size()) {
        throw FormatError("rw_base_value: base_index out of codebook range");
    }
    return codebook_values[w.base_index] * scale;
}

// ────────────────────────────────────────────────────────────────────────────
// Φ component — harmonic series identical to RecursiveWeight::phase_at()
// ────────────────────────────────────────────────────────────────────────────

float rw_phase_contribution(const RecursiveWeight& w, double t) {
    if (w.phase.empty()) {
        return 0.0f;
    }
    constexpr double kTwoPi = 2.0 * M_PI;
    double acc = 0.0;
    for (size_t i = 0; i < w.phase.size(); ++i) {
        acc += static_cast<double>(w.phase[i]) *
               std::sin(static_cast<double>(i + 1) * kTwoPi * t);
    }
    return static_cast<float>(acc);
}

// ────────────────────────────────────────────────────────────────────────────
// R component — self-reference (α·W_prev) + Σ_i mean(R_slice_i)·W_prev
// ────────────────────────────────────────────────────────────────────────────
//
// The reference tensor is stored row-major as a flat k·r_d·r_d array.
// For a scalar prev_value the matrix-times-vector reduction collapses to
// the per-slice mean times prev_value, summed over k slices.

float rw_reference_contribution(const RecursiveWeight& w,
                                const RwComputeContext& /*ctx*/,
                                float prev_value) {
    // Self-reference term α·W_prev is part of the reference mechanism per
    // briefing §3.1. It applies whether or not R is present.
    double acc = static_cast<double>(w.self_reference_coeff) *
                 static_cast<double>(prev_value);

    if (w.reference.empty() || w.r_k == 0 || w.r_d == 0) {
        return static_cast<float>(acc);
    }

    // Sanity: with a validated weight reference.size() == r_k * r_d * r_d.
    const size_t slice_len = static_cast<size_t>(w.r_d) * static_cast<size_t>(w.r_d);
    assert(w.reference.size() == static_cast<size_t>(w.r_k) * slice_len);

    if (slice_len == 0) {
        return static_cast<float>(acc);
    }

    const double prev_d = static_cast<double>(prev_value);
    for (uint32_t i = 0; i < w.r_k; ++i) {
        const size_t base = static_cast<size_t>(i) * slice_len;
        double slice_sum = 0.0;
        for (size_t off = 0; off < slice_len; ++off) {
            slice_sum += static_cast<double>(w.reference[base + off]);
        }
        const double slice_mean = slice_sum / static_cast<double>(slice_len);
        acc += slice_mean * prev_d;
    }
    return static_cast<float>(acc);
}

// ────────────────────────────────────────────────────────────────────────────
// ε component — mean of the error preservation vector
// ────────────────────────────────────────────────────────────────────────────

float rw_error_contribution(const RecursiveWeight& w) {
    if (w.error.empty()) {
        return 0.0f;
    }
    double sum = 0.0;
    for (float e : w.error) {
        sum += static_cast<double>(e);
    }
    return static_cast<float>(sum / static_cast<double>(w.error.size()));
}

// ────────────────────────────────────────────────────────────────────────────
// Full effective value (recursive descent)
// ────────────────────────────────────────────────────────────────────────────

float rw_compute_effective_value(const RecursiveWeight& w,
                                 const std::vector<float>& codebook_values,
                                 float scale,
                                 RwComputeContext ctx) {
    // Hard depth ceiling: clamp to base value (matches Python behavior
    // returning get_base_value() once max_recursion_depth is reached).
    if (ctx.current_depth >= ctx.max_depth) {
        return rw_base_value(w, codebook_values, scale);
    }

    const float base = rw_base_value(w, codebook_values, scale);
    const float phase_c = rw_phase_contribution(w, ctx.timestamp);
    const float err_c   = rw_error_contribution(w);

    // Base case (depth 0): no recursive reference term.
    if (ctx.current_depth == 0) {
        return base + phase_c + err_c;
    }

    // Recursive case: descend by one level, then fold in R-contribution.
    RwComputeContext ctx_prev = ctx;
    ctx_prev.current_depth = ctx.current_depth - 1;
    const float prev_val = rw_compute_effective_value(w, codebook_values, scale, ctx_prev);

    const float ref_c = rw_reference_contribution(w, ctx, prev_val);

    return base + ref_c + phase_c + err_c;
}

// ────────────────────────────────────────────────────────────────────────────
// Iterative convergence helper
// ────────────────────────────────────────────────────────────────────────────
//
// Iterates depths 0, 1, 2, ... up to max_iter. Each iteration is an
// independent rw_compute_effective_value call at that depth. Stops when the
// successive-depth delta falls below tol.

RwConvergenceResult rw_converge(const RecursiveWeight& w,
                                const std::vector<float>& codebook_values,
                                float scale,
                                float tol,
                                uint32_t max_iter) {
    RwConvergenceResult result{};
    result.value       = 0.0f;
    result.iterations  = 0;
    result.converged   = false;
    result.final_delta = 0.0f;

    if (max_iter == 0) {
        return result;
    }

    // Depth 0 — base case anchor.
    RwComputeContext ctx{};
    ctx.timestamp     = 0.0;
    ctx.max_depth     = max_iter;
    ctx.current_depth = 0;

    float prev = rw_compute_effective_value(w, codebook_values, scale, ctx);
    result.value      = prev;
    result.iterations = 1;

    for (uint32_t step = 1; step < max_iter; ++step) {
        ctx.current_depth = step;
        const float cur = rw_compute_effective_value(w, codebook_values, scale, ctx);
        const float delta = std::fabs(cur - prev);

        result.value       = cur;
        result.iterations  = step + 1;
        result.final_delta = delta;

        if (delta < tol) {
            result.converged = true;
            return result;
        }
        prev = cur;
    }

    return result;
}

} // namespace lqt
