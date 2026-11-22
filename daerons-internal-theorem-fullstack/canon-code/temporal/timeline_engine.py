"""
EIGENLOOM/COSMOS Lineage — THE SACRED TIMELINE

The engine owns a primary evolving timeline and alternate temporal worlds that
inherit real history, diverge under independent state evolution, retain causal
identity, exchange harmonic influence, and may later synchronize or converge.
It is neither a neural-network layer nor an event scheduler: queues, tensors,
causal graphs, recursive closures, and harmonic fields are mechanisms inside a
branching-state simulation ontology.

IO surface:
    No import-time execution, network access, or global logging configuration.
    Optional snapshots use atomic JSON files. NumPy is the sole non-stdlib
    dependency and is fundamental to the engine's tensor and harmonic algebra.

Modified: 2026-08-14
Modified by: OpenAI Codex, in collaboration with Daeron
Justification: frontier reconstruction of the standalone Timeline Engine around
    explicit temporal identity, branch-local worlds, causal inheritance,
    deterministic dynamics, harmonic coupling, divergence/convergence geometry,
    recursive closure, and complete recoverable state.
Provenance: direct evolution of the supplied timeline_engine-1.py artifact.
Files: timeline_engine-1.py
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import math
import os
import threading
import time
import uuid
from collections import defaultdict, deque
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Final, TypeAlias

import heapq
import numpy as np
from numpy.typing import NDArray


logger = logging.getLogger("TimelineEngine")
logger.addHandler(logging.NullHandler())

PHI: Final = (1.0 + math.sqrt(5.0)) / 2.0
TAU: Final = math.tau
SACRED_RATIO: Final = PHI / TAU
PSALTER_SCALE: Final = 1.0
STATE_SCHEMA: Final = "loom-cosmos-timeline-engine"
STATE_VERSION: Final = 3
DEFAULT_HARMONICS: Final = 8
EPSILON: Final = 1e-12

FloatArray: TypeAlias = NDArray[np.float64]
JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
Observer: TypeAlias = Callable[["TemporalEvent", int], None]


class TimelineError(RuntimeError):
    """Base failure for timeline-world operations."""


class TemporalConstraintError(TimelineError, ValueError):
    """Raised when a temporal invariant would be violated."""

    def __init__(
        self,
        message: str = "Temporal constraint violation detected",
        constraint_type: str | None = None,
        violation_time: float | None = None,
        affected_events: Sequence[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.constraint_type = constraint_type
        self.violation_time = violation_time
        self.affected_events = tuple(affected_events or ())

    def __str__(self) -> str:
        """Render structured constraint context."""
        details = []
        if self.constraint_type:
            details.append(f"constraint={self.constraint_type}")
        if self.violation_time is not None:
            details.append(f"time={self.violation_time:.12g}")
        if self.affected_events:
            details.append(f"events={len(self.affected_events)}")
        return self.message if not details else f"{self.message} ({', '.join(details)})"


class TimelineParadoxError(TimelineError):
    """Raised when causal requirements cannot be reconciled automatically."""

    def __init__(
        self,
        message: str = "Temporal paradox detected in timeline",
        severity: float | None = None,
        affected_branches: Sequence[int] | None = None,
        timeline_point: float | None = None,
    ) -> None:
        super().__init__(message)
        self.severity = severity
        self.affected_branches = tuple(affected_branches or ())
        self.timeline_point = timeline_point


class QuantumDecoherenceError(TimelineError):
    """Raised when a branch state loses a usable normalized representation."""


class RealityFragmentationError(TimelineError):
    """Raised when branch relationships become globally inconsistent."""


class SerializationError(TimelineError):
    """Raised when a snapshot cannot preserve timeline identity."""


class BreathPhase(Enum):
    """Seven-stage recursive breath governing temporal phase transitions."""

    INHALE = auto()
    PAUSE_RISING = auto()
    HOLD = auto()
    PAUSE_FALLING = auto()
    EXHALE = auto()
    REST = auto()
    DREAM = auto()

    # Compatibility aliases from the later four-phase public surface.
    HOLD_IN = HOLD
    HOLD_OUT = REST

    def next_phase(self) -> BreathPhase:
        """Return the next distinct phase in the seven-stage cycle."""
        phases = list(BreathPhase)
        return phases[(phases.index(self) + 1) % len(phases)]

    @property
    def duration_weight(self) -> float:
        """Return this phase's share of a non-uniform breath cycle."""
        return {
            BreathPhase.INHALE: 1.0,
            BreathPhase.PAUSE_RISING: 0.3,
            BreathPhase.HOLD: 1.0,
            BreathPhase.PAUSE_FALLING: 0.3,
            BreathPhase.EXHALE: 1.2,
            BreathPhase.REST: 0.8,
            BreathPhase.DREAM: 1.5,
        }[self]

    @property
    def description(self) -> str:
        """Return the operational meaning of this temporal phase."""
        return {
            BreathPhase.INHALE: "possibility intake and state acquisition",
            BreathPhase.PAUSE_RISING: "pre-integration reflection",
            BreathPhase.HOLD: "fixed-point processing and coherence retention",
            BreathPhase.PAUSE_FALLING: "pre-expression reflection",
            BreathPhase.EXHALE: "state expression and causal realization",
            BreathPhase.REST: "memory integration and relaxation",
            BreathPhase.DREAM: "cross-scale recursive recombination",
        }[self]

    @classmethod
    def from_cycle_position(cls, position: float) -> BreathPhase:
        """Map a normalized cycle position onto weighted phase intervals."""
        value = _finite(position, "position") % 1.0
        phases = list(cls)
        total = math.fsum(phase.duration_weight for phase in phases)
        cursor = 0.0
        for phase in phases:
            cursor += phase.duration_weight / total
            if value < cursor:
                return phase
        return phases[-1]


class BranchStatus(Enum):
    """Lifecycle status of a temporal world."""

    ACTIVE = auto()
    FROZEN = auto()
    DORMANT = auto()
    MERGED = auto()
    FRAGMENTED = auto()


class ParadoxKind(Enum):
    """Causal failure classes recognized by the engine."""

    ORPHAN_PARENT = "orphan_parent"
    REVERSE_CAUSALITY = "reverse_causality"
    CAUSAL_LOOP = "causal_loop"
    IDENTITY_COLLISION = "identity_collision"
    STATE_INVALID = "state_invalid"


def _finite(value: float, name: str) -> float:
    """Return a finite float or raise a temporal constraint error."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TemporalConstraintError(f"{name} must be numeric", "numeric") from exc
    if not math.isfinite(result):
        raise TemporalConstraintError(f"{name} must be finite", "numeric")
    return result


def _bounded(value: float, name: str, low: float, high: float) -> float:
    """Validate a finite scalar within inclusive bounds."""
    result = _finite(value, name)
    if not low <= result <= high:
        raise TemporalConstraintError(
            f"{name} must be in [{low}, {high}]", "bounds",
        )
    return result


def _vector(
    value: Sequence[float] | FloatArray | None,
    size: int,
    name: str,
    *,
    default: float = 0.0,
) -> FloatArray:
    """Create an owned, finite, one-dimensional float vector."""
    if value is None:
        return np.full(size, default, dtype=np.float64)
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 1:
        raise TemporalConstraintError(f"{name} must be one-dimensional", "shape")
    if array.size != size:
        if array.size > size:
            array = array[:size]
        else:
            array = np.pad(array, (0, size - array.size))
    if not np.all(np.isfinite(array)):
        raise TemporalConstraintError(f"{name} contains non-finite values", "numeric")
    return np.array(array, dtype=np.float64, copy=True)


def _normalize_distribution(value: FloatArray) -> FloatArray:
    """Map an arbitrary finite vector to a stable probability simplex."""
    shifted = np.asarray(value, dtype=np.float64)
    if shifted.size == 0:
        raise QuantumDecoherenceError("empty state vector")
    minimum = float(np.min(shifted))
    if minimum < 0.0:
        shifted = shifted - minimum
    total = float(np.sum(shifted))
    if total <= EPSILON:
        return np.full(shifted.size, 1.0 / shifted.size, dtype=np.float64)
    return shifted / total


def _phase_distance(left: float, right: float) -> float:
    """Return minimum angular distance in radians."""
    return abs((left - right + math.pi) % TAU - math.pi)


def _stable_digest(value: object) -> str:
    """Return a deterministic digest for dynamic but serializable values."""
    encoded = json.dumps(
        _json_safe(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _json_safe(value: object, *, depth: int = 0) -> JsonValue:
    """Convert dynamic state into deterministic JSON without identity aliases."""
    if depth > 64:
        raise SerializationError("snapshot nesting exceeds 64 levels")
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SerializationError("non-finite float cannot be serialized")
        return value
    if isinstance(value, np.generic):
        return _json_safe(value.item(), depth=depth + 1)
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist(), depth=depth + 1)
    if isinstance(value, Enum):
        return {"$enum": f"{type(value).__name__}.{value.name}"}
    if isinstance(value, Path):
        return {"$path": str(value)}
    if isinstance(value, TemporalEvent):
        return {"$event": value.event_id}
    if isinstance(value, Mapping):
        if all(isinstance(key, str) for key in value):
            return {
                str(key): _json_safe(item, depth=depth + 1)
                for key, item in sorted(value.items())
            }
        pairs = [
            [_json_safe(key, depth=depth + 1), _json_safe(item, depth=depth + 1)]
            for key, item in value.items()
        ]
        pairs.sort(key=lambda pair: json.dumps(pair[0], sort_keys=True))
        return {"$mapping": pairs}
    if isinstance(value, (set, frozenset)):
        items = [_json_safe(item, depth=depth + 1) for item in value]
        items.sort(key=lambda item: json.dumps(item, sort_keys=True))
        return items
    if isinstance(value, (list, tuple, deque)):
        return [_json_safe(item, depth=depth + 1) for item in value]
    return {"$type": type(value).__qualname__, "$repr": repr(value)}


@dataclass(slots=True)
class TimelineMetrics:
    """Bounded histories and cumulative measures of temporal-world evolution."""

    sampling_rate: int = 256
    coherence_history: deque[float] = field(init=False)
    divergence_history: deque[float] = field(init=False)
    paradox_count: int = 0
    branch_count: int = 0
    merge_count: int = 0
    events_processed: int = 0
    recursion_depth: int = 0
    runtime_ns: int = 0
    last_update: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        """Allocate bounded metric histories."""
        if not isinstance(self.sampling_rate, int) or self.sampling_rate < 2:
            raise TemporalConstraintError("sampling_rate must be at least 2", "metrics")
        self.coherence_history = deque(maxlen=self.sampling_rate)
        self.divergence_history = deque(maxlen=self.sampling_rate)

    def update(self, timeline_state: Mapping[str, object]) -> dict[str, object]:
        """Accumulate one state sample and return the current summary."""
        self.coherence_history.append(
            _bounded(float(timeline_state.get("coherence", 1.0)), "coherence", 0.0, 1.0)
        )
        self.divergence_history.append(
            _bounded(float(timeline_state.get("divergence", 0.0)), "divergence", 0.0, 1.0)
        )
        self.paradox_count += int(timeline_state.get("new_paradoxes", 0))
        self.branch_count += int(timeline_state.get("new_branches", 0))
        self.merge_count += int(timeline_state.get("new_merges", 0))
        self.events_processed += int(timeline_state.get("events_processed", 0))
        self.recursion_depth = max(
            self.recursion_depth, int(timeline_state.get("recursion_depth", 0)),
        )
        self.runtime_ns = int(timeline_state.get("runtime_ns", self.runtime_ns))
        self.last_update = time.time()
        return self.get_summary()

    def get_summary(self) -> dict[str, object]:
        """Return stable aggregate metrics."""
        return {
            "avg_coherence": math.fsum(self.coherence_history) / len(self.coherence_history)
            if self.coherence_history else 1.0,
            "avg_divergence": math.fsum(self.divergence_history) / len(self.divergence_history)
            if self.divergence_history else 0.0,
            "paradox_count": self.paradox_count,
            "branch_count": self.branch_count,
            "merge_count": self.merge_count,
            "events_processed": self.events_processed,
            "max_recursion_depth": self.recursion_depth,
            "runtime_ns": self.runtime_ns,
            "last_update": self.last_update,
        }

    def measure_divergence(self) -> float:
        """Return the recent mean branch divergence."""
        return math.fsum(self.divergence_history) / len(self.divergence_history) \
            if self.divergence_history else 0.0

    def reset(self) -> None:
        """Clear bounded history and cumulative counters."""
        self.coherence_history.clear()
        self.divergence_history.clear()
        self.paradox_count = self.branch_count = self.merge_count = 0
        self.events_processed = self.recursion_depth = self.runtime_ns = 0
        self.last_update = time.time()


@dataclass(slots=True)
class CausalViolation:
    """Structured paradox evidence retained by a branch."""

    kind: ParadoxKind
    event_id: str
    parent_id: str | None
    branch_id: str
    time: float
    severity: float
    detail: str

    def to_dict(self) -> dict[str, object]:
        """Serialize violation evidence."""
        return {
            "kind": self.kind.value, "event_id": self.event_id,
            "parent_id": self.parent_id, "branch_id": self.branch_id,
            "time": self.time, "severity": self.severity, "detail": self.detail,
        }


@dataclass(slots=True)
class MergeReport:
    """Detailed result of a non-destructive timeline convergence operation."""

    source: int
    target: int
    strategy: str
    imported_events: int
    conflicts: int
    convergence_before: float
    convergence_after: float
    merge_event_id: str | None

    @property
    def success(self) -> bool:
        """Return whether a convergence event was committed."""
        return self.merge_event_id is not None


@dataclass(slots=True)
class TemporalEvent:
    """Stable causal event inhabiting one or more timeline histories.

    The first fields preserve the historical constructor surface. Event identity
    is explicit and survives serialization; Python object addresses never enter
    causal semantics.
    """

    timestamp: float
    event_type: str
    quantum_state: FloatArray | Sequence[float] | None = None
    ethical_vectors: FloatArray | Sequence[float] | None = None
    causal_parents: list[TemporalEvent | str] = field(default_factory=list)
    recursion_depth: int = 0
    metadata: dict[str, object] = field(default_factory=dict)
    entropy_consumed: float = 0.0
    paradox_resolved: bool = False
    phase: float = 0.0
    amplitude: float = 0.0
    is_inhale: bool = False
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    priority: int = 0
    origin_branch_id: str | None = None
    sequence: int = 0

    def __post_init__(self) -> None:
        """Normalize event identity, arrays, parents, and scalar invariants."""
        self.timestamp = _finite(self.timestamp, "timestamp")
        if not isinstance(self.event_type, str) or not self.event_type:
            raise TemporalConstraintError("event_type must be non-empty", "event")
        self.event_id = str(self.event_id or uuid.uuid4().hex)
        self.quantum_state = _vector(
            self.quantum_state, len(self.quantum_state) if self.quantum_state is not None else 10,
            "quantum_state", default=1.0,
        )
        self.ethical_vectors = _vector(
            self.ethical_vectors,
            len(self.ethical_vectors) if self.ethical_vectors is not None else 3,
            "ethical_vectors",
        )
        if not isinstance(self.recursion_depth, int) or self.recursion_depth < 0:
            raise TemporalConstraintError("recursion_depth must be non-negative", "recursion")
        self.entropy_consumed = _finite(self.entropy_consumed, "entropy_consumed")
        self.phase = _finite(self.phase, "phase") % TAU
        self.amplitude = _finite(self.amplitude, "amplitude")
        if not isinstance(self.priority, int):
            raise TemporalConstraintError("priority must be an integer", "event")
        if not isinstance(self.sequence, int) or self.sequence < 0:
            raise TemporalConstraintError("sequence must be non-negative", "event")
        self.metadata = dict(self.metadata)
        self.causal_parents = list(self.causal_parents)

    @property
    def parent_ids(self) -> tuple[str, ...]:
        """Return de-duplicated stable parent identities in declared order."""
        return tuple(dict.fromkeys(
            parent.event_id if isinstance(parent, TemporalEvent) else str(parent)
            for parent in self.causal_parents
        ))

    @property
    def heap_key(self) -> tuple[float, int, int, str]:
        """Return a total deterministic ordering key for event horizons."""
        return (self.timestamp, -self.priority, self.sequence, self.event_id)

    def __lt__(self, other: TemporalEvent) -> bool:
        """Order events deterministically for priority queues."""
        if not isinstance(other, TemporalEvent):
            return NotImplemented
        return self.heap_key < other.heap_key

    def clone(
        self, *, preserve_id: bool = True, timestamp: float | None = None,
        origin_branch_id: str | None = None,
    ) -> TemporalEvent:
        """Return an isolated event copy suitable for another temporal world."""
        return TemporalEvent(
            timestamp=self.timestamp if timestamp is None else timestamp,
            event_type=self.event_type,
            quantum_state=np.array(self.quantum_state, copy=True),
            ethical_vectors=np.array(self.ethical_vectors, copy=True),
            causal_parents=list(self.parent_ids),
            recursion_depth=self.recursion_depth,
            metadata=copy.deepcopy(self.metadata),
            entropy_consumed=self.entropy_consumed,
            paradox_resolved=self.paradox_resolved,
            phase=self.phase,
            amplitude=self.amplitude,
            is_inhale=self.is_inhale,
            event_id=self.event_id if preserve_id else uuid.uuid4().hex,
            priority=self.priority,
            origin_branch_id=origin_branch_id or self.origin_branch_id,
            sequence=self.sequence,
        )

    def semantic_fingerprint(self) -> str:
        """Hash event meaning while excluding branch-local scheduling identity."""
        return _stable_digest({
            "type": self.event_type,
            "state": np.round(self.quantum_state, 12).tolist(),
            "ethical": np.round(self.ethical_vectors, 12).tolist(),
            "parents": self.parent_ids,
            "metadata": self.metadata,
        })

    def to_dict(self) -> dict[str, object]:
        """Serialize complete event state."""
        return {
            "event_id": self.event_id, "timestamp": self.timestamp,
            "event_type": self.event_type,
            "quantum_state": self.quantum_state.tolist(),
            "ethical_vectors": self.ethical_vectors.tolist(),
            "causal_parents": list(self.parent_ids),
            "recursion_depth": self.recursion_depth,
            "metadata": _json_safe(self.metadata),
            "entropy_consumed": self.entropy_consumed,
            "paradox_resolved": self.paradox_resolved,
            "phase": self.phase, "amplitude": self.amplitude,
            "is_inhale": self.is_inhale, "priority": self.priority,
            "origin_branch_id": self.origin_branch_id, "sequence": self.sequence,
        }

    @classmethod
    def from_dict(cls, event_dict: Mapping[str, object]) -> TemporalEvent:
        """Validate and reconstruct an event without mutating caller data."""
        data = dict(event_dict)
        if "event_type" not in data and "type" in data:
            data["event_type"] = data.pop("type")
        if "timestamp" not in data or "event_type" not in data:
            raise TemporalConstraintError(
                "event requires timestamp and event_type", "event_schema",
            )
        allowed = {
            "timestamp", "event_type", "quantum_state", "ethical_vectors",
            "causal_parents", "recursion_depth", "metadata", "entropy_consumed",
            "paradox_resolved", "phase", "amplitude", "is_inhale", "event_id",
            "priority", "origin_branch_id", "sequence",
        }
        unknown = set(data) - allowed
        if unknown:
            raise TemporalConstraintError(
                f"unknown event fields: {sorted(unknown)}", "event_schema",
            )
        return cls(**data)  # type: ignore[arg-type]


@dataclass
class TemporalBranch:
    """A temporal world with inherited history and independent evolution."""

    id: str
    parent_id: str | None = None
    branch_point: float = 0.0
    attributes: dict[str, object] = field(default_factory=dict)
    creation_time: float = field(default_factory=time.time)
    child_branches: list[str] = field(default_factory=list)
    events: list[TemporalEvent] = field(default_factory=list)
    pending: list[TemporalEvent] = field(default_factory=list)
    active: bool = True
    coherence: float = 1.0
    local_time: float = 0.0
    tick: int = 0
    generation: int = 0
    status: BranchStatus = BranchStatus.ACTIVE
    harmonic_phase: float = 0.0
    natural_frequency: float = 1.0
    freeze_until: float | None = None
    divergence: float = 0.0
    state_vector: FloatArray = field(default_factory=lambda: np.zeros(4, dtype=np.float64))
    ethical_state: FloatArray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    harmonic_amplitudes: FloatArray = field(
        default_factory=lambda: np.ones(DEFAULT_HARMONICS, dtype=np.float64)
    )
    harmonic_phases: FloatArray = field(
        default_factory=lambda: np.zeros(DEFAULT_HARMONICS, dtype=np.float64)
    )
    causal_parents: dict[str, set[str]] = field(default_factory=dict)
    causal_children: dict[str, set[str]] = field(default_factory=dict)
    event_index: dict[str, TemporalEvent] = field(default_factory=dict)
    pending_ids: set[str] = field(default_factory=set)
    paradoxes: deque[CausalViolation] = field(default_factory=lambda: deque(maxlen=128))
    merge_records: list[dict[str, object]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize branch clocks, arrays, heaps, and causal indexes."""
        self.id = str(self.id)
        if not self.id:
            raise TemporalConstraintError("branch id must be non-empty", "branch")
        self.branch_point = _finite(self.branch_point, "branch_point")
        self.local_time = _finite(self.local_time, "local_time")
        self.coherence = _bounded(self.coherence, "coherence", 0.0, 1.0)
        self.divergence = _bounded(self.divergence, "divergence", 0.0, 1.0)
        self.natural_frequency = _finite(self.natural_frequency, "natural_frequency")
        if self.natural_frequency <= 0.0:
            raise TemporalConstraintError("natural_frequency must be positive", "frequency")
        self.state_vector = np.asarray(self.state_vector, dtype=np.float64).copy()
        self.ethical_state = np.asarray(self.ethical_state, dtype=np.float64).copy()
        self.harmonic_amplitudes = np.asarray(
            self.harmonic_amplitudes, dtype=np.float64,
        ).copy()
        self.harmonic_phases = np.asarray(self.harmonic_phases, dtype=np.float64).copy()
        if self.harmonic_amplitudes.shape != self.harmonic_phases.shape:
            raise TemporalConstraintError("harmonic arrays must share shape", "shape")
        if not all(np.all(np.isfinite(array)) for array in (
            self.state_vector, self.ethical_state,
            self.harmonic_amplitudes, self.harmonic_phases,
        )):
            raise TemporalConstraintError("branch arrays contain non-finite values", "numeric")
        self.events = list(self.events)
        self.pending = list(self.pending)
        heapq.heapify(self.pending)
        self.pending_ids = {event.event_id for event in self.pending}
        if len(self.pending_ids) != len(self.pending):
            raise TemporalConstraintError("duplicate pending event identity", "identity")
        self.rebuild_causal_indexes()

    def add_child_branch(self, branch_id: str) -> None:
        """Register a direct descendant exactly once."""
        identifier = str(branch_id)
        if identifier not in self.child_branches:
            self.child_branches.append(identifier)

    def add_event(self, event: TemporalEvent) -> None:
        """Commit an event into ordered history and causal indexes."""
        existing = self.event_index.get(event.event_id)
        if existing is not None:
            if existing.semantic_fingerprint() != event.semantic_fingerprint():
                raise TemporalConstraintError(
                    f"event identity collision: {event.event_id}", "identity",
                )
            return
        self.events.append(event)
        self.event_index[event.event_id] = event
        self.causal_parents[event.event_id] = set(event.parent_ids)
        self.causal_children.setdefault(event.event_id, set())
        for parent_id in event.parent_ids:
            self.causal_children.setdefault(parent_id, set()).add(event.event_id)

    def add_pending(self, event: TemporalEvent) -> None:
        """Place an event on this world's deterministic horizon."""
        if event.event_id in self.pending_ids or event.event_id in self.event_index:
            raise TemporalConstraintError(
                f"duplicate event id {event.event_id}", "identity_collision",
            )
        heapq.heappush(self.pending, event)
        self.pending_ids.add(event.event_id)

    def get_events_in_range(self, start_time: float, end_time: float) -> list[TemporalEvent]:
        """Return committed events within an inclusive temporal interval."""
        start = _finite(start_time, "start_time")
        end = _finite(end_time, "end_time")
        if start > end:
            raise TemporalConstraintError("start_time exceeds end_time", "interval")
        return [event for event in self.events if start <= event.timestamp <= end]

    def set_active(self, active: bool) -> None:
        """Set whether this world participates in ordinary evolution."""
        self.active = bool(active)
        if self.status not in {BranchStatus.MERGED, BranchStatus.FRAGMENTED}:
            self.status = BranchStatus.ACTIVE if self.active else BranchStatus.DORMANT

    def update_coherence(self, new_coherence: float) -> None:
        """Set bounded branch coherence."""
        self.coherence = _bounded(new_coherence, "coherence", 0.0, 1.0)

    def rebuild_causal_indexes(self) -> None:
        """Reconstruct causal source-of-truth indexes from committed history."""
        self.event_index = {}
        self.causal_parents = {}
        self.causal_children = defaultdict(set)
        for event in self.events:
            if event.event_id in self.event_index:
                raise TemporalConstraintError(
                    f"duplicate event id {event.event_id}", "identity",
                )
            self.event_index[event.event_id] = event
            parents = set(event.parent_ids)
            self.causal_parents[event.event_id] = parents
            self.causal_children.setdefault(event.event_id, set())
            for parent_id in parents:
                self.causal_children[parent_id].add(event.event_id)

    @property
    def latest_event(self) -> TemporalEvent | None:
        """Return the latest committed event."""
        return self.events[-1] if self.events else None

    def to_dict(self) -> dict[str, object]:
        """Serialize the complete temporal world."""
        return {
            "id": self.id, "parent_id": self.parent_id,
            "branch_point": self.branch_point, "attributes": _json_safe(self.attributes),
            "creation_time": self.creation_time,
            "child_branches": list(self.child_branches),
            "events": [event.to_dict() for event in self.events],
            "pending": [event.to_dict() for event in sorted(self.pending)],
            "active": self.active, "coherence": self.coherence,
            "local_time": self.local_time, "tick": self.tick,
            "generation": self.generation, "status": self.status.name,
            "harmonic_phase": self.harmonic_phase,
            "natural_frequency": self.natural_frequency,
            "freeze_until": self.freeze_until, "divergence": self.divergence,
            "state_vector": self.state_vector.tolist(),
            "ethical_state": self.ethical_state.tolist(),
            "harmonic_amplitudes": self.harmonic_amplitudes.tolist(),
            "harmonic_phases": self.harmonic_phases.tolist(),
            "paradoxes": [violation.to_dict() for violation in self.paradoxes],
            "merge_records": _json_safe(self.merge_records),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> TemporalBranch:
        """Restore a branch and rebuild its causal indexes."""
        try:
            branch = cls(
                id=str(data["id"]),
                parent_id=None if data.get("parent_id") is None else str(data["parent_id"]),
                branch_point=float(data.get("branch_point", 0.0)),
                attributes=dict(data.get("attributes", {})),
                creation_time=float(data.get("creation_time", time.time())),
                child_branches=[str(value) for value in data.get("child_branches", [])],
                events=[TemporalEvent.from_dict(item) for item in data.get("events", [])],
                pending=[TemporalEvent.from_dict(item) for item in data.get("pending", [])],
                active=bool(data.get("active", True)),
                coherence=float(data.get("coherence", 1.0)),
                local_time=float(data.get("local_time", 0.0)),
                tick=int(data.get("tick", 0)),
                generation=int(data.get("generation", 0)),
                status=BranchStatus[str(data.get("status", "ACTIVE"))],
                harmonic_phase=float(data.get("harmonic_phase", 0.0)),
                natural_frequency=float(data.get("natural_frequency", 1.0)),
                freeze_until=None if data.get("freeze_until") is None else float(data["freeze_until"]),
                divergence=float(data.get("divergence", 0.0)),
                state_vector=np.asarray(data.get("state_vector", [0.0] * 4), dtype=np.float64),
                ethical_state=np.asarray(data.get("ethical_state", [0.0] * 3), dtype=np.float64),
                harmonic_amplitudes=np.asarray(
                    data.get("harmonic_amplitudes", [1.0] * DEFAULT_HARMONICS),
                    dtype=np.float64,
                ),
                harmonic_phases=np.asarray(
                    data.get("harmonic_phases", [0.0] * DEFAULT_HARMONICS),
                    dtype=np.float64,
                ),
                merge_records=list(data.get("merge_records", [])),
            )
            for raw in data.get("paradoxes", []):
                branch.paradoxes.append(CausalViolation(
                    kind=ParadoxKind(str(raw["kind"])),
                    event_id=str(raw["event_id"]),
                    parent_id=None if raw.get("parent_id") is None else str(raw["parent_id"]),
                    branch_id=str(raw["branch_id"]),
                    time=float(raw["time"]), severity=float(raw["severity"]),
                    detail=str(raw["detail"]),
                ))
            return branch
        except (KeyError, TypeError, ValueError, TemporalConstraintError) as exc:
            raise SerializationError("invalid TemporalBranch state") from exc


__all__: list[str]


class TimelineEngine:
    """Branching temporal-world simulator with causal and harmonic dynamics."""

    def __init__(
        self,
        breath_frequency: float = 1.0,
        max_recursion_depth: int = 8,
        num_dimensions: int = 4,
        ethical_dimensions: int = 3,
        parallel_timelines: int = 1,
        auto_stabilize: bool = True,
        *,
        seed: int = 0,
        harmonic_modes: int = DEFAULT_HARMONICS,
        coupling_strength: float = 0.15,
    ) -> None:
        """Create a primary timeline and optional sibling temporal worlds.

        Args:
            breath_frequency: Fundamental world oscillation in hertz.
            max_recursion_depth: Maximum nested temporal closure depth.
            num_dimensions: State/tensor dimensions.
            ethical_dimensions: Dimensions in the ethical state field.
            parallel_timelines: Initial number of temporal worlds.
            auto_stabilize: Whether low-coherence worlds self-stabilize.
            seed: Deterministic stochastic field seed.
            harmonic_modes: Number of coupled harmonic modes per world.
            coupling_strength: Kuramoto-style cross-world phase coupling.
        """
        self._validate_initialization_parameters(
            breath_frequency, max_recursion_depth, num_dimensions,
            ethical_dimensions, parallel_timelines, auto_stabilize,
            harmonic_modes, coupling_strength,
        )
        self.breath_frequency = float(breath_frequency)
        self.temporal_resolution = 1.0 / (2.0 * self.breath_frequency)
        self.max_recursion_depth = max_recursion_depth
        self.num_dimensions = num_dimensions
        self.ethical_dimensions = ethical_dimensions
        self.harmonic_modes = harmonic_modes
        self.coupling_strength = float(coupling_strength)
        self.auto_stabilize = auto_stabilize
        self.stability_threshold = 0.3
        self.seed = int(seed)
        self.master_tick = 0
        self.phase = 0.0
        self.active_timeline = 0
        self._sequence = 0
        self._lock = threading.RLock()
        self.sync_lock = self._lock
        self._closed = False
        self._observers: list[Observer | str] = []
        self.observers = self._observers
        self._event_cache: dict[tuple[str, int, str], TemporalEvent] = {}
        self.event_cache = self._event_cache
        self.cache_hit_rate = 0.0
        self.cache_miss_count = 0
        self._last_merge_report: MergeReport | None = None
        self.metrics_tracker = TimelineMetrics()
        self.metrics: dict[str, int] = {
            "paradoxes_resolved": 0,
            "events_processed": 0,
            "cache_hits": 0,
            "cache_miss_count": 0,
            "timeline_branches": 0,
            "timeline_merges": 0,
            "quantum_collapses": 0,
            "ethical_corrections": 0,
            "runtime_ns": 0,
        }

        primary = self._new_branch(
            identifier="timeline-0", parent_id=None, branch_point=0.0,
            generation=0, natural_frequency=self.breath_frequency,
        )
        self.branches: list[TemporalBranch] = [primary]
        self._branch_by_id: dict[str, int] = {primary.id: 0}
        for index in range(1, parallel_timelines):
            sibling = self._new_branch(
                identifier=f"timeline-{index}", parent_id=primary.id,
                branch_point=0.0, generation=1,
                natural_frequency=self.breath_frequency * (1.0 + 0.005 * index),
            )
            self.branches.append(sibling)
            self._branch_by_id[sibling.id] = index
            primary.add_child_branch(sibling.id)

        self.entanglement_matrix = np.eye(parallel_timelines, dtype=np.float64)
        if parallel_timelines > 1:
            self.entanglement_matrix += (
                np.ones((parallel_timelines, parallel_timelines), dtype=np.float64)
                - np.eye(parallel_timelines, dtype=np.float64)
            ) * 0.25
        self._refresh_compatibility_views()

    def _validate_initialization_parameters(
        self,
        breath_frequency: float,
        max_recursion_depth: int,
        num_dimensions: int,
        ethical_dimensions: int,
        parallel_timelines: int,
        auto_stabilize: bool,
        harmonic_modes: int = DEFAULT_HARMONICS,
        coupling_strength: float = 0.15,
    ) -> None:
        """Validate simulation geometry without imposing arbitrary small ceilings."""
        frequency = _finite(breath_frequency, "breath_frequency")
        if frequency <= 0.0:
            raise TemporalConstraintError(
                "breath_frequency must be positive", "frequency_bounds",
            )
        for name, value, minimum in (
            ("max_recursion_depth", max_recursion_depth, 1),
            ("num_dimensions", num_dimensions, 2),
            ("ethical_dimensions", ethical_dimensions, 1),
            ("parallel_timelines", parallel_timelines, 1),
            ("harmonic_modes", harmonic_modes, 1),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
                raise TemporalConstraintError(
                    f"{name} must be an integer >= {minimum}", "configuration",
                )
        if not isinstance(auto_stabilize, bool):
            raise TemporalConstraintError("auto_stabilize must be bool", "configuration")
        _bounded(coupling_strength, "coupling_strength", 0.0, 10.0)
        estimated = parallel_timelines * (
            (num_dimensions + ethical_dimensions + harmonic_modes * 2) * 8
            + parallel_timelines * 8
        )
        if estimated > 4 * 1024**3:
            raise TemporalConstraintError(
                "initial tensor geometry exceeds 4 GiB", "resource_geometry",
            )

    def _new_branch(
        self,
        *,
        identifier: str,
        parent_id: str | None,
        branch_point: float,
        generation: int,
        natural_frequency: float,
    ) -> TemporalBranch:
        """Construct an empty temporal world with engine-compatible geometry."""
        mode_numbers = np.arange(1, self.harmonic_modes + 1, dtype=np.float64)
        return TemporalBranch(
            id=identifier,
            parent_id=parent_id,
            branch_point=branch_point,
            local_time=branch_point,
            generation=generation,
            natural_frequency=natural_frequency,
            state_vector=np.zeros(self.num_dimensions, dtype=np.float64),
            ethical_state=np.zeros(self.ethical_dimensions, dtype=np.float64),
            harmonic_amplitudes=1.0 / np.sqrt(mode_numbers),
            harmonic_phases=np.zeros(self.harmonic_modes, dtype=np.float64),
        )

    def _refresh_compatibility_views(self) -> None:
        """Expose historical array surfaces as live branch-owned structures."""
        self.event_horizons = [branch.pending for branch in self.branches]
        self.timestreams = [branch.causal_children for branch in self.branches]
        self.recursion_stacks = [
            deque(maxlen=self.max_recursion_depth) for _ in self.branches
        ] if not hasattr(self, "recursion_stacks") else self.recursion_stacks
        while len(self.recursion_stacks) < len(self.branches):
            self.recursion_stacks.append(deque(maxlen=self.max_recursion_depth))
        self.paradox_buffers = [branch.paradoxes for branch in self.branches]
        self.timeline_coherence = np.asarray(
            [branch.coherence for branch in self.branches], dtype=np.float64,
        )
        self.breath_phase_array = np.asarray(
            [branch.harmonic_phase for branch in self.branches], dtype=np.float64,
        )
        self.ethical_tensors = np.stack(
            [branch.ethical_state for branch in self.branches], axis=0,
        )

    def _sync_arrays_to_branches(self) -> None:
        """Accept compatible direct array edits back into branch state."""
        for index, branch in enumerate(self.branches):
            if index < self.timeline_coherence.size:
                branch.coherence = _bounded(
                    float(self.timeline_coherence[index]), "coherence", 0.0, 1.0,
                )
            if index < self.breath_phase_array.size:
                branch.harmonic_phase = float(self.breath_phase_array[index]) % TAU
            if index < len(self.ethical_tensors):
                branch.ethical_state = _vector(
                    self.ethical_tensors[index], self.ethical_dimensions,
                    "ethical_state",
                )

    def _branch(self, timeline_idx: int | None = None) -> TemporalBranch:
        """Resolve and validate a timeline index."""
        index = self.active_timeline if timeline_idx is None else timeline_idx
        if not isinstance(index, int) or isinstance(index, bool):
            raise TemporalConstraintError("timeline index must be integer", "timeline_bounds")
        if not 0 <= index < len(self.branches):
            raise TemporalConstraintError(
                f"timeline {index} out of bounds", "timeline_bounds",
            )
        return self.branches[index]

    def _branch_index(self, branch_id: str) -> int:
        """Resolve a stable branch identifier to its current index."""
        try:
            return self._branch_by_id[branch_id]
        except KeyError as exc:
            raise TemporalConstraintError(
                f"unknown branch id {branch_id!r}", "timeline_bounds",
            ) from exc

    def _next_sequence(self) -> int:
        """Return a strictly increasing engine-local event sequence."""
        self._sequence += 1
        return self._sequence

    def get_absolute_time(self) -> float:
        """Return the active world's real local simulation time."""
        return self._branch().local_time

    def schedule_event(
        self,
        event: Mapping[str, object] | TemporalEvent,
        timeline_idx: int | None = None,
        recursion_depth: int = 0,
    ) -> TemporalEvent:
        """Schedule an isolated event into one temporal world's future horizon."""
        branch = self._branch(timeline_idx)
        if not isinstance(recursion_depth, int) or recursion_depth < 0:
            raise TemporalConstraintError(
                "recursion_depth must be non-negative", "recursion_bounds",
            )
        if recursion_depth > self.max_recursion_depth:
            raise TemporalConstraintError(
                f"recursion depth {recursion_depth} exceeds {self.max_recursion_depth}",
                "recursion_bounds",
            )
        if isinstance(event, Mapping):
            event_obj = TemporalEvent.from_dict(event)
        elif isinstance(event, TemporalEvent):
            event_obj = event.clone()
        else:
            raise TemporalConstraintError("event must be mapping or TemporalEvent", "event_schema")
        with self._lock:
            if (
                event_obj.event_id in branch.event_index
                or event_obj.event_id in branch.pending_ids
            ):
                raise TemporalConstraintError(
                    f"event id {event_obj.event_id} already exists in branch",
                    "identity_collision", event_obj.timestamp, [event_obj.event_id],
                )
            event_obj.recursion_depth = recursion_depth
            event_obj.origin_branch_id = event_obj.origin_branch_id or branch.id
            event_obj.sequence = self._next_sequence()
            self._validate_event_metadata(event_obj)
            branch.add_pending(event_obj)
            self._refresh_compatibility_views()
            return event_obj

    def temporal_injection(
        self, event: TemporalEvent, timeline_idx: int | None = None,
    ) -> None:
        """Inject an event into a branch through the validated horizon path."""
        self.schedule_event(event, timeline_idx, event.recursion_depth)

    def process_tick(
        self,
        inputs: Mapping[str, object],
        rcf_operator: Callable[[Mapping[str, object]], Mapping[str, object]],
        timeline_idx: int | None = None,
    ) -> dict[str, object]:
        """Advance one temporal world by one quantum and realize all due events."""
        if not isinstance(inputs, Mapping):
            raise TemporalConstraintError("inputs must be a mapping", "input_schema")
        if not callable(rcf_operator):
            raise TemporalConstraintError("rcf_operator must be callable", "input_schema")
        start_ns = time.perf_counter_ns()
        stabilized = rcf_operator(copy.deepcopy(dict(inputs)))
        if not isinstance(stabilized, Mapping):
            raise TemporalConstraintError("rcf_operator must return a mapping", "input_schema")
        stabilized = copy.deepcopy(dict(stabilized))
        with self._lock:
            if self._closed:
                raise TimelineError("timeline engine is closed")
            self._sync_arrays_to_branches()
            index = self.active_timeline if timeline_idx is None else timeline_idx
            branch = self._branch(index)
            if branch.status in {BranchStatus.MERGED, BranchStatus.FRAGMENTED}:
                raise TemporalConstraintError(
                    f"branch {index} cannot evolve in status {branch.status.name}",
                    "branch_lifecycle",
                )
            if branch.freeze_until is not None and branch.local_time < branch.freeze_until:
                target_time = min(branch.local_time + self.temporal_resolution, branch.freeze_until)
                branch.local_time = target_time
                branch.tick += 1
                self.master_tick += 1
                if branch.local_time >= branch.freeze_until - EPSILON:
                    branch.freeze_until = None
                    branch.status = BranchStatus.ACTIVE
                    branch.active = True
                self._advance_harmonic_field(index, self.temporal_resolution, excitation=0.0)
                self._refresh_compatibility_views()
                return self._tick_output(index, [], [], start_ns, frozen=True)

            target_time = branch.local_time + self.temporal_resolution
            due: list[TemporalEvent] = []
            while branch.pending and branch.pending[0].timestamp <= target_time + EPSILON:
                candidate = heapq.heappop(branch.pending)
                branch.pending_ids.discard(candidate.event_id)
                due.append(candidate)
            due = self._order_due_events(due)

            tensors: list[FloatArray] = []
            validations: list[dict[str, object]] = []
            processed = 0
            excitation = 0.0
            for event in due:
                violation = self._causal_violation(event, branch)
                if violation is not None:
                    validations.append(violation.to_dict())
                    branch.paradoxes.append(violation)
                    replacement = self._resolve_violation(event, violation, index)
                    if replacement is not None:
                        branch.add_pending(replacement)
                    continue
                resolved = self._apply_temporal_constraints(event, stabilized, index)
                self._evolve_branch_state(branch, resolved, stabilized)
                branch.add_event(resolved)
                tensors.append(self._generate_time_tensor(resolved, index))
                validations.append({
                    "event_id": resolved.event_id, "valid": True,
                    "parents": list(resolved.parent_ids),
                })
                excitation += abs(resolved.amplitude) + float(np.linalg.norm(resolved.quantum_state))
                self.notify_observers(resolved, index)
                processed += 1

            branch.local_time = target_time
            branch.tick += 1
            self.master_tick += 1
            self._advance_harmonic_field(index, self.temporal_resolution, excitation)
            self._update_branch_coherence(index, processed, len(validations) - processed)
            self._evolve_entanglement(index)
            if self.auto_stabilize and branch.coherence < self.stability_threshold:
                self._stabilize_timeline(index)
            runtime_ns = time.perf_counter_ns() - start_ns
            self.metrics["events_processed"] += processed
            self.metrics["runtime_ns"] = runtime_ns
            self.metrics_tracker.update({
                "coherence": branch.coherence,
                "divergence": branch.divergence,
                "new_paradoxes": len(validations) - processed,
                "events_processed": processed,
                "recursion_depth": max(
                    (event.recursion_depth for event in due), default=0,
                ),
                "runtime_ns": runtime_ns,
            })
            self.phase = branch.harmonic_phase
            self._refresh_compatibility_views()
            return self._tick_output(index, tensors, validations, start_ns, frozen=False)

    @staticmethod
    def _order_due_events(events: Sequence[TemporalEvent]) -> list[TemporalEvent]:
        """Topologically order a due batch while retaining deterministic heap priority."""
        by_id = {event.event_id: event for event in events}
        if len(by_id) != len(events):
            raise TemporalConstraintError("duplicate event identity in due batch", "identity")
        indegree = {event_id: 0 for event_id in by_id}
        children: dict[str, list[str]] = defaultdict(list)
        for event in events:
            for parent_id in event.parent_ids:
                if parent_id in by_id:
                    indegree[event.event_id] += 1
                    children[parent_id].append(event.event_id)
        ready = [by_id[event_id] for event_id, degree in indegree.items() if degree == 0]
        heapq.heapify(ready)
        ordered: list[TemporalEvent] = []
        while ready:
            event = heapq.heappop(ready)
            ordered.append(event)
            for child_id in children.get(event.event_id, ()):
                indegree[child_id] -= 1
                if indegree[child_id] == 0:
                    heapq.heappush(ready, by_id[child_id])
        if len(ordered) != len(events):
            cyclic = [by_id[event_id] for event_id, degree in indegree.items() if degree > 0]
            ordered.extend(sorted(cyclic))
        return ordered

    def _tick_output(
        self,
        index: int,
        tensors: Sequence[FloatArray],
        validations: Sequence[Mapping[str, object]],
        start_ns: int,
        *,
        frozen: bool,
    ) -> dict[str, object]:
        """Build one stable tick result."""
        branch = self._branch(index)
        self.metrics["runtime_ns"] = time.perf_counter_ns() - start_ns
        return {
            "master_tick": self.master_tick,
            "branch_tick": branch.tick,
            "timeline": index,
            "branch_id": branch.id,
            "local_time": branch.local_time,
            "time_tensors": list(tensors),
            "causal_validations": [dict(item) for item in validations],
            "breath_pulse": self._generate_breath_pulse(index),
            "coherence": branch.coherence,
            "divergence": branch.divergence,
            "frozen": frozen,
            "metrics": self.get_metrics(),
        }

    def process_all_timelines(
        self,
        inputs: Mapping[str, object],
        rcf_operator: Callable[[Mapping[str, object]], Mapping[str, object]],
    ) -> list[dict[str, object]]:
        """Advance every active world once from a consistent branch ordering."""
        results = []
        for index, branch in enumerate(tuple(self.branches)):
            if branch.active and branch.status in {BranchStatus.ACTIVE, BranchStatus.FROZEN}:
                results.append(self.process_tick(inputs, rcf_operator, index))
        return results

    def _process_timelines_in_parallel(
        self,
        inputs: Mapping[str, object],
        rcf_operator: Callable[[Mapping[str, object]], Mapping[str, object]],
    ) -> None:
        """Compatibility entry point for deterministic multi-world advancement."""
        self.process_all_timelines(inputs, rcf_operator)

    def branch_timeline(
        self,
        branch_point_event: Mapping[str, object] | TemporalEvent | None = None,
        *,
        source_idx: int | None = None,
        branch_time: float | None = None,
        attributes: Mapping[str, object] | None = None,
    ) -> int:
        """Fork a causally inherited temporal world from an explicit point.

        Committed history through the branch point retains event identity while
        receiving isolated objects. Future committed history is not inherited;
        future pending possibilities are copied into the new world's horizon.
        """
        with self._lock:
            source_index = self.active_timeline if source_idx is None else source_idx
            source = self._branch(source_index)
            if branch_time is None:
                if isinstance(branch_point_event, TemporalEvent):
                    point = branch_point_event.timestamp
                elif isinstance(branch_point_event, Mapping) and "timestamp" in branch_point_event:
                    point = float(branch_point_event["timestamp"])
                else:
                    point = source.local_time
            else:
                point = _finite(branch_time, "branch_time")
            if point > source.local_time + EPSILON:
                raise TemporalConstraintError(
                    "cannot fork beyond source world present", "branch_point", point,
                )

            new_index = len(self.branches)
            identifier = f"timeline-{new_index}-{uuid.uuid4().hex[:8]}"
            child = self._new_branch(
                identifier=identifier, parent_id=source.id,
                branch_point=point, generation=source.generation + 1,
                natural_frequency=source.natural_frequency * (
                    1.0 + SACRED_RATIO * 0.01 * (new_index + 1)
                ),
            )
            child.attributes = copy.deepcopy(dict(attributes or {}))
            inherited = [event.clone() for event in source.events if event.timestamp <= point + EPSILON]
            child.events = inherited
            child.local_time = point
            child.tick = max(0, int(round(point / self.temporal_resolution)))
            child.rebuild_causal_indexes()
            child.pending = [
                event.clone() for event in source.pending if event.timestamp >= point - EPSILON
            ]
            child.pending.extend(
                event.clone() for event in source.events if event.timestamp > point + EPSILON
            )
            heapq.heapify(child.pending)
            child.pending_ids = {event.event_id for event in child.pending}
            self._reconstruct_branch_fields(child)
            child.harmonic_phase = source.harmonic_phase
            child.harmonic_amplitudes = np.array(source.harmonic_amplitudes, copy=True)
            child.harmonic_phases = np.array(source.harmonic_phases, copy=True)
            child.coherence = max(0.0, source.coherence * 0.995)

            self.branches.append(child)
            self._branch_by_id[child.id] = new_index
            source.add_child_branch(child.id)
            self._expand_entanglement(source_index, new_index)
            self.recursion_stacks.append(deque(maxlen=self.max_recursion_depth))
            self.metrics["timeline_branches"] += 1
            self.metrics_tracker.branch_count += 1

            if branch_point_event is not None:
                event = TemporalEvent.from_dict(branch_point_event) \
                    if isinstance(branch_point_event, Mapping) \
                    else branch_point_event.clone(preserve_id=False)
                event.timestamp = max(point, event.timestamp)
                event.metadata = {
                    **event.metadata,
                    "branch_point": True,
                    "parent_timeline": source_index,
                    "child_timeline": new_index,
                }
                self.schedule_event(event, new_index, event.recursion_depth)
            self._refresh_compatibility_views()
            self._update_all_divergences()
            return new_index

    def _reconstruct_branch_fields(self, branch: TemporalBranch) -> None:
        """Reconstruct state and ethics from inherited realized history."""
        branch.state_vector = np.zeros(self.num_dimensions, dtype=np.float64)
        branch.ethical_state = np.zeros(self.ethical_dimensions, dtype=np.float64)
        for event in branch.events:
            event_state = _vector(
                event.quantum_state, self.num_dimensions, "quantum_state",
            )
            event_ethics = _vector(
                event.ethical_vectors, self.ethical_dimensions, "ethical_vectors",
            )
            alpha = min(0.85, 1.0 / (2.0 + event.recursion_depth))
            branch.state_vector = (1.0 - alpha) * branch.state_vector + alpha * event_state
            branch.ethical_state = (1.0 - alpha) * branch.ethical_state + alpha * event_ethics

    def _expand_entanglement(self, source_idx: int, child_idx: int) -> None:
        """Expand the symmetric relation field for a new inherited world."""
        old_size = self.entanglement_matrix.shape[0]
        matrix = np.eye(old_size + 1, dtype=np.float64)
        matrix[:old_size, :old_size] = self.entanglement_matrix
        shared = self._shared_history_ratio(source_idx, child_idx, child_override=self.branches[child_idx])
        inherited_coupling = max(0.5, shared)
        matrix[source_idx, child_idx] = matrix[child_idx, source_idx] = inherited_coupling
        for index in range(old_size):
            if index == source_idx:
                continue
            propagated = self.entanglement_matrix[source_idx, index] * PHI**-1
            matrix[index, child_idx] = matrix[child_idx, index] = propagated
        self.entanglement_matrix = matrix

    def switch_timeline(self, timeline_idx: int) -> bool:
        """Switch the active world without altering its state."""
        with self._lock:
            try:
                branch = self._branch(timeline_idx)
            except TemporalConstraintError:
                return False
            if branch.status in {BranchStatus.MERGED, BranchStatus.FRAGMENTED}:
                return False
            self.active_timeline = timeline_idx
            self.phase = branch.harmonic_phase
            return True

    def create_counterfactual(
        self,
        intervention: Mapping[str, object] | TemporalEvent,
        *,
        source_idx: int | None = None,
        at_time: float | None = None,
    ) -> int:
        """Fork a world and inject an explicitly marked intervention."""
        index = self.branch_timeline(
            source_idx=source_idx, branch_time=at_time,
            attributes={"counterfactual": True},
        )
        event = TemporalEvent.from_dict(intervention) \
            if isinstance(intervention, Mapping) else intervention.clone(preserve_id=False)
        event.metadata = {**event.metadata, "intervention": True}
        event.timestamp = max(event.timestamp, self.branches[index].local_time)
        self.schedule_event(event, index, event.recursion_depth)
        return index

    def common_ancestor(self, left_idx: int, right_idx: int) -> int | None:
        """Return the nearest common branch ancestor by stable lineage identity."""
        left = self._branch(left_idx)
        right = self._branch(right_idx)
        left_chain: dict[str, int] = {}
        cursor: TemporalBranch | None = left
        depth = 0
        while cursor is not None:
            left_chain[cursor.id] = depth
            cursor = self.branches[self._branch_by_id[cursor.parent_id]] \
                if cursor.parent_id in self._branch_by_id else None
            depth += 1
        cursor = right
        while cursor is not None:
            if cursor.id in left_chain:
                return self._branch_by_id[cursor.id]
            cursor = self.branches[self._branch_by_id[cursor.parent_id]] \
                if cursor.parent_id in self._branch_by_id else None
        return None

    def branch_lineage(self, timeline_idx: int) -> list[int]:
        """Return root-to-world branch lineage indices."""
        branch = self._branch(timeline_idx)
        lineage = []
        cursor: TemporalBranch | None = branch
        while cursor is not None:
            lineage.append(self._branch_by_id[cursor.id])
            cursor = self.branches[self._branch_by_id[cursor.parent_id]] \
                if cursor.parent_id in self._branch_by_id else None
        lineage.reverse()
        return lineage

    def merge_timelines(
        self,
        source_idx: int,
        target_idx: int,
        merge_strategy: str = "overlay",
    ) -> bool:
        """Converge source into target without consuming either world's history."""
        return self.merge_timelines_detailed(source_idx, target_idx, merge_strategy).success

    def merge_timelines_detailed(
        self,
        source_idx: int,
        target_idx: int,
        merge_strategy: str = "overlay",
    ) -> MergeReport:
        """Perform deterministic causal reconciliation and return merge evidence."""
        if source_idx == target_idx:
            raise TemporalConstraintError("cannot merge a timeline into itself", "merge")
        if merge_strategy not in {"overlay", "interleave", "selective"}:
            raise TemporalConstraintError(
                f"unknown merge strategy {merge_strategy!r}", "merge_strategy",
            )
        with self._lock:
            source = self._branch(source_idx)
            target = self._branch(target_idx)
            before = 1.0 - self.measure_pair_divergence(source_idx, target_idx)
            target_ids = set(target.event_index)
            source_delta = [event for event in source.events if event.event_id not in target_ids]
            target_keys = {
                self._event_conflict_key(event): event for event in target.events
            }
            imported = 0
            conflicts = 0
            imported_ids: list[str] = []
            identity_map: dict[str, str] = {}
            for source_event in source_delta:
                key = self._event_conflict_key(source_event)
                conflict = target_keys.get(key)
                if conflict is not None and (
                    conflict.semantic_fingerprint() != source_event.semantic_fingerprint()
                ):
                    conflicts += 1
                    if merge_strategy == "selective":
                        continue
                    event = self._reconcile_conflict(
                        source_event, conflict, source_idx, target_idx, merge_strategy,
                    )
                else:
                    event = source_event.clone(preserve_id=False, origin_branch_id=source.id)
                    event.metadata = {
                        **event.metadata,
                        "imported_from": source_idx,
                        "source_event_id": source_event.event_id,
                    }
                event.timestamp = max(
                    target.local_time + self.temporal_resolution,
                    event.timestamp if merge_strategy != "interleave" else target.local_time
                    + self.temporal_resolution * (imported + 1),
                )
                available = set(target.event_index) | set(imported_ids)
                event.causal_parents = [
                    identity_map.get(parent_id, parent_id)
                    for parent_id in event.parent_ids
                    if identity_map.get(parent_id, parent_id) in available
                ]
                event.sequence = self._next_sequence()
                event.origin_branch_id = target.id
                target.add_pending(event)
                imported_ids.append(event.event_id)
                identity_map[source_event.event_id] = event.event_id
                imported += 1

            parents = ([target.latest_event.event_id] if target.latest_event else [])
            if imported_ids:
                parents.append(imported_ids[-1])
            weight_source = source.coherence / max(
                source.coherence + target.coherence, EPSILON,
            )
            merge_state = (
                weight_source * source.state_vector
                + (1.0 - weight_source) * target.state_vector
            )
            merge_event = TemporalEvent(
                timestamp=target.local_time + self.temporal_resolution * (imported + 1),
                event_type="timeline_merge",
                quantum_state=merge_state,
                ethical_vectors=(
                    weight_source * source.ethical_state
                    + (1.0 - weight_source) * target.ethical_state
                ),
                causal_parents=parents,
                metadata={
                    "source_timeline": source_idx,
                    "target_timeline": target_idx,
                    "strategy": merge_strategy,
                    "imported_events": imported,
                    "conflicts": conflicts,
                    "common_ancestor": self.common_ancestor(source_idx, target_idx),
                },
                amplitude=1.0 - before,
                event_id=uuid.uuid4().hex,
                priority=1,
                origin_branch_id=target.id,
                sequence=self._next_sequence(),
            )
            target.add_pending(merge_event)
            coupling = min(1.0, 0.75 + 0.25 * before)
            self.entanglement_matrix[source_idx, target_idx] = coupling
            self.entanglement_matrix[target_idx, source_idx] = coupling
            target.coherence = min(
                1.0, (target.coherence + source.coherence) * 0.5
                * math.exp(-0.05 * conflicts),
            )
            predicted_after = min(1.0, before + 0.5 * (1.0 - before))
            record = {
                "source": source_idx, "target": target_idx,
                "strategy": merge_strategy, "time": target.local_time,
                "merge_event_id": merge_event.event_id,
            }
            target.merge_records.append(record)
            self.metrics["timeline_merges"] += 1
            self.metrics_tracker.merge_count += 1
            report = MergeReport(
                source_idx, target_idx, merge_strategy, imported, conflicts,
                before, predicted_after, merge_event.event_id,
            )
            self._last_merge_report = report
            self._refresh_compatibility_views()
            return report

    def _event_conflict_key(self, event: TemporalEvent) -> tuple[int, str]:
        """Map an event into a temporal-resolution conflict cell."""
        quantum = int(round(event.timestamp / self.temporal_resolution))
        return (quantum, event.event_type)

    def _reconcile_conflict(
        self,
        source: TemporalEvent,
        target: TemporalEvent,
        source_idx: int,
        target_idx: int,
        strategy: str,
    ) -> TemporalEvent:
        """Synthesize a new event from incompatible realizations."""
        source_weight = self.branches[source_idx].coherence
        target_weight = self.branches[target_idx].coherence
        total = max(source_weight + target_weight, EPSILON)
        source_weight /= total
        target_weight /= total
        if strategy == "overlay":
            state = source_weight * _vector(
                source.quantum_state, self.num_dimensions, "quantum_state",
            ) + target_weight * _vector(
                target.quantum_state, self.num_dimensions, "quantum_state",
            )
            ethics = source_weight * _vector(
                source.ethical_vectors, self.ethical_dimensions, "ethical_vectors",
            ) + target_weight * _vector(
                target.ethical_vectors, self.ethical_dimensions, "ethical_vectors",
            )
        else:
            state = np.concatenate((source.quantum_state, target.quantum_state))
            spectrum = np.fft.rfft(state)
            state = np.fft.irfft(spectrum, n=state.size)[:self.num_dimensions]
            state = _vector(state, self.num_dimensions, "quantum_state")
            ethics = 0.5 * (
                _vector(source.ethical_vectors, self.ethical_dimensions, "ethical_vectors")
                + _vector(target.ethical_vectors, self.ethical_dimensions, "ethical_vectors")
            )
        return TemporalEvent(
            timestamp=max(source.timestamp, target.timestamp),
            event_type=source.event_type,
            quantum_state=state,
            ethical_vectors=ethics,
            causal_parents=[target.event_id],
            recursion_depth=max(source.recursion_depth, target.recursion_depth),
            metadata={
                "reconciliation": strategy,
                "source_event_id": source.event_id,
                "target_event_id": target.event_id,
            },
            entropy_consumed=(
                source.entropy_consumed + target.entropy_consumed
                + self._jensen_shannon(source.quantum_state, target.quantum_state)
            ),
            paradox_resolved=True,
            phase=np.angle(
                np.exp(1j * source.phase) + np.exp(1j * target.phase)
            ) % TAU,
            amplitude=0.5 * (source.amplitude + target.amplitude),
            event_id=uuid.uuid4().hex,
        )

    def _validate_event_metadata(self, event: TemporalEvent) -> None:
        """Ensure dynamic metadata is bounded, serializable, and non-recursive."""
        encoded = json.dumps(_json_safe(event.metadata), sort_keys=True, allow_nan=False)
        if len(encoded.encode("utf-8")) > 4 * 1024 * 1024:
            raise TemporalConstraintError("event metadata exceeds 4 MiB", "resource_geometry")

    def _causal_violation(
        self, event: TemporalEvent, branch: TemporalBranch,
    ) -> CausalViolation | None:
        """Return the first causal invariant violated by a candidate event."""
        if event.event_id in branch.event_index:
            existing = branch.event_index[event.event_id]
            if existing.semantic_fingerprint() != event.semantic_fingerprint():
                return CausalViolation(
                    ParadoxKind.IDENTITY_COLLISION, event.event_id, None, branch.id,
                    event.timestamp, 1.0, "stable identity denotes incompatible events",
                )
            return None
        for parent_id in event.parent_ids:
            parent = branch.event_index.get(parent_id)
            if parent is None:
                return CausalViolation(
                    ParadoxKind.ORPHAN_PARENT, event.event_id, parent_id, branch.id,
                    event.timestamp, 0.65, "causal parent is absent from realized history",
                )
            if parent.timestamp > event.timestamp + EPSILON:
                return CausalViolation(
                    ParadoxKind.REVERSE_CAUSALITY, event.event_id, parent_id, branch.id,
                    event.timestamp, 0.9, "effect precedes its declared cause",
                )
            if self._causal_reachable(branch, event.event_id, parent_id):
                return CausalViolation(
                    ParadoxKind.CAUSAL_LOOP, event.event_id, parent_id, branch.id,
                    event.timestamp, 1.0, "causal edge closes a directed cycle",
                )
        return None

    @staticmethod
    def _causal_reachable(branch: TemporalBranch, start: str, goal: str) -> bool:
        """Test reachability in the committed parent-to-child causal DAG."""
        frontier = [start]
        seen: set[str] = set()
        while frontier:
            node = frontier.pop()
            if node == goal:
                return True
            if node in seen:
                continue
            seen.add(node)
            frontier.extend(branch.causal_children.get(node, ()))
        return False

    def _resolve_violation(
        self, event: TemporalEvent, violation: CausalViolation, timeline_idx: int,
    ) -> TemporalEvent | None:
        """Resolve only failures with a semantics-preserving repair."""
        self.metrics["paradoxes_resolved"] += 1
        self.metrics_tracker.paradox_count += 1
        if violation.kind is ParadoxKind.ORPHAN_PARENT:
            branch = self._branch(timeline_idx)
            pending_ids = {item.event_id for item in branch.pending}
            if violation.parent_id in pending_ids:
                delayed = event.clone(timestamp=event.timestamp + self.temporal_resolution)
                delayed.sequence = self._next_sequence()
                delayed.metadata["causal_deferred"] = int(
                    delayed.metadata.get("causal_deferred", 0)
                ) + 1
                if delayed.metadata["causal_deferred"] <= self.max_recursion_depth:
                    return delayed
        return None

    def _apply_temporal_constraints(
        self, event: TemporalEvent, inputs: Mapping[str, object], timeline_idx: int,
    ) -> TemporalEvent:
        """Project a candidate event onto this engine's temporal geometry."""
        branch = self._branch(timeline_idx)
        result = event.clone()
        result.quantum_state = _vector(result.quantum_state, self.num_dimensions, "quantum_state")
        result.ethical_vectors = _vector(
            result.ethical_vectors, self.ethical_dimensions, "ethical_vectors",
        )
        if result.timestamp < branch.branch_point - EPSILON:
            raise TemporalConstraintError(
                "event predates branch identity", "branch_point", result.timestamp,
            )
        result.phase = (result.phase + branch.harmonic_phase) % TAU
        modulation = inputs.get("temporal_modulation", 1.0)
        if isinstance(modulation, (int, float, np.number)):
            result.amplitude *= _finite(float(modulation), "temporal_modulation")
        if bool(result.metadata.get("quantum_collapse", False)):
            result.quantum_state = self._collapse_quantum_state(result, timeline_idx)
            self.metrics["quantum_collapses"] += 1
        return result

    def _collapse_quantum_state(
        self, event: TemporalEvent, timeline_idx: int,
    ) -> FloatArray:
        """Collapse amplitudes reproducibly without order-dependent global RNG state."""
        weights = np.square(np.abs(_vector(
            event.quantum_state, self.num_dimensions, "quantum_state",
        )))
        probabilities = _normalize_distribution(weights)
        digest = hashlib.sha256(
            f"{self.seed}:{timeline_idx}:{event.semantic_fingerprint()}".encode()
        ).digest()
        draw = int.from_bytes(digest[:8], "big") / float(2**64)
        selected = min(
            int(np.searchsorted(np.cumsum(probabilities), draw, side="right")),
            self.num_dimensions - 1,
        )
        collapsed = np.zeros(self.num_dimensions, dtype=np.float64)
        collapsed[selected] = 1.0
        return collapsed

    def _evolve_branch_state(
        self, branch: TemporalBranch, event: TemporalEvent,
        inputs: Mapping[str, object],
    ) -> None:
        """Integrate one event using depth-aware exponential state memory."""
        alpha = min(0.8, 1.0 / (2.0 + event.recursion_depth))
        branch.state_vector = (
            (1.0 - alpha) * branch.state_vector + alpha * event.quantum_state
        )
        ethical_alpha = alpha * 0.5
        branch.ethical_state = (
            (1.0 - ethical_alpha) * branch.ethical_state
            + ethical_alpha * event.ethical_vectors
        )
        forcing = inputs.get("state_forcing")
        if forcing is not None:
            branch.state_vector += 0.05 * _vector(
                forcing, self.num_dimensions, "state_forcing",
            )
        if not np.all(np.isfinite(branch.state_vector)):
            raise QuantumDecoherenceError("state evolution produced non-finite values")

    def _advance_harmonic_field(
        self, timeline_idx: int, dt: float, excitation: float,
    ) -> None:
        """Advance a multi-mode Kuramoto field coupled through branch entanglement."""
        branch = self._branch(timeline_idx)
        phases = np.asarray([item.harmonic_phase for item in self.branches])
        weights = self.entanglement_matrix[timeline_idx]
        coupling = float(np.sum(weights * np.sin(phases - branch.harmonic_phase)))
        coupling /= max(float(np.sum(weights)), EPSILON)
        branch.harmonic_phase = (
            branch.harmonic_phase
            + TAU * branch.natural_frequency * dt
            + self.coupling_strength * coupling * dt
        ) % TAU
        modes = np.arange(1, self.harmonic_modes + 1, dtype=np.float64)
        modal_coupling = np.sin(
            modes * branch.harmonic_phase - branch.harmonic_phases
        )
        branch.harmonic_phases = (
            branch.harmonic_phases
            + TAU * branch.natural_frequency * modes * dt
            + self.coupling_strength * modal_coupling * dt
        ) % TAU
        energy = math.log1p(max(0.0, excitation))
        target = 1.0 / np.sqrt(modes)
        branch.harmonic_amplitudes = (
            0.985 * branch.harmonic_amplitudes + 0.015 * target
            + energy * 0.001 / modes
        )

    def _update_branch_coherence(
        self, timeline_idx: int, processed: int, violations: int,
    ) -> None:
        """Estimate causal, state, harmonic, and ethical self-consistency."""
        branch = self._branch(timeline_idx)
        causal = processed / max(processed + violations, 1)
        state_norm = float(np.linalg.norm(branch.state_vector))
        state_health = 1.0 / (1.0 + max(0.0, state_norm - math.sqrt(self.num_dimensions)))
        order = abs(np.mean(np.exp(1j * branch.harmonic_phases)))
        ethical = 1.0 / (1.0 + float(np.linalg.norm(branch.ethical_state)) / 8.0)
        observed = 0.35 * causal + 0.25 * state_health + 0.25 * order + 0.15 * ethical
        branch.coherence = float(np.clip(0.85 * branch.coherence + 0.15 * observed, 0.0, 1.0))
        self._update_all_divergences()

    def _evolve_entanglement(self, changed_idx: int) -> None:
        """Relax pair relations toward shared-history and state similarity."""
        for other in range(len(self.branches)):
            if other == changed_idx:
                continue
            similarity = 1.0 - self.measure_pair_divergence(changed_idx, other)
            old = self.entanglement_matrix[changed_idx, other]
            value = float(np.clip(0.97 * old + 0.03 * similarity, 0.0, 1.0))
            self.entanglement_matrix[changed_idx, other] = value
            self.entanglement_matrix[other, changed_idx] = value
        np.fill_diagonal(self.entanglement_matrix, 1.0)

    def _stabilize_timeline(self, timeline_idx: int) -> None:
        """Damp unstable modes while retaining the world's realized history."""
        branch = self._branch(timeline_idx)
        branch.state_vector = np.tanh(branch.state_vector)
        branch.ethical_state = np.tanh(branch.ethical_state)
        modes = np.arange(1, self.harmonic_modes + 1, dtype=np.float64)
        branch.harmonic_amplitudes = np.minimum(
            branch.harmonic_amplitudes, 2.0 / np.sqrt(modes),
        )
        branch.coherence = min(1.0, branch.coherence + 0.08)

    def _generate_time_tensor(
        self, event: TemporalEvent, timeline_idx: int,
    ) -> FloatArray:
        """Encode event/state/causal phase interaction as a finite temporal tensor."""
        branch = self._branch(timeline_idx)
        fingerprint = _stable_digest({
            "event": event.semantic_fingerprint(),
            "state": np.round(branch.state_vector, 12).tolist(),
            "ethics": np.round(branch.ethical_state, 12).tolist(),
            "phase": round(branch.harmonic_phase, 12),
            "coherence": round(branch.coherence, 12),
        })
        cache_key = (event.event_id, timeline_idx, fingerprint)
        cached = self._event_cache.get(cache_key)
        if cached is not None:
            self.metrics["cache_hits"] += 1
            total = self.metrics["cache_hits"] + self.metrics["cache_miss_count"]
            self.cache_hit_rate = self.metrics["cache_hits"] / total
            return np.array(cached.quantum_state, copy=True).reshape(
                self.num_dimensions, self.ethical_dimensions,
            )
        state = _vector(event.quantum_state, self.num_dimensions, "quantum_state")
        ethics = _vector(event.ethical_vectors, self.ethical_dimensions, "ethical_vectors")
        phase_wave = np.cos(
            branch.harmonic_phase + np.arange(self.num_dimensions) * TAU / self.num_dimensions
        )
        causal_gain = 1.0 / (1.0 + len(event.parent_ids) + event.recursion_depth)
        tensor = np.outer(
            np.tanh(state + branch.state_vector) + causal_gain * phase_wave,
            np.tanh(ethics + branch.ethical_state),
        ) * branch.coherence
        self.metrics["cache_miss_count"] += 1
        self.cache_miss_count = self.metrics["cache_miss_count"]
        total = self.metrics["cache_hits"] + self.metrics["cache_miss_count"]
        self.cache_hit_rate = self.metrics["cache_hits"] / total
        # A lightweight event envelope preserves the historical cache surface.
        envelope = event.clone()
        envelope.quantum_state = np.array(tensor, copy=True).reshape(-1)
        self._event_cache[cache_key] = envelope
        if len(self._event_cache) > 4096:
            self._event_cache.pop(next(iter(self._event_cache)))
        return tensor

    def _generate_breath_pulse(self, timeline_idx: int | None = None) -> dict[str, object]:
        """Return the current weighted breath phase and harmonic field strength."""
        branch = self._branch(timeline_idx)
        position = (branch.harmonic_phase / TAU) % 1.0
        phase = BreathPhase.from_cycle_position(position)
        return {
            "phase": phase, "phase_name": phase.name,
            "position": position, "amplitude": float(
                np.linalg.norm(branch.harmonic_amplitudes)
            ), "description": phase.description,
        }

    @staticmethod
    def _jensen_shannon(left: Sequence[float], right: Sequence[float]) -> float:
        """Return normalized Jensen-Shannon divergence in [0, 1]."""
        size = max(len(left), len(right))
        p = _normalize_distribution(_vector(left, size, "left"))
        q = _normalize_distribution(_vector(right, size, "right"))
        midpoint = 0.5 * (p + q)
        def kl(source: FloatArray, target: FloatArray) -> float:
            mask = source > EPSILON
            return float(np.sum(source[mask] * np.log2(source[mask] / target[mask])))
        return float(np.clip(0.5 * kl(p, midpoint) + 0.5 * kl(q, midpoint), 0.0, 1.0))

    def _shared_history_ratio(
        self, left_idx: int, right_idx: int,
        *, child_override: TemporalBranch | None = None,
    ) -> float:
        """Measure stable event identity shared by two realized histories."""
        left = self._branch(left_idx)
        right = child_override or self._branch(right_idx)
        a, b = set(left.event_index), set(right.event_index)
        return len(a & b) / max(len(a | b), 1)

    def measure_pair_divergence(self, left_idx: int, right_idx: int) -> float:
        """Measure world separation across state, history, harmonics, and ethics."""
        left, right = self._branch(left_idx), self._branch(right_idx)
        js_state = self._jensen_shannon(left.state_vector, right.state_vector)
        scale = max(
            float(np.linalg.norm(left.state_vector)),
            float(np.linalg.norm(right.state_vector)), 1.0,
        )
        euclidean = min(
            1.0, float(np.linalg.norm(left.state_vector - right.state_vector)) / scale,
        )
        state = 0.5 * (js_state + euclidean)
        history = 1.0 - self._shared_history_ratio(left_idx, right_idx)
        harmonic = _phase_distance(left.harmonic_phase, right.harmonic_phase) / math.pi
        ln, rn = np.linalg.norm(left.ethical_state), np.linalg.norm(right.ethical_state)
        if ln <= EPSILON and rn <= EPSILON:
            ethical = 0.0
        elif ln <= EPSILON or rn <= EPSILON:
            ethical = 1.0
        else:
            ethical = 0.5 * (1.0 - float(np.dot(
                left.ethical_state / ln, right.ethical_state / rn,
            )))
        return float(np.clip(0.4 * state + 0.3 * history + 0.2 * harmonic + 0.1 * ethical, 0, 1))

    def _update_all_divergences(self) -> None:
        """Update each world's mean separation from all other worlds."""
        count = len(self.branches)
        for index, branch in enumerate(self.branches):
            branch.divergence = 0.0 if count == 1 else math.fsum(
                self.measure_pair_divergence(index, other)
                for other in range(count) if other != index
            ) / (count - 1)

    def measure_timeline_divergence(self) -> float:
        """Return mean pairwise world divergence without mutating state."""
        pairs = [
            self.measure_pair_divergence(i, j)
            for i in range(len(self.branches)) for j in range(i + 1, len(self.branches))
        ]
        return math.fsum(pairs) / len(pairs) if pairs else 0.0

    def spectral_signature(self, timeline_idx: int | None = None) -> FloatArray:
        """Return the branch's normalized complex harmonic spectrum."""
        branch = self._branch(timeline_idx)
        spectrum = branch.harmonic_amplitudes * np.exp(1j * branch.harmonic_phases)
        norm = float(np.linalg.norm(spectrum))
        return spectrum if norm <= EPSILON else spectrum / norm

    def causal_ancestors(self, event_id: str, timeline_idx: int | None = None) -> set[str]:
        """Return transitive causal ancestors of a committed event."""
        branch = self._branch(timeline_idx)
        if event_id not in branch.event_index:
            raise TemporalConstraintError("unknown event id", "causal_query")
        result: set[str] = set()
        frontier = list(branch.causal_parents.get(event_id, ()))
        while frontier:
            node = frontier.pop()
            if node not in result:
                result.add(node)
                frontier.extend(branch.causal_parents.get(node, ()))
        return result

    def causal_descendants(self, event_id: str, timeline_idx: int | None = None) -> set[str]:
        """Return transitive causal descendants of a committed event."""
        branch = self._branch(timeline_idx)
        if event_id not in branch.event_index:
            raise TemporalConstraintError("unknown event id", "causal_query")
        result: set[str] = set()
        frontier = list(branch.causal_children.get(event_id, ()))
        while frontier:
            node = frontier.pop()
            if node not in result:
                result.add(node)
                frontier.extend(branch.causal_children.get(node, ()))
        return result

    def validate_causal_graph(self, timeline_idx: int | None = None) -> dict[str, object]:
        """Audit identity, parent existence, temporal order, and DAG acyclicity."""
        branch = self._branch(timeline_idx)
        violations: list[dict[str, object]] = []
        indegree = {event_id: 0 for event_id in branch.event_index}
        for event in branch.events:
            for parent_id in event.parent_ids:
                parent = branch.event_index.get(parent_id)
                if parent is None:
                    violations.append({"kind": "orphan_parent", "event_id": event.event_id,
                                       "parent_id": parent_id})
                    continue
                indegree[event.event_id] += 1
                if parent.timestamp > event.timestamp + EPSILON:
                    violations.append({"kind": "reverse_causality", "event_id": event.event_id,
                                       "parent_id": parent_id})
        queue = deque(event_id for event_id, degree in indegree.items() if degree == 0)
        visited = 0
        while queue:
            node = queue.popleft()
            visited += 1
            for child in branch.causal_children.get(node, ()):
                if child in indegree:
                    indegree[child] -= 1
                    if indegree[child] == 0:
                        queue.append(child)
        if visited != len(indegree):
            violations.append({"kind": "causal_loop", "cycle_nodes": [
                event_id for event_id, degree in indegree.items() if degree > 0
            ]})
        return {"valid": not violations, "event_count": len(indegree),
                "violations": violations}

    def causal_binding(
        self, cause: TemporalEvent | str, effect: TemporalEvent,
        timeline_idx: int | None = None,
    ) -> TemporalEvent:
        """Bind a scheduled effect to a stable realized cause."""
        branch = self._branch(timeline_idx)
        cause_id = cause.event_id if isinstance(cause, TemporalEvent) else str(cause)
        if cause_id not in branch.event_index:
            raise TemporalConstraintError("cause must be realized in target world", "causality")
        bound = effect.clone(preserve_id=False)
        bound.causal_parents = list(dict.fromkeys((*bound.parent_ids, cause_id)))
        bound.timestamp = max(bound.timestamp, branch.event_index[cause_id].timestamp)
        return self.schedule_event(bound, timeline_idx, bound.recursion_depth)

    def breath_synchronization(
        self, events: Sequence[TemporalEvent], timeline_idx: int | None = None,
    ) -> list[TemporalEvent]:
        """Return isolated events aligned to the next phase quantum."""
        branch = self._branch(timeline_idx)
        return self._align_events_to_breath(events, branch.local_time)

    def _align_events_to_breath(
        self, events: Sequence[TemporalEvent], origin: float = 0.0,
    ) -> list[TemporalEvent]:
        """Quantize event times without mutating caller-owned events."""
        aligned = []
        for event in events:
            quantum = max(0, math.ceil((event.timestamp - origin) / self.temporal_resolution - EPSILON))
            clone = event.clone(timestamp=origin + quantum * self.temporal_resolution)
            clone.phase = (clone.timestamp * TAU * self.breath_frequency) % TAU
            aligned.append(clone)
        return aligned

    def create_recursive_loop(
        self, events: Sequence[TemporalEvent], timeline_idx: int | None = None,
    ) -> list[TemporalEvent]:
        """Create a bounded causal recursion with explicit predecessor identity."""
        if not events:
            return []
        branch = self._branch(timeline_idx)
        generated: list[TemporalEvent] = []
        parent = branch.latest_event.event_id if branch.latest_event else None
        for depth, template in enumerate(events[:self.max_recursion_depth], 1):
            clone = template.clone(preserve_id=False)
            clone.recursion_depth = depth
            clone.timestamp = max(
                clone.timestamp, branch.local_time + depth * self.temporal_resolution,
            )
            clone.causal_parents = [parent] if parent else []
            clone.metadata = {**clone.metadata, "recursive_loop": True, "iteration": depth}
            generated.append(self.schedule_event(clone, timeline_idx, depth))
            parent = generated[-1].event_id
        return generated

    def recursive_closure(
        self, operator: Callable[[object], object], initial: object,
        *, tolerance: float = 1e-9, max_iterations: int | None = None,
    ) -> dict[str, object]:
        """Find a bounded fixed point or exact representational cycle."""
        if not callable(operator):
            raise TemporalConstraintError("operator must be callable", "recursion")
        limit = self.max_recursion_depth if max_iterations is None else int(max_iterations)
        if not 1 <= limit <= max(1024, self.max_recursion_depth):
            raise TemporalConstraintError("invalid closure iteration limit", "recursion")
        current = copy.deepcopy(initial)
        seen: dict[str, int] = {_stable_digest(current): 0}
        for iteration in range(1, limit + 1):
            nxt = operator(copy.deepcopy(current))
            converged = False
            try:
                left = np.asarray(current, dtype=np.float64)
                right = np.asarray(nxt, dtype=np.float64)
                converged = left.shape == right.shape and bool(np.allclose(
                    left, right, rtol=tolerance, atol=tolerance,
                ))
            except (TypeError, ValueError):
                converged = nxt == current
            digest = _stable_digest(nxt)
            if converged:
                return {"value": nxt, "converged": True, "cycle_length": 1, "iterations": iteration}
            if digest in seen:
                return {"value": nxt, "converged": False,
                        "cycle_length": iteration - seen[digest], "iterations": iteration}
            seen[digest] = iteration
            current = nxt
        return {"value": current, "converged": False, "cycle_length": 0, "iterations": limit}

    def enforce_boundary_conditions(
        self, events: Iterable[TemporalEvent], start_time: float, end_time: float,
    ) -> list[TemporalEvent]:
        """Return isolated events inside an inclusive finite temporal boundary."""
        start, end = _finite(start_time, "start_time"), _finite(end_time, "end_time")
        if start > end:
            raise TemporalConstraintError("start_time exceeds end_time", "interval")
        return [event.clone() for event in events if start <= event.timestamp <= end]

    def propagate_state(
        self, source_idx: int, target_idx: int, strength: float = 0.5,
    ) -> None:
        """Propagate state through entanglement without merging histories."""
        amount = _bounded(strength, "strength", 0.0, 1.0)
        with self._lock:
            source, target = self._branch(source_idx), self._branch(target_idx)
            gain = amount * self.entanglement_matrix[source_idx, target_idx]
            target.state_vector = (1 - gain) * target.state_vector + gain * source.state_vector
            target.ethical_state = (1 - gain) * target.ethical_state + gain * source.ethical_state
            target.harmonic_phase = float(np.angle(
                (1 - gain) * np.exp(1j * target.harmonic_phase)
                + gain * np.exp(1j * source.harmonic_phase)
            ) % TAU)
            self._update_all_divergences()
            self._refresh_compatibility_views()

    def register_observer(self, observer: Observer | str) -> None:
        """Register a callable or named method observer exactly once."""
        if not callable(observer) and not isinstance(observer, str):
            raise TemporalConstraintError("observer must be callable or method name", "observer")
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def unregister_observer(self, observer: Observer | str) -> bool:
        """Remove an observer if registered."""
        with self._lock:
            try:
                self._observers.remove(observer)
                return True
            except ValueError:
                return False

    def notify_observers(self, event: TemporalEvent, timeline_idx: int) -> None:
        """Notify a stable observer snapshot and isolate callback failures."""
        for observer in tuple(self._observers):
            try:
                callback = getattr(self, observer) if isinstance(observer, str) else observer
                callback(event.clone(), timeline_idx)
            except BaseException as exc:
                if isinstance(exc, (KeyboardInterrupt, SystemExit, GeneratorExit)):
                    raise
                logger.exception("timeline observer failed", extra={"event_id": event.event_id})

    def create_temporal_freeze(
        self, duration: float, timeline_idx: int | None = None,
    ) -> dict[str, object]:
        """Freeze realization while allowing local time and harmonics to advance."""
        interval = _finite(duration, "duration")
        if interval < 0:
            raise TemporalConstraintError("duration must be non-negative", "freeze")
        branch = self._branch(timeline_idx)
        branch.freeze_until = branch.local_time + interval
        branch.status = BranchStatus.FROZEN if interval > 0 else BranchStatus.ACTIVE
        return {"timeline": self._branch_index(branch.id), "until": branch.freeze_until}

    def apply_ethical_corrections(
        self, threshold: float = 1.0, timeline_idx: int | None = None,
    ) -> FloatArray:
        """Project excessive ethical components into a smooth bounded region."""
        limit = _finite(threshold, "threshold")
        if limit <= 0:
            raise TemporalConstraintError("threshold must be positive", "ethics")
        branch = self._branch(timeline_idx)
        corrected = limit * np.tanh(branch.ethical_state / limit)
        if not np.allclose(corrected, branch.ethical_state):
            self.metrics["ethical_corrections"] += 1
        branch.ethical_state = corrected
        self._refresh_compatibility_views()
        return np.array(corrected, copy=True)

    def generate_signature(self, timeline_idx: int | None = None) -> str:
        """Return a deterministic semantic signature for one temporal world."""
        branch = self._branch(timeline_idx)
        return _stable_digest({
            "history": [event.semantic_fingerprint() for event in branch.events],
            "pending": [event.semantic_fingerprint() for event in sorted(branch.pending)],
            "state": np.round(branch.state_vector, 12).tolist(),
            "ethics": np.round(branch.ethical_state, 12).tolist(),
            "time": branch.local_time, "tick": branch.tick,
        })

    def get_current_state(self, timeline_idx: int | None = None) -> dict[str, object]:
        """Return an isolated diagnostic view of one temporal world."""
        branch = self._branch(timeline_idx)
        return {
            "branch_id": branch.id, "local_time": branch.local_time,
            "tick": branch.tick, "status": branch.status.name,
            "coherence": branch.coherence, "divergence": branch.divergence,
            "state_vector": np.array(branch.state_vector, copy=True),
            "ethical_state": np.array(branch.ethical_state, copy=True),
            "pending_events": len(branch.pending), "realized_events": len(branch.events),
            "breath_phase": self._generate_breath_pulse(timeline_idx),
        }

    def get_metrics(self) -> dict[str, object]:
        """Return cumulative and bounded metric summaries."""
        return {**self.metrics, **self.metrics_tracker.get_summary(),
                "timeline_count": len(self.branches),
                "global_divergence": self.measure_timeline_divergence()}

    def resolve_incoherence(self, timeline_idx: int | None = None) -> float:
        """Explicitly stabilize a world and return resulting coherence."""
        index = self.active_timeline if timeline_idx is None else timeline_idx
        self._stabilize_timeline(index)
        self._refresh_compatibility_views()
        return self._branch(index).coherence

    def resolve_paradox(
        self, event: TemporalEvent, timeline_idx: int | None = None,
    ) -> TemporalEvent | None:
        """Validate and, where sound, defer a paradoxical event."""
        index = self.active_timeline if timeline_idx is None else timeline_idx
        violation = self._causal_violation(event, self._branch(index))
        return event.clone() if violation is None else self._resolve_violation(event, violation, index)

    def dump_state(self) -> dict[str, object]:
        """Compatibility alias for a complete in-memory snapshot."""
        return self.export_state()

    def export_state(self) -> dict[str, object]:
        """Export all identity-bearing and evolution-bearing engine state."""
        with self._lock:
            payload = {
                "schema": STATE_SCHEMA, "version": STATE_VERSION,
                "config": {
                    "breath_frequency": self.breath_frequency,
                    "max_recursion_depth": self.max_recursion_depth,
                    "num_dimensions": self.num_dimensions,
                    "ethical_dimensions": self.ethical_dimensions,
                    "auto_stabilize": self.auto_stabilize, "seed": self.seed,
                    "harmonic_modes": self.harmonic_modes,
                    "coupling_strength": self.coupling_strength,
                },
                "master_tick": self.master_tick, "phase": self.phase,
                "active_timeline": self.active_timeline, "sequence": self._sequence,
                "closed": self._closed,
                "branches": [branch.to_dict() for branch in self.branches],
                "entanglement_matrix": self.entanglement_matrix.tolist(),
                "metrics": dict(self.metrics),
                "metric_state": {
                    "sampling_rate": self.metrics_tracker.sampling_rate,
                    "coherence_history": list(self.metrics_tracker.coherence_history),
                    "divergence_history": list(self.metrics_tracker.divergence_history),
                    "paradox_count": self.metrics_tracker.paradox_count,
                    "branch_count": self.metrics_tracker.branch_count,
                    "merge_count": self.metrics_tracker.merge_count,
                    "events_processed": self.metrics_tracker.events_processed,
                    "recursion_depth": self.metrics_tracker.recursion_depth,
                    "runtime_ns": self.metrics_tracker.runtime_ns,
                    "last_update": self.metrics_tracker.last_update,
                },
            }
            safe = _json_safe(payload)
            assert isinstance(safe, dict)
            safe["integrity"] = _stable_digest(safe)
            return safe

    @classmethod
    def from_state(cls, snapshot: Mapping[str, object]) -> TimelineEngine:
        """Construct an engine transactionally from a validated snapshot."""
        data = copy.deepcopy(dict(snapshot))
        integrity = data.pop("integrity", None)
        if data.get("schema") != STATE_SCHEMA or int(data.get("version", -1)) != STATE_VERSION:
            raise SerializationError("unsupported timeline snapshot schema/version")
        if integrity is not None and str(integrity) != _stable_digest(data):
            raise SerializationError("timeline snapshot integrity check failed")
        try:
            config = dict(data["config"])
            engine = cls(parallel_timelines=1, **config)  # type: ignore[arg-type]
            branches = [TemporalBranch.from_dict(item) for item in data["branches"]]
            if not branches:
                raise SerializationError("snapshot contains no temporal worlds")
            ids = [branch.id for branch in branches]
            if len(ids) != len(set(ids)):
                raise SerializationError("duplicate branch identity")
            engine.branches = branches
            engine._branch_by_id = {branch.id: i for i, branch in enumerate(branches)}
            for branch in branches:
                if branch.parent_id is not None and branch.parent_id not in engine._branch_by_id:
                    raise SerializationError("branch parent is absent")
                if branch.state_vector.size != engine.num_dimensions:
                    raise SerializationError("branch state geometry mismatch")
                if branch.ethical_state.size != engine.ethical_dimensions:
                    raise SerializationError("branch ethical geometry mismatch")
                if branch.harmonic_phases.size != engine.harmonic_modes:
                    raise SerializationError("branch harmonic geometry mismatch")
            matrix = np.asarray(data["entanglement_matrix"], dtype=np.float64)
            if matrix.shape != (len(branches), len(branches)) or not np.all(np.isfinite(matrix)):
                raise SerializationError("invalid entanglement geometry")
            if not np.allclose(matrix, matrix.T, atol=1e-12) or not np.allclose(np.diag(matrix), 1):
                raise SerializationError("entanglement matrix violates symmetry")
            engine.entanglement_matrix = np.clip(matrix, 0.0, 1.0)
            engine.master_tick = int(data.get("master_tick", 0))
            engine.phase = float(data.get("phase", 0.0))
            engine.active_timeline = int(data.get("active_timeline", 0))
            engine._branch(engine.active_timeline)
            engine._sequence = int(data.get("sequence", 0))
            engine._closed = bool(data.get("closed", False))
            engine.metrics.update({
                key: int(value) for key, value in dict(data.get("metrics", {})).items()
                if key in engine.metrics
            })
            metric_state = dict(data.get("metric_state", {}))
            engine.metrics_tracker = TimelineMetrics(
                sampling_rate=int(metric_state.get("sampling_rate", 256)),
            )
            engine.metrics_tracker.coherence_history.extend(
                float(value) for value in metric_state.get("coherence_history", [])
            )
            engine.metrics_tracker.divergence_history.extend(
                float(value) for value in metric_state.get("divergence_history", [])
            )
            for name in (
                "paradox_count", "branch_count", "merge_count", "events_processed",
                "recursion_depth", "runtime_ns",
            ):
                setattr(engine.metrics_tracker, name, int(metric_state.get(name, 0)))
            engine.metrics_tracker.last_update = float(
                metric_state.get("last_update", engine.metrics_tracker.last_update)
            )
            engine._refresh_compatibility_views()
            return engine
        except (KeyError, TypeError, ValueError, TemporalConstraintError) as exc:
            if isinstance(exc, SerializationError):
                raise
            raise SerializationError("invalid timeline engine snapshot") from exc

    def restore_state(self, snapshot: Mapping[str, object]) -> None:
        """Replace engine state only after complete snapshot validation."""
        restored = type(self).from_state(snapshot)
        with self._lock:
            observers = self._observers
            lock = self._lock
            self.__dict__.update(restored.__dict__)
            self._lock = self.sync_lock = lock
            self._observers = self.observers = observers

    def save_state(self, path: str | os.PathLike[str]) -> Path:
        """Atomically persist a complete JSON snapshot."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.{uuid.uuid4().hex}.tmp")
        try:
            with temporary.open("x", encoding="utf-8") as handle:
                json.dump(self.export_state(), handle, sort_keys=True, separators=(",", ":"))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
            try:
                directory_fd = os.open(destination.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                pass
            return destination
        finally:
            if temporary.exists():
                temporary.unlink()

    @classmethod
    def load_state(cls, path: str | os.PathLike[str]) -> TimelineEngine:
        """Load and validate an atomic JSON snapshot."""
        try:
            with Path(path).open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise SerializationError("unable to load timeline snapshot") from exc
        if not isinstance(data, Mapping):
            raise SerializationError("snapshot root must be an object")
        return cls.from_state(data)

    @property
    def is_active(self) -> bool:
        """Return whether this engine accepts evolution operations."""
        return not self._closed

    def close(self) -> None:
        """Stop future evolution while preserving inspectable state."""
        with self._lock:
            self._closed = True

    def __enter__(self) -> TimelineEngine:
        """Enter a managed engine lifetime."""
        if self._closed:
            raise TimelineError("timeline engine is closed")
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        """Close the engine at managed-lifetime exit."""
        self.close()


def initialize(
    engine: TimelineEngine | None = None, **kwargs: object,
) -> TimelineEngine:
    """Create an engine, or validate and return an existing compatible engine."""
    if engine is not None:
        if kwargs:
            raise TemporalConstraintError("cannot reconfigure an existing engine", "configuration")
        if not isinstance(engine, TimelineEngine):
            raise TemporalConstraintError("engine must be TimelineEngine", "configuration")
        return engine
    return TimelineEngine(**kwargs)  # type: ignore[arg-type]


def test_observer(event: TemporalEvent, timeline_idx: int) -> None:
    """Minimal no-op observer retained for compatibility and examples."""
    del event, timeline_idx


__all__ = [
    "BreathPhase", "BranchStatus", "CausalViolation", "MergeReport",
    "ParadoxKind", "QuantumDecoherenceError", "RealityFragmentationError",
    "SerializationError", "TemporalBranch", "TemporalConstraintError",
    "TemporalEvent", "TimelineEngine", "TimelineError", "TimelineMetrics",
    "initialize", "test_observer",
]
