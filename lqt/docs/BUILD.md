# LQT — Build and Test Guide

## Prerequisites

| Tool | Minimum version | Notes |
|---|---|---|
| C++ compiler | GCC 11 or Clang 14 | C++17 required; GCC 11.5.0 used in CI |
| CMake | 3.16 | 3.22.2 used in CI |
| POSIX threads | Any | Linked automatically via `Threads::Threads` |
| mmap | POSIX-compliant OS | Linux, macOS, or any POSIX system |

No third-party libraries are required. The implementation depends only on the C++ standard library and POSIX `mmap`.

---

## Build steps

Configure with `RelWithDebInfo` (optimizations on, debug symbols present):

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build -j
```

This produces `build/liblqt.a` (static library, approximately 4 MB) and one executable per file in `tests/` and `examples/`.

To build with a different type:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
```

---

## Run tests

```sh
ctest --test-dir build --output-on-failure
```

Expected result: 9 suites, 119 cases, all passing, zero warnings.

To run a specific suite by name:

```sh
ctest --test-dir build -R test_rta --output-on-failure
```

To run with verbose output from the test binary itself:

```sh
./build/test_model
```

---

## Running all tests

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build -j$(nproc)
ctest --test-dir build --output-on-failure
```

Expected output: all test suites pass (119+ test cases).

## Building examples

After building:

```sh
./build/write_lqt
./build/load_reconstruct
./build/mutate_lqt
```

## Enabling SIMD

To enable AVX2 vectorized paths (x86-64):

```sh
cmake -S . -B build -DCMAKE_CXX_FLAGS="-mavx2 -mfma"
cmake --build build -j$(nproc)
```

To force scalar (for debugging):

```sh
cmake -S . -B build -DCMAKE_CXX_FLAGS="-DLQT_FORCE_SCALAR=1"
```

---

## Single-file compile pattern

For quick experiments against the installed headers without running CMake:

```sh
g++ -std=c++17 -I include \
    src/crc.cpp src/header.cpp src/tlv.cpp \
    src/descriptor.cpp src/codebook.cpp src/reconstruct.cpp \
    src/delta.cpp src/sparse_mask.cpp src/rta.cpp \
    src/recursive_weight.cpp src/edit_log.cpp src/mutation.cpp \
    src/mmap.cpp src/model.cpp \
    my_program.cpp \
    -lpthread -o my_program
```

---

## CMake auto-glob behavior

The CMakeLists.txt uses `file(GLOB ... CONFIGURE_DEPENDS)` for all three source trees:

- `src/*.cpp` — compiled into `liblqt.a`
- `tests/test_*.cpp` — each file becomes a separately named CTest executable
- `examples/*.cpp` — each file becomes a separately named executable, linked against `liblqt.a`

This means dropping a new `src/foo.cpp`, `tests/test_foo.cpp`, or `examples/foo.cpp` file into the tree and re-running `cmake --build build` is sufficient; the file does not need to be registered anywhere.

Note: CMake re-scans the globs at configure time. If you add a file and the build does not pick it up, re-run:

```sh
cmake -S . -B build
```

---

## Troubleshooting

**`fatal error: lqt/model.h: No such file or directory`**
The `-I include` flag (or `target_include_directories`) is not set. Ensure `include/` is on the include path.

**`undefined reference to pthread_...`**
Link with `-lpthread` (or `-pthread`). CMake does this automatically via `Threads::Threads`.

**`undefined reference to lqt::...`**
Link order matters with static libraries. Put `-llqt` after your object files, or place `liblqt.a` after the translation unit that references it.

**CTest reports a test not found after adding a new test file**
Re-configure: `cmake -S . -B build`. The glob is re-evaluated at configure time, not at build time.

**mmap-related `LqtError` on Linux**
Ensure the file is readable by the current user and is not on a filesystem that does not support `mmap` (e.g., some network mounts). The error message includes `strerror(errno)` for diagnosis.
