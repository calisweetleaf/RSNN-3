// bindings/lqt_native_rta.cpp — COMPUTE half of lqt_native: the header-only
// rta::RecursiveTensor<double> (lqt/recursive-tensor-cpp, C++ port of
// recursive_tensor.py v2.1.0) with numpy interop and .rta (RTNZ v2) I/O.
// Split from lqt_native.cpp only to bound per-TU compiler memory on the 7 GB
// shared sandbox (the single-TU build was OOM-killed, exit 137, 2026-11-21).
#include <pybind11/functional.h>
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

void bind_recursive_tensor_decomp(py::class_<RT>& cls);  // lqt_native_rta_decomp.cpp

namespace {
// ---------------------------------------------------------------- RecursiveTensor <-> numpy
F64Array rt_to_numpy(const RT& t) {
    std::vector<py::ssize_t> shape(t.shape().begin(), t.shape().end());
    F64Array out(shape);
    const std::vector<double> dense = t.to_dense_array();
    if (!dense.empty()) std::memcpy(out.mutable_data(), dense.data(), dense.size() * sizeof(double));
    return out;
}

RT rt_from_numpy(const F64Array& a) {
    rta::Shape shape;
    for (py::ssize_t i = 0; i < a.ndim(); ++i) shape.push_back(static_cast<rta::Extent>(a.shape(i)));
    return RT::from_dense(shape, std::vector<double>(a.data(), a.data() + a.size()));
}

rta::Matrix<double> matrix_from_numpy(const F64Array& a) {
    if (a.ndim() != 2) throw py::value_error("matrix must be 2-D");
    rta::Matrix<double> m(static_cast<size_t>(a.shape(0)), static_cast<size_t>(a.shape(1)));
    std::memcpy(m.a.data(), a.data(), static_cast<size_t>(a.size()) * sizeof(double));
    return m;
}


}  // namespace

void bind_recursive_tensor(py::module_& m) {
    py::register_exception<rta::Error>(m, "RtaError", PyExc_RuntimeError);
    // ------------------------------------------------------------ rta::RecursiveTensor<double>
    py::enum_<rta::Distribution>(m, "Distribution")
        .value("Normal", rta::Distribution::Normal).value("Uniform", rta::Distribution::Uniform)
        .value("PowerLaw", rta::Distribution::PowerLaw).value("ComplexGaussian", rta::Distribution::ComplexGaussian)
        .value("Orthogonal", rta::Distribution::Orthogonal).value("Empty", rta::Distribution::Empty)
        .value("Explicit", rta::Distribution::Explicit);
    py::enum_<rta::NormType>(m, "NormType")
        .value("L1", rta::NormType::L1).value("L2", rta::NormType::L2).value("Inf", rta::NormType::Inf);
    py::enum_<rta::ReduceOp>(m, "ReduceOp")
        .value("Sum", rta::ReduceOp::Sum).value("Mean", rta::ReduceOp::Mean)
        .value("Max", rta::ReduceOp::Max).value("Min", rta::ReduceOp::Min);

    py::class_<RT> cls(m, "RecursiveTensor",
        "Compute tensor (rta::RecursiveTensor<double>, C++ port of recursive_tensor.py v2.1.0, .rta RTNZ v2 I/O).");
    cls
        .def(py::init([](std::vector<rta::Extent> shape, rta::Distribution dist, double sparsity, std::optional<uint64_t> seed) {
                 return RT(rta::Shape(shape.begin(), shape.end()), dist, sparsity, seed);
             }), py::arg("shape"), py::arg("distribution") = rta::Distribution::Normal,
             py::arg("sparsity") = 0.1, py::arg("seed") = py::none())
        .def_static("zeros", [](std::vector<rta::Extent> s) { return RT::zeros(rta::Shape(s.begin(), s.end())); }, py::arg("shape"))
        .def_static("from_numpy", &rt_from_numpy, py::arg("array"))
        .def("to_numpy", &rt_to_numpy)
        .def("__array__", [](const RT& t, py::args, py::kwargs) { return rt_to_numpy(t); })
        .def_property_readonly("shape", [](const RT& t) { return std::vector<rta::Extent>(t.shape().begin(), t.shape().end()); })
        .def_property_readonly("rank", &RT::rank)
        .def_property_readonly("volume", &RT::volume)
        .def_property_readonly("is_sparse", &RT::is_sparse)
        .def_property_readonly("distribution", &RT::distribution)
        .def("nnz", &RT::nnz)
        .def("measured_sparsity", &RT::measured_sparsity)
        .def("get", [](const RT& t, std::vector<rta::Extent> i) { return t.get(rta::Index(i.begin(), i.end())); }, py::arg("index"))
        .def("set", [](RT& t, std::vector<rta::Extent> i, double v) { t.set(rta::Index(i.begin(), i.end()), v); }, py::arg("index"), py::arg("value"))
        .def("to_dense", &RT::to_dense)
        .def("to_sparse", &RT::to_sparse, py::arg("threshold") = 0.0)
        .def("contract", [](const RT& a, const RT& b, rta::Axes ax, rta::Axes bx) {
                py::gil_scoped_release nogil; return a.contract(b, ax, bx);
            }, py::arg("other"), py::arg("axes_self") = rta::Axes{0}, py::arg("axes_other") = rta::Axes{0},
            "Generalized tensordot (Python contract(other, axes=((..),(..))).")
        .def("transpose", &RT::transpose, py::arg("perm"))
        .def("swap_axes", &RT::swap_axes, py::arg("a"), py::arg("b"))
        .def("reshape", [](const RT& t, std::vector<rta::Extent> s) { return t.reshape(rta::Shape(s.begin(), s.end())); }, py::arg("shape"))
        .def("expand", [](const RT& t, std::vector<rta::Extent> s) { return t.expand(rta::Shape(s.begin(), s.end())); }, py::arg("new_dims"))
        .def("project", [](const RT& t, const F64Array& basis, rta::Axes axes) { return t.project(matrix_from_numpy(basis), axes); },
             py::arg("basis"), py::arg("axes") = rta::Axes{0})
        .def("transform", [](const RT& t, const F64Array& M, std::optional<rta::Axes> axes) { return t.transform(matrix_from_numpy(M), axes); },
             py::arg("matrix"), py::arg("axes") = py::none())
        .def("reduce", [](const RT& t, rta::ReduceOp op, size_t axis) {
                auto r = t.reduce(op, axis);
                return py::make_tuple(*r.values, r.arg);
            }, py::arg("op"), py::arg("axis"), "Returns (values_tensor, argmax/argmin list).")
        .def("norm", &RT::norm, py::arg("type") = rta::NormType::L2)
        .def("normalize", &RT::normalize, py::arg("type") = rta::NormType::L2)
        .def("compute_entropy", &RT::compute_entropy)
        .def("compatibility", &RT::compatibility, py::arg("other"))
        .def("apply_temporal_convolution", &RT::apply_temporal_convolution, py::arg("kernel"), py::arg("time_axis") = py::none());
    cls
        .def("__add__", [](const RT& a, const RT& b) { return a + b; })
        .def("__add__", [](const RT& a, double s) { return a + s; })
        .def("__sub__", [](const RT& a, const RT& b) { return a - b; })
        .def("__mul__", [](const RT& a, const RT& b) { return a * b; })
        .def("__mul__", [](const RT& a, double s) { return a * s; })
        .def("save", [](const RT& t, const std::string& p) { rta::io::save(t, p); }, py::arg("path"), "Write .rta (RTNZ v2).")
        .def_static("load", [](const std::string& p) { return rta::io::load<double>(p, true); }, py::arg("path"))
        .def("describe", &RT::describe)
        .def("__repr__", &RT::describe);
    bind_recursive_tensor_decomp(cls);  // lqt_native_rta_decomp.cpp
}
