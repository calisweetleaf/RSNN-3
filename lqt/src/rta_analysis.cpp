// lqt/src/rta_analysis.cpp — RTA analysis operations.
//
// Council module: Thor (Patch 4).
// Ported from recursive_tensor.py (lines 748–1140) and recursive_tensor_whitepaper.md
//   §2.3 Sparsity Properties and §2.4 Recursive Properties (Theorem 2 / Banach
//   fixed-point).
//
// All math operates on flat std::vector<float> buffers (no torch, no numpy).
// Functions are pure: they consume inputs and return new vectors.
#include "lqt/rta_analysis.h"

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <limits>
#include <numeric>
#include <stdexcept>

namespace lqt {

namespace {

// Numerical epsilon for log-domain stability (matches Python's 1e-10).
constexpr float kLogEpsilon = 1e-10f;

// Threshold below which a computed norm is treated as zero.
constexpr float kNormZero = 1e-8f;

} // namespace

// ────────────────────────────────────────────────────────────────────────────
// rta_fractal_iterate — element-wise z = z² + c(idx, z) Mandelbrot-style loop
// ────────────────────────────────────────────────────────────────────────────
// For each element, we capture the c-constant once from c_func(idx, initial z)
// (matching the Python branch that calls c_function(None, z) before the loop),
// then iterate z = z*z + c until |z| > escape_radius. Elements that have
// already escaped stop early; surviving elements run the full max_iter.
std::vector<float> rta_fractal_iterate(
    const std::vector<float>& data,
    std::function<float(size_t, float)> c_func,
    uint32_t max_iter,
    float escape_radius) {
    if (!c_func) {
        throw std::invalid_argument("rta_fractal_iterate: c_func must be callable");
    }

    const size_t n = data.size();
    std::vector<float> z = data;
    if (n == 0) {
        return z;
    }

    // Capture per-element c with the initial z value (mirrors Python semantics).
    std::vector<float> c(n);
    for (size_t i = 0; i < n; ++i) {
        c[i] = c_func(i, z[i]);
    }

    // Track which elements are still iterating; once |z| > radius they freeze.
    std::vector<uint8_t> active(n, 1u);

    for (uint32_t iter = 0; iter < max_iter; ++iter) {
        bool any_active = false;
        for (size_t i = 0; i < n; ++i) {
            if (!active[i]) {
                continue;
            }
            const float zi = z[i];
            const float next = zi * zi + c[i];
            z[i] = next;
            if (std::fabs(next) > escape_radius) {
                active[i] = 0u;
            } else {
                any_active = true;
            }
        }
        if (!any_active) {
            break;
        }
    }

    return z;
}

// ────────────────────────────────────────────────────────────────────────────
// rta_entropy — Shannon entropy from |value| as unnormalised probability mass
// ────────────────────────────────────────────────────────────────────────────
// Mirrors RecursiveTensor.compute_entropy(): sum of |v| forms the partition
// function; per-element probability p_i = |v_i| / sum; entropy -Σ p log(p+ε).
// Zero values contribute nothing and are skipped, matching the Python branch
// where values <= 0 are filtered before the probability computation.
float rta_entropy(const std::vector<float>& values) {
    if (values.empty()) {
        return 0.0f;
    }

    double total = 0.0;
    for (const float v : values) {
        const double a = static_cast<double>(std::fabs(v));
        total += a;
    }
    if (total <= 0.0) {
        return 0.0f;
    }

    double entropy = 0.0;
    for (const float v : values) {
        const double a = static_cast<double>(std::fabs(v));
        if (a <= 0.0) {
            continue;
        }
        const double p = a / total;
        entropy -= p * std::log(p + static_cast<double>(kLogEpsilon));
    }

    return static_cast<float>(entropy);
}

// ────────────────────────────────────────────────────────────────────────────
// rta_normalize — divide every element by the chosen vector norm
// ────────────────────────────────────────────────────────────────────────────
// L1   : Σ|v|
// L2   : sqrt(Σ v²)
// Inf  : max|v|
// Fro  : sqrt(Σ v²) (Frobenius == L2 over a flat buffer; matches numpy)
//
// Mirrors RecursiveTensor.normalize: a near-zero norm returns the input
// unchanged (copy) rather than dividing by zero.
std::vector<float> rta_normalize(const std::vector<float>& data, NormType norm) {
    std::vector<float> out = data;
    if (out.empty()) {
        return out;
    }

    double norm_val = 0.0;
    switch (norm) {
        case NormType::L1: {
            double s = 0.0;
            for (const float v : out) s += std::fabs(static_cast<double>(v));
            norm_val = s;
            break;
        }
        case NormType::L2:
        case NormType::Frobenius: {
            double s = 0.0;
            for (const float v : out) {
                const double d = static_cast<double>(v);
                s += d * d;
            }
            norm_val = std::sqrt(s);
            break;
        }
        case NormType::Inf: {
            double m = 0.0;
            for (const float v : out) {
                const double a = std::fabs(static_cast<double>(v));
                if (a > m) m = a;
            }
            norm_val = m;
            break;
        }
    }

    if (norm_val < static_cast<double>(kNormZero)) {
        return out;
    }

    const float inv = static_cast<float>(1.0 / norm_val);
    for (float& v : out) {
        v *= inv;
    }
    return out;
}

// ────────────────────────────────────────────────────────────────────────────
// rta_apply_function — element-wise functor with optional |value| threshold
// ────────────────────────────────────────────────────────────────────────────
// Mirrors RecursiveTensor.apply_function: when a non-negative threshold is
// provided, any output with |result| <= threshold is set to exactly 0.0f.
// A negative threshold disables the cut (Python's None).
std::vector<float> rta_apply_function(
    const std::vector<float>& data,
    std::function<float(float)> func,
    float threshold) {
    if (!func) {
        throw std::invalid_argument("rta_apply_function: func must be callable");
    }

    std::vector<float> out(data.size());
    const bool use_threshold = (threshold >= 0.0f);
    for (size_t i = 0; i < data.size(); ++i) {
        const float r = func(data[i]);
        if (use_threshold && std::fabs(r) <= threshold) {
            out[i] = 0.0f;
        } else {
            out[i] = r;
        }
    }
    return out;
}

// ────────────────────────────────────────────────────────────────────────────
// rta_density — histogram with density normalisation (matches numpy's
// np.histogram(..., density=True))
// ────────────────────────────────────────────────────────────────────────────
// Steps:
//   1. Filter values by |v| > threshold.
//   2. Compute [min, max] of the surviving |v| sample.
//   3. Build resolution+1 equally-spaced bin edges across [min, max].
//   4. Count elements per bin (last bin is inclusive of max, matching numpy).
//   5. Divide each count by (total * bin_width) so Σ counts * bin_width == 1.
//
// Edge cases:
//   * Resolution must be > 0.
//   * If no values survive the filter, returns empty bin_edges and counts.
//   * If min == max (degenerate range), we widen by 0.5 on each side so the
//     histogram still has positive bin width (numpy does the same).
DensityResult rta_density(
    const std::vector<float>& values,
    uint32_t resolution,
    float threshold) {
    if (resolution == 0) {
        throw std::invalid_argument("rta_density: resolution must be > 0");
    }

    DensityResult result;
    const size_t n_in = values.size();

    // Filter |v| > threshold (matches Python's np.abs(values) > threshold).
    std::vector<float> filtered;
    filtered.reserve(n_in);
    for (const float v : values) {
        if (std::fabs(v) > threshold) {
            filtered.push_back(std::fabs(v));
        }
    }

    if (filtered.empty()) {
        return result; // both vectors empty
    }

    float lo = filtered.front();
    float hi = filtered.front();
    for (const float v : filtered) {
        if (v < lo) lo = v;
        if (v > hi) hi = v;
    }

    if (hi <= lo) {
        // Degenerate range: widen by 0.5 each side (matches np.histogram).
        lo -= 0.5f;
        hi += 0.5f;
    }

    const double width = (static_cast<double>(hi) - static_cast<double>(lo)) /
                         static_cast<double>(resolution);

    result.bin_edges.resize(static_cast<size_t>(resolution) + 1u);
    for (uint32_t i = 0; i <= resolution; ++i) {
        result.bin_edges[i] = static_cast<float>(static_cast<double>(lo) +
                                                 static_cast<double>(i) * width);
    }
    // Force exact endpoints to avoid floating drift.
    result.bin_edges.front() = lo;
    result.bin_edges.back()  = hi;

    result.counts.assign(resolution, 0.0f);

    // Bin assignment: indices 0..resolution-1; last bin is inclusive of hi.
    for (const float v : filtered) {
        double rel = (static_cast<double>(v) - static_cast<double>(lo)) / width;
        long bin = static_cast<long>(std::floor(rel));
        if (bin < 0) bin = 0;
        if (bin >= static_cast<long>(resolution)) bin = static_cast<long>(resolution) - 1;
        result.counts[static_cast<size_t>(bin)] += 1.0f;
    }

    // Density normalisation: divide each count by (total * bin_width).
    const double total = static_cast<double>(filtered.size());
    if (total > 0.0 && width > 0.0) {
        const float scale = static_cast<float>(1.0 / (total * width));
        for (float& c : result.counts) {
            c *= scale;
        }
    }

    return result;
}

// ────────────────────────────────────────────────────────────────────────────
// rta_find_fixed_point — Banach iteration for contractive f
// ────────────────────────────────────────────────────────────────────────────
// Whitepaper §2.4 / Theorem 2 / Appendix A.2: if f : R^n → R^n is a
// contraction on a complete metric space, the sequence v_{k+1} = f(v_k)
// converges to a unique fixed point v* satisfying f(v*) = v*. We iterate
// until ||v_{k+1} - v_k||_2 < tol or max_iter is exhausted.
//
// Returns the latest iterate regardless of convergence so callers can
// inspect divergent or near-converged states.
FixedPointResult rta_find_fixed_point(
    const std::vector<float>& initial,
    std::function<std::vector<float>(const std::vector<float>&)> f,
    float tol,
    uint32_t max_iter) {
    if (!f) {
        throw std::invalid_argument("rta_find_fixed_point: f must be callable");
    }

    FixedPointResult result;
    result.converged = false;
    result.value = initial;
    result.iters = 0;

    if (max_iter == 0) {
        return result;
    }

    for (uint32_t k = 0; k < max_iter; ++k) {
        std::vector<float> next = f(result.value);
        if (next.size() != result.value.size()) {
            throw std::invalid_argument(
                "rta_find_fixed_point: f changed vector dimension");
        }

        double sq = 0.0;
        for (size_t i = 0; i < next.size(); ++i) {
            const double d = static_cast<double>(next[i]) -
                             static_cast<double>(result.value[i]);
            sq += d * d;
        }
        const double dist = std::sqrt(sq);

        result.value = std::move(next);
        result.iters = k + 1;

        if (dist < static_cast<double>(tol)) {
            result.converged = true;
            break;
        }
    }

    return result;
}

} // namespace lqt
