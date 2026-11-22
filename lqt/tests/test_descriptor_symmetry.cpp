// tests/test_descriptor_symmetry.cpp — the writer must refuse descriptors the
// reader rejects (2026-11-21, lane lqt-bindings). Before this, LqtModel::save
// wrote a rank-3 RecursiveTensor descriptor and LqtModel::parse then threw
// "RecursiveTensor must have rank 5" on the file it had just produced.
#include <cstdint>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/descriptor.h"
#include "lqt/error.h"
#include "lqt/model.h"
#include "lqt/reconstruct.h"
#include "lqt/rta.h"
#include "test_framework.h"

using namespace lqt;

static LqtModel model_with_rt_shape(std::vector<uint32_t> shape) {
    LqtModel m;
    Codebook cb(0, 4, 1);
    for (uint32_t i = 0; i < 4; ++i) cb.set_scalar(i, static_cast<float>(i));
    m.add_codebook(cb);
    TensorDescriptor d;
    d.name = "lattice";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype = DType::INT8;
    d.shape = std::move(shape);
    d.codebook_id = 0;
    const size_t n = static_cast<size_t>(d.element_count());
    m.add_tensor(d, pack_indices(std::vector<uint32_t>(n, 1), DType::INT8));
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 2; blk.dims.dim_sizes[1] = 2; blk.dims.dim_sizes[2] = 2;
    blk.sparse_payload = sparse_build_uniform(static_cast<uint32_t>(n));
    m.add_rta_block("lattice", blk);
    return m;
}

TEST_CASE(save_rejects_non_rank5_recursive_tensor_descriptor) {
    LqtModel m = model_with_rt_shape({2, 2, 2});
    CHECK_THROWS_AS(m.serialize_to_bytes(), FormatError);
}

TEST_CASE(rank5_recursive_tensor_descriptor_roundtrips) {
    LqtModel m = model_with_rt_shape({2, 2, 2, 1, 1});
    const std::vector<uint8_t> img = m.serialize_to_bytes();
    LqtModel back = LqtModel::parse(img.data(), img.size());
    const std::vector<float> w = back.reconstruct("lattice");
    CHECK_EQ(w.size(), static_cast<size_t>(8));
    for (float v : w) CHECK_NEAR(v, 1.0f, 1e-6f);
}

int main() { return lqttest::run_all(); }
