// tests/test_gguf_converter.cpp — GGUF converter integration tests (Patch 6).
//
// Builds minimal valid GGUF v3 binaries in-memory and verifies from_gguf()
// produces a loadable LqtModel with real weight bytes — not zero-filled stubs.
//
// GGUF wire format (v3, little-endian):
//   [magic:u32][version:u32][tensor_count:u64][kv_count:u64]
//   { [key:gguf_str][vtype:u32][value...] } * kv_count
//   { [name:gguf_str][ndim:u32][dims:u32*ndim][gguf_type:u32][offset:u64] } * tensor_count
//   [padding to alignment boundary]
//   [tensor data blobs in declaration order]

#include <cstdint>
#include <cstring>
#include <string>
#include <unistd.h>
#include <vector>

#include "lqt/converters.h"
#include "lqt/error.h"
#include "lqt/model.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqttest;

// ── Tiny GGUF binary builder ──────────────────────────────────────────────────

struct GgufBuilder {
    std::vector<uint8_t> buf;

    void put_u8 (uint8_t  v) { buf.push_back(v); }
    void put_u16(uint16_t v) { put_bytes(&v, 2); }
    void put_u32(uint32_t v) { put_bytes(&v, 4); }
    void put_u64(uint64_t v) { put_bytes(&v, 8); }
    void put_f32(float    v) { put_bytes(&v, 4); }

    void put_bytes(const void* p, size_t n) {
        const auto* src = static_cast<const uint8_t*>(p);
        buf.insert(buf.end(), src, src + n);
    }

    // GGUF-style length-prefixed string
    void put_gguf_str(const std::string& s) {
        put_u64(static_cast<uint64_t>(s.size()));
        put_bytes(s.data(), s.size());
    }

    // Pad to `align` boundary
    void pad_to(size_t align) {
        while (buf.size() % align != 0) buf.push_back(0);
    }

    size_t size() const { return buf.size(); }
    void patch_u64(size_t pos, uint64_t v) {
        std::memcpy(buf.data() + pos, &v, 8);
    }
};

// Build a minimal GGUF v3 file:
//   - one F32 tensor (name="weight.0", shape={4})
//   - real weight bytes = {1.0f, 2.0f, 3.0f, 4.0f}
//   - no KV metadata (kv_count=0)
//   - alignment=32 (GGUF default, stored as KV)
static std::vector<uint8_t> make_minimal_gguf_f32() {
    GgufBuilder g;

    // Header
    g.put_u32(0x46554747u); // magic "GGUF"
    g.put_u32(3);            // version 3
    g.put_u64(1);            // tensor_count = 1
    g.put_u64(1);            // kv_count = 1 (we add general.alignment)

    // KV: "general.alignment" = 32 (UINT32 = 4)
    g.put_gguf_str("general.alignment");
    g.put_u32(4); // GgufValueType::UINT32
    g.put_u32(32);

    // Tensor info: name, ndim=1, shape=[4], gguf_type=0 (F32), offset=0
    g.put_gguf_str("weight.0");
    g.put_u32(1);  // ndim
    g.put_u32(4);  // shape[0] = 4
    g.put_u32(0);  // gguf_type = GGML_TYPE_F32
    g.put_u64(0);  // offset within data region = 0

    // Pad to 32-byte alignment (data region starts here)
    g.pad_to(32);

    // Tensor data: 4 x f32 = {1.0f, 2.0f, 3.0f, 4.0f}
    g.put_f32(1.0f);
    g.put_f32(2.0f);
    g.put_f32(3.0f);
    g.put_f32(4.0f);

    return g.buf;
}

// Build a GGUF with two tensors: F16 and Q4_0, no KV metadata
static std::vector<uint8_t> make_two_tensor_gguf() {
    GgufBuilder g;

    // Header: 2 tensors, 0 KV pairs
    g.put_u32(0x46554747u);
    g.put_u32(3);
    g.put_u64(2);   // tensor_count
    g.put_u64(0);   // kv_count

    // Tensor 0: F16, shape=[2], offset=0  → 2 * 2 = 4 bytes
    g.put_gguf_str("emb");
    g.put_u32(1);  // ndim=1
    g.put_u32(2);  // shape=[2]
    g.put_u32(1);  // F16
    g.put_u64(0);  // offset=0

    // Tensor 1: Q4_0, shape=[32], offset=4 (right after 4 bytes of F16)
    // Q4_0 block spec: 18 bytes per 32 elements → 1 block = 18 bytes
    g.put_gguf_str("mlp");
    g.put_u32(1);  // ndim=1
    g.put_u32(32); // shape=[32]
    g.put_u32(2);  // Q4_0
    g.put_u64(4);  // offset=4 (after the F16 blob)

    // Pad to alignment 32 (default, no KV override)
    g.pad_to(32);

    // Tensor 0 data: 2 x f16 = {0x3C00, 0x4000} = {1.0f, 2.0f} in f16
    uint16_t f16_1 = 0x3C00u; // 1.0 in IEEE 754 half-precision
    uint16_t f16_2 = 0x4000u; // 2.0 in f16
    g.put_u16(f16_1);
    g.put_u16(f16_2);

    // Tensor 1 data: 1 Q4_0 block = 18 bytes (pattern: non-zero)
    for (int i = 0; i < 18; ++i) g.put_u8(static_cast<uint8_t>(i + 1));

    return g.buf;
}

// ── Tests ─────────────────────────────────────────────────────────────────────

TEST_CASE(gguf_bad_magic_throws) {
    std::vector<uint8_t> buf = {0xDE, 0xAD, 0xBE, 0xEF, 0x03, 0x00, 0x00, 0x00};
    buf.resize(32, 0);
    CHECK_THROWS_AS(from_gguf(buf.data(), buf.size()), FormatError);
}

TEST_CASE(gguf_too_small_throws) {
    std::vector<uint8_t> buf = {0x47, 0x47, 0x55, 0x46}; // magic only
    CHECK_THROWS_AS(from_gguf(buf.data(), buf.size()), FormatError);
}

TEST_CASE(gguf_f32_tensor_real_bytes_loaded) {
    const auto gguf = make_minimal_gguf_f32();
    LqtModel model = from_gguf(gguf.data(), gguf.size());

    // One tensor must be present
    CHECK_EQ(model.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = model.find_tensor("weight.0");
    CHECK_MSG(tb != nullptr, "tensor 'weight.0' not found after from_gguf");

    // Shape and dtype
    CHECK_EQ(tb->desc.shape.size(), static_cast<size_t>(1));
    CHECK_EQ(tb->desc.shape[0], 4u);
    CHECK_EQ(tb->desc.dtype, DType::FP32);

    // The index blob must contain the REAL bytes {1.0f, 2.0f, 3.0f, 4.0f}
    // (not zeros — that's the whole point of Patch 6).
    CHECK(tb->indices.size() >= 16u); // 4 * 4 bytes, padded to 16
    float vals[4];
    std::memcpy(vals, tb->indices.data(), 16);
    CHECK_NEAR(vals[0], 1.0f, 1e-6);
    CHECK_NEAR(vals[1], 2.0f, 1e-6);
    CHECK_NEAR(vals[2], 3.0f, 1e-6);
    CHECK_NEAR(vals[3], 4.0f, 1e-6);
}

TEST_CASE(gguf_two_tensors_correct_dtypes) {
    const auto gguf = make_two_tensor_gguf();
    LqtModel model = from_gguf(gguf.data(), gguf.size());

    CHECK_EQ(model.tensors().size(), static_cast<size_t>(2));

    const TensorBlob* emb = model.find_tensor("emb");
    CHECK_MSG(emb != nullptr, "tensor 'emb' not found");
    CHECK_EQ(emb->desc.dtype, DType::FP16);
    CHECK(emb->indices.size() >= 4u); // 2 * 2 bytes

    const TensorBlob* mlp = model.find_tensor("mlp");
    CHECK_MSG(mlp != nullptr, "tensor 'mlp' not found");
    CHECK_EQ(mlp->desc.dtype, DType::INT4);
    // After block-scale extraction (Patch 9), the 2-byte fp16 scale header is
    // stripped; only the 16 nibble bytes per block are kept in index_bytes.
    CHECK(mlp->indices.size() >= 16u); // 1 Q4_0 block = 16 nibble bytes (scale extracted)
}

TEST_CASE(gguf_f16_real_bytes) {
    // Verify the F16 tensor has the exact bytes we wrote (0x3C00 = 1.0f16)
    const auto gguf = make_two_tensor_gguf();
    LqtModel model = from_gguf(gguf.data(), gguf.size());

    const TensorBlob* emb = model.find_tensor("emb");
    CHECK_MSG(emb != nullptr, "tensor 'emb' not found");
    uint16_t f16_0, f16_1;
    std::memcpy(&f16_0, emb->indices.data() + 0, 2);
    std::memcpy(&f16_1, emb->indices.data() + 2, 2);
    CHECK_EQ(f16_0, static_cast<uint16_t>(0x3C00)); // 1.0 in f16
    CHECK_EQ(f16_1, static_cast<uint16_t>(0x4000)); // 2.0 in f16
}

TEST_CASE(gguf_q4_block_bytes_nonzero) {
    // Q4_0 block: after scale extraction the scale header (2 bytes) is stripped.
    // The remaining 16 nibble bytes came from positions 2..17 of the original
    // GGUF block which was filled with bytes 1..18 (all non-zero).
    const auto gguf = make_two_tensor_gguf();
    LqtModel model = from_gguf(gguf.data(), gguf.size());

    const TensorBlob* mlp = model.find_tensor("mlp");
    CHECK_MSG(mlp != nullptr, "tensor 'mlp' not found");
    // After extraction: 16 nibble bytes (scale header stripped). All should be non-zero.
    bool all_nonzero = true;
    for (int i = 0; i < 16; ++i) {
        if (mlp->indices[i] == 0) { all_nonzero = false; break; }
    }
    CHECK_MSG(all_nonzero, "Q4_0 nibble bytes should be non-zero (scale header stripped)");
    // Verify the mean scale was extracted and stored correctly (non-zero, finite).
    CHECK(mlp->desc.scale > 0.0f);
    CHECK(std::isfinite(mlp->desc.scale));
}

TEST_CASE(gguf_model_save_reload_roundtrip) {
    // Build a GGUF, convert to LqtModel, save to .lqt, reload — verify byte match.
    const auto gguf = make_minimal_gguf_f32();
    LqtModel model = from_gguf(gguf.data(), gguf.size());

    char tmp[] = "/tmp/lqt_gguf_rt_XXXXXX";
    int fd = mkstemp(tmp);
    if (fd >= 0) ::close(fd);

    model.save(tmp);
    LqtModel loaded = LqtModel::load(tmp);
    ::unlink(tmp);

    CHECK_EQ(loaded.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = loaded.find_tensor("weight.0");
    CHECK_MSG(tb != nullptr, "tensor survived save/reload");

    float vals[4];
    std::memcpy(vals, tb->indices.data(), 16);
    CHECK_NEAR(vals[0], 1.0f, 1e-6);
    CHECK_NEAR(vals[3], 4.0f, 1e-6);
}

int main() { return lqttest::run_all(); }
