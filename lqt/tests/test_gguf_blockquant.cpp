// tests/test_gguf_blockquant.cpp — Block-quantized GGUF scale extraction (Patch 9).
//
// Verifies that from_gguf() correctly extracts per-block FP16 scales from
// Q4_0 and Q8_0 tensors, storing the mean scale in desc.scale so that
// LqtModel::reconstruct() can produce approximate float values.

#include <cstdint>
#include <cstring>
#include <cmath>
#include <string>
#include <vector>

#include "lqt/converters.h"
#include "lqt/fp16.h"
#include "lqt/model.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqttest;

// ── GGUF binary builder (copied from test_gguf_converter.cpp) ─────────────────

struct BqGgufBuilder {
    std::vector<uint8_t> buf;
    void put_u32(uint32_t v){ const auto* p=reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(),p,p+4); }
    void put_u64(uint64_t v){ const auto* p=reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(),p,p+8); }
    void put_u16(uint16_t v){ const auto* p=reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(),p,p+2); }
    void put_gguf_str(const std::string& s){ put_u64(s.size()); buf.insert(buf.end(),s.begin(),s.end()); }
    void pad_to(size_t a){ while(buf.size()%a) buf.push_back(0); }
    void put_bytes(const void* d, size_t n){ const auto* p=static_cast<const uint8_t*>(d); buf.insert(buf.end(),p,p+n); }
};

// Build one Q4_0 block: [fp16_scale : 2 bytes][nibbles : 16 bytes]
// Elements encode nibbles 0..15 (two elements per byte, low nibble first, D-007).
static std::vector<uint8_t> make_q4_0_block(float scale, uint8_t nibble_fill = 0x07) {
    std::vector<uint8_t> blk(18, 0);
    const uint16_t fp16 = lqt::fp32_to_fp16(scale);
    std::memcpy(blk.data(), &fp16, 2);
    // Fill 16 nibble bytes with nibble_fill in both nibbles.
    for (int i = 2; i < 18; ++i) blk[i] = static_cast<uint8_t>((nibble_fill & 0xF) | ((nibble_fill & 0xF) << 4));
    return blk;
}

// Build one Q8_0 block: [fp16_scale : 2 bytes][int8 * 32]
static std::vector<uint8_t> make_q8_0_block(float scale, int8_t int8_fill = 10) {
    std::vector<uint8_t> blk(34, 0);
    const uint16_t fp16 = lqt::fp32_to_fp16(scale);
    std::memcpy(blk.data(), &fp16, 2);
    std::memset(blk.data() + 2, static_cast<uint8_t>(int8_fill), 32);
    return blk;
}

// Assemble a GGUF file with one tensor of the given block-quant type.
static std::vector<uint8_t> make_block_quant_gguf(
    uint32_t gguf_type, const std::vector<uint8_t>& tensor_data,
    uint32_t shape_dim)
{
    BqGgufBuilder g;
    // Header: magic, version, tensor_count=1, kv_count=0
    g.put_u32(0x46554747u);
    g.put_u32(3);
    g.put_u64(1);
    g.put_u64(0);
    // Tensor info: name="w", ndim=1, shape=[shape_dim], gguf_type, offset=0
    g.put_gguf_str("w");
    g.put_u32(1);          // ndim
    g.put_u32(shape_dim);  // shape[0]
    g.put_u32(gguf_type);
    g.put_u64(0);          // offset in data region
    // Pad to 32-byte alignment for data region
    g.pad_to(32);
    // Tensor data
    g.put_bytes(tensor_data.data(), tensor_data.size());
    return g.buf;
}

// ── Tests ─────────────────────────────────────────────────────────────────────

TEST_CASE(gguf_q4_0_scale_extracted_single_block) {
    // One Q4_0 block (32 elements), scale = 0.5f.
    const float expected_scale = 0.5f;
    auto block = make_q4_0_block(expected_scale, 7);
    auto gguf  = make_block_quant_gguf(2, block, 32);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    CHECK_EQ(model.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = model.find_tensor("w");
    CHECK_MSG(tb != nullptr, "tensor 'w' not found");
    CHECK_EQ(tb->desc.dtype, DType::INT4);
    // Mean scale should be close to expected_scale.
    CHECK_NEAR(tb->desc.scale, expected_scale, 0.01f);
    // Index bytes should be 16 bytes (just the nibbles, no scale header).
    CHECK(tb->indices.size() >= 16u);
}

TEST_CASE(gguf_q8_0_scale_extracted_single_block) {
    const float expected_scale = 0.25f;
    auto block = make_q8_0_block(expected_scale, 5);
    auto gguf  = make_block_quant_gguf(8, block, 32);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const TensorBlob* tb = model.find_tensor("w");
    CHECK_MSG(tb != nullptr, "tensor 'w' not found");
    CHECK_EQ(tb->desc.dtype, DType::INT8);
    CHECK_NEAR(tb->desc.scale, expected_scale, 0.01f);
    // 32 int8 bytes (no 2-byte scale header).
    CHECK(tb->indices.size() >= 32u);
}

TEST_CASE(gguf_q4_0_mean_scale_two_blocks) {
    // Two Q4_0 blocks with different scales: mean should be average.
    auto blk0 = make_q4_0_block(0.4f, 8);
    auto blk1 = make_q4_0_block(0.6f, 4);
    std::vector<uint8_t> data(blk0.begin(), blk0.end());
    data.insert(data.end(), blk1.begin(), blk1.end()); // 36 bytes, 64 elements
    auto gguf = make_block_quant_gguf(2, data, 64);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const TensorBlob* tb = model.find_tensor("w");
    CHECK_MSG(tb != nullptr, "tensor 'w' not found");
    // Mean of 0.4 and 0.6 = 0.5.
    CHECK_NEAR(tb->desc.scale, 0.5f, 0.02f);
    // Two blocks × 16 nibble bytes = 32 bytes (no scale headers).
    CHECK(tb->indices.size() >= 32u);
}

TEST_CASE(gguf_q8_0_scale_preserves_codebook_entry) {
    // The mean scale should also be stored as cb.scalar(1).
    const float expected_scale = 0.125f;
    auto block = make_q8_0_block(expected_scale, 10);
    auto gguf  = make_block_quant_gguf(8, block, 32);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const TensorBlob* tb = model.find_tensor("w");
    CHECK_MSG(tb != nullptr, "tensor 'w' missing");
    const Codebook* cb = model.codebook(tb->desc.codebook_id);
    CHECK_MSG(cb != nullptr, "codebook missing");
    // Codebook entry 1 holds the mean scale.
    CHECK_NEAR(cb->scalar(1), expected_scale, 0.01f);
}

TEST_CASE(gguf_f32_tensor_unaffected) {
    // F32 tensors (gguf_type=0) should still work unchanged.
    float raw[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    std::vector<uint8_t> data(16);
    std::memcpy(data.data(), raw, 16);
    auto gguf = make_block_quant_gguf(0, data, 4);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const TensorBlob* tb = model.find_tensor("w");
    CHECK_MSG(tb != nullptr, "F32 tensor missing");
    CHECK_EQ(tb->desc.dtype, DType::FP32);
    CHECK_NEAR(tb->desc.scale, 1.0f, 1e-6f); // non-block type → scale stays 1.0
    float got[4]; std::memcpy(got, tb->indices.data(), 16);
    CHECK_NEAR(got[0], 1.0f, 1e-6f);
    CHECK_NEAR(got[3], 4.0f, 1e-6f);
}

int main() { return lqttest::run_all(); }
