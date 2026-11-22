// tests/test_onnx_decoder.cpp — ONNX protobuf decoder tests (Patch 8).
//
// Builds minimal valid ONNX ModelProto binaries in memory (by hand-encoding
// the proto3 wire format) and verifies from_onnx() extracts tensors + metadata.
//
// Protobuf encoding helpers:
//   varint(v): each byte holds 7 bits; MSB=1 signals continuation.
//   tag(field, wtype): (field << 3) | wtype.
//     wire type 0 = varint, 2 = length-delimited.

#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <unistd.h>

#include "lqt/converters.h"
#include "lqt/error.h"
#include "lqt/model.h"
#include "test_framework.h"

using namespace lqt;
using namespace lqttest;

// ── Proto3 binary builder ─────────────────────────────────────────────────────

struct OnnxBuilder {
    std::vector<uint8_t> buf;

    // Encode a varint.
    void put_varint(uint64_t v) {
        do {
            uint8_t byte = static_cast<uint8_t>(v & 0x7Fu);
            v >>= 7;
            if (v) byte |= 0x80u;
            buf.push_back(byte);
        } while (v);
    }

    // Encode a tag: (field_number << 3) | wire_type.
    void put_tag(uint32_t field, uint8_t wtype) {
        put_varint(static_cast<uint64_t>((field << 3) | wtype));
    }

    // Encode a length-delimited blob (wire type 2).
    void put_len_delim(uint32_t field, const std::vector<uint8_t>& payload) {
        put_tag(field, 2);
        put_varint(payload.size());
        buf.insert(buf.end(), payload.begin(), payload.end());
    }

    // Encode a length-delimited string.
    void put_string(uint32_t field, const std::string& s) {
        put_tag(field, 2);
        put_varint(s.size());
        buf.insert(buf.end(), s.begin(), s.end());
    }

    // Encode a raw bytes field.
    void put_bytes_field(uint32_t field, const void* data, size_t n) {
        put_tag(field, 2);
        put_varint(n);
        const auto* p = static_cast<const uint8_t*>(data);
        buf.insert(buf.end(), p, p + n);
    }

    // Encode a varint field.
    void put_varint_field(uint32_t field, uint64_t val) {
        put_tag(field, 0);
        put_varint(val);
    }

    const std::vector<uint8_t>& bytes() const { return buf; }
};

// Build a TensorProto: name + dims + data_type + raw_data.
static std::vector<uint8_t> make_tensor_proto(const std::string& name,
                                               const std::vector<int64_t>& dims,
                                               int32_t data_type,
                                               const void* raw, size_t raw_size) {
    OnnxBuilder t;
    // field 1 = dims (repeated int64 varint)
    for (int64_t d : dims) t.put_varint_field(1, static_cast<uint64_t>(d));
    // field 2 = data_type
    t.put_varint_field(2, static_cast<uint64_t>(data_type));
    // field 8 = name
    t.put_string(8, name);
    // field 9 = raw_data
    if (raw && raw_size > 0) t.put_bytes_field(9, raw, raw_size);
    return t.bytes();
}

// Build a GraphProto containing the given TensorProto initializers.
static std::vector<uint8_t> make_graph_proto(
    const std::vector<std::vector<uint8_t>>& tensors) {
    OnnxBuilder g;
    for (const auto& t : tensors)
        g.put_len_delim(4, t); // field 4 = initializer
    return g.bytes();
}

// Build a ModelProto wrapping a graph.
static std::vector<uint8_t> make_model_proto(
    const std::vector<uint8_t>& graph,
    uint64_t ir_version = 6,
    uint64_t opset_version = 17) {
    OnnxBuilder m;
    m.put_varint_field(1, ir_version); // field 1 = ir_version
    // opset_import: OperatorSetIdProto (field 2), contains version (field 2)
    OnnxBuilder opset;
    opset.put_varint_field(2, opset_version);
    m.put_len_delim(2, opset.bytes());
    // graph: field 7
    m.put_len_delim(7, graph);
    return m.bytes();
}

// ── Tests ─────────────────────────────────────────────────────────────────────

TEST_CASE(onnx_bad_first_byte_throws) {
    std::vector<uint8_t> buf = {0xFF, 0x00};
    CHECK_THROWS_AS(from_onnx(buf.data(), buf.size()), FormatError);
}

TEST_CASE(onnx_empty_buffer_throws) {
    CHECK_THROWS_AS(from_onnx(nullptr, 0), FormatError);
}

TEST_CASE(onnx_f32_tensor_extracted) {
    // One FLOAT tensor "weight", shape [4], raw_data = {1,2,3,4} as f32.
    float raw[4] = {1.0f, 2.0f, 3.0f, 4.0f};
    auto tensor  = make_tensor_proto("weight", {4}, 1, raw, 16);
    auto graph   = make_graph_proto({tensor});
    auto model_buf = make_model_proto(graph);

    LqtModel model = from_onnx(model_buf.data(), model_buf.size());

    CHECK_EQ(model.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = model.find_tensor("weight");
    CHECK_MSG(tb != nullptr, "tensor 'weight' not found");
    CHECK_EQ(tb->desc.dtype, DType::FP32);
    CHECK_EQ(tb->desc.shape.size(), static_cast<size_t>(1));
    CHECK_EQ(tb->desc.shape[0], 4u);

    // Verify real bytes round-tripped.
    float got[4];
    std::memcpy(got, tb->indices.data(), 16);
    CHECK_NEAR(got[0], 1.0f, 1e-6);
    CHECK_NEAR(got[3], 4.0f, 1e-6);
}

TEST_CASE(onnx_multiple_tensors_extracted) {
    float w1[2] = {10.0f, 20.0f};
    float w2[3] = {1.0f, 2.0f, 3.0f};
    auto t1 = make_tensor_proto("embed", {2}, 1, w1, 8);
    auto t2 = make_tensor_proto("proj",  {3}, 1, w2, 12);
    auto graph = make_graph_proto({t1, t2});
    auto buf   = make_model_proto(graph);

    LqtModel model = from_onnx(buf.data(), buf.size());
    CHECK_EQ(model.tensors().size(), static_cast<size_t>(2));
    CHECK_MSG(model.find_tensor("embed") != nullptr, "tensor 'embed' missing");
    CHECK_MSG(model.find_tensor("proj")  != nullptr, "tensor 'proj' missing");
}

TEST_CASE(onnx_int8_dtype_mapped) {
    int8_t raw[4] = {-1, 0, 1, 2};
    auto t     = make_tensor_proto("q_weight", {4}, 3 /* INT8 */, raw, 4);
    auto graph = make_graph_proto({t});
    auto buf   = make_model_proto(graph);

    LqtModel model = from_onnx(buf.data(), buf.size());
    CHECK_EQ(model.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = model.find_tensor("q_weight");
    CHECK_MSG(tb != nullptr, "tensor 'q_weight' missing");
    CHECK_EQ(tb->desc.dtype, DType::INT8);
}

TEST_CASE(onnx_opset_version_as_hyperparam) {
    auto graph = make_graph_proto({});           // empty graph
    auto buf   = make_model_proto(graph, 6, 17); // ir=6, opset=17

    LqtModel model = from_onnx(buf.data(), buf.size());
    bool found = false;
    for (const auto& hp : model.hyperparams()) {
        if (hp.first == "onnx_opset") {
            CHECK_NEAR(hp.second, 17.0f, 0.5f);
            found = true;
        }
    }
    CHECK_MSG(found, "hyperparam 'onnx_opset' not found");
}

TEST_CASE(onnx_2d_shape_extracted) {
    float w[6] = {1,2,3,4,5,6};
    auto t   = make_tensor_proto("mat", {2, 3}, 1, w, 24);
    auto g   = make_graph_proto({t});
    auto buf = make_model_proto(g);

    LqtModel model = from_onnx(buf.data(), buf.size());
    const TensorBlob* tb = model.find_tensor("mat");
    CHECK_MSG(tb != nullptr, "tensor 'mat' missing");
    CHECK_EQ(tb->desc.shape.size(), static_cast<size_t>(2));
    CHECK_EQ(tb->desc.shape[0], 2u);
    CHECK_EQ(tb->desc.shape[1], 3u);
}

TEST_CASE(onnx_save_reload_roundtrip) {
    float raw[4] = {5.0f, 6.0f, 7.0f, 8.0f};
    auto buf = make_model_proto(make_graph_proto({
        make_tensor_proto("w", {4}, 1, raw, 16)
    }));
    LqtModel model = from_onnx(buf.data(), buf.size());

    char tmp[] = "/tmp/lqt_onnx_rt_XXXXXX";
    int fd = mkstemp(tmp); if (fd >= 0) ::close(fd);
    model.save(tmp);
    LqtModel loaded = LqtModel::load(tmp);
    ::unlink(tmp);

    CHECK_EQ(loaded.tensors().size(), static_cast<size_t>(1));
    const TensorBlob* tb = loaded.find_tensor("w");
    CHECK_MSG(tb != nullptr, "tensor 'w' survived save/reload");
    float got[4]; std::memcpy(got, tb->indices.data(), 16);
    CHECK_NEAR(got[0], 5.0f, 1e-6);
}

int main() { return lqttest::run_all(); }
