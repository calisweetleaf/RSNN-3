// lqt/model.h — LQTModel: top-level container assembly, parsing, reconstruction.
//
// Council module: A10 (integration), LEAD. This is the capstone that assembles
// every other module into a complete .lqt file and reads it back.
// Canon: lqt.md §2.1 (Binary Layout Overview), §3.1 (reconstruction), §9.1
//        (Core Model Class).
//
// File layout produced/consumed (canon §2.1 with documented framing):
//   [0x00]            FileHeader (36 bytes, D-001)
//   [metadata_offset] u64 tlv_length (D-011) + TLV MetadataSection
//   [.. 64B-aligned ] Codebook blocks      (located via CodebookTable 0x0005)
//   [tensor_offset]   Tensor blobs          (walked in descriptor order, D-009)
//   [.. 4B-aligned ]  Delta buffers         (located via DeltaTable 0x0006)
//   [.. 4B-aligned ]  Sparse masks          (located via SparseMaskTable 0x0007)
//   [footer_offset]   FileFooter (64 bytes), checksum = whole-file CRC32 (D-004)
//
// DESIGN DECISION D-009: tensor blobs are stored contiguously starting at
//   header.tensor_offset, in the same order as the TensorDescriptors chunk.
//   Each blob = [codebook_id:u16][delta_id:u16][sparse_mask_id:u16][indices...]
//   padded to LQT_ALIGN_INDEX (16). Index byte length is derived from the
//   descriptor (element_count * dtype_bits, INT4 packs 2/byte) — no per-tensor
//   offset table is needed (canon defines none).
//
// DESIGN DECISION D-010: the TensorDescriptors chunk (0x0002) value is framed
//   as [u32 count][descriptor...]. Canon gives no multi-descriptor framing.
//
// DESIGN DECISION D-011: the metadata region begins with a u64 giving the TLV
//   byte length, making the region self-delimiting (the header carries only
//   metadata_offset/tensor_offset/footer_offset, and codebooks sit between
//   metadata and tensor_offset, so an explicit length is required to find the
//   codebook region without ordering tricks).
#pragma once

#include <cstdint>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

#include "lqt/codebook.h"
#include "lqt/delta.h"
#include "lqt/descriptor.h"
#include "lqt/edit_log.h"
#include "lqt/header.h"
#include "lqt/recursive_weight.h"
#include "lqt/rta.h"
#include "lqt/sparse_mask.h"

namespace lqt {

// One tensor's stored data: its descriptor + raw packed quantized index bytes.
struct TensorBlob {
    TensorDescriptor     desc;
    std::vector<uint8_t> indices; // packed quantized indices (dtype-dependent)
};

// Snapshot of the state of one component before a mutation, enabling rollback.
// One snapshot is pushed per mutation call; rollback(n) pops the last n.
struct MutationSnapshot {
    MutationType             type;
    std::string              target;

    // CodebookEdit: previous vector at the edited index.
    uint16_t                 codebook_id   = 0;
    uint32_t                 vector_idx    = 0;
    std::vector<float>       prev_vectors; // full prev vector (dim == codebook.vector_dim())

    // DeltaUpdate: previous delta buffer.
    DeltaBuffer              prev_delta;

    // ModuleSwap: previous tensor indices OR modules_ entry.
    std::string              module_name;
    std::vector<uint8_t>     prev_blob;
    bool                     was_tensor = false; // true if module was in tensors_

    // RecursiveWeightEdit (D-025): previous bucket values at the edited slots.
    std::vector<std::pair<uint32_t, RecursiveWeight>> prev_buckets;

    // TensorAttach / TensorDetach (D-025): full previous state of the name.
    bool                         had_tensor  = false;
    size_t                       tensor_pos  = 0;   // index in tensors_
    TensorBlob                   prev_tensor;
    bool                         had_rta     = false;
    RtaBlock                     prev_rta;
    bool                         had_buckets = false;
    std::vector<RecursiveWeight> prev_all_buckets;
};

class LqtModel {
public:
    LqtModel() = default;

    // ---- builders ----------------------------------------------------------
    void set_hyperparam(const std::string& key, float value);
    void set_module_graph_json(std::string json) { module_graph_json_ = std::move(json); }
    void add_codebook(Codebook cb) { codebooks_[cb.id()] = std::move(cb); }
    void add_tensor(TensorDescriptor desc, std::vector<uint8_t> index_bytes) {
        tensors_.push_back(TensorBlob{std::move(desc), std::move(index_bytes)});
    }
    void add_delta(DeltaBuffer d) { deltas_[d.delta_id] = std::move(d); }
    void add_sparse_mask(SparseMask m) { masks_[m.mask_id] = std::move(m); }

    // ---- I/O ---------------------------------------------------------------
    std::vector<uint8_t> serialize_to_bytes() const;        // full file image
    void save(const std::string& path) const;               // write image to disk
    static LqtModel parse(const uint8_t* data, size_t size); // verifies CRC; throws
    static LqtModel load(const std::string& path);           // read + parse

    // ---- access ------------------------------------------------------------
    const FileHeader& header() const { return header_; }
    const std::vector<TensorBlob>& tensors() const { return tensors_; }
    const std::vector<std::pair<std::string, float>>& hyperparams() const { return hyperparams_; }
    const std::string& module_graph_json() const { return module_graph_json_; }

    const Codebook* codebook(uint16_t id) const {
        auto it = codebooks_.find(id); return it == codebooks_.end() ? nullptr : &it->second;
    }
    const DeltaBuffer* delta(uint16_t id) const {
        auto it = deltas_.find(id); return it == deltas_.end() ? nullptr : &it->second;
    }
    const SparseMask* sparse_mask(uint16_t id) const {
        auto it = masks_.find(id); return it == masks_.end() ? nullptr : &it->second;
    }
    const TensorBlob* find_tensor(const std::string& name) const;

    // Mutable codebook access for codebook-edit mutations (A7 integration).
    Codebook* codebook_mut(uint16_t id) {
        auto it = codebooks_.find(id); return it == codebooks_.end() ? nullptr : &it->second;
    }

    // ---- reconstruction (canon §3.1) --------------------------------------
    // Reconstruct full-precision weights for a standard tensor by name:
    //   w = codebook[idx]*scale  (+ delta)  (* mask)
    std::vector<float> reconstruct(const std::string& name) const;

    // ---- edit log (D-012) --------------------------------------------------
    const EditLog& edit_log() const { return edit_log_; }

    // ---- mutation surface (D-013) -----------------------------------------
    // Each method validates bounds, appends a tamper-evident EditLogEntry,
    // and applies the change. See src/model.cpp for implementations.
    void edit_codebook(uint16_t codebook_id, uint32_t vector_idx,
                       const std::vector<float>& new_value);
    // Scalar-codebook convenience overload (vector_dim == 1).
    void edit_codebook(uint16_t codebook_id, uint32_t vector_idx, float scalar_value);
    void update_delta(uint16_t delta_id, const DeltaBuffer& replacement);
    // Convenience: derive delta_id from replacement.delta_id.
    void update_delta(const DeltaBuffer& replacement);
    void hot_swap_module(const std::string& module_name,
                         std::vector<uint8_t> new_blob);

    // ---- RTA blocks (D-014) -----------------------------------------------
    void add_rta_block(const std::string& name, RtaBlock block);
    const RtaBlock* get_rta_block(const std::string& name) const;

    // ---- Recursive weights (D-024) -----------------------------------------
    // Weights are storage buckets, not tensors: each RecursiveWeight is one
    // self-contained W={B,Phi,R,T,epsilon} quintuple (its own codebook index
    // B and its own 5D lattice position T). A RecursiveTensor is the compute
    // engine over a *set* of these buckets -- its RtaBlock (dims + sparsity)
    // selects which lattice positions receive computation, and each selected
    // position's value comes from the bucket whose T matches that position.
    // One tensor name may have zero, one, or many buckets attached.
    void add_recursive_weight(const std::string& name, RecursiveWeight weight);
    const std::vector<RecursiveWeight>* get_recursive_weights(const std::string& name) const;

    // ---- D-025: logged RecursiveWeight / RecursiveTensor mutations ----------
    // edit_recursive_weights replaces the buckets at the given slot indices of
    // `name` (B, Phi, R, T, epsilon, coeff -- the whole quintuple) as ONE
    // mutation: one hash-chained EditLog entry (payload = [u32 slot][RW
    // bytes]...) and one undo snapshot. Validates each replacement, that B
    // indexes the tensor's codebook, that T lies inside the tensor's RTA dims,
    // and that no two buckets of the name resolve to the same lattice position
    // (the D-024 reconstruction bounds) BEFORE anything is applied.
    void edit_recursive_weights(const std::string& name,
                                const std::vector<std::pair<uint32_t, RecursiveWeight>>& edits);
    void edit_recursive_weight(const std::string& name, uint32_t slot, const RecursiveWeight& w);
    // attach_recursive_tensor adds (or replaces, when the name exists) one
    // RecursiveTensor: descriptor + packed index bytes + RtaBlock + its
    // buckets, as one logged mutation. detach_tensor removes all four.
    // Both are undone exactly by rollback().
    void attach_recursive_tensor(TensorDescriptor desc, std::vector<uint8_t> index_bytes,
                                 RtaBlock block, std::vector<RecursiveWeight> buckets);
    void detach_tensor(const std::string& name);

    // ---- undo stack (D-019) -----------------------------------------------
    // rollback(n) reverses the last n mutations atomically. Throws
    // ValidationError if n > undo_stack_.size(). Calls EditLog::truncate(n).
    void rollback(size_t n);
    size_t undo_depth() const { return undo_stack_.size(); }

private:
    FileHeader                                  header_;
    std::vector<std::pair<std::string, float>>  hyperparams_;
    std::string                                 module_graph_json_;
    std::vector<TensorBlob>                     tensors_;
    std::map<uint16_t, Codebook>                codebooks_;
    std::map<uint16_t, DeltaBuffer>             deltas_;
    std::map<uint16_t, SparseMask>              masks_;
    EditLog                                     edit_log_;
    std::unordered_map<std::string, RtaBlock>   rta_blocks_;
    std::unordered_map<std::string, std::vector<RecursiveWeight>> recursive_weights_;
    std::unordered_map<std::string, std::vector<uint8_t>> modules_;
    std::vector<MutationSnapshot>               undo_stack_;
};

// Number of packed index bytes a descriptor's quantized blob occupies.
size_t tensor_index_byte_length(const TensorDescriptor& desc);

} // namespace lqt
