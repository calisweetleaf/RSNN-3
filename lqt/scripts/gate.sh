#!/usr/bin/env bash
# LQT repository admission gate.
# Uses CMake/CTest when available; otherwise runs the documented direct GCC
# build without installing packages or requiring network access.
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT}/build/manual-gate"
TEST_TIMEOUT="${LQT_TEST_TIMEOUT_SECONDS:-30}"
CXX_BIN="${CXX:-g++}"

if ! command -v "${CXX_BIN}" >/dev/null 2>&1; then
    echo "gate: compiler not found: ${CXX_BIN}" >&2
    exit 2
fi

if command -v cmake >/dev/null 2>&1; then
    echo "gate: using CMake/CTest"
    cmake -S "${ROOT}" -B "${ROOT}/build/cmake-gate" \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo
    cmake --build "${ROOT}/build/cmake-gate" --parallel
    ctest --test-dir "${ROOT}/build/cmake-gate" \
        --output-on-failure --timeout "${TEST_TIMEOUT}"
    exit $?
fi

echo "gate: cmake unavailable; using direct GCC fallback"
mkdir -p "${BUILD_DIR}/obj" "${BUILD_DIR}/bin"

for src in "${ROOT}"/src/*.cpp; do
    name="$(basename "${src%.cpp}.o")"
    flags=()
    if [[ "${src}" == "${ROOT}/src/simd.cpp" ]]; then
        flags=(-mavx2 -mf16c -mfma)
    fi
    "${CXX_BIN}" -std=c++17 -I "${ROOT}/include" -pthread \
        -Wall -Wextra -Wpedantic "${flags[@]}" -c "${src}" \
        -o "${BUILD_DIR}/obj/${name}" || exit 1
done

ar rcs "${BUILD_DIR}/liblqt.a" "${BUILD_DIR}/obj"/*.o || exit 1

for src in "${ROOT}"/tests/test_*.cpp; do
    name="$(basename "${src%.cpp}")"
    "${CXX_BIN}" -std=c++17 -I "${ROOT}/include" -I "${ROOT}/tests" \
        -pthread -Wall -Wextra -Wpedantic "${src}" \
        "${BUILD_DIR}/liblqt.a" -o "${BUILD_DIR}/bin/${name}" || exit 1
done

failures=0
completed=0
passed_cases=0
for test in "${BUILD_DIR}/bin"/test_*; do
    echo "=== $(basename "${test}") ==="
    log="${BUILD_DIR}/$(basename "${test}").log"
    if timeout "${TEST_TIMEOUT}s" stdbuf -o0 "${test}" | tee "${log}"; then
        completed=$((completed + 1))
        cases="$(sed -n 's/^Total: \([0-9][0-9]*\).*Passed: \([0-9][0-9]*\).*$/\1 \2/p' "${log}" | tail -1)"
        if [[ -n "${cases}" ]]; then
            passed_cases=$((passed_cases + ${cases##* }))
        fi
    else
        failures=$((failures + 1))
        echo "gate: FAILED or TIMED OUT: $(basename "${test}")" >&2
    fi
done

echo "gate: completed_binaries=${completed} failed_or_timed_out=${failures} passed_cases=${passed_cases}"
if (( failures != 0 )); then
    exit 1
fi
exit 0
