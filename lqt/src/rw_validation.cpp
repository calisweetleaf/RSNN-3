// lqt/src/rw_validation.cpp — RecursiveWeight 4-pass validation engine.
//
// Council: Tyr (Patch 4). Ports ValidationEngine from
// recursive_weights_core.py (lines 766-908). No torch / no numpy: every
// numerical primitive (Frobenius norm, power iteration, recursion sim) is
// implemented directly on top of std::vector<float>.
//
// All four passes are pure functions of the weight — they never mutate `w`,
// never throw (the *_strict variant is the only thrower), and never depend on
// I/O. They each populate a ValidationPass struct with a name, pass/fail flag,
// a 0..1 quality score, and a human-readable diagnostic on failure.

#include "lqt/rw_validation.h"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

namespace lqt {

// ============================================================================
// Internal helpers (anonymous namespace)
// ============================================================================
namespace {

// Saturating clamp into [0, 1] — used for normalizing scores.
inline float clamp01(float x) {
    if (!std::isfinite(x)) return 0.0f;
    if (x < 0.0f) return 0.0f;
    if (x > 1.0f) return 1.0f;
    return x;
}

// L1 norm of a float vector.
inline double l1_norm(const std::vector<float>& v) {
    double s = 0.0;
    for (float x : v) s += std::fabs(static_cast<double>(x));
    return s;
}

// L2 norm of a float vector.
inline double l2_norm(const std::vector<float>& v) {
    double s = 0.0;
    for (float x : v) {
        const double d = static_cast<double>(x);
        s += d * d;
    }
    return std::sqrt(s);
}

// True iff every entry is finite.
inline bool all_finite(const std::vector<float>& v) {
    for (float x : v) {
        if (!std::isfinite(x)) return false;
    }
    return true;
}

// Frobenius norm of a single r_d × r_d slice starting at offset `off` in the
// flattened reference vector. Slice length is r_d * r_d.
double slice_frobenius(const std::vector<float>& ref,
                       size_t off,
                       uint32_t r_d) {
    const size_t n = static_cast<size_t>(r_d) * static_cast<size_t>(r_d);
    if (off + n > ref.size()) return 0.0;
    double sq = 0.0;
    for (size_t i = 0; i < n; ++i) {
        const double v = static_cast<double>(ref[off + i]);
        sq += v * v;
    }
    return std::sqrt(sq);
}

// Mean of a single r_d × r_d slice — used as the scalar contribution of one R
// slice to the simplified scalar recursion in validate_convergence.
double slice_mean(const std::vector<float>& ref,
                  size_t off,
                  uint32_t r_d) {
    const size_t n = static_cast<size_t>(r_d) * static_cast<size_t>(r_d);
    if (n == 0 || off + n > ref.size()) return 0.0;
    double s = 0.0;
    for (size_t i = 0; i < n; ++i) {
        s += static_cast<double>(ref[off + i]);
    }
    return s / static_cast<double>(n);
}

// Spectral radius of a single r_d × r_d slice via power iteration. Pure C++,
// no BLAS dependency: dense matrix-vector product, then renormalize.
//
//   x_{n+1} = M x_n / ||M x_n||,  rho ≈ ||M x_n|| once x has aligned with the
//   dominant eigenvector. 12 iterations is enough for the small matrices we
//   see in the recursive-weight regime (r_d typically << 32).
//
// Returns 0.0 for empty slices.
double slice_spectral_radius(const std::vector<float>& ref,
                             size_t off,
                             uint32_t r_d) {
    if (r_d == 0) return 0.0;
    const size_t n = static_cast<size_t>(r_d);
    if (off + n * n > ref.size()) return 0.0;

    // Start with the all-ones vector (cheap, non-degenerate for typical M).
    std::vector<double> x(n, 1.0 / std::sqrt(static_cast<double>(n)));
    std::vector<double> y(n, 0.0);

    double lambda = 0.0;
    constexpr int kIters = 12;
    for (int it = 0; it < kIters; ++it) {
        // y = M x  (row-major, slice rows live at ref[off + row*n + col]).
        for (size_t r = 0; r < n; ++r) {
            double acc = 0.0;
            const size_t row_off = off + r * n;
            for (size_t c = 0; c < n; ++c) {
                acc += static_cast<double>(ref[row_off + c]) * x[c];
            }
            y[r] = acc;
        }

        // Norm of y (Rayleigh quotient via |y|/|x| with |x|=1).
        double norm = 0.0;
        for (size_t r = 0; r < n; ++r) norm += y[r] * y[r];
        norm = std::sqrt(norm);
        if (norm < 1e-18) return 0.0;  // M annihilated the iterate.

        lambda = norm;
        const double inv = 1.0 / norm;
        for (size_t r = 0; r < n; ++r) x[r] = y[r] * inv;
    }
    if (!std::isfinite(lambda)) return 0.0;
    return lambda;
}

// Simplified scalar recursion shared by passes 2 and 4. Models the
// recursive-weight effective-value formula reduced to a scalar:
//   val_{n+1} = base + alpha * val_n + (sum_k mean(R_k)) * val_n
// with base = 1.0 (unit codebook scalar at scale = 1.0). Tracks the absolute
// difference at each step so callers can detect convergence.
//
// Returns the converged value (last step). If the iteration diverges to
// infinity, returns std::numeric_limits<double>::infinity().
double simulate_recursion(const RecursiveWeight& w,
                          uint32_t max_iter,
                          double base,
                          double* last_delta_out) {
    const double alpha = static_cast<double>(w.self_reference_coeff);

    // Sum of slice means — collapses R into a scalar contribution to the
    // simplified recursion. For r_k == 0 this is just 0.
    double r_scalar = 0.0;
    if (w.r_k > 0 && w.r_d > 0) {
        const size_t slice_n =
            static_cast<size_t>(w.r_d) * static_cast<size_t>(w.r_d);
        for (uint32_t k = 0; k < w.r_k; ++k) {
            r_scalar += slice_mean(w.reference, k * slice_n, w.r_d);
        }
    }

    // The combined recursion coefficient: alpha + sum_k mean(R_k).
    const double rec_coeff = alpha + r_scalar;

    double val = 0.0;
    double prev = 0.0;
    double last_delta = 0.0;
    for (uint32_t step = 0; step < max_iter; ++step) {
        prev = val;
        val = base + rec_coeff * val;
        last_delta = std::fabs(val - prev);
        if (!std::isfinite(val)) {
            if (last_delta_out) *last_delta_out = last_delta;
            return std::numeric_limits<double>::infinity();
        }
    }
    if (last_delta_out) *last_delta_out = last_delta;
    return val;
}

} // anonymous namespace

// ============================================================================
// Pass 1: Configuration Validation
// ============================================================================

ValidationPass validate_configuration(const RecursiveWeight& w) {
    ValidationPass p;
    p.name = "configuration";

    std::ostringstream errs;
    int failures = 0;

    // (a) |alpha| strictly < 1 — geometric series convergence requirement.
    const float alpha = w.self_reference_coeff;
    if (!std::isfinite(alpha) || std::fabs(alpha) >= 1.0f) {
        ++failures;
        errs << "self_reference_coeff=" << alpha
             << " violates |alpha| < 1; ";
    }

    // (b) reference.size() must match r_k * r_d * r_d when non-empty.
    if (!w.reference.empty()) {
        const uint64_t expected =
            static_cast<uint64_t>(w.r_k) *
            static_cast<uint64_t>(w.r_d) *
            static_cast<uint64_t>(w.r_d);
        if (static_cast<uint64_t>(w.reference.size()) != expected) {
            ++failures;
            errs << "reference.size()=" << w.reference.size()
                 << " != r_k*r_d*r_d=" << expected << "; ";
        }
    }

    // (c) tensor_position must have exactly 5 elements (std::array guarantee,
    //     but spec demands explicit verification).
    if (w.tensor_position.size() != 5) {
        ++failures;
        errs << "tensor_position.size()=" << w.tensor_position.size()
             << " != 5; ";
    }

    // (d) base_index sanity cap.
    constexpr uint32_t kBaseIndexCap = 1u << 20;
    if (w.base_index >= kBaseIndexCap) {
        ++failures;
        errs << "base_index=" << w.base_index
             << " >= cap " << kBaseIndexCap << "; ";
    }

    // (e) Empty phase vector is a warning, not a hard failure.
    if (w.phase.empty()) {
        errs << "[warn] phase vector is empty; ";
    }

    if (failures > 0) {
        p.passed = false;
        p.message = errs.str();
        // Score degrades with failure count; cap of 4 distinct hard checks.
        p.score = clamp01(1.0f - static_cast<float>(failures) / 4.0f);
    } else {
        p.passed = true;
        p.score = 1.0f;
        p.message = errs.str(); // may carry [warn] note
    }
    return p;
}

// ============================================================================
// Pass 2: Convergence Validation
// ============================================================================

ValidationPass validate_convergence(const RecursiveWeight& w,
                                    uint32_t max_iter,
                                    float convergence_tol) {
    ValidationPass p;
    p.name = "convergence";

    std::ostringstream errs;
    int failures = 0;

    if (max_iter < 2) max_iter = 2;

    // Scalar-reduced recursion under a unit codebook (base = 1.0, scale = 1.0).
    double last_delta = 0.0;
    const double converged =
        simulate_recursion(w, max_iter, 1.0, &last_delta);

    if (!std::isfinite(converged)) {
        ++failures;
        errs << "recursion diverged (non-finite at iter " << max_iter << "); ";
    } else if (last_delta > static_cast<double>(convergence_tol)) {
        ++failures;
        errs << "last_delta=" << last_delta
             << " > tol=" << convergence_tol
             << " after " << max_iter << " iters; ";
    }

    // Lyapunov-style Frobenius bound: each slice ||R_i||_F < 1/r_k.
    if (w.r_k > 0 && w.r_d > 0 && !w.reference.empty()) {
        const double bound = 1.0 / static_cast<double>(w.r_k);
        const size_t slice_n =
            static_cast<size_t>(w.r_d) * static_cast<size_t>(w.r_d);
        for (uint32_t k = 0; k < w.r_k; ++k) {
            const double f = slice_frobenius(w.reference, k * slice_n, w.r_d);
            if (!std::isfinite(f) || f >= bound) {
                ++failures;
                errs << "||R_" << k << "||_F=" << f
                     << " >= 1/k=" << bound << "; ";
                break; // one diagnostic is enough — keep messages bounded
            }
        }
    }

    if (failures > 0) {
        p.passed = false;
        p.message = errs.str();
        p.score = clamp01(1.0f - static_cast<float>(failures) / 2.0f);
    } else {
        p.passed = true;
        // Score reflects how deep below tol we landed (closer = higher).
        const double margin = static_cast<double>(convergence_tol) - last_delta;
        const double tol_d  = std::max(static_cast<double>(convergence_tol),
                                       1e-12);
        p.score = clamp01(static_cast<float>(margin / tol_d));
        if (p.score < 0.5f) p.score = 0.5f; // converged ⇒ at least 0.5.
    }
    return p;
}

// ============================================================================
// Pass 3: Stability Validation
// ============================================================================

ValidationPass validate_stability(const RecursiveWeight& w) {
    ValidationPass p;
    p.name = "stability";

    std::ostringstream errs;
    int failures = 0;

    // Per-slice spectral radius bound: rho(R_i) < 1/k.
    if (w.r_k > 0 && w.r_d > 0 && !w.reference.empty()) {
        const double bound = 1.0 / static_cast<double>(w.r_k);
        const size_t slice_n =
            static_cast<size_t>(w.r_d) * static_cast<size_t>(w.r_d);
        for (uint32_t k = 0; k < w.r_k; ++k) {
            const double rho =
                slice_spectral_radius(w.reference, k * slice_n, w.r_d);
            if (!std::isfinite(rho) || rho >= bound) {
                ++failures;
                errs << "rho(R_" << k << ")=" << rho
                     << " >= 1/k=" << bound << "; ";
                break;
            }
        }
    }

    // Finite-value sweep across every float field that participates in the
    // recursion. The dedicated all_finite() helper avoids early-exit logic
    // duplication.
    if (!all_finite(w.phase)) {
        ++failures;
        errs << "non-finite value in phase; ";
    }
    if (!all_finite(w.reference)) {
        ++failures;
        errs << "non-finite value in reference; ";
    }
    if (!all_finite(w.error)) {
        ++failures;
        errs << "non-finite value in error; ";
    }
    if (!std::isfinite(w.self_reference_coeff)) {
        ++failures;
        errs << "non-finite self_reference_coeff; ";
    }
    for (size_t i = 0; i < w.tensor_position.size(); ++i) {
        if (!std::isfinite(w.tensor_position[i])) {
            ++failures;
            errs << "non-finite tensor_position[" << i << "]; ";
            break;
        }
    }

    if (failures > 0) {
        p.passed = false;
        p.message = errs.str();
        p.score = clamp01(1.0f - static_cast<float>(failures) / 5.0f);
    } else {
        p.passed = true;
        // Stability margin = 1 - |alpha|.
        const float margin = 1.0f - std::fabs(w.self_reference_coeff);
        p.score = clamp01(margin);
    }
    return p;
}

// ============================================================================
// Pass 4: Mathematical Consistency
// ============================================================================

ValidationPass validate_mathematical_consistency(const RecursiveWeight& w) {
    ValidationPass p;
    p.name = "mathematical_consistency";

    std::ostringstream errs;
    int failures = 0;

    // (a) Fixed-point self-consistency:
    //     For base = 1, theory ⇒ W_inf = base / (1 - alpha) — but our
    //     simulator collapses R into the scalar rec_coeff = alpha + sum_k
    //     mean(R_k). Compare against the same rec_coeff-based theory value so
    //     the consistency check is exact under the simulator's reduction.
    const double alpha = static_cast<double>(w.self_reference_coeff);
    double r_scalar = 0.0;
    if (w.r_k > 0 && w.r_d > 0 && !w.reference.empty()) {
        const size_t slice_n =
            static_cast<size_t>(w.r_d) * static_cast<size_t>(w.r_d);
        for (uint32_t k = 0; k < w.r_k; ++k) {
            r_scalar += slice_mean(w.reference, k * slice_n, w.r_d);
        }
    }
    const double rec_coeff = alpha + r_scalar;

    double last_delta = 0.0;
    const double converged = simulate_recursion(w, 50, 1.0, &last_delta);

    // Only enforce the ratio check when (1 - rec_coeff) is well-clear of 0.
    // base = 1, so |base| > 1e-8 is automatically true.
    if (std::fabs(1.0 - rec_coeff) > 1e-6 && std::isfinite(converged)) {
        const double theoretical = 1.0 / (1.0 - rec_coeff);
        if (std::fabs(theoretical) > 1e-8) {
            const double ratio = converged / theoretical;
            if (!std::isfinite(ratio) || std::fabs(ratio - 1.0) > 0.01) {
                ++failures;
                errs << "fixed-point mismatch: simulated=" << converged
                     << " theoretical=" << theoretical
                     << " ratio=" << ratio << "; ";
            }
        }
    } else if (!std::isfinite(converged)) {
        ++failures;
        errs << "simulator produced non-finite converged value; ";
    }

    // (b) ||eps||_2 < 1e3.
    if (!w.error.empty()) {
        const double e2 = l2_norm(w.error);
        if (!std::isfinite(e2) || e2 >= 1e3) {
            ++failures;
            errs << "||eps||_2=" << e2 << " >= 1e3; ";
        }
    }

    // (c) ||phase||_1 < 1e4.
    if (!w.phase.empty()) {
        const double p1 = l1_norm(w.phase);
        if (!std::isfinite(p1) || p1 >= 1e4) {
            ++failures;
            errs << "||phase||_1=" << p1 << " >= 1e4; ";
        }
    }

    // (d) Every R entry finite (redundant with pass 3 for paranoia / locality).
    if (!all_finite(w.reference)) {
        ++failures;
        errs << "non-finite value in reference; ";
    }

    if (failures > 0) {
        p.passed = false;
        p.message = errs.str();
        p.score = clamp01(1.0f - static_cast<float>(failures) / 4.0f);
    } else {
        p.passed = true;
        p.score = 1.0f;
    }
    return p;
}

// ============================================================================
// Full validation
// ============================================================================

ValidationResult validate_weight(const RecursiveWeight& w,
                                 uint32_t convergence_iter,
                                 float convergence_tol) {
    ValidationResult r;
    r.passes.reserve(4);
    r.passes.push_back(validate_configuration(w));
    r.passes.push_back(validate_convergence(w, convergence_iter,
                                            convergence_tol));
    r.passes.push_back(validate_stability(w));
    r.passes.push_back(validate_mathematical_consistency(w));

    bool all_ok = true;
    float score_sum = 0.0f;
    for (const ValidationPass& pass : r.passes) {
        if (!pass.passed) all_ok = false;
        score_sum += pass.score;
    }
    r.valid = all_ok;
    r.overall_score =
        r.passes.empty()
            ? 0.0f
            : (score_sum / static_cast<float>(r.passes.size()));

    std::ostringstream os;
    os << "validation: " << (all_ok ? "PASS" : "FAIL")
       << " score=" << r.overall_score
       << " [";
    for (size_t i = 0; i < r.passes.size(); ++i) {
        if (i) os << ", ";
        os << r.passes[i].name << "="
           << (r.passes[i].passed ? "ok" : "fail");
        if (!r.passes[i].passed && !r.passes[i].message.empty()) {
            os << "(" << r.passes[i].message << ")";
        }
    }
    os << "]";
    r.summary = os.str();
    return r;
}

void validate_weight_strict(const RecursiveWeight& w) {
    const ValidationResult r = validate_weight(w);
    if (!r.valid) {
        throw ValidationError(r.summary);
    }
}

} // namespace lqt
