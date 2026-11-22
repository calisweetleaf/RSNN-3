// lqt/recursive_weight.h — Module A6: Recursive Weights (quintuple W = {B, Φ, R, T, ε}).
//
// Canon: lqt.md §5 "Five-Dimensional Semantic Logic and Recursive Operations"
// Briefing: §3 "Mathematical Formalism: Recursive Weights"
//
// Recursive weights encode quantized model parameters as a five-component
// mathematical structure that enables temporal modulation, recursive self-
// referential correction, and error accumulation prevention across recursion.
//
// The quintuple is:
//   B  — Base index into a quantized codebook (uint32).
//   Φ  — Phase transformation vector: time-dependent harmonic modulation.
//   R  — Recursive reference matrix: 3-D tensor of shape k×d×d (floats).
//   T  — Tensor context embedding: exactly 5 floats mapping to RTA dims d0..d4.
//   ε  — Error preservation vector: residual capturing reconstruction error to
//          prevent accumulation during recursive operations.
#pragma once

#include <array>
#include <cmath>
#include <cstdint>
#include <numeric>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ============================================================================
// RecursiveWeight — on-disk + in-memory representation of W = {B, Φ, R, T, ε}
// ============================================================================

/*
 * DESIGN DECISION: phase_at(t) — harmonic series formula
 * -------------------------------------------------------
 * Canon §5 describes Φ as a "time-dependent phase/temporal modulation vector"
 * but does not specify an exact formula. A standard harmonic series satisfies
 * all documented requirements (temporal variation, finite, bounded):
 *
 *   phase_at(t) = Σ_{i=0}^{N-1}  phase[i] * sin((i+1) * ω * t)
 *
 * where ω = 2π / T_period, with T_period = 1.0 second chosen as the canonical
 * unit period. This gives N harmonics (fundamental and overtones), each
 * amplitude-weighted by phase[i]. The result is bounded by ||phase||_1 for any
 * t (since |sin| ≤ 1), making it globally stable. The varying frequency
 * factors (i+1) ensure the output genuinely changes with t even when all
 * phase[i] have the same sign.
 */

/*
 * DESIGN DECISION: reconstruct() — reconstruction operator
 * ---------------------------------------------------------
 * Canon §3 / briefing §3 defines the semantic components but leaves the scalar
 * combination operator underspecified. From the briefing formula hint:
 *
 *   W_eff(t) = Codebook[B] × scale × (1 + phase_at(t))  +  mean(ε)
 *
 * Rationale:
 *   • Codebook[B] * scale  is the primary quantized scalar (canon B component).
 *   • (1 + phase_at(t))    applies temporal modulation multiplicatively so that
 *     the phase acts as a gain factor, giving smooth variation around the base
 *     value rather than a disconnected additive offset.  When phase_at(0) = 0
 *     the unmodulated base value is recovered exactly.
 *   • mean(ε)              adds the mean residual error, fulfilling "ε prevents
 *     error accumulation across recursion" by folding the mean residual back
 *     into the reconstructed scalar at each recursion step — canceling
 *     systematic drift without amplifying variance.
 *   • T (tensor_position)  is the 5-D positional embedding; it is structurally
 *     part of W for indexing/addressing within the RTA lattice and is not
 *     directly summed into a scalar, consistent with its role as a position tag.
 *   • R (reference matrix) contributes via reference_energy() for downstream
 *     consumers that need the full matrix interaction; it is not reduced to a
 *     scalar in reconstruct() to preserve its role as a structural operator.
 *
 * The operator ensures: changing base_index changes cb.scalar(base_index),
 * which directly changes the output. The result is finite whenever the codebook
 * entry and all vector components are finite.
 */

struct RecursiveWeight {
    // B — quantized codebook index
    uint32_t base_index = 0;

    // Φ — phase transformation vector (length N, typically 8 harmonics)
    std::vector<float> phase;

    // R — recursive reference matrix, 3-D tensor of shape k×d×d
    uint32_t r_k = 0;  // first dimension (number of slices)
    uint32_t r_d = 0;  // spatial dimension (each slice is r_d × r_d)
    std::vector<float> reference; // size == r_k * r_d * r_d, row-major

    // T — tensor context embedding: exactly LQT_RTA_RANK (5) floats
    std::array<float, LQT_RTA_RANK> tensor_position{};

    // ε — error preservation vector (same length as phase, or any length)
    std::vector<float> error;

    // α — self-reference coefficient (bounded |α| < 1 for convergence of the
    // recursive effective-value computation; see reconstruct() and
    // convergence_value()). Default 0.5 sits well inside the stability bound.
    float self_reference_coeff = 0.5f;

    // ------------------------------------------------------------------ I/O --

    void serialize(ByteWriter& w) const;
    static RecursiveWeight parse(ByteReader& r);

    // Validate invariants; throws ValidationError on violations.
    // Checked:
    //   • tensor_position has exactly LQT_RTA_RANK (5) elements (always true
    //     via std::array, but the spec mandates explicit checking).
    //   • reference.size() == r_k * r_d * r_d.
    //   • All floats in phase, reference, tensor_position, error are finite
    //     (no NaN / Inf that would poison downstream computation).
    void validate() const;

    // -------------------------------------------------------- Math operators --

    // Phase harmonic evaluation at time t (seconds).
    // Returns Σ_{i=0}^{N-1} phase[i] * sin((i+1) * ω * t)
    // where ω = 2π (period = 1 s). Bounded by ||phase||_1 for all t.
    float phase_at(double t) const;

    // Scalar reconstruction from the quintuple via the full effective-value
    // formula (Theorem 1.2.1):
    //   W_eff(depth, t) = base_val + α·W_eff(depth-1, t)
    //                   + Σ_k mean(R_k) · W_eff(depth-1, t)
    //                   + Φ(t) + mean(ε)
    // evaluated at a fixed practical recursion depth.
    // Requires cb to be a scalar codebook (vector_dim == 1).
    // Throws FormatError if base_index >= cb.num_vectors().
    float reconstruct(const Codebook& cb, float scale, double t = 0.0) const;

    // Iterates the recursive effective-value computation until the result
    // stabilizes (|Δ| < 1e-6) or the maximum depth (32) is reached. Returns
    // the stable fixed-point reconstruction value.
    float convergence_value(const Codebook& cb, float scale, double t = 0.0) const;

    // Frobenius energy of the R reference tensor (sum of squares of all
    // entries, square-rooted). Useful for inspecting/testing the R component.
    float reference_energy() const;
};

} // namespace lqt
