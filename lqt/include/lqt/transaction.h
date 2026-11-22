// lqt/transaction.h — Atomic, all-or-nothing mutation transaction with rollback.
//
// Council module: A7 (mutation safety layer).
// Canon: lqt.md §5.6 (Transaction System).
//
// DESIGN DECISION (sandboxed trial, canon §5.6):
//   commit() copies the target State, applies all staged operations to the
//   copy, then runs the caller's validator on the copy.  On success the
//   copy is move-assigned back into the real target (atomic from the caller's
//   perspective).  On any failure — either validate(copy) returning {ok:false}
//   or any exception thrown from an op or the validator — the copy is
//   discarded and the real target is left byte-identical to its pre-commit
//   state.  This requires State to be CopyConstructible and MoveAssignable.
//
//   Rationale: a copy-based sandbox is simple, provably correct, and avoids
//   the complexity of per-operation undo hooks.  The cost is one full State
//   copy per commit, which is acceptable given the rarity of transactions
//   relative to read operations.
//
// Usage:
//   Transaction<MyState> txn(state);
//   txn.stage([](MyState& s){ s.x = 42; });
//   txn.stage([](MyState& s){ s.y = 99; });
//   bool ok = txn.commit([](const MyState& s){
//       return s.x < s.y ? ValidationResult::pass() : ValidationResult::fail("...");
//   });
//   // If ok == false, state is unchanged.
#pragma once

#include <exception>
#include <functional>
#include <utility>
#include <vector>

#include "lqt/mutation.h"  // ValidationResult

namespace lqt {

// ---------------------------------------------------------------------------
// Transaction<State> — header-only template
// ---------------------------------------------------------------------------
template <class State>
class Transaction {
public:
    // Construct a transaction over the given target state.  The target must
    // outlive the Transaction object.
    explicit Transaction(State& target)
        : target_(target), aborted_(false) {}

    // Stage an operation.  The operation is stored for later execution
    // against a sandbox copy; the real target is NOT touched until commit().
    // Calling stage() on an aborted transaction is a no-op.
    void stage(std::function<void(State&)> op) {
        if (!aborted_) {
            ops_.push_back(std::move(op));
        }
    }

    // Attempt to commit all staged operations atomically.
    //
    // Process:
    //   1. Copy target_ into a sandbox.
    //   2. Apply every staged op to the sandbox in order.
    //   3. Call validate(sandbox).
    //   4a. If validate.ok and no exception: move-assign sandbox -> target_.
    //       Clear the staged ops and return true.
    //   4b. Otherwise: discard sandbox, leave target_ untouched, return false.
    //
    // Returns false (and leaves target_ unchanged) if:
    //   - validate returns a ValidationResult with ok == false.
    //   - Any staged op throws an exception.
    //   - validate itself throws an exception.
    //   - abort() was previously called.
    bool commit(std::function<ValidationResult(const State&)> validate) {
        if (aborted_) return false;

        try {
            State sandbox(target_);            // CopyConstructible required
            for (auto& op : ops_) {
                op(sandbox);                   // apply ops to sandbox
            }
            ValidationResult result = validate(sandbox);
            if (!result.ok) {
                return false;                  // sandbox discarded automatically
            }
            target_ = std::move(sandbox);      // MoveAssignable required
            ops_.clear();
            return true;
        } catch (...) {
            // Any exception: target_ is untouched (sandbox was a local copy).
            return false;
        }
    }

    // Abort the transaction: discard all staged ops and mark this transaction
    // as permanently aborted.  Subsequent stage() and commit() calls are no-ops.
    void abort() {
        ops_.clear();
        aborted_ = true;
    }

    // Number of staged (uncommitted) operations.
    size_t staged_count() const noexcept { return ops_.size(); }

    // True if abort() has been called.
    bool is_aborted() const noexcept { return aborted_; }

private:
    State&                                   target_;
    std::vector<std::function<void(State&)>> ops_;
    bool                                     aborted_;
};

} // namespace lqt
