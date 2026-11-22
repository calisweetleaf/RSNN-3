// lqt/mutation.h — 4-constraint Mutation Validation Framework.
//
// Council module: A7 (mutation safety layer).
// Canon: lqt.md §5.2 (Mutation Validation Framework).
// Transitioning doc §4 (4-constraint validation).
//
// The four constraints, as required by canon §5.2 / transitioning §4:
//   (1) Dimension Constraints — tensor shape change compatibility.
//   (2) Value Bounds          — all floats finite AND within [value_lo, value_hi].
//   (3) Topology Rules        — module graph is acyclic and fully resolved.
//   (4) Access Control        — Protected tensors require authorization.
//
// DESIGN DECISION: MutationValidator is decoupled from any concrete codebook,
// delta, or mask type.  It operates exclusively on TensorDescriptor + abstract
// arguments so that the lead's model layer can wire it to concrete state.
#pragma once

#include <cmath>
#include <map>
#include <string>
#include <vector>

#include "lqt/descriptor.h"
#include "lqt/error.h"
#include "lqt/format.h"

namespace lqt {

// ---------------------------------------------------------------------------
// ValidationResult — outcome of a single constraint check
// ---------------------------------------------------------------------------
struct ValidationResult {
    bool        ok     = true;
    std::string reason;

    // Convenience: build a passing result.
    static ValidationResult pass() { return {true, {}}; }

    // Convenience: build a failing result with a reason string.
    static ValidationResult fail(std::string r) { return {false, std::move(r)}; }
};

// ---------------------------------------------------------------------------
// MutationValidator — implements all 4 mutation constraints
// ---------------------------------------------------------------------------
class MutationValidator {
public:
    // Create a validator with configurable value-bound range.
    // Default: all finite float values are acceptable.
    explicit MutationValidator(float value_lo = -1e30f, float value_hi = 1e30f)
        : value_lo_(value_lo), value_hi_(value_hi) {}

    // --- Constraint 1: Dimension Constraints --------------------------------
    // Validates that the proposed_shape is compatible with the current tensor's
    // shape.  "Compatible" means element_count(proposed) == element_count(current)
    // (same number of elements, shapes may be permuted/reshaped).
    // If current descriptor has no shape (empty), any proposed shape is accepted.
    ValidationResult check_dimensions(
        const TensorDescriptor&       current,
        const std::vector<uint32_t>&  proposed_shape) const;

    // --- Constraint 2: Value Bounds -----------------------------------------
    // All n float values at `values` must be finite (not NaN, not ±Inf) AND
    // within [value_lo_, value_hi_].  Returns fail on the first offending index.
    ValidationResult check_value_bounds(const float* values, size_t n) const;

    // --- Constraint 3: Topology Rules ---------------------------------------
    // Validates that:
    //   (a) `target` is a key in module_graph.
    //   (b) Every string in each adjacency list is also a key in module_graph
    //       (all edges resolve).
    //   (c) The graph is acyclic — implemented with iterative DFS.
    // Returns fail if any of (a)-(c) is violated.
    ValidationResult check_topology(
        const std::string&                                    target,
        const std::map<std::string, std::vector<std::string>>& module_graph) const;

    // --- Constraint 4: Access Control ---------------------------------------
    // If target_desc has the TensorFlag::Protected flag set, access is denied
    // unless `authorized` is true.
    // A non-protected tensor always passes regardless of `authorized`.
    ValidationResult check_access(
        const TensorDescriptor& target_desc,
        bool                    authorized) const;

    // --- Convenience: run all applicable checks -----------------------------
    // Runs check_dimensions, check_value_bounds, check_access, and
    // check_topology (if module_graph is non-empty) in sequence and returns
    // the first failure, or ValidationResult::pass() if all succeed.
    //
    // Pass nullptr for values / 0 for n to skip check_value_bounds.
    // Pass an empty module_graph to skip check_topology.
    ValidationResult validate(
        const TensorDescriptor&                                target_desc,
        const std::vector<uint32_t>&                           proposed_shape,
        const float*                                           values,
        size_t                                                 n,
        bool                                                   authorized,
        const std::map<std::string, std::vector<std::string>>& module_graph = {}) const;

    // Getters / setters for the value bound range.
    float value_lo() const noexcept { return value_lo_; }
    float value_hi() const noexcept { return value_hi_; }
    void set_value_bounds(float lo, float hi) { value_lo_ = lo; value_hi_ = hi; }

private:
    float value_lo_;
    float value_hi_;
};

} // namespace lqt
