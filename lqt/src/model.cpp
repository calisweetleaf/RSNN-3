// lqt/src/model.cpp — LQTModel container assembly, parsing, reconstruction.
#include "lqt/model.h"

#include <chrono>
#include <cmath>
#include <fstream>
#include <numeric>

#include "lqt/crc.h"
#include "lqt/endian.h"
#include "lqt/error.h"
#include "lqt/reconstruct.h"
#include "lqt/tlv.h"

namespace lqt {
namespace {

inline size_t align_up(size_t x, size_t a) { return (x + a - 1) / a * a; }

// Pad the writer with zeros until its size equals `target` (must not overshoot).
void pad_to_offset(ByteWriter& w, size_t target) {
    if (w.size() > target) throw FormatError("LqtModel: layout overshoot while assembling");
    w.put_zeros(target - w.size());
}

// Encode the TensorDescriptors chunk value: [u32 count][descriptor...] (D-010).
std::vector<uint8_t> encode_descriptors(const std::vector<TensorBlob>& tensors) {
    ByteWriter w;
    w.put_u32(static_cast<uint32_t>(tensors.size()));
    for (const auto& t : tensors) t.desc.serialize(w);
    return w.take();
}

} // namespace

size_t tensor_index_byte_length(const TensorDescriptor& desc) {
    const uint64_t bits = desc.element_count() * static_cast<uint64_t>(dtype_bits(desc.dtype));
    return static_cast<size_t>((bits + 7) / 8);
}

void LqtModel::set_hyperparam(const std::string& key, float value) {
    for (auto& p : hyperparams_) {
        if (p.first == key) { p.second = value; return; }
    }
    hyperparams_.emplace_back(key, value);
}

const TensorBlob* LqtModel::find_tensor(const std::string& name) const {
    for (const auto& t : tensors_) {
        if (t.desc.name == name) return &t;
    }
    return nullptr;
}

std::vector<uint8_t> LqtModel::serialize_to_bytes() const {
    // 0. Writer/reader symmetry (2026-11-21): parse() validates every tensor
    //    descriptor, so the model writer must refuse descriptors it could not
    //    read back (previously a rank-3 RecursiveTensor saved fine and the file
    //    then failed to load). Low-level TensorDescriptor::serialize stays
    //    unvalidated so corruption tests can still craft rejected bytes.
    for (const auto& t : tensors_) t.desc.validate();
    // 1. Pre-serialize codebooks / deltas / masks / blobs to know their sizes.
    std::vector<std::pair<uint16_t, std::vector<uint8_t>>> cb_bytes;
    for (const auto& [id, cb] : codebooks_) {
        ByteWriter w; cb.serialize(w); cb_bytes.emplace_back(id, w.take());
    }
    std::vector<std::pair<uint16_t, std::vector<uint8_t>>> dl_bytes;
    for (const auto& [id, d] : deltas_) {
        ByteWriter w; d.serialize(w); dl_bytes.emplace_back(id, w.take());
    }
    std::vector<std::pair<uint16_t, std::vector<uint8_t>>> mk_bytes;
    for (const auto& [id, m] : masks_) {
        ByteWriter w; m.serialize(w); mk_bytes.emplace_back(id, w.take());
    }
    std::vector<std::vector<uint8_t>> blob_bytes; // descriptor order (D-009)
    for (const auto& t : tensors_) {
        ByteWriter w;
        w.put_u16(t.desc.codebook_id);
        w.put_u16(t.desc.delta_id);
        w.put_u16(t.desc.sparse_mask_id);
        w.put_bytes(t.indices.data(), t.indices.size());
        w.pad_to(LQT_ALIGN_INDEX);
        blob_bytes.push_back(w.take());
    }

    // Pre-serialize the EditLog (D-012) as a 0x000B chunk value.
    std::vector<uint8_t> edit_log_blob;
    {
        ByteWriter elw; edit_log_.serialize(elw); edit_log_blob = elw.take();
    }

    // Pre-serialize the RTA blocks (D-014) as a 0x0012 chunk value:
    //   [u32 count] then for each block: [name:str][rta_block_bytes...]
    std::vector<uint8_t> rta_blob;
    if (!rta_blocks_.empty()) {
        ByteWriter rw;
        rw.put_u32(static_cast<uint32_t>(rta_blocks_.size()));
        for (const auto& [name, block] : rta_blocks_) {
            rw.put_string(name);
            block.serialize(rw);
        }
        rta_blob = rw.take();
    }

    // Pre-serialize the RecursiveWeight table (D-024) as a 0x0011 chunk value:
    //   [u32 bucket_count] then for each bucket: [name:str][recursive_weight_bytes...]
    // A tensor name may repeat across multiple entries: weights are storage
    // buckets, not one-per-tensor -- each bucket is a self-contained
    // quintuple with its own lattice position T.
    std::vector<uint8_t> rw_blob;
    if (!recursive_weights_.empty()) {
        ByteWriter rww;
        size_t bucket_count = 0;
        for (const auto& [name, weights] : recursive_weights_) bucket_count += weights.size();
        rww.put_u32(static_cast<uint32_t>(bucket_count));
        for (const auto& [name, weights] : recursive_weights_) {
            for (const auto& weight : weights) {
                rww.put_string(name);
                weight.serialize(rww);
            }
        }
        rw_blob = rww.take();
    }

    // 2. Metadata builder (size depends only on entry counts, not offset values).
    auto build_meta = [&](const std::vector<TableEntry>& cbt,
                          const std::vector<TableEntry>& dlt,
                          const std::vector<TableEntry>& mkt) {
        MetadataSection sec;
        sec.add(ChunkType::ModelHyperparameters, encode_hyperparams(hyperparams_));
        sec.add(ChunkType::TensorDescriptors, encode_descriptors(tensors_));
        if (!module_graph_json_.empty()) {
            set_json(sec, ChunkType::ModuleDefinitions, module_graph_json_);
        }
        sec.add(ChunkType::CodebookTable, encode_table(cbt));
        sec.add(ChunkType::DeltaTable, encode_table(dlt));
        sec.add(ChunkType::SparseMaskTable, encode_table(mkt));
        // D-012: persist EditLog as 0x000B (always; an empty log is 4 bytes).
        sec.add(ChunkType::EditLog, edit_log_blob);
        // D-014: persist RTA blocks as 0x0012 when present.
        if (!rta_blob.empty()) {
            sec.add(ChunkType::RecursiveWeightMeta, rta_blob);
        }
        // D-024: persist the RecursiveWeight table as 0x0011 when present.
        if (!rw_blob.empty()) {
            sec.add(ChunkType::RecursiveWeightTable, rw_blob);
        }
        ByteWriter w; sec.serialize(w); return w.take();
    };

    // 3. Measure metadata size with placeholder tables (ids set, offsets 0).
    std::vector<TableEntry> cbt(cb_bytes.size()), dlt(dl_bytes.size()), mkt(mk_bytes.size());
    for (size_t i = 0; i < cb_bytes.size(); ++i) cbt[i] = {cb_bytes[i].first, 0, 0};
    for (size_t i = 0; i < dl_bytes.size(); ++i) dlt[i] = {dl_bytes[i].first, 0, 0};
    for (size_t i = 0; i < mk_bytes.size(); ++i) mkt[i] = {mk_bytes[i].first, 0, 0};
    const size_t meta_tlv_size = build_meta(cbt, dlt, mkt).size();

    // 4. Compute the absolute layout. Metadata region = [36, 36+8+tlv] (D-011).
    const size_t off_meta = LQT_HEADER_SIZE;
    const size_t meta_region_end = off_meta + 8 + meta_tlv_size;

    size_t cursor = align_up(meta_region_end, LQT_ALIGN_CODEBOOK);
    const size_t off_codebooks = cursor;
    for (size_t i = 0; i < cb_bytes.size(); ++i) {
        cursor = align_up(cursor, LQT_ALIGN_CODEBOOK);
        cbt[i].offset = cursor;
        cbt[i].size = cb_bytes[i].second.size();
        cursor += cb_bytes[i].second.size();
    }

    cursor = align_up(cursor, LQT_ALIGN_INDEX);
    const size_t off_tensors = cursor;
    for (const auto& bb : blob_bytes) cursor += bb.size(); // each pre-padded to 16

    cursor = align_up(cursor, LQT_ALIGN_DELTA);
    for (size_t i = 0; i < dl_bytes.size(); ++i) {
        cursor = align_up(cursor, LQT_ALIGN_DELTA);
        dlt[i].offset = cursor;
        dlt[i].size = dl_bytes[i].second.size();
        cursor += dl_bytes[i].second.size();
    }

    cursor = align_up(cursor, LQT_ALIGN_DELTA);
    for (size_t i = 0; i < mk_bytes.size(); ++i) {
        cursor = align_up(cursor, LQT_ALIGN_DELTA);
        mkt[i].offset = cursor;
        mkt[i].size = mk_bytes[i].second.size();
        cursor += mk_bytes[i].second.size();
    }

    cursor = align_up(cursor, LQT_ALIGN_DELTA);
    const size_t off_footer = cursor;

    // 5. Rebuild metadata with real table offsets (size must be unchanged).
    const std::vector<uint8_t> meta_real = build_meta(cbt, dlt, mkt);
    if (meta_real.size() != meta_tlv_size) {
        throw FormatError("LqtModel: metadata size drift between layout passes");
    }

    // Returns the byte offset of chunk `target`'s VALUE within the serialized
    // MetadataSection bytes (not the whole file). Returns SIZE_MAX if not found.
    // Mirrors MetadataSection::serialize/parse: iterate [u16 type][u32 length]
    // [value][pad-to-LQT_ALIGN_TLV] until the region is exhausted.
    auto find_meta_chunk_value_offset = [&](const std::vector<uint8_t>& meta,
                                             ChunkType target) -> size_t {
        ByteReader mr(meta);
        while (mr.position() < meta.size()) {
            if (meta.size() - mr.position() < 6) break; // partial header guard
            const auto type = static_cast<ChunkType>(mr.get_u16());
            const uint32_t len = mr.get_u32();
            const size_t val_pos = mr.position();
            if (type == target) return val_pos;
            mr.skip(len);
            mr.align_to(LQT_ALIGN_TLV);
        }
        return SIZE_MAX;
    };

    // Compute absolute file offset of the EditLog TLV chunk value (D-019).
    uint64_t edit_log_abs_offset = 0;
    {
        const size_t val_in_meta = find_meta_chunk_value_offset(meta_real, ChunkType::EditLog);
        if (val_in_meta != SIZE_MAX) {
            // off_meta = LQT_HEADER_SIZE = 36. +8 for the u64 tlv-length prefix (D-011).
            edit_log_abs_offset = static_cast<uint64_t>(off_meta + 8 + val_in_meta);
        }
    }

    // 6. Assemble the full file image.
    ByteWriter w(off_footer + LQT_FOOTER_SIZE);
    FileHeader h;
    h.magic = LQT_HEADER_MAGIC;
    h.version = LQT_FORMAT_VERSION;
    h.header_size = LQT_HEADER_SIZE;
    h.flags = header_.flags;
    flag_assign(h.flags, HeaderFlag::HasDeltas, !deltas_.empty());
    flag_assign(h.flags, HeaderFlag::HasSparseMasks, !masks_.empty());
    h.metadata_offset = off_meta;
    h.tensor_offset = off_tensors;
    h.footer_offset = off_footer;
    h.serialize(w); // 36 bytes

    w.put_u64(static_cast<uint64_t>(meta_tlv_size));      // D-011 length prefix
    w.put_bytes(meta_real.data(), meta_real.size());

    pad_to_offset(w, off_codebooks);
    for (size_t i = 0; i < cb_bytes.size(); ++i) {
        pad_to_offset(w, static_cast<size_t>(cbt[i].offset));
        w.put_bytes(cb_bytes[i].second.data(), cb_bytes[i].second.size());
    }

    pad_to_offset(w, off_tensors);
    for (const auto& bb : blob_bytes) w.put_bytes(bb.data(), bb.size());

    for (size_t i = 0; i < dl_bytes.size(); ++i) {
        pad_to_offset(w, static_cast<size_t>(dlt[i].offset));
        w.put_bytes(dl_bytes[i].second.data(), dl_bytes[i].second.size());
    }
    for (size_t i = 0; i < mk_bytes.size(); ++i) {
        pad_to_offset(w, static_cast<size_t>(mkt[i].offset));
        w.put_bytes(mk_bytes[i].second.data(), mk_bytes[i].second.size());
    }

    pad_to_offset(w, off_footer);
    FileFooter f;
    f.checksum = 0;
    f.edit_log_offset = edit_log_abs_offset;
    f.timestamp_ns = now_unix_nanos();
    f.serialize(w);

    std::vector<uint8_t> buf = w.take();
    // 7. Whole-file CRC32 with the checksum field excluded (D-004), patched in.
    const uint32_t crc = compute_file_checksum(buf.data(), buf.size(), off_footer);
    for (int i = 0; i < 4; ++i) {
        buf[static_cast<size_t>(off_footer) + 4 + i] = static_cast<uint8_t>((crc >> (8 * i)) & 0xFF);
    }
    return buf;
}

LqtModel LqtModel::parse(const uint8_t* data, size_t size) {
    ByteReader r(data, size);
    FileHeader h = FileHeader::parse(r); // validates magic/version/size

    // Footer + whole-file integrity check FIRST.
    if (h.footer_offset + LQT_FOOTER_SIZE > size) {
        throw FormatError("LqtModel::parse: footer offset past end of file");
    }
    ByteReader fr(data, size);
    fr.seek(static_cast<size_t>(h.footer_offset));
    FileFooter f = FileFooter::parse(fr);
    const uint32_t actual = compute_file_checksum(data, size, h.footer_offset);
    if (actual != f.checksum) {
        throw IntegrityError("LqtModel::parse: file CRC32 mismatch (corruption detected)");
    }

    // D-019: validate footer.edit_log_offset when set.
    // The field points at the VALUE of the 0x000B TLV chunk inside the metadata
    // region. A non-zero value must lie within [metadata_offset+8, tensor_offset).
    if (f.edit_log_offset != 0) {
        const uint64_t meta_data_start = h.metadata_offset + 8; // skip u64 length prefix
        if (f.edit_log_offset < meta_data_start || f.edit_log_offset >= h.tensor_offset) {
            throw IntegrityError(
                "LqtModel::parse: footer.edit_log_offset is outside the metadata region");
        }
    }

    // Metadata region (D-011): u64 tlv length, then the TLV section.
    ByteReader mr(data, size);
    mr.seek(static_cast<size_t>(h.metadata_offset));
    const uint64_t tlv_len = mr.get_u64();
    MetadataSection sec = MetadataSection::parse(mr, static_cast<size_t>(tlv_len));

    LqtModel m;
    m.header_ = h;

    if (const TlvEntry* e = sec.find(ChunkType::ModelHyperparameters)) {
        m.hyperparams_ = decode_hyperparams(e->value);
    }
    m.module_graph_json_ = get_json(sec, ChunkType::ModuleDefinitions);

    // Tensor descriptors (D-010).
    std::vector<TensorDescriptor> descs;
    if (const TlvEntry* e = sec.find(ChunkType::TensorDescriptors)) {
        ByteReader dr(e->value);
        const uint32_t count = dr.get_u32();
        descs.reserve(count);
        for (uint32_t i = 0; i < count; ++i) descs.push_back(TensorDescriptor::parse(dr));
    }

    // Codebooks / deltas / masks via their tables (absolute offsets).
    if (const TlvEntry* e = sec.find(ChunkType::CodebookTable)) {
        for (const auto& te : decode_table(e->value)) {
            ByteReader cr(data, size); cr.seek(static_cast<size_t>(te.offset));
            m.codebooks_[te.id] = Codebook::parse(cr);
        }
    }
    if (const TlvEntry* e = sec.find(ChunkType::DeltaTable)) {
        for (const auto& te : decode_table(e->value)) {
            ByteReader dr(data, size); dr.seek(static_cast<size_t>(te.offset));
            m.deltas_[te.id] = DeltaBuffer::parse(dr);
        }
    }
    if (const TlvEntry* e = sec.find(ChunkType::SparseMaskTable)) {
        for (const auto& te : decode_table(e->value)) {
            ByteReader sr(data, size); sr.seek(static_cast<size_t>(te.offset));
            m.masks_[te.id] = SparseMask::parse(sr);
        }
    }

    // D-012: parse EditLog chunk if present (absent => empty log on v0.1 files).
    if (const TlvEntry* e = sec.find(ChunkType::EditLog)) {
        ByteReader er(e->value);
        m.edit_log_ = EditLog::parse(er);
    }

    // D-014: parse RTA block chunk if present.
    if (const TlvEntry* e = sec.find(ChunkType::RecursiveWeightMeta)) {
        ByteReader rr(e->value);
        const uint32_t count = rr.get_u32();
        for (uint32_t i = 0; i < count; ++i) {
            std::string name = rr.get_string();
            RtaBlock blk = RtaBlock::parse(rr);
            m.rta_blocks_.emplace(std::move(name), std::move(blk));
        }
    }

    // D-024: parse RecursiveWeight table chunk if present. Buckets, not a
    // one-per-tensor map: a name may repeat across entries.
    if (const TlvEntry* e = sec.find(ChunkType::RecursiveWeightTable)) {
        ByteReader rwr(e->value);
        const uint32_t count = rwr.get_u32();
        for (uint32_t i = 0; i < count; ++i) {
            std::string name = rwr.get_string();
            RecursiveWeight w = RecursiveWeight::parse(rwr);
            m.recursive_weights_[name].push_back(std::move(w));
        }
    }

    // Tensor blobs: walk contiguously from tensor_offset in descriptor order.
    ByteReader br(data, size);
    br.seek(static_cast<size_t>(h.tensor_offset));
    for (const auto& d : descs) {
        const uint16_t blob_cb = br.get_u16();
        const uint16_t blob_dl = br.get_u16();
        const uint16_t blob_mk = br.get_u16();
        if (blob_cb != d.codebook_id || blob_dl != d.delta_id || blob_mk != d.sparse_mask_id) {
            throw FormatError("LqtModel::parse: tensor blob ids disagree with descriptor");
        }
        const size_t ilen = tensor_index_byte_length(d);
        TensorBlob tb;
        tb.desc = d;
        tb.indices.resize(ilen);
        if (ilen > 0) br.get_bytes(tb.indices.data(), ilen);
        br.align_to(LQT_ALIGN_INDEX);
        m.tensors_.push_back(std::move(tb));
    }

    return m;
}

void LqtModel::save(const std::string& path) const {
    const std::vector<uint8_t> buf = serialize_to_bytes();
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) throw LqtError("LqtModel::save: cannot open file for write: " + path);
    out.write(reinterpret_cast<const char*>(buf.data()), static_cast<std::streamsize>(buf.size()));
    if (!out) throw LqtError("LqtModel::save: write failed: " + path);
}

LqtModel LqtModel::load(const std::string& path) {
    std::ifstream in(path, std::ios::binary | std::ios::ate);
    if (!in) throw LqtError("LqtModel::load: cannot open file: " + path);
    const std::streamsize size = in.tellg();
    if (size < static_cast<std::streamsize>(LQT_HEADER_SIZE + LQT_FOOTER_SIZE)) {
        throw FormatError("LqtModel::load: file too small to be a valid LQT");
    }
    in.seekg(0);
    std::vector<uint8_t> buf(static_cast<size_t>(size));
    in.read(reinterpret_cast<char*>(buf.data()), size);
    if (!in) throw LqtError("LqtModel::load: read failed: " + path);
    return parse(buf.data(), buf.size());
}

std::vector<float> LqtModel::reconstruct(const std::string& name) const {
    const TensorBlob* tb = find_tensor(name);
    if (!tb) throw FormatError("LqtModel::reconstruct: tensor not found: " + name);
    const TensorDescriptor& d = tb->desc;

    const size_t count = static_cast<size_t>(d.element_count());

    // D-024: RecursiveTensor reconstruction. Weights are storage buckets, not
    // tensors: a RecursiveWeight is a self-contained W={B,Phi,R,T,epsilon}
    // quintuple with its own codebook index and its own 5D lattice position.
    // The RecursiveTensor (RtaBlock: dims + sparsity) is the compute engine
    // that selects which lattice positions receive computation; each
    // selected position's value comes from the bucket whose T matches it, if
    // one is attached. Positions with no attached bucket fall back to the
    // tensor's own per-element codebook index array (D-009), i.e. a purely
    // structural RecursiveTensor with no RWA state behaves like a Standard
    // tensor shaped by RTA sparsity -- it does not error just for lacking
    // buckets, since RTA structure-with-no-weights is a real, valid case.
    if (d.tensor_type == TensorType::RecursiveTensor) {
        auto it = rta_blocks_.find(d.name);
        if (it == rta_blocks_.end()) {
            throw FormatError("RecursiveTensor has no RTA block");
        }
        const RtaBlock& blk = it->second;

        // RtaReference (Direct/Transformed/Fractal) has no per-element binding
        // in the v1.3 wire format: a reference carries only a target node
        // index and, for Transformed/Fractal, block-level parameters -- no
        // field ties it to a specific output element or to another named
        // tensor. No supplied canon, whitepaper, or test resolves what
        // `target` addresses (the whitepaper's own resolve_references
        // pseudocode calls an undefined _resolve_value and is never
        // completed). Bound this explicitly instead of fabricating a mapping.
        if (!blk.references.empty()) {
            throw FormatError(
                "LqtModel::reconstruct: RecursiveTensor '" + name +
                "' carries RtaReference entries; reference-based "
                "reconstruction is not defined by any supplied specification "
                "(see docs/SPEC_COMPLIANCE.md D-024) and is intentionally "
                "left unimplemented rather than guessed");
        }

        // B term: RecursiveTensor descriptors carry the same per-element
        // codebook index array as any other codebook tensor (D-009); reuse
        // the standard unpack+dequant path.
        const std::vector<uint32_t> idx =
            unpack_indices(tb->indices.data(), tb->indices.size(), count, d.dtype);
        std::vector<float> w;
        w.reserve(count);
        if (d.has_codebook()) {
            const Codebook* cb = codebook(d.codebook_id);
            if (!cb) throw FormatError("LqtModel::reconstruct: codebook missing for " + name);
            w = reconstruct_standard(*cb, idx, d.scale);
        } else {
            for (uint32_t q : idx) w.push_back(dequant_affine(static_cast<int64_t>(q), d.scale, d.zero_point));
        }
        if (d.has_delta()) {
            if (const DeltaBuffer* dl = delta(d.delta_id)) dl->apply(w.data(), w.size());
        }

        // Sparse structure (DD-04): RLE and CsrCscCsf carry literal f32
        // values on the wire, which are authoritative and override the B
        // term for the positions they cover. Hierarchical and
        // CompressedBitmap carry exact per-element presence (no values) and
        // zero out absent positions. PerDimension carries only aggregate
        // per-axis density, not exact membership -- it cannot be turned into
        // an exact mask without inventing a rule, so it is bounded like the
        // reference case above rather than guessed. Uniform means fully
        // dense (no masking).
        switch (blk.sparse_encoding) {
            case SparseEncoding::Uniform:
                break;
            case SparseEncoding::PerDimension:
                throw FormatError(
                    "LqtModel::reconstruct: RecursiveTensor '" + name +
                    "' uses PerDimension sparse encoding, which records only "
                    "aggregate per-axis density, not exact element membership; "
                    "exact reconstruction is not defined (see D-024)");
            case SparseEncoding::Hierarchical: {
                const HierarchicalSparse h = sparse_parse_hierarchical(blk.sparse_payload);
                if (static_cast<size_t>(h.total_elements) != count) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' Hierarchical sparse total_elements disagrees with descriptor element_count");
                }
                std::vector<bool> present(count, false);
                for (uint32_t flat : h.l1_indices) {
                    if (flat < count) present[flat] = true;
                }
                for (size_t i = 0; i < count; ++i) {
                    if (!present[i]) w[i] = 0.0f;
                }
                break;
            }
            case SparseEncoding::RLE: {
                std::vector<float> dense(count, 0.0f);
                for (const auto& run : sparse_parse_rle(blk.sparse_payload)) {
                    for (uint32_t k = 0; k < run.length && static_cast<size_t>(run.start) + k < count; ++k) {
                        dense[static_cast<size_t>(run.start) + k] = run.value;
                    }
                }
                w = std::move(dense);
                break;
            }
            case SparseEncoding::CompressedBitmap: {
                const BitmapSparse bm = sparse_parse_bitmap(blk.sparse_payload);
                if (static_cast<size_t>(bm.num_elements) != count) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' CompressedBitmap num_elements disagrees with descriptor element_count");
                }
                for (size_t i = 0; i < count; ++i) {
                    const bool set = (bm.words[i / 64] >> (i % 64)) & 1u;
                    if (!set) w[i] = 0.0f;
                }
                break;
            }
            case SparseEncoding::CsrCscCsf: {
                const CsrSparse csr = sparse_parse_csr(blk.sparse_payload);
                const uint32_t ncols = blk.dims.dim_sizes[1];
                if (static_cast<size_t>(csr.nrows) * static_cast<size_t>(ncols) != count) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' CSR nrows*dim_sizes[1] disagrees with descriptor element_count");
                }
                std::vector<float> dense(count, 0.0f);
                for (size_t r = 0; r < csr.nrows; ++r) {
                    for (uint32_t p = csr.row_ptr[r]; p < csr.row_ptr[r + 1]; ++p) {
                        const size_t flat = r * static_cast<size_t>(ncols) + csr.col_idx[p];
                        if (flat < count) dense[flat] = csr.values[p];
                    }
                }
                w = std::move(dense);
                break;
            }
        }

        // Weight buckets (D-024): each attached RecursiveWeight is a
        // self-contained storage unit -- its own B (codebook index) and its
        // own T (5D lattice position). Where one is attached, it is
        // authoritative for its own position and overrides whatever the
        // structural base path above computed there (a bucket's value is not
        // a modulation of the base term; it *is* the value for that cell,
        // per the RWA storage doctrine: weights carry state, RTA only
        // selects which positions compute). T is rounded to the nearest
        // integer coordinate and flattened row-major against blk.dims
        // (matching DenseTensor5D's convention in rta_ops.h and the CSR
        // flattening used above), consistent with T's documented role
        // ("exactly 5 floats mapping to RTA dims d0..d4",
        // recursive_weight.h).
        if (const std::vector<RecursiveWeight>* buckets = get_recursive_weights(name)) {
            std::vector<bool> bucket_written(count, false);
            for (const RecursiveWeight& rwv : *buckets) {
                size_t flat = 0;
                for (size_t axis = 0; axis < LQT_RTA_RANK; ++axis) {
                    const uint32_t dim_sz = blk.dims.dim_sizes[axis];
                    const long rounded = std::lround(rwv.tensor_position[axis]);
                    if (rounded < 0 || static_cast<uint32_t>(rounded) >= dim_sz) {
                        throw FormatError(
                            "LqtModel::reconstruct: RecursiveTensor '" + name +
                            "' has a RecursiveWeight bucket whose tensor_position[" +
                            std::to_string(axis) + "] does not map to a valid "
                            "coordinate in the tensor's own dims");
                    }
                    flat = flat * dim_sz + static_cast<uint32_t>(rounded);
                }
                if (flat >= count) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' bucket position resolves outside the descriptor's element count");
                }
                if (bucket_written[flat]) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' has two RecursiveWeight buckets mapping to the same position; "
                                       "no rule resolves this ambiguity");
                }
                const Codebook* cb = codebook(d.codebook_id);
                if (!cb) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' has a RecursiveWeight bucket but no codebook to resolve its base_index against");
                }
                if (rwv.base_index >= cb->num_vectors()) {
                    throw FormatError("LqtModel::reconstruct: RecursiveTensor '" + name +
                                       "' bucket base_index out of range for its codebook");
                }
                const float eps_mean = rwv.error.empty()
                    ? 0.0f
                    : std::accumulate(rwv.error.begin(), rwv.error.end(), 0.0f) /
                          static_cast<float>(rwv.error.size());
                w[flat] = cb->scalar(rwv.base_index) * d.scale + rwv.phase_at(0.0) + eps_mean;
                bucket_written[flat] = true;
            }
        }

        if (d.has_mask()) {
            if (const SparseMask* mk = sparse_mask(d.sparse_mask_id)) mk->apply(w.data(), w.size());
        }
        return w;
    }

    // D-015: codebook-less standard tensors fall back to affine dequantization.
    if (!d.has_codebook()) {
        const std::vector<uint32_t> idx =
            unpack_indices(tb->indices.data(), tb->indices.size(), count, d.dtype);
        std::vector<float> w;
        w.reserve(count);
        for (uint32_t q : idx) {
            w.push_back(dequant_affine(static_cast<int64_t>(q), d.scale, d.zero_point));
        }
        if (d.has_delta()) {
            if (const DeltaBuffer* dl = delta(d.delta_id)) dl->apply(w.data(), w.size());
        }
        if (d.has_mask()) {
            if (const SparseMask* mk = sparse_mask(d.sparse_mask_id)) mk->apply(w.data(), w.size());
        }
        return w;
    }

    const Codebook* cb = codebook(d.codebook_id);
    if (!cb) throw FormatError("LqtModel::reconstruct: codebook missing for " + name);

    const std::vector<uint32_t> idx =
        unpack_indices(tb->indices.data(), tb->indices.size(), count, d.dtype);
    std::vector<float> w = reconstruct_standard(*cb, idx, d.scale);

    if (d.has_delta()) {
        if (const DeltaBuffer* dl = delta(d.delta_id)) dl->apply(w.data(), w.size());
    }
    if (d.has_mask()) {
        if (const SparseMask* mk = sparse_mask(d.sparse_mask_id)) mk->apply(w.data(), w.size());
    }
    return w;
}

// ---- D-013: mutation surface --------------------------------------------------
namespace {
inline uint64_t mutation_timestamp_ns() {
    using namespace std::chrono;
    return static_cast<uint64_t>(
        duration_cast<nanoseconds>(system_clock::now().time_since_epoch()).count());
}
} // namespace

void LqtModel::edit_codebook(uint16_t codebook_id, uint32_t vector_idx,
                             const std::vector<float>& new_value) {
    Codebook* cb = codebook_mut(codebook_id);
    if (!cb) throw ValidationError("LqtModel::edit_codebook: unknown codebook id");
    if (vector_idx >= cb->num_vectors()) {
        throw ValidationError("LqtModel::edit_codebook: vector_idx out of range");
    }
    if (new_value.size() != cb->vector_dim()) {
        throw ValidationError("LqtModel::edit_codebook: vector dim mismatch");
    }
    const std::string target = "codebook:" + std::to_string(codebook_id);
    // Snapshot pre-mutation state for rollback.
    MutationSnapshot snap;
    snap.type        = MutationType::CodebookEdit;
    snap.target      = target;
    snap.codebook_id = codebook_id;
    snap.vector_idx  = vector_idx;
    snap.prev_vectors.resize(cb->vector_dim());
    {
        const float* prev = cb->vector(vector_idx);
        for (uint32_t j = 0; j < cb->vector_dim(); ++j) snap.prev_vectors[j] = prev[j];
    }
    EditLogEntry entry = make_entry(
        MutationType::CodebookEdit, target,
        new_value.data(),
        new_value.size() * sizeof(float),
        edit_log_.tail_hash(),
        mutation_timestamp_ns());
    edit_log_.append(std::move(entry));
    cb->set_vector(vector_idx, new_value.data());
    undo_stack_.push_back(std::move(snap));
}

void LqtModel::edit_codebook(uint16_t codebook_id, uint32_t vector_idx,
                             float scalar_value) {
    edit_codebook(codebook_id, vector_idx, std::vector<float>{scalar_value});
}

void LqtModel::update_delta(uint16_t delta_id, const DeltaBuffer& replacement) {
    auto it = deltas_.find(delta_id);
    if (it == deltas_.end()) {
        throw ValidationError("LqtModel::update_delta: unknown delta id");
    }
    const std::string target = "delta:" + std::to_string(delta_id);
    MutationSnapshot snap;
    snap.type       = MutationType::DeltaUpdate;
    snap.target     = target;
    snap.prev_delta = it->second; // current delta buffer before replacement
    EditLogEntry entry = make_entry(
        MutationType::DeltaUpdate, target,
        replacement.values.data(),
        replacement.values.size() * sizeof(float),
        edit_log_.tail_hash(),
        mutation_timestamp_ns());
    edit_log_.append(std::move(entry));
    DeltaBuffer copy = replacement;
    copy.delta_id = delta_id;
    it->second = std::move(copy);
    undo_stack_.push_back(std::move(snap));
}

void LqtModel::update_delta(const DeltaBuffer& replacement) {
    update_delta(replacement.delta_id, replacement);
}

void LqtModel::hot_swap_module(const std::string& module_name,
                               std::vector<uint8_t> new_blob) {
    MutationSnapshot snap;
    snap.type        = MutationType::ModuleSwap;
    snap.target      = module_name;
    snap.module_name = module_name;
    // Capture previous state: check tensors_ first.
    snap.was_tensor  = false;
    for (const auto& t : tensors_) {
        if (t.desc.name == module_name) {
            snap.prev_blob  = t.indices;
            snap.was_tensor = true;
            break;
        }
    }
    if (!snap.was_tensor) {
        auto mit = modules_.find(module_name);
        if (mit != modules_.end()) snap.prev_blob = mit->second;
    }
    EditLogEntry entry = make_entry(
        MutationType::ModuleSwap, module_name,
        new_blob.data(), new_blob.size(),
        edit_log_.tail_hash(),
        mutation_timestamp_ns());
    edit_log_.append(std::move(entry));
    // If a tensor of this name exists, swap its packed-index bytes; otherwise
    // store the blob in the modules_ map as an opaque named module payload.
    bool applied = false;
    for (auto& t : tensors_) {
        if (t.desc.name == module_name) {
            t.indices = std::move(new_blob);
            applied = true;
            break;
        }
    }
    if (!applied) {
        modules_[module_name] = std::move(new_blob);
    }
    undo_stack_.push_back(std::move(snap));
}

// ---- D-014: RTA block accessors -----------------------------------------------
void LqtModel::add_rta_block(const std::string& name, RtaBlock block) {
    rta_blocks_[name] = std::move(block);
}

const RtaBlock* LqtModel::get_rta_block(const std::string& name) const {
    auto it = rta_blocks_.find(name);
    return it == rta_blocks_.end() ? nullptr : &it->second;
}

// ---- D-024: RecursiveWeight (storage bucket) accessors -------------------------
void LqtModel::add_recursive_weight(const std::string& name, RecursiveWeight weight) {
    weight.validate();
    recursive_weights_[name].push_back(std::move(weight));
}

const std::vector<RecursiveWeight>* LqtModel::get_recursive_weights(const std::string& name) const {
    auto it = recursive_weights_.find(name);
    return it == recursive_weights_.end() ? nullptr : &it->second;
}

// ---- D-025: logged RecursiveWeight bucket edits + RecursiveTensor attach/detach ----
namespace {
// Flat lattice position of a bucket's T against RTA dims; throws ValidationError
// (mutation-time) for the same conditions D-024 reconstruct() bounds.
size_t d025_bucket_flat(const RecursiveWeight& rw, const RtaBlock& blk, const std::string& name) {
    size_t flat = 0;
    for (size_t axis = 0; axis < LQT_RTA_RANK; ++axis) {
        const uint32_t dim_sz = blk.dims.dim_sizes[axis];
        const long rounded = std::lround(rw.tensor_position[axis]);
        if (rounded < 0 || static_cast<uint32_t>(rounded) >= dim_sz) {
            throw ValidationError("LqtModel D-025: bucket tensor_position[" + std::to_string(axis) +
                                  "] outside RTA dims of '" + name + "'");
        }
        flat = flat * dim_sz + static_cast<uint32_t>(rounded);
    }
    return flat;
}

void d025_check_bucket_set(const std::vector<RecursiveWeight>& buckets, const TensorBlob* tb,
                           const RtaBlock* blk, const Codebook* cb, const std::string& name) {
    std::vector<bool> seen;
    if (blk) {
        size_t total = 1;
        for (size_t a = 0; a < LQT_RTA_RANK; ++a) total *= blk->dims.dim_sizes[a];
        seen.assign(total, false);
    }
    for (const RecursiveWeight& rw : buckets) {
        rw.validate();
        if (tb && tb->desc.has_codebook()) {
            if (!cb) throw ValidationError("LqtModel D-025: codebook missing for '" + name + "'");
            if (rw.base_index >= cb->num_vectors())
                throw ValidationError("LqtModel D-025: bucket base_index out of range for '" + name + "'");
        }
        if (blk) {
            const size_t flat = d025_bucket_flat(rw, *blk, name);
            if (seen[flat])
                throw ValidationError("LqtModel D-025: two buckets of '" + name +
                                      "' resolve to the same lattice position");
            seen[flat] = true;
        }
    }
}

std::vector<uint8_t> d025_rw_payload(const std::vector<std::pair<uint32_t, RecursiveWeight>>& edits) {
    ByteWriter w;
    w.put_u32(static_cast<uint32_t>(edits.size()));
    for (const auto& e : edits) { w.put_u32(e.first); e.second.serialize(w); }
    return w.take();
}
} // namespace

void LqtModel::edit_recursive_weights(const std::string& name,
                                      const std::vector<std::pair<uint32_t, RecursiveWeight>>& edits) {
    auto it = recursive_weights_.find(name);
    if (it == recursive_weights_.end())
        throw ValidationError("LqtModel::edit_recursive_weights: no buckets attached to '" + name + "'");
    if (edits.empty())
        throw ValidationError("LqtModel::edit_recursive_weights: empty edit set for '" + name + "'");
    std::vector<RecursiveWeight> proposed = it->second;
    std::vector<bool> touched(proposed.size(), false);
    for (const auto& e : edits) {
        if (e.first >= proposed.size())
            throw ValidationError("LqtModel::edit_recursive_weights: slot out of range for '" + name + "'");
        if (touched[e.first])
            throw ValidationError("LqtModel::edit_recursive_weights: slot edited twice in one mutation");
        touched[e.first] = true;
        proposed[e.first] = e.second;
    }
    const TensorBlob* tb = find_tensor(name);
    d025_check_bucket_set(proposed, tb, get_rta_block(name),
                          tb && tb->desc.has_codebook() ? codebook(tb->desc.codebook_id) : nullptr, name);
    MutationSnapshot snap;
    snap.type   = MutationType::RecursiveWeightEdit;
    snap.target = "rw:" + name;
    snap.prev_buckets.reserve(edits.size());
    for (const auto& e : edits) snap.prev_buckets.emplace_back(e.first, it->second[e.first]);
    const std::vector<uint8_t> payload = d025_rw_payload(edits);
    edit_log_.append(make_entry(MutationType::RecursiveWeightEdit, snap.target,
                                payload.data(), payload.size(), edit_log_.tail_hash(),
                                mutation_timestamp_ns()));
    it->second = std::move(proposed);
    undo_stack_.push_back(std::move(snap));
}

void LqtModel::edit_recursive_weight(const std::string& name, uint32_t slot, const RecursiveWeight& w) {
    edit_recursive_weights(name, {{slot, w}});
}

void LqtModel::attach_recursive_tensor(TensorDescriptor desc, std::vector<uint8_t> index_bytes,
                                       RtaBlock block, std::vector<RecursiveWeight> buckets) {
    desc.validate();
    if (desc.tensor_type != TensorType::RecursiveTensor)
        throw ValidationError("LqtModel::attach_recursive_tensor: descriptor is not a RecursiveTensor");
    if (index_bytes.size() != tensor_index_byte_length(desc))
        throw ValidationError("LqtModel::attach_recursive_tensor: index byte length disagrees with descriptor");
    block.validate();
    for (size_t a = 0; a < LQT_RTA_RANK; ++a) {
        if (block.dims.dim_sizes[a] != desc.shape[a])
            throw ValidationError("LqtModel::attach_recursive_tensor: RTA dims disagree with descriptor shape");
    }
    const Codebook* cb = desc.has_codebook() ? codebook(desc.codebook_id) : nullptr;
    if (desc.has_codebook() && !cb)
        throw ValidationError("LqtModel::attach_recursive_tensor: codebook missing");
    if (desc.has_delta() && !delta(desc.delta_id))
        throw ValidationError("LqtModel::attach_recursive_tensor: delta buffer missing");
    TensorBlob probe{desc, {}};
    d025_check_bucket_set(buckets, &probe, &block, cb, desc.name);

    const std::string name = desc.name;
    MutationSnapshot snap;
    snap.type   = MutationType::TensorAttach;
    snap.target = "tensor:" + name;
    for (size_t i = 0; i < tensors_.size(); ++i) {
        if (tensors_[i].desc.name == name) {
            snap.had_tensor = true; snap.tensor_pos = i; snap.prev_tensor = tensors_[i]; break;
        }
    }
    if (auto rit = rta_blocks_.find(name); rit != rta_blocks_.end()) { snap.had_rta = true; snap.prev_rta = rit->second; }
    if (auto bit = recursive_weights_.find(name); bit != recursive_weights_.end()) {
        snap.had_buckets = true; snap.prev_all_buckets = bit->second;
    }
    ByteWriter pw;
    desc.serialize(pw);
    pw.put_u32(static_cast<uint32_t>(index_bytes.size()));
    pw.put_bytes(index_bytes.data(), index_bytes.size());
    block.serialize(pw);
    pw.put_u32(static_cast<uint32_t>(buckets.size()));
    for (const RecursiveWeight& rw : buckets) rw.serialize(pw);
    const std::vector<uint8_t> payload = pw.take();
    edit_log_.append(make_entry(MutationType::TensorAttach, snap.target, payload.data(), payload.size(),
                                edit_log_.tail_hash(), mutation_timestamp_ns()));
    if (snap.had_tensor) tensors_[snap.tensor_pos] = TensorBlob{std::move(desc), std::move(index_bytes)};
    else                 tensors_.push_back(TensorBlob{std::move(desc), std::move(index_bytes)});
    rta_blocks_[name] = std::move(block);
    if (buckets.empty()) recursive_weights_.erase(name);
    else                 recursive_weights_[name] = std::move(buckets);
    undo_stack_.push_back(std::move(snap));
}

void LqtModel::detach_tensor(const std::string& name) {
    MutationSnapshot snap;
    snap.type   = MutationType::TensorDetach;
    snap.target = "tensor:" + name;
    for (size_t i = 0; i < tensors_.size(); ++i) {
        if (tensors_[i].desc.name == name) {
            snap.had_tensor = true; snap.tensor_pos = i; snap.prev_tensor = tensors_[i]; break;
        }
    }
    if (!snap.had_tensor) throw ValidationError("LqtModel::detach_tensor: unknown tensor '" + name + "'");
    if (auto rit = rta_blocks_.find(name); rit != rta_blocks_.end()) { snap.had_rta = true; snap.prev_rta = rit->second; }
    if (auto bit = recursive_weights_.find(name); bit != recursive_weights_.end()) {
        snap.had_buckets = true; snap.prev_all_buckets = bit->second;
    }
    edit_log_.append(make_entry(MutationType::TensorDetach, snap.target, name.data(), name.size(),
                                edit_log_.tail_hash(), mutation_timestamp_ns()));
    tensors_.erase(tensors_.begin() + static_cast<std::ptrdiff_t>(snap.tensor_pos));
    rta_blocks_.erase(name);
    recursive_weights_.erase(name);
    undo_stack_.push_back(std::move(snap));
}

// ---- D-019: rollback ----------------------------------------------------------
void LqtModel::rollback(size_t n) {
    if (n == 0) return;
    if (n > undo_stack_.size()) {
        throw ValidationError("LqtModel::rollback: n exceeds undo stack depth");
    }
    // Restore the last n mutations in reverse order.
    for (size_t i = 0; i < n; ++i) {
        const MutationSnapshot& snap = undo_stack_[undo_stack_.size() - 1 - i];
        switch (snap.type) {
            case MutationType::CodebookEdit: {
                Codebook* cb = codebook_mut(snap.codebook_id);
                if (cb) cb->set_vector(snap.vector_idx, snap.prev_vectors.data());
                break;
            }
            case MutationType::DeltaUpdate: {
                deltas_[snap.prev_delta.delta_id] = snap.prev_delta;
                break;
            }
            case MutationType::ModuleSwap: {
                if (snap.was_tensor) {
                    for (auto& t : tensors_) {
                        if (t.desc.name == snap.module_name) {
                            t.indices = snap.prev_blob;
                            break;
                        }
                    }
                } else {
                    if (snap.prev_blob.empty()) {
                        modules_.erase(snap.module_name);
                    } else {
                        modules_[snap.module_name] = snap.prev_blob;
                    }
                }
                break;
            }
            case MutationType::RecursiveWeightEdit: {
                const std::string name = snap.target.substr(3); // strip "rw:"
                auto& vec = recursive_weights_[name];
                for (auto pit = snap.prev_buckets.rbegin(); pit != snap.prev_buckets.rend(); ++pit) {
                    vec[pit->first] = pit->second;
                }
                break;
            }
            case MutationType::TensorAttach:
            case MutationType::TensorDetach: {
                const std::string name = snap.target.substr(7); // strip "tensor:"
                if (snap.type == MutationType::TensorAttach) {
                    if (snap.had_tensor) {
                        tensors_[snap.tensor_pos] = snap.prev_tensor;
                    } else {
                        for (size_t k = 0; k < tensors_.size(); ++k) {
                            if (tensors_[k].desc.name == name) {
                                tensors_.erase(tensors_.begin() + static_cast<std::ptrdiff_t>(k));
                                break;
                            }
                        }
                    }
                } else {
                    tensors_.insert(tensors_.begin() + static_cast<std::ptrdiff_t>(snap.tensor_pos),
                                    snap.prev_tensor);
                }
                if (snap.had_rta) rta_blocks_[name] = snap.prev_rta; else rta_blocks_.erase(name);
                if (snap.had_buckets) recursive_weights_[name] = snap.prev_all_buckets;
                else recursive_weights_.erase(name);
                break;
            }
            default:
                break;
        }
    }
    // Truncate undo stack.
    undo_stack_.resize(undo_stack_.size() - n);
    // Truncate the edit log to match (D-019; provided by Agent Beta).
    edit_log_.truncate(n);
}

} // namespace lqt
