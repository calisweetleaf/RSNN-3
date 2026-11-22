// bindings/lqt_native_rta_decomp.cpp — RecursiveTensor decompositions
// (eigenstates, Tucker, MPS/tensor-train). Own TU: these instantiate the
// header-only eigensolvers and are the heaviest part of the rta bindings
// (single rta TU was OOM-killed, exit 137, on the shared 7 GB sandbox).
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cstring>
#include <optional>
#include <vector>

#include <rta/rta.hpp>

namespace py = pybind11;
using RT = rta::RecursiveTensor<double>;
using F64Array = py::array_t<double, py::array::c_style | py::array::forcecast>;

namespace {
F64Array matrix_to_numpy(const rta::Matrix<double>& m) {
    F64Array out({static_cast<py::ssize_t>(m.rows), static_cast<py::ssize_t>(m.cols)});
    if (!m.a.empty()) std::memcpy(out.mutable_data(), m.a.data(), m.a.size() * sizeof(double));
    return out;
}
}  // namespace

void bind_recursive_tensor_decomp(py::class_<RT>& cls) {
    cls
        .def("compute_eigenstates", [](const RT& t, size_t k, double thr) {
                auto r = t.compute_eigenstates(k, thr);
                return py::make_tuple(r.values, r.vectors ? py::cast(*r.vectors) : py::none(), r.converged);
            }, py::arg("k") = 6, py::arg("threshold") = 1e-8, "Returns (eigenvalues, vectors_tensor, converged).")
        .def("tucker_decomposition", [](const RT& t, std::optional<std::vector<size_t>> ranks) {
                auto r = t.tucker_decomposition(ranks);
                py::list factors; for (const auto& f : r.factors) factors.append(matrix_to_numpy(f));
                return py::make_tuple(*r.core, factors);
            }, py::arg("ranks") = py::none(), "Returns (core_tensor, [factor matrices]).")
        .def("to_mps", &RT::to_mps, py::arg("max_bond") = py::none(), py::arg("rel_cutoff") = 0.0)
        .def_static("from_mps", &RT::from_mps, py::arg("cores"));
}
