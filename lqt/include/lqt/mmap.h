// include/lqt/mmap.h — POSIX memory-mapped file wrapper for the LQT library.
//
// Council module: A8 (Concurrency + Memory-Mapping Layer).
// Canon: lqt.md §5.1 "Memory-Mapped Operation".
//
// MemoryMappedFile wraps POSIX mmap/munmap in a RAII type.  It supports:
//   - Read-only mapping  (open_read)
//   - Read-write mapping (open_readwrite)
//   - File creation + mapping at a given size (create)
// On failure the constructors / factories throw lqt::LqtError with the
// OS error text from strerror(errno).
//
// DESIGN DECISION (error type):
//   We throw lqt::LqtError (the base exception) rather than a more specific
//   subtype for OS-level mmap failures because these are system resource
//   errors, not format/integrity/access-control errors.  The error message
//   includes the path and strerror(errno) text for diagnosability.
#pragma once

#include <cstddef>
#include <cstdint>
#include <string>

namespace lqt {

// RAII POSIX memory-mapped file.
// Non-copyable; movable.
class MemoryMappedFile {
public:
    // Default-constructed object is closed (is_open() == false).
    MemoryMappedFile() noexcept;

    // Move construction / assignment.
    MemoryMappedFile(MemoryMappedFile&& other) noexcept;
    MemoryMappedFile& operator=(MemoryMappedFile&& other) noexcept;

    // No copying — the OS mapping is a unique resource.
    MemoryMappedFile(const MemoryMappedFile&) = delete;
    MemoryMappedFile& operator=(const MemoryMappedFile&) = delete;

    // Destructor: munmap + close.
    ~MemoryMappedFile();

    // -----------------------------------------------------------------------
    // Factories
    // -----------------------------------------------------------------------

    // Open an existing file read-only and map it with PROT_READ / MAP_SHARED.
    // Throws lqt::LqtError on failure.
    static MemoryMappedFile open_read(const std::string& path);

    // Open an existing file read-write and map it with
    // PROT_READ|PROT_WRITE / MAP_SHARED.
    // Throws lqt::LqtError on failure.
    static MemoryMappedFile open_readwrite(const std::string& path);

    // Create (or truncate) a file at `path` to exactly `size` bytes via
    // ftruncate, then map it read-write.  Intended for writers creating new
    // LQT files.  Throws lqt::LqtError on failure.
    static MemoryMappedFile create(const std::string& path, std::size_t size);

    // -----------------------------------------------------------------------
    // Accessors
    // -----------------------------------------------------------------------

    // Pointer to the first byte of the mapping (nullptr if closed).
    const uint8_t* data()         const noexcept { return static_cast<const uint8_t*>(addr_); }

    // Mutable pointer — only valid for rw mappings (returns nullptr for ro).
    uint8_t*       mutable_data()       noexcept {
        return writable_ ? static_cast<uint8_t*>(addr_) : nullptr;
    }

    // Number of bytes in the mapping.
    std::size_t    size()         const noexcept { return size_; }

    // True if a mapping is currently open.
    bool           is_open()      const noexcept { return addr_ != nullptr; }

    // -----------------------------------------------------------------------
    // Operations
    // -----------------------------------------------------------------------

    // msync(MS_SYNC) — flush dirty pages to the underlying file.
    // No-op if the mapping is not open or not writable.
    // Throws lqt::LqtError if msync fails.
    void flush();

    // Alias for flush() — both names are common in the ecosystem.
    void sync() { flush(); }

    // Close the mapping (munmap + close fd).  Safe to call on an already-
    // closed object.  After close(), is_open() == false.
    void close() noexcept;

private:
    // Private constructor used by the factory methods.
    MemoryMappedFile(void* addr, std::size_t size, int fd, bool writable) noexcept;

    void*       addr_{nullptr};
    std::size_t size_{0};
    int         fd_{-1};
    bool        writable_{false};
};

} // namespace lqt
