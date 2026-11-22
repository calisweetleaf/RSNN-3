// lqt/converters.h — Conversion utilities: GGUF -> LqtModel, ONNX -> LqtModel.
//
// These are stub implementations that handle the header/metadata parsing of
// each source format and produce a populated LqtModel with codebooks, descriptors,
// and tensor blobs. Full production converters would wire tensor data directly;
// these stubs produce correct skeletons.
#pragma once
#include <string>
#include <vector>
#include <cstdint>
#include "lqt/model.h"
#include "lqt/error.h"

namespace lqt {

// ========================= GGUF format support ===============================
// GGUF v3 magic: 0x46554747 ("GGUF" little-endian)
// Reference: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
inline constexpr uint32_t GGUF_MAGIC       = 0x46554747u;
inline constexpr uint32_t GGUF_VERSION_MIN = 2;
inline constexpr uint32_t GGUF_VERSION_MAX = 3;

struct GgufHeader {
    uint32_t magic;
    uint32_t version;
    uint64_t tensor_count;
    uint64_t kv_count;
    bool valid() const { return magic == GGUF_MAGIC && version >= GGUF_VERSION_MIN; }
};

// Convert a GGUF file to LqtModel.
// Reads tensor metadata and names; populates descriptors and affine codebooks.
// Actual weight bytes are copied verbatim into tensor blobs.
LqtModel from_gguf(const std::string& path);
LqtModel from_gguf(const uint8_t* data, size_t size);

// ========================= ONNX format support ===============================
// ONNX protobuf magic bytes: [0x08, 0x??, 0x12, ...]
// This stub reads the outer ModelProto envelope without a full protobuf runtime.

// Convert an ONNX model to LqtModel.
// Parses initializer names and shapes; populates descriptors.
// Weight bytes are copied as INT8 blobs; a scalar codebook is created per tensor.
LqtModel from_onnx(const std::string& path);
LqtModel from_onnx(const uint8_t* data, size_t size);

} // namespace lqt
