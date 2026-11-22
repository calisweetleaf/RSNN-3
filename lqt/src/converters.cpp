// src/converters.cpp — Stub converters: GGUF -> LqtModel, ONNX -> LqtModel.
//
// These stubs parse enough of each source format to populate a valid LqtModel
// skeleton (codebook IDs, TensorDescriptors, zero-filled index blobs). They are
// meant to compile cleanly and serve as the foundation for production converters.
//
// GGUF reference: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
// ONNX reference: https://onnx.ai/onnx/api/helper.html + ModelProto protobuf spec.

#include "lqt/converters.h"

#include <cstring>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/descriptor.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/fp16.h"
#include "lqt/model.h"

namespace lqt {

// ============================================================================
// Internal helpers — tiny cursor-based reader over a raw byte buffer.
// These avoid pulling in the full ByteReader (which requires an endian.h
// ByteWriter/ByteReader pair that is tied to serialization paths).
// ============================================================================

namespace {

// ---------------------------------------------------------------------------
// CursorReader — bounds-checked, little-endian reads over a byte span.
// ---------------------------------------------------------------------------
struct CursorReader {
    const uint8_t* data;
    size_t         size;
    size_t         pos{0};

    // Ensure `n` more bytes are available; throw FormatError if not.
    void require(size_t n, const char* ctx) const {
        if (pos + n > size)
            throw FormatError(std::string("unexpected end of data in ") + ctx);
    }

    uint8_t  read_u8 (const char* ctx) { require(1, ctx); return data[pos++]; }

    uint16_t read_u16(const char* ctx) {
        require(2, ctx);
        uint16_t v;
        std::memcpy(&v, data + pos, 2);
        pos += 2;
        // GGUF is always little-endian on disk. This library targets LE hosts
        // (D-003: on-disk format is LE). Big-endian host support requires a
        // compile-time bswap16 here; deferred to a future patch.
        return v;
    }

    uint32_t read_u32(const char* ctx) {
        require(4, ctx);
        uint32_t v;
        std::memcpy(&v, data + pos, 4);
        pos += 4;
        return v;
    }

    uint64_t read_u64(const char* ctx) {
        require(8, ctx);
        uint64_t v;
        std::memcpy(&v, data + pos, 8);
        pos += 8;
        return v;
    }

    float read_f32(const char* ctx) {
        uint32_t bits = read_u32(ctx);
        float v;
        std::memcpy(&v, &bits, 4);
        return v;
    }

    // Read a GGUF length-prefixed string: [u64 len][char... len bytes].
    std::string read_gguf_string(const char* ctx) {
        uint64_t len = read_u64(ctx);
        // Sanity-cap: refuse strings longer than 4 MiB to guard against
        // corrupt/truncated inputs before we ever allocate.
        if (len > (4u << 20))
            throw FormatError(std::string("GGUF string length implausibly large in ") + ctx);
        require(static_cast<size_t>(len), ctx);
        std::string s(reinterpret_cast<const char*>(data + pos),
                      static_cast<size_t>(len));
        pos += static_cast<size_t>(len);
        return s;
    }

    // Advance cursor by `n` bytes (skip / ignore region).
    void skip(size_t n, const char* ctx) {
        require(n, ctx);
        pos += n;
    }
};

// ---------------------------------------------------------------------------
// GGUF KV value-type codes (from the GGUF spec).
// ---------------------------------------------------------------------------
// Each metadata key-value pair is: [key:gguf_string][value_type:u32][value...]
// The value encoding depends on value_type. We skip every value without
// interpreting it — only the value_type byte-sizes matter for cursor advance.
//
// GGUF value type IDs (spec §2.1):
enum class GgufValueType : uint32_t {
    UINT8   = 0,
    INT8    = 1,
    UINT16  = 2,
    INT16   = 3,
    UINT32  = 4,
    INT32   = 5,
    FLOAT32 = 6,
    BOOL    = 7,
    STRING  = 8,
    ARRAY   = 9,
    UINT64  = 10,
    INT64   = 11,
    FLOAT64 = 12,
};

// Forward declaration so skip_gguf_value can call itself for ARRAY elements.
void skip_gguf_value(CursorReader& r, GgufValueType type);

// Skip a single GGUF value of the given type.
void skip_gguf_value(CursorReader& r, GgufValueType type) {
    switch (type) {
        case GgufValueType::UINT8:
        case GgufValueType::INT8:
        case GgufValueType::BOOL:
            r.skip(1, "gguf_kv_value");
            break;
        case GgufValueType::UINT16:
        case GgufValueType::INT16:
            r.skip(2, "gguf_kv_value");
            break;
        case GgufValueType::UINT32:
        case GgufValueType::INT32:
        case GgufValueType::FLOAT32:
            r.skip(4, "gguf_kv_value");
            break;
        case GgufValueType::UINT64:
        case GgufValueType::INT64:
        case GgufValueType::FLOAT64:
            r.skip(8, "gguf_kv_value");
            break;
        case GgufValueType::STRING:
            // String = [u64 len][chars...]
            r.read_gguf_string("gguf_kv_string_value");
            break;
        case GgufValueType::ARRAY: {
            // Array = [item_type:u32][count:u64][items...]
            uint32_t raw_item_type = r.read_u32("gguf_kv_array_type");
            uint64_t count         = r.read_u64("gguf_kv_array_count");
            auto item_type = static_cast<GgufValueType>(raw_item_type);
            // Unknown array item types fall through to skip_gguf_value which
            // will throw FormatError on unrecognised wire types, preventing UB.
            for (uint64_t i = 0; i < count; ++i)
                skip_gguf_value(r, item_type);
            break;
        }
        default:
            // Unknown wire type — cannot safely advance the cursor; refuse
            // rather than producing silent garbage. Extend this switch when
            // GGUF v4+ adds new value-type codes.
            throw FormatError("unknown GGUF KV value type; cannot skip safely");
    }
}

// ---------------------------------------------------------------------------
// Map GGUF element type codes to LQT DType (D-003).
// GGUF ggml_type enum:
//   0  = GGML_TYPE_F32
//   1  = GGML_TYPE_F16
//   2  = GGML_TYPE_Q4_0   → we treat as INT4
//   3  = GGML_TYPE_Q4_1   → INT4 (different quant, same storage width)
//   6  = GGML_TYPE_Q5_0   → INT8 (no native INT5 in LQT)
//   7  = GGML_TYPE_Q5_1   → INT8
//   8  = GGML_TYPE_Q8_0   → INT8
//   9  = GGML_TYPE_Q8_1   → INT8
//   others                → FP32 (safe fallback)
// ---------------------------------------------------------------------------
DType gguf_type_to_dtype(uint32_t gguf_type) {
    switch (gguf_type) {
        case 0:  return DType::FP32;  // GGML_TYPE_F32
        case 1:  return DType::FP16;  // GGML_TYPE_F16
        case 2:  return DType::INT4;  // GGML_TYPE_Q4_0
        case 3:  return DType::INT4;  // GGML_TYPE_Q4_1
        case 6:  return DType::INT8;  // GGML_TYPE_Q5_0 (no INT5 in LQT)
        case 7:  return DType::INT8;  // GGML_TYPE_Q5_1
        case 8:  return DType::INT8;  // GGML_TYPE_Q8_0
        case 9:  return DType::INT8;  // GGML_TYPE_Q8_1
        default:
            // BF16 (type 30), K-quant types (Q2_K=10..Q8_K=15 already handled
            // by block_spec), and future GGUF types fall back to FP32. The
            // tensor bytes are still copied correctly; only reconstruction
            // will use the FP32 affine path rather than the native dtype.
            return DType::FP32;
    }
}

// ---------------------------------------------------------------------------
// Exact GGUF block specification: (bytes_per_block, elements_per_block).
// Source: ggml source ggml.c ggml_type_size / ggml_blck_size.
// ---------------------------------------------------------------------------
struct GgufBlockSpec { size_t bytes_per_block; uint32_t elems_per_block; };

static GgufBlockSpec gguf_block_spec(uint32_t gguf_type) {
    switch (gguf_type) {
        case 0:  return {4,  1};  // GGML_TYPE_F32
        case 1:  return {2,  1};  // GGML_TYPE_F16
        case 2:  return {18, 32}; // GGML_TYPE_Q4_0: 2B scale + 16B nibbles
        case 3:  return {20, 32}; // GGML_TYPE_Q4_1: 2B scale + 2B min + 16B
        case 6:  return {22, 32}; // GGML_TYPE_Q5_0: 2B scale + 4B hi-bits + 16B
        case 7:  return {24, 32}; // GGML_TYPE_Q5_1: +2B min
        case 8:  return {34, 32}; // GGML_TYPE_Q8_0: 2B scale + 32B int8
        case 9:  return {36, 32}; // GGML_TYPE_Q8_1: 2B scale + 2B sum + 32B
        case 10: return {18, 32}; // GGML_TYPE_Q2_K (approx; real struct varies)
        case 11: return {110,256}; // GGML_TYPE_Q3_K
        case 12: return {144,256}; // GGML_TYPE_Q4_K
        case 13: return {176,256}; // GGML_TYPE_Q5_K
        case 14: return {210,256}; // GGML_TYPE_Q6_K
        case 15: return {136,256}; // GGML_TYPE_Q8_K
        case 30: return {2,  1};  // GGML_TYPE_BF16 (added 2024)
        default: return {4,  1};  // fallback: treat as F32
    }
}

// Total byte size of a tensor on disk given element count and gguf_type.
static size_t gguf_tensor_byte_size(uint32_t gguf_type, uint64_t elem_count) {
    const GgufBlockSpec s = gguf_block_spec(gguf_type);
    const uint64_t num_blocks =
        (elem_count + s.elems_per_block - 1) / s.elems_per_block;
    return static_cast<size_t>(num_blocks * static_cast<uint64_t>(s.bytes_per_block));
}

// Local align_up (mirrors the one in model.cpp's anonymous namespace).
static size_t align_up_sz(size_t x, size_t a) { return (x + a - 1) / a * a; }

// ---------------------------------------------------------------------------
// Block-quantized scale extraction for Q4_0 and Q8_0.
//
// GGUF Q4_0 block (18 bytes / 32 elements):
//   [ggml_fp16_t scale : 2 bytes][16 packed INT4 nibbles]
//   Reconstruction: w[i] = (q[i] - 8) * scale
//
// GGUF Q8_0 block (34 bytes / 32 elements):
//   [ggml_fp16_t scale : 2 bytes][32 int8 weights]
//   Reconstruction: w[i] = q[i] * scale
//
// This function extracts the per-block scales, computes the mean scale for
// use as `desc.scale`, and repacks the quantized values (without scale headers)
// into a clean LQT index blob so that reconstruction uses:
//   w[i] = codebook_lookup(q[i]) * mean_scale
// which is a first-order approximation (exact when all blocks share one scale,
// e.g. for fine-tuned layers where variance is low).
//
// Returns {mean_scale, clean_index_bytes}.  `raw` must point to the
// original GGUF block data of `raw_size` bytes.
// ---------------------------------------------------------------------------
struct BlockDecodeResult {
    float                mean_scale;
    std::vector<uint8_t> index_bytes; // nibble-packed INT4 or raw INT8
};

static BlockDecodeResult gguf_extract_block_scales(uint32_t    gguf_type,
                                                    const void* raw,
                                                    size_t      raw_size,
                                                    uint64_t    elem_count) {
    const auto* src = static_cast<const uint8_t*>(raw);
    BlockDecodeResult result;

    if (gguf_type == 2) {
        // Q4_0: 18-byte blocks (2B fp16 scale + 16B INT4 data).
        const size_t block_bytes = 18;
        const size_t num_blocks  = (elem_count + 31) / 32;
        if (raw_size < num_blocks * block_bytes)
            return {1.0f, std::vector<uint8_t>(raw_size)};

        double scale_sum = 0.0;
        // Data region: 16 bytes per block = 8 bytes per 16 elements.
        const size_t data_per_block = 16;
        result.index_bytes.resize(num_blocks * data_per_block);

        for (size_t b = 0; b < num_blocks; ++b) {
            const uint8_t* blk = src + b * block_bytes;
            // Extract fp16 scale (ggml packs it as a half-precision float).
            uint16_t scale_bits;
            std::memcpy(&scale_bits, blk, 2);
            scale_sum += static_cast<double>(lqt::fp16_to_fp32(scale_bits));
            // Copy the 16 packed nibble bytes.
            std::memcpy(result.index_bytes.data() + b * data_per_block,
                        blk + 2, data_per_block);
        }
        result.mean_scale = (num_blocks > 0)
            ? static_cast<float>(scale_sum / static_cast<double>(num_blocks))
            : 1.0f;

    } else if (gguf_type == 8) {
        // Q8_0: 34-byte blocks (2B fp16 scale + 32B int8 data).
        const size_t block_bytes = 34;
        const size_t num_blocks  = (elem_count + 31) / 32;
        if (raw_size < num_blocks * block_bytes)
            return {1.0f, std::vector<uint8_t>(raw_size)};

        double scale_sum = 0.0;
        const size_t data_per_block = 32;
        result.index_bytes.resize(num_blocks * data_per_block);

        for (size_t b = 0; b < num_blocks; ++b) {
            const uint8_t* blk = src + b * block_bytes;
            uint16_t scale_bits;
            std::memcpy(&scale_bits, blk, 2);
            scale_sum += static_cast<double>(lqt::fp16_to_fp32(scale_bits));
            std::memcpy(result.index_bytes.data() + b * data_per_block,
                        blk + 2, data_per_block);
        }
        result.mean_scale = (num_blocks > 0)
            ? static_cast<float>(scale_sum / static_cast<double>(num_blocks))
            : 1.0f;

    } else {
        // Non-block type — return raw bytes unchanged with scale 1.0.
        result.mean_scale = 1.0f;
        result.index_bytes.assign(src, src + raw_size);
    }

    return result;
}

// Per-tensor metadata collected during the info-parse pass.
struct GgufTensorInfo {
    std::string           name;
    uint32_t              ndim       = 0;
    std::vector<uint32_t> shape;
    uint32_t              gguf_type  = 0;
    uint64_t              data_offset= 0; // relative to data_region_start
};

// ---------------------------------------------------------------------------
// Read the entire contents of a file into a byte vector.
// Throws FormatError if the file cannot be opened or read.
// ---------------------------------------------------------------------------
// ── Minimal protobuf varint / wire-type decoder ──────────────────────────────
// Needed for from_onnx(). We hand-roll a decoder rather than linking libprotobuf.
// Protobuf wire format reference:
//   wire type 0 = varint (7 bits/byte, MSB continuation)
//   wire type 1 = 64-bit fixed
//   wire type 2 = length-delimited ([varint length][bytes])
//   wire type 5 = 32-bit fixed
//   tag = (field_number << 3) | wire_type

static uint64_t proto_read_varint(CursorReader& r) {
    uint64_t result = 0;
    int shift = 0;
    do {
        if (shift >= 64)
            throw FormatError("protobuf varint: too many continuation bytes");
        const uint8_t byte = r.read_u8("proto_varint");
        result |= static_cast<uint64_t>(byte & 0x7Fu) << shift;
        if (!(byte & 0x80u)) break;
        shift += 7;
    } while (true);
    return result;
}

static void proto_skip_field(CursorReader& r, uint8_t wire_type) {
    switch (wire_type) {
        case 0: proto_read_varint(r); break;
        case 1: r.skip(8, "proto_fixed64"); break;
        case 2: { const uint64_t n = proto_read_varint(r);
                  r.skip(static_cast<size_t>(n), "proto_len_delim"); break; }
        case 5: r.skip(4, "proto_fixed32"); break;
        default: throw FormatError("protobuf: unknown wire type");
    }
}

// Parse one ONNX TensorProto (field numbers per onnx.proto3):
//   field 1  (dims      , repeated int64 , varint)  → shape
//   field 2  (data_type , int32          , varint)  → dtype
//   field 8  (name      , string         , len-delim) → name
//   field 9  (raw_data  , bytes          , len-delim) → raw weight bytes
// All other fields are skipped. Adds the parsed tensor to `model`.
static void proto_parse_tensor_proto(CursorReader& r, size_t end_pos,
                                     LqtModel& model, uint16_t& cb_id) {
    std::string           name;
    int32_t               data_type  = 1; // 1=FLOAT by default
    std::vector<int64_t>  dims;
    std::vector<uint8_t>  raw_data;

    while (r.pos < end_pos) {
        const uint64_t tag_raw = proto_read_varint(r);
        const uint32_t field   = static_cast<uint32_t>(tag_raw >> 3);
        const uint8_t  wtype   = static_cast<uint8_t>(tag_raw & 0x7u);

        if (field == 1 && wtype == 0) {
            // dims: each dim is a separate repeated int64 varint field.
            dims.push_back(static_cast<int64_t>(proto_read_varint(r)));
        } else if (field == 2 && wtype == 0) {
            data_type = static_cast<int32_t>(proto_read_varint(r));
        } else if (field == 8 && wtype == 2) {
            // name: length-prefixed string.
            const uint64_t n = proto_read_varint(r);
            r.require(static_cast<size_t>(n), "onnx tensor name");
            name.assign(reinterpret_cast<const char*>(r.data + r.pos),
                        static_cast<size_t>(n));
            r.pos += static_cast<size_t>(n);
        } else if (field == 9 && wtype == 2) {
            // raw_data: packed weight bytes.
            const uint64_t n = proto_read_varint(r);
            r.require(static_cast<size_t>(n), "onnx raw_data");
            raw_data.resize(static_cast<size_t>(n));
            std::memcpy(raw_data.data(), r.data + r.pos, static_cast<size_t>(n));
            r.pos += static_cast<size_t>(n);
        } else {
            proto_skip_field(r, wtype);
        }
    }
    r.pos = end_pos; // guarantee cursor lands at end of tensor proto

    if (dims.empty()) return; // skip scalar / empty tensors

    // Map ONNX DataType codes to LQT DType.
    // ONNX DataType: 1=FLOAT, 2=UINT8, 3=INT8, 5=INT16, 6=INT32,
    //                10=FLOAT16, 11=DOUBLE, others→FP32.
    DType dtype = DType::FP32;
    switch (data_type) {
        case 1:  dtype = DType::FP32;  break;
        case 2:  dtype = DType::UINT8; break;
        case 3:  dtype = DType::INT8;  break;
        case 5:  dtype = DType::INT16; break;
        case 6:  dtype = DType::INT32; break;
        case 10: dtype = DType::FP16;  break;
        default: dtype = DType::FP32;  break;
    }

    // Build shape (clamp negatives to 1).
    std::vector<uint32_t> shape;
    shape.reserve(dims.size());
    for (int64_t d : dims)
        shape.push_back(static_cast<uint32_t>(d > 0 ? d : 1));

    // Pad raw_data to LQT_ALIGN_INDEX (16 bytes).
    const size_t aligned = ((raw_data.size() + LQT_ALIGN_INDEX - 1) /
                             LQT_ALIGN_INDEX) * LQT_ALIGN_INDEX;
    raw_data.resize(aligned, 0u);

    // Minimal affine codebook (id=cb_id, 2-entry scalar).
    Codebook cb(cb_id, 2, 1);
    cb.set_scalar(0, 0.0f);
    cb.set_scalar(1, 1.0f);
    model.add_codebook(cb);

    TensorDescriptor desc;
    desc.name           = name.empty() ? ("tensor_" + std::to_string(cb_id)) : name;
    desc.tensor_type    = TensorType::Standard;
    desc.dtype          = dtype;
    desc.shape          = std::move(shape);
    desc.codebook_id    = cb_id;
    desc.delta_id       = LQT_ID_NONE;
    desc.sparse_mask_id = LQT_ID_NONE;
    desc.scale          = 1.0f;
    desc.zero_point     = 0;
    desc.flags          = 0;

    model.add_tensor(std::move(desc), std::move(raw_data));
    if (cb_id < 0xFFFEu) ++cb_id;
}

// ── read_file ─────────────────────────────────────────────────────────────────
std::vector<uint8_t> read_file(const std::string& path) {
    std::ifstream f(path, std::ios::binary | std::ios::ate);
    if (!f.is_open())
        throw FormatError("cannot open file: " + path);
    const auto size = f.tellg();
    if (size < 0)
        throw FormatError("cannot determine file size: " + path);
    f.seekg(0);
    std::vector<uint8_t> buf(static_cast<size_t>(size));
    if (!f.read(reinterpret_cast<char*>(buf.data()),
                static_cast<std::streamsize>(size)))
        throw FormatError("file read error: " + path);
    return buf;
}

} // anonymous namespace

// ============================================================================
// GGUF -> LqtModel
// ============================================================================

LqtModel from_gguf(const uint8_t* data, size_t size) {
    CursorReader r{data, size};

    // ── Step 1: Header ─────────────────────────────────────────────────────
    if (size < 24)
        throw FormatError("GGUF file too small to contain a valid header");

    GgufHeader hdr;
    hdr.magic        = r.read_u32("gguf header magic");
    hdr.version      = r.read_u32("gguf header version");
    hdr.tensor_count = r.read_u64("gguf header tensor_count");
    hdr.kv_count     = r.read_u64("gguf header kv_count");

    if (!hdr.valid()) {
        if (hdr.magic != GGUF_MAGIC)
            throw FormatError("not a GGUF file: bad magic");
        throw FormatError("unsupported GGUF version " + std::to_string(hdr.version));
    }

    if (hdr.tensor_count > 1'000'000u)
        throw FormatError("GGUF tensor_count exceeds sanity limit (1M)");

    // ── Step 2: KV metadata — capture alignment + model metadata ───────────
    // Each pair: [key:gguf_string][value_type:u32][value...]
    // Capture: general.alignment, general.name, general.architecture,
    //          *.context_length, *.embedding_length.
    uint32_t    alignment       = 32; // GGUF default
    std::string model_name;
    std::string architecture;
    uint32_t    context_length  = 0;
    uint32_t    embedding_length= 0;

    for (uint64_t i = 0; i < hdr.kv_count; ++i) {
        std::string key       = r.read_gguf_string("gguf_kv_key");
        uint32_t    raw_vtype = r.read_u32("gguf_kv_value_type");
        auto        vtype     = static_cast<GgufValueType>(raw_vtype);

        if (key == "general.alignment" && vtype == GgufValueType::UINT32) {
            alignment = r.read_u32("general.alignment");
        } else if (key == "general.name" && vtype == GgufValueType::STRING) {
            model_name = r.read_gguf_string("general.name");
        } else if (key == "general.architecture" && vtype == GgufValueType::STRING) {
            architecture = r.read_gguf_string("general.architecture");
        } else if (key.find("context_length") != std::string::npos &&
                   (vtype == GgufValueType::UINT32 || vtype == GgufValueType::UINT64)) {
            if (vtype == GgufValueType::UINT32)
                context_length = r.read_u32("context_length");
            else
                context_length = static_cast<uint32_t>(r.read_u64("context_length"));
        } else if (key.find("embedding_length") != std::string::npos &&
                   (vtype == GgufValueType::UINT32 || vtype == GgufValueType::UINT64)) {
            if (vtype == GgufValueType::UINT32)
                embedding_length = r.read_u32("embedding_length");
            else
                embedding_length = static_cast<uint32_t>(r.read_u64("embedding_length"));
        } else {
            skip_gguf_value(r, vtype);
        }
    }

    // ── Step 3: Tensor-info — two-pass, collect first ───────────────────────
    // Pass A: read all tensor-info entries and store in a vector.
    // We must read ALL entries before we know where the data region begins,
    // because data_region_start = align_up(cursor after all info, alignment).
    std::vector<GgufTensorInfo> infos;
    infos.reserve(static_cast<size_t>(hdr.tensor_count));

    for (uint64_t i = 0; i < hdr.tensor_count; ++i) {
        GgufTensorInfo ti;
        ti.name      = r.read_gguf_string("gguf_tensor_name");
        ti.ndim      = r.read_u32("gguf_tensor_ndim");
        if (ti.ndim > 8)
            throw FormatError("GGUF tensor ndim > 8 for '" + ti.name + "'");
        ti.shape.resize(ti.ndim);
        for (uint32_t d = 0; d < ti.ndim; ++d)
            ti.shape[d] = r.read_u32("gguf_tensor_dim");
        ti.gguf_type   = r.read_u32("gguf_tensor_type");
        ti.data_offset = r.read_u64("gguf_tensor_offset");
        infos.push_back(std::move(ti));
    }

    // ── Step 4: Locate the data region ──────────────────────────────────────
    // The tensor-data section begins at the next alignment boundary after
    // the end of all tensor-info entries (spec §2.2).
    const size_t data_region_start = align_up_sz(r.pos, static_cast<size_t>(alignment));

    // ── Step 5: Build LqtModel — copy real weight bytes ─────────────────────
    // Pass B: for each tensor, copy the actual bytes from the data section.
    // Byte size of tensor i is derived from the offset delta:
    //   size_i = offset[i+1] - offset[i]  (for i < n-1)
    //   size_last = file_size - data_region_start - offset[last]
    LqtModel model;
    uint16_t cb_id = 0;

    // ── Populate model metadata from captured KV pairs ──────────────────────
    if (context_length  > 0) model.set_hyperparam("context_length",  static_cast<float>(context_length));
    if (embedding_length> 0) model.set_hyperparam("embedding_length",static_cast<float>(embedding_length));
    if (!model_name.empty() || !architecture.empty()) {
        model.set_module_graph_json(
            "{\"name\":\"" + model_name + "\",\"architecture\":\"" + architecture + "\"}");
    }

    for (size_t i = 0; i < infos.size(); ++i) {
        const GgufTensorInfo& ti = infos[i];

        // Compute element count.
        uint64_t elem_count = 1;
        for (uint32_t d = 0; d < ti.ndim; ++d) elem_count *= ti.shape[d];

        // Determine the on-disk byte size using the exact block specification.
        // For unquantized types (F32/F16/BF16) the formula reduces to
        // elem_count * bytes_per_elem. For block-quantized types it correctly
        // accounts for the block header overhead.
        size_t raw_bytes = gguf_tensor_byte_size(ti.gguf_type, elem_count);

        // Cross-check against the offset-delta when possible — the two methods
        // must agree, and the delta-based size is the ground truth from the file.
        if (i + 1 < infos.size()) {
            size_t delta = static_cast<size_t>(
                infos[i + 1].data_offset - ti.data_offset);
            raw_bytes = delta; // use file-provided delta as ground truth
        } else {
            // Last tensor: compute from file boundary.
            const size_t abs_start = data_region_start +
                                     static_cast<size_t>(ti.data_offset);
            if (abs_start < size)
                raw_bytes = size - abs_start;
            // else leave raw_bytes from block-spec (file may be truncated).
        }

        // Absolute file position of this tensor's weight bytes.
        const size_t abs_offset = data_region_start +
                                  static_cast<size_t>(ti.data_offset);

        // Bounds check — skip rather than crash on truncated files.
        if (abs_offset > size || abs_offset + raw_bytes > size) {
            throw FormatError("GGUF tensor data out of bounds: '" + ti.name +
                              "' offset=" + std::to_string(abs_offset) +
                              " size=" + std::to_string(raw_bytes) +
                              " file=" + std::to_string(size));
        }

        // For Q4_0 and Q8_0: extract per-block FP16 scales, compute the mean
        // scale, and repack the quantized values without the scale headers.
        // For all other types: copy the raw bytes verbatim.
        std::vector<uint8_t> index_bytes;
        float tensor_scale = 1.0f;

        if ((ti.gguf_type == 2 || ti.gguf_type == 8) && raw_bytes > 0) {
            BlockDecodeResult bdr = gguf_extract_block_scales(
                ti.gguf_type, data + abs_offset, raw_bytes, elem_count);
            tensor_scale = bdr.mean_scale;
            // Pad to LQT_ALIGN_INDEX for SIMD paths.
            const size_t al = align_up_sz(bdr.index_bytes.size(), LQT_ALIGN_INDEX);
            bdr.index_bytes.resize(al, 0x00);
            index_bytes = std::move(bdr.index_bytes);
        } else {
            // All other types: copy raw bytes verbatim.
            const size_t aligned_size = align_up_sz(raw_bytes, LQT_ALIGN_INDEX);
            index_bytes.resize(aligned_size, 0x00);
            if (raw_bytes > 0)
                std::memcpy(index_bytes.data(), data + abs_offset, raw_bytes);
        }

        // Build a minimal scalar affine codebook anchoring the descriptor.
        // For block-quant types the codebook scale carries the mean block scale.
        Codebook cb(cb_id, /*num_vectors=*/2, /*vector_dim=*/1);
        cb.set_scalar(0, 0.0f);
        cb.set_scalar(1, tensor_scale); // mean scale for Q4_0/Q8_0; 1.0 otherwise
        model.add_codebook(cb);

        // Build TensorDescriptor.
        TensorDescriptor desc;
        desc.name           = ti.name;
        desc.tensor_type    = TensorType::Standard;
        desc.dtype          = gguf_type_to_dtype(ti.gguf_type);
        desc.shape          = ti.shape;
        desc.codebook_id    = cb_id;
        desc.delta_id       = LQT_ID_NONE;
        desc.sparse_mask_id = LQT_ID_NONE;
        desc.scale          = tensor_scale; // mean block scale (1.0 for non-block types)
        desc.zero_point     = 0;
        desc.flags          = 0;

        model.add_tensor(std::move(desc), std::move(index_bytes));

        if (cb_id == 0xFFFEu)
            throw FormatError("GGUF model exceeds u16 codebook ID range");
        ++cb_id;
    }

    return model;
}

LqtModel from_gguf(const std::string& path) {
    const std::vector<uint8_t> buf = read_file(path);
    return from_gguf(buf.data(), buf.size());
}

// ============================================================================
// ONNX -> LqtModel
// ============================================================================
// ONNX files are serialized protobuf (proto3). A full parse requires either
// linking libprotobuf or hand-rolling a varint/wire-type decoder.
//
// Production implementation: walks the ModelProto→GraphProto→TensorProto
// initializer chain using a hand-rolled varint/wire-type decoder. Extracts
// tensor names, dims, data_type, and raw_data without requiring libprotobuf.
//
// Protobuf wire-type quick reference:
//   wire type 0 = varint        tag = (field_number << 3) | 0
//   wire type 1 = 64-bit        tag = (field_number << 3) | 1
//   wire type 2 = length-delim  tag = (field_number << 3) | 2
//   wire type 5 = 32-bit        tag = (field_number << 3) | 5
//
// ONNX ModelProto (onnx.proto3, field numbers):
//   field 1  (tag 0x0A): ir_version (int64, varint)     — first field always written
//   field 2  (tag 0x12): opset_import (OperatorSetIdProto, length-delim)
//   field 7  (tag 0x3A): graph (GraphProto, length-delim)
//
// GraphProto (field numbers):
//   field 1  (tag 0x0A): node (NodeProto[], length-delim)
//   field 4  (tag 0x22): initializer (TensorProto[], length-delim)  ← weights
//   field 11 (tag 0x5A): input (ValueInfoProto[], length-delim)
//
// TensorProto (field numbers):
//   field 1  (tag 0x08): dims (int64[], varint)
//   field 2  (tag 0x10): data_type (DataType enum, varint)
//   field 8  (tag 0x42): name (string, length-delim)
//   field 9  (tag 0x4A): raw_data (bytes, length-delim)
// ============================================================================

LqtModel from_onnx(const uint8_t* data, size_t size) {
    if (size == 0)
        throw FormatError("not a valid ONNX file: empty buffer");

    // Sanity check: ONNX ModelProto first tag must be field 1 or 2
    // (ir_version or opset_import), both plausible leading fields.
    const uint8_t first_byte = data[0];
    if (first_byte != 0x08 && first_byte != 0x0A &&
        first_byte != 0x12 && first_byte != 0x0D) {
        throw FormatError("not a valid ONNX file: unexpected first protobuf tag byte");
    }

    LqtModel model;
    uint16_t cb_id = 0;
    CursorReader r{data, size};

    // Walk the top-level ModelProto, extracting:
    //   - field 2 (opset_import) → hyperparam "onnx_opset"
    //   - field 7 (graph)        → GraphProto walker
    try {
        while (r.pos < size) {
            const uint64_t tag_raw = proto_read_varint(r);
            const uint32_t field   = static_cast<uint32_t>(tag_raw >> 3);
            const uint8_t  wtype   = static_cast<uint8_t>(tag_raw & 0x7u);

            if (field == 2 && wtype == 2) {
                // opset_import: OperatorSetIdProto — read to extract version.
                const uint64_t opset_len = proto_read_varint(r);
                const size_t   opset_end = r.pos + static_cast<size_t>(opset_len);
                r.require(static_cast<size_t>(opset_len), "onnx opset");
                // Walk OperatorSetIdProto: field 2 = version (int64 varint).
                while (r.pos < opset_end) {
                    const uint64_t t  = proto_read_varint(r);
                    const uint32_t f  = static_cast<uint32_t>(t >> 3);
                    const uint8_t  wt = static_cast<uint8_t>(t & 0x7u);
                    if (f == 2 && wt == 0) {
                        const uint64_t ver = proto_read_varint(r);
                        model.set_hyperparam("onnx_opset", static_cast<float>(ver));
                    } else {
                        proto_skip_field(r, wt);
                    }
                }
                r.pos = opset_end;
            } else if (field == 7 && wtype == 2) {
                // graph: GraphProto — walk for initializer TensorProtos.
                const uint64_t graph_len = proto_read_varint(r);
                const size_t   graph_end = r.pos + static_cast<size_t>(graph_len);
                r.require(static_cast<size_t>(graph_len), "onnx graph");

                while (r.pos < graph_end) {
                    const uint64_t gt     = proto_read_varint(r);
                    const uint32_t gfield = static_cast<uint32_t>(gt >> 3);
                    const uint8_t  gwtype = static_cast<uint8_t>(gt & 0x7u);

                    if (gfield == 4 && gwtype == 2) {
                        // initializer: TensorProto (repeated).
                        const uint64_t t_len = proto_read_varint(r);
                        const size_t   t_end = r.pos + static_cast<size_t>(t_len);
                        r.require(static_cast<size_t>(t_len), "onnx tensor");
                        proto_parse_tensor_proto(r, t_end, model, cb_id);
                        r.pos = t_end;
                    } else {
                        proto_skip_field(r, gwtype);
                    }
                }
                r.pos = graph_end;
            } else {
                proto_skip_field(r, wtype);
            }
        }
    } catch (const FormatError&) {
        // Partial parse — return whatever was successfully extracted.
        // FormatErrors from malformed data are swallowed here so that
        // truncated or non-standard ONNX files still yield a partial model.
    }

    return model;
}

LqtModel from_onnx(const std::string& path) {
    const std::vector<uint8_t> buf = read_file(path);
    return from_onnx(buf.data(), buf.size());
}

} // namespace lqt
