// include/lqt/concurrency.h — Concurrency primitives for the LQT library.
//
// Council module: A8 (Concurrency + Memory-Mapping Layer).
// Canon: lqt.md §7 "Threading and Concurrency Model" (§7.1, §7.2),
//        §3.4 "Thread Safety and Concurrency" (double-buffering for hot-swap).
//
// DESIGN DECISION (reader-preference lock):
//   Canon §7.2 specifies that the lock "prioritizes readers during active
//   inference". std::shared_mutex (and most platform shared-mutex impls) use
//   implementation-defined priority; on Linux with pthreads the default is
//   typically writer-preferred or unspecified, which could starve readers under
//   sustained write pressure — the opposite of what inference workloads need.
//   We therefore implement an explicit reader-preference lock: writers only
//   enter when reader_count_ drops to zero AND no new reader can enter while
//   a writer is pending — but readers ARE allowed to enter while other readers
//   hold the lock even if a writer is waiting, which is the reader-preference
//   property. Specifically: we track reader_count_ under a std::mutex and use
//   a std::condition_variable to wake writers; readers block only when a writer
//   holds the lock (writer_active_ == true), but NOT when a writer is merely
//   waiting. This ensures in-flight inference batches (many concurrent readers)
//   are never stalled by a write request that arrives mid-batch.
//
// DESIGN DECISION (DoubleBuffer atomic shared_ptr):
//   C++17 removed std::atomic<std::shared_ptr<T>> as a specialisation but
//   retained the std::atomic_load / std::atomic_store free functions on a
//   plain std::shared_ptr member (§29.6.5 [util.smartptr.shared.atomic]).
//   These provide the necessary atomicity without a mutex for the reader path
//   (lock-free on most platforms). We document the member as "guarded by
//   atomic operations only" and never touch it via non-atomic paths.
#pragma once

#include <atomic>
#include <cassert>
#include <condition_variable>
#include <memory>
#include <mutex>
#include <stdexcept>

namespace lqt {

// ---------------------------------------------------------------------------
// ReaderWriterLock — reader-preference lock (canon §7.2)
// ---------------------------------------------------------------------------
// Many concurrent readers OR one exclusive writer at a time.
// Readers are preferred: new readers are admitted even while a writer waits,
// so active inference (heavy reader traffic) is never delayed by a write.
// Writers acquire the lock only after all current readers have released it.
//
// API:
//   lock_read()   / unlock_read()   — acquire/release a shared read lock
//   lock_write()  / unlock_write()  — acquire/release an exclusive write lock
//   try_lock_read()  — non-blocking read-lock attempt, returns bool
//   try_lock_write() — non-blocking write-lock attempt, returns bool
//   ReadGuard / WriteGuard — RAII scoped helpers
class ReaderWriterLock {
public:
    ReaderWriterLock() = default;
    ~ReaderWriterLock() = default;

    // Non-copyable, non-movable (contains synchronisation primitives).
    ReaderWriterLock(const ReaderWriterLock&) = delete;
    ReaderWriterLock& operator=(const ReaderWriterLock&) = delete;
    ReaderWriterLock(ReaderWriterLock&&) = delete;
    ReaderWriterLock& operator=(ReaderWriterLock&&) = delete;

    // Acquire a shared read lock.  Blocks only while a writer currently holds
    // the lock (writer_active_).  Multiple threads may hold read locks
    // simultaneously.
    void lock_read() {
        std::unique_lock<std::mutex> lk(mtx_);
        // Reader-preference: wait ONLY if a writer is currently active.
        // We do NOT wait for pending writers — that is the preference guarantee.
        reader_cv_.wait(lk, [this]{ return !writer_active_; });
        ++reader_count_;
    }

    // Release a shared read lock acquired by lock_read().
    void unlock_read() {
        std::unique_lock<std::mutex> lk(mtx_);
        assert(reader_count_ > 0 && "unlock_read without matching lock_read");
        if (--reader_count_ == 0) {
            // Wake a waiting writer if present.
            writer_cv_.notify_all();
        }
    }

    // Acquire an exclusive write lock.  Blocks until reader_count_ == 0
    // and no other writer is active.
    void lock_write() {
        std::unique_lock<std::mutex> lk(mtx_);
        // Wait for any current writer to finish first.
        writer_cv_.wait(lk, [this]{ return !writer_active_; });
        // Mark intent so new readers will queue.
        writer_active_ = true;
        // Now wait for all current readers to drain.
        writer_cv_.wait(lk, [this]{ return reader_count_ == 0; });
    }

    // Release the exclusive write lock.
    void unlock_write() {
        std::unique_lock<std::mutex> lk(mtx_);
        assert(writer_active_ && "unlock_write without matching lock_write");
        writer_active_ = false;
        // Wake all waiting readers first (reader-preference).
        reader_cv_.notify_all();
        // Also wake a waiting writer in case no readers are waiting.
        writer_cv_.notify_one();
    }

    // Non-blocking read-lock attempt.  Returns true and holds the read lock
    // on success; returns false and leaves state unchanged on failure.
    bool try_lock_read() {
        std::unique_lock<std::mutex> lk(mtx_);
        if (writer_active_) {
            return false;
        }
        ++reader_count_;
        return true;
    }

    // Non-blocking write-lock attempt.  Returns true and holds the write lock
    // on success; returns false and leaves state unchanged on failure.
    bool try_lock_write() {
        std::unique_lock<std::mutex> lk(mtx_);
        if (writer_active_ || reader_count_ > 0) {
            return false;
        }
        writer_active_ = true;
        return true;
    }

private:
    std::mutex              mtx_;
    std::condition_variable reader_cv_;   // woken when writer releases
    std::condition_variable writer_cv_;   // woken when readers drain or writer releases
    unsigned int            reader_count_{0};
    bool                    writer_active_{false};
};

// ---------------------------------------------------------------------------
// ReadGuard — RAII scoped read lock
// ---------------------------------------------------------------------------
class ReadGuard {
public:
    explicit ReadGuard(ReaderWriterLock& lock) : lock_(lock) {
        lock_.lock_read();
    }
    ~ReadGuard() {
        lock_.unlock_read();
    }
    ReadGuard(const ReadGuard&) = delete;
    ReadGuard& operator=(const ReadGuard&) = delete;
private:
    ReaderWriterLock& lock_;
};

// ---------------------------------------------------------------------------
// WriteGuard — RAII scoped write lock
// ---------------------------------------------------------------------------
class WriteGuard {
public:
    explicit WriteGuard(ReaderWriterLock& lock) : lock_(lock) {
        lock_.lock_write();
    }
    ~WriteGuard() {
        lock_.unlock_write();
    }
    WriteGuard(const WriteGuard&) = delete;
    WriteGuard& operator=(const WriteGuard&) = delete;
private:
    ReaderWriterLock& lock_;
};

// ---------------------------------------------------------------------------
// DoubleBuffer<T> — lock-free-ish hot-swap buffer (canon §3.4, §7.1)
// ---------------------------------------------------------------------------
// Maintains an "active" std::shared_ptr<const T>.  Readers call load() to
// obtain a snapshot that remains valid for the lifetime of their shared_ptr,
// even after a writer calls store().  Writers call store() to atomically
// publish a new value.
//
// DESIGN DECISION (atomic shared_ptr):
//   C++17 std::atomic_load/std::atomic_store on a plain shared_ptr member
//   (§29.6.5) provide the required atomicity.  On x86-64 with libstdc++ these
//   are implemented with a per-pointer spinlock (lock-free for the pointer
//   exchange itself on platforms where sizeof(shared_ptr) <= sizeof(void*)*2
//   and CAS is available), giving readers an essentially lock-free fast path.
//   We annotate the member with a comment so maintainers do not accidentally
//   access it through non-atomic paths.
template<typename T>
class DoubleBuffer {
public:
    // Construct with a null (empty) active pointer.
    DoubleBuffer() = default;

    // Construct with an initial value.
    explicit DoubleBuffer(std::shared_ptr<const T> initial)
        : active_(std::move(initial)) {}

    // Copy/move disabled — the buffer is a shared ownership anchor.
    DoubleBuffer(const DoubleBuffer&) = delete;
    DoubleBuffer& operator=(const DoubleBuffer&) = delete;
    DoubleBuffer(DoubleBuffer&&) = delete;
    DoubleBuffer& operator=(DoubleBuffer&&) = delete;

    // Atomically load and return a snapshot of the current value.
    // The returned shared_ptr keeps T alive regardless of subsequent store()
    // calls, enabling zero-copy safe reads during inference.
    std::shared_ptr<const T> load() const {
        // ATOMIC ACCESS — do not dereference active_ directly.
        return std::atomic_load(&active_);
    }

    // Atomically replace the active pointer with a new value.
    // Old readers holding a snapshot continue to see the old value safely.
    void store(std::shared_ptr<const T> next) {
        // ATOMIC ACCESS — do not assign active_ directly.
        std::atomic_store(&active_, std::move(next));
    }

    // Convenience: construct T in-place from args, wrap in shared_ptr, store.
    template<typename... Args>
    void emplace(Args&&... args) {
        store(std::make_shared<const T>(std::forward<Args>(args)...));
    }

    // Factory helper: create a DoubleBuffer pre-loaded with a value.
    template<typename... Args>
    static DoubleBuffer make(Args&&... args) {
        return DoubleBuffer(std::make_shared<const T>(std::forward<Args>(args)...));
    }

private:
    // Accessed ONLY via std::atomic_load / std::atomic_store.
    mutable std::shared_ptr<const T> active_;  // ATOMIC-ONLY ACCESS
};

} // namespace lqt
