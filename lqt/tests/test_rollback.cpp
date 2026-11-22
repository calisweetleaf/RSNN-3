// tests/test_rollback.cpp — Rollback / undo semantics on the model + edit log.
//
// Council module: A7 (mutation safety) + A10 (model integration).
// Canon: lqt.md §5.3 (Edit Log Management), §4.4, §8.
//
// Each TEST_CASE is fully self-contained: it constructs its own LqtModel from
// scratch. The rollback() / undo_depth() entry points are implemented by the
// model layer (Agent Apex). Truncate is owned here on the EditLog itself.
#include "test_framework.h"

#include "lqt/codebook.h"
#include "lqt/descriptor.h"
#include "lqt/edit_log.h"
#include "lqt/error.h"
#include "lqt/format.h"
#include "lqt/model.h"

#include <cstdio>
#include <cstring>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <unistd.h>

using namespace lqt;

// ============================================================================
// Test helper — build a tiny self-consistent model with one scalar codebook
// (id 0, 4 entries) and one INT8 tensor "w0" of 4 elements indexing it.
// ============================================================================
static LqtModel build_test_model() {
    LqtModel m;

    Codebook cb(/*id=*/0, /*num_vectors=*/4, /*vector_dim=*/1);
    cb.set_scalar(0, 1.0f);
    cb.set_scalar(1, 2.0f);
    cb.set_scalar(2, 3.0f);
    cb.set_scalar(3, 4.0f);
    m.add_codebook(std::move(cb));

    TensorDescriptor d;
    d.name           = "w0";
    d.tensor_type    = TensorType::Standard;
    d.dtype          = DType::INT8;
    d.shape          = {4};
    d.codebook_id    = 0;
    d.delta_id       = LQT_ID_NONE;
    d.sparse_mask_id = LQT_ID_NONE;
    d.scale          = 1.0f;
    // INT8: 1 byte per element. Indices {0,1,2,3} -> raw bytes.
    m.add_tensor(d, std::vector<uint8_t>{0, 1, 2, 3});
    return m;
}

// ============================================================================
// TEST 1 — edit_log_offset is nonzero after save (basic wiring check)
// ============================================================================
TEST_CASE(rollback_edit_log_offset_nonzero_after_save) {
    LqtModel m = build_test_model();
    // Force at least one edit-log entry so the offset can be meaningful.
    m.edit_codebook(/*codebook_id=*/0, /*index=*/1, /*value=*/9.5f);

    char tmp[] = "/tmp/lqt_rollback_XXXXXX";
    int fd = mkstemp(tmp);
    if (fd >= 0) ::close(fd);
    m.save(tmp);

    LqtModel reloaded = LqtModel::load(tmp);
    // The header carries metadata/tensor/footer offsets; the footer carries
    // edit_log_offset. We can't peek at the footer through the public API, but
    // we CAN peek at the raw bytes: read the file in, parse the footer.
    std::ifstream in(tmp, std::ios::binary);
    in.seekg(0, std::ios::end);
    const size_t fsize = static_cast<size_t>(in.tellg());
    in.seekg(0, std::ios::beg);
    std::vector<uint8_t> buf(fsize);
    in.read(reinterpret_cast<char*>(buf.data()), static_cast<std::streamsize>(fsize));
    in.close();

    const uint64_t footer_off = reloaded.header().footer_offset;
    // edit_log_offset is at footer + 8 (after 4-byte magic + 4-byte checksum), LE u64.
    uint64_t edit_log_off = 0;
    for (int i = 0; i < 8; ++i) {
        edit_log_off |= static_cast<uint64_t>(buf[footer_off + 8 + i]) << (8 * i);
    }
    CHECK(edit_log_off != 0);

    ::unlink(tmp);
}

// ============================================================================
// TEST 2 — edit_log_offset is stable across save/reload
// ============================================================================
TEST_CASE(rollback_edit_log_offset_stable_across_save_reload) {
    LqtModel m = build_test_model();
    m.edit_codebook(0, 0, 11.0f);
    m.edit_codebook(0, 2, 22.0f);

    char tmp1[] = "/tmp/lqt_rollback_XXXXXX";
    int fd1 = mkstemp(tmp1);
    if (fd1 >= 0) ::close(fd1);
    m.save(tmp1);

    // Read tmp1's edit_log_offset.
    auto read_edit_log_offset = [](const std::string& path) -> uint64_t {
        std::ifstream in(path, std::ios::binary);
        in.seekg(0, std::ios::end);
        const size_t sz = static_cast<size_t>(in.tellg());
        in.seekg(0, std::ios::beg);
        std::vector<uint8_t> b(sz);
        in.read(reinterpret_cast<char*>(b.data()), static_cast<std::streamsize>(sz));
        in.close();
        LqtModel parsed = LqtModel::parse(b.data(), b.size());
        const uint64_t foff = parsed.header().footer_offset;
        uint64_t v = 0;
        for (int i = 0; i < 8; ++i) {
            v |= static_cast<uint64_t>(b[foff + 8 + i]) << (8 * i);
        }
        return v;
    };

    const uint64_t off1 = read_edit_log_offset(tmp1);

    // Round-trip: load, then save again to a fresh path.
    LqtModel m2 = LqtModel::load(tmp1);
    char tmp2[] = "/tmp/lqt_rollback_XXXXXX";
    int fd2 = mkstemp(tmp2);
    if (fd2 >= 0) ::close(fd2);
    m2.save(tmp2);
    const uint64_t off2 = read_edit_log_offset(tmp2);

    CHECK_EQ(off1, off2);

    ::unlink(tmp1);
    ::unlink(tmp2);
}

// ============================================================================
// TEST 3 — EditLog::truncate works correctly on in-memory log
// ============================================================================
TEST_CASE(rollback_edit_log_truncate_in_memory) {
    EditLog log;
    const char p0[] = "alpha";
    const char p1[] = "beta";
    const char p2[] = "gamma";
    EditLogEntry e0 = make_entry(MutationType::CodebookEdit, "t0", p0, sizeof(p0) - 1, 0, 100);
    EditLogEntry e1 = make_entry(MutationType::DeltaUpdate,  "t1", p1, sizeof(p1) - 1, e0.data_hash, 200);
    EditLogEntry e2 = make_entry(MutationType::ModuleSwap,   "t2", p2, sizeof(p2) - 1, e1.data_hash, 300);
    log.append(e0);
    log.append(e1);
    log.append(e2);
    CHECK_EQ(log.size(), static_cast<size_t>(3));

    // Truncate 1 entry off the tail.
    log.truncate(1);
    CHECK_EQ(log.size(), static_cast<size_t>(2));
    CHECK_EQ(log.at(0).target, std::string("t0"));
    CHECK_EQ(log.at(1).target, std::string("t1"));
    // The remaining prefix must still verify.
    CHECK(log.verify_chain());

    // Truncate the remaining two.
    log.truncate(2);
    CHECK_EQ(log.size(), static_cast<size_t>(0));
    CHECK(log.verify_chain()); // empty log verifies trivially

    // out_of_range when truncating more than size.
    CHECK_THROWS_AS(log.truncate(1), std::out_of_range);
}

// ============================================================================
// TEST 4 — rollback(1) after a codebook edit restores the previous value
// ============================================================================
TEST_CASE(rollback_one_after_codebook_edit_restores_value) {
    LqtModel m = build_test_model();

    const std::vector<float> before = m.reconstruct("w0");
    CHECK_NEAR(before[2], 3.0f, 1e-6);

    // Mutate codebook entry 2 from 3.0 -> 99.0.
    m.edit_codebook(0, 2, 99.0f);
    const std::vector<float> mid = m.reconstruct("w0");
    CHECK_NEAR(mid[2], 99.0f, 1e-6);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));

    // Rollback the single edit -> codebook entry 2 must be 3.0 again.
    m.rollback(1);
    const std::vector<float> after = m.reconstruct("w0");
    CHECK_EQ(after.size(), static_cast<size_t>(4));
    CHECK_NEAR(after[0], 1.0f, 1e-6);
    CHECK_NEAR(after[1], 2.0f, 1e-6);
    CHECK_NEAR(after[2], 3.0f, 1e-6);
    CHECK_NEAR(after[3], 4.0f, 1e-6);
}

// ============================================================================
// TEST 5 — rollback(2) after two edits restores original state of both
// ============================================================================
TEST_CASE(rollback_two_after_two_edits_restores_both) {
    LqtModel m = build_test_model();

    // Two distinct edits.
    m.edit_codebook(0, 0, -10.0f);
    m.edit_codebook(0, 3, 77.0f);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(2));

    const std::vector<float> mid = m.reconstruct("w0");
    CHECK_NEAR(mid[0], -10.0f, 1e-6);
    CHECK_NEAR(mid[3],  77.0f, 1e-6);

    // Roll back BOTH mutations.
    m.rollback(2);

    const std::vector<float> after = m.reconstruct("w0");
    CHECK_EQ(after.size(), static_cast<size_t>(4));
    CHECK_NEAR(after[0], 1.0f, 1e-6);
    CHECK_NEAR(after[1], 2.0f, 1e-6);
    CHECK_NEAR(after[2], 3.0f, 1e-6);
    CHECK_NEAR(after[3], 4.0f, 1e-6);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(0));
}

// ============================================================================
// TEST 6 — rollback beyond stack depth throws ValidationError
// ============================================================================
TEST_CASE(rollback_beyond_depth_throws_validation_error) {
    LqtModel m = build_test_model();
    m.edit_codebook(0, 1, 8.0f);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(1));

    // Rolling back 2 when only 1 is undoable must throw ValidationError.
    CHECK_THROWS_AS(m.rollback(2), ValidationError);
}

// ============================================================================
// TEST 7 — undo_depth() tracks correctly
// ============================================================================
TEST_CASE(rollback_undo_depth_tracks_correctly) {
    LqtModel m = build_test_model();
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(0));

    m.edit_codebook(0, 0, 5.0f);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(1));

    m.edit_codebook(0, 1, 6.0f);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(2));

    m.edit_codebook(0, 2, 7.0f);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(3));

    m.rollback(1);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(2));

    m.rollback(2);
    CHECK_EQ(m.undo_depth(), static_cast<size_t>(0));
}

// ============================================================================
// TEST 8 — After rollback, edit_log().size() is reduced by n
// ============================================================================
TEST_CASE(rollback_reduces_edit_log_size_by_n) {
    LqtModel m = build_test_model();
    m.edit_codebook(0, 0, 1.1f);
    m.edit_codebook(0, 1, 2.2f);
    m.edit_codebook(0, 2, 3.3f);
    m.edit_codebook(0, 3, 4.4f);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(4));

    m.rollback(3);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));

    m.rollback(1);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(0));
}

// ============================================================================
// TEST 9 — After rollback and re-mutation, the chain is still valid
// ============================================================================
TEST_CASE(rollback_chain_remains_valid_after_remutation) {
    LqtModel m = build_test_model();
    m.edit_codebook(0, 0, 10.0f);
    m.edit_codebook(0, 1, 20.0f);
    CHECK(m.edit_log().verify_chain());

    // Roll back one mutation, then perform a fresh one. The remaining log
    // (one old + one new) must verify cleanly as a single chain.
    m.rollback(1);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(1));
    CHECK(m.edit_log().verify_chain());

    m.edit_codebook(0, 2, 30.0f);
    CHECK_EQ(m.edit_log().size(), static_cast<size_t>(2));
    CHECK(m.edit_log().verify_chain());

    // Sanity: roll back the new one, the original tail entry's chain stays sound.
    m.rollback(1);
    CHECK(m.edit_log().verify_chain());
}

// ============================================================================
// TEST 10 — rollback(0) is a no-op
// ============================================================================
TEST_CASE(rollback_zero_is_noop) {
    LqtModel m = build_test_model();
    m.edit_codebook(0, 0, 42.0f);
    m.edit_codebook(0, 3, 43.0f);

    const size_t depth_before = m.undo_depth();
    const size_t logsz_before = m.edit_log().size();
    const std::vector<float> w_before = m.reconstruct("w0");

    m.rollback(0); // must do nothing, must not throw.

    CHECK_EQ(m.undo_depth(),      depth_before);
    CHECK_EQ(m.edit_log().size(), logsz_before);
    CHECK(m.edit_log().verify_chain());

    const std::vector<float> w_after = m.reconstruct("w0");
    CHECK_EQ(w_after.size(), w_before.size());
    for (size_t i = 0; i < w_after.size(); ++i) {
        CHECK_NEAR(w_after[i], w_before[i], 1e-6);
    }
}

// ============================================================================
// MAIN
// ============================================================================
int main() { return lqttest::run_all(); }
