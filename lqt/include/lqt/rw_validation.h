// lqt/rw_validation.h — RecursiveWeight 4-pass validation engine.
// Ports ValidationEngine from recursive_weights_core.py.
// Council: Tyr (Patch 4).
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "lqt/error.h"
#include "lqt/recursive_weight.h"

namespace lqt {

// ── Per-pass validation result ──────────────────────────────────────────────
struct ValidationPass {
    bool        passed   = true;
    std::string name;
    std::string message;     // populated when failed
    float       score = 1.0f; // 0..1 quality score
};

// ── Full validation result ──────────────────────────────────────────────────
struct ValidationResult {
    bool                       valid   = true;
    std::vector<ValidationPass> passes;   // exactly 4 entries
    std::string                summary;
    float                      overall_score = 1.0f;

    // True if ALL passes passed.
    explicit operator bool() const { return valid; }
};

// ── Pass 1: Configuration Validation ───────────────────────────────────────
// Checks:
//   - self_reference_coeff (alpha) in (-1, 1) exclusive — convergence requires |alpha| < 1
//   - r_k * r_d * r_d == reference.size() when reference is non-empty
//   - phase vector is non-empty or a note is emitted (warning, not failure)
//   - tensor_position has exactly 5 elements
//   - base_index < some reasonable cap (< 1<<20)
ValidationPass validate_configuration(const RecursiveWeight& w);

// ── Pass 2: Convergence Validation ─────────────────────────────────────────
// Simulates the recursion for max_iter steps using a unit codebook (value=1.0, scale=1.0).
// Checks that the recursion converges (|val[i] - val[i-1]| < convergence_tol after enough steps).
// Also checks that the Frobenius norm of R slices satisfies the Lyapunov condition.
// max_iter: default 50. convergence_tol: default 1e-4.
ValidationPass validate_convergence(const RecursiveWeight& w,
                                    uint32_t max_iter = 50,
                                    float convergence_tol = 1e-4f);

// ── Pass 3: Stability Validation ────────────────────────────────────────────
// Checks that the spectral radius of each R slice (approximated by power iteration)
// is bounded: rho(R_i) < 1/k where k = r_k.
// Also checks all float fields (phase, reference, error, self_reference_coeff) are finite.
ValidationPass validate_stability(const RecursiveWeight& w);

// ── Pass 4: Mathematical Consistency ────────────────────────────────────────
// Checks:
//   - Fixed-point formula is self-consistent: base/(1-alpha) within 1% of converged value
//   - Error preservation vector has bounded norm (||eps||_2 < 1e3)
//   - Phase vector energy is bounded (||phase||_1 < 1e4)
//   - R matrix entries are all finite
ValidationPass validate_mathematical_consistency(const RecursiveWeight& w);

// ── Full validation (runs all 4 passes) ─────────────────────────────────────
// Runs all 4 passes sequentially. Overall valid = all 4 pass.
// Does NOT throw — returns ValidationResult with details.
ValidationResult validate_weight(const RecursiveWeight& w,
                                 uint32_t convergence_iter = 50,
                                 float convergence_tol     = 1e-4f);

// ── Strict variant: throws ValidationError on any failure ───────────────────
void validate_weight_strict(const RecursiveWeight& w);

} // namespace lqt
