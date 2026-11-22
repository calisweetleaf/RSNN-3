// lqt/tests/test_recursive_weight.cpp — Module A6: Recursive Weight tests.
//
// Canon: lqt.md §5 "Five-Dimensional Semantic Logic and Recursive Operations"
// Briefing: §3 "Mathematical Formalism: Recursive Weights"
//
// Tests:
//   1.  Serialize/parse round-trip for all five W components (B, Φ, R, T, ε).
//   2.  reconstruct() is finite and |value| > 1e-6 for a representative weight.
//   3.  phase_at(t) is finite, bounded (|.| < 1e3), and varies across t values.
//   4.  validate() passes on a well-formed weight.
//   5.  validate() throws ValidationError when reference.size() != r_k*r_d*r_d.
//   6.  validate() throws ValidationError on another reference dimension mismatch.
//   7.  Changing a codebook entry changes reconstruct() output.
//   8.  reference_energy() returns finite non-negative value; 0 for empty R.
//   9.  Empty phase/error vectors behave gracefully.
//   10. phase_at(t=0) is zero (all sin(0)=0).

#include "lqt/recursive_weight.h"
#include "test_framework.h"

#include <array>
#include <cmath>
#include <iostream>
#include <vector>

using namespace lqt;

// ============================================================================
// Helpers
// ============================================================================

static RecursiveWeight make_sample_weight() {
    RecursiveWeight w;
    w.base_index = 2;
    w.phase = {0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.6f, 0.7f, 0.8f};
    w.r_k = 2;
    w.r_d = 3;
    w.reference.resize(static_cast<size_t>(w.r_k) * w.r_d * w.r_d);
    for (size_t i = 0; i < w.reference.size(); ++i) {
        w.reference[i] = static_cast<float>(i) * 0.05f;
    }
    w.tensor_position = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f};
    w.error = {0.01f, 0.02f, 0.03f, 0.04f, 0.05f, 0.06f, 0.07f, 0.08f};
    w.self_reference_coeff = 0.3f; // non-default to exercise wire round-trip
    return w;
}

static Codebook make_scalar_codebook() {
    Codebook cb(1, 8, 1);
    const float vals[] = {-2.0f, -1.5f, 1.0f, 0.5f, 0.75f, 1.5f, 2.0f, 2.5f};
    for (uint32_t i = 0; i < 8; ++i) cb.set_scalar(i, vals[i]);
    return cb;
}

// ============================================================================
// Test 1: Serialize / parse round-trip (all 5 components)
// ============================================================================
TEST_CASE(round_trip_serialize_parse) {
    RecursiveWeight orig = make_sample_weight();

    ByteWriter bw;
    orig.serialize(bw);

    ByteReader br(bw.bytes());
    RecursiveWeight loaded = RecursiveWeight::parse(br);

    // B
    CHECK_EQ(loaded.base_index, orig.base_index);

    // Φ
    CHECK_EQ(loaded.phase.size(), orig.phase.size());
    for (size_t i = 0; i < orig.phase.size(); ++i) {
        CHECK(std::abs(loaded.phase[i] - orig.phase[i]) < 1e-6f);
    }

    // R dims and data
    CHECK_EQ(loaded.r_k, orig.r_k);
    CHECK_EQ(loaded.r_d, orig.r_d);
    CHECK_EQ(loaded.reference.size(), orig.reference.size());
    for (size_t i = 0; i < orig.reference.size(); ++i) {
        CHECK(std::abs(loaded.reference[i] - orig.reference[i]) < 1e-6f);
    }

    // T — all 5 position components
    for (size_t i = 0; i < 5; ++i) {
        CHECK(std::abs(loaded.tensor_position[i] - orig.tensor_position[i]) < 1e-6f);
    }

    // ε
    CHECK_EQ(loaded.error.size(), orig.error.size());
    for (size_t i = 0; i < orig.error.size(); ++i) {
        CHECK(std::abs(loaded.error[i] - orig.error[i]) < 1e-6f);
    }

    // α — self_reference_coeff now wired into wire format (Patch 5)
    CHECK(std::abs(loaded.self_reference_coeff - orig.self_reference_coeff) < 1e-6f);

    // All bytes consumed
    CHECK_EQ(br.remaining(), size_t(0));
}

// ============================================================================
// Test 2: reconstruct() finite and |value| > 1e-6
// ============================================================================
TEST_CASE(reconstruct_finite_and_nontrivial) {
    RecursiveWeight w = make_sample_weight();
    Codebook cb = make_scalar_codebook();
    const float scale = 1.5f;

    const float val = w.reconstruct(cb, scale, 0.0);

    CHECK(std::isfinite(val));
    CHECK(std::abs(val) > 1e-6f);
}

// ============================================================================
// Test 3: phase_at(t) finite, bounded (|.| < 1e3), and varies with t
// ============================================================================
TEST_CASE(phase_at_finite_bounded_varying) {
    RecursiveWeight w = make_sample_weight();

    // Compute L1-norm bound (sum of |phase[i]|); result must not exceed it.
    float l1_bound = 0.0f;
    for (float p : w.phase) l1_bound += std::abs(p);

    const double times[] = {0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 3.14159};
    float vals[7];

    for (int k = 0; k < 7; ++k) {
        vals[k] = w.phase_at(times[k]);
        CHECK(std::isfinite(vals[k]));
        CHECK(std::abs(vals[k]) <= l1_bound + 1e-4f);
        CHECK(std::abs(vals[k]) < 1e3f);
    }

    // Must vary across different time values.
    bool has_variation = false;
    for (int k = 1; k < 7; ++k) {
        if (std::abs(vals[k] - vals[0]) > 1e-6f) { has_variation = true; break; }
    }
    CHECK(has_variation);
}

// ============================================================================
// Test 4: validate() passes on a well-formed weight
// ============================================================================
TEST_CASE(validate_passes_for_valid_weight) {
    RecursiveWeight w = make_sample_weight();
    w.validate(); // must not throw
}

// ============================================================================
// Test 5: validate() throws ValidationError when reference.size() != r_k*r_d*r_d
// ============================================================================
TEST_CASE(validate_throws_on_bad_reference_size) {
    RecursiveWeight w = make_sample_weight();
    w.reference.pop_back(); // corrupt: now size < r_k*r_d*r_d
    CHECK_THROWS_AS(w.validate(), ValidationError);
}

// ============================================================================
// Test 6: validate() throws ValidationError when r_d is inflated (mismatch)
// ============================================================================
TEST_CASE(validate_throws_on_dim_mismatch) {
    RecursiveWeight w = make_sample_weight();
    w.r_d = 10; // expected = 2*10*10 = 200, actual reference.size() = 18
    CHECK_THROWS_AS(w.validate(), ValidationError);
}

// ============================================================================
// Test 7: Changing a codebook entry changes reconstruct() output
// ============================================================================
// validate() must throw when |self_reference_coeff| >= 1.0 (Patch 5)
TEST_CASE(validate_throws_on_alpha_out_of_range) {
    RecursiveWeight w = make_sample_weight();
    w.self_reference_coeff = 1.0f; // boundary: >= 1 is invalid
    CHECK_THROWS_AS(w.validate(), ValidationError);
    w.self_reference_coeff = -1.0f; // negative boundary also invalid
    CHECK_THROWS_AS(w.validate(), ValidationError);
    w.self_reference_coeff = 0.99f; // just inside → should pass
    w.validate(); // must not throw
}

TEST_CASE(changing_codebook_changes_reconstruct) {
    RecursiveWeight w = make_sample_weight();
    const float scale = 1.0f;
    const double t = 0.0;

    Codebook cb1 = make_scalar_codebook();
    const float val1 = w.reconstruct(cb1, scale, t);

    Codebook cb2 = make_scalar_codebook();
    cb2.set_scalar(w.base_index, 99.0f); // drastically different entry
    const float val2 = w.reconstruct(cb2, scale, t);

    CHECK(std::isfinite(val1));
    CHECK(std::isfinite(val2));
    CHECK(std::abs(val1 - val2) > 1e-4f); // output must differ
}

// ============================================================================
// Test 8: reference_energy() finite, non-negative; zero for empty R
// ============================================================================
TEST_CASE(reference_energy_finite_nonneg) {
    RecursiveWeight w = make_sample_weight();
    const float e = w.reference_energy();
    CHECK(std::isfinite(e));
    CHECK(e >= 0.0f);
    CHECK(e > 0.0f); // sample has non-zero entries

    RecursiveWeight empty;
    CHECK(empty.reference_energy() == 0.0f);
}

// ============================================================================
// Test 9: Empty phase/error vectors behave gracefully
// ============================================================================
TEST_CASE(empty_vectors_graceful) {
    RecursiveWeight w;
    w.base_index = 0;
    w.r_k = 0;
    w.r_d = 0;
    w.tensor_position = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};

    // phase_at with empty phase must return 0.
    CHECK(w.phase_at(1.234) == 0.0f);

    // Serialize / parse with empty vectors.
    ByteWriter bw;
    w.serialize(bw);
    ByteReader br(bw.bytes());
    RecursiveWeight loaded = RecursiveWeight::parse(br);

    CHECK(loaded.phase.empty());
    CHECK(loaded.error.empty());
    CHECK_EQ(loaded.r_k, uint32_t(0));
    CHECK_EQ(loaded.r_d, uint32_t(0));
    CHECK(loaded.reference.empty());
    CHECK_EQ(br.remaining(), size_t(0));
}

// ============================================================================
// Test 10: phase_at(t=0) is exactly 0 (sin(0)=0 for every harmonic)
// ============================================================================
TEST_CASE(phase_at_zero_is_zero) {
    RecursiveWeight w = make_sample_weight();
    const float pv = w.phase_at(0.0);
    CHECK(std::abs(pv) < 1e-6f);
}

// ============================================================================
// Main
// ============================================================================
int main() {
    return lqttest::run_all();
}
