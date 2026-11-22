# bindings/ — pybind11 module `lqt_native`.
# Links the real static liblqt (lqt/, built from source here with PIC) and the
# header-only RecursiveTensor library (lqt/recursive-tensor-cpp/include).
#
#   . forge/.toolchain/env.sh
#   cmake -S bindings -B bindings/build -G Ninja -DCMAKE_BUILD_TYPE=Release \
#         -DCMAKE_AR=$(which zar) -DCMAKE_RANLIB=$(which zranlib) \
#         -Dpybind11_DIR=$(python -c 'import pybind11;print(pybind11.get_cmake_dir())')
#   cmake --build bindings/build --target lqt_native -j1
# The built .so is copied next to lqt_py/ (lqt_py/lqt_native*.so) by POST_BUILD.
cmake_minimum_required(VERSION 3.16)
project(lqt_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)   # liblqt.a is linked into a shared module
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

get_filename_component(REPO_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/.. ABSOLUTE)
set(LQT_DIR ${REPO_ROOT}/lqt)
set(RTA_INCLUDE ${LQT_DIR}/recursive-tensor-cpp/include)

# Real liblqt from lqt/src (same glob as lqt/CMakeLists.txt). Tests/examples
# are not pulled in: they belong to the lqt/ CTest build.
file(GLOB LQT_SOURCES CONFIGURE_DEPENDS ${LQT_DIR}/src/*.cpp)
add_library(lqt_pic STATIC ${LQT_SOURCES})
target_include_directories(lqt_pic PUBLIC ${LQT_DIR}/include)
find_package(Threads REQUIRED)
target_link_libraries(lqt_pic PUBLIC Threads::Threads)
# aarch64: no x86 SIMD flags (simd.h selects NEON). Mirror lqt/CMakeLists guard.
if(CMAKE_SYSTEM_PROCESSOR MATCHES "^(x86_64|AMD64|amd64|i[3-6]86)$")
  include(CheckCXXCompilerFlag)
  check_cxx_compiler_flag("-mavx2 -mf16c -mfma" LQT_CXX_HAS_AVX2_FLAGS)
  if(LQT_CXX_HAS_AVX2_FLAGS)
    set_source_files_properties(${LQT_DIR}/src/simd.cpp PROPERTIES COMPILE_OPTIONS "-mavx2;-mf16c;-mfma")
  endif()
endif()

find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# NO_EXTRAS: pybind11's default -flto makes the zig linker abort (exit 134,
# 2026-11-21). Visibility is set explicitly instead.
pybind11_add_module(lqt_native MODULE NO_EXTRAS
  lqt_native.cpp             # storage: LqtModel, Codebook, RecursiveWeight, RtaBlock, EditLog, rta_ops
  lqt_native_rta.cpp         # compute: rta::RecursiveTensor<double> core ops + .rta I/O
  lqt_native_rta_decomp.cpp) # compute: eigenstates / Tucker / MPS
# The two header-only-rta TUs are compiled at -O2: at -O3 the single rta TU was
# OOM-killed (exit 137) on the shared 7 GB sandbox while other lanes run torch.
set_source_files_properties(lqt_native_rta.cpp lqt_native_rta_decomp.cpp PROPERTIES COMPILE_OPTIONS "-O2")
set_target_properties(lqt_native PROPERTIES CXX_VISIBILITY_PRESET hidden VISIBILITY_INLINES_HIDDEN ON)
target_include_directories(lqt_native PRIVATE ${RTA_INCLUDE})
target_link_libraries(lqt_native PRIVATE lqt_pic Threads::Threads)

add_custom_command(TARGET lqt_native POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:lqt_native> ${REPO_ROOT}/lqt_py/
  COMMENT "Copying lqt_native into lqt_py/")
