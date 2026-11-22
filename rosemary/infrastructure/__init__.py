# infrastructure/__init__.py
"""
Infrastructure Package

Provides observability, security, scalability, and ethical components.
"""

from .observability import (
    ObservabilityEngine,
    log_event,
    log_error,
    log_exception,
    log_metric,
    log_trace,
    register_exception_class,
)

from .security import AccessControlEngine, SecurityLevel
# scalability.py defines ScalabilityEngine and LoadBalancer; no ScalabilityManager exists.
from .scalability import ScalabilityEngine, LoadBalancer
# ethical_tensor.py defines no class named EthicalTensor (that name exists only in
# lqt/original-py-code as an nn.Module). Export what the module actually defines;
# `from rosemary.infrastructure import EthicalTensor` raises ImportError.
from .ethical_tensor import (
    BreathPhase,
    CollapseAdapter,
    EthicalTensorFactory,
    SymbolicQuantumState,
    create_ethical_tensor,
    apply_ethical_force,
    analyze_ethical_distribution,
)

__all__ = [
    "ObservabilityEngine",
    "log_event",
    "log_error",
    "log_exception",
    "log_metric",
    "log_trace",
    "register_exception_class",
    "AccessControlEngine",
    "SecurityLevel",
    "ScalabilityEngine",
    "LoadBalancer",
    "BreathPhase",
    "CollapseAdapter",
    "EthicalTensorFactory",
    "SymbolicQuantumState",
    "create_ethical_tensor",
    "apply_ethical_force",
    "analyze_ethical_distribution",
]
