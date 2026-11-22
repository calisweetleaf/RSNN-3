// lqt/rta_ops.h — Higher-level RTA tensor operations.
// Ported from recursive_tensor.py: contract(), project(), expand().
// Council: Odin (Patch 4).
//
// This header introduces light-weight dense and sparse 5D tensor containers and
// three core operations used by the RTA layer:
//
//   * rta_contract        — tensor product summed over a pair of axis lists
//                            (dense × dense → dense)
//   * rta_contract_sparse — same operation for hash-map sparse tensors
//   * rta_project         — projection onto an L2-normalised basis along
//                            one or more axes
//   * rta_expand          — prepend new size-broadcasted leading dimensions
//
// Conversion helpers are provided to move between dense and sparse forms.
//
// Design notes
// ------------
// DD-A  RtaIndex is a fixed 5-tuple of uint32_t.  The recursive tensor model
//       (rta.h) pins rank at exactly 5, so we mirror that here rather than
//       paying for std::vector storage per coordinate.
// DD-B  Sparse output keeps entries whose magnitude exceeds 1e-8 (matching
//       the Python reference's tolerance in _sparse_project_single_axis).
// DD-C  Dense storage is row-major: idx[0] is the slowest-varying axis,
//       idx[4] is the fastest-varying axis.
// DD-D  Contract operates on arbitrary subsets of axes provided that
//       len(axes_a) == len(axes_b) and corresponding dimensions match.
//       The result rank is (5 - len(axes_a)) + (5 - len(axes_b)), but for
//       compatibility with the rest of the RTA stack we pad the result back
//       up to a 5D dense container (unused trailing axes are size 1).
// DD-E  Project preserves rank.  For each axis in `axes`, the size of that
//       axis becomes basis.size() (number of basis rows).
// DD-F  Expand prepends `num_new_dims` axes each of size `new_size`,
//       broadcasting by 1.0 (outer product with an all-ones tensor).
//       Since output rank must remain 5, the caller must ensure that
//       num_new_dims + (number of populated input dims) <= 5.

#pragma once

#include <array>
#include <cstdint>
#include <cstddef>
#include <functional>
#include <unordered_map>
#include <vector>

#include "lqt/error.h"
#include "lqt/rta.h"

namespace lqt {

// ── Sparse index type: 5 uint32_t coordinates ──────────────────────────────
using RtaIndex = std::array<uint32_t, 5>;

struct RtaIndexHash {
    size_t operator()(const RtaIndex& k) const noexcept {
        size_t seed = 0;
        for (auto v : k) {
            seed ^= std::hash<uint32_t>{}(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

// Sparse storage: map from 5D index → value (only non-zero entries stored).
using SparseTensor5D = std::unordered_map<RtaIndex, float, RtaIndexHash>;

// Dense 5D tensor stored row-major in a flat vector.
// Shape is always 5 dimensions; size-1 axes are used to model lower-rank
// tensors without changing the container type.
struct DenseTensor5D {
    std::array<uint32_t, 5> shape = {1, 1, 1, 1, 1};
    std::vector<float>      data;   // shape[0]*shape[1]*shape[2]*shape[3]*shape[4]

    // Compute the row-major flat offset for a coordinate.
    // Throws ValidationError if any axis is out of range.
    size_t flat_index(const RtaIndex& idx) const;

    // Bounds-checked element accessor.  Returns 0.0f if the cell is out of
    // range only in defensive callers — the default behaviour is to throw.
    float  at(const RtaIndex& idx) const;

    // Bounds-checked mutator.  Throws on out-of-range.
    void   set(const RtaIndex& idx, float v);

    // Total element count = product of shape.
    size_t numel() const noexcept;
};

// ── Contract (tensor product summed over specified axes) ───────────────────
// Port of RecursiveTensor.contract(other, axes).
//   axes_a / axes_b: equal-length lists of axis indices to contract; for each
//                    pair (axes_a[i], axes_b[i]) the corresponding dimensions
//                    of a and b must match.
// The contracted axes are summed out; remaining axes of `a` come first in
// the result, followed by remaining axes of `b` (matching numpy.tensordot).
// The result is returned as a 5D dense container with unused trailing axes
// padded to size 1; the meaningful rank is (5 - axes_a.size()) +
// (5 - axes_b.size()), which must be <= 5.
DenseTensor5D rta_contract(const DenseTensor5D& a,
                           const DenseTensor5D& b,
                           const std::vector<uint32_t>& axes_a,
                           const std::vector<uint32_t>& axes_b);

// Sparse variant: contracts two SparseTensor5D objects along axes.
// Only output entries with |value| > 1e-8 are kept (matching the Python
// reference in _sparse_project_single_axis).
SparseTensor5D rta_contract_sparse(const SparseTensor5D& a,
                                   const SparseTensor5D& b,
                                   const std::vector<uint32_t>& axes_a,
                                   const std::vector<uint32_t>& axes_b);

// ── Project (projection onto subspace basis) ───────────────────────────────
// Port of RecursiveTensor.project(subspace_basis, axes).
//   basis: rows = basis vectors, cols = original axis size.  Each row is L2
//          normalised internally (matching the numpy reference).
//   axes:  list of axes along which to project.  All listed axes must share
//          the same source size == basis[i].size().
// Returns a new tensor with the same rank; each projected axis is resized to
// basis.size().
DenseTensor5D rta_project(const DenseTensor5D& src,
                          const std::vector<std::vector<float>>& basis,
                          const std::vector<uint32_t>& axes);

// ── Expand (prepend broadcast dimensions) ──────────────────────────────────
// Port of RecursiveTensor.expand(new_dimensions).
// Prepends `num_new_dims` axes each of size `new_size`, broadcasting the
// original data along the new axes (every prepended slice is a copy of the
// original tensor).  The original tensor's used rank + num_new_dims must
// not exceed 5.
DenseTensor5D rta_expand(const DenseTensor5D& src,
                         uint32_t new_size,
                         uint32_t num_new_dims);

// ── Conversion helpers ─────────────────────────────────────────────────────
// Densify a sparse map into a tensor of the given shape.  Coordinates that
// exceed the supplied shape are rejected with ValidationError.
DenseTensor5D  sparse_to_dense(const SparseTensor5D& s,
                               const std::array<uint32_t, 5>& shape);

// Convert a dense tensor into a sparse map, dropping entries with magnitude
// at or below `threshold`.
SparseTensor5D dense_to_sparse(const DenseTensor5D& d,
                               float threshold = 1e-8f);

} // namespace lqt
