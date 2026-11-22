// lqt/src/recursive_weight.cpp — Module A6: Recursive Weights implementation.
//
// Canon: lqt.md §5 "Five-Dimensional Semantic Logic and Recursive Operations"
// Briefing: §3 "Mathematical Formalism: Recursive Weights"
//
// Implements serialization, validation, and the two core mathematical operators
// (phase_at, reconstruct) for the quintuple W = {B, Φ, R, T, ε}.

#include "lqt/recursive_weight.h"

#include <cmath>
#include <limits>
#include <numeric>
#include <sstream>

namespace lqt {

// ============================================================================
// Serialization wire format (all fields little-endian via ByteWriter/Reader)
// ============================================================================
//
// Layout:
//   [u32]  base_index                    — B
//   [u32]  phase_count                   — length of Φ vector
//   [phase_count x f32]                  — Φ entries
//   [u32]  r_k                           — R first dim
//   [u32]  r_d                           — R spatial dim
//   [r_k*r_d*r_d x f32]                  — R entries (may be 0 if r_k==0)
//   [5 x f32]                            — T (tensor_position, always 5 floats)
//   [u32]  error_count                   — length of ε vector
//   [error_count x f32]                  — ε entries
//   [f32]  self_reference_coeff          — α (convergence requires |α| < 1)

void RecursiveWeight::serialize(ByteWriter& w) const {
    // B
    w.put_u32(base_index);

    // Φ
    w.put_u32(static_cast<uint32_t>(phase.size()));
    for (float v : phase) {
        w.put_f32(v);
    }

    // R dims and data
    w.put_u32(r_k);
    w.put_u32(r_d);
    for (float v : reference) {
        w.put_f32(v);
    }

    // T — always exactly 5 floats
    for (float v : tensor_position) {
        w.put_f32(v);
    }

    // ε
    w.put_u32(static_cast<uint32_t>(error.size()));
    for (float v : error) {
        w.put_f32(v);
    }

    // α — self-reference coefficient (Patch 5: wired into wire format)
    w.put_f32(self_reference_coeff);
}

RecursiveWeight RecursiveWeight::parse(ByteReader& r) {
    RecursiveWeight w;

    // B
    w.base_index = r.get_u32();

    // Φ
    const uint32_t phase_count = r.get_u32();
    w.phase.resize(phase_count);
    for (uint32_t i = 0; i < phase_count; ++i) {
        w.phase[i] = r.get_f32();
    }

    // R
    w.r_k = r.get_u32();
    w.r_d = r.get_u32();
    const uint64_t r_size = static_cast<uint64_t>(w.r_k) *
                            static_cast<uint64_t>(w.r_d) *
                            static_cast<uint64_t>(w.r_d);
    if (r_size > 0) {
        // Guard against implausibly large sizes before allocating.
        if (r_size > 1024u * 1024u * 64u) { // 64M floats max
            throw FormatError("RecursiveWeight::parse: R tensor too large");
        }
        w.reference.resize(static_cast<size_t>(r_size));
        for (size_t i = 0; i < static_cast<size_t>(r_size); ++i) {
            w.reference[i] = r.get_f32();
        }
    }

    // T — always exactly 5 floats
    for (size_t i = 0; i < LQT_RTA_RANK; ++i) {
        w.tensor_position[i] = r.get_f32();
    }

    // ε
    const uint32_t error_count = r.get_u32();
    w.error.resize(error_count);
    for (uint32_t i = 0; i < error_count; ++i) {
        w.error[i] = r.get_f32();
    }

    // α — self-reference coefficient (Patch 5: wired into wire format)
    w.self_reference_coeff = r.get_f32();

    return w;
}

// ============================================================================
// validate()
// ============================================================================

void RecursiveWeight::validate() const {
    // T must be exactly LQT_RTA_RANK == 5 floats.
    // std::array<float,5> always has size() == 5; we still check finiteness.
    // (The size check is implicit but we make it explicit for documentation.)
    static_assert(std::tuple_size<decltype(tensor_position)>::value == LQT_RTA_RANK,
                  "tensor_position must have exactly LQT_RTA_RANK elements");

    // reference.size() must equal r_k * r_d * r_d.
    const uint64_t expected_r = static_cast<uint64_t>(r_k) *
                                static_cast<uint64_t>(r_d) *
                                static_cast<uint64_t>(r_d);
    if (reference.size() != static_cast<size_t>(expected_r)) {
        std::ostringstream oss;
        oss << "RecursiveWeight::validate: reference.size() = " << reference.size()
            << " != r_k*r_d*r_d = " << expected_r
            << " (r_k=" << r_k << ", r_d=" << r_d << ")";
        throw ValidationError(oss.str());
    }

    // All phase floats must be finite.
    for (size_t i = 0; i < phase.size(); ++i) {
        if (!std::isfinite(phase[i])) {
            throw ValidationError("RecursiveWeight::validate: non-finite value in phase vector");
        }
    }

    // All reference floats must be finite.
    for (size_t i = 0; i < reference.size(); ++i) {
        if (!std::isfinite(reference[i])) {
            throw ValidationError("RecursiveWeight::validate: non-finite value in reference matrix");
        }
    }

    // All tensor_position floats must be finite.
    for (size_t i = 0; i < tensor_position.size(); ++i) {
        if (!std::isfinite(tensor_position[i])) {
            throw ValidationError("RecursiveWeight::validate: non-finite value in tensor_position");
        }
    }

    // All error floats must be finite.
    for (size_t i = 0; i < error.size(); ++i) {
        if (!std::isfinite(error[i])) {
            throw ValidationError("RecursiveWeight::validate: non-finite value in error vector");
        }
    }

    // α must be finite and strictly inside (-1, 1) for convergence (Theorem 1.2.1).
    if (!std::isfinite(self_reference_coeff) || std::fabs(self_reference_coeff) >= 1.0f) {
        throw ValidationError(
            "RecursiveWeight::validate: |self_reference_coeff| >= 1.0 violates convergence bound");
    }
}

// ============================================================================
// phase_at(t)
// ============================================================================
//
// DESIGN DECISION: harmonic series formula (documented in header)
//   phase_at(t) = Σ_{i=0}^{N-1}  phase[i] * sin((i+1) * 2π * t)
//
// Uses double precision accumulation to keep the sum numerically clean even
// for large N, then casts to float at the end. The fixed angular frequency
// ω = 2π gives a fundamental period of 1 second; harmonic i has period
// 1/(i+1) seconds. The result is bounded by ||phase||_1 for all t.

float RecursiveWeight::phase_at(double t) const {
    if (phase.empty()) {
        return 0.0f;
    }

    constexpr double kTwoPi = 2.0 * M_PI;
    double acc = 0.0;
    for (size_t i = 0; i < phase.size(); ++i) {
        // Harmonic (i+1): angular frequency = (i+1) * 2π, period = 1/(i+1) s.
        acc += static_cast<double>(phase[i]) * std::sin(static_cast<double>(i + 1) * kTwoPi * t);
    }
    return static_cast<float>(acc);
}

// ============================================================================
// reconstruct() — full effective-value computation (Theorem 1.2.1)
// ============================================================================
//
// DESIGN DECISION: recursive effective-value formula
//   W_eff(d, t) = base_val + α·W_eff(d-1, t)
//               + Σ_k mean(R_k) · W_eff(d-1, t)
//               + Φ(t) + mean(ε)
//
// Base case (d == 0):
//   W_eff(0, t) = base_val + Φ(t) + mean(ε)
//
// where base_val = cb.scalar(base_index) * scale and mean(R_k) is the mean of
// the k-th r_d × r_d slice of the reference tensor. The α and R contributions
// vanish at d == 0 so the recursion terminates with a finite, well-defined
// scalar. A practical depth limit (DEPTH = 8) is used here; convergence_value()
// iterates further with an explicit fixed-point criterion (max depth 32).
//
// Stability: convergence requires the effective multiplier
// (α + Σ_k mean(R_k)) to have magnitude < 1. The default α = 0.5 keeps the
// linear term well inside the stable regime when the R slices are small.

namespace {

// File-local recursion helper. Returns W_eff at the given depth.
float rw_eff_value(const RecursiveWeight& w, const Codebook& cb,
                   float scale, double t, uint32_t depth) {
    const float base_val = cb.scalar(w.base_index) * scale;
    const float phase_val = w.phase_at(t);

    float eps_mean = 0.0f;
    if (!w.error.empty()) {
        double sum = 0.0;
        for (float e : w.error) {
            sum += static_cast<double>(e);
        }
        eps_mean = static_cast<float>(sum / static_cast<double>(w.error.size()));
    }

    if (depth == 0) {
        return base_val + phase_val + eps_mean;
    }

    const float prev = rw_eff_value(w, cb, scale, t, depth - 1);

    // R contribution: mean of each r_k slice multiplied by prev.
    float r_contrib = 0.0f;
    if (w.r_k > 0 && w.r_d > 0 && !w.reference.empty()) {
        const uint32_t slice_size = w.r_d * w.r_d;
        for (uint32_t k = 0; k < w.r_k; ++k) {
            double slice_sum = 0.0;
            const size_t base = static_cast<size_t>(k) * slice_size;
            for (uint32_t i = 0; i < slice_size; ++i) {
                slice_sum += static_cast<double>(w.reference[base + i]);
            }
            const float slice_mean = static_cast<float>(
                slice_sum / static_cast<double>(slice_size));
            r_contrib += slice_mean * prev;
        }
    }

    const float alpha = w.self_reference_coeff;
    return base_val + alpha * prev + r_contrib + phase_val + eps_mean;
}

} // namespace

float RecursiveWeight::reconstruct(const Codebook& cb, float scale, double t) const {
    if (base_index >= cb.num_vectors()) {
        throw FormatError("RecursiveWeight::reconstruct: base_index out of codebook range");
    }
    constexpr uint32_t DEPTH = 8;  // practical depth limit for a single call
    return rw_eff_value(*this, cb, scale, t, DEPTH);
}

// ============================================================================
// convergence_value() — fixed-point iteration of the effective-value formula
// ============================================================================
//
// Iterates rw_eff_value with increasing depth until consecutive values agree
// to within 1e-6 (absolute), or the maximum depth of 32 is reached. Returns
// the last computed value (which equals the converged fixed point when the
// recurrence is contractive, i.e. |α + Σ_k mean(R_k)| < 1).

float RecursiveWeight::convergence_value(const Codebook& cb, float scale, double t) const {
    if (base_index >= cb.num_vectors()) {
        throw FormatError("RecursiveWeight::convergence_value: base_index out of codebook range");
    }
    constexpr uint32_t MAX_DEPTH = 32;
    constexpr float EPSILON = 1e-6f;

    float prev = 0.0f;
    float curr = 0.0f;
    for (uint32_t d = 0; d < MAX_DEPTH; ++d) {
        curr = rw_eff_value(*this, cb, scale, t, d);
        if (d > 0 && std::fabs(curr - prev) < EPSILON) {
            break;
        }
        prev = curr;
    }
    return curr;
}

// ============================================================================
// reference_energy()
// ============================================================================
//
// Frobenius norm of the R tensor: sqrt( Σ r[i]^2 ).
// Returns 0.0f for an empty reference matrix.

float RecursiveWeight::reference_energy() const {
    if (reference.empty()) {
        return 0.0f;
    }
    double sum_sq = 0.0;
    for (float v : reference) {
        sum_sq += static_cast<double>(v) * static_cast<double>(v);
    }
    return static_cast<float>(std::sqrt(sum_sq));
}

} // namespace lqt
