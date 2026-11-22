#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LQT Bridge: the single seam between cognition/ and the LQT substrate.

Doctrine (operator): weights are storage, tensors are compute.

- Storage: every learned parameter the triaxial backbone uses lives in an
  LQT bucket -- a quantized codebook, an index array into it, and an optional
  delta (error-preservation) term.  Effective values are reconstructed from
  the bucket, never held as free-floating float matrices.
- Compute: tensor contraction (the RTA operation the backbone uses to apply
  stored weights to the unified triaxial state) goes through a backend.

Backends
--------
``python``  The operator's originals in ``lqt/original-py-code``:
            ``recursive_tensor.RecursiveTensor.contract`` for compute and
            ``lqt_library.LQTWriter.quantize_tensor`` (k-means codebook) for
            storage.  Bucket persistence uses ``rta_numpy`` (the RTNZ v2.0
            reader/writer in ``lqt/recursive-tensor-cpp/python``, written to
            cross-check the C++ format).
``native``  The C++ pybind11 module ``lqt_native`` (``import lqt_py``) built by lane
            lqt-bindings: ``LqtModel`` storage with a hash-chained edit log,
            ``RecursiveTensor`` contraction.  Storage is the UNIFIED live model
            (:class:`UnifiedModel`): one ``model.lqt`` whose RecursiveWeight
            buckets are the base every learnable tensor of the cognitive stack
            quantizes into; the loop computes from it and edits it through
            logged D-025 mutations.  It is not a checkpoint format.

Selection: ``get_backend(name)``; ``name=None`` reads ``LQT_BACKEND`` and
defaults to ``native`` (flipped once the python-vs-native backbone parity test
passed).  There is no silent fallback: requesting ``native``
when it cannot be bound raises :class:`LQTBackendUnavailable`.

Known defects in the Python originals that this bridge routes around (they
are the operator's evidence files and are not edited here):

- ``LQTWriter.add_tensor`` with no codebook passes a 1-D k-means codebook to
  ``register_codebook``, which requires 2-D -> ValueError.  The bridge calls
  ``quantize_tensor`` itself and keeps the (K, 1) codebook in the bucket.
- ``LQTWriter.save`` opens the file ``'wb'`` and later reads it back for the
  CRC (io.UnsupportedOperation), and ``LQTLoader.load`` unpacks a 36-byte
  header the writer never wrote (32 bytes).  The ``.lqt`` container I/O in
  ``lqt_library.py`` is therefore not used; ``.lqt`` container I/O belongs to
  the native backend.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
ORIGINALS_DIR = REPO_ROOT / "lqt" / "original-py-code"
RTA_PY_DIR = REPO_ROOT / "lqt" / "recursive-tensor-cpp" / "python"

BACKEND_ENV = "LQT_BACKEND"
DEFAULT_BACKEND = "native"  # flipped after tests/test_native_backend.py backbone parity (state max-abs 6e-8)

Axes = Union[int, Tuple[Sequence[int], Sequence[int]]]

_import_lock = threading.Lock()


class LQTBackendUnavailable(RuntimeError):
    """Raised when a requested LQT backend cannot be bound. Never swallowed."""


def _ensure_path(directory: Path) -> None:
    """Put a non-package source directory on sys.path (idempotent)."""
    if not directory.is_dir():
        raise LQTBackendUnavailable(f"required source directory missing: {directory}")
    text = str(directory)
    if text not in sys.path:
        sys.path.insert(0, text)


def load_original(module_name: str) -> Any:
    """Import one of the operator's modules from ``lqt/original-py-code``.

    The directory is not a package (hyphenated name, flat sibling imports such
    as ``from recursive_tensor import RecursiveTensor``), so it is placed on
    ``sys.path`` and the module imported by its flat name.

    Args:
        module_name: e.g. ``"ethical_tensor"``, ``"metacognitive_tensor"``.

    Returns:
        The imported module object.
    """
    with _import_lock:
        _ensure_path(ORIGINALS_DIR)
        return importlib.import_module(module_name)


def _load_rta_numpy() -> Any:
    """Import the RTNZ v2.0 NumPy reader/writer that cross-checks the C++ format."""
    with _import_lock:
        _ensure_path(RTA_PY_DIR)
        return importlib.import_module("rta_numpy")


# ================================================================
# STORAGE UNIT
# ================================================================

@dataclass
class LQTBucket:
    """One stored weight: ``W = codebook[indices].reshape(shape) (+ delta)``.

    ``codebook`` is (K, vector_dim) float32 (vector_dim == 1 for scalar
    k-means), ``indices`` is a flat uint32 array, ``delta`` is optional and
    plays the epsilon (error preservation) role.
    """

    name: str
    shape: Tuple[int, ...]
    codebook: np.ndarray
    indices: np.ndarray
    bits: int
    delta: Optional[np.ndarray] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def num_entries(self) -> int:
        """Number of codebook entries actually present."""
        return int(self.codebook.shape[0])


# ================================================================
# PYTHON-ORIGINALS BACKEND
# ================================================================

class PythonOriginalsBackend:
    """LQT storage + RTA contraction from the operator's Python originals."""

    name = "python"

    def __init__(self) -> None:
        """Bind recursive_tensor, lqt_library and rta_numpy; raise if any is missing."""
        try:
            self._rt_mod = load_original("recursive_tensor")
            self._lqt_mod = load_original("lqt_library")
            self._rta = _load_rta_numpy()
        except ImportError as exc:
            raise LQTBackendUnavailable(f"python LQT originals failed to import: {exc}") from exc
        self.RecursiveTensor = self._rt_mod.RecursiveTensor

    # ---------------- compute ----------------

    def new_recursive_tensor(self, dimensions: Union[int, Sequence[int]], rank: int = 2,
                             distribution: str = "uniform", sparsity: float = 0.0) -> Any:
        """Construct an original ``RecursiveTensor``."""
        return self.RecursiveTensor(dimensions=dimensions, rank=rank,
                                    distribution=distribution, sparsity=sparsity)

    def as_recursive_tensor(self, data: np.ndarray) -> Any:
        """Wrap a dense array as a ``RecursiveTensor`` carrying exactly that payload."""
        arr = np.ascontiguousarray(data, dtype=np.float32)
        shape = tuple(int(d) for d in arr.shape) or (1,)
        rt = self.RecursiveTensor(dimensions=shape, distribution="uniform", sparsity=0.0)
        rt.data = arr.reshape(shape)
        rt.dimensions = shape
        rt.rank = len(shape)
        return rt

    def contract(self, a: Any, b: Any, axes: Axes = ((0,), (0,))) -> np.ndarray:
        """RTA contraction via ``RecursiveTensor.contract``; returns a dense ndarray."""
        left = a if isinstance(a, self.RecursiveTensor) else self.as_recursive_tensor(a)
        right = b if isinstance(b, self.RecursiveTensor) else self.as_recursive_tensor(b)
        out = left.contract(right, axes=axes)
        data = out.data
        if isinstance(data, dict):
            dense = np.zeros(out.dimensions, dtype=np.float32)
            for idx, val in data.items():
                dense[idx] = val
            return dense
        return np.asarray(data, dtype=np.float32)

    # ---------------- storage ----------------

    def quantize(self, name: str, weights: np.ndarray, bits: int = 4,
                 preserve_error: bool = False) -> LQTBucket:
        """Quantize ``weights`` into an LQT bucket with the original k-means quantizer."""
        w = np.ascontiguousarray(weights, dtype=np.float32)
        writer = self._lqt_mod.LQTWriter()
        indices, codebook = writer.quantize_tensor(name, w, bits)
        codebook = np.asarray(codebook, dtype=np.float32).reshape(len(codebook), -1)
        indices = np.asarray(indices, dtype=np.uint32).reshape(-1)
        bucket = LQTBucket(name=name, shape=tuple(w.shape), codebook=codebook,
                           indices=indices, bits=int(bits),
                           meta={"quantizer": writer.quantization_method, "backend": self.name})
        if preserve_error:
            bucket.delta = (w - self.reconstruct(bucket)).astype(np.float32)
        return bucket

    def reconstruct(self, bucket: LQTBucket) -> np.ndarray:
        """``codebook[indices]`` reshaped, plus delta when present."""
        values = bucket.codebook[bucket.indices]
        out = values.reshape(bucket.shape).astype(np.float32)
        if bucket.delta is not None:
            out = out + bucket.delta.reshape(bucket.shape)
        return out

    def save_store(self, directory: Union[str, Path], buckets: Dict[str, LQTBucket]) -> Path:
        """Persist buckets as RTNZ (.rta) component files plus a manifest."""
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        manifest: Dict[str, Any] = {"format": "lqt-bucket-store/rtnz", "backend": self.name, "buckets": {}}
        for name, b in buckets.items():
            entry = {"shape": list(b.shape), "bits": b.bits, "meta": b.meta,
                     "codebook": f"{name}.codebook.rta", "indices": f"{name}.indices.rta"}
            self._rta.save(str(root / entry["codebook"]), b.codebook, description=f"{name}:codebook")
            # uint32 is not an RTNZ dtype; float64 holds every index < 2**53 exactly.
            self._rta.save(str(root / entry["indices"]), b.indices.astype(np.float64),
                           description=f"{name}:indices")
            if b.delta is not None:
                entry["delta"] = f"{name}.delta.rta"
                self._rta.save(str(root / entry["delta"]), b.delta, description=f"{name}:delta")
            manifest["buckets"][name] = entry
        (root / "manifest.json").write_text(json.dumps(manifest, indent=2))
        return root

    def load_store(self, directory: Union[str, Path]) -> Dict[str, LQTBucket]:
        """Load buckets written by :meth:`save_store`."""
        root = Path(directory)
        manifest = json.loads((root / "manifest.json").read_text())
        buckets: Dict[str, LQTBucket] = {}
        for name, e in manifest["buckets"].items():
            codebook = np.asarray(self._rta.load(str(root / e["codebook"])), dtype=np.float32)
            indices = np.asarray(self._rta.load(str(root / e["indices"])), dtype=np.uint32).reshape(-1)
            delta = None
            if "delta" in e:
                delta = np.asarray(self._rta.load(str(root / e["delta"])), dtype=np.float32)
            buckets[name] = LQTBucket(name=name, shape=tuple(e["shape"]), codebook=codebook,
                                      indices=indices, bits=int(e["bits"]), delta=delta,
                                      meta=dict(e.get("meta", {})))
        return buckets


# ================================================================
# NATIVE BACKEND (lqt_native via lqt_py, lane lqt-bindings api board seq 40)
# ================================================================

def _import_lqt_py() -> Any:
    """Import the compiled ``lqt_py`` package (pybind11 ``lqt_native``) from the repo root.

    Raises:
        LQTBackendUnavailable: the extension is not built or fails to load.  There
        is no fallback to the Python originals.
    """
    with _import_lock:
        root = str(REPO_ROOT)
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            return importlib.import_module("lqt_py")
        except ImportError as exc:
            raise LQTBackendUnavailable(
                "LQT backend 'native' requested but lqt_py/lqt_native is not importable "
                f"({exc}). Build it with the BUILD line of board seq 40 "
                "(cmake -S bindings -B bindings/build ... -DCMAKE_CXX_FLAGS=-mcpu=baseline; "
                "cmake --build bindings/build --target lqt_native -j1), or select backend "
                "'python' explicitly."
            ) from exc


class NativeTensor:
    """Compute-side handle: a dense payload the caller may write into (``.data``)
    that is handed to ``lqt_native.RecursiveTensor`` for every operation.

    The backbone writes its input into ``rt.data`` before contracting, so the
    handle keeps a mutable float32 ndarray; the crossing into the C++ tensor
    (float64 ``rta::RecursiveTensor<double>``) happens explicitly in
    :meth:`to_native` at contraction time.
    """

    def __init__(self, data: np.ndarray, L: Any) -> None:
        self.data = np.ascontiguousarray(data, dtype=np.float32)
        self._L = L

    @property
    def dimensions(self) -> Tuple[int, ...]:
        return tuple(int(d) for d in self.data.shape)

    @property
    def rank(self) -> int:
        return int(self.data.ndim)

    def to_native(self) -> Any:
        """Explicit numpy -> C++ hop."""
        return self._L.RecursiveTensor.from_numpy(np.ascontiguousarray(self.data, dtype=np.float64))


def _pad5(shape: Sequence[int]) -> List[int]:
    """Lattice shape of a weight: its own dims padded with 1s to RTA rank 5."""
    dims = [int(d) for d in shape]
    if len(dims) > 5 or len(dims) == 0:
        raise ValueError(f"LQT RecursiveTensor storage needs 1..5 dims, got shape {tuple(shape)}")
    return dims + [1] * (5 - len(dims))


def _fp16_exact(values: np.ndarray) -> np.ndarray:
    """Round to FP16-representable float32 (the .lqt codebook wire dtype), so a
    codebook survives save -> load bit-exactly."""
    return np.asarray(values, dtype=np.float32).astype(np.float16).astype(np.float32)


def _kmeans_codebook(flat: np.ndarray, entries: int) -> Tuple[np.ndarray, np.ndarray]:
    """Initial codebook fit: the same call the Python originals make
    (``LQTWriter._kmeans_quantization``: scipy ``kmeans2(iter=100, minit='points')``
    on the global numpy RNG), so both backends quantize a fresh weight
    identically under the same seed.  This is host-side fitting of the bucket
    contents; the bucket itself is written into the C++ ``LqtModel``."""
    from scipy.cluster.vq import kmeans2
    codebook, indices = kmeans2(flat, entries, iter=100, minit="points")
    return np.asarray(codebook, dtype=np.float32).reshape(-1), np.asarray(indices, dtype=np.uint32).reshape(-1)


class NativeModelStore:
    """The triaxial backbone's Psi weights (W_R, W_E, W_M) as a view over the
    unified live model (:class:`UnifiedModel`, defined below).

    Each Psi weight is a RecursiveTensor whose every lattice position carries a
    live RecursiveWeight bucket quantized into the shared RW base (codebook 0):
    B = nearest base entry, T = position, eps = residual.  ``put`` on an existing
    weight is ONE logged D-025 ``edit_recursive_weights`` mutation over the
    changed buckets (hash-chained, rollback-able); there is no separate
    checkpoint image and no per-step Psi-only file.  ``save`` writes the whole
    unified model (``model.lqt``) and a ``manifest.json`` pointing at it.

    ``bits`` passed to ``put`` is recorded but not used: every tensor shares the
    8-bit RW base (BASE_BITS); exactness comes from eps.
    """

    def __init__(self, L: Any, unified: Optional["UnifiedModel"] = None) -> None:
        self.L = L
        self.unified = unified if unified is not None else UnifiedModel(L)
        self._put_ops: List[Tuple[str, int]] = []
        self.requested_bits: Dict[str, int] = {}

    @property
    def model(self) -> Any:
        return self.unified.model

    @property
    def meta(self) -> Dict[str, Dict[str, Any]]:
        return {n: m for n, m in self.unified.meta.items() if m["group"] == "psi"}

    def names(self) -> List[str]:
        return list(self.meta)

    def reconstruct(self, name: str) -> np.ndarray:
        return np.array(self.unified.cache[name], dtype=np.float32, copy=True)

    def bucket_view(self, name: str) -> LQTBucket:
        m = self.unified.meta[name]
        b, eps, _t, _n = self.model.recursive_weight_arrays(name)
        return LQTBucket(name=name, shape=tuple(m["shape"]), codebook=self.unified.base.reshape(-1, 1),
                         indices=np.asarray(b, np.uint32), bits=BASE_BITS,
                         delta=np.asarray(eps, np.float32).reshape(tuple(m["shape"])),
                         meta={"backend": "native", "layout": "unified RW buckets (D-024/D-025)",
                               "scale": m["scale"], "requested_bits": self.requested_bits.get(name)})

    def put(self, name: str, weights: np.ndarray, bits: int = 4, preserve_error: bool = False) -> LQTBucket:
        w = np.ascontiguousarray(weights, dtype=np.float32)
        self.requested_bits[name] = int(bits)
        if name not in self.unified.meta:
            self.unified.add(name, w, "psi", logged=False)
        else:
            _, ops = self.unified.edit(name, w)
            self._put_ops.append((name, ops))
        return self.bucket_view(name)

    def verify_edit_log(self) -> bool:
        return bool(self.model.verify_edit_log())

    def edit_log(self) -> List[Dict[str, Any]]:
        return list(self.model.edit_log())

    def rollback_updates(self, n: int = 1) -> List[str]:
        """Undo the last ``n`` Psi puts (only valid while they are the newest mutations)."""
        if n > len(self._put_ops):
            raise ValueError(f"only {len(self._put_ops)} updates on the undo stack, asked for {n}")
        undone, total = [], 0
        for _ in range(n):
            name, ops = self._put_ops.pop()
            total += ops
            undone.append(name)
        self.unified.rollback(total)
        return undone

    def save(self, directory: Union[str, Path]) -> Path:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        target = self.unified.path if self.unified.path is not None else root / UNIFIED_FILE
        info = self.unified.save(target)
        manifest = {"format": "lqt-unified", "file": str(Path(info["file"]).resolve()), **info,
                    "psi": {n: {"shape": m["shape"], "scale": m["scale"]} for n, m in self.meta.items()}}
        (root / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
        return root

    def load(self, directory: Union[str, Path]) -> None:
        root = Path(directory)
        manifest = json.loads((root / "manifest.json").read_text())
        if manifest.get("format") != "lqt-unified":
            raise LQTBackendUnavailable(f"{root}: manifest format {manifest.get('format')!r} is not 'lqt-unified' "
                                        "(pre-unification psi_weights.lqt stores are not loaded)")
        target = Path(manifest["file"]).resolve()
        if self.unified.path is not None and self.unified.path.resolve() == target and self.names():
            return  # the bound unified model was loaded from this file already
        self.unified = UnifiedModel.load(self.L, target)
        self._put_ops = []


class NativeBackend:
    """C++ backend over ``lqt_py`` (pybind11 ``lqt_native``).

    Storage = ``LqtModel`` / ``Codebook`` / ``DeltaBuffer`` / ``RtaBlock`` /
    ``RecursiveWeight`` (see :class:`NativeModelStore`).  Compute =
    ``lqt_native.RecursiveTensor`` (``rta::RecursiveTensor<double>``) contraction.
    Crossing between them is an explicit numpy hop: ``LqtModel.reconstruct`` ->
    float32 ndarray -> ``RecursiveTensor.from_numpy(float64)``.  Construction
    raises :class:`LQTBackendUnavailable` if the extension cannot be imported or
    lacks a required symbol; nothing falls back to Python.
    """

    name = "native"
    REQUIRED = ("LqtModel", "Codebook", "TensorDescriptor", "DeltaBuffer", "RtaBlock",
                "RtaDimensionBlock", "RecursiveWeight", "RecursiveTensor", "DType", "TensorType",
                "SparseEncoding", "Distribution", "ID_NONE", "FormatError")

    def __init__(self) -> None:
        self.L = _import_lqt_py()
        missing = [s for s in self.REQUIRED if not hasattr(self.L, s)]
        if missing:
            raise LQTBackendUnavailable(f"lqt_native is missing required symbols: {missing}")

    # ---------------- compute ----------------

    def new_recursive_tensor(self, dimensions: Union[int, Sequence[int]], rank: int = 2,
                             distribution: str = "uniform", sparsity: float = 0.0) -> NativeTensor:
        """Dense compute tensor with a writable payload.

        ``uniform`` draws U(-0.01, 0.01) from the global numpy RNG exactly as the
        original ``RecursiveTensor`` does (same range, same RNG stream, so runs
        stay comparable across backends); other distributions are drawn by the
        C++ ``RecursiveTensor`` with a seed taken from the numpy RNG.
        """
        shape = [int(dimensions)] * int(rank) if isinstance(dimensions, (int, np.integer)) else [int(d) for d in dimensions]
        if distribution == "uniform":
            data = np.random.uniform(-0.01, 0.01, shape).astype(np.float32)
        else:
            dist = {"normal": self.L.Distribution.Normal, "power_law": self.L.Distribution.PowerLaw,
                    "orthogonal": self.L.Distribution.Orthogonal}.get(distribution)
            if dist is None:
                raise ValueError(f"native backend: unsupported distribution {distribution!r}")
            seed = int(np.random.randint(0, 2**31 - 1))
            data = self.L.RecursiveTensor(shape, dist, float(sparsity), seed).to_numpy()
        return NativeTensor(data, self.L)

    def as_recursive_tensor(self, data: np.ndarray) -> NativeTensor:
        arr = np.asarray(data, dtype=np.float32)
        return NativeTensor(arr.reshape(arr.shape or (1,)), self.L)

    def _to_native(self, x: Any) -> Any:
        if isinstance(x, NativeTensor):
            return x.to_native()
        if isinstance(x, self.L.RecursiveTensor):
            return x
        arr = np.asarray(x, dtype=np.float64)
        return self.L.RecursiveTensor.from_numpy(np.ascontiguousarray(arr.reshape(arr.shape or (1,))))

    def contract(self, a: Any, b: Any, axes: Axes = ((0,), (0,))) -> np.ndarray:
        """RTA contraction in C++ (GIL released); returns a dense float32 ndarray.

        ``axes`` follows the original's convention: an int ``n`` contracts the
        last n axes of ``a`` with the first n of ``b`` (0 = outer product), or a
        pair of axis sequences.
        """
        left, right = self._to_native(a), self._to_native(b)
        if isinstance(axes, (int, np.integer)):
            n = int(axes)
            ax_a = list(range(left.rank - n, left.rank))
            ax_b = list(range(n))
        else:
            ax_a = [int(i) for i in axes[0]]
            ax_b = [int(i) for i in axes[1]]
        out = left.contract(right, ax_a, ax_b)
        return np.asarray(out.to_numpy(), dtype=np.float32)

    # ---------------- storage ----------------

    def create_storage(self) -> NativeModelStore:
        """Psi weight store over the bound unified model (:func:`bind_unified`),
        or over a fresh UnifiedModel when none is bound."""
        return NativeModelStore(self.L, unified=_UNIFIED)


# ================================================================
# UNIFIED MODEL: one live .lqt that IS the cognitive stack's weights
# ================================================================
#
# Operator correction (Daeron, 2026-11-21): LQT is not an archive or a
# checkpoint format.  The RecursiveWeights are the BASE and every learnable
# tensor of the cognitive stack quantizes INTO that base inside ONE .lqt file.
# The loop loads that file, computes from it, and every change it makes to a
# weight is a logged edit of the same in-memory model, which is saved back to
# the same file.
#
# Layout (one LqtModel):
#   Codebook 0  "RW base": 2**BASE_BITS scalar entries, uniform lattice on
#               [-1, 1], FP16-exact.  Every RecursiveWeight bucket's B and every
#               structural index in the file points into this one table.
#   Per tensor  TensorDescriptor(TensorType.RecursiveTensor, shape = own shape
#               padded with 1s to the RTA rank-5 lattice, dtype UINT8,
#               codebook 0, scale = max|w|) + RtaBlock(dims = that lattice,
#               Uniform: every position selected for computation, metadata =
#               original shape / group / representation) and EITHER
#     "buckets":  one RecursiveWeight per lattice position, B = nearest base
#                 entry to w/scale, T = the position, eps = [w - base[B]*scale].
#                 Value (D-024) = base[B]*scale + Phi(0) + mean(eps).  Edited
#                 with the D-025 logged op edit_recursive_weights.
#     "base_eps": the D-024 structural base term of the same base table for
#                 positions without a bucket: index array B + FP32 DeltaBuffer
#                 eps.  Value = base[B]*scale + eps.  Edited with the logged
#                 ops hot_swap_module (B) + update_delta (eps).  Used only for
#                 tensors above BUCKET_LIMIT (4096) elements present at genesis:
#                 a scalar RecursiveWeight serializes to ~120 bytes, so buckets
#                 for every element of the 5.4M-parameter torch heads made a
#                 268 MB file (measured, run 2026-11-21_unified_seed0 first pass).
#   Tensors that first appear during a run are attached with the logged D-025
#   TensorAttach op (always "buckets"); tensors that disappear are removed with
#   the logged TensorDetach op.
#
# Live state is always written FROM the model: after load and after every
# edit, the live numpy/torch tensor is set to model.reconstruct(name), so the
# loop computes from the model's values and live == reconstruct exactly.

BASE_CODEBOOK_ID = 0
BASE_BITS = 8
BUCKET_LIMIT = 4096
UNIFIED_FILE = "model.lqt"
RESCALE_HEADROOM = 1.25   # a re-quantized tensor gets scale = 1.25 * peak so slow growth does not re-scale every step

_UNIFIED: Optional["UnifiedModel"] = None


def bind_unified(model: Optional["UnifiedModel"]) -> None:
    """Make ``model`` the process-wide unified model that native LQT stores
    (the triaxial backbone's Psi store) attach to.  ``None`` unbinds."""
    global _UNIFIED
    _UNIFIED = model


def bound_unified() -> Optional["UnifiedModel"]:
    return _UNIFIED


def _base_table() -> np.ndarray:
    return _fp16_exact(np.linspace(-1.0, 1.0, 2 ** BASE_BITS, dtype=np.float32))


class LiveTensor:
    """Accessor for one live tensor of the running cognitive stack."""

    def __init__(self, name: str, group: str, get, set_) -> None:
        self.name, self.group, self._get, self._set = name, group, get, set_

    def get(self) -> np.ndarray:
        return np.asarray(self._get(), dtype=np.float32)

    def set(self, value: np.ndarray) -> None:
        self._set(value)


class UnifiedModel:
    """The single live ``model.lqt``: RW base + every learnable tensor."""

    def __init__(self, L: Any, path: Optional[Union[str, Path]] = None) -> None:
        self.L = L
        self.path = Path(path) if path is not None else None
        self.model = L.LqtModel()
        self.base = _base_table()
        self.model.add_codebook(L.Codebook.from_numpy(BASE_CODEBOOK_ID, self.base))
        self.meta: Dict[str, Dict[str, Any]] = {}
        self.cache: Dict[str, np.ndarray] = {}     # last reconstruct per name (never mutated in place)
        self._next_delta = 1
        self.loaded_from: Optional[Dict[str, Any]] = None
        self.op_counts: Dict[str, int] = {}
        # Non-tensor identity of runtime-created entities (text, keys, ints), JSON,
        # carried in the module graph so the owners of their tensors can be rebuilt
        # on load.  Values never live here: every float stays a model tensor.
        self.stack: Dict[str, Any] = {}

    # ---------------- quantization into the base ----------------

    def quantize(self, flat: np.ndarray, scale: float) -> Tuple[np.ndarray, np.ndarray]:
        """B = nearest base entry to flat/scale, eps = flat - base[B]*scale (float32)."""
        x = (flat / np.float32(scale)).astype(np.float32)
        hi = np.searchsorted(self.base, x).clip(1, self.base.shape[0] - 1)
        lo = hi - 1
        b = np.where(np.abs(x - self.base[lo]) <= np.abs(self.base[hi] - x), lo, hi).astype(np.uint32)
        eps = (flat - self.base[b] * np.float32(scale)).astype(np.float32)
        return b, eps

    @staticmethod
    def _scale(flat: np.ndarray) -> float:
        m = float(np.max(np.abs(flat))) if flat.size else 0.0
        return m if m > 0.0 and np.isfinite(m) else 1.0

    def _descriptor(self, name: str, shape: Tuple[int, ...], scale: float, delta_id: int) -> Any:
        L = self.L
        lattice = _pad5(shape or (1,))
        return L.TensorDescriptor(name, lattice, L.DType.UINT8, L.TensorType.RecursiveTensor,
                                  BASE_CODEBOOK_ID, delta_id, L.ID_NONE, float(scale), 0, 0)

    @staticmethod
    def _md(shape: Tuple[int, ...], group: str, rep: str) -> List[Tuple[str, str]]:
        return [("shape", ",".join(str(int(s)) for s in shape)), ("group", group), ("repr", rep)]

    # ---------------- add / attach ----------------

    def add(self, name: str, value: np.ndarray, group: str, logged: bool, headroom: float = 1.0) -> np.ndarray:
        """Quantize ``value`` into the base and add it (builder at genesis, D-025
        TensorAttach when ``logged``). Returns the reconstruct the live tensor must take."""
        L = self.L
        v = np.ascontiguousarray(value, dtype=np.float32)
        shape = tuple(int(s) for s in v.shape)
        if len(shape) > 5:
            raise ValueError(f"{name}: rank {len(shape)} > RTA rank 5")
        flat = v.reshape(-1)
        if not np.all(np.isfinite(flat)):
            raise ValueError(f"{name}: non-finite values cannot be quantized into the RW base")
        scale = self._scale(flat) * float(headroom)
        b, eps = self.quantize(flat, scale)
        rep = "buckets" if (logged or flat.size <= BUCKET_LIMIT) else "base_eps"
        if rep == "buckets":
            desc = self._descriptor(name, shape, scale, L.ID_NONE)
            self.model.attach_recursive_tensor_scalar(desc, b, eps, np.ones(flat.size, np.uint32),
                                                      bool(logged), self._md(shape, group, rep))
            delta_id = None
        else:
            delta_id = self._next_delta
            self._next_delta += 1
            if delta_id >= 0xFFFF:
                raise ValueError("delta id space (u16) exhausted")
            desc = self._descriptor(name, shape, scale, delta_id)
            desc.validate()
            self.model.add_delta(L.DeltaBuffer(delta_id, eps, None, L.DType.FP32))
            self.model.add_tensor_indices(desc, b)
            self.model.add_rta_block(name, L.RtaBlock(L.RtaDimensionBlock(_pad5(shape or (1,))),
                                                      L.SparseEncoding.Uniform,
                                                      L.sparse_build_uniform(int(flat.size)),
                                                      self._md(shape, group, rep)))
        if logged:
            self.op_counts["TensorAttach"] = self.op_counts.get("TensorAttach", 0) + 1
        self.meta[name] = {"shape": list(shape), "group": group, "repr": rep, "scale": scale,
                           "delta_id": delta_id, "elements": int(flat.size)}
        return self.refresh(name)

    def detach(self, name: str) -> None:
        self.model.detach_tensor(name)
        self.op_counts["TensorDetach"] = self.op_counts.get("TensorDetach", 0) + 1
        self.meta.pop(name, None)
        self.cache.pop(name, None)

    # ---------------- read ----------------

    def reconstruct(self, name: str, model: Any = None) -> np.ndarray:
        m = model if model is not None else self.model
        shape = tuple(self.meta[name]["shape"])
        return np.asarray(m.reconstruct(name, False), dtype=np.float32).reshape(shape)

    def refresh(self, name: str) -> np.ndarray:
        arr = self.reconstruct(name)
        arr.setflags(write=False)
        self.cache[name] = arr
        return arr

    # ---------------- logged edits ----------------

    def edit(self, name: str, value: np.ndarray) -> Tuple[np.ndarray, int]:
        """Make the model hold ``value`` for ``name`` through logged ops only.
        Returns (reconstruct, number of logged mutations)."""
        m = self.meta[name]
        v = np.ascontiguousarray(value, dtype=np.float32)
        if tuple(v.shape) != tuple(m["shape"]):
            raise ValueError(f"{name}: shape {v.shape} != stored {tuple(m['shape'])}")
        flat = v.reshape(-1)
        if not np.all(np.isfinite(flat)):
            raise ValueError(f"{name}: non-finite update refused (would poison the base)")
        peak = float(np.max(np.abs(flat))) if flat.size else 0.0
        if peak > m["scale"]:
            # The value left the range its base lattice was scaled for: B would
            # saturate and eps would carry the whole value.  Re-quantize the
            # tensor into the base at the new scale as ONE logged TensorAttach
            # (replace; rollback restores the old descriptor, block and buckets).
            if m["repr"] != "buckets":
                raise LQTBackendUnavailable(
                    f"{name}: base_eps tensor ({m['elements']} elements) outgrew its scale "
                    f"{m['scale']} -> {peak}; the format has no logged descriptor-scale edit for it")
            self.op_counts["Rescale"] = self.op_counts.get("Rescale", 0) + 1
            return self.add(name, v, m["group"], logged=True, headroom=RESCALE_HEADROOM), 1
        b, eps = self.quantize(flat, m["scale"])
        ops = 0
        if m["repr"] == "buckets":
            cur = self.cache[name].reshape(-1)
            slots = np.nonzero(flat != cur)[0].astype(np.uint32)
            if slots.size:
                self.model.edit_recursive_weights_scalar(name, slots, b[slots], eps[slots],
                                                         np.ones(slots.size, np.uint32))
                ops += 1
                self.op_counts["RecursiveWeightEdit"] = self.op_counts.get("RecursiveWeightEdit", 0) + 1
        else:
            L = self.L
            old_b = np.asarray(self.model.indices(name), dtype=np.uint32).reshape(-1)
            if not np.array_equal(old_b, b):
                self.model.hot_swap_module(name, L.pack_indices(b, L.DType.UINT8))
                ops += 1
                self.op_counts["ModuleSwap"] = self.op_counts.get("ModuleSwap", 0) + 1
            self.model.update_delta(L.DeltaBuffer(m["delta_id"], eps, None, L.DType.FP32))
            ops += 1
            self.op_counts["DeltaUpdate"] = self.op_counts.get("DeltaUpdate", 0) + 1
        return self.refresh(name), ops

    # ---------------- live binding ----------------

    def genesis(self, live: Dict[str, LiveTensor]) -> None:
        """Builder: put every live tensor not yet in the model into it (no log entries)."""
        for name, t in live.items():
            if name in self.meta:
                continue
            t.set(self.add(name, t.get(), t.group, logged=False))

    def apply_to_live(self, live: Dict[str, LiveTensor]) -> Dict[str, Any]:
        """After load: every live tensor takes its value from the model.  A live
        tensor the model lacks, or a stored one with no live counterpart, is an error."""
        missing = sorted(set(live) - set(self.meta))
        if missing:
            raise LQTBackendUnavailable(f"model.lqt lacks {len(missing)} live tensors, e.g. {missing[:5]}")
        orphan = sorted(n for n in self.meta if n not in live and self.meta[n]["group"] != "psi")
        if orphan:
            raise LQTBackendUnavailable(f"model.lqt holds {len(orphan)} tensors with no live counterpart, e.g. {orphan[:5]}")
        for name, t in live.items():
            got = t.get()
            if tuple(got.shape) != tuple(self.meta[name]["shape"]):
                raise LQTBackendUnavailable(f"{name}: live shape {got.shape} != model {self.meta[name]['shape']}")
            t.set(self.cache[name])
        return {"applied": len(live)}

    def sync(self, live: Dict[str, LiveTensor], keep: Any = ()) -> Dict[str, int]:
        """After a loop step: every change the step made to a live tensor becomes
        logged edits on the model, and the live tensor takes the model's value.
        Stored tensors named in ``keep`` (dormant: no live owner in this process)
        are left in the model instead of being detached."""
        stats = {"edited": 0, "attached": 0, "detached": 0, "ops": 0, "elements_changed": 0, "names": []}
        for name, t in live.items():
            v = t.get()
            if name not in self.meta:
                t.set(self.add(name, v, t.group, logged=True))
                stats["attached"] += 1
                stats["ops"] += 1
                stats["names"].append(("attach", name))
                continue
            if tuple(v.shape) != tuple(self.meta[name]["shape"]):
                self.model.detach_tensor(name)      # logged; then re-attach with the new shape
                self.op_counts["TensorDetach"] = self.op_counts.get("TensorDetach", 0) + 1
                t.set(self.add(name, v, t.group, logged=True))
                stats["attached"] += 1
                stats["detached"] += 1
                stats["ops"] += 2
                continue
            cur = self.cache[name]
            if np.array_equal(v, cur):
                continue
            stats["elements_changed"] += int(np.count_nonzero(v != cur))
            new, ops = self.edit(name, v)
            t.set(new)
            stats["edited"] += 1
            stats["ops"] += ops
            stats["names"].append(("edit", name))
        for name in [n for n in self.meta if n not in live and self.meta[n]["group"] != "psi" and n not in keep]:
            self.detach(name)
            stats["names"].append(("detach", name))
            stats["detached"] += 1
            stats["ops"] += 1
        return stats

    # ---------------- rollback ----------------

    def rollback(self, n: int) -> None:
        """Undo the last ``n`` logged mutations and re-derive meta/cache from the model."""
        self.model.rollback(int(n))
        self._reindex()

    def _reindex(self) -> None:
        meta: Dict[str, Dict[str, Any]] = {}
        for name in self.model.tensor_names():
            d = self.model.descriptor(name)
            md = dict(self.model.rta_block(name).metadata)
            shape = [int(s) for s in md["shape"].split(",") if s != ""]
            meta[name] = {"shape": shape, "group": md["group"], "repr": md["repr"],
                          "scale": float(d.scale),
                          "delta_id": None if d.delta_id == self.L.ID_NONE else int(d.delta_id),
                          "elements": int(np.prod(shape)) if shape else 1}
        self.meta = meta
        self.cache = {}
        for name in meta:
            self.refresh(name)

    # ---------------- persistence ----------------

    def _graph(self) -> str:
        return json.dumps({"unified": {"base_codebook": BASE_CODEBOOK_ID, "base_bits": BASE_BITS,
                                       "bucket_limit": BUCKET_LIMIT, "next_delta": self._next_delta,
                                       "loaded_from": self.loaded_from,
                                       **({"stack": self.stack} if self.stack else {})}},
                          sort_keys=True, default=str)

    def save(self, path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        import hashlib
        p = Path(path) if path is not None else self.path
        if p is None:
            raise ValueError("UnifiedModel.save: no path")
        p.parent.mkdir(parents=True, exist_ok=True)
        self.model.module_graph_json = self._graph()
        tmp = p.with_suffix(".lqt.tmp")
        self.model.save(str(tmp))
        os.replace(tmp, p)
        self.path = p
        data = p.read_bytes()
        return {"file": str(p), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "edit_log_entries": len(self.model.edit_log()),
                "edit_log_tail_hash": self.model.edit_log_tail_hash,
                "verify_edit_log": bool(self.model.verify_edit_log())}

    @classmethod
    def load(cls, L: Any, path: Union[str, Path]) -> "UnifiedModel":
        import hashlib
        p = Path(path)
        self = cls.__new__(cls)
        self.L = L
        self.path = p
        self.model = L.LqtModel.load(str(p))
        if not self.model.verify_edit_log():
            raise LQTBackendUnavailable(f"{p}: edit log hash chain does not verify")
        cb = self.model.codebook(BASE_CODEBOOK_ID)
        if cb is None:
            raise LQTBackendUnavailable(f"{p}: no RW base codebook {BASE_CODEBOOK_ID}")
        self.base = np.asarray(cb.values(), dtype=np.float32).reshape(-1)
        graph = json.loads(self.model.module_graph_json or "{}").get("unified")
        if graph is None:
            raise LQTBackendUnavailable(f"{p}: not a unified model (module graph has no 'unified')")
        self._next_delta = int(graph["next_delta"])
        self.stack = dict(graph.get("stack") or {})
        self.op_counts = {}
        self.loaded_from = {"file": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                            "edit_log_entries": len(self.model.edit_log()),
                            "edit_log_tail_hash": self.model.edit_log_tail_hash}
        self._reindex()
        return self

    def table(self) -> List[Dict[str, Any]]:
        """Per tensor: name, shape, group, representation, base, bits, scale and
        the error of the base term alone (B without eps) vs the stored value."""
        rows = []
        for name, m in self.meta.items():
            val = self.cache[name].reshape(-1)
            b, _ = self.quantize(val, m["scale"])
            base_only = self.base[b] * np.float32(m["scale"])
            rows.append({"name": name, "shape": m["shape"], "group": m["group"], "repr": m["repr"],
                         "base": f"codebook {BASE_CODEBOOK_ID} (RW base, {2 ** BASE_BITS} entries)",
                         "bits": BASE_BITS, "scale": m["scale"], "elements": m["elements"],
                         "base_only_max_abs_err": float(np.max(np.abs(val - base_only))) if val.size else 0.0})
        return rows


# ---------------- live tensor enumeration of the cognitive stack ----------------

# Path fragments that mark activations, histories, caches, corpora and the Psi
# store itself (Psi is handled by NativeModelStore) -- not learnable state.
LIVE_EXCLUDE = ("_last_state", "_state_history", "history", "_cache", "cache[", "weight_store",
                ".W[", "theorem_substrate", "documents", "_executor", "_lock", "last_output",
                "last_state", "_buffer_log")
MOTIVATION_CONTAINERS = ("proto_values", "emerging_values", "values", "proto_goals", "goals", "patterns")


def _group_of(path: str) -> str:
    for key, group in (("recursive_tensor", "rta"), ("meta_reflective_head", "meta_reflective"),
                       ("metacog", "metacognitive"), ("ethical", "ethical"),
                       ("weight_registry", "rw_registry"), ("meta_cognitive_weight", "rw_registry"),
                       ("autodidactic", "iala"), ("iala.", "iala"), ("backbone", "backbone")):
        if key in path:
            return group
    return "engine"


def collect_live_tensors(engine: Any, iala: Any = None, bayes: Any = None,
                         motivation: Any = None) -> Dict[str, LiveTensor]:
    """Every learnable float tensor of the running cognitive stack, by stable path.

    - torch parameters and buffers of the CognitiveEngine (thought encoder,
      heads, meta-reflective head, RecursiveWeight modules, backbone modules)
      and of every module reachable from it (the RW registry);
    - float numpy arrays / torch tensors held by plain objects reachable from
      the engine (triaxial field: RTA tensor, ethical state, metacognitive
      tensor) and from the IALA learner;
    - Bayesian beliefs: one vector per parameter (sorted distribution_params + uncertainty);
    - motivation: one vector per value/goal entity (its float fields, sorted).
    Psi (W_R/W_E/W_M) is excluded here: it lives in the store as RW buckets.
    """
    import torch
    out: Dict[str, LiveTensor] = {}
    seen_tensor: set = set()
    seen_obj: set = set()

    def add_torch(path: str, t: Any) -> None:
        if id(t) in seen_tensor or not t.dtype.is_floating_point or t.numel() == 0:
            return
        seen_tensor.add(id(t))

        def _set(v, t=t):
            with torch.no_grad():
                t.data.copy_(torch.from_numpy(np.array(v, copy=True, order="C")).to(device=t.device, dtype=t.dtype).reshape(t.shape))
        out[path] = LiveTensor(path, _group_of(path), lambda t=t: t.detach().cpu().float().numpy(), _set)

    def add_np(path: str, a: np.ndarray) -> None:
        if id(a) in seen_tensor or a.dtype.kind != "f" or a.size == 0:
            return
        seen_tensor.add(id(a))

        def _set(v, a=a):
            a[...] = np.asarray(v).reshape(a.shape).astype(a.dtype)
        out[path] = LiveTensor(path, _group_of(path), lambda a=a: a, _set)

    queue: List[Tuple[Any, str, int]] = []

    def visit(obj: Any, path: str, depth: int) -> None:
        if depth > 7 or any(x in path for x in LIVE_EXCLUDE):
            return
        if isinstance(obj, torch.Tensor):
            add_torch(path, obj)
            return
        if isinstance(obj, np.ndarray):
            add_np(path, obj)
            return
        if obj is None or isinstance(obj, (str, bytes, int, float, bool, complex, type, Path)):
            return
        if id(obj) in seen_obj:
            return
        seen_obj.add(id(obj))
        if isinstance(obj, dict):
            if len(obj) > 4096:
                raise LQTBackendUnavailable(f"{path}: dict of {len(obj)} entries exceeds the enumerator bound")
            for k, v in obj.items():
                queue.append((v, f"{path}[{k!r}]", depth + 1))
            return
        if isinstance(obj, (list, tuple)):
            if len(obj) > 1024:
                return  # bulk records (corpora), not tensors; bound is explicit
            for i, v in enumerate(obj):
                queue.append((v, f"{path}[{i}]", depth + 1))
            return
        mod = type(obj).__module__ or ""
        if isinstance(obj, torch.nn.Module):
            for n, p in obj.named_parameters(recurse=False):
                add_torch(f"{path}.{n}", p)
            for n, b in obj.named_buffers(recurse=False):
                if b is not None:
                    add_torch(f"{path}.{n}", b)
            for n, c in obj.named_children():
                queue.append((c, f"{path}.{n}", depth + 1))
            attrs = {k: v for k, v in vars(obj).items() if k not in ("_parameters", "_buffers", "_modules")}
        elif mod.split(".")[0] in ("builtins", "logging", "threading", "concurrent", "torch", "numpy", "scipy",
                                   "queue", "_thread", "sqlite3", "pathlib", "collections", "enum", "re",
                                   "networkx", "random") or not hasattr(obj, "__dict__"):
            return
        else:
            attrs = vars(obj)
        for k, v in attrs.items():
            queue.append((v, f"{path}.{k}", depth + 1))

    def walk(root: Any, path: str) -> None:
        """Breadth-first, so every object is named by its shortest path from the root."""
        queue.append((root, path, 0))
        while queue:
            visit(*queue.pop(0))

    walk(engine, "engine")
    if iala is not None:
        walk(iala, "iala")   # usually the engine's own learner: deduplicated by identity

    if bayes is not None:
        for pname, belief in sorted(bayes.parameter_beliefs.items()):
            keys = sorted(k for k, v in belief.distribution_params.items() if isinstance(v, (int, float)))

            def _get(b=belief, keys=keys):
                return np.array([float(b.distribution_params[k]) for k in keys] + [float(b.uncertainty)],
                                np.float32)

            def _set(v, b=belief, keys=keys):
                v = np.asarray(v, np.float32).reshape(-1)
                for i, k in enumerate(keys):
                    b.distribution_params[k] = float(v[i])
                b.uncertainty = float(v[len(keys)])
            name = f"bayes.beliefs[{pname!r}]"
            out[name] = LiveTensor(name, "bayes", _get, _set)

    if motivation is not None:
        containers: List[Tuple[str, Dict[str, Any]]] = []

        seen_cont: set = set()

        def find(obj: Any, path: str, depth: int) -> None:
            if depth > 4 or not hasattr(obj, "__dict__"):
                return
            for k, v in vars(obj).items():
                if k in MOTIVATION_CONTAINERS and isinstance(v, dict):
                    if id(v) not in seen_cont:          # shared sub-systems are stored once
                        seen_cont.add(id(v))
                        containers.append((f"{path}.{k}", v))
                elif hasattr(v, "__dict__") and (type(v).__module__ or "").startswith(("runtime", "rosemary.canon")):
                    find(v, f"{path}.{k}", depth + 1)
        find(motivation, "motivation", 0)
        for cpath, cont in containers:
            for eid, ent in sorted(cont.items(), key=lambda kv: str(kv[0])):
                fields = sorted(k for k, v in vars(ent).items()
                                if isinstance(v, float) and not isinstance(v, bool)
                                and not any(t in k for t in ("time", "created", "updated", "last_")))
                if not fields:
                    continue

                def _get(e=ent, f=fields):
                    return np.array([float(getattr(e, k)) for k in f], np.float32)

                def _set(v, e=ent, f=fields):
                    v = np.asarray(v, np.float32).reshape(-1)
                    for i, k in enumerate(f):
                        setattr(e, k, float(v[i]))
                name = f"{cpath}[{eid!r}]"
                out[name] = LiveTensor(name, "motivation", _get, _set)
    return out


# ================================================================
# SELECTION + STORE
# ================================================================

_BACKENDS = {"python": PythonOriginalsBackend, "native": NativeBackend}
_instances: Dict[str, Any] = {}


def get_backend(name: Optional[str] = None) -> Any:
    """Return the backend ``name`` (or ``$LQT_BACKEND``, default ``native``).

    Raises:
        LQTBackendUnavailable: unknown name, or the backend cannot be bound.
    """
    chosen = (name or os.environ.get(BACKEND_ENV) or DEFAULT_BACKEND).strip().lower()
    if chosen not in _BACKENDS:
        raise LQTBackendUnavailable(f"unknown LQT backend {chosen!r}; expected one of {sorted(_BACKENDS)}")
    with _import_lock:
        inst = _instances.get(chosen)
    if inst is None:
        inst = _BACKENDS[chosen]()
        with _import_lock:
            _instances[chosen] = inst
    return inst


class LQTStore:
    """Named LQT buckets with reconstruction through one backend.

    Python backend: buckets are held here (``LQTBucket``) and re-quantized on
    every ``put``.  Native backend: buckets live in one C++ ``LqtModel``
    (:class:`NativeModelStore`); ``put`` on an existing name goes through the
    model's logged edit ops, and ``buckets`` is a read view of the model.
    """

    def __init__(self, backend: Any) -> None:
        """Bind the store to a backend returned by :func:`get_backend`."""
        self.backend = backend
        self.native: Optional[NativeModelStore] = (
            backend.create_storage() if hasattr(backend, "create_storage") else None)
        self._buckets: Dict[str, LQTBucket] = {}
        self._cache: Dict[str, np.ndarray] = {}

    @property
    def buckets(self) -> Dict[str, LQTBucket]:
        """name -> bucket (for native: a fresh view of the model's codebook/indices/delta)."""
        if self.native is not None:
            return {n: self.native.bucket_view(n) for n in self.native.names()}
        return self._buckets

    @buckets.setter
    def buckets(self, value: Dict[str, LQTBucket]) -> None:
        if self.native is not None:
            raise AttributeError("native LQTStore buckets live in the LqtModel; use put()/load()")
        self._buckets = value

    def put(self, name: str, weights: np.ndarray, bits: int = 4, preserve_error: bool = False) -> LQTBucket:
        """Quantize and store ``weights`` under ``name`` (native: edit ops when ``name`` exists)."""
        if self.native is not None:
            bucket = self.native.put(name, weights, bits=bits, preserve_error=preserve_error)
        else:
            bucket = self.backend.quantize(name, weights, bits=bits, preserve_error=preserve_error)
            self._buckets[name] = bucket
        self._cache.pop(name, None)
        return bucket

    def get(self, name: str) -> np.ndarray:
        """Reconstructed effective weights for ``name`` (cached until replaced)."""
        if name not in self._cache:
            if self.native is not None:
                self._cache[name] = self.native.reconstruct(name)
            else:
                self._cache[name] = self.backend.reconstruct(self._buckets[name])
        return self._cache[name]

    def save(self, directory: Union[str, Path]) -> Path:
        """Persist all buckets through the backend (native: a verified ``.lqt`` file)."""
        if self.native is not None:
            return self.native.save(directory)
        return self.backend.save_store(directory, self._buckets)

    def load(self, directory: Union[str, Path]) -> None:
        """Replace contents with buckets loaded through the backend."""
        if self.native is not None:
            self.native.load(directory)
        else:
            self._buckets = self.backend.load_store(directory)
        self._cache.clear()

    def rollback(self, n: int = 1) -> List[str]:
        """Native only: undo the last ``n`` updates via ``LqtModel.rollback``."""
        if self.native is None:
            raise LQTBackendUnavailable("rollback needs the native backend's edit log")
        undone = self.native.rollback_updates(n)
        self._cache.clear()
        return undone

    def verify_edit_log(self) -> bool:
        """Native only: hash-chain verification of every recorded edit."""
        if self.native is None:
            raise LQTBackendUnavailable("edit log exists only on the native backend")
        return self.native.verify_edit_log()

    def summary(self) -> Dict[str, Any]:
        """Per-bucket shape, codebook size and bits (+ edit log state on native)."""
        out: Dict[str, Any] = {n: {"shape": list(b.shape), "codebook_entries": b.num_entries, "bits": b.bits,
                                   "has_delta": b.delta is not None} for n, b in self.buckets.items()}
        if self.native is not None:
            out["_edit_log"] = {"entries": len(self.native.edit_log()),
                                "tail_hash": self.native.model.edit_log_tail_hash,
                                "undo_depth": int(self.native.model.undo_depth)}
        return out


__all__ = [
    "UnifiedModel", "LiveTensor", "collect_live_tensors", "bind_unified", "bound_unified", "BASE_CODEBOOK_ID", "BASE_BITS",
    "BUCKET_LIMIT", "UNIFIED_FILE", "LQTBackendUnavailable", "LQTBucket", "LQTStore", "PythonOriginalsBackend",
    "NativeBackend", "NativeModelStore", "NativeTensor", "get_backend", "load_original", "ORIGINALS_DIR", "BACKEND_ENV",
]
