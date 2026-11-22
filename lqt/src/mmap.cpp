// src/mmap.cpp — POSIX memory-mapped file implementation.
//
// Council module: A8 (Concurrency + Memory-Mapping Layer).
// Canon: lqt.md §5.1 "Memory-Mapped Operation".
//
// See include/lqt/mmap.h for API documentation.

#include "lqt/mmap.h"
#include "lqt/error.h"

#include <cerrno>
#include <cstring>     // strerror
#include <stdexcept>
#include <string>
#include <utility>     // std::swap

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

namespace lqt {

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

namespace {

// Build a human-readable LqtError message that includes the path and the OS
// error string.
[[noreturn]] void throw_os_error(const std::string& path, const char* action) {
    const int saved = errno;
    throw LqtError(std::string("MemoryMappedFile: ") + action +
                   " '" + path + "': " + strerror(saved));
}

// Stat the open fd to get file size.
std::size_t fd_size(int fd, const std::string& path) {
    struct stat st{};
    if (::fstat(fd, &st) != 0) {
        throw_os_error(path, "fstat");
    }
    return static_cast<std::size_t>(st.st_size);
}

} // anonymous namespace

// ---------------------------------------------------------------------------
// Constructors / destructor
// ---------------------------------------------------------------------------

MemoryMappedFile::MemoryMappedFile() noexcept = default;

MemoryMappedFile::MemoryMappedFile(void* addr, std::size_t size,
                                   int fd, bool writable) noexcept
    : addr_(addr), size_(size), fd_(fd), writable_(writable)
{}

MemoryMappedFile::MemoryMappedFile(MemoryMappedFile&& other) noexcept
    : addr_(other.addr_), size_(other.size_),
      fd_(other.fd_), writable_(other.writable_)
{
    other.addr_     = nullptr;
    other.size_     = 0;
    other.fd_       = -1;
    other.writable_ = false;
}

MemoryMappedFile& MemoryMappedFile::operator=(MemoryMappedFile&& other) noexcept {
    if (this != &other) {
        close();  // release current mapping if any
        addr_     = other.addr_;
        size_     = other.size_;
        fd_       = other.fd_;
        writable_ = other.writable_;
        other.addr_     = nullptr;
        other.size_     = 0;
        other.fd_       = -1;
        other.writable_ = false;
    }
    return *this;
}

MemoryMappedFile::~MemoryMappedFile() {
    close();
}

// ---------------------------------------------------------------------------
// Factories
// ---------------------------------------------------------------------------

MemoryMappedFile MemoryMappedFile::open_read(const std::string& path) {
    const int fd = ::open(path.c_str(), O_RDONLY | O_CLOEXEC);
    if (fd == -1) {
        throw_os_error(path, "open");
    }

    const std::size_t sz = fd_size(fd, path);

    // Handle zero-length files: mmap(0) is undefined; map 1 byte as a
    // degenerate case (the caller should check size() == 0 before reading).
    // DESIGN DECISION: we still allow mapping empty files so callers can
    // open and inspect the size without special-casing the factory call.
    const std::size_t map_len = sz == 0 ? 1 : sz;

    void* addr = ::mmap(nullptr, map_len, PROT_READ, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED) {
        const int saved = errno;
        ::close(fd);
        errno = saved;
        throw_os_error(path, "mmap");
    }

    return MemoryMappedFile(addr, sz, fd, /*writable=*/false);
}

MemoryMappedFile MemoryMappedFile::open_readwrite(const std::string& path) {
    const int fd = ::open(path.c_str(), O_RDWR | O_CLOEXEC);
    if (fd == -1) {
        throw_os_error(path, "open");
    }

    const std::size_t sz = fd_size(fd, path);
    const std::size_t map_len = sz == 0 ? 1 : sz;

    void* addr = ::mmap(nullptr, map_len,
                        PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED) {
        const int saved = errno;
        ::close(fd);
        errno = saved;
        throw_os_error(path, "mmap");
    }

    return MemoryMappedFile(addr, sz, fd, /*writable=*/true);
}

MemoryMappedFile MemoryMappedFile::create(const std::string& path,
                                          std::size_t size) {
    // O_CREAT | O_TRUNC: create new or truncate existing.
    const int fd = ::open(path.c_str(),
                          O_RDWR | O_CREAT | O_TRUNC | O_CLOEXEC,
                          0600);
    if (fd == -1) {
        throw_os_error(path, "open(create)");
    }

    // Extend (or truncate) to the requested size.
    if (::ftruncate(fd, static_cast<off_t>(size)) != 0) {
        const int saved = errno;
        ::close(fd);
        errno = saved;
        throw_os_error(path, "ftruncate");
    }

    // Map even a zero-size request as 1 byte to keep the API consistent.
    const std::size_t map_len = size == 0 ? 1 : size;

    void* addr = ::mmap(nullptr, map_len,
                        PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED) {
        const int saved = errno;
        ::close(fd);
        errno = saved;
        throw_os_error(path, "mmap(create)");
    }

    return MemoryMappedFile(addr, size, fd, /*writable=*/true);
}

// ---------------------------------------------------------------------------
// Operations
// ---------------------------------------------------------------------------

void MemoryMappedFile::flush() {
    if (!is_open() || !writable_) {
        return;
    }
    const std::size_t map_len = size_ == 0 ? 1 : size_;
    if (::msync(addr_, map_len, MS_SYNC) != 0) {
        throw LqtError(std::string("MemoryMappedFile::flush msync: ") +
                       strerror(errno));
    }
}

void MemoryMappedFile::close() noexcept {
    if (addr_ != nullptr) {
        const std::size_t map_len = size_ == 0 ? 1 : size_;
        ::munmap(addr_, map_len);
        addr_ = nullptr;
        size_ = 0;
    }
    if (fd_ != -1) {
        ::close(fd_);
        fd_ = -1;
    }
    writable_ = false;
}

} // namespace lqt
