// tests/test_model.cpp — A10 end-to-end: assemble a full .lqt, read it back,
// reconstruct, and prove the whole-file CRC detects corruption.
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

#include "lqt/model.h"
#include "test_framework.h"

using namespace lqt;

// Build a representative model: 1 codebook, 1 INT4 tensor, 1 delta, 1 mask.
static LqtModel build_sample() {
    LqtModel m;
    m.set_hyperparam("num_layers", 2.0f);
    m.set_hyperparam("hidden_dim", 8.0f);
    m.set_module_graph_json(
        "{\"modules\":[{\"id\":\"l0\",\"type\":\"FFN\"}],\"inputs\":[\"x\"],\"outputs\":[\"y\"]}");

    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m.add_codebook(cb);

    TensorDescriptor d;
    d.name = "w0";
    d.tensor_type = TensorType::Standard;
    d.dtype = DType::INT4;
    d.shape = {4};
    d.codebook_id = 0;
    d.delta_id = 0;
    d.sparse_mask_id = 0;
    d.scale = 2.0f;
    d.set_flag(TensorFlag::Trainable, true);
    // INT4 indices {0,1,2,3} packed low-nibble-first: byte0=0x10, byte1=0x32.
    m.add_tensor(d, std::vector<uint8_t>{0x10, 0x32});

    DeltaBuffer dl;
    dl.delta_id = 0;
    dl.dtype = DType::FP32;
    dl.sparse = false;
    dl.values = {0.5f, 0.5f, 0.5f, 0.5f};
    m.add_delta(dl);

    // Mask keeps weights 0,1,3 and prunes weight 2.
    m.add_sparse_mask(SparseMask(0, SparseEncoding::CompressedBitmap,
                                 std::vector<bool>{true, true, false, true}));
    return m;
}

TEST_CASE(model_full_roundtrip_reconstruct) {
    LqtModel m = build_sample();
    const std::vector<uint8_t> bytes = m.serialize_to_bytes();
    CHECK(bytes.size() > static_cast<size_t>(LQT_HEADER_SIZE + LQT_FOOTER_SIZE));

    LqtModel m2 = LqtModel::parse(bytes.data(), bytes.size());

    // Header + flags
    CHECK_EQ(m2.header().magic, LQT_HEADER_MAGIC);
    CHECK_EQ(m2.header().version, static_cast<uint16_t>(0x0103));
    CHECK_EQ(m2.header().header_size, static_cast<uint32_t>(36));
    CHECK(m2.header().has_flag(HeaderFlag::HasDeltas));
    CHECK(m2.header().has_flag(HeaderFlag::HasSparseMasks));

    // Hyperparameters survive
    bool found = false;
    for (const auto& p : m2.hyperparams()) {
        if (p.first == "num_layers") { found = true; CHECK_NEAR(p.second, 2.0f, 1e-6); }
    }
    CHECK(found);

    // Module graph JSON survives
    CHECK(m2.module_graph_json().find("modules") != std::string::npos);

    // Descriptor survives
    const TensorBlob* tb = m2.find_tensor("w0");
    CHECK(tb != nullptr);
    CHECK(tb->desc.dtype == DType::INT4);
    CHECK_EQ(tb->desc.shape.size(), static_cast<size_t>(1));
    CHECK_EQ(tb->desc.shape[0], 4u);
    CHECK(tb->desc.has_flag(TensorFlag::Trainable));

    // Reconstruction: {1,2,3,4}*2 = {2,4,6,8}; +0.5 = {2.5,4.5,6.5,8.5}; prune idx2.
    const std::vector<float> w = m2.reconstruct("w0");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 2.5f, 1e-3);
    CHECK_NEAR(w[1], 4.5f, 1e-3);
    CHECK_NEAR(w[2], 0.0f, 1e-6); // pruned by mask
    CHECK_NEAR(w[3], 8.5f, 1e-3);
}

TEST_CASE(model_save_and_load_file) {
    LqtModel m = build_sample();
    const std::string path = "/tmp/lqt_test_model.lqt";
    m.save(path);
    LqtModel m2 = LqtModel::load(path);
    const std::vector<float> w = m2.reconstruct("w0");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 2.5f, 1e-3);
    CHECK_NEAR(w[2], 0.0f, 1e-6);
    std::remove(path.c_str());
}

TEST_CASE(model_crc_detects_corruption) {
    LqtModel m = build_sample();
    std::vector<uint8_t> bytes = m.serialize_to_bytes();
    // Corrupt a data byte just past the header (inside the metadata region),
    // which parse() checks via whole-file CRC before any structural parsing.
    bytes[LQT_HEADER_SIZE + 4] ^= 0xFF;
    CHECK_THROWS_AS(LqtModel::parse(bytes.data(), bytes.size()), IntegrityError);
}

TEST_CASE(model_bad_magic_rejected) {
    LqtModel m = build_sample();
    std::vector<uint8_t> bytes = m.serialize_to_bytes();
    bytes[0] ^= 0xFF; // break the LQT1 magic
    CHECK_THROWS_AS(LqtModel::parse(bytes.data(), bytes.size()), FormatError);
}

TEST_CASE(model_empty_optional_regions) {
    // A model with a codebook + tensor but NO deltas and NO masks must still
    // round-trip (empty delta/mask tables, no flags set).
    LqtModel m;
    Codebook cb(0, 2, 1);
    cb.set_scalar(0, 5.0f);
    cb.set_scalar(1, 6.0f);
    m.add_codebook(cb);
    TensorDescriptor d;
    d.name = "t";
    d.dtype = DType::INT8;
    d.shape = {2};
    d.codebook_id = 0;
    d.scale = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0, 1});
    LqtModel m2 = LqtModel::parse(m.serialize_to_bytes().data(),
                                  m.serialize_to_bytes().size());
    CHECK(!m2.header().has_flag(HeaderFlag::HasDeltas));
    CHECK(!m2.header().has_flag(HeaderFlag::HasSparseMasks));
    const std::vector<float> w = m2.reconstruct("t");
    CHECK_NEAR(w[0], 5.0f, 1e-3);
    CHECK_NEAR(w[1], 6.0f, 1e-3);
}

int main() { return lqttest::run_all(); }
