// tests/test_integration_roundtrip.cpp — full write -> save -> reload -> verify cycle.
//
// Council module: A10 (integration), Patch 2 closure.
// Canon: lqt.md §2.1 (Binary Layout Overview), §3.1 (Reconstruction),
//        §8 (Integrity / whole-file CRC-32), Binary Spec v1.3 §4 (RTA).
//
// This file exercises the entire LqtModel surface end-to-end:
//   * Build a model containing 2 tensors (Standard + RecursiveTensor),
//     1 codebook, 1 delta buffer, 1 sparse mask, 1 RTA block.
//   * Save it to a temp file under /tmp.
//   * Reload it from disk into a fresh LqtModel.
//   * Verify: descriptors round-trip, codebook entries are byte-equal,
//     delta values match, sparse mask bits match, the RTA block is present
//     and reachable via get_rta_block(), and edit_log size matches after
//     mutations applied before save.
//   * Verify the whole-file CRC-32 detects corruption: flip a byte inside
//     the file image and confirm LqtModel::parse() throws IntegrityError.
//   * Clean up the temp file.
//
// Each TEST_CASE is self-contained.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <string>
#include <unistd.h>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/delta.h"
#include "lqt/descriptor.h"
#include "lqt/edit_log.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/header.h"
#include "lqt/model.h"
#include "lqt/rta.h"
#include "lqt/sparse_mask.h"
#include "test_framework.h"

using namespace lqt;

// ============================================================================
// Helpers — temp path + small builder for the integration model.
// ============================================================================

// Allocate a unique-ish temp path under /tmp. mkstemp() creates and opens
// the file; we close the fd immediately so the model's own writer can
// truncate-and-replace it cleanly. The caller is responsible for unlinking.
static std::string make_temp_path() {
    char tmpl[] = "/tmp/lqt_integration_XXXXXX";
    int fd = mkstemp(tmpl);
    if (fd >= 0) ::close(fd);
    return std::string(tmpl);
}

static LqtModel build_integration_model() {
    LqtModel m;
    m.set_hyperparam("num_layers", 2.0f);
    m.set_hyperparam("hidden_dim", 4.0f);
    m.set_module_graph_json(
        "{\"modules\":[{\"id\":\"l0\",\"type\":\"FFN\"}],"
        "\"inputs\":[\"x\"],\"outputs\":[\"y\"]}");

    // 1 codebook (id 0, 4 scalar entries).
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m.add_codebook(cb);

    // Standard INT4 tensor "ffn0.weight" of 4 elements,
    // packed indices {0,1,2,3} -> bytes {0x10, 0x32}.
    TensorDescriptor d_std;
    d_std.name          = "ffn0.weight";
    d_std.tensor_type   = TensorType::Standard;
    d_std.dtype         = DType::INT4;
    d_std.shape         = {4};
    d_std.codebook_id   = 0;
    d_std.delta_id      = 0;
    d_std.sparse_mask_id= 0;
    d_std.scale         = 1.0f;
    d_std.set_flag(TensorFlag::Trainable, true);
    m.add_tensor(d_std, std::vector<uint8_t>{0x10, 0x32});

    // RecursiveTensor "rt0" — rank-5 enforced by TensorDescriptor validation
    // (D-001 / LQT_RTA_RANK=5). Shape must have exactly 5 dimensions.
    TensorDescriptor d_rt;
    d_rt.name        = "rt0";
    d_rt.tensor_type = TensorType::RecursiveTensor;
    d_rt.dtype       = DType::INT8;
    d_rt.shape       = {1, 1, 1, 1, 1};  // rank-5 required for RecursiveTensor
    d_rt.codebook_id = LQT_ID_NONE;
    d_rt.scale       = 1.0f;
    m.add_tensor(d_rt, std::vector<uint8_t>{1});

    // 1 dense FP32 delta buffer (id 0).
    DeltaBuffer dl;
    dl.delta_id = 0;
    dl.dtype    = DType::FP32;
    dl.sparse   = false;
    dl.values   = {0.5f, 0.5f, 0.5f, 0.5f};
    m.add_delta(dl);

    // 1 sparse mask (id 0) keeping {0,1,3} and pruning element 2.
    m.add_sparse_mask(SparseMask(0, SparseEncoding::CompressedBitmap,
                                 std::vector<bool>{true, true, false, true}));

    // 1 RTA block named "rt0" matching the RecursiveTensor descriptor.
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::Uniform;
    blk.sparse_payload  = sparse_build_uniform(1);
    blk.metadata.push_back({"role", "integration_test"});
    m.add_rta_block("rt0", blk);

    return m;
}

// ============================================================================
// Integration round-trip: build, mutate, save, reload, verify everything.
// ============================================================================

TEST_CASE(integration_full_save_reload_verify) {
    LqtModel m = build_integration_model();

    // Apply two mutations before save so we can verify the edit log size
    // survives the round-trip exactly.
    m.edit_codebook(/*codebook_id=*/0, /*index=*/2, /*value=*/30.0f);
    DeltaBuffer dl_new;
    dl_new.delta_id = 0;
    dl_new.dtype    = DType::FP32;
    dl_new.sparse   = false;
    dl_new.values   = {0.25f, 0.25f, 0.25f, 0.25f};
    m.update_delta(dl_new);

    const size_t expected_log = m.edit_log().size();
    CHECK_EQ(expected_log, static_cast<size_t>(2));

    // Save to a temp file and reload from disk.
    const std::string path = make_temp_path();
    m.save(path);

    LqtModel reloaded = LqtModel::load(path);

    // ---- Tensor descriptors ----
    CHECK_EQ(reloaded.tensors().size(), static_cast<size_t>(2));
    const TensorBlob* tb_std = reloaded.find_tensor("ffn0.weight");
    CHECK(tb_std != nullptr);
    CHECK_EQ(static_cast<uint8_t>(tb_std->desc.tensor_type),
             static_cast<uint8_t>(TensorType::Standard));
    CHECK_EQ(static_cast<uint8_t>(tb_std->desc.dtype),
             static_cast<uint8_t>(DType::INT4));
    CHECK_EQ(tb_std->desc.shape.size(), static_cast<size_t>(1));
    CHECK_EQ(tb_std->desc.shape[0], 4u);
    CHECK(tb_std->desc.has_flag(TensorFlag::Trainable));

    const TensorBlob* tb_rt = reloaded.find_tensor("rt0");
    CHECK(tb_rt != nullptr);
    CHECK_EQ(static_cast<uint8_t>(tb_rt->desc.tensor_type),
             static_cast<uint8_t>(TensorType::RecursiveTensor));

    // ---- Codebook entries ----
    const Codebook* cb = reloaded.codebook(0);
    CHECK(cb != nullptr);
    CHECK_EQ(cb->num_vectors(), static_cast<uint16_t>(4));
    CHECK_EQ(cb->vector_dim(),  static_cast<uint16_t>(1));
    CHECK_NEAR(cb->scalar(0),  1.0f, 1e-3);
    CHECK_NEAR(cb->scalar(1),  2.0f, 1e-3);
    // codebook[2] was edited to 30.0 before save.
    CHECK_NEAR(cb->scalar(2), 30.0f, 1e-2);
    CHECK_NEAR(cb->scalar(3),  4.0f, 1e-3);

    // ---- Delta buffer ----
    const DeltaBuffer* dl = reloaded.delta(0);
    CHECK(dl != nullptr);
    CHECK_EQ(dl->values.size(), static_cast<size_t>(4));
    CHECK_NEAR(dl->values[0], 0.25f, 1e-6);
    CHECK_NEAR(dl->values[1], 0.25f, 1e-6);
    CHECK_NEAR(dl->values[2], 0.25f, 1e-6);
    CHECK_NEAR(dl->values[3], 0.25f, 1e-6);

    // ---- Sparse mask ----
    const SparseMask* mk = reloaded.sparse_mask(0);
    CHECK(mk != nullptr);
    CHECK_EQ(mk->element_count, 4u);
    CHECK_EQ(mk->bit(0), true);
    CHECK_EQ(mk->bit(1), true);
    CHECK_EQ(mk->bit(2), false);
    CHECK_EQ(mk->bit(3), true);

    // ---- RTA block ----
    const RtaBlock* rt_back = reloaded.get_rta_block("rt0");
    CHECK(rt_back != nullptr);
    CHECK_EQ(rt_back->dims.rank, static_cast<uint8_t>(LQT_RTA_RANK));
    CHECK_EQ(rt_back->dims.dim_sizes[0], 1u);
    CHECK_EQ(rt_back->dims.dim_sizes[4], 1u);
    CHECK_EQ(rt_back->metadata.size(), static_cast<size_t>(1));
    CHECK_EQ(rt_back->metadata[0].first,  std::string("role"));
    CHECK_EQ(rt_back->metadata[0].second, std::string("integration_test"));

    // ---- Edit log entry count ----
    CHECK_EQ(reloaded.edit_log().size(), expected_log);
    CHECK(reloaded.edit_log().verify_chain());

    // ---- Hyperparameters survive ----
    bool found_layers = false;
    for (const auto& p : reloaded.hyperparams()) {
        if (p.first == "num_layers") { found_layers = true; CHECK_NEAR(p.second, 2.0f, 1e-6); }
    }
    CHECK(found_layers);

    // ---- Reconstruction of the Standard tensor still works end-to-end ----
    // Codebook now {1,2,30,4}, delta {0.25,0.25,0.25,0.25}, mask keeps {0,1,3}.
    // weight = cb[idx]*1.0 + 0.25, then mask zeros index 2.
    const std::vector<float> w = reloaded.reconstruct("ffn0.weight");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0],  1.25f, 1e-3);
    CHECK_NEAR(w[1],  2.25f, 1e-3);
    CHECK_NEAR(w[2],  0.0f,  1e-6); // pruned by mask
    CHECK_NEAR(w[3],  4.25f, 1e-3);

    std::remove(path.c_str());
}

// ============================================================================
// CRC-32 corruption detection on the full integration file image.
// ============================================================================

TEST_CASE(integration_crc_corruption_detected) {
    LqtModel m = build_integration_model();
    const std::string path = make_temp_path();
    m.save(path);

    // Read the entire saved file into memory.
    std::ifstream in(path, std::ios::binary | std::ios::ate);
    CHECK(in.good());
    const std::streamsize size = in.tellg();
    CHECK(size > static_cast<std::streamsize>(LQT_HEADER_SIZE + LQT_FOOTER_SIZE));
    in.seekg(0);
    std::vector<uint8_t> buf(static_cast<size_t>(size));
    in.read(reinterpret_cast<char*>(buf.data()), size);
    in.close();

    // A clean parse must succeed.
    LqtModel ok = LqtModel::parse(buf.data(), buf.size());
    (void)ok;

    // Flip a byte inside the body region (just past the header, well clear
    // of the footer's checksum field). parse() runs whole-file CRC-32 first
    // and must raise IntegrityError on any single-bit mutation.
    std::vector<uint8_t> bad = buf;
    bad[LQT_HEADER_SIZE + 4] ^= 0xFF;
    CHECK_THROWS_AS(LqtModel::parse(bad.data(), bad.size()), IntegrityError);

    // load() (which delegates to parse) must surface the same error.
    {
        const std::string bad_path = make_temp_path();
        std::ofstream out(bad_path, std::ios::binary | std::ios::trunc);
        out.write(reinterpret_cast<const char*>(bad.data()),
                  static_cast<std::streamsize>(bad.size()));
        out.close();
        CHECK_THROWS_AS(LqtModel::load(bad_path), IntegrityError);
        std::remove(bad_path.c_str());
    }

    std::remove(path.c_str());
}

// ============================================================================
// MAIN
// ============================================================================

int main() { return lqttest::run_all(); }
