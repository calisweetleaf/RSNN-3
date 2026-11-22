// tests/test_concurrency.cpp — Concurrency + mmap stress tests.
//
// Council module: A8 (Concurrency + Memory-Mapping Layer).
// Canon: lqt.md §7 (ReaderWriterLock, DoubleBuffer), §5.1 (MemoryMappedFile).
//
// Test plan:
//   1. rwlock_basic         — single-threaded read/write lock/unlock sanity
//   2. rwlock_try           — try_lock_read / try_lock_write contention check
//   3. rwlock_stress        — 8 threads × 1000 ops; invariant a == b*2 never torn
//   4. double_buffer_basic  — load/store single-threaded
//   5. double_buffer_stress — concurrent readers + writer; snapshots consistent
//   6. mmap_create_write_read — create file, write pattern, re-open, verify
//   7. mmap_nonexistent     — open_read on missing path throws LqtError

#include "lqt/concurrency.h"
#include "lqt/error.h"
#include "lqt/mmap.h"
#include "test_framework.h"

#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>  // getpid
#include <vector>

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

static std::string tmp_path(const char* tag) {
    // Produce a unique path in /tmp for each test run + tag.
    return std::string("/tmp/lqt_test_") + tag +
           "_" + std::to_string(static_cast<unsigned>(::getpid()));
}

// ---------------------------------------------------------------------------
// ReaderWriterLock tests
// ---------------------------------------------------------------------------

TEST_CASE(rwlock_basic) {
    lqt::ReaderWriterLock rwl;

    // Multiple readers can nest without deadlock.
    rwl.lock_read();
    rwl.lock_read();
    rwl.unlock_read();
    rwl.unlock_read();

    // Write lock round-trip.
    rwl.lock_write();
    rwl.unlock_write();

    // After releasing write lock, readers should acquire.
    rwl.lock_read();
    rwl.unlock_read();
}

TEST_CASE(rwlock_try) {
    lqt::ReaderWriterLock rwl;

    // try_lock_read on free lock succeeds.
    CHECK(rwl.try_lock_read());

    // try_lock_write fails while a reader holds.
    CHECK(!rwl.try_lock_write());

    rwl.unlock_read();

    // try_lock_write on free lock succeeds.
    CHECK(rwl.try_lock_write());

    // try_lock_read fails while writer is active.
    CHECK(!rwl.try_lock_read());

    rwl.unlock_write();
}

TEST_CASE(rwlock_stress) {
    // Shared state: a pair (a, b) maintained with invariant a == b * 2.
    // Writer updates both atomically under WriteGuard.
    // Readers verify the invariant under ReadGuard.
    struct SharedState {
        long a{0};
        long b{0};
    };

    SharedState state;
    lqt::ReaderWriterLock rwl;

    constexpr int N_THREADS = 8;
    constexpr int M_OPS     = 1000;

    std::atomic<long>  total_ops{0};
    std::atomic<bool>  invariant_violated{false};

    // 2 writer threads, 6 reader threads.
    constexpr int N_WRITERS = 2;
    constexpr int N_READERS = N_THREADS - N_WRITERS;

    std::vector<std::thread> threads;
    threads.reserve(N_THREADS);

    // Writer threads: each does M_OPS write operations.
    for (int w = 0; w < N_WRITERS; ++w) {
        threads.emplace_back([&, w]() {
            for (int i = 0; i < M_OPS; ++i) {
                lqt::WriteGuard wg(rwl);
                long val = w * M_OPS + i + 1;
                state.b = val;
                state.a = val * 2;
                ++total_ops;
            }
        });
    }

    // Reader threads: each does M_OPS read operations.
    for (int r = 0; r < N_READERS; ++r) {
        threads.emplace_back([&]() {
            for (int i = 0; i < M_OPS; ++i) {
                lqt::ReadGuard rg(rwl);
                // The invariant must hold at any point inside a read lock.
                long a = state.a;
                long b = state.b;
                if (a != b * 2) {
                    invariant_violated.store(true, std::memory_order_relaxed);
                }
                ++total_ops;
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    CHECK_EQ(total_ops.load(), static_cast<long>(N_THREADS * M_OPS));
    CHECK(!invariant_violated.load());
}

// ---------------------------------------------------------------------------
// DoubleBuffer tests
// ---------------------------------------------------------------------------

TEST_CASE(double_buffer_basic) {
    lqt::DoubleBuffer<std::vector<int>> buf;

    // Initially null.
    CHECK(buf.load() == nullptr);

    // store and retrieve.
    buf.store(std::make_shared<const std::vector<int>>(
                  std::vector<int>{1, 2, 3}));
    auto snap = buf.load();
    CHECK(snap != nullptr);
    CHECK_EQ(snap->size(), std::size_t(3));
    CHECK_EQ((*snap)[0], 1);

    // emplace helper.
    buf.emplace(std::vector<int>{10, 20});
    auto snap2 = buf.load();
    CHECK_EQ(snap2->size(), std::size_t(2));
    CHECK_EQ((*snap2)[0], 10);

    // Old snapshot remains valid.
    CHECK_EQ((*snap)[0], 1);
}

TEST_CASE(double_buffer_stress) {
    // Writer stores vectors filled with a sentinel value (version number).
    // Concurrent readers verify every element in their snapshot equals the
    // sentinel for that snapshot's version.  No crash = correct atomics.

    constexpr int N_READERS     = 6;
    constexpr int WRITE_CYCLES  = 500;
    constexpr int READS_PER_THR = 2000;
    constexpr int VEC_SIZE      = 64;

    lqt::DoubleBuffer<std::vector<int>> buf;
    // Seed with version 0.
    buf.emplace(std::vector<int>(VEC_SIZE, 0));

    std::atomic<bool> writer_done{false};
    std::atomic<bool> consistency_error{false};

    // Writer thread.
    std::thread writer([&]() {
        for (int v = 1; v <= WRITE_CYCLES; ++v) {
            buf.store(std::make_shared<const std::vector<int>>(
                          std::vector<int>(VEC_SIZE, v)));
        }
        writer_done.store(true, std::memory_order_release);
    });

    // Reader threads.
    std::vector<std::thread> readers;
    readers.reserve(N_READERS);
    for (int r = 0; r < N_READERS; ++r) {
        readers.emplace_back([&]() {
            for (int i = 0; i < READS_PER_THR; ++i) {
                auto snap = buf.load();
                if (snap) {
                    // All elements must equal the first element (single sentinel).
                    int sentinel = (*snap)[0];
                    for (int j = 1; j < VEC_SIZE; ++j) {
                        if ((*snap)[j] != sentinel) {
                            consistency_error.store(true,
                                std::memory_order_relaxed);
                        }
                    }
                }
            }
        });
    }

    writer.join();
    for (auto& t : readers) t.join();

    CHECK(!consistency_error.load());

    // Final value must be the last written version.
    auto final_snap = buf.load();
    CHECK(final_snap != nullptr);
    CHECK_EQ((*final_snap)[0], WRITE_CYCLES);
}

// ---------------------------------------------------------------------------
// MemoryMappedFile tests
// ---------------------------------------------------------------------------

TEST_CASE(mmap_create_write_read) {
    const std::string path = tmp_path("rw");
    constexpr std::size_t SZ = 4096;

    // --- Create and write ---
    {
        lqt::MemoryMappedFile mmf = lqt::MemoryMappedFile::create(path, SZ);
        CHECK(mmf.is_open());
        CHECK_EQ(mmf.size(), SZ);
        CHECK(mmf.mutable_data() != nullptr);

        // Write a recognisable pattern: byte[i] = i & 0xFF, with a 4-byte
        // magic header 0xDEADBEEF.
        uint8_t* p = mmf.mutable_data();
        p[0] = 0xDE; p[1] = 0xAD; p[2] = 0xBE; p[3] = 0xEF;
        for (std::size_t i = 4; i < SZ; ++i) {
            p[i] = static_cast<uint8_t>(i & 0xFF);
        }
        mmf.sync();
    }  // destructor munmaps and closes

    // --- Re-open read-only and verify ---
    {
        lqt::MemoryMappedFile mmf = lqt::MemoryMappedFile::open_read(path);
        CHECK(mmf.is_open());
        CHECK_EQ(mmf.size(), SZ);
        // mutable_data() must return nullptr for ro mapping.
        CHECK(mmf.mutable_data() == nullptr);

        const uint8_t* p = mmf.data();
        CHECK_EQ(p[0], uint8_t(0xDE));
        CHECK_EQ(p[1], uint8_t(0xAD));
        CHECK_EQ(p[2], uint8_t(0xBE));
        CHECK_EQ(p[3], uint8_t(0xEF));
        bool pattern_ok = true;
        for (std::size_t i = 4; i < SZ; ++i) {
            if (p[i] != static_cast<uint8_t>(i & 0xFF)) {
                pattern_ok = false;
                break;
            }
        }
        CHECK(pattern_ok);
    }

    // Cleanup temp file.
    ::unlink(path.c_str());
}

TEST_CASE(mmap_nonexistent) {
    CHECK_THROWS_AS(
        lqt::MemoryMappedFile::open_read("/tmp/__lqt_does_not_exist_XYZ__"),
        lqt::LqtError
    );
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

int main() {
    return lqttest::run_all();
}
