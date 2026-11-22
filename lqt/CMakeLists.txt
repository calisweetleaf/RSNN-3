# LQT reference implementation — build configuration.
# Council module: A10 (integration). OWNED BY LEAD — operators do not edit this.
#
# Sources and tests are auto-globbed so parallel operators can drop new
# src/*.cpp and tests/test_*.cpp files in without touching this file.
cmake_minimum_required(VERSION 3.16)
project(lqt LANGUAGES CXX VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()

add_compile_options(-Wall -Wextra -Wpedantic)

# --- Library -----------------------------------------------------------------
file(GLOB LQT_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)
add_library(lqt STATIC ${LQT_SOURCES})
target_include_directories(lqt PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_features(lqt PUBLIC cxx_std_17)

find_package(Threads REQUIRED)
target_link_libraries(lqt PUBLIC Threads::Threads)

# Per-file AVX2/F16C/FMA flags for simd.cpp (Patch 7).
# CPU confirmed avx2+f16c+fma in /proc/cpuinfo. Applied only to simd.cpp
# so the rest of the library is not forced into a higher ISA baseline.
# 2026-11-21: guarded by target ISA. On aarch64 (this sandbox, zig/clang) the
# x86 feature flags are a hard error; simd.h then selects the NEON path.
include(CheckCXXCompilerFlag)
if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|AMD64|amd64|i[3-6]86)$")
  check_cxx_compiler_flag("-mavx2 -mf16c -mfma" LQT_CXX_HAS_AVX2_FLAGS)
  if(LQT_CXX_HAS_AVX2_FLAGS)
    set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/src/simd.cpp
        PROPERTIES COMPILE_OPTIONS "-mavx2;-mf16c;-mfma")
  endif()
endif()

# --- Tests -------------------------------------------------------------------
enable_testing()
file(GLOB LQT_TESTS CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_*.cpp)
foreach(test_src ${LQT_TESTS})
  get_filename_component(test_name ${test_src} NAME_WE)
  add_executable(${test_name} ${test_src})
  target_include_directories(${test_name} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/tests)
  target_link_libraries(${test_name} PRIVATE lqt)
  add_test(NAME ${test_name} COMMAND ${test_name})
endforeach()

# --- Examples (optional, globbed) --------------------------------------------
file(GLOB LQT_EXAMPLES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.cpp)
foreach(example_src ${LQT_EXAMPLES})
  get_filename_component(example_name ${example_src} NAME_WE)
  add_executable(${example_name} ${example_src})
  target_link_libraries(${example_name} PRIVATE lqt)
endforeach()

# --- Explicit test target helper (Patch 2 additions) -------------------------
# add_lqt_test(<test_name> <relative_source_path>) — declares a test executable,
# wires include + link, and registers it with CTest. Idempotent: skips if the
# target is already declared by the auto-globbed loop above.
function(add_lqt_test test_name test_src)
  if(NOT TARGET ${test_name})
    add_executable(${test_name} ${CMAKE_CURRENT_SOURCE_DIR}/${test_src})
    target_include_directories(${test_name} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/tests)
    target_link_libraries(${test_name} PRIVATE lqt)
    add_test(NAME ${test_name} COMMAND ${test_name})
  endif()
endfunction()

# Patch 2 test suites (model mutation surface + integration round-trip).
add_lqt_test(test_model_mutations tests/test_model_mutations.cpp)
add_lqt_test(test_integration_roundtrip tests/test_integration_roundtrip.cpp)
add_lqt_test(test_rollback tests/test_rollback.cpp)

# Patch 2 example binaries (explicit so they survive a glob-less reconfigure).
if(NOT TARGET write_lqt)
  add_executable(write_lqt examples/write_lqt.cpp)
  target_link_libraries(write_lqt lqt)
endif()
if(NOT TARGET load_reconstruct)
  add_executable(load_reconstruct examples/load_reconstruct.cpp)
  target_link_libraries(load_reconstruct lqt)
endif()
if(NOT TARGET mutate_lqt)
  add_executable(mutate_lqt examples/mutate_lqt.cpp)
  target_link_libraries(mutate_lqt lqt)
endif()
