// tests/test_descriptor_codebook.cpp — A3 descriptors, codebooks, reconstruction.
#include <cstdint>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/descriptor.h"
#include "lqt/reconstruct.h"
#include "test_framework.h"

using namespace lqt;

// --- Tensor descriptor ------------------------------------------------------
TEST_CASE(descriptor_roundtrip) {
    TensorDescriptor d;
    d.name = "attention.q_proj.weight";
    d.tensor_type = TensorType::Standard;
    d.dtype = DType::INT4;
    d.shape = {4096, 4096};
    d.codebook_id = 7;
    d.delta_id = 3;
    d.sparse_mask_id = LQT_ID_NONE;
    d.scale = 0.0123f;
    d.zero_point = -8;
    d.set_flag(TensorFlag::Trainable, true);
    d.set_flag(TensorFlag::HotSwappable, true);

    ByteWriter w;
    d.serialize(w);
    ByteReader r(w.bytes());
    TensorDescriptor d2 = TensorDescriptor::parse(r);

    CHECK_EQ(d2.name, d.name);
    CHECK(d2.tensor_type == TensorType::Standard);
    CHECK(d2.dtype == DType::INT4);
    CHECK_EQ(d2.shape.size(), static_cast<size_t>(2));
    CHECK_EQ(d2.shape[0], 4096u);
    CHECK_EQ(d2.shape[1], 4096u);
    CHECK_EQ(d2.codebook_id, static_cast<uint16_t>(7));
    CHECK_EQ(d2.delta_id, static_cast<uint16_t>(3));
    CHECK(!d2.has_mask());
    CHECK_NEAR(d2.scale, 0.0123f, 1e-7);
    CHECK_EQ(d2.zero_point, -8);
    CHECK(d2.has_flag(TensorFlag::Trainable));
    CHECK(d2.has_flag(TensorFlag::HotSwappable));
    CHECK(!d2.has_flag(TensorFlag::Protected));
    CHECK_EQ(d2.element_count(), static_cast<uint64_t>(4096) * 4096);
}

TEST_CASE(descriptor_recursive_requires_rank5) {
    TensorDescriptor d;
    d.name = "rta";
    d.tensor_type = TensorType::RecursiveTensor;
    d.shape = {2, 2, 2}; // rank 3 — illegal for RTA
    ByteWriter w;
    d.serialize(w);
    ByteReader r(w.bytes());
    CHECK_THROWS_AS(TensorDescriptor::parse(r), FormatError);
}

// --- Codebook ---------------------------------------------------------------
TEST_CASE(codebook_scalar_roundtrip_and_edit) {
    Codebook cb(5, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    ByteWriter w;
    cb.serialize(w);
    ByteReader r(w.bytes());
    Codebook cb2 = Codebook::parse(r);
    CHECK_EQ(cb2.id(), static_cast<uint16_t>(5));
    CHECK_EQ(cb2.num_vectors(), static_cast<uint16_t>(4));
    CHECK(cb2.is_scalar());
    CHECK_NEAR(cb2.scalar(0), 1.0f, 1e-3);
    CHECK_NEAR(cb2.scalar(3), 4.0f, 1e-3);
    // codebook edit (mutation primitive)
    cb2.set_scalar(2, 9.0f);
    CHECK_NEAR(cb2.scalar(2), 9.0f, 1e-3);
    // out-of-range lookup throws
    CHECK_THROWS_AS(cb2.scalar(4), FormatError);
}

TEST_CASE(codebook_vector_roundtrip) {
    Codebook cb(1, 3, 2);
    float v0[] = {0.5f, -0.5f};
    float v1[] = {1.5f, 2.0f};
    float v2[] = {-3.0f, 4.0f};
    cb.set_vector(0, v0); cb.set_vector(1, v1); cb.set_vector(2, v2);
    ByteWriter w; cb.serialize(w);
    ByteReader r(w.bytes());
    Codebook cb2 = Codebook::parse(r);
    CHECK_EQ(cb2.vector_dim(), static_cast<uint16_t>(2));
    CHECK_NEAR(cb2.vector(1)[0], 1.5f, 1e-3);
    CHECK_NEAR(cb2.vector(2)[1], 4.0f, 1e-3);
}

TEST_CASE(codebook_expand) {
    Codebook cb(0, 2, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.expand(2);
    CHECK_EQ(cb.num_vectors(), static_cast<uint16_t>(4));
    cb.set_scalar(3, 7.0f);
    CHECK_NEAR(cb.scalar(3), 7.0f, 1e-3);
}

// --- Index unpacking --------------------------------------------------------
TEST_CASE(unpack_int4_low_nibble_first) {
    const uint8_t bytes[] = {0x21, 0x43}; // -> 1,2,3,4
    auto idx = unpack_indices(bytes, sizeof(bytes), 4, DType::INT4);
    CHECK_EQ(idx.size(), static_cast<size_t>(4));
    CHECK_EQ(idx[0], 1u); CHECK_EQ(idx[1], 2u);
    CHECK_EQ(idx[2], 3u); CHECK_EQ(idx[3], 4u);
}

TEST_CASE(unpack_int8_and_int16) {
    const uint8_t b8[] = {10, 200, 0};
    auto i8 = unpack_indices(b8, sizeof(b8), 3, DType::INT8);
    CHECK_EQ(i8[1], 200u);
    const uint8_t b16[] = {0x34, 0x12, 0xFF, 0x00}; // 0x1234, 0x00FF
    auto i16 = unpack_indices(b16, sizeof(b16), 2, DType::INT16);
    CHECK_EQ(i16[0], 0x1234u);
    CHECK_EQ(i16[1], 0x00FFu);
}

// --- Multi-stage reconstruction (canon §3.1) --------------------------------
TEST_CASE(reconstruct_scalar_codebook_scale) {
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f); cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f); cb.set_scalar(3, 4.0f);
    std::vector<uint32_t> idx = {0, 1, 2, 3};
    auto w = reconstruct_standard(cb, idx, 2.0f);
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 2.0f, 1e-3);
    CHECK_NEAR(w[1], 4.0f, 1e-3);
    CHECK_NEAR(w[3], 8.0f, 1e-3);
}

TEST_CASE(reconstruct_with_delta_and_mask) {
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f); cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f); cb.set_scalar(3, 4.0f);
    std::vector<uint32_t> idx = {0, 1, 2, 3};
    float delta[] = {0.25f, 0.25f, 0.25f, 0.25f};
    // mask: keep weights 0,2,3; prune weight 1  -> bits 1101 = 0x0D
    uint8_t mask[] = {0x0D};
    auto w = reconstruct_standard(cb, idx, 2.0f, delta, mask);
    CHECK_NEAR(w[0], 2.25f, 1e-3);  // 1*2 + 0.25
    CHECK_NEAR(w[1], 0.0f, 1e-6);   // pruned
    CHECK_NEAR(w[2], 6.25f, 1e-3);  // 3*2 + 0.25
    CHECK_NEAR(w[3], 8.25f, 1e-3);  // 4*2 + 0.25
}

TEST_CASE(reconstruct_vector_codebook) {
    Codebook cb(0, 2, 2);
    float a[] = {1.0f, 2.0f}; float b[] = {3.0f, 4.0f};
    cb.set_vector(0, a); cb.set_vector(1, b);
    std::vector<uint32_t> idx = {1, 0};
    auto w = reconstruct_standard(cb, idx, 1.0f);
    CHECK_EQ(w.size(), static_cast<size_t>(4)); // 2 indices * vector_dim 2
    CHECK_NEAR(w[0], 3.0f, 1e-3); CHECK_NEAR(w[1], 4.0f, 1e-3);
    CHECK_NEAR(w[2], 1.0f, 1e-3); CHECK_NEAR(w[3], 2.0f, 1e-3);
}

TEST_CASE(reconstruct_hierarchical_codebook) {
    HierarchicalCodebook hcb;
    hcb.primary = Codebook(0, 2, 1);
    hcb.primary.set_scalar(0, 1.0f); hcb.primary.set_scalar(1, 5.0f);
    hcb.residual = Codebook(1, 2, 1);
    hcb.residual.set_scalar(0, 0.0f); hcb.residual.set_scalar(1, 1.0f);
    hcb.residual_scale = 0.1f;
    std::vector<uint32_t> p = {0, 1};
    std::vector<uint32_t> rr = {1, 1};
    auto w = reconstruct_hierarchical(hcb, p, rr, 1.0f);
    CHECK_NEAR(w[0], 1.1f, 1e-3);  // 1 + 1*0.1
    CHECK_NEAR(w[1], 5.1f, 1e-3);  // 5 + 1*0.1
}

TEST_CASE(affine_dequant_formula) {
    CHECK_NEAR(dequant_affine(10, 0.5f, 2), 4.0f, 1e-6);   // (10-2)*0.5
    CHECK_NEAR(dequant_affine(0, 0.25f, 8), -2.0f, 1e-6);  // (0-8)*0.25
}

TEST_CASE(end_to_end_int4_reconstruct) {
    Codebook cb(0, 16, 1);
    for (int i = 0; i < 16; ++i) cb.set_scalar(i, static_cast<float>(i));
    const uint8_t packed[] = {0x21, 0x43}; // indices 1,2,3,4
    auto idx = unpack_indices(packed, sizeof(packed), 4, DType::INT4);
    auto w = reconstruct_standard(cb, idx, 10.0f);
    CHECK_NEAR(w[0], 10.0f, 1e-3);
    CHECK_NEAR(w[3], 40.0f, 1e-3);
}

int main() { return lqttest::run_all(); }
