// lqt/src/rta_ops.cpp — Higher-level RTA tensor operations implementation.
//
// Council module: Odin (Patch 4).
// Ported from recursive_tensor.py: contract(), project(), expand().
//
// All math is manual: no torch, no numpy.  std::vector<float> backs the dense
// container, std::unordered_map backs the sparse one.  Designed to compile
// cleanly under -Wall -Wextra -Wpedantic with C++17.

#include "lqt/rta_ops.h"

#include <algorithm>
#include <cmath>
#include <cstring>
#include <numeric>
#include <stdexcept>
#include <string>

namespace lqt {

// ============================================================================
// Internal helpers
// ============================================================================
namespace {

constexpr float kSparseEpsilon = 1e-8f;

// Build a row-major stride table for a 5D shape (slowest-varying first).
std::array<size_t, 5> compute_strides(const std::array<uint32_t, 5>& shape) {
    std::array<size_t, 5> s{};
    s[4] = 1;
    s[3] = s[4] * static_cast<size_t>(shape[4]);
    s[2] = s[3] * static_cast<size_t>(shape[3]);
    s[1] = s[2] * static_cast<size_t>(shape[2]);
    s[0] = s[1] * static_cast<size_t>(shape[1]);
    return s;
}

// Product of all five entries of a shape array as size_t.
size_t shape_product(const std::array<uint32_t, 5>& shape) {
    size_t p = 1;
    for (auto v : shape) p *= static_cast<size_t>(v);
    return p;
}

// True if `axis` is a member of `axes` (linear scan; axes lists are tiny).
bool contains_axis(const std::vector<uint32_t>& axes, uint32_t axis) {
    for (auto a : axes) {
        if (a == axis) return true;
    }
    return false;
}

// The "effective rank" of a dense tensor is the position of the last axis
// whose size is > 1, plus one.  Trailing 1-axes are treated as padding.
// Returns 0 for a scalar (all dims == 1).
uint32_t effective_rank(const std::array<uint32_t, 5>& shape) {
    for (int i = 4; i >= 0; --i) {
        if (shape[static_cast<size_t>(i)] > 1) {
            return static_cast<uint32_t>(i + 1);
        }
    }
    return 0;
}

// Validate that every axis listed in `axes` is < 5.  Throws on violation.
void check_axes_in_range(const std::vector<uint32_t>& axes, const char* who) {
    for (auto a : axes) {
        if (a >= 5) {
            throw ValidationError(std::string(who) + ": axis " +
                                  std::to_string(a) + " out of range (max 4)");
        }
    }
}

} // namespace

// ============================================================================
// DenseTensor5D members
// ============================================================================

size_t DenseTensor5D::flat_index(const RtaIndex& idx) const {
    for (size_t d = 0; d < 5; ++d) {
        if (idx[d] >= shape[d]) {
            throw ValidationError("DenseTensor5D::flat_index: axis " +
                                  std::to_string(d) + " index " +
                                  std::to_string(idx[d]) +
                                  " out of range (size " +
                                  std::to_string(shape[d]) + ")");
        }
    }
    const auto s = compute_strides(shape);
    size_t off = 0;
    for (size_t d = 0; d < 5; ++d) {
        off += static_cast<size_t>(idx[d]) * s[d];
    }
    return off;
}

float DenseTensor5D::at(const RtaIndex& idx) const {
    const size_t off = flat_index(idx);
    if (off >= data.size()) {
        throw ValidationError("DenseTensor5D::at: computed offset exceeds data size");
    }
    return data[off];
}

void DenseTensor5D::set(const RtaIndex& idx, float v) {
    const size_t off = flat_index(idx);
    if (off >= data.size()) {
        throw ValidationError("DenseTensor5D::set: computed offset exceeds data size");
    }
    data[off] = v;
}

size_t DenseTensor5D::numel() const noexcept {
    return shape_product(shape);
}

// ============================================================================
// rta_contract — dense × dense → dense
// ============================================================================
//
// Layout strategy:
//   * Determine the list of "free" axes of a (axes NOT in axes_a) and of
//     b (axes NOT in axes_b), preserving original order.
//   * The result's logical axes are: free_a ... free_b (numpy.tensordot order)
//     padded with size-1 axes up to rank 5.
//   * Iterate over every combination of free-a indices, every combination of
//     free-b indices, and for each pair iterate over the contracted indices
//     summing a[full_a_idx] * b[full_b_idx].
//
// Verification: axes_a.size() must equal axes_b.size() and for each pair
// (axes_a[i], axes_b[i]) the two shapes must match.

DenseTensor5D rta_contract(const DenseTensor5D& a,
                           const DenseTensor5D& b,
                           const std::vector<uint32_t>& axes_a,
                           const std::vector<uint32_t>& axes_b)
{
    if (axes_a.size() != axes_b.size()) {
        throw ValidationError("rta_contract: axes_a and axes_b must have equal length");
    }
    check_axes_in_range(axes_a, "rta_contract");
    check_axes_in_range(axes_b, "rta_contract");
    if (a.data.size() != a.numel() || b.data.size() != b.numel()) {
        throw ValidationError("rta_contract: tensor data size does not match shape");
    }

    // Verify matching contracted dimensions.
    for (size_t i = 0; i < axes_a.size(); ++i) {
        const uint32_t da = a.shape[axes_a[i]];
        const uint32_t db = b.shape[axes_b[i]];
        if (da != db) {
            throw ValidationError(
                "rta_contract: contracted axis size mismatch at pair " +
                std::to_string(i) + " (" + std::to_string(da) + " vs " +
                std::to_string(db) + ")");
        }
    }

    // Build free-axis lists.
    std::vector<uint32_t> free_a, free_b;
    free_a.reserve(5);
    free_b.reserve(5);
    for (uint32_t ax = 0; ax < 5; ++ax) {
        if (!contains_axis(axes_a, ax)) free_a.push_back(ax);
    }
    for (uint32_t ax = 0; ax < 5; ++ax) {
        if (!contains_axis(axes_b, ax)) free_b.push_back(ax);
    }

    // Compute the result shape.  We only keep the axes that are actually
    // populated above size 1 in their source — but to keep things uniform we
    // pack free_a-then-free_b dimensions into the leading positions of the
    // 5D output, padding trailing axes with size 1.
    DenseTensor5D out;
    out.shape.fill(1);

    const size_t total_free = free_a.size() + free_b.size();
    if (total_free > 5) {
        throw ValidationError("rta_contract: result rank exceeds 5 "
                              "(free_a=" + std::to_string(free_a.size()) +
                              ", free_b=" + std::to_string(free_b.size()) + ")");
    }

    // Build a list of (source: 0=a/1=b, source_axis) describing each output dim.
    // 0 means "this output axis comes from a's free axis at index i in free_a".
    struct OutDimSrc { int source; uint32_t src_axis; };
    std::array<OutDimSrc, 5> out_src{};
    size_t out_dim = 0;
    for (uint32_t ax : free_a) {
        out.shape[out_dim] = a.shape[ax];
        out_src[out_dim] = {0, ax};
        ++out_dim;
    }
    for (uint32_t ax : free_b) {
        out.shape[out_dim] = b.shape[ax];
        out_src[out_dim] = {1, ax};
        ++out_dim;
    }

    out.data.assign(shape_product(out.shape), 0.0f);

    // Precompute the contracted shape (product of contracted dims).
    std::vector<uint32_t> contracted_sizes;
    contracted_sizes.reserve(axes_a.size());
    for (size_t i = 0; i < axes_a.size(); ++i) {
        contracted_sizes.push_back(a.shape[axes_a[i]]);
    }

    // Number of free index combinations.
    const auto out_strides = compute_strides(out.shape);

    // Iterate via odometers over the output coordinate space.
    RtaIndex out_idx{0, 0, 0, 0, 0};
    const size_t out_total = out.data.size();
    for (size_t flat = 0; flat < out_total; ++flat) {
        // Decode flat -> out_idx.
        {
            size_t rem = flat;
            for (size_t d = 0; d < 5; ++d) {
                out_idx[d] = static_cast<uint32_t>(rem / out_strides[d]);
                rem        = rem % out_strides[d];
            }
        }

        // Build the base a-index and b-index from free axes only (contracted
        // axes are left at 0 to be filled by the inner loop below).
        RtaIndex a_idx{0, 0, 0, 0, 0};
        RtaIndex b_idx{0, 0, 0, 0, 0};
        for (size_t d = 0; d < total_free; ++d) {
            if (out_src[d].source == 0) {
                a_idx[out_src[d].src_axis] = out_idx[d];
            } else {
                b_idx[out_src[d].src_axis] = out_idx[d];
            }
        }

        // Iterate over the contracted index space (product of contracted_sizes).
        size_t contracted_total = 1;
        for (auto v : contracted_sizes) contracted_total *= v;

        double acc = 0.0;
        for (size_t cflat = 0; cflat < contracted_total; ++cflat) {
            // Decode cflat into per-contracted-axis indices.  Use row-major
            // order over contracted_sizes (last axis fastest).
            size_t rem = cflat;
            for (size_t i = 0; i < axes_a.size(); ++i) {
                // Compute the stride for this contracted axis.
                size_t stride = 1;
                for (size_t j = i + 1; j < axes_a.size(); ++j) {
                    stride *= static_cast<size_t>(contracted_sizes[j]);
                }
                const uint32_t k = static_cast<uint32_t>(rem / stride);
                rem = rem % stride;
                a_idx[axes_a[i]] = k;
                b_idx[axes_b[i]] = k;
            }
            acc += static_cast<double>(a.data[a.flat_index(a_idx)]) *
                   static_cast<double>(b.data[b.flat_index(b_idx)]);
        }
        out.data[flat] = static_cast<float>(acc);
    }

    return out;
}

// ============================================================================
// rta_contract_sparse — sparse × sparse → sparse
// ============================================================================
//
// Direct port of _sparse_tensor_contract in the Python reference: iterate
// over the cartesian product of non-zero entries in a and b, and accumulate
// where the contracted-axis coordinates agree.
//
// Result indexing: remaining a-axes first, then remaining b-axes.  Output is
// also a SparseTensor5D, so we again pack the surviving (free_a + free_b)
// axes into the leading positions of a 5-tuple and zero-pad the rest.

SparseTensor5D rta_contract_sparse(const SparseTensor5D& a,
                                   const SparseTensor5D& b,
                                   const std::vector<uint32_t>& axes_a,
                                   const std::vector<uint32_t>& axes_b)
{
    if (axes_a.size() != axes_b.size()) {
        throw ValidationError("rta_contract_sparse: axes_a and axes_b must "
                              "have equal length");
    }
    check_axes_in_range(axes_a, "rta_contract_sparse");
    check_axes_in_range(axes_b, "rta_contract_sparse");

    std::vector<uint32_t> free_a, free_b;
    free_a.reserve(5);
    free_b.reserve(5);
    for (uint32_t ax = 0; ax < 5; ++ax) {
        if (!contains_axis(axes_a, ax)) free_a.push_back(ax);
    }
    for (uint32_t ax = 0; ax < 5; ++ax) {
        if (!contains_axis(axes_b, ax)) free_b.push_back(ax);
    }
    const size_t total_free = free_a.size() + free_b.size();
    if (total_free > 5) {
        throw ValidationError("rta_contract_sparse: result rank exceeds 5");
    }

    SparseTensor5D out;
    out.reserve(a.size());  // rough lower bound; map grows as needed.

    for (const auto& entry_a : a) {
        const RtaIndex& idx_a = entry_a.first;
        const float     val_a = entry_a.second;
        for (const auto& entry_b : b) {
            const RtaIndex& idx_b = entry_b.first;
            const float     val_b = entry_b.second;

            // All contracted axes must agree.
            bool match = true;
            for (size_t i = 0; i < axes_a.size(); ++i) {
                if (idx_a[axes_a[i]] != idx_b[axes_b[i]]) {
                    match = false;
                    break;
                }
            }
            if (!match) continue;

            // Build result key: free_a coords then free_b coords, padded.
            RtaIndex key{0, 0, 0, 0, 0};
            size_t k = 0;
            for (auto ax : free_a) key[k++] = idx_a[ax];
            for (auto ax : free_b) key[k++] = idx_b[ax];

            const float contribution = val_a * val_b;
            auto it = out.find(key);
            if (it == out.end()) {
                out.emplace(key, contribution);
            } else {
                it->second += contribution;
            }
        }
    }

    // Drop near-zero entries (|v| <= epsilon).
    for (auto it = out.begin(); it != out.end(); ) {
        if (std::fabs(it->second) <= kSparseEpsilon) {
            it = out.erase(it);
        } else {
            ++it;
        }
    }

    return out;
}

// ============================================================================
// rta_project — projection onto an L2-normalised basis along one or more axes
// ============================================================================
//
// For each axis a in `axes`:
//   1. L2-normalise every basis row (rows are basis vectors, length = src axis size).
//   2. Replace the chosen axis dim with basis.size().
//   3. result[..., b_idx along a, ...] = sum_k basis_normalised[b_idx][k] *
//                                        src[..., k along a, ...]
//
// The Python reference uses swapaxes + matmul, but the math is identical to
// the explicit loops below.  We iterate the projected tensor through each
// requested axis in turn.

DenseTensor5D rta_project(const DenseTensor5D& src,
                          const std::vector<std::vector<float>>& basis,
                          const std::vector<uint32_t>& axes)
{
    check_axes_in_range(axes, "rta_project");
    if (src.data.size() != src.numel()) {
        throw ValidationError("rta_project: src data size does not match shape");
    }
    if (basis.empty()) {
        throw ValidationError("rta_project: basis must contain at least one row");
    }
    const size_t basis_cols = basis.front().size();
    if (basis_cols == 0) {
        throw ValidationError("rta_project: basis rows must be non-empty");
    }
    for (const auto& row : basis) {
        if (row.size() != basis_cols) {
            throw ValidationError("rta_project: all basis rows must share length");
        }
    }

    // Normalise basis (L2 per row).  We copy because the inputs are const.
    std::vector<std::vector<float>> nb(basis.size(),
                                        std::vector<float>(basis_cols, 0.0f));
    for (size_t r = 0; r < basis.size(); ++r) {
        double sumsq = 0.0;
        for (size_t c = 0; c < basis_cols; ++c) {
            sumsq += static_cast<double>(basis[r][c]) *
                     static_cast<double>(basis[r][c]);
        }
        const double norm = std::sqrt(sumsq);
        if (norm == 0.0) {
            // Match numpy's behaviour: division by zero would produce NaN/Inf.
            // We throw instead to keep results well-defined.
            throw ValidationError("rta_project: basis row " + std::to_string(r) +
                                  " has zero norm");
        }
        for (size_t c = 0; c < basis_cols; ++c) {
            nb[r][c] = static_cast<float>(static_cast<double>(basis[r][c]) / norm);
        }
    }

    // Start from a copy of the source.
    DenseTensor5D current = src;

    for (uint32_t ax : axes) {
        if (current.shape[ax] != static_cast<uint32_t>(basis_cols)) {
            throw ValidationError(
                "rta_project: basis column count (" +
                std::to_string(basis_cols) +
                ") does not match source axis " + std::to_string(ax) +
                " size (" + std::to_string(current.shape[ax]) + ")");
        }

        // Construct the new shape for this projection step.
        std::array<uint32_t, 5> new_shape = current.shape;
        new_shape[ax] = static_cast<uint32_t>(nb.size());

        DenseTensor5D next;
        next.shape = new_shape;
        next.data.assign(shape_product(new_shape), 0.0f);

        const auto cur_strides  = compute_strides(current.shape);
        const auto next_strides = compute_strides(new_shape);

        const uint32_t src_size = current.shape[ax];
        const uint32_t dst_size = static_cast<uint32_t>(nb.size());

        // Loop over all output coordinates and compute the dot product
        // along the projected axis.
        RtaIndex idx{0, 0, 0, 0, 0};
        const size_t n_out = next.data.size();
        for (size_t flat = 0; flat < n_out; ++flat) {
            size_t rem = flat;
            for (size_t d = 0; d < 5; ++d) {
                idx[d] = static_cast<uint32_t>(rem / next_strides[d]);
                rem    = rem % next_strides[d];
            }

            const uint32_t b_row = idx[ax];
            if (b_row >= dst_size) {
                // Should never happen given the construction above.
                throw ValidationError("rta_project: internal index error");
            }

            // Walk the corresponding source slice across the projected axis.
            RtaIndex src_idx = idx;
            double acc = 0.0;
            for (uint32_t k = 0; k < src_size; ++k) {
                src_idx[ax] = k;
                size_t cur_flat = 0;
                for (size_t d = 0; d < 5; ++d) {
                    cur_flat += static_cast<size_t>(src_idx[d]) * cur_strides[d];
                }
                acc += static_cast<double>(nb[b_row][k]) *
                       static_cast<double>(current.data[cur_flat]);
            }
            next.data[flat] = static_cast<float>(acc);
        }

        current = std::move(next);
    }

    return current;
}

// ============================================================================
// rta_expand — prepend broadcast dimensions
// ============================================================================
//
// Reference behaviour: produce a tensor whose leading axes are the new
// dimensions, with each slice along those axes being a copy of the source.
// Equivalent to: result = ones(new_shape) ⊗ src (outer product).
//
// Constraints: because the dense container has fixed rank 5, the source must
// have effective rank (last-nonsingleton axis + 1) <= 5 - num_new_dims.

DenseTensor5D rta_expand(const DenseTensor5D& src,
                         uint32_t new_size,
                         uint32_t num_new_dims)
{
    if (num_new_dims == 0) {
        // Identity expansion: just copy the source.
        return src;
    }
    if (num_new_dims > 5) {
        throw ValidationError("rta_expand: num_new_dims (" +
                              std::to_string(num_new_dims) +
                              ") exceeds rank 5");
    }
    if (new_size == 0) {
        throw ValidationError("rta_expand: new_size must be >= 1");
    }
    if (src.data.size() != src.numel()) {
        throw ValidationError("rta_expand: src data size does not match shape");
    }

    const uint32_t src_rank = effective_rank(src.shape);
    if (src_rank + num_new_dims > 5) {
        throw ValidationError("rta_expand: src effective rank (" +
                              std::to_string(src_rank) +
                              ") + num_new_dims (" +
                              std::to_string(num_new_dims) +
                              ") exceeds 5");
    }

    // Build new shape: first num_new_dims axes = new_size, then the populated
    // src axes (its first src_rank axes), then 1-padding to rank 5.
    DenseTensor5D out;
    out.shape.fill(1);
    for (uint32_t d = 0; d < num_new_dims; ++d) {
        out.shape[d] = new_size;
    }
    for (uint32_t d = 0; d < src_rank; ++d) {
        out.shape[num_new_dims + d] = src.shape[d];
    }

    out.data.assign(shape_product(out.shape), 0.0f);

    // Source contribution at output position (n0, n1, ..., s0, s1, ...) is
    // simply src[s0, s1, ...] (broadcast along the new axes).  We compute it
    // by iterating over all output coordinates and decoding the source slice.
    const auto out_strides = compute_strides(out.shape);
    const auto src_strides = compute_strides(src.shape);
    const size_t total     = out.data.size();

    RtaIndex out_idx{0, 0, 0, 0, 0};
    for (size_t flat = 0; flat < total; ++flat) {
        size_t rem = flat;
        for (size_t d = 0; d < 5; ++d) {
            out_idx[d] = static_cast<uint32_t>(rem / out_strides[d]);
            rem        = rem % out_strides[d];
        }
        // Source coordinate = the trailing slots of out_idx, padded with 0.
        RtaIndex s_idx{0, 0, 0, 0, 0};
        for (uint32_t d = 0; d < src_rank; ++d) {
            s_idx[d] = out_idx[num_new_dims + d];
        }
        size_t s_off = 0;
        for (size_t d = 0; d < 5; ++d) {
            s_off += static_cast<size_t>(s_idx[d]) * src_strides[d];
        }
        out.data[flat] = src.data[s_off];
    }

    return out;
}

// ============================================================================
// Conversion helpers
// ============================================================================

DenseTensor5D sparse_to_dense(const SparseTensor5D& s,
                              const std::array<uint32_t, 5>& shape)
{
    DenseTensor5D out;
    out.shape = shape;
    out.data.assign(shape_product(shape), 0.0f);

    for (const auto& entry : s) {
        const RtaIndex& idx = entry.first;
        // Verify the coordinate is within the requested shape.
        for (size_t d = 0; d < 5; ++d) {
            if (idx[d] >= shape[d]) {
                throw ValidationError(
                    "sparse_to_dense: index axis " + std::to_string(d) +
                    " value " + std::to_string(idx[d]) +
                    " exceeds shape size " + std::to_string(shape[d]));
            }
        }
        out.set(idx, entry.second);
    }
    return out;
}

SparseTensor5D dense_to_sparse(const DenseTensor5D& d, float threshold)
{
    if (d.data.size() != d.numel()) {
        throw ValidationError("dense_to_sparse: data size does not match shape");
    }
    SparseTensor5D out;
    const auto strides = compute_strides(d.shape);

    RtaIndex idx{0, 0, 0, 0, 0};
    const size_t total = d.data.size();
    for (size_t flat = 0; flat < total; ++flat) {
        const float v = d.data[flat];
        if (std::fabs(v) <= threshold) continue;
        size_t rem = flat;
        for (size_t k = 0; k < 5; ++k) {
            idx[k] = static_cast<uint32_t>(rem / strides[k]);
            rem    = rem % strides[k];
        }
        out.emplace(idx, v);
    }
    return out;
}

} // namespace lqt
