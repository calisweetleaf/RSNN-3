// lqt/rw_compute.h — RecursiveWeight full effective value computation.
// Ports RecursiveWeight.compute_effective_value() and sub-components.
// Council: Loki (Patch 4).
//
// Canon: lqt.md §5; Briefing §3.1 / §3.2 (Reconstruction Algorithms).
// Reference: recursive_weights_core.py RecursiveWeight.compute_effective_value()
//            and recursive-weights-comprehensive-reference.md §1.2 Theorem 1.2.1
//            (Fixed-Point Convergence).
//
// The recursive effective value satisfies:
//   W_effective(i, t) = B(t) + α·W_effective(i-1, t) + Σ R_j·W_ref(j, t)
//                     + Φ(t) + ε(t)
// For |α| < 1 the iteration converges to a fixed point
//   W_∞ = (B + R_contrib + Φ + ε) / (1 - α)
// per Theorem 1.2.1.
#pragma once

#include <array>
#include <cstdint>
#include <functional>
#include <vector>

#include "lqt/error.h"
#include "lqt/recursive_weight.h"

namespace lqt {

// Maximum safe recursion depth (prevents stack overflow on deep weights).
inline constexpr uint32_t RW_MAX_RECURSION_DEPTH = 32;

// ── Runtime context for one effective-value computation ────────────────────
// Passed down the recursion chain to share parameters and bound depth.
struct RwComputeContext {
    double   timestamp     = 0.0;                       // t — time parameter for Φ(t)
    uint32_t max_depth     = RW_MAX_RECURSION_DEPTH;    // hard ceiling on recursion
    uint32_t current_depth = 0;                         // current recursion level
};

// ── Component computations ──────────────────────────────────────────────────

// B component: retrieve base codebook value at base_index and apply scale.
// Returns codebook_values[w.base_index] * scale as a single float.
// Throws FormatError if base_index >= codebook_values.size().
float rw_base_value(const RecursiveWeight& w,
                    const std::vector<float>& codebook_values,
                    float scale);

// Φ component: phase harmonic sum at time t.
//   Φ(t) = Σ_{i=0}^{N-1} phase[i] * sin((i+1) * 2π * t)
// Identical formula to RecursiveWeight::phase_at(t); duplicated here so the
// rw_compute API forms a complete self-contained surface.
float rw_phase_contribution(const RecursiveWeight& w, double t);

// R component: contribution from the recursive reference matrix.
// For a scalar prev_value the reference tensor contributes the row-by-vector
// dot product per slice, which (since prev_value is a scalar) reduces to
//   Σ_i mean(R_slice_i) * prev_value
// summed across k slices. Self-reference (α·W_prev) is folded in here per
// briefing §3.1, since it is structurally part of the reference mechanism:
//   return α·prev_value + Σ_i mean(R_slice_i)·prev_value
// When w.reference is empty only the α·prev_value term remains.
float rw_reference_contribution(const RecursiveWeight& w,
                                const RwComputeContext& ctx,
                                float prev_value);

// ε component: mean of the error preservation vector.
// Returns mean(ε) if non-empty, else 0.0f.
float rw_error_contribution(const RecursiveWeight& w);

// ── Full effective value ────────────────────────────────────────────────────
// Computes W_effective(current_depth, t) by recursive descent:
//
//   if current_depth == 0:        base + Φ(t) + ε
//   else (within max_depth):      base + R_contrib(W_prev) + Φ(t) + ε
//   if current_depth >= max_depth: clamp to base value (depth limit reached)
//
// where W_prev = rw_compute_effective_value at current_depth - 1, and
// R_contrib includes both α·W_prev and Σ_i mean(R_slice_i)·W_prev per
// rw_reference_contribution above.
//
// codebook_values: flat array of num_vectors scalars (scalar codebook).
// scale:           affine scale applied to codebook lookup.
//
// Each level adds α·W_prev + R(W_prev), so for |α| + ||R||·... < 1 the
// iteration converges to base / (1 - α) per Theorem 1.2.1.
float rw_compute_effective_value(const RecursiveWeight& w,
                                 const std::vector<float>& codebook_values,
                                 float scale,
                                 RwComputeContext ctx = {});

// ── Convergence helpers ─────────────────────────────────────────────────────
// Iteratively computes effective values at depths 0..max_iter and stops when
// the change between consecutive depths falls below tol.
struct RwConvergenceResult {
    float    value;        // effective value at the final depth evaluated
    uint32_t iterations;   // number of depth steps actually evaluated
    bool     converged;    // true if |Δ| < tol before max_iter exhausted
    float    final_delta;  // |value_last - value_prev| at the stopping point
};

RwConvergenceResult rw_converge(const RecursiveWeight& w,
                                const std::vector<float>& codebook_values,
                                float scale,
                                float tol = 1e-6f,
                                uint32_t max_iter = RW_MAX_RECURSION_DEPTH);

} // namespace lqt
