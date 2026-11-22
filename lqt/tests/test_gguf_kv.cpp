// tests/test_gguf_kv.cpp — GGUF KV metadata extraction tests (Patch 7).
//
// Verifies that the from_gguf() converter populates LqtModel hyperparams
// and module_graph_json from the GGUF key-value metadata section.

#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

#include "lqt/converters.h"
#include "lqt/error.h"
#include "lqt/model.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqttest;

// ── Minimal GGUF binary builder ───────────────────────────────────────────────

struct KvGgufBuilder {
    std::vector<uint8_t> buf;
    uint64_t kv_count = 0;
    uint64_t tensor_count = 0;

    void put_u8(uint8_t v)   { buf.push_back(v); }
    void put_u32(uint32_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(), p, p+4); }
    void put_u64(uint64_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(), p, p+8); }
    void put_f32(float v)    { const auto* p = reinterpret_cast<const uint8_t*>(&v); buf.insert(buf.end(), p, p+4); }
    void put_gguf_str(const std::string& s) {
        uint64_t n = s.size(); put_u64(n);
        buf.insert(buf.end(), s.begin(), s.end());
    }
    void pad_to(size_t a) { while (buf.size() % a) buf.push_back(0); }

    void add_kv_u32(const std::string& key, uint32_t val) {
        put_gguf_str(key);
        put_u32(4); // GgufValueType::UINT32 = 4
        put_u32(val);
        ++kv_count;
    }
    void add_kv_string(const std::string& key, const std::string& val) {
        put_gguf_str(key);
        put_u32(8); // GgufValueType::STRING = 8
        put_gguf_str(val);
        ++kv_count;
    }

    // Finalize: write header (backpatch counts) + optional one F32 tensor.
    std::vector<uint8_t> finalize(bool add_tensor = true) {
        // Build header prefix (24 bytes: magic/ver/tensor_count/kv_count)
        std::vector<uint8_t> hdr;
        auto append32 = [&](uint32_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); hdr.insert(hdr.end(), p, p+4); };
        auto append64 = [&](uint64_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); hdr.insert(hdr.end(), p, p+8); };
        append32(0x46554747u); // GGUF magic
        append32(3);           // version 3
        append64(add_tensor ? 1ULL : 0ULL); // tensor_count
        append64(kv_count);

        // Assemble: header + KV blob + tensor info + padding + tensor data
        std::vector<uint8_t> full;
        full.insert(full.end(), hdr.begin(), hdr.end());
        full.insert(full.end(), buf.begin(), buf.end());

        if (add_tensor) {
            // Tensor info: name="t0", ndim=1, shape=[4], type=F32=0, offset=0
            auto put32 = [&](uint32_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); full.insert(full.end(), p, p+4); };
            auto put64 = [&](uint64_t v) { const auto* p = reinterpret_cast<const uint8_t*>(&v); full.insert(full.end(), p, p+8); };
            // name: gguf string "t0"
            uint64_t nlen = 2; const auto* pp = reinterpret_cast<const uint8_t*>(&nlen);
            full.insert(full.end(), pp, pp+8);
            full.push_back('t'); full.push_back('0');
            put32(1);  // ndim
            put32(4);  // shape[0]
            put32(0);  // ggml_type F32
            put64(0);  // offset

            // Pad to 32-byte alignment
            while (full.size() % 32) full.push_back(0);

            // Tensor data: 4 x f32 = {1,2,3,4}
            float vals[4] = {1.f, 2.f, 3.f, 4.f};
            const auto* vp = reinterpret_cast<const uint8_t*>(vals);
            full.insert(full.end(), vp, vp + 16);
        }
        return full;
    }
};

// ── Tests ─────────────────────────────────────────────────────────────────────

TEST_CASE(gguf_kv_context_length_extracted) {
    KvGgufBuilder g;
    g.add_kv_u32("llama.context_length", 4096);
    auto gguf = g.finalize(true);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    bool found = false;
    for (const auto& hp : model.hyperparams()) {
        if (hp.first == "context_length") {
            CHECK_NEAR(hp.second, 4096.0f, 0.5f);
            found = true;
        }
    }
    CHECK_MSG(found, "hyperparam 'context_length' not found after from_gguf");
}

TEST_CASE(gguf_kv_embedding_length_extracted) {
    KvGgufBuilder g;
    g.add_kv_u32("llama.embedding_length", 512);
    auto gguf = g.finalize(true);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    bool found = false;
    for (const auto& hp : model.hyperparams()) {
        if (hp.first == "embedding_length") {
            CHECK_NEAR(hp.second, 512.0f, 0.5f);
            found = true;
        }
    }
    CHECK_MSG(found, "hyperparam 'embedding_length' not found");
}

TEST_CASE(gguf_kv_architecture_sets_module_graph) {
    KvGgufBuilder g;
    g.add_kv_string("general.architecture", "llama");
    auto gguf = g.finalize(true);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const std::string& mj = model.module_graph_json();
    CHECK_MSG(!mj.empty(), "module_graph_json is empty after from_gguf with architecture KV");
    CHECK_MSG(mj.find("llama") != std::string::npos,
              "architecture 'llama' not found in module_graph_json");
}

TEST_CASE(gguf_kv_general_name_captured) {
    KvGgufBuilder g;
    g.add_kv_string("general.name", "test-model");
    auto gguf = g.finalize(true);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    const std::string& mj = model.module_graph_json();
    CHECK_MSG(!mj.empty(), "module_graph_json empty after general.name KV");
    CHECK_MSG(mj.find("test-model") != std::string::npos,
              "model name 'test-model' not found in module_graph_json");
}

TEST_CASE(gguf_no_kv_still_loads) {
    KvGgufBuilder g;
    // No KV pairs added — kv_count stays 0
    auto gguf = g.finalize(true);

    LqtModel model = from_gguf(gguf.data(), gguf.size());
    CHECK_EQ(model.tensors().size(), static_cast<size_t>(1));
}

int main() { return lqttest::run_all(); }
