// bindings/lqt_native.cpp — pybind11 module exposing the C++ LQT reference
// implementation (lqt/, static liblqt) and the header-only RecursiveTensor
// library (lqt/recursive-tensor-cpp/include/rta) to Python.
//
// Doctrine (lqt/docs/TRIAXIAL_ARCHITECTURE.md §3):
//   * WEIGHTS ARE STORAGE: LqtModel, Codebook, RecursiveWeight (B, Phi, R, T,
//     epsilon buckets), DeltaBuffer, RtaBlock (dims + sparsity) and the
//     hash-chained EditLog live in the .lqt container.
//   * TENSORS ARE COMPUTE: rta::RecursiveTensor<double> (exposed as
//     RecursiveTensor) and the lqt rta_ops DenseTensor5D kernels perform
//     contraction/projection/transform on values selected from storage.
// The two surfaces are bound side by side; nothing here converts one into the
// other implicitly. Moving values across the boundary is an explicit numpy
// hand-off (LqtModel.reconstruct -> RecursiveTensor.from_numpy).
//
// Replaces (Python originals kept as evidence in lqt/original-py-code/):
//   recursive_weights_core.py -> RecursiveWeight, PatternLibrary,
//       EvolutionEngine, validate_weight, dynamics.*
//   recursive_tensor.py       -> RecursiveTensor (rta header-only port v2.1.0)
//   lqt_library.py            -> LqtModel (+ Codebook, TensorDescriptor,
//       DeltaBuffer, RtaBlock, EditLog)
//   ethical_tensor.py / metacognitive_tensor.py: no C++ port exists in this
//       repository; nothing is bound for them (no stand-ins).
//
// Not bound: lqt::MutationValidator (mutation.h). mutation.h and
// rw_validation.h both define lqt::ValidationResult with different layouts,
// so one TU cannot include both; the RecursiveWeight validator is bound.

#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cstring>
#include <string>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/delta.h"
#include "lqt/descriptor.h"
#include "lqt/edit_log.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/model.h"
#include "lqt/reconstruct.h"
#include "lqt/recursive_weight.h"
#include "lqt/rta.h"
#include "lqt/rta_ops.h"
#include "lqt/rw_compute.h"
#include "lqt/rw_dynamics.h"
#include "lqt/rw_evolution.h"
#include "lqt/rw_validation.h"
#include "lqt/version.h"


namespace py = pybind11;
void bind_recursive_tensor(py::module_& m);  // lqt_native_rta.cpp
using namespace lqt;

using F32Array = py::array_t<float, py::array::c_style | py::array::forcecast>;
using F64Array = py::array_t<double, py::array::c_style | py::array::forcecast>;
using U32Array = py::array_t<uint32_t, py::array::c_style | py::array::forcecast>;

namespace {

std::vector<float> to_fvec(const F32Array& a) {
    return std::vector<float>(a.data(), a.data() + a.size());
}

F32Array from_fvec(const std::vector<float>& v) {
    F32Array out(static_cast<py::ssize_t>(v.size()));
    if (!v.empty()) std::memcpy(out.mutable_data(), v.data(), v.size() * sizeof(float));
    return out;
}

py::bytes to_pybytes(const std::vector<uint8_t>& v) {
    return py::bytes(reinterpret_cast<const char*>(v.data()), v.size());
}

std::vector<uint8_t> from_pybytes(const py::bytes& b) {
    std::string s = b;
    return std::vector<uint8_t>(s.begin(), s.end());
}

// ---------------------------------------------------------------- RecursiveWeight
RecursiveWeight make_weight(uint32_t base_index, const F32Array& phase, const F32Array& reference,
                            const F32Array& tensor_position, const F32Array& error,
                            float self_reference_coeff) {
    RecursiveWeight w;
    w.base_index = base_index;
    w.phase = to_fvec(phase);
    if (reference.size() > 0) {
        if (reference.ndim() != 3 || reference.shape(1) != reference.shape(2)) {
            throw py::value_error("reference must have shape (k, d, d)");
        }
        w.r_k = static_cast<uint32_t>(reference.shape(0));
        w.r_d = static_cast<uint32_t>(reference.shape(1));
        w.reference = to_fvec(reference);
    }
    if (tensor_position.size() != static_cast<py::ssize_t>(LQT_RTA_RANK)) {
        throw py::value_error("tensor_position must have exactly 5 elements (RTA dims d0..d4)");
    }
    for (size_t i = 0; i < LQT_RTA_RANK; ++i) w.tensor_position[i] = tensor_position.data()[i];
    w.error = to_fvec(error);
    w.self_reference_coeff = self_reference_coeff;
    w.validate();
    return w;
}

F32Array weight_reference(const RecursiveWeight& w) {
    F32Array out({static_cast<py::ssize_t>(w.r_k), static_cast<py::ssize_t>(w.r_d),
                  static_cast<py::ssize_t>(w.r_d)});
    if (!w.reference.empty())
        std::memcpy(out.mutable_data(), w.reference.data(), w.reference.size() * sizeof(float));
    return out;
}

py::bytes weight_to_bytes(const RecursiveWeight& w) {
    ByteWriter bw;
    w.serialize(bw);
    return to_pybytes(bw.bytes());
}

RecursiveWeight weight_from_bytes(const py::bytes& b) {
    std::vector<uint8_t> buf = from_pybytes(b);
    ByteReader br(buf.data(), buf.size());
    return RecursiveWeight::parse(br);
}

// ---------------------------------------------------------------- Codebook
F32Array codebook_values(const Codebook& cb) {
    F32Array out({static_cast<py::ssize_t>(cb.num_vectors()), static_cast<py::ssize_t>(cb.vector_dim())});
    if (!cb.data().empty())
        std::memcpy(out.mutable_data(), cb.data().data(), cb.data().size() * sizeof(float));
    return out;
}

Codebook codebook_from_numpy(uint16_t id, const F32Array& values) {
    if (values.ndim() != 1 && values.ndim() != 2) throw py::value_error("values must be 1-D (scalar) or 2-D (n, dim)");
    const auto n = values.shape(0);
    const auto dim = values.ndim() == 2 ? values.shape(1) : 1;
    if (n <= 0 || n > 0xFFFF || dim <= 0 || dim > 0xFFFF) throw py::value_error("codebook size out of u16 range");
    Codebook cb(id, static_cast<uint16_t>(n), static_cast<uint16_t>(dim));
    std::memcpy(cb.data().data(), values.data(), static_cast<size_t>(n * dim) * sizeof(float));
    return cb;
}

// ---------------------------------------------------------------- EditLog
py::dict edit_entry_dict(const EditLogEntry& e) {
    py::dict d;
    d["timestamp_ns"] = e.timestamp_ns;
    d["type"] = e.type;
    d["target"] = e.target;
    d["data_hash"] = e.data_hash;
    d["signature"] = to_pybytes(e.signature);
    return d;
}

// ---------------------------------------------------------------- DenseTensor5D <-> numpy
DenseTensor5D dense5_from_numpy(const F32Array& a) {
    if (a.ndim() != 5) throw py::value_error("DenseTensor5D requires a 5-D array");
    DenseTensor5D t;
    for (int i = 0; i < 5; ++i) t.shape[static_cast<size_t>(i)] = static_cast<uint32_t>(a.shape(i));
    t.data = to_fvec(a);
    return t;
}

F32Array dense5_to_numpy(const DenseTensor5D& t) {
    F32Array out({static_cast<py::ssize_t>(t.shape[0]), static_cast<py::ssize_t>(t.shape[1]),
                  static_cast<py::ssize_t>(t.shape[2]), static_cast<py::ssize_t>(t.shape[3]),
                  static_cast<py::ssize_t>(t.shape[4])});
    if (!t.data.empty()) std::memcpy(out.mutable_data(), t.data.data(), t.data.size() * sizeof(float));
    return out;
}

}  // namespace

PYBIND11_MODULE(lqt_native, m) {
    m.doc() = "LQT reference implementation (C++17) + RecursiveTensor (rta) bound for Python. "
              "Weights are storage (LqtModel/RecursiveWeight); tensors are compute (RecursiveTensor).";
    m.attr("FORMAT_VERSION") = LQT_FORMAT_VERSION;
    m.attr("RTA_RANK") = LQT_RTA_RANK;
    m.attr("ID_NONE") = LQT_ID_NONE;

    // ------------------------------------------------------------ exceptions
    auto exc_base = py::register_exception<LqtError>(m, "LqtError", PyExc_RuntimeError);
    py::register_exception<FormatError>(m, "FormatError", exc_base.ptr());
    py::register_exception<ValidationError>(m, "ValidationError", exc_base.ptr());

    // ------------------------------------------------------------ enums
    py::enum_<DType>(m, "DType")
        .value("FP32", DType::FP32).value("FP16", DType::FP16).value("BF16", DType::BF16)
        .value("INT8", DType::INT8).value("INT4", DType::INT4).value("UINT8", DType::UINT8)
        .value("INT16", DType::INT16).value("INT32", DType::INT32);
    py::enum_<TensorType>(m, "TensorType")
        .value("Standard", TensorType::Standard).value("RecursiveTensor", TensorType::RecursiveTensor);
    py::enum_<TensorFlag>(m, "TensorFlag")
        .value("Trainable", TensorFlag::Trainable).value("Protected", TensorFlag::Protected)
        .value("Shared", TensorFlag::Shared).value("HotSwappable", TensorFlag::HotSwappable)
        .value("Cached", TensorFlag::Cached).value("Checkpoint", TensorFlag::Checkpoint);
    py::enum_<SparseEncoding>(m, "SparseEncoding")
        .value("Uniform", SparseEncoding::Uniform).value("PerDimension", SparseEncoding::PerDimension)
        .value("Hierarchical", SparseEncoding::Hierarchical).value("RLE", SparseEncoding::RLE)
        .value("CompressedBitmap", SparseEncoding::CompressedBitmap).value("CsrCscCsf", SparseEncoding::CsrCscCsf);
    py::enum_<RtaDistribution>(m, "RtaDistribution")
        .value("Normal", RtaDistribution::Normal).value("Uniform", RtaDistribution::Uniform)
        .value("Exponential", RtaDistribution::Exponential).value("Custom", RtaDistribution::Custom);
    py::enum_<MutationType>(m, "MutationType")
        .value("CodebookEdit", MutationType::CodebookEdit).value("DeltaUpdate", MutationType::DeltaUpdate)
        .value("ModuleSwap", MutationType::ModuleSwap).value("SparseMaskUpdate", MutationType::SparseMaskUpdate)
        .value("Hyperparameter", MutationType::Hyperparameter).value("CodebookExpand", MutationType::CodebookExpand)
        .value("RecursiveWeightEdit", MutationType::RecursiveWeightEdit).value("TensorAttach", MutationType::TensorAttach)
        .value("TensorDetach", MutationType::TensorDetach);

    // ============================================================ STORAGE
    // ------------------------------------------------------------ Codebook
    py::class_<Codebook>(m, "Codebook")
        .def(py::init<uint16_t, uint16_t, uint16_t>(), py::arg("id"), py::arg("num_vectors"), py::arg("vector_dim") = 1)
        .def_static("from_numpy", &codebook_from_numpy, py::arg("id"), py::arg("values"),
                    "1-D values -> scalar codebook; 2-D (n, dim) -> vector codebook.")
        .def_property_readonly("id", &Codebook::id)
        .def_property_readonly("num_vectors", &Codebook::num_vectors)
        .def_property_readonly("vector_dim", &Codebook::vector_dim)
        .def_property_readonly("is_scalar", &Codebook::is_scalar)
        .def("values", &codebook_values, "Copy of the codebook as float32 (num_vectors, vector_dim).")
        .def("scalar", &Codebook::scalar, py::arg("index"))
        .def("set_scalar", &Codebook::set_scalar, py::arg("index"), py::arg("value"))
        .def("set_vector", [](Codebook& cb, uint32_t idx, const F32Array& v) {
                if (v.size() != cb.vector_dim()) throw py::value_error("vector length != vector_dim");
                cb.set_vector(idx, v.data());
            }, py::arg("index"), py::arg("vector"))
        .def("expand", &Codebook::expand, py::arg("added"));

    // ------------------------------------------------------------ TensorDescriptor
    py::class_<TensorDescriptor>(m, "TensorDescriptor")
        .def(py::init([](std::string name, std::vector<uint32_t> shape, DType dtype, TensorType tensor_type,
                         uint16_t codebook_id, uint16_t delta_id, uint16_t sparse_mask_id, float scale,
                         int32_t zero_point, uint16_t flags) {
                 TensorDescriptor d;
                 d.name = std::move(name); d.shape = std::move(shape); d.dtype = dtype;
                 d.tensor_type = tensor_type; d.codebook_id = codebook_id; d.delta_id = delta_id;
                 d.sparse_mask_id = sparse_mask_id; d.scale = scale; d.zero_point = zero_point; d.flags = flags;
                 return d;
             }),
             py::arg("name"), py::arg("shape"), py::arg("dtype") = DType::INT8,
             py::arg("tensor_type") = TensorType::Standard, py::arg("codebook_id") = LQT_ID_NONE,
             py::arg("delta_id") = LQT_ID_NONE, py::arg("sparse_mask_id") = LQT_ID_NONE,
             py::arg("scale") = 1.0f, py::arg("zero_point") = 0, py::arg("flags") = 0)
        .def_readwrite("name", &TensorDescriptor::name)
        .def_readwrite("tensor_type", &TensorDescriptor::tensor_type)
        .def_readwrite("dtype", &TensorDescriptor::dtype)
        .def_readwrite("shape", &TensorDescriptor::shape)
        .def_readwrite("codebook_id", &TensorDescriptor::codebook_id)
        .def_readwrite("delta_id", &TensorDescriptor::delta_id)
        .def_readwrite("sparse_mask_id", &TensorDescriptor::sparse_mask_id)
        .def_readwrite("scale", &TensorDescriptor::scale)
        .def_readwrite("zero_point", &TensorDescriptor::zero_point)
        .def_readwrite("flags", &TensorDescriptor::flags)
        .def("element_count", &TensorDescriptor::element_count)
        .def("has_flag", &TensorDescriptor::has_flag)
        .def("set_flag", &TensorDescriptor::set_flag, py::arg("flag"), py::arg("on") = true)
        .def("validate", &TensorDescriptor::validate);

    // ------------------------------------------------------------ DeltaBuffer
    py::class_<DeltaBuffer>(m, "DeltaBuffer")
        .def(py::init([](uint16_t delta_id, const F32Array& values, py::object indices, DType dtype) {
                 DeltaBuffer d;
                 d.delta_id = delta_id; d.dtype = dtype; d.values = to_fvec(values);
                 if (!indices.is_none()) {
                     U32Array idx = indices.cast<U32Array>();
                     d.sparse = true;
                     d.indices.assign(idx.data(), idx.data() + idx.size());
                     if (d.indices.size() != d.values.size())
                         throw py::value_error("sparse delta: indices and values lengths differ");
                 }
                 return d;
             }),
             py::arg("delta_id"), py::arg("values"), py::arg("indices") = py::none(), py::arg("dtype") = DType::FP16)
        .def_readwrite("delta_id", &DeltaBuffer::delta_id)
        .def_readwrite("dtype", &DeltaBuffer::dtype)
        .def_readonly("sparse", &DeltaBuffer::sparse)
        .def_property_readonly("values", [](const DeltaBuffer& d) { return from_fvec(d.values); })
        .def_property_readonly("indices", [](const DeltaBuffer& d) {
            U32Array out(static_cast<py::ssize_t>(d.indices.size()));
            if (!d.indices.empty()) std::memcpy(out.mutable_data(), d.indices.data(), d.indices.size() * 4);
            return out;
        });

    // ------------------------------------------------------------ RTA block (structure stored in .lqt)
    py::class_<RtaDimensionBlock>(m, "RtaDimensionBlock")
        .def(py::init([](std::array<uint32_t, 5> dims, RtaDistribution dist, uint8_t flags) {
                 RtaDimensionBlock b;
                 for (size_t i = 0; i < 5; ++i) b.dim_sizes[i] = dims[i];
                 b.distribution = dist; b.flags = flags;
                 return b;
             }),
             py::arg("dim_sizes") = std::array<uint32_t, 5>{1, 1, 1, 1, 1},
             py::arg("distribution") = RtaDistribution::Normal, py::arg("flags") = 0)
        .def_readonly("rank", &RtaDimensionBlock::rank)
        .def_readwrite("distribution", &RtaDimensionBlock::distribution)
        .def_readwrite("flags", &RtaDimensionBlock::flags)
        .def_property("dim_sizes",
            [](const RtaDimensionBlock& b) { return std::array<uint32_t, 5>{b.dim_sizes[0], b.dim_sizes[1], b.dim_sizes[2], b.dim_sizes[3], b.dim_sizes[4]}; },
            [](RtaDimensionBlock& b, std::array<uint32_t, 5> v) { for (size_t i = 0; i < 5; ++i) b.dim_sizes[i] = v[i]; })
        .def("validate", &RtaDimensionBlock::validate);

    py::class_<RtaBlock>(m, "RtaBlock")
        .def(py::init([](RtaDimensionBlock dims, SparseEncoding enc, py::bytes payload,
                         std::vector<std::pair<std::string, std::string>> metadata) {
                 RtaBlock b;
                 b.dims = dims; b.sparse_encoding = enc; b.sparse_payload = from_pybytes(payload);
                 b.metadata = std::move(metadata);
                 return b;
             }),
             py::arg("dims"), py::arg("sparse_encoding") = SparseEncoding::Uniform,
             py::arg("sparse_payload") = py::bytes(),
             py::arg("metadata") = std::vector<std::pair<std::string, std::string>>{})
        .def_readwrite("dims", &RtaBlock::dims)
        .def_readwrite("sparse_encoding", &RtaBlock::sparse_encoding)
        .def_readwrite("metadata", &RtaBlock::metadata)
        .def_property("sparse_payload", [](const RtaBlock& b) { return to_pybytes(b.sparse_payload); },
                      [](RtaBlock& b, py::bytes p) { b.sparse_payload = from_pybytes(p); })
        .def_property_readonly("num_references", [](const RtaBlock& b) { return b.references.size(); })
        .def("validate", &RtaBlock::validate);

    m.def("sparse_build_uniform", [](uint32_t n) { return to_pybytes(sparse_build_uniform(n)); }, py::arg("element_count"));
    m.def("sparse_build_bitmap", [](const std::vector<bool>& present) {
              std::vector<uint64_t> words((present.size() + 63) / 64, 0);
              for (size_t i = 0; i < present.size(); ++i) if (present[i]) words[i / 64] |= (uint64_t{1} << (i % 64));
              return to_pybytes(sparse_build_bitmap(static_cast<uint32_t>(present.size()), words));
          }, py::arg("present"), "Exact-membership bitmap payload (CompressedBitmap) from a bool list.");
    m.def("sparse_build_rle", [](const std::vector<std::tuple<uint32_t, uint32_t, float>>& runs) {
              std::vector<RleRun> r;
              for (auto& [s, l, v] : runs) r.push_back(RleRun{s, l, v});
              return to_pybytes(sparse_build_rle(r));
          }, py::arg("runs"), "RLE payload from [(start, length, value), ...].");
    m.def("sparse_build_hierarchical", [](uint32_t total, const std::vector<uint32_t>& nonzero, uint32_t block_size) {
              HierarchicalSparse h;
              h.block_size = block_size; h.total_elements = total; h.l1_indices = nonzero;
              h.l0_words.assign(((total + block_size - 1) / block_size + 63) / 64, 0);
              for (uint32_t f : nonzero) { uint32_t blk = f / block_size; h.l0_words[blk / 64] |= (uint64_t{1} << (blk % 64)); }
              return to_pybytes(sparse_build_hierarchical(h));
          }, py::arg("total_elements"), py::arg("nonzero_indices"), py::arg("block_size") = 64);

    // ------------------------------------------------------------ RecursiveWeight (storage bucket)
    py::class_<RecursiveWeight>(m, "RecursiveWeight",
        "Storage bucket W = {B, Phi, R, T, epsilon}: own codebook index B, phase harmonics Phi, "
        "reference tensor R (k,d,d), 5-D lattice position T, error vector epsilon, self-reference alpha.")
        .def(py::init(&make_weight),
             py::arg("base_index") = 0, py::arg("phase") = F32Array(0), py::arg("reference") = F32Array(0),
             py::arg("tensor_position") = F32Array(std::vector<py::ssize_t>{5}), py::arg("error") = F32Array(0),
             py::arg("self_reference_coeff") = 0.5f)
        .def_readwrite("base_index", &RecursiveWeight::base_index)
        .def_readwrite("self_reference_coeff", &RecursiveWeight::self_reference_coeff)
        .def_property("phase", [](const RecursiveWeight& w) { return from_fvec(w.phase); },
                      [](RecursiveWeight& w, const F32Array& a) { w.phase = to_fvec(a); })
        .def_property("error", [](const RecursiveWeight& w) { return from_fvec(w.error); },
                      [](RecursiveWeight& w, const F32Array& a) { w.error = to_fvec(a); })
        .def_property("tensor_position",
            [](const RecursiveWeight& w) { return from_fvec(std::vector<float>(w.tensor_position.begin(), w.tensor_position.end())); },
            [](RecursiveWeight& w, const F32Array& a) {
                if (a.size() != 5) throw py::value_error("tensor_position must have 5 elements");
                for (size_t i = 0; i < 5; ++i) w.tensor_position[i] = a.data()[i];
            })
        .def_property_readonly("reference", &weight_reference, "Copy of R as float32 (k, d, d).")
        .def("validate", &RecursiveWeight::validate)
        .def("phase_at", &RecursiveWeight::phase_at, py::arg("t"))
        .def("reconstruct", &RecursiveWeight::reconstruct, py::arg("codebook"), py::arg("scale"), py::arg("t") = 0.0)
        .def("convergence_value", &RecursiveWeight::convergence_value, py::arg("codebook"), py::arg("scale"), py::arg("t") = 0.0)
        .def("reference_energy", &RecursiveWeight::reference_energy)
        .def("compute_effective_value", [](const RecursiveWeight& w, const F32Array& cb, float scale, double t, uint32_t max_depth, uint32_t depth) {
                RwComputeContext ctx; ctx.timestamp = t; ctx.max_depth = max_depth; ctx.current_depth = depth;
                return rw_compute_effective_value(w, to_fvec(cb), scale, ctx);
            }, py::arg("codebook_values"), py::arg("scale") = 1.0f, py::arg("t") = 0.0,
               py::arg("max_depth") = RW_MAX_RECURSION_DEPTH, py::arg("depth") = 8u)
        .def("converge", [](const RecursiveWeight& w, const F32Array& cb, float scale, float tol, uint32_t max_iter) {
                RwConvergenceResult r = rw_converge(w, to_fvec(cb), scale, tol, max_iter);
                py::dict d; d["value"] = r.value; d["iterations"] = r.iterations;
                d["converged"] = r.converged; d["final_delta"] = r.final_delta; return d;
            }, py::arg("codebook_values"), py::arg("scale") = 1.0f, py::arg("tol") = 1e-6f,
               py::arg("max_iter") = RW_MAX_RECURSION_DEPTH)
        .def("to_bytes", &weight_to_bytes)
        .def_static("from_bytes", &weight_from_bytes, py::arg("data"))
        .def("copy", [](const RecursiveWeight& w) { return RecursiveWeight(w); })
        .def("__repr__", [](const RecursiveWeight& w) {
            return "RecursiveWeight(B=" + std::to_string(w.base_index) + ", |Phi|=" + std::to_string(w.phase.size()) +
                   ", R=" + std::to_string(w.r_k) + "x" + std::to_string(w.r_d) + "x" + std::to_string(w.r_d) +
                   ", |eps|=" + std::to_string(w.error.size()) + ", alpha=" + std::to_string(w.self_reference_coeff) + ")";
        });

    m.def("validate_weight", [](const RecursiveWeight& w, uint32_t iters, float tol) {
              ValidationResult r = validate_weight(w, iters, tol);
              py::list passes;
              for (const auto& p : r.passes) {
                  py::dict d; d["name"] = p.name; d["passed"] = p.passed; d["message"] = p.message; d["score"] = p.score;
                  passes.append(d);
              }
              py::dict d; d["valid"] = r.valid; d["summary"] = r.summary; d["overall_score"] = r.overall_score; d["passes"] = passes;
              return d;
          }, py::arg("weight"), py::arg("convergence_iter") = 50u, py::arg("convergence_tol") = 1e-4f);

    py::class_<PatternLibrary>(m, "PatternLibrary")
        .def(py::init<>())
        .def("register_pattern", [](PatternLibrary& p, uint32_t id, const F32Array& data, const std::string& name) {
                p.register_pattern(id, to_fvec(data), name);
            }, py::arg("pattern_id"), py::arg("data"), py::arg("name") = "")
        .def("get_pattern_value", [](const PatternLibrary& p, uint32_t id, const F32Array& ctx) {
                return from_fvec(p.get_pattern_value(id, to_fvec(ctx)));
            }, py::arg("pattern_id"), py::arg("context") = F32Array(0))
        .def("has_pattern", &PatternLibrary::has_pattern)
        .def("__len__", &PatternLibrary::size);

    py::class_<EvolutionEngine>(m, "EvolutionEngine")
        .def(py::init<uint64_t>(), py::arg("seed") = 42)
        .def("evolve_generation", [](EvolutionEngine& e, std::vector<RecursiveWeight> pop, FitnessFunc fit, float mr, float cr) {
                float avg = e.evolve_generation(pop, std::move(fit), mr, cr);
                return py::make_tuple(pop, avg);
            }, py::arg("population"), py::arg("fitness"), py::arg("mutation_rate") = 0.01f, py::arg("crossover_rate") = 0.1f,
            "Returns (new_population, average_fitness).")
        .def("evolve", [](EvolutionEngine& e, std::vector<RecursiveWeight> pop, FitnessFunc fit, uint32_t gens, float mr, float cr) {
                std::vector<float> hist = e.evolve(pop, std::move(fit), gens, mr, cr);
                return py::make_tuple(pop, hist);
            }, py::arg("population"), py::arg("fitness"), py::arg("generations") = 10u,
            py::arg("mutation_rate") = 0.01f, py::arg("crossover_rate") = 0.1f,
            "Returns (new_population, fitness_history).")
        .def("mutate", [](EvolutionEngine& e, RecursiveWeight w, float mr) { e.mutate(w, mr); return w; },
             py::arg("weight"), py::arg("mutation_rate"), "Returns a mutated copy.")
        .def("crossover", &EvolutionEngine::crossover, py::arg("parent1"), py::arg("parent2"));

    // dynamics (rw_dynamics.h): reference matrices passed as list of flat d*d float lists
    py::module_ dyn = m.def_submodule("dynamics", "Recursive-weight dynamical-systems analysis (rw_dynamics.h).");
    dyn.def("fixed_point_convergence", [](float alpha, const F32Array& base) { return from_fvec(dynamics::fixed_point_convergence(alpha, to_fvec(base))); },
            py::arg("alpha"), py::arg("base_components"));
    dyn.def("lyapunov_stable", &dynamics::lyapunov_stable, py::arg("reference_matrices"), py::arg("d"));
    dyn.def("attractor_dimension", &dynamics::attractor_dimension, py::arg("reference_matrices"), py::arg("d"));
    dyn.def("spectral_radius", [](const std::vector<float>& mtx, uint32_t d) { return dynamics::spectral_radius(mtx, d); },
            py::arg("matrix"), py::arg("d"));
    dyn.def("self_similarity_metric", &dynamics::self_similarity_metric, py::arg("reference_matrices"), py::arg("d"));
    dyn.def("error_correction_capacity", &dynamics::error_correction_capacity, py::arg("gamma"), py::arg("epsilon_max"));
    dyn.def("convergence_rate", &dynamics::convergence_rate, py::arg("epsilon"), py::arg("gamma"), py::arg("C"));

    // ------------------------------------------------------------ LqtModel (the .lqt container)
    py::class_<LqtModel>(m, "LqtModel",
        "In-memory .lqt container: codebooks, quantized tensors, deltas, RTA blocks, RecursiveWeight buckets, "
        "hash-chained edit log + undo stack.")
        .def(py::init<>())
        .def_static("load", &LqtModel::load, py::arg("path"))
        .def("save", &LqtModel::save, py::arg("path"))
        .def("to_bytes", [](const LqtModel& mm) { return to_pybytes(mm.serialize_to_bytes()); })
        .def_static("from_bytes", [](const py::bytes& b) {
                std::vector<uint8_t> buf = from_pybytes(b);
                return LqtModel::parse(buf.data(), buf.size());
            }, py::arg("data"))
        .def_property_readonly("format_version", [](const LqtModel& mm) { return mm.header().version; })
        .def("set_hyperparam", &LqtModel::set_hyperparam, py::arg("key"), py::arg("value"))
        .def_property_readonly("hyperparams", [](const LqtModel& mm) { return mm.hyperparams(); })
        .def_property("module_graph_json", &LqtModel::module_graph_json, &LqtModel::set_module_graph_json)
        .def("add_codebook", &LqtModel::add_codebook, py::arg("codebook"))
        .def("codebook", [](const LqtModel& mm, uint16_t id) -> py::object {
                const Codebook* cb = mm.codebook(id); if (!cb) return py::none(); return py::cast(*cb);
            }, py::arg("id"), "Copy of codebook `id`, or None.")
        .def("add_tensor", [](LqtModel& mm, TensorDescriptor d, py::bytes packed) {
                mm.add_tensor(std::move(d), from_pybytes(packed));
            }, py::arg("descriptor"), py::arg("packed_indices"))
        .def("add_tensor_indices", [](LqtModel& mm, TensorDescriptor d, const U32Array& idx) {
                if (static_cast<uint64_t>(idx.size()) != d.element_count())
                    throw py::value_error("indices length != descriptor element_count");
                std::vector<uint32_t> v(idx.data(), idx.data() + idx.size());
                std::vector<uint8_t> packed = pack_indices(v, d.dtype);
                mm.add_tensor(std::move(d), std::move(packed));
            }, py::arg("descriptor"), py::arg("indices"),
            "Pack u32 codebook indices with lqt::pack_indices (inverse of unpack_indices) and add the tensor.")
        .def("tensor_names", [](const LqtModel& mm) {
                std::vector<std::string> n; for (const auto& t : mm.tensors()) n.push_back(t.desc.name); return n;
            })
        .def("descriptor", [](const LqtModel& mm, const std::string& name) {
                const TensorBlob* tb = mm.find_tensor(name);
                if (!tb) throw py::key_error("tensor not found: " + name);
                return tb->desc;
            }, py::arg("name"))
        .def("indices", [](const LqtModel& mm, const std::string& name) {
                const TensorBlob* tb = mm.find_tensor(name);
                if (!tb) throw py::key_error("tensor not found: " + name);
                std::vector<uint32_t> v = unpack_indices(tb->indices.data(), tb->indices.size(),
                                                         static_cast<size_t>(tb->desc.element_count()), tb->desc.dtype);
                U32Array out(static_cast<py::ssize_t>(v.size()));
                if (!v.empty()) std::memcpy(out.mutable_data(), v.data(), v.size() * 4);
                return out;
            }, py::arg("name"))
        .def("add_delta", &LqtModel::add_delta, py::arg("delta"))
        .def("delta", [](const LqtModel& mm, uint16_t id) -> py::object {
                const DeltaBuffer* d = mm.delta(id); if (!d) return py::none(); return py::cast(*d);
            }, py::arg("id"))
        .def("add_rta_block", &LqtModel::add_rta_block, py::arg("name"), py::arg("block"))
        .def("rta_block", [](const LqtModel& mm, const std::string& n) -> py::object {
                const RtaBlock* b = mm.get_rta_block(n); if (!b) return py::none(); return py::cast(*b);
            }, py::arg("name"))
        .def("add_recursive_weight", &LqtModel::add_recursive_weight, py::arg("name"), py::arg("weight"))
        .def("recursive_weights", [](const LqtModel& mm, const std::string& n) {
                const auto* v = mm.get_recursive_weights(n);
                return v ? *v : std::vector<RecursiveWeight>{};
            }, py::arg("name"))
        .def("reconstruct", [](const LqtModel& mm, const std::string& name, bool shaped) {
                std::vector<float> v;
                std::vector<uint32_t> shape;
                {
                    py::gil_scoped_release nogil;
                    v = mm.reconstruct(name);
                    const TensorBlob* tb = mm.find_tensor(name);
                    if (tb) shape = tb->desc.shape;
                }
                F32Array out = from_fvec(v);
                uint64_t prod = 1; for (auto s : shape) prod *= s;
                if (shaped && !shape.empty() && prod == v.size()) {
                    std::vector<py::ssize_t> sh(shape.begin(), shape.end());
                    return F32Array(out.reshape(sh));
                }
                return out;
            }, py::arg("name"), py::arg("shaped") = true,
            "Dequantized float32 values (codebook*scale + delta, RTA sparsity, RecursiveWeight buckets; D-024).")
        // mutation surface (each appends a chained EditLog entry and an undo snapshot)
        .def("edit_codebook", [](LqtModel& mm, uint16_t id, uint32_t idx, const F32Array& v) {
                mm.edit_codebook(id, idx, to_fvec(v));
            }, py::arg("codebook_id"), py::arg("vector_idx"), py::arg("value"))
        .def("edit_codebook_scalar", py::overload_cast<uint16_t, uint32_t, float>(&LqtModel::edit_codebook),
             py::arg("codebook_id"), py::arg("vector_idx"), py::arg("value"))
        .def("update_delta", py::overload_cast<const DeltaBuffer&>(&LqtModel::update_delta), py::arg("replacement"))
        .def("hot_swap_module", [](LqtModel& mm, const std::string& n, py::bytes blob) {
                mm.hot_swap_module(n, from_pybytes(blob));
            }, py::arg("module_name"), py::arg("blob"))
        // ---- D-025 logged RecursiveWeight / RecursiveTensor mutations ----
        .def("edit_recursive_weights", [](LqtModel& mm, const std::string& n,
                                          std::vector<std::pair<uint32_t, RecursiveWeight>> edits) {
                mm.edit_recursive_weights(n, edits);
            }, py::arg("name"), py::arg("edits"),
            "Replace buckets [(slot, RecursiveWeight)] of `name` as ONE logged, rollback-able mutation (D-025).")
        .def("edit_recursive_weight", &LqtModel::edit_recursive_weight, py::arg("name"), py::arg("slot"), py::arg("weight"))
        .def("edit_recursive_weights_scalar", [](LqtModel& mm, const std::string& n, const U32Array& slots,
                                                 const U32Array& base_index, const F32Array& error,
                                                 const U32Array& keep_error) {
                const auto* cur = mm.get_recursive_weights(n);
                if (!cur) throw py::key_error("no buckets attached to: " + n);
                const py::ssize_t k = slots.size();
                if (base_index.size() != k || error.size() != k || keep_error.size() != k)
                    throw py::value_error("slots/base_index/error/keep_error length mismatch");
                std::vector<std::pair<uint32_t, RecursiveWeight>> edits;
                edits.reserve(static_cast<size_t>(k));
                for (py::ssize_t i = 0; i < k; ++i) {
                    const uint32_t slot = slots.data()[i];
                    if (slot >= cur->size()) throw py::index_error("bucket slot out of range");
                    RecursiveWeight rw = (*cur)[slot];   // keeps T, Phi, R, alpha
                    rw.base_index = base_index.data()[i];
                    rw.error.clear();
                    if (keep_error.data()[i]) rw.error.push_back(error.data()[i]);
                    edits.emplace_back(slot, std::move(rw));
                }
                { py::gil_scoped_release nogil; mm.edit_recursive_weights(n, edits); }
            }, py::arg("name"), py::arg("slots"), py::arg("base_index"), py::arg("error"), py::arg("keep_error"),
            "Bulk D-025 edit of scalar buckets: per slot set B and epsilon=[error] (or [] when keep_error==0); "
            "T, Phi, R and alpha are kept. One logged mutation.")
        .def("attach_recursive_tensor", [](LqtModel& mm, TensorDescriptor d, const U32Array& idx, RtaBlock blk,
                                           std::vector<RecursiveWeight> buckets) {
                if (static_cast<uint64_t>(idx.size()) != d.element_count())
                    throw py::value_error("indices length != descriptor element_count");
                std::vector<uint32_t> v(idx.data(), idx.data() + idx.size());
                std::vector<uint8_t> packed = pack_indices(v, d.dtype);
                mm.attach_recursive_tensor(std::move(d), std::move(packed), std::move(blk), std::move(buckets));
            }, py::arg("descriptor"), py::arg("indices"), py::arg("block"), py::arg("buckets"))
        .def("attach_recursive_tensor_scalar", [](LqtModel& mm, TensorDescriptor d, const U32Array& base_index,
                                                  const F32Array& error, const U32Array& keep_error, bool logged,
                                                  std::vector<std::pair<std::string, std::string>> metadata) {
                const uint64_t n = d.element_count();
                if (static_cast<uint64_t>(base_index.size()) != n || static_cast<uint64_t>(error.size()) != n ||
                    static_cast<uint64_t>(keep_error.size()) != n)
                    throw py::value_error("base_index/error/keep_error length != descriptor element_count");
                if (d.shape.size() != LQT_RTA_RANK) throw py::value_error("descriptor must be rank 5");
                RtaBlock blk;
                for (size_t a = 0; a < LQT_RTA_RANK; ++a) blk.dims.dim_sizes[a] = d.shape[a];
                blk.sparse_encoding = SparseEncoding::Uniform;
                blk.sparse_payload = sparse_build_uniform(static_cast<uint32_t>(n));
                blk.metadata = std::move(metadata);
                std::vector<uint32_t> v(base_index.data(), base_index.data() + n);
                std::vector<RecursiveWeight> buckets(static_cast<size_t>(n));
                {
                    py::gil_scoped_release nogil;
                    for (uint64_t i = 0; i < n; ++i) {
                        RecursiveWeight& rw = buckets[static_cast<size_t>(i)];
                        rw.base_index = v[static_cast<size_t>(i)];
                        uint64_t rem = i;
                        for (int a = static_cast<int>(LQT_RTA_RANK) - 1; a >= 0; --a) {
                            rw.tensor_position[static_cast<size_t>(a)] = static_cast<float>(rem % d.shape[static_cast<size_t>(a)]);
                            rem /= d.shape[static_cast<size_t>(a)];
                        }
                        if (keep_error.data()[i]) rw.error.push_back(error.data()[i]);
                    }
                }
                std::vector<uint8_t> packed = pack_indices(v, d.dtype);
                if (logged) {
                    py::gil_scoped_release nogil;
                    mm.attach_recursive_tensor(std::move(d), std::move(packed), std::move(blk), std::move(buckets));
                } else {
                    // builder path (model construction, not a mutation): same validation, no log entry
                    d.validate();
                    const std::string name = d.name;
                    mm.add_tensor(std::move(d), std::move(packed));
                    mm.add_rta_block(name, std::move(blk));
                    for (auto& rw : buckets) mm.add_recursive_weight(name, std::move(rw));
                }
            }, py::arg("descriptor"), py::arg("base_index"), py::arg("error"), py::arg("keep_error"),
            py::arg("logged") = true,
            py::arg("metadata") = std::vector<std::pair<std::string, std::string>>{},
            "One scalar RecursiveWeight bucket per lattice position (B=base_index[i], T=unravel(i), "
            "epsilon=[error[i]] or []), Uniform RtaBlock over the descriptor's 5-D shape, structural index "
            "array = B. logged=True: one D-025 TensorAttach mutation; logged=False: builder (genesis).")
        .def("recursive_weight_arrays", [](const LqtModel& mm, const std::string& n) {
                const auto* cur = mm.get_recursive_weights(n);
                if (!cur) throw py::key_error("no buckets attached to: " + n);
                const py::ssize_t k = static_cast<py::ssize_t>(cur->size());
                U32Array b(k); F32Array e(k); F32Array t(std::vector<py::ssize_t>{k, 5});
                U32Array ne(k);
                for (py::ssize_t i = 0; i < k; ++i) {
                    const RecursiveWeight& rw = (*cur)[static_cast<size_t>(i)];
                    b.mutable_data()[i] = rw.base_index;
                    float acc = 0.0f; for (float x : rw.error) acc += x;
                    e.mutable_data()[i] = rw.error.empty() ? 0.0f : acc / static_cast<float>(rw.error.size());
                    ne.mutable_data()[i] = static_cast<uint32_t>(rw.error.size());
                    for (int a = 0; a < 5; ++a) t.mutable_data()[i * 5 + a] = rw.tensor_position[static_cast<size_t>(a)];
                }
                return py::make_tuple(b, e, t, ne);
            }, py::arg("name"), "(base_index u32[n], mean(epsilon) f32[n], T f32[n,5], len(epsilon) u32[n]) of the buckets.")
        .def("detach_tensor", &LqtModel::detach_tensor, py::arg("name"))
        .def("rollback", &LqtModel::rollback, py::arg("n") = 1)
        .def_property_readonly("undo_depth", &LqtModel::undo_depth)
        .def("edit_log", [](const LqtModel& mm) {
                py::list out; const EditLog& log = mm.edit_log();
                for (size_t i = 0; i < log.size(); ++i) out.append(edit_entry_dict(log.at(i)));
                return out;
            }, "List of edit-log entries as dicts (timestamp_ns, type, target, data_hash, signature).")
        .def("verify_edit_log", [](const LqtModel& mm) { return mm.edit_log().verify_chain(); })
        .def_property_readonly("edit_log_tail_hash", [](const LqtModel& mm) { return mm.edit_log().tail_hash(); });

    m.def("pack_indices", [](const U32Array& idx, DType dt) {
              std::vector<uint32_t> v(idx.data(), idx.data() + idx.size());
              return to_pybytes(pack_indices(v, dt));
          }, py::arg("indices"), py::arg("dtype"));
    m.def("unpack_indices", [](py::bytes b, size_t count, DType dt) {
              std::vector<uint8_t> buf = from_pybytes(b);
              std::vector<uint32_t> v = unpack_indices(buf.data(), buf.size(), count, dt);
              U32Array out(static_cast<py::ssize_t>(v.size()));
              if (!v.empty()) std::memcpy(out.mutable_data(), v.data(), v.size() * 4);
              return out;
          }, py::arg("data"), py::arg("count"), py::arg("dtype"));

    // ============================================================ COMPUTE
    // ------------------------------------------------------------ lqt rta_ops (5-D dense kernels)
    m.def("rta_contract", [](const F32Array& a, const F32Array& b, std::vector<uint32_t> axa, std::vector<uint32_t> axb) {
              return dense5_to_numpy(rta_contract(dense5_from_numpy(a), dense5_from_numpy(b), axa, axb));
          }, py::arg("a"), py::arg("b"), py::arg("axes_a"), py::arg("axes_b"),
          "lqt::rta_contract over 5-D float32 arrays (shape stays rank-5 per rta_ops.h).");
    m.def("rta_project", [](const F32Array& src, const std::vector<std::vector<float>>& basis, std::vector<uint32_t> axes) {
              return dense5_to_numpy(rta_project(dense5_from_numpy(src), basis, axes));
          }, py::arg("src"), py::arg("basis"), py::arg("axes"));
    m.def("rta_expand", [](const F32Array& src, uint32_t new_size, uint32_t num_new_dims) {
              return dense5_to_numpy(rta_expand(dense5_from_numpy(src), new_size, num_new_dims));
          }, py::arg("src"), py::arg("new_size"), py::arg("num_new_dims"));

    // ------------------------------------------------------------ rta::RecursiveTensor<double>
    bind_recursive_tensor(m);  // bindings/lqt_native_rta.cpp (separate TU: keeps per-TU compile memory < ~1.5 GB)
}
