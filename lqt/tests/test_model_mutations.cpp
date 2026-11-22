// tests/test_model_mutations.cpp — Patch 2 model mutation surface tests.
//
// Council module: A10 + A7 integration (model mutation surface).
// Canon: lqt.md §4.1 (Mutation Categories), §5.2 (Mutation Validation),
//        §8 (Tamper-evident edit logs), v1.3 spec §3 (TensorType switch).
//
// These tests pin the contracts for the "Next patch list" items in
// docs/AGENT_REPORT.md:
//   2. LqtModel::edit_codebook / update_delta / hot_swap_module
//   3. LqtModel::add_rta_block / RTA reconstruction routing
//   4. Affine-only reconstruction fallback (codebook_id == LQT_ID_NONE)
//   + EditLog persistence and tamper detection at the model layer.
//
// Each TEST_CASE is self-contained (builds its own LqtModel from scratch).
#include <cstdint>
#include <cstdio>
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
#include "lqt/recursive_weight.h"
#include "lqt/rta.h"
#include "lqt/sparse_mask.h"
#include "test_framework.h"

using namespace lqt;

// ============================================================================
// Test helpers — minimal models that can be mutated in isolation.
// ============================================================================

// Build a model with one scalar codebook (id 0, 4 entries) and one INT4
// tensor "w" of 4 elements whose packed indices are {0,1,2,3}, scale=1.0,
// no delta, no mask. reconstruct("w") returns the raw codebook values.
static LqtModel build_codebook_only_model() {
    LqtModel m;
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m.add_codebook(cb);

    TensorDescriptor d;
    d.name          = "w";
    d.tensor_type   = TensorType::Standard;
    d.dtype         = DType::INT4;
    d.shape         = {4};
    d.codebook_id   = 0;
    d.delta_id      = LQT_ID_NONE;
    d.sparse_mask_id= LQT_ID_NONE;
    d.scale         = 1.0f;
    // INT4 indices {0,1,2,3} packed low-nibble-first: byte0=0x10, byte1=0x32.
    m.add_tensor(d, std::vector<uint8_t>{0x10, 0x32});
    return m;
}

// Build a model with codebook + INT4 tensor + dense FP32 delta_id 0 of length 4.
static LqtModel build_codebook_delta_model() {
    LqtModel m = build_codebook_only_model();

    // Re-add the tensor with a delta link. The simplest path is to rebuild:
    // we need the tensor descriptor to declare delta_id = 0.
    LqtModel m2;
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m2.add_codebook(cb);

    TensorDescriptor d;
    d.name        = "w";
    d.tensor_type = TensorType::Standard;
    d.dtype       = DType::INT4;
    d.shape       = {4};
    d.codebook_id = 0;
    d.delta_id    = 0;
    d.scale       = 1.0f;
    m2.add_tensor(d, std::vector<uint8_t>{0x10, 0x32});

    DeltaBuffer dl;
    dl.delta_id = 0;
    dl.dtype    = DType::FP32;
    dl.sparse   = false;
    dl.values   = {0.0f, 0.0f, 0.0f, 0.0f};
    m2.add_delta(dl);
    return m2;
}

// Build a minimal RTA block (rank-5, uniform sparse, 1x1x1x1x1).
static RtaBlock build_minimal_rta_block() {
    RtaBlock blk;
    blk.dims.dim_sizes[0] = 1;
    blk.dims.dim_sizes[1] = 1;
    blk.dims.dim_sizes[2] = 1;
    blk.dims.dim_sizes[3] = 1;
    blk.dims.dim_sizes[4] = 1;
    blk.sparse_encoding = SparseEncoding::Uniform;
    blk.sparse_payload  = sparse_build_uniform(1);
    return blk;
}

// ============================================================================
// CODEBOOK EDIT — LqtModel::edit_codebook(id, index, value)
// ============================================================================

TEST_CASE(model_edit_codebook_changes_reconstruction) {
    LqtModel m = build_codebook_only_model();

    // Baseline reconstruction: codebook[0..3] -> {1,2,3,4}.
    const std::vector<float> before = m.reconstruct("w");
    CHECK_EQ(before.size(), static_cast<size_t>(4));
    CHECK_NEAR(before[0], 1.0f, 1e-6);
    CHECK_NEAR(before[1], 2.0f, 1e-6);
    CHECK_NEAR(before[2], 3.0f, 1e-6);
    CHECK_NEAR(before[3], 4.0f, 1e-6);

    // Mutate codebook[0] entry 2 from 3.0 to 30.0 via the model API.
    m.edit_codebook(/*codebook_id=*/0, /*index=*/2, /*value=*/30.0f);

    // Reconstruction must reflect the new value at the position whose index is 2.
    const std::vector<float> after = m.reconstruct("w");
    CHECK_EQ(after.size(), static_cast<size_t>(4));
    CHECK_NEAR(after[0], 1.0f,  1e-6);
    CHECK_NEAR(after[1], 2.0f,  1e-6);
    CHECK_NEAR(after[2], 30.0f, 1e-6);
    CHECK_NEAR(after[3], 4.0f,  1e-6);
}

TEST_CASE(model_edit_codebook_appends_edit_log_entry) {
    LqtModel m = build_codebook_only_model();
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(0));

    m.edit_codebook(0, 1, -5.5f);

    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));
    CHECK_EQ(m.edit_log().at(0).type, MutationType::CodebookEdit);
    CHECK(m.edit_log().verify_chain());
}

// ============================================================================
// DELTA UPDATE — LqtModel::update_delta(buffer)
// ============================================================================

TEST_CASE(model_update_delta_replaces_buffer_in_reconstruction) {
    LqtModel m = build_codebook_delta_model();

    // Baseline reconstruction: codebook {1,2,3,4} + zero delta -> {1,2,3,4}.
    const std::vector<float> before = m.reconstruct("w");
    CHECK_EQ(before.size(), static_cast<size_t>(4));
    CHECK_NEAR(before[0], 1.0f, 1e-6);
    CHECK_NEAR(before[3], 4.0f, 1e-6);

    // Replace delta_id 0 with a non-zero dense FP32 buffer.
    DeltaBuffer replacement;
    replacement.delta_id = 0;
    replacement.dtype    = DType::FP32;
    replacement.sparse   = false;
    replacement.values   = {0.25f, 0.5f, 0.75f, 1.0f};
    m.update_delta(replacement);

    const std::vector<float> after = m.reconstruct("w");
    CHECK_EQ(after.size(), static_cast<size_t>(4));
    CHECK_NEAR(after[0], 1.25f, 1e-6);
    CHECK_NEAR(after[1], 2.5f,  1e-6);
    CHECK_NEAR(after[2], 3.75f, 1e-6);
    CHECK_NEAR(after[3], 5.0f,  1e-6);

    // The edit log must have recorded a DeltaUpdate entry.
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));
    CHECK_EQ(m.edit_log().at(0).type, MutationType::DeltaUpdate);
}

// ============================================================================
// MODULE HOT-SWAP — LqtModel::hot_swap_module(name, new_blob)
// ============================================================================

TEST_CASE(model_hot_swap_module_replaces_blob) {
    LqtModel m = build_codebook_only_model();

    // The original tensor "w" has packed indices {0x10, 0x32} -> {0,1,2,3}.
    // Hot-swap it with packed indices {0x32, 0x10} -> {2,3,0,1}.
    const std::vector<uint8_t> new_blob = {0x32, 0x10};
    m.hot_swap_module("w", new_blob);

    const std::vector<float> w = m.reconstruct("w");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 3.0f, 1e-6);
    CHECK_NEAR(w[1], 4.0f, 1e-6);
    CHECK_NEAR(w[2], 1.0f, 1e-6);
    CHECK_NEAR(w[3], 2.0f, 1e-6);

    // Edit log must have recorded a ModuleSwap entry.
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));
    CHECK_EQ(m.edit_log().at(0).type, MutationType::ModuleSwap);
    CHECK_EQ(m.edit_log().at(0).target, std::string("w"));
}

// ============================================================================
// EDIT LOG — persistence through save / load round-trip
// ============================================================================

TEST_CASE(model_edit_log_persists_through_save_load) {
    LqtModel m = build_codebook_delta_model();

    // Three mutations of different types — should produce three log entries.
    m.edit_codebook(0, 0, -1.0f);
    DeltaBuffer d2;
    d2.delta_id = 0;
    d2.dtype    = DType::FP32;
    d2.sparse   = false;
    d2.values   = {0.0f, 0.0f, 0.0f, 0.0f};
    m.update_delta(d2);
    m.hot_swap_module("w", std::vector<uint8_t>{0x10, 0x32});

    const size_t expected_count = m.edit_log().size();
    CHECK_EQ(expected_count, static_cast<size_t>(3));
    CHECK(m.edit_log().verify_chain());

    // Save + reload: edit log entry count must match exactly.
    const std::string path = "/tmp/lqt_edit_log_persist.lqt";
    m.save(path);
    LqtModel m2 = LqtModel::load(path);
    CHECK_EQ(m2.edit_log().size(), expected_count);
    CHECK(m2.edit_log().verify_chain());

    // Entry types must round-trip.
    CHECK_EQ(m2.edit_log().at(0).type, MutationType::CodebookEdit);
    CHECK_EQ(m2.edit_log().at(1).type, MutationType::DeltaUpdate);
    CHECK_EQ(m2.edit_log().at(2).type, MutationType::ModuleSwap);

    std::remove(path.c_str());
}

// ============================================================================
// EDIT LOG — tamper detection
// ============================================================================

TEST_CASE(model_edit_log_tamper_detection) {
    // Build an in-memory log via the same primitives the model layer uses,
    // serialize it, flip a single byte inside one entry's payload region,
    // re-parse and confirm verify_chain() returns false.
    EditLog log;
    const char p0[] = "alpha";
    const char p1[] = "beta";
    const char p2[] = "gamma";
    EditLogEntry e0 = make_entry(MutationType::CodebookEdit, "cb0", p0, sizeof(p0) - 1, 0, 1000);
    EditLogEntry e1 = make_entry(MutationType::DeltaUpdate,  "d0",  p1, sizeof(p1) - 1, e0.data_hash, 2000);
    EditLogEntry e2 = make_entry(MutationType::ModuleSwap,   "w",   p2, sizeof(p2) - 1, e1.data_hash, 3000);
    log.append(e0);
    log.append(e1);
    log.append(e2);
    CHECK(log.verify_chain());

    // Serialize, mutate a byte of entry[1]'s target, re-parse, verify_chain() must FAIL.
    ByteWriter w;
    log.serialize(w);
    ByteReader r(w.bytes());
    EditLog parsed = EditLog::parse(r);

    // Reconstruct with one entry whose target has been corrupted.
    EditLog tampered;
    tampered.append(parsed.at(0));
    {
        EditLogEntry bad = parsed.at(1);
        // Corrupt one target byte. data_hash was computed over the
        // original target bytes, so any change must break verify_chain().
        if (!bad.target.empty()) bad.target[0] = static_cast<char>(bad.target[0] ^ 0x01);
        tampered.append(bad);
    }
    tampered.append(parsed.at(2));

    CHECK(!tampered.verify_chain());
}

// ============================================================================
// AFFINE-ONLY RECONSTRUCTION — codebook_id == LQT_ID_NONE
// ============================================================================

TEST_CASE(model_affine_only_reconstruction) {
    // A tensor with codebook_id = LQT_ID_NONE (0xFFFF) must reconstruct via
    // affine dequantization: weight[i] = (q[i] - zero_point) * scale.
    LqtModel m;

    TensorDescriptor d;
    d.name          = "affine";
    d.tensor_type   = TensorType::Standard;
    d.dtype         = DType::INT8;
    d.shape         = {4};
    d.codebook_id   = LQT_ID_NONE;        // <-- no codebook
    d.delta_id      = LQT_ID_NONE;
    d.sparse_mask_id= LQT_ID_NONE;
    d.scale         = 0.5f;
    d.zero_point    = 10;
    // INT8 quantized values q = {10, 12, 14, 16}.
    // Expected reconstruct: (q - zero_point) * scale = {0, 1, 2, 3}.
    m.add_tensor(d, std::vector<uint8_t>{10, 12, 14, 16});

    // This MUST NOT throw — the codebook-less path is the next-patch contract.
    const std::vector<float> w = m.reconstruct("affine");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 0.0f, 1e-6);
    CHECK_NEAR(w[1], 1.0f, 1e-6);
    CHECK_NEAR(w[2], 2.0f, 1e-6);
    CHECK_NEAR(w[3], 3.0f, 1e-6);
}

// ============================================================================
// RTA RECONSTRUCTION PATH — TensorType::RecursiveTensor routes through RTA
// ============================================================================

TEST_CASE(model_rta_reconstruction_path) {
    LqtModel m;

    // Register an RTA block under a known name.
    RtaBlock blk = build_minimal_rta_block();
    blk.metadata.push_back({"role", "test"});
    m.add_rta_block("rt0", blk);

    // Add a TensorDescriptor whose tensor_type == RecursiveTensor and whose
    // name matches the RTA block. The patch contract routes reconstruct()
    // for recursive tensors through the A5 RTA path.
    TensorDescriptor d;
    d.name        = "rt0";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {1};
    d.codebook_id = LQT_ID_NONE;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0});

    // D-024: reconstruct() must return the real affine-dequantized value
    // (no codebook, no RecursiveWeight attached: q=0, scale=1.0, zero_point=0
    // -> 0.0), not the old dim_sizes-cycling placeholder.
    const std::vector<float> w = m.reconstruct("rt0");
    CHECK_EQ(w.size(), static_cast<size_t>(1));
    CHECK_NEAR(w[0], 0.0f, 1e-6f);

    // The RTA block must be retrievable by name.
    const RtaBlock* got = m.get_rta_block("rt0");
    CHECK(got != nullptr);
    CHECK_EQ(got->dims.rank, static_cast<uint8_t>(LQT_RTA_RANK));
}

// D-024: RecursiveTensor reconstruction where some lattice positions have an
// attached RecursiveWeight storage bucket (own B, own T, own Phi/epsilon)
// and others fall back to the tensor's own codebook-indexed base value.
// Weights are storage buckets, not tensors: a bucket's value overrides the
// structural base only at the one position its T resolves to.
TEST_CASE(model_rta_reconstruction_with_recursive_weight) {
    LqtModel m;

    Codebook cb(5, 4, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m.add_codebook(cb);

    RtaBlock blk = build_minimal_rta_block();
    blk.dims.dim_sizes[0] = 4;
    blk.sparse_encoding = SparseEncoding::Uniform;
    blk.sparse_payload = sparse_build_uniform(4);
    m.add_rta_block("rt1", blk);

    // Bucket at flat position 0: own base_index=3 (codebook[3]=4.0), own
    // epsilon mean 0.5 -> overrides the base value at position 0 with 4.5.
    RecursiveWeight bucket_a;
    bucket_a.base_index = 3;
    bucket_a.tensor_position = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    bucket_a.error = {0.5f};
    m.add_recursive_weight("rt1", bucket_a);

    // Bucket at flat position 2: own base_index=1 (codebook[1]=2.0), no
    // epsilon -> overrides the base value at position 2 with 2.0.
    RecursiveWeight bucket_b;
    bucket_b.base_index = 1;
    bucket_b.tensor_position = {2.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    m.add_recursive_weight("rt1", bucket_b);

    TensorDescriptor d;
    d.name        = "rt1";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {4};
    d.codebook_id = 5;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0, 1, 2, 3});

    // Base (no bucket) values from the tensor's own codebook indices
    // {0,1,2,3} -> {1,2,3,4}. Positions 0 and 2 are overridden by their
    // attached buckets; positions 1 and 3 keep the structural base value.
    const std::vector<float> w = m.reconstruct("rt1");
    CHECK_EQ(w.size(), static_cast<size_t>(4));
    CHECK_NEAR(w[0], 4.5f, 1e-6f); // bucket_a: codebook[3]*1.0 + 0 + mean({0.5})
    CHECK_NEAR(w[1], 2.0f, 1e-6f); // base: codebook[1]*1.0
    CHECK_NEAR(w[2], 2.0f, 1e-6f); // bucket_b: codebook[1]*1.0 + 0 + 0
    CHECK_NEAR(w[3], 4.0f, 1e-6f); // base: codebook[3]*1.0
}

// D-024: two RecursiveWeight buckets whose T resolves to the same lattice
// position is ambiguous -- no rule resolves it -- reconstruct() must throw.
TEST_CASE(model_rta_reconstruction_bounds_colliding_buckets) {
    LqtModel m;

    Codebook cb(6, 2, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    m.add_codebook(cb);

    RtaBlock blk = build_minimal_rta_block();
    blk.dims.dim_sizes[0] = 2;
    blk.sparse_payload = sparse_build_uniform(2);
    m.add_rta_block("rt5", blk);

    RecursiveWeight a;
    a.base_index = 0;
    a.tensor_position = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    m.add_recursive_weight("rt5", a);
    RecursiveWeight b;
    b.base_index = 1;
    b.tensor_position = {0.0f, 0.0f, 0.0f, 0.0f, 0.0f}; // same position as `a`
    m.add_recursive_weight("rt5", b);

    TensorDescriptor d;
    d.name        = "rt5";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {2};
    d.codebook_id = 6;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0, 1});

    CHECK_THROWS_AS(m.reconstruct("rt5"), FormatError);
}

// D-024: a RecursiveWeight bucket whose T does not map to a valid coordinate
// in the tensor's own dims must throw rather than silently drop the bucket.
TEST_CASE(model_rta_reconstruction_bounds_bucket_out_of_range) {
    LqtModel m;

    Codebook cb(7, 2, 1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    m.add_codebook(cb);

    RtaBlock blk = build_minimal_rta_block();
    blk.dims.dim_sizes[0] = 2;
    blk.sparse_payload = sparse_build_uniform(2);
    m.add_rta_block("rt6", blk);

    RecursiveWeight a;
    a.base_index = 0;
    a.tensor_position = {5.0f, 0.0f, 0.0f, 0.0f, 0.0f}; // dim_sizes[0] == 2
    m.add_recursive_weight("rt6", a);

    TensorDescriptor d;
    d.name        = "rt6";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {2};
    d.codebook_id = 7;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0, 1});

    CHECK_THROWS_AS(m.reconstruct("rt6"), FormatError);
}

// D-024: a RecursiveTensor whose RtaBlock carries RtaReference entries has no
// defined per-element binding for those references (no supplied spec
// resolves it) — reconstruct() must throw rather than fabricate a mapping.
TEST_CASE(model_rta_reconstruction_bounds_references) {
    LqtModel m;

    RtaBlock blk = build_minimal_rta_block();
    RtaReference ref;
    ref.kind = ReferenceKind::Direct;
    ref.target = 0;
    blk.references.push_back(ref);
    m.add_rta_block("rt2", blk);

    TensorDescriptor d;
    d.name        = "rt2";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {1};
    d.codebook_id = LQT_ID_NONE;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0});

    CHECK_THROWS_AS(m.reconstruct("rt2"), FormatError);
}

// D-024: PerDimension sparse encoding records only aggregate per-axis
// density, not exact element membership — reconstruct() must throw rather
// than guess a membership mask.
TEST_CASE(model_rta_reconstruction_bounds_per_dimension) {
    LqtModel m;

    RtaBlock blk = build_minimal_rta_block();
    blk.sparse_encoding = SparseEncoding::PerDimension;
    PerDimMap maps(LQT_RTA_RANK);
    maps[0].push_back({0, 1.0f});
    blk.sparse_payload = sparse_build_per_dimension(maps);
    m.add_rta_block("rt3", blk);

    TensorDescriptor d;
    d.name        = "rt3";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {1};
    d.codebook_id = LQT_ID_NONE;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0});

    CHECK_THROWS_AS(m.reconstruct("rt3"), FormatError);
}

// D-024: the new RecursiveWeightTable chunk (0x0011) must round-trip through
// serialize_to_bytes()/parse() byte-for-byte (quintuple survives save/load).
TEST_CASE(model_recursive_weight_table_roundtrip) {
    LqtModel m;

    RtaBlock blk = build_minimal_rta_block();
    m.add_rta_block("rt4", blk);

    RecursiveWeight rwv;
    rwv.base_index = 2;
    rwv.phase = {0.1f, 0.2f, 0.3f};
    rwv.r_k = 1;
    rwv.r_d = 2;
    rwv.reference = {1.0f, 2.0f, 3.0f, 4.0f};
    rwv.tensor_position = {1.0f, 2.0f, 3.0f, 4.0f, 5.0f};
    rwv.error = {0.05f};
    rwv.self_reference_coeff = 0.25f;
    m.add_recursive_weight("rt4", rwv);

    TensorDescriptor d;
    d.name        = "rt4";
    d.tensor_type = TensorType::RecursiveTensor;
    d.dtype       = DType::INT8;
    d.shape       = {1, 1, 1, 1, 1};
    d.codebook_id = LQT_ID_NONE;
    d.scale       = 1.0f;
    m.add_tensor(d, std::vector<uint8_t>{0});

    const std::vector<uint8_t> bytes = m.serialize_to_bytes();
    const LqtModel back = LqtModel::parse(bytes.data(), bytes.size());

    const std::vector<RecursiveWeight>* got = back.get_recursive_weights("rt4");
    CHECK(got != nullptr);
    CHECK_EQ(got->size(), static_cast<size_t>(1));
    const RecursiveWeight& bucket = (*got)[0];
    CHECK_EQ(bucket.base_index, 2u);
    CHECK_EQ(bucket.phase.size(), static_cast<size_t>(3));
    CHECK_NEAR(bucket.phase[0], 0.1f, 1e-6f);
    CHECK_NEAR(bucket.phase[1], 0.2f, 1e-6f);
    CHECK_NEAR(bucket.phase[2], 0.3f, 1e-6f);
    CHECK_EQ(bucket.r_k, 1u);
    CHECK_EQ(bucket.r_d, 2u);
    CHECK_EQ(bucket.reference.size(), static_cast<size_t>(4));
    CHECK_NEAR(bucket.reference[3], 4.0f, 1e-6f);
    CHECK_NEAR(bucket.tensor_position[4], 5.0f, 1e-6f);
    CHECK_EQ(bucket.error.size(), static_cast<size_t>(1));
    CHECK_NEAR(bucket.error[0], 0.05f, 1e-6f);
    CHECK_NEAR(bucket.self_reference_coeff, 0.25f, 1e-6f);
}

// ============================================================================
// MAIN
// ============================================================================

int main() { return lqttest::run_all(); }
