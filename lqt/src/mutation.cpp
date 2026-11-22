// src/mutation.cpp — Mutation Validation Framework implementation.
//
// Council module: A7 (mutation safety layer).
// Canon: lqt.md §5.2 (Mutation Validation Framework).
// Transitioning doc §4 (4-constraint validation).
#include "lqt/mutation.h"

#include <cmath>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

namespace lqt {

// ---------------------------------------------------------------------------
// Constraint 1: Dimension Constraints
// ---------------------------------------------------------------------------
ValidationResult MutationValidator::check_dimensions(
    const TensorDescriptor&      current,
    const std::vector<uint32_t>& proposed_shape) const
{
    // An empty current shape means there is no established geometry — accept anything.
    if (current.shape.empty()) {
        return ValidationResult::pass();
    }

    // Compute element counts.
    uint64_t current_elems = 1;
    for (uint32_t d : current.shape) {
        current_elems *= d;
    }

    uint64_t proposed_elems = 1;
    for (uint32_t d : proposed_shape) {
        proposed_elems *= d;
    }

    if (current_elems != proposed_elems) {
        std::ostringstream oss;
        oss << "Dimension mismatch: current element count " << current_elems
            << " != proposed element count " << proposed_elems;
        return ValidationResult::fail(oss.str());
    }
    return ValidationResult::pass();
}

// ---------------------------------------------------------------------------
// Constraint 2: Value Bounds
// ---------------------------------------------------------------------------
ValidationResult MutationValidator::check_value_bounds(
    const float* values, size_t n) const
{
    if (values == nullptr || n == 0) {
        return ValidationResult::pass();
    }

    for (size_t i = 0; i < n; ++i) {
        float v = values[i];
        // Must be finite (not NaN, not +-Inf).
        if (!std::isfinite(v)) {
            std::ostringstream oss;
            oss << "Value at index " << i << " is non-finite (" << v << ")";
            return ValidationResult::fail(oss.str());
        }
        // Must be within [value_lo_, value_hi_].
        if (v < value_lo_ || v > value_hi_) {
            std::ostringstream oss;
            oss << "Value at index " << i << " (" << v
                << ") is outside bounds [" << value_lo_ << ", " << value_hi_ << "]";
            return ValidationResult::fail(oss.str());
        }
    }
    return ValidationResult::pass();
}

// ---------------------------------------------------------------------------
// Constraint 3: Topology Rules (DFS cycle detection)
// ---------------------------------------------------------------------------

// DESIGN DECISION: iterative DFS using an explicit stack and a three-colour
// visit state (unvisited / in-stack / done) to reliably detect back-edges
// that form cycles.  A back-edge exists when we encounter a node that is
// currently on the DFS stack (grey).

ValidationResult MutationValidator::check_topology(
    const std::string&                                    target,
    const std::map<std::string, std::vector<std::string>>& module_graph) const
{
    // (a) Target must exist.
    if (module_graph.find(target) == module_graph.end()) {
        return ValidationResult::fail(
            "Topology: target module '" + target + "' not found in module graph");
    }

    // (b) All edge destinations must resolve (exist as keys).
    for (const auto& kv : module_graph) {
        for (const auto& dep : kv.second) {
            if (module_graph.find(dep) == module_graph.end()) {
                return ValidationResult::fail(
                    "Topology: module '" + kv.first +
                    "' has unresolved dependency '" + dep + "'");
            }
        }
    }

    // (c) No cycle — iterative DFS from every node to handle disconnected components.
    // Colour coding: 0 = unvisited, 1 = on stack (grey), 2 = finished (black).
    std::unordered_map<std::string, int> colour;
    for (const auto& kv : module_graph) {
        colour[kv.first] = 0;
    }

    // We use an explicit stack of (node, iterator-into-adjacency-list) pairs.
    // When we push a node we colour it grey (1).
    // When we exhaust its neighbours we colour it black (2).
    for (const auto& kv : module_graph) {
        if (colour[kv.first] != 0) continue; // already visited

        // DFS stack: each element is (node_name, index_of_next_child_to_visit).
        struct Frame { std::string node; size_t child_idx; };
        std::vector<Frame> stack;

        colour[kv.first] = 1; // grey
        stack.push_back({kv.first, 0});

        while (!stack.empty()) {
            Frame& top = stack.back();
            const auto& neighbours = module_graph.at(top.node);

            if (top.child_idx < neighbours.size()) {
                const std::string& nbr = neighbours[top.child_idx];
                ++top.child_idx;

                int c = colour[nbr];
                if (c == 1) {
                    // Back-edge detected — cycle found.
                    return ValidationResult::fail(
                        "Topology: cycle detected involving module '" + nbr + "'");
                }
                if (c == 0) {
                    colour[nbr] = 1; // grey
                    stack.push_back({nbr, 0});
                }
                // c == 2: already finished, skip.
            } else {
                // All children explored — finish this node.
                colour[top.node] = 2; // black
                stack.pop_back();
            }
        }
    }

    return ValidationResult::pass();
}

// ---------------------------------------------------------------------------
// Constraint 4: Access Control
// ---------------------------------------------------------------------------
ValidationResult MutationValidator::check_access(
    const TensorDescriptor& target_desc,
    bool                    authorized) const
{
    if (target_desc.has_flag(TensorFlag::Protected) && !authorized) {
        return ValidationResult::fail(
            "Access denied: tensor '" + target_desc.name +
            "' is Protected and the operation is not authorized");
    }
    return ValidationResult::pass();
}

// ---------------------------------------------------------------------------
// Convenience: validate
// ---------------------------------------------------------------------------
ValidationResult MutationValidator::validate(
    const TensorDescriptor&                                target_desc,
    const std::vector<uint32_t>&                           proposed_shape,
    const float*                                           values,
    size_t                                                 n,
    bool                                                   authorized,
    const std::map<std::string, std::vector<std::string>>& module_graph) const
{
    // (1) Dimensions.
    {
        auto r = check_dimensions(target_desc, proposed_shape);
        if (!r.ok) return r;
    }
    // (2) Value bounds.
    if (values != nullptr && n > 0) {
        auto r = check_value_bounds(values, n);
        if (!r.ok) return r;
    }
    // (3) Topology (only if a graph is provided).
    if (!module_graph.empty()) {
        auto r = check_topology(target_desc.name, module_graph);
        if (!r.ok) return r;
    }
    // (4) Access control.
    {
        auto r = check_access(target_desc, authorized);
        if (!r.ok) return r;
    }
    return ValidationResult::pass();
}

} // namespace lqt
