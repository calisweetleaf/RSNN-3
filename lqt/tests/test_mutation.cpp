// tests/test_mutation.cpp — A7 mutation safety layer tests.
//
// Council module: A7 (mutation safety layer).
// Tests: edit-log append + serialize/parse round-trip; verify_chain() true
// for intact log and FALSE after flipping one entry's target; validator
// accepts a valid edit, rejects NaN/inf and over-bound values, rejects a
// Protected tensor when !authorized, rejects dimension mismatch, detects a
// cycle in a module graph; transaction commits a 3-op batch on success;
// transaction rolls back fully when the validator rejects.
#include "test_framework.h"

#include <cmath>
#include <cstring>
#include <limits>
#include <map>
#include <string>
#include <vector>

#include "lqt/edit_log.h"
#include "lqt/mutation.h"
#include "lqt/transaction.h"
#include "lqt/endian.h"

// ============================================================================
// Helper: build a TensorDescriptor for tests
// ============================================================================
static lqt::TensorDescriptor make_desc(
    const std::string& name,
    std::vector<uint32_t> shape,
    bool protect = false)
{
    lqt::TensorDescriptor d;
    d.name  = name;
    d.shape = std::move(shape);
    d.dtype = lqt::DType::FP32;
    if (protect) {
        d.set_flag(lqt::TensorFlag::Protected, true);
    }
    return d;
}

// ============================================================================
// EDIT LOG TESTS
// ============================================================================

TEST_CASE(editlog_append_and_access) {
    lqt::EditLog log;
    CHECK_EQ(log.size(), static_cast<size_t>(0));

    auto e0 = lqt::make_entry(lqt::MutationType::CodebookEdit, "layer0",
                               nullptr, 0, 0, 1000);
    auto e1 = lqt::make_entry(lqt::MutationType::DeltaUpdate, "layer1",
                               nullptr, 0, e0.data_hash, 2000);

    log.append(e0);
    log.append(e1);

    CHECK_EQ(log.size(), static_cast<size_t>(2));
    CHECK_EQ(log.at(0).target, std::string("layer0"));
    CHECK_EQ(log.at(1).target, std::string("layer1"));
    CHECK_EQ(log.at(0).type, lqt::MutationType::CodebookEdit);
    CHECK_EQ(log.at(1).type, lqt::MutationType::DeltaUpdate);
}

TEST_CASE(editlog_serialize_parse_roundtrip) {
    // Build a log with three entries carrying a real payload.
    const char payload0[] = "hello";
    const char payload1[] = "world_update";
    const char payload2[] = "swap_me";

    lqt::EditLog log;
    auto e0 = lqt::make_entry(lqt::MutationType::CodebookEdit,   "attn.q",
                               payload0, sizeof(payload0) - 1, 0);
    auto e1 = lqt::make_entry(lqt::MutationType::DeltaUpdate,    "attn.k",
                               payload1, sizeof(payload1) - 1, e0.data_hash);
    auto e2 = lqt::make_entry(lqt::MutationType::ModuleSwap,     "attn.v",
                               payload2, sizeof(payload2) - 1, e1.data_hash);
    log.append(e0);
    log.append(e1);
    log.append(e2);

    // Serialize.
    lqt::ByteWriter w;
    log.serialize(w);

    // Parse.
    lqt::ByteReader r(w.bytes());
    lqt::EditLog log2 = lqt::EditLog::parse(r);

    CHECK_EQ(log2.size(), static_cast<size_t>(3));
    CHECK_EQ(log2.at(0).target,     std::string("attn.q"));
    CHECK_EQ(log2.at(1).target,     std::string("attn.k"));
    CHECK_EQ(log2.at(2).target,     std::string("attn.v"));
    CHECK_EQ(log2.at(0).timestamp_ns, log.at(0).timestamp_ns);
    CHECK_EQ(log2.at(1).timestamp_ns, log.at(1).timestamp_ns);
    CHECK_EQ(log2.at(2).timestamp_ns, log.at(2).timestamp_ns);
    CHECK_EQ(log2.at(0).data_hash,  log.at(0).data_hash);
    CHECK_EQ(log2.at(1).data_hash,  log.at(1).data_hash);
    CHECK_EQ(log2.at(2).data_hash,  log.at(2).data_hash);
    CHECK_EQ(log2.at(0).signature.size(), log.at(0).signature.size());
}

TEST_CASE(editlog_verify_chain_intact) {
    lqt::EditLog log;
    const char p0[] = "payload_zero";
    const char p1[] = "payload_one";
    const char p2[] = "payload_two";

    auto e0 = lqt::make_entry(lqt::MutationType::CodebookEdit, "mod_a",
                               p0, sizeof(p0) - 1, 0, 10000);
    auto e1 = lqt::make_entry(lqt::MutationType::DeltaUpdate,  "mod_b",
                               p1, sizeof(p1) - 1, e0.data_hash, 20000);
    auto e2 = lqt::make_entry(lqt::MutationType::SparseMaskUpdate, "mod_c",
                               p2, sizeof(p2) - 1, e1.data_hash, 30000);
    log.append(e0);
    log.append(e1);
    log.append(e2);

    CHECK(log.verify_chain());
}

TEST_CASE(editlog_verify_chain_detects_tamper) {
    lqt::EditLog log;
    const char p0[] = "data_a";
    const char p1[] = "data_b";
    const char p2[] = "data_c";

    auto e0 = lqt::make_entry(lqt::MutationType::CodebookEdit, "mod_x",
                               p0, sizeof(p0) - 1, 0, 100);
    auto e1 = lqt::make_entry(lqt::MutationType::DeltaUpdate,  "mod_y",
                               p1, sizeof(p1) - 1, e0.data_hash, 200);
    auto e2 = lqt::make_entry(lqt::MutationType::ModuleSwap,   "mod_z",
                               p2, sizeof(p2) - 1, e1.data_hash, 300);
    log.append(e0);
    log.append(e1);
    log.append(e2);

    // Verify intact first.
    CHECK(log.verify_chain());

    // Serialize, parse, flip the target of entry[1], re-verify -> must fail.
    lqt::ByteWriter w;
    log.serialize(w);
    lqt::ByteReader r(w.bytes());
    lqt::EditLog log2 = lqt::EditLog::parse(r);

    // Mutate entry 1's target (direct access via mutable parse result).
    // We must reconstruct since at() returns const ref.
    // Re-parse into a mutable vector by serializing entries individually.
    // Simplest: re-append with tampered target.
    lqt::EditLog log3;
    log3.append(log2.at(0));  // entry 0 untouched
    {
        lqt::EditLogEntry tampered = log2.at(1);
        tampered.target = "TAMPERED_TARGET";
        log3.append(tampered);  // entry 1 tampered
    }
    log3.append(log2.at(2));  // entry 2 untouched

    CHECK(!log3.verify_chain());
}

// ============================================================================
// MUTATION VALIDATOR TESTS
// ============================================================================

TEST_CASE(validator_accepts_valid_edit) {
    lqt::MutationValidator v(-100.0f, 100.0f);
    auto desc = make_desc("w", {4, 4});

    // (1) Same element count reshape: [4,4] -> [2,8].
    auto r1 = v.check_dimensions(desc, {2, 8});
    CHECK(r1.ok);

    // (2) Values within bounds.
    float vals[] = {0.0f, 1.5f, -99.9f, 99.9f};
    auto r2 = v.check_value_bounds(vals, 4);
    CHECK(r2.ok);

    // (3) Topology: simple DAG with no cycle.
    std::map<std::string, std::vector<std::string>> graph = {
        {"a", {"b", "c"}},
        {"b", {"d"}},
        {"c", {"d"}},
        {"d", {}}
    };
    auto r3 = v.check_topology("a", graph);
    CHECK(r3.ok);

    // (4) Access: non-protected tensor, any auth.
    auto r4 = v.check_access(desc, false);
    CHECK(r4.ok);
}

TEST_CASE(validator_rejects_nan) {
    lqt::MutationValidator v;
    float vals[] = {1.0f, std::numeric_limits<float>::quiet_NaN(), 2.0f};
    auto r = v.check_value_bounds(vals, 3);
    CHECK(!r.ok);
    CHECK_MSG(r.reason.find("non-finite") != std::string::npos, "reason should say non-finite");
}

TEST_CASE(validator_rejects_inf) {
    lqt::MutationValidator v;
    float vals[] = {0.5f, std::numeric_limits<float>::infinity()};
    auto r = v.check_value_bounds(vals, 2);
    CHECK(!r.ok);
}

TEST_CASE(validator_rejects_over_bound) {
    lqt::MutationValidator v(-10.0f, 10.0f);
    float vals[] = {5.0f, 10.001f};
    auto r = v.check_value_bounds(vals, 2);
    CHECK(!r.ok);
    CHECK_MSG(r.reason.find("outside bounds") != std::string::npos,
              "reason should mention outside bounds");
}

TEST_CASE(validator_rejects_under_bound) {
    lqt::MutationValidator v(-10.0f, 10.0f);
    float vals[] = {-10.001f, 0.0f};
    auto r = v.check_value_bounds(vals, 2);
    CHECK(!r.ok);
}

TEST_CASE(validator_rejects_protected_tensor_no_auth) {
    lqt::MutationValidator v;
    auto desc = make_desc("attn.core", {8, 8}, /*protect=*/true);
    auto r = v.check_access(desc, /*authorized=*/false);
    CHECK(!r.ok);
    CHECK_MSG(r.reason.find("Protected") != std::string::npos,
              "reason should mention Protected");
}

TEST_CASE(validator_allows_protected_tensor_with_auth) {
    lqt::MutationValidator v;
    auto desc = make_desc("attn.core", {8, 8}, /*protect=*/true);
    auto r = v.check_access(desc, /*authorized=*/true);
    CHECK(r.ok);
}

TEST_CASE(validator_rejects_dimension_mismatch) {
    lqt::MutationValidator v;
    auto desc = make_desc("w", {4, 4}); // 16 elements
    // proposed shape has 15 elements -- mismatch.
    auto r = v.check_dimensions(desc, {3, 5});
    CHECK(!r.ok);
    CHECK_MSG(r.reason.find("mismatch") != std::string::npos,
              "reason should mention mismatch");
}

TEST_CASE(validator_detects_cycle_in_module_graph) {
    lqt::MutationValidator v;
    // a -> b -> c -> a   (cycle)
    std::map<std::string, std::vector<std::string>> graph = {
        {"a", {"b"}},
        {"b", {"c"}},
        {"c", {"a"}}
    };
    auto r = v.check_topology("a", graph);
    CHECK(!r.ok);
    CHECK_MSG(r.reason.find("cycle") != std::string::npos,
              "reason should mention cycle");
}

TEST_CASE(validator_rejects_missing_target_in_graph) {
    lqt::MutationValidator v;
    std::map<std::string, std::vector<std::string>> graph = {
        {"a", {"b"}},
        {"b", {}}
    };
    auto r = v.check_topology("z", graph); // "z" not in graph
    CHECK(!r.ok);
}

TEST_CASE(validator_rejects_unresolved_edge) {
    lqt::MutationValidator v;
    // "a" depends on "missing" which is not a key in the graph.
    std::map<std::string, std::vector<std::string>> graph = {
        {"a", {"missing"}}
    };
    auto r = v.check_topology("a", graph);
    CHECK(!r.ok);
}

// ============================================================================
// TRANSACTION TESTS
// ============================================================================

// Simple state for transaction tests.
struct CounterState {
    int value = 0;
    std::string label;
    int extra = 0;
};

TEST_CASE(transaction_commits_three_op_batch) {
    CounterState state;
    state.value = 0;
    state.label = "initial";

    lqt::Transaction<CounterState> txn(state);
    txn.stage([](CounterState& s){ s.value += 10; });
    txn.stage([](CounterState& s){ s.value += 5;  });
    txn.stage([](CounterState& s){ s.label = "committed"; });

    bool ok = txn.commit([](const CounterState& s) -> lqt::ValidationResult {
        if (s.value == 15 && s.label == "committed") {
            return lqt::ValidationResult::pass();
        }
        return lqt::ValidationResult::fail("unexpected state");
    });

    CHECK(ok);
    CHECK_EQ(state.value, 15);
    CHECK_EQ(state.label, std::string("committed"));
}

TEST_CASE(transaction_rollback_on_validation_failure) {
    CounterState state;
    state.value = 42;
    state.label = "original";
    state.extra = 7;

    lqt::Transaction<CounterState> txn(state);
    txn.stage([](CounterState& s){ s.value  = 999; });
    txn.stage([](CounterState& s){ s.label  = "changed"; });
    txn.stage([](CounterState& s){ s.extra  = -1;  });

    bool ok = txn.commit([](const CounterState&) -> lqt::ValidationResult {
        return lqt::ValidationResult::fail("rejected by validator");
    });

    CHECK(!ok);
    // Original state must be byte-identical.
    CHECK_EQ(state.value,  42);
    CHECK_EQ(state.label,  std::string("original"));
    CHECK_EQ(state.extra,  7);
}

TEST_CASE(transaction_rollback_on_op_exception) {
    CounterState state;
    state.value = 10;
    state.label = "safe";

    lqt::Transaction<CounterState> txn(state);
    txn.stage([](CounterState& s){ s.value = 100; });
    txn.stage([](CounterState&) -> void {
        throw std::runtime_error("simulated op failure");
    });
    txn.stage([](CounterState& s){ s.label = "broken"; });

    bool ok = txn.commit([](const CounterState&) -> lqt::ValidationResult {
        return lqt::ValidationResult::pass();
    });

    CHECK(!ok);
    CHECK_EQ(state.value, 10);
    CHECK_EQ(state.label, std::string("safe"));
}

TEST_CASE(transaction_abort_prevents_commit) {
    CounterState state;
    state.value = 5;

    lqt::Transaction<CounterState> txn(state);
    txn.stage([](CounterState& s){ s.value = 999; });
    txn.abort();

    bool ok = txn.commit([](const CounterState&) -> lqt::ValidationResult {
        return lqt::ValidationResult::pass();
    });

    CHECK(!ok);
    CHECK_EQ(state.value, 5);
}

TEST_CASE(transaction_stage_after_abort_is_noop) {
    CounterState state;
    state.value = 3;

    lqt::Transaction<CounterState> txn(state);
    txn.abort();
    txn.stage([](CounterState& s){ s.value = 100; }); // should be ignored
    CHECK_EQ(txn.staged_count(), static_cast<size_t>(0));

    bool ok = txn.commit([](const CounterState&) -> lqt::ValidationResult {
        return lqt::ValidationResult::pass();
    });
    CHECK(!ok);
    CHECK_EQ(state.value, 3);
}

// ============================================================================
// MAIN
// ============================================================================

int main() {
    return lqttest::run_all();
}
