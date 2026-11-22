// lqt/endian.h — Little-endian (de)serialization primitives.
//
// Council module: A1 (container) — shared by every serializer.
// Canon: lqt.md §2.2 (BIG_ENDIAN flag, default little-endian).
//
// DECISION: on-disk canonical byte order is little-endian. Writers always emit
// little-endian. Readers byte-swap on the fly when a file's BIG_ENDIAN flag is
// set (handled at a higher layer by reading through the swap helpers). These
// ByteReader/ByteWriter cursors do bounds-checked LE encode/decode and are the
// only place raw integer bytes are touched.
#pragma once

#include <cstdint>
#include <cstring>
#include <memory>
#include <string>
#include <vector>
#include "lqt/error.h"

namespace lqt {

// --------------------------- Host byte order --------------------------------
inline bool host_is_little_endian() {
    const uint16_t probe = 0x0001;
    return *reinterpret_cast<const uint8_t*>(&probe) == 0x01;
}

constexpr uint16_t bswap16(uint16_t v) {
    return static_cast<uint16_t>((v >> 8) | (v << 8));
}
constexpr uint32_t bswap32(uint32_t v) {
    return ((v & 0x000000FFu) << 24) | ((v & 0x0000FF00u) << 8) |
           ((v & 0x00FF0000u) >> 8) | ((v & 0xFF000000u) >> 24);
}
constexpr uint64_t bswap64(uint64_t v) {
    return ((v & 0x00000000000000FFull) << 56) | ((v & 0x000000000000FF00ull) << 40) |
           ((v & 0x0000000000FF0000ull) << 24) | ((v & 0x00000000FF000000ull) << 8) |
           ((v & 0x000000FF00000000ull) >> 8)  | ((v & 0x0000FF0000000000ull) >> 24) |
           ((v & 0x00FF000000000000ull) >> 40) | ((v & 0xFF00000000000000ull) >> 56);
}

// =============================== ByteWriter =================================
// Appends little-endian encoded primitives to an owned byte buffer.
class ByteWriter {
public:
    ByteWriter() = default;
    explicit ByteWriter(size_t reserve_hint) { buf_.reserve(reserve_hint); }

    void put_u8(uint8_t v) { buf_.push_back(v); }
    void put_i8(int8_t v) { buf_.push_back(static_cast<uint8_t>(v)); }

    void put_u16(uint16_t v) {
        buf_.push_back(static_cast<uint8_t>(v & 0xFF));
        buf_.push_back(static_cast<uint8_t>((v >> 8) & 0xFF));
    }
    void put_u32(uint32_t v) {
        for (int i = 0; i < 4; ++i) buf_.push_back(static_cast<uint8_t>((v >> (8 * i)) & 0xFF));
    }
    void put_u64(uint64_t v) {
        for (int i = 0; i < 8; ++i) buf_.push_back(static_cast<uint8_t>((v >> (8 * i)) & 0xFF));
    }
    void put_i16(int16_t v) { put_u16(static_cast<uint16_t>(v)); }
    void put_i32(int32_t v) { put_u32(static_cast<uint32_t>(v)); }
    void put_i64(int64_t v) { put_u64(static_cast<uint64_t>(v)); }

    // 24-bit unsigned (delta block num_elements). Value must fit in 24 bits.
    void put_u24(uint32_t v) {
        buf_.push_back(static_cast<uint8_t>(v & 0xFF));
        buf_.push_back(static_cast<uint8_t>((v >> 8) & 0xFF));
        buf_.push_back(static_cast<uint8_t>((v >> 16) & 0xFF));
    }

    void put_f32(float v) {
        uint32_t bits;
        std::memcpy(&bits, &v, sizeof(bits));
        put_u32(bits);
    }
    void put_f64(double v) {
        uint64_t bits;
        std::memcpy(&bits, &v, sizeof(bits));
        put_u64(bits);
    }

    void put_bytes(const void* data, size_t n) {
        const uint8_t* p = static_cast<const uint8_t*>(data);
        buf_.insert(buf_.end(), p, p + n);
    }
    void put_zeros(size_t n) { buf_.insert(buf_.end(), n, 0); }

    // Length-prefixed UTF-8 string: uint32 length then raw bytes.
    void put_string(const std::string& s) {
        put_u32(static_cast<uint32_t>(s.size()));
        put_bytes(s.data(), s.size());
    }

    // Pad with zero bytes until size() is a multiple of `alignment`.
    void pad_to(size_t alignment) {
        if (alignment <= 1) return;
        const size_t rem = buf_.size() % alignment;
        if (rem != 0) put_zeros(alignment - rem);
    }

    size_t size() const { return buf_.size(); }
    const std::vector<uint8_t>& bytes() const { return buf_; }
    std::vector<uint8_t> take() { return std::move(buf_); }

    // Overwrite 8 bytes at an earlier position (used for back-patching offsets).
    void patch_u64(size_t pos, uint64_t v) {
        if (pos + 8 > buf_.size()) throw FormatError("ByteWriter::patch_u64 out of range");
        for (int i = 0; i < 8; ++i) buf_[pos + i] = static_cast<uint8_t>((v >> (8 * i)) & 0xFF);
    }
    void patch_u32(size_t pos, uint32_t v) {
        if (pos + 4 > buf_.size()) throw FormatError("ByteWriter::patch_u32 out of range");
        for (int i = 0; i < 4; ++i) buf_[pos + i] = static_cast<uint8_t>((v >> (8 * i)) & 0xFF);
    }

private:
    std::vector<uint8_t> buf_;
};

// =============================== ByteReader =================================
// Bounds-checked little-endian decode cursor over a borrowed buffer.
class ByteReader {
public:
    ByteReader(const uint8_t* data, size_t size) : data_(data), size_(size), pos_(0) {}
    explicit ByteReader(const std::vector<uint8_t>& v) : ByteReader(v.data(), v.size()) {}
    // Polymorphic base: make_reader() hands out unique_ptr<ByteReader> that may
    // own a BigEndianByteReader, so destruction must dispatch virtually
    // (2026-11-21; clang -Wdelete-non-abstract-non-virtual-dtor, 42 sites).
    virtual ~ByteReader() = default;
    ByteReader(const ByteReader&) = default;
    ByteReader& operator=(const ByteReader&) = default;
    ByteReader(ByteReader&&) = default;
    ByteReader& operator=(ByteReader&&) = default;

    size_t position() const { return pos_; }
    size_t size() const { return size_; }
    size_t remaining() const { return size_ - pos_; }
    const uint8_t* current() const { return data_ + pos_; }

    void require(size_t n) const {
        if (pos_ + n > size_) throw FormatError("ByteReader: unexpected end of buffer");
    }
    void seek(size_t pos) {
        if (pos > size_) throw FormatError("ByteReader::seek past end");
        pos_ = pos;
    }
    void skip(size_t n) { require(n); pos_ += n; }

    // Advance to next multiple of `alignment` relative to buffer start.
    void align_to(size_t alignment) {
        if (alignment <= 1) return;
        const size_t rem = pos_ % alignment;
        if (rem != 0) skip(alignment - rem);
    }

    uint8_t  get_u8()  { require(1); return data_[pos_++]; }
    int8_t   get_i8()  { return static_cast<int8_t>(get_u8()); }

    // Multi-byte getters are virtual so a BigEndianByteReader can be passed
    // through any ByteReader& interface (parser functions) and still byte-swap
    // (D-016 wiring). Single-byte getters and byte-range reads are endian-
    // neutral and stay non-virtual.
    virtual uint16_t get_u16() {
        require(2);
        uint16_t v = static_cast<uint16_t>(data_[pos_]) |
                     (static_cast<uint16_t>(data_[pos_ + 1]) << 8);
        pos_ += 2; return v;
    }
    virtual uint32_t get_u32() {
        require(4);
        uint32_t v = 0;
        for (int i = 0; i < 4; ++i) v |= static_cast<uint32_t>(data_[pos_ + i]) << (8 * i);
        pos_ += 4; return v;
    }
    virtual uint64_t get_u64() {
        require(8);
        uint64_t v = 0;
        for (int i = 0; i < 8; ++i) v |= static_cast<uint64_t>(data_[pos_ + i]) << (8 * i);
        pos_ += 8; return v;
    }
    virtual int16_t  get_i16() { return static_cast<int16_t>(get_u16()); }
    virtual int32_t  get_i32() { return static_cast<int32_t>(get_u32()); }
    virtual int64_t  get_i64() { return static_cast<int64_t>(get_u64()); }

    virtual uint32_t get_u24() {
        require(3);
        uint32_t v = static_cast<uint32_t>(data_[pos_]) |
                     (static_cast<uint32_t>(data_[pos_ + 1]) << 8) |
                     (static_cast<uint32_t>(data_[pos_ + 2]) << 16);
        pos_ += 3; return v;
    }

    virtual float get_f32() {
        uint32_t bits = get_u32();
        float v; std::memcpy(&v, &bits, sizeof(v)); return v;
    }
    virtual double get_f64() {
        uint64_t bits = get_u64();
        double v; std::memcpy(&v, &bits, sizeof(v)); return v;
    }

    void get_bytes(void* dst, size_t n) {
        require(n);
        std::memcpy(dst, data_ + pos_, n);
        pos_ += n;
    }
    virtual std::string get_string() {
        uint32_t n = get_u32();
        require(n);
        std::string s(reinterpret_cast<const char*>(data_ + pos_), n);
        pos_ += n; return s;
    }

private:
    const uint8_t* data_;
    size_t size_;
    size_t pos_;
};

// NOTE: files written by this library are always little-endian.
// BigEndianByteReader provides a read-only load path for files
// produced by big-endian hosts (flag HeaderFlag::BigEndian). The container
// layer (LqtModel::parse) routes every parser through this reader when the
// flag is set, and additionally materializes multi-byte index/float payloads
// to host order in memory (D-016 full read-side materialization).
// Writer endian swap remains out of scope for v0.1.

// Big-endian cursor — byte-swaps all multi-byte reads.
// Use when a file's FileHeader has HeaderFlag::BigEndian set.
class BigEndianByteReader : public ByteReader {
public:
    using ByteReader::ByteReader;
    uint16_t get_u16() override { return bswap16(ByteReader::get_u16()); }
    uint32_t get_u32() override { return bswap32(ByteReader::get_u32()); }
    uint64_t get_u64() override { return bswap64(ByteReader::get_u64()); }
    int16_t  get_i16() override { return static_cast<int16_t>(get_u16()); }
    int32_t  get_i32() override { return static_cast<int32_t>(get_u32()); }
    int64_t  get_i64() override { return static_cast<int64_t>(get_u64()); }
    uint32_t get_u24() override {
        require(3);
        const uint32_t v = (static_cast<uint32_t>(current()[0]) << 16) |
                           (static_cast<uint32_t>(current()[1]) << 8)  |
                            static_cast<uint32_t>(current()[2]);
        skip(3);
        return v;
    }
    float    get_f32() override { uint32_t b = get_u32(); float v; std::memcpy(&v, &b, 4); return v; }
    double   get_f64() override { uint64_t b = get_u64(); double v; std::memcpy(&v, &b, 8); return v; }
    std::string get_string() override {
        const uint32_t n = get_u32(); // BE-decoded length
        require(n);
        std::string s(reinterpret_cast<const char*>(current()), n);
        skip(n);
        return s;
    }
};

// Factory: returns a ByteReader or BigEndianByteReader depending on the file's endian flag.
// The file buffer must outlive the returned object.
// Usage: auto r = lqt::make_reader(buf, size, is_big_endian);
// Returns unique_ptr<ByteReader>.
inline std::unique_ptr<ByteReader>
make_reader(const uint8_t* data, size_t size, bool big_endian) {
    if (big_endian)
        return std::make_unique<BigEndianByteReader>(data, size);
    return std::make_unique<ByteReader>(data, size);
}

} // namespace lqt
