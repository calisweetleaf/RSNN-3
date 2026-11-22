"""lqt_py — Python entry point for the C++ LQT implementation.

Import from the repo root:  ``import lqt_py`` or ``from lqt_py import LqtModel``.

Everything here is the compiled ``lqt_native`` pybind11 module (bindings/),
which links the real C++ sources in lqt/src and the header-only
RecursiveTensor library in lqt/recursive-tensor-cpp/include.  There is no
Python fallback: if the extension is not built, import fails loudly with the
build command.

Doctrine: weights are storage (LqtModel, Codebook, RecursiveWeight buckets,
RtaBlock structure, EditLog); tensors are compute (RecursiveTensor,
rta_contract/rta_project/rta_expand).  Crossing the boundary is explicit:
``RecursiveTensor.from_numpy(model.reconstruct(name).astype("float64"))``.
"""
from __future__ import annotations

try:
    from . import lqt_native as _native  # built .so copied here by bindings/CMakeLists POST_BUILD
except ImportError as exc:  # pragma: no cover - exercised only when unbuilt
    raise ImportError(
        "lqt_native extension is not built. Build it with:\n"
        "  . forge/.toolchain/env.sh\n"
        "  cmake -S bindings -B bindings/build -G Ninja -DCMAKE_BUILD_TYPE=Release "
        "-DCMAKE_AR=$(which zar) -DCMAKE_RANLIB=$(which zranlib) "
        "-Dpybind11_DIR=$(python -c 'import pybind11;print(pybind11.get_cmake_dir())')\n"
        "  cmake --build bindings/build --target lqt_native -j1"
    ) from exc

from .lqt_native import *  # noqa: F401,F403  (re-export the native API)
from .lqt_native import (  # explicit names for linters / readers
    FORMAT_VERSION, RTA_RANK, ID_NONE,
    LqtError, FormatError, ValidationError, RtaError,
    DType, TensorType, TensorFlag, SparseEncoding, RtaDistribution, MutationType,
    Distribution, NormType, ReduceOp,
    Codebook, TensorDescriptor, DeltaBuffer, RtaDimensionBlock, RtaBlock,
    RecursiveWeight, PatternLibrary, EvolutionEngine, validate_weight, dynamics,
    LqtModel, pack_indices, unpack_indices,
    sparse_build_uniform, sparse_build_bitmap, sparse_build_rle, sparse_build_hierarchical,
    RecursiveTensor, rta_contract, rta_project, rta_expand,
)

native = _native

__all__ = [n for n in dir(_native) if not n.startswith("_")] + ["native"]
