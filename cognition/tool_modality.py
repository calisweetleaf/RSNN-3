"""
Universal Tool and External Control Output Head (Canonical Muad'Dib v3 Edition)

Production-grade typed tool action emission, autonomous tool synthesis,
deterministic Set-of-Mark visual attention grounding, DocDB v1.5.0+ persistent
genome/system memory, and universal 8-domain system control reconciled onto
Muad'Dib's single canonical Transformer backbone (transformer_backbone.py +
neural_config.py at d_model=512).

Source: Sovereign MCP Server - Muad'Dib Neural Substrate
Modified: 2026-11-11
Modified by: daeron
Justification: Completed all 8 ControlDomain heads (Digital, Mechanical, Analog,
    Electromagnetic, Optical, Chemical, Biological, Quantum) and profile/constraint/
    objective conditioning without erasing any original architecture; wired
    DocDBToolMemoryAdapter directly to in-process DocDB v1.5.0+ (docdb.sqlite WAL +
    Somnus 2.2.0 URNs + 512-D embeddings); added DeterministicVisualAttentionBridge
    over visual_tool.py Set-of-Mark UI grounding; added differentiable forward();
    and exposed ToolModalityOrgan with 6 compiled bb7_tm_* intelligence surfaces.
Provenance: SCOPE.md (mode: EDIT)
Files: muadib/tool_modality.py
"""

from __future__ import annotations

import asyncio
import collections
import concurrent.futures
import contextlib
import hashlib
import json
import logging
import math
import os
from pathlib import Path
import queue
import sqlite3
import struct
import threading
import time
from collections import defaultdict, deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F

from .neural_config import AeronRMSNorm, NeuralNetConfig
from .transformer_backbone import (
    CanonicalBackboneDecoder,
    CanonicalBackboneEncoder,
    MultiHeadAttention,
    NeuralMemoryNetwork,
)

logger = logging.getLogger(__name__)


def _resolve_sovereign_data_dir(explicit_dir: Optional[Union[str, Path]] = None) -> Path:
    """Resolve canonical SOVEREIGN_DATA_DIR without CWD brain-forking."""
    if explicit_dir is not None and str(explicit_dir).strip():
        resolved = Path(explicit_dir).expanduser().resolve()
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved
    for env_key in ("SOMNUS_DATA_DIR", "SOVEREIGN_DATA_DIR", "MUADDIB_DATA_DIR"):
        env_val = os.environ.get(env_key, "").strip()
        if env_val:
            resolved = Path(env_val).expanduser().resolve()
            resolved.mkdir(parents=True, exist_ok=True)
            return resolved
    default_sovereign = Path("/home/daeron/Somnus-MCP/data")
    try:
        default_sovereign.mkdir(parents=True, exist_ok=True)
        return default_sovereign
    except OSError as exc:
        logger.error("Fallback from %s due to OSError: %s", default_sovereign, exc)
        fallback = Path(__file__).resolve().parent.parent / "data"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


class BB7Response(str):
    """
    Dual-surface string subclass carrying tensor-ready structured evidence,
    provenance, and SQLite/DocDB context for Muad'Dib modality heads while
    remaining a drop-in str (and awaitable) for legacy callers.
    """

    structured: Dict[str, Any]
    evidence: List[Any]
    sql_context: Dict[str, Any]
    tool_name: str
    modality: str

    def __new__(
        cls,
        narrative: str,
        *,
        structured: Optional[Dict[str, Any]] = None,
        evidence: Optional[List[Any]] = None,
        sql_context: Optional[Dict[str, Any]] = None,
        tool_name: str = "tool_modality",
        modality: str = "tool",
    ) -> "BB7Response":
        """Construct a dual-surface BB7Response envelope."""
        instance = super().__new__(cls, narrative)
        instance.structured = dict(structured or {})
        instance.evidence = list(evidence or [])
        instance.sql_context = dict(sql_context or {})
        instance.tool_name = str(tool_name or "tool_modality")
        instance.modality = str(modality or "tool")
        return instance

    def __await__(self) -> Iterator["BB7Response"]:
        """Allow both synchronous and awaited invocation semantics."""
        async def _coro() -> "BB7Response":
            return self

        return _coro().__await__()

    def to_envelope(self) -> Dict[str, Any]:
        """Serialize canonical structured observation envelope for neural projection."""
        return {
            "tool_name": self.tool_name,
            "modality": self.modality,
            "narrative": str(self),
            "structured": self.structured,
            "evidence": self.evidence,
            "sql_context": self.sql_context,
        }


def _ensure_seq3d(x: torch.Tensor) -> torch.Tensor:
    """Normalize 1D [d], 2D [s, d], or 3D [b, s, d] tensors to [b, s, d]."""
    if x.dim() == 1:
        return x.unsqueeze(0).unsqueeze(0)
    if x.dim() == 2:
        return x.unsqueeze(0)
    return x


def _pool_2d(x: torch.Tensor) -> torch.Tensor:
    """Pool [d], [s, d], or [b, s, d] tensors to [b, d] (with b=1 for unbatched)."""
    seq3d = _ensure_seq3d(x)
    return seq3d.mean(dim=1)


def _hash_token_to_vec(
    text: str,
    dim: int,
    device: torch.device,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """Deterministically project text into an L2-normalized R^dim spectral vector."""
    vec = torch.zeros(dim, dtype=torch.float32, device=device)
    cleaned = (text or "empty").strip().lower()
    tokens = cleaned.split() or [cleaned]
    for tok_idx, tok in enumerate(tokens[:32]):
        for salt in range(4):
            digest = hashlib.blake2b(
                f"{tok}:{tok_idx}:{salt}".encode("utf-8"), digest_size=8
            ).digest()
            hv = int.from_bytes(digest, "little")
            bucket = hv % dim
            sign = 1.0 if ((hv >> 32) & 1) == 0 else -1.0
            vec[bucket] += sign / math.sqrt(float(tok_idx + 1))
    return F.normalize(vec, p=2, dim=-1, eps=1e-6).to(dtype=dtype)


def _text_to_canonical_sequence(
    text: str,
    d_model: int = 512,
    seq_len: int = 8,
    device: Optional[torch.device] = None,
) -> torch.Tensor:
    """Project natural-language intent/objective text into [1, seq_len, d_model=512]."""
    dev = device or torch.device("cpu")
    words = [w for w in (text or "autonomous_operation").strip().split() if w]
    if not words:
        words = ["autonomous_operation"]
    eff_len = max(1, min(seq_len, len(words)))
    chunk_sz = max(1, math.ceil(len(words) / eff_len))
    rows: List[torch.Tensor] = []
    for pos in range(eff_len):
        segment = " ".join(words[pos * chunk_sz : (pos + 1) * chunk_sz]) or words[-1]
        base = _hash_token_to_vec(f"pos:{pos}:{segment}", d_model, dev)
        angle = float(pos + 1) / float(eff_len)
        base[0] = math.sin(angle * math.pi)
        base[1] = math.cos(angle * math.pi)
        rows.append(base * math.sqrt(float(d_model) * 0.25))
    return torch.stack(rows, dim=0).unsqueeze(0)


class ActionKind(Enum):
    """Typed action classes emitted by TypedToolActionHead."""

    REGISTERED_TOOL = "registered_tool"
    SHELL_COMMAND = "shell_command"
    STRUCTURED_OUTPUT = "structured_output"
    ABSTAIN = "abstain"

class OperationMode(Enum):
    """High-level execution modes for UniversalToolControlOutputHead."""

    TOOL_SYNTHESIS = auto()
    EXTERNAL_CONTROL = auto()
    HYBRID_OPERATION = auto()
    AUTONOMOUS_DISCOVERY = auto()

class ControlDomain(Enum):
    """Physical and computational control domains supported by Muad'Dib."""

    DIGITAL = auto()
    ANALOG = auto()
    MECHANICAL = auto()
    ELECTROMAGNETIC = auto()
    OPTICAL = auto()
    CHEMICAL = auto()
    BIOLOGICAL = auto()
    QUANTUM = auto()

class FunctionCallMode(Enum):
    """Callable invocation surfaces for synthesized or registered operations."""

    STANDARD = auto()
    PLUGIN_API = auto()
    CODE_EXECUTION = auto()
    SYSTEM_INTEGRATION = auto()
    AUTONOMOUS_SYNTHESIS = auto()

@dataclass
class UniversalControlConfig:
    """Runtime and conditioning configuration for UniversalToolControlOutputHead."""

    operation_mode: OperationMode = OperationMode.HYBRID_OPERATION
    max_parameters: int = 100
    timeout_seconds: float = 300.0
    memory_limit_mb: int = 16384
    parameter_validation: bool = True
    signature_verification: bool = True
    memory_conditioning_weight: float = 0.3
    reasoning_conditioning_weight: float = 0.5
    visual_conditioning_weight: float = 0.35
    enable_streaming: bool = True
    use_fp16: bool = True
    max_concurrent_systems: int = 50
    safety_threshold: float = 0.95
    auto_discovery: bool = True
    persist_to_docdb: bool = True
    learning_rate: float = 1e-4
    evolution_cycles: int = 1000

@dataclass
class SystemProfile:
    """Discovered external/internal capability system profile."""

    system_id: str
    system_type: str
    capabilities: Dict[str, Any]
    interfaces: List[str]
    control_domains: List[ControlDomain]
    safety_constraints: Dict[str, Any]
    communication_protocols: List[str]
    resource_requirements: Dict[str, float]
    reliability_score: float
    last_updated: float
    somnus_urn: Optional[str] = None
    docdb_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize SystemProfile for DocDB persistence and BB7Response envelopes."""
        return {
            "system_id": self.system_id,
            "system_type": self.system_type,
            "capabilities": dict(self.capabilities),
            "interfaces": list(self.interfaces),
            "control_domains": [d.name for d in self.control_domains],
            "safety_constraints": dict(self.safety_constraints),
            "communication_protocols": list(self.communication_protocols),
            "resource_requirements": dict(self.resource_requirements),
            "reliability_score": float(self.reliability_score),
            "last_updated": float(self.last_updated),
            "somnus_urn": self.somnus_urn,
            "docdb_id": self.docdb_id,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "SystemProfile":
        """Reconstruct a SystemProfile from DocDB JSON metadata."""
        raw_domains = payload.get("control_domains", ["DIGITAL"])
        domains: List[ControlDomain] = []
        for item in raw_domains:
            if isinstance(item, ControlDomain):
                domains.append(item)
            elif isinstance(item, str) and item in ControlDomain.__members__:
                domains.append(ControlDomain[item])
        return cls(
            system_id=str(payload["system_id"]),
            system_type=str(payload.get("system_type", "simple_system")),
            capabilities=dict(payload.get("capabilities", {})),
            interfaces=list(payload.get("interfaces", [])),
            control_domains=domains or [ControlDomain.DIGITAL],
            safety_constraints=dict(payload.get("safety_constraints", {})),
            communication_protocols=list(payload.get("communication_protocols", ["generic"])),
            resource_requirements=dict(payload.get("resource_requirements", {})),
            reliability_score=float(payload.get("reliability_score", 0.5)),
            last_updated=float(payload.get("last_updated", time.time())),
            somnus_urn=payload.get("somnus_urn"),
            docdb_id=payload.get("docdb_id"),
        )

@dataclass
class ToolGenome:
    """Synthesized or evolved compositional tool genome in d_model=512 space."""

    genome_id: str
    functionality_vector: torch.Tensor
    complexity_score: float
    efficiency_rating: float
    safety_rating: float
    usage_count: int
    success_rate: float
    evolution_generation: int
    parent_genomes: List[str]
    created_timestamp: float
    implementation_blueprint: Optional[Dict[str, Any]] = None
    somnus_urn: Optional[str] = None
    docdb_id: Optional[int] = None

    def to_dict(self, include_vector: bool = False) -> Dict[str, Any]:
        """Serialize ToolGenome metadata (and optional 512-D vector) for DocDB."""
        data: Dict[str, Any] = {
            "genome_id": self.genome_id,
            "vector_dim": int(self.functionality_vector.numel()),
            "vector_norm": round(float(self.functionality_vector.detach().norm().item()), 4),
            "complexity_score": round(float(self.complexity_score), 4),
            "efficiency_rating": round(float(self.efficiency_rating), 4),
            "safety_rating": round(float(self.safety_rating), 4),
            "usage_count": int(self.usage_count),
            "success_rate": round(float(self.success_rate), 4),
            "evolution_generation": int(self.evolution_generation),
            "parent_genomes": list(self.parent_genomes),
            "created_timestamp": float(self.created_timestamp),
            "implementation_blueprint": dict(self.implementation_blueprint or {}),
            "somnus_urn": self.somnus_urn,
            "docdb_id": self.docdb_id,
        }
        if include_vector:
            data["functionality_vector"] = [
                round(float(x), 6) for x in self.functionality_vector.detach().cpu().tolist()
            ]
        return data

    @classmethod
    def from_dict(
        cls,
        payload: Dict[str, Any],
        vector_override: Optional[torch.Tensor] = None,
        d_model: int = 512,
    ) -> "ToolGenome":
        """Reconstruct a ToolGenome from DocDB metadata + 512-D embedding blob."""
        if vector_override is not None:
            vec = vector_override.detach().clone().to(dtype=torch.float32).view(-1)
        elif isinstance(payload.get("functionality_vector"), list) and payload["functionality_vector"]:
            vec = torch.tensor(payload["functionality_vector"], dtype=torch.float32)
        else:
            vec = _hash_token_to_vec(str(payload.get("genome_id", "genome")), d_model, torch.device("cpu"))
        return cls(
            genome_id=str(payload["genome_id"]),
            functionality_vector=vec,
            complexity_score=float(payload.get("complexity_score", 0.5)),
            efficiency_rating=float(payload.get("efficiency_rating", 0.5)),
            safety_rating=float(payload.get("safety_rating", 0.5)),
            usage_count=int(payload.get("usage_count", 0)),
            success_rate=float(payload.get("success_rate", 0.0)),
            evolution_generation=int(payload.get("evolution_generation", 1)),
            parent_genomes=list(payload.get("parent_genomes", [])),
            created_timestamp=float(payload.get("created_timestamp", time.time())),
            implementation_blueprint=payload.get("implementation_blueprint"),
            somnus_urn=payload.get("somnus_urn"),
            docdb_id=payload.get("docdb_id"),
        )


def _encode_system_profile_vec(
    profile: Optional[SystemProfile],
    hidden_size: int,
    device: torch.device,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """Encode a SystemProfile into a [1, hidden_size] conditioning vector."""
    vec = torch.zeros(hidden_size, dtype=torch.float32, device=device)
    if profile is None:
        return vec.unsqueeze(0).to(dtype=dtype)
    sig = f"sys:{profile.system_id}:{profile.system_type}:{'|'.join(profile.communication_protocols)}"
    base = _hash_token_to_vec(sig, hidden_size, device)
    vec = base * (0.5 + 0.5 * float(profile.reliability_score))
    for dom in profile.control_domains:
        idx = (dom.value - 1) % hidden_size
        vec[idx] += 0.35
    res_req = profile.resource_requirements or {}
    if hidden_size >= 8:
        vec[0] += float(profile.reliability_score)
        vec[1] += min(1.0, float(res_req.get("cpu_usage", 0.1)))
        vec[2] += min(1.0, float(res_req.get("memory_mb", 64.0)) / 1024.0)
        vec[3] += min(1.0, float(res_req.get("power_watts", 5.0)) / 100.0)
    return F.normalize(vec, p=2, dim=-1, eps=1e-6).unsqueeze(0).to(dtype=dtype)


def _encode_safety_constraints_scale(safety_constraints: Optional[Dict[str, Any]]) -> float:
    """Compute a bounded modulation factor in [0.25, 1.0] from safety_constraints."""
    if not safety_constraints:
        return 1.0
    max_risk = float(safety_constraints.get("max_risk_level", 0.9))
    emergency_stop = bool(safety_constraints.get("emergency_stop_required", False))
    scale = max(0.25, min(1.0, max_risk))
    if emergency_stop:
        scale *= 0.85
    return round(scale, 4)

class GraphNeuralNetwork(nn.Module):
    """Graph Neural Network for system topology mapping"""
    
    def __init__(self, hidden_size: int, num_layers: int = 4):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.node_embedder = nn.Linear(hidden_size, hidden_size)
        self.edge_embedder = nn.Linear(hidden_size, hidden_size)
        
        self.gnn_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size * 2, hidden_size),
                nn.ReLU(),
                nn.Linear(hidden_size, hidden_size),
                nn.LayerNorm(hidden_size)
            ) for _ in range(num_layers)
        ])
        
        self.output_projector = nn.Linear(hidden_size, hidden_size)
    
    def forward(self, node_features: torch.Tensor, edge_indices: torch.Tensor, 
                edge_features: torch.Tensor) -> torch.Tensor:
        
        h = self.node_embedder(node_features)
        edge_h = self.edge_embedder(edge_features)
        
        for layer in self.gnn_layers:
            h_updated = h.clone()
            
            for i in range(edge_indices.shape[0]):
                src, dst = edge_indices[i]
                edge_feat = edge_h[i]
                
                combined = torch.cat([h[src], edge_feat], dim=-1)
                update = layer(combined)
                h_updated[dst] = h_updated[dst] + update
            
            h = h_updated
        
        return self.output_projector(h)

class SystemDiscoveryEngine(nn.Module):
    """Autonomous system discovery and profiling on canonical Muad'Dib backbone."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize SystemDiscoveryEngine using NeuralNetConfig (d_model=512)."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.fingerprint_analyzer = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.LayerNorm(1024),
            nn.ReLU(),
            nn.Linear(1024, 2048)
        )
        
        self.capability_predictor = CanonicalBackboneEncoder(self.config, num_layers=2)
        
        self.interface_detector = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 500),
            nn.Sigmoid()
        )
        
        self.topology_mapper = GraphNeuralNetwork(self.hidden_size, 4)
        
        self.reliability_assessor = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
        
        self.discovered_systems: Dict[str, SystemProfile] = {}
        self.discovery_history: deque = deque(maxlen=10000)
    
    def discover_system(self, probe_data: torch.Tensor) -> SystemProfile:
        """Profile a target capability/system from probe representation tensor."""
        with torch.no_grad():
            pooled = _pool_2d(probe_data).squeeze(0)
            seq3d = _ensure_seq3d(probe_data)
            fingerprint = self.fingerprint_analyzer(pooled)
            capabilities = self.capability_predictor(seq3d).mean(dim=1).squeeze(0)
            interfaces = self.interface_detector(pooled)
            reliability = self.reliability_assessor(pooled)
            
            system_id = hashlib.sha256(fingerprint.cpu().numpy().tobytes()).hexdigest()[:16]
            
            capability_indices = torch.where(capabilities > 0.5)[0]
            capabilities_dict = {f"capability_{i.item()}": capabilities[i].item() 
                               for i in capability_indices}
            
            interface_indices = torch.where(interfaces > 0.7)[0]
            interface_list = [f"interface_{i.item()}" for i in interface_indices]
            
            control_domains = self._infer_control_domains(capabilities)
            
            profile = SystemProfile(
                system_id=system_id,
                system_type=self._classify_system_type(fingerprint),
                capabilities=capabilities_dict,
                interfaces=interface_list,
                control_domains=control_domains,
                safety_constraints=self._generate_safety_constraints(fingerprint),
                communication_protocols=self._detect_protocols(interfaces),
                resource_requirements=self._estimate_resource_requirements(capabilities),
                reliability_score=reliability.item(),
                last_updated=time.time()
            )
            
            self.discovered_systems[system_id] = profile
            self.discovery_history.append(profile)
            
            return profile
    
    def _infer_control_domains(self, capabilities: torch.Tensor) -> List[ControlDomain]:
        """Infer active ControlDomains across all 8 canonical 64-D capability slices."""
        domains: List[ControlDomain] = []
        cap_values = capabilities.squeeze(0) if capabilities.dim() > 1 else capabilities
        total_dim = int(cap_values.numel())
        domain_order = list(ControlDomain)
        slice_width = max(1, total_dim // len(domain_order))

        for idx, dom in enumerate(domain_order):
            start = idx * slice_width
            end = total_dim if idx == len(domain_order) - 1 else min(total_dim, (idx + 1) * slice_width)
            if start < end and torch.sigmoid(cap_values[start:end]).mean().item() > 0.56:
                domains.append(dom)

        return domains if domains else [ControlDomain.DIGITAL]

    def map_system_topology(self, profiles: Sequence[SystemProfile]) -> Optional[torch.Tensor]:
        """Map inter-system topology over discovered SystemProfiles via GraphNeuralNetwork."""
        if not profiles:
            return None
        device = next(self.parameters()).device
        node_vecs = torch.stack(
            [_encode_system_profile_vec(p, self.hidden_size, device).squeeze(0) for p in profiles]
        )
        if len(profiles) == 1:
            return self.topology_mapper.output_projector(self.topology_mapper.node_embedder(node_vecs))
        pairs = [[i, j] for i in range(len(profiles)) for j in range(len(profiles)) if i != j]
        edge_indices = torch.tensor(pairs, dtype=torch.long, device=device)
        edge_features = torch.stack(
            [0.5 * (node_vecs[i] + node_vecs[j]) for i, j in pairs]
        )
        return self.topology_mapper(node_vecs, edge_indices, edge_features)
    
    def _classify_system_type(self, fingerprint: torch.Tensor) -> str:
        fp_mean = fingerprint.mean().item()
        if fp_mean > 0.8:
            return "high_complexity_system"
        elif fp_mean > 0.5:
            return "medium_complexity_system"
        else:
            return "simple_system"
    
    def _generate_safety_constraints(self, fingerprint: torch.Tensor) -> Dict[str, Any]:
        return {
            "max_power": min(100.0, fingerprint[:10].sum().item()),
            "max_temperature": min(85.0, fingerprint[10:20].sum().item() * 10),
            "max_voltage": min(24.0, fingerprint[20:30].sum().item() * 5),
            "emergency_stop_required": fingerprint[30:40].sum().item() > 5.0
        }
    
    def _detect_protocols(self, interfaces: torch.Tensor) -> List[str]:
        protocols = []
        interface_values = interfaces
        
        protocol_mapping = {
            "i2c": 0, "spi": 1, "uart": 2, "can": 3, "ethernet": 4,
            "wifi": 5, "bluetooth": 6, "lora": 7, "modbus": 8, "tcp": 9
        }
        
        for protocol, idx in protocol_mapping.items():
            if idx < len(interface_values) and interface_values[idx] > 0.8:
                protocols.append(protocol)
        
        return protocols if protocols else ["generic"]
    
    def _estimate_resource_requirements(self, capabilities: torch.Tensor) -> Dict[str, float]:
        cap_sum = capabilities.sum().item()
        return {
            "cpu_usage": min(1.0, cap_sum / 1000),
            "memory_mb": min(1024.0, cap_sum * 10),
            "bandwidth_mbps": min(100.0, cap_sum / 10),
            "power_watts": min(50.0, cap_sum / 20)
        }

class InterfaceAdaptationEngine(nn.Module):
    """Adapt to communication interfaces dynamically using canonical dimensions."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize InterfaceAdaptationEngine using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.protocol_learner = nn.LSTM(
            self.hidden_size, self.hidden_size,
            num_layers=2, batch_first=True, bidirectional=True
        )
        
        self.signal_encoder = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.LayerNorm(1024),
            nn.ReLU(),
            nn.Linear(1024, 2048)
        )
        
        self.signal_decoder = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Linear(512, self.hidden_size)
        )
        
        self.timing_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        
        self.error_corrector = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.hidden_size)
        )
        
        self.adaptation_memory: Dict[str, Any] = {}
        self.protocol_cache: Dict[str, Any] = {}
    
    def adapt_interface(self, system_profile: SystemProfile, 
                       hidden_states: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Adapt interface signaling for system_profile given 2D or 3D hidden_states."""
        protocol_context = _ensure_seq3d(hidden_states)
        pooled = _pool_2d(hidden_states)
        protocol_output, _ = self.protocol_learner(protocol_context)
        encoded_signals = self.signal_encoder(protocol_context)
        timing_params = self.timing_controller(pooled)
        error_correction = self.error_corrector(pooled)
        
        adaptation_result = {
            'protocol_adaptation': protocol_output.squeeze(0),
            'encoded_signals': encoded_signals.squeeze(0),
            'timing_parameters': timing_params,
            'error_correction': error_correction,
            'interface_ready': True
        }
        
        self.adaptation_memory[system_profile.system_id] = adaptation_result
        return adaptation_result
    
    def decode_response(self, response_data: torch.Tensor) -> torch.Tensor:
        """Decode interface signal back into d_model hidden space."""
        return self.signal_decoder(response_data)

class ToolSynthesisEngine(nn.Module):
    """Generate compositional tool genomes using CanonicalBackboneDecoder."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize ToolSynthesisEngine using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.tool_genome_generator = nn.Sequential(
            nn.Linear(self.hidden_size, self.hidden_size * 2),
            nn.ReLU(),
            nn.Linear(self.hidden_size * 2, self.hidden_size),
            nn.LayerNorm(self.hidden_size),
            nn.ReLU(),
            nn.Linear(self.hidden_size, self.hidden_size)
        )
        
        self.capability_composer = CanonicalBackboneDecoder(self.config, num_layers=2)
        self.mutation_projector = nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        
        self.implementation_synthesizer = nn.Sequential(
            nn.Linear(self.hidden_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.ReLU(),
            nn.Linear(2048, 4096)
        )
        
        self.validation_predictor = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
        
        self.complexity_estimator = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        self.tool_genome_registry: Dict[str, ToolGenome] = {}
        self.synthesis_history: deque = deque(maxlen=50000)
    
    @staticmethod
    def _decode_implementation_blueprint(impl_vec: torch.Tensor) -> Dict[str, Any]:
        """Decode the 4096-D implementation synthesizer vector into an executable blueprint."""
        flat = impl_vec.detach().view(-1)
        arity = max(1, min(12, int(round(torch.sigmoid(flat[:16].mean()).item() * 8.0)) + 1))
        call_modes = list(FunctionCallMode)
        mode_scores = torch.stack(
            [flat[32 + i * 32 : 32 + (i + 1) * 32].mean() for i in range(len(call_modes))]
        )
        selected_call_mode = call_modes[int(torch.argmax(mode_scores).item())].name.lower()
        dom_list = list(ControlDomain)
        dom_scores = F.softmax(
            torch.stack([flat[256 + i * 64 : 256 + (i + 1) * 64].mean() for i in range(len(dom_list))]),
            dim=0,
        )
        top_dom = dom_list[int(torch.argmax(dom_scores).item())].name
        return {
            "call_mode": selected_call_mode,
            "parameter_arity": arity,
            "prefer_parallel": bool(torch.sigmoid(flat[16:24].mean()).item() > 0.5),
            "idempotent_score": round(float(torch.sigmoid(flat[24:32].mean()).item()), 4),
            "verification_gate_weight": round(float(torch.sigmoid(flat[768:832].mean()).item()), 4),
            "timeout_budget_s": round(5.0 + 55.0 * float(torch.sigmoid(flat[832:896].mean()).item()), 2),
            "primary_domain_affinity": top_dom,
            "blueprint_sha16": hashlib.blake2b(
                flat[:256].cpu().numpy().tobytes(), digest_size=8
            ).hexdigest(),
        }

    def synthesize_tool(self, requirement_context: torch.Tensor,
                       existing_tools: Optional[List[ToolGenome]] = None) -> ToolGenome:
        """Synthesize a ToolGenome from requirement_context and optional parent genomes."""
        pooled = _pool_2d(requirement_context)
        genome_vector = self.tool_genome_generator(pooled)
        
        if existing_tools:
            dev = genome_vector.device
            existing_genomes = torch.stack(
                [tool.functionality_vector.to(device=dev, dtype=genome_vector.dtype) for tool in existing_tools]
            ).unsqueeze(0)
            composed = self.capability_composer(
                genome_vector.unsqueeze(1),
                existing_genomes
            )
            genome_vector = composed.mean(dim=1)
        
        impl_vec = self.implementation_synthesizer(genome_vector)
        blueprint = self._decode_implementation_blueprint(impl_vec)
        validation_score = self.validation_predictor(genome_vector)
        complexity_score = self.complexity_estimator(genome_vector)
        
        vec_1d = F.normalize(genome_vector[0], p=2, dim=-1, eps=1e-6)
        genome_id = hashlib.sha256(vec_1d.detach().cpu().numpy().tobytes()).hexdigest()[:16]
        
        tool_genome = ToolGenome(
            genome_id=genome_id,
            functionality_vector=vec_1d,
            complexity_score=complexity_score[0].item(),
            efficiency_rating=round(1.0 - 0.35 * complexity_score[0].item(), 4),
            safety_rating=validation_score[0].item(),
            usage_count=0,
            success_rate=0.0,
            evolution_generation=max((t.evolution_generation for t in (existing_tools or [])), default=0) + 1,
            parent_genomes=[tool.genome_id for tool in existing_tools] if existing_tools else [],
            created_timestamp=time.time(),
            implementation_blueprint=blueprint,
        )
        
        self.tool_genome_registry[genome_id] = tool_genome
        self.synthesis_history.append(tool_genome)
        return tool_genome
    
    def evolve_tool(self, base_genome: ToolGenome, 
                   performance_feedback: Dict[str, float]) -> ToolGenome:
        """Deterministically evolve a ToolGenome conditioned on performance feedback."""
        dev = next(self.parameters()).device
        base_vec = base_genome.functionality_vector.to(device=dev, dtype=torch.float32)
        observed_sr = float(performance_feedback.get('success_rate', base_genome.success_rate or 0.5))
        mutation_strength = max(0.05, 1.0 - observed_sr)
        delta = torch.tanh(self.mutation_projector(base_vec)) * mutation_strength * 0.1
        
        evolved_vector = F.normalize(base_vec + delta, dim=0, eps=1e-6)
        impl_vec = self.implementation_synthesizer(evolved_vector.unsqueeze(0))
        blueprint = self._decode_implementation_blueprint(impl_vec)
        validation_score = self.validation_predictor(evolved_vector.unsqueeze(0))
        complexity_score = self.complexity_estimator(evolved_vector.unsqueeze(0))
        
        evolved_id = hashlib.sha256(evolved_vector.detach().cpu().numpy().tobytes()).hexdigest()[:16]
        evolved_genome = ToolGenome(
            genome_id=evolved_id,
            functionality_vector=evolved_vector,
            complexity_score=complexity_score.item(),
            efficiency_rating=min(1.0, base_genome.efficiency_rating * (1.05 + 0.05 * observed_sr)),
            safety_rating=validation_score.item(),
            usage_count=0,
            success_rate=observed_sr,
            evolution_generation=base_genome.evolution_generation + 1,
            parent_genomes=[base_genome.genome_id],
            created_timestamp=time.time(),
            implementation_blueprint=blueprint,
        )
        
        self.tool_genome_registry[evolved_id] = evolved_genome
        self.synthesis_history.append(evolved_genome)
        return evolved_genome

    def record_execution_feedback(
        self,
        genome_id: str,
        *,
        success: bool,
        latency_ms: float = 0.0,
        evolve_below_sr: float = 0.6,
    ) -> Optional[ToolGenome]:
        """Update ToolGenome empirical stats and evolve when reliability lags."""
        genome = self.tool_genome_registry.get(genome_id)
        if genome is None:
            return None
        prev_n = int(genome.usage_count)
        new_n = prev_n + 1
        obs = 1.0 if success else 0.0
        genome.usage_count = new_n
        genome.success_rate = ((genome.success_rate * prev_n) + obs) / float(new_n)
        if latency_ms > 0.0:
            speed_factor = max(0.2, min(1.0, 1000.0 / (1000.0 + float(latency_ms))))
            genome.efficiency_rating = round(0.8 * genome.efficiency_rating + 0.2 * speed_factor, 4)
        if new_n >= 2 and genome.success_rate < evolve_below_sr:
            return self.evolve_tool(genome, {"success_rate": genome.success_rate})
        return genome

class CommandSynthesisEngine(nn.Module):
    """Generate structured commands for target systems on canonical backbone."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize CommandSynthesisEngine using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.structure_learner = CanonicalBackboneEncoder(self.config, num_layers=2)
        
        self.param_optimizer = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.LayerNorm(1024),
            nn.ReLU(),
            nn.Linear(1024, 2048)
        )
        
        self.sequence_planner = nn.LSTM(
            self.hidden_size, self.hidden_size,
            num_layers=2, batch_first=True
        )
        
        self.error_predictor = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 100),
            nn.Softmax(dim=-1)
        )
        
        self.command_validator = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
    
    def synthesize_command(self, system_profile: SystemProfile,
                          objective_context: torch.Tensor,
                          safety_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize profile- and safety-conditioned command parameters and sequence."""
        seq3d = _ensure_seq3d(objective_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, seq3d.device, seq3d.dtype
        ).unsqueeze(1)
        safety_scale = _encode_safety_constraints_scale(safety_constraints)
        conditioned_seq = seq3d + 0.15 * prof_vec
        command_structure = self.structure_learner(conditioned_seq)
        pooled = command_structure.mean(dim=1)
        
        optimized_params = self.param_optimizer(pooled) * safety_scale
        sequence_output, _ = self.sequence_planner(command_structure)
        error_probs = self.error_predictor(pooled)
        safety_score = self.command_validator(pooled)
        sequence_steps = torch.argmax(sequence_output, dim=-1)
        
        return {
            'system_id': system_profile.system_id,
            'command_structure': command_structure.squeeze(0),
            'parameters': self._extract_parameters(optimized_params),
            'execution_sequence': self._plan_execution_sequence(sequence_steps),
            'error_mitigation': self._generate_error_mitigation(error_probs),
            'safety_score': float(safety_score[0].item()) * safety_scale,
            'safety_modulation': safety_scale,
            'estimated_duration': self._estimate_duration(sequence_output),
            'resource_requirements': self._estimate_command_resources(command_structure)
        }
    
    def _extract_parameters(self, param_tensor: torch.Tensor) -> Dict[str, Any]:
        params = {}
        param_values = param_tensor.squeeze(0)
        
        # Extract different parameter types
        for i in range(0, min(len(param_values), 100), 10):
            param_group = param_values[i:i+10]
            param_name = f"param_group_{i//10}"
            params[param_name] = {
                'values': param_group.tolist(),
                'type': 'continuous' if param_group.std() > 0.1 else 'discrete',
                'range': [param_group.min().item(), param_group.max().item()]
            }
        
        return params
    
    def _plan_execution_sequence(self, sequence_tensor: torch.Tensor) -> List[Dict[str, Any]]:
        sequence = []
        seq_values = sequence_tensor.squeeze(0) if sequence_tensor.dim() > 1 else sequence_tensor
        
        for i, step_id in enumerate(seq_values[:20]):  # Limit to 20 steps
            step = {
                'step_id': i,
                'command_id': step_id.item(),
                'estimated_duration': 0.1 + (i * 0.05),
                'dependencies': list(range(max(0, i-2), i)),
                'parallel_eligible': i % 3 == 0
            }
            sequence.append(step)
        
        return sequence
    
    def _generate_error_mitigation(self, error_probs: torch.Tensor) -> Dict[str, Any]:
        error_vals = error_probs.squeeze(0)
        top_errors = torch.topk(error_vals, k=5)
        
        mitigation = {
            'high_risk_errors': [f"error_type_{idx.item()}" for idx in top_errors.indices],
            'mitigation_strategies': [f"strategy_{idx.item()}" for idx in top_errors.indices],
            'fallback_commands': [f"fallback_{idx.item()}" for idx in top_errors.indices],
            'monitoring_points': list(range(len(top_errors.indices)))
        }
        
        return mitigation
    
    def _estimate_duration(self, sequence_output: torch.Tensor) -> float:
        complexity = sequence_output.var().item()
        base_duration = 1.0
        return base_duration * (1.0 + complexity)
    
    def _estimate_command_resources(self, command_structure: torch.Tensor) -> Dict[str, float]:
        complexity = command_structure.norm().item()
        return {
            'cpu_utilization': min(1.0, complexity / 100),
            'memory_mb': min(512.0, complexity * 5),
            'network_bandwidth_mbps': min(10.0, complexity / 10),
            'storage_mb': min(100.0, complexity)
        }

class DigitalControlHead(nn.Module):
    """Control digital systems - shell, processes, APIs, and local capabilities."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize DigitalControlHead using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.api_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.LayerNorm(2048),
            nn.ReLU(),
            nn.Linear(2048, 4096)
        )
        
        self.data_controller = CanonicalBackboneDecoder(self.config, num_layers=2)
        
        self.process_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 1024)
        )
        
        self.protocol_handler = nn.LSTM(
            self.hidden_size, self.hidden_size,
            batch_first=True
        )
    
    def generate_control_signals(self, command_context: torch.Tensor,
                                system_profile: SystemProfile) -> Dict[str, Any]:
        """Generate profile-conditioned digital API, data, and process control signals."""
        seq3d = _ensure_seq3d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, seq3d.device, seq3d.dtype
        )
        conditioned = seq3d + 0.15 * prof_vec.unsqueeze(1)
        pooled = conditioned.mean(dim=1)
        api_commands = self.api_controller(pooled)
        data_commands = self.data_controller(conditioned, conditioned)
        process_commands = self.process_controller(pooled)
        protocol_output, _ = self.protocol_handler(conditioned)
        
        return {
            'api_commands': api_commands,
            'data_commands': data_commands.squeeze(0),
            'process_commands': process_commands,
            'protocol_signals': protocol_output.squeeze(0),
            'protocols_active': list(system_profile.communication_protocols),
            'control_ready': True
        }

class MechanicalControlHead(nn.Module):
    """Control mechanical systems - actuators and kinematics."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize MechanicalControlHead using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.kinematic_planner = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 6),
            nn.Tanh()
        )
        
        self.force_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )
        
        self.path_planner = CanonicalBackboneEncoder(self.config, num_layers=2)
        self.collision_avoider = MultiHeadAttention(self.config)
        
        self.safety_monitor = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
            nn.Sigmoid()
        )
    
    def generate_motion_control(self, command_context: torch.Tensor,
                               system_profile: SystemProfile) -> Dict[str, Any]:
        """Generate profile-conditioned kinematic and safety-monitored motion signals."""
        seq3d = _ensure_seq3d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, seq3d.device, seq3d.dtype
        )
        conditioned = seq3d + 0.15 * prof_vec.unsqueeze(1)
        pooled = conditioned.mean(dim=1)
        kinematic_commands = self.kinematic_planner(pooled) * float(system_profile.reliability_score)
        force_commands = self.force_controller(pooled)
        path_plan = self.path_planner(conditioned)
        collision_avoidance, _ = self.collision_avoider(conditioned, conditioned, conditioned)
        safety_params = self.safety_monitor(pooled)
        
        return {
            'kinematic_commands': kinematic_commands,
            'force_commands': force_commands,
            'path_plan': path_plan.squeeze(0),
            'collision_avoidance': collision_avoidance.squeeze(0),
            'safety_parameters': safety_params,
            'emergency_stop_armed': bool(system_profile.safety_constraints.get('emergency_stop_required', False)),
            'motion_ready': True
        }

class AnalogControlHead(nn.Module):
    """Control analog systems - power, sensors, instruments."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize AnalogControlHead using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.signal_generator = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.Tanh()
        )
        
        self.pid_synthesizer = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )
        
        self.calibrator = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        
        self.filter_designer = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )
    
    def generate_analog_control(self, command_context: torch.Tensor,
                               system_profile: SystemProfile) -> Dict[str, Any]:
        """Generate profile-conditioned continuous PID, calibration, and filter signals."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        v_cap = float(system_profile.safety_constraints.get('max_voltage', 24.0)) / 24.0
        return {
            'analog_signals': self.signal_generator(conditioned) * max(0.1, min(1.0, v_cap)),
            'pid_parameters': F.softplus(self.pid_synthesizer(conditioned)),
            'calibration_params': self.calibrator(conditioned),
            'filter_parameters': self.filter_designer(conditioned),
            'analog_ready': True
        }

class ElectromagneticControlHead(nn.Module):
    """Control electromagnetic systems - RF, radio, antennas."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize ElectromagneticControlHead using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.rf_synthesizer = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )
        
        self.antenna_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )
        
        self.field_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )
        
        self.modulation_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 32)
        )
    
    def generate_em_control(self, command_context: torch.Tensor,
                           system_profile: SystemProfile) -> Dict[str, Any]:
        """Generate profile-conditioned RF, antenna, field, and modulation parameters."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        return {
            'rf_signals': self.rf_synthesizer(conditioned),
            'antenna_control': self.antenna_controller(conditioned),
            'field_control': self.field_controller(conditioned),
            'modulation_parameters': self.modulation_controller(conditioned),
            'em_ready': True
        }


class OpticalControlHead(nn.Module):
    """
    Control optical, photonic, camera, and deterministic Set-of-Mark UI screen
    perception/targeting surfaces.
    """

    def __init__(self, config: Optional[NeuralNetConfig] = None) -> None:
        """Initialize OpticalControlHead on canonical d_model=512 dimensions."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        self.exposure_focus_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 8),
            nn.Sigmoid(),
        )
        self.roi_gaze_predictor = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 4),
            nn.Sigmoid(),
        )
        self.wavelength_band_selector = nn.Linear(self.hidden_size, 16)

    def generate_optical_control(
        self,
        command_context: torch.Tensor,
        system_profile: SystemProfile,
        visual_attention: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate optical sensor parameters and deterministic UI ROI gaze focus."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        roi_box = self.roi_gaze_predictor(conditioned)
        selected_mark_id = None
        selected_evidence_token = None
        if isinstance(visual_attention, dict):
            selected_mark_id = visual_attention.get("selected_mark_id")
            selected_evidence_token = visual_attention.get("selected_evidence_token")
        return {
            "exposure_focus_params": self.exposure_focus_controller(conditioned),
            "roi_normalized_bbox": roi_box,
            "spectral_bands": F.softmax(self.wavelength_band_selector(conditioned), dim=-1),
            "selected_mark_id": selected_mark_id,
            "selected_evidence_token": selected_evidence_token,
            "optical_ready": True,
        }


class ChemicalControlHead(nn.Module):
    """Control chemical synthesis, microfluidic dosing, and thermal reaction bounds."""

    def __init__(self, config: Optional[NeuralNetConfig] = None) -> None:
        """Initialize ChemicalControlHead on canonical d_model=512 dimensions."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        self.stoichiometry_planner = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 16),
            nn.Softmax(dim=-1),
        )
        self.kinetics_controller = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 6),
            nn.Sigmoid(),
        )

    def generate_chemical_control(
        self,
        command_context: torch.Tensor,
        system_profile: SystemProfile,
    ) -> Dict[str, Any]:
        """Generate stoichiometry ratios and temperature/flow kinetics bounds."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        return {
            "stoichiometry_ratios": self.stoichiometry_planner(conditioned),
            "kinetics_setpoints": self.kinetics_controller(conditioned),
            "max_temp_c": float(system_profile.safety_constraints.get("max_temperature", 85.0)),
            "chemical_ready": True,
        }


class BiologicalControlHead(nn.Module):
    """Control bioreactor homeostasis, fluidic assay schedules, and containment."""

    def __init__(self, config: Optional[NeuralNetConfig] = None) -> None:
        """Initialize BiologicalControlHead on canonical d_model=512 dimensions."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        self.homeostasis_regulator = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 8),
            nn.Sigmoid(),
        )
        self.containment_gate = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.SiLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def generate_biological_control(
        self,
        command_context: torch.Tensor,
        system_profile: SystemProfile,
    ) -> Dict[str, Any]:
        """Generate bounded homeostasis parameters and containment interlock verification."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        interlock = self.containment_gate(conditioned)
        return {
            "homeostasis_setpoints": self.homeostasis_regulator(conditioned),
            "containment_integrity": interlock,
            "biological_ready": bool(float(interlock.mean().item()) > 0.25),
        }


class QuantumControlHead(nn.Module):
    """Control quantum pulse envelopes, unitary gate schedules, and error mitigation."""

    def __init__(self, config: Optional[NeuralNetConfig] = None) -> None:
        """Initialize QuantumControlHead on canonical d_model=512 dimensions."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        self.pulse_shaper = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.SiLU(),
            nn.Linear(128, 32),
            nn.Tanh(),
        )
        self.gate_scheduler = nn.Linear(self.hidden_size, 16)

    def generate_quantum_control(
        self,
        command_context: torch.Tensor,
        system_profile: SystemProfile,
    ) -> Dict[str, Any]:
        """Generate bounded I/Q pulse envelopes and gate-sequence logits."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        return {
            "iq_pulse_envelope": self.pulse_shaper(conditioned),
            "gate_schedule_probs": F.softmax(self.gate_scheduler(conditioned), dim=-1),
            "quantum_ready": True,
        }

class MultiSystemCoordinator(nn.Module):
    """Coordinate control across multiple external systems without random edge noise."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize MultiSystemCoordinator using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.relationship_mapper = GraphNeuralNetwork(self.hidden_size, 4)
        self.edge_feature_proj = nn.Linear(self.hidden_size * 2, self.hidden_size)
        
        self.conflict_resolver = nn.Sequential(
            nn.Linear(self.hidden_size * 2, self.hidden_size),
            nn.ReLU(),
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 3),
            nn.Softmax(dim=-1)
        )
        
        self.resource_allocator = MultiHeadAttention(self.config)
        
        self.sync_controller = nn.LSTM(
            self.hidden_size, self.hidden_size,
            batch_first=True
        )
        
        self.priority_scheduler = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
    
    def coordinate_systems(self, system_contexts: List[torch.Tensor],
                          system_profiles: List[SystemProfile]) -> Dict[str, Any]:
        """Coordinate execution priorities and conflict resolution across systems."""
        if len(system_contexts) < 2:
            return {'coordination_needed': False}
        
        norm_vecs = [_pool_2d(ctx).squeeze(0) for ctx in system_contexts]
        stacked_contexts = torch.stack(norm_vecs)
        device = stacked_contexts.device
        
        pairs = [[i, j] for i in range(len(norm_vecs)) for j in range(len(norm_vecs)) if i != j]
        edge_indices = torch.tensor(pairs, dtype=torch.long, device=device)
        edge_inputs = torch.stack(
            [torch.cat([stacked_contexts[i], stacked_contexts[j]], dim=-1) for i, j in pairs]
        )
        edge_features = self.edge_feature_proj(edge_inputs)
        
        system_relationships = self.relationship_mapper(
            stacked_contexts, edge_indices, edge_features
        )
        
        conflict_pairs = []
        for i in range(len(norm_vecs)):
            for j in range(i + 1, len(norm_vecs)):
                combined_context = torch.cat([norm_vecs[i], norm_vecs[j]], dim=-1).unsqueeze(0)
                resolution = self.conflict_resolver(combined_context)
                conflict_pairs.append({
                    'systems': [system_profiles[i].system_id, system_profiles[j].system_id],
                    'resolution': resolution.squeeze(0),
                    'priority': torch.argmax(resolution).item()
                })
        
        seq_contexts = stacked_contexts.unsqueeze(0)
        resource_allocation, _ = self.resource_allocator(
            seq_contexts, seq_contexts, seq_contexts
        )
        sync_output, _ = self.sync_controller(seq_contexts)
        priorities = [
            self.priority_scheduler(v.unsqueeze(0)).item() for v in norm_vecs
        ]
        
        return {
            'coordination_needed': True,
            'system_relationships': system_relationships,
            'conflict_resolutions': conflict_pairs,
            'resource_allocation': resource_allocation.squeeze(0),
            'synchronization_plan': sync_output.squeeze(0),
            'execution_priorities': priorities,
            'coordination_overhead': len(norm_vecs) * 0.1
        }

class SafetyValidationEngine(nn.Module):
    """Ensure safe operation across all controlled systems."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize SafetyValidationEngine using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.risk_assessor = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
            nn.Sigmoid()
        )
        
        self.boundary_enforcer = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.Sigmoid()
        )
        
        self.emergency_predictor = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        self.safety_monitor = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 20)
        )
    
    def validate_safety(self, command_context: torch.Tensor,
                       system_profile: SystemProfile,
                       safety_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Validate safety envelopes and constraint thresholds conditioned on SystemProfile."""
        pooled = _pool_2d(command_context)
        prof_vec = _encode_system_profile_vec(
            system_profile, self.hidden_size, pooled.device, pooled.dtype
        )
        conditioned = pooled + 0.15 * prof_vec
        risk_scores = self.risk_assessor(conditioned)
        boundary_compliance = self.boundary_enforcer(conditioned)
        emergency_probability = self.emergency_predictor(conditioned)
        safety_params = self.safety_monitor(conditioned)
        
        merged_constraints = dict(system_profile.safety_constraints or {})
        merged_constraints.update(safety_constraints or {})
        constraint_violations = []
        param_vec = safety_params[0]
        for constraint, limit in merged_constraints.items():
            if isinstance(limit, (int, float)) and not isinstance(limit, bool) and limit > 0:
                digest = hashlib.blake2b(str(constraint).encode("utf-8"), digest_size=4).digest()
                param_idx = int.from_bytes(digest, "little") % len(param_vec)
                param_value = torch.sigmoid(param_vec[param_idx]).item()
                if param_value > float(limit):
                    constraint_violations.append({
                        'constraint': constraint,
                        'limit': limit,
                        'current_value': param_value,
                        'severity': param_value / max(abs(float(limit)), 1e-6)
                    })
        
        return {
            'overall_safety_score': boundary_compliance.mean().item(),
            'profile_reliability': float(system_profile.reliability_score),
            'risk_categories': risk_scores[0].tolist(),
            'emergency_probability': emergency_probability[0].item(),
            'constraint_violations': constraint_violations,
            'safety_parameters': param_vec.tolist(),
            'safe_to_execute': (
                boundary_compliance.mean().item() > 0.3 and 
                emergency_probability[0].item() < 0.8 and 
                len(constraint_violations) == 0
            ),
            'recommended_actions': self._generate_safety_recommendations(
                risk_scores[0:1], constraint_violations
            )
        }
    
    def _generate_safety_recommendations(self, risk_scores: torch.Tensor,
                                        violations: List[Dict[str, Any]]) -> List[str]:
        recommendations = []
        high_risks = torch.where(risk_scores.squeeze(0) > 0.7)[0]
        for risk_idx in high_risks:
            recommendations.append(f"Monitor risk category {risk_idx.item()}")
        for violation in violations:
            if violation['severity'] > 2.0:
                recommendations.append(f"Critical: Reduce {violation['constraint']}")
            elif violation['severity'] > 1.5:
                recommendations.append(f"Warning: Monitor {violation['constraint']}")
        return recommendations if recommendations else ["No safety concerns detected"]

class ExecutionOrchestrator(nn.Module):
    """Plan and coordinate multi-tool workflows on canonical Muad'Dib dimensions."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize ExecutionOrchestrator using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.dependency_mapper = GraphNeuralNetwork(self.hidden_size, 4)
        self.edge_feature_proj = nn.Linear(self.hidden_size * 2, self.hidden_size)
        
        self.execution_scheduler = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )
        
        self.resource_allocator = MultiHeadAttention(self.config)
        
        self.parallelization_planner = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.Sigmoid()
        )
        
        self.workflow_optimizer = nn.LSTM(
            self.hidden_size, self.hidden_size,
            num_layers=2, batch_first=True
        )
    
    def orchestrate_execution(self, tool_contexts: List[torch.Tensor],
                             execution_objectives: Dict[str, Any]) -> Dict[str, Any]:
        """Build an objective- and dependency-aware execution plan over tool_contexts."""
        if not tool_contexts:
            return {'execution_plan': None, 'orchestration_needed': False}
        
        norm_vecs = [_pool_2d(t).squeeze(0) for t in tool_contexts]
        stacked_contexts = torch.stack(norm_vecs)
        device = stacked_contexts.device
        obj_text = str((execution_objectives or {}).get('primary', 'autonomous_operation'))
        max_parallel = max(1, int((execution_objectives or {}).get('max_parallel', 3)))
        latency_budget = float((execution_objectives or {}).get('latency_budget_s', 30.0))
        obj_vec = _hash_token_to_vec(obj_text, self.hidden_size, device, stacked_contexts.dtype)
        conditioned_contexts = stacked_contexts + 0.10 * obj_vec.unsqueeze(0)
        
        if len(norm_vecs) > 1:
            pairs = [[i, j] for i in range(len(norm_vecs)) for j in range(len(norm_vecs)) if i != j]
            edge_indices = torch.tensor(pairs, dtype=torch.long, device=device)
            edge_inputs = torch.stack(
                [torch.cat([conditioned_contexts[i], conditioned_contexts[j]], dim=-1) for i, j in pairs]
            )
            edge_features = self.edge_feature_proj(edge_inputs)
            dependency_map = self.dependency_mapper(conditioned_contexts, edge_indices, edge_features)
        else:
            dependency_map = conditioned_contexts
        
        execution_schedule = self.execution_scheduler(conditioned_contexts.mean(0, keepdim=True))
        seq_ctx = conditioned_contexts.unsqueeze(0)
        resource_allocation, _ = self.resource_allocator(seq_ctx, seq_ctx, seq_ctx)
        parallel_eligibility = self.parallelization_planner(conditioned_contexts)
        workflow_optimization, _ = self.workflow_optimizer(seq_ctx)
        est_duration = self._estimate_total_duration(execution_schedule)
        
        return {
            'tool_count': len(norm_vecs),
            'primary_objective': obj_text,
            'dependency_graph': dependency_map,
            'execution_schedule': execution_schedule,
            'resource_allocation': resource_allocation.squeeze(0),
            'parallel_groups': self._identify_parallel_groups(parallel_eligibility, max_group_size=max_parallel),
            'workflow_optimization': workflow_optimization.squeeze(0),
            'estimated_duration': est_duration,
            'within_latency_budget': bool(est_duration <= latency_budget),
            'critical_path': self._identify_critical_path(dependency_map),
            'orchestration_needed': True
        }
    
    def _identify_parallel_groups(
        self,
        parallel_eligibility: torch.Tensor,
        max_group_size: int = 3,
    ) -> List[List[int]]:
        groups = []
        scores = parallel_eligibility.mean(dim=-1) if parallel_eligibility.dim() > 1 else parallel_eligibility
        eligible_indices = torch.where(scores > 0.5)[0]
        current_group: List[int] = []
        cap = max(1, int(max_group_size))
        for idx in eligible_indices:
            if len(current_group) < cap:
                current_group.append(idx.item())
            else:
                groups.append(current_group)
                current_group = [idx.item()]
        if current_group:
            groups.append(current_group)
        return groups
    
    def _estimate_total_duration(self, execution_schedule: torch.Tensor) -> float:
        complexity = execution_schedule.norm().item()
        return 2.0 * (1.0 + complexity / 10.0)
    
    def _identify_critical_path(self, dependency_map: torch.Tensor) -> List[int]:
        dependencies = dependency_map.sum(dim=-1)
        critical_indices = torch.argsort(dependencies, descending=True)[:5]
        return critical_indices.tolist()

class ProtocolSynthesisEngine(nn.Module):
    """Learn and synthesize communication protocols on canonical backbone."""
    
    def __init__(self, config: Optional[NeuralNetConfig] = None):
        """Initialize ProtocolSynthesisEngine using NeuralNetConfig."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        self.pattern_recognizer = CanonicalBackboneEncoder(self.config, num_layers=2)
        
        self.message_formatter = nn.Sequential(
            nn.Linear(self.hidden_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.LayerNorm(2048),
            nn.ReLU(),
            nn.Linear(2048, 4096)
        )
        
        self.checksum_generator = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        
        self.protocol_optimizer = nn.LSTM(
            self.hidden_size, self.hidden_size,
            batch_first=True
        )
    
    def synthesize_protocol(self, communication_context: torch.Tensor,
                           target_systems: List[SystemProfile]) -> Dict[str, Any]:
        """Synthesize message format and error-correction parameters."""
        seq3d = _ensure_seq3d(communication_context)
        protocol_patterns = self.pattern_recognizer(seq3d)
        pooled = protocol_patterns.mean(dim=1)
        message_format = self.message_formatter(pooled)
        checksum_params = self.checksum_generator(pooled)
        protocol_optimization, _ = self.protocol_optimizer(protocol_patterns)
        
        return {
            'protocol_id': hashlib.sha256(protocol_patterns.detach().cpu().numpy().tobytes()).hexdigest()[:8],
            'message_format': message_format,
            'checksum_algorithm': checksum_params[0],
            'optimization_params': protocol_optimization.squeeze(0),
            'target_systems': [sys.system_id for sys in target_systems],
            'protocol_overhead': self._estimate_protocol_overhead(message_format),
            'error_correction': self._generate_error_correction(checksum_params[0]),
            'bandwidth_efficiency': self._calculate_bandwidth_efficiency(protocol_patterns)
        }
    
    def _estimate_protocol_overhead(self, message_format: torch.Tensor) -> float:
        format_complexity = message_format.norm().item()
        return min(0.5, format_complexity / 1000)
    
    def _generate_error_correction(self, checksum_params: torch.Tensor) -> Dict[str, Any]:
        return {
            'error_detection': checksum_params[:16].tolist(),
            'error_correction': checksum_params[16:].tolist(),
            'correction_strength': checksum_params.mean().item()
        }
    
    def _calculate_bandwidth_efficiency(self, protocol_patterns: torch.Tensor) -> float:
        pattern_efficiency = 1.0 - protocol_patterns.std().item()
        return max(0.1, min(1.0, pattern_efficiency))

class TypedToolActionHead(nn.Module):
    """
    Typed BB7 Tool Action Head (Stage B/C native action proposal head).

    Consumes canonical hidden_states [batch, seq_len, d_model=512] plus an
    optional legal_action_mask [batch, vocab_size] and emits:
      - action_kind_logits / selected_action_kind (registered_tool | shell_command | structured_output | abstain)
      - masked_tool_logits / top_tool_ids / top_tool_probs (strictly legal-masked)
      - argument_slot_vectors [batch, max_arg_slots, d_model]
      - value_estimate [-1, 1] and epistemic_uncertainty [0, 1]
      - abstention_prob [0, 1]
    """

    def __init__(
        self,
        config: Optional[NeuralNetConfig] = None,
        max_arg_slots: int = 8,
    ) -> None:
        """Initialize TypedToolActionHead on NeuralNetConfig (d_model=512)."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.d_model = self.config.d_model
        self.vocab_size = self.config.vocab_size
        self.max_arg_slots = max_arg_slots

        self.pre_norm = AeronRMSNorm(self.d_model, eps=self.config.rms_norm_eps)
        self.action_kind_head = nn.Linear(self.d_model, len(ActionKind))
        self.tool_logits_head = nn.Sequential(
            nn.Linear(self.d_model, self.d_model),
            nn.SiLU(),
            nn.Linear(self.d_model, self.vocab_size),
        )
        self.arg_slot_queries = nn.Parameter(
            torch.randn(1, max_arg_slots, self.d_model) * 0.02
        )
        self.arg_slot_decoder = CanonicalBackboneDecoder(self.config, num_layers=1)
        self.value_head = nn.Sequential(
            nn.Linear(self.d_model, self.d_model // 2),
            nn.SiLU(),
            nn.Linear(self.d_model // 2, 1),
            nn.Tanh(),
        )
        self.uncertainty_head = nn.Sequential(
            nn.Linear(self.d_model, self.d_model // 2),
            nn.SiLU(),
            nn.Linear(self.d_model // 2, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        legal_action_mask: Optional[torch.Tensor] = None,
        prior_bonuses: Optional[torch.Tensor] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Emit legal-masked typed action proposals and argument slot tensors."""
        seq3d = self.pre_norm(_ensure_seq3d(hidden_states))
        batch_size = seq3d.shape[0]
        pooled = seq3d.mean(dim=1)

        kind_logits = self.action_kind_head(pooled)
        kind_probs = F.softmax(kind_logits, dim=-1)
        kind_list = list(ActionKind)
        selected_kinds = [
            kind_list[int(idx)].value
            for idx in torch.argmax(kind_probs, dim=-1).tolist()
        ]

        raw_tool_logits = self.tool_logits_head(pooled)
        if prior_bonuses is not None and prior_bonuses.shape == raw_tool_logits.shape:
            raw_tool_logits = raw_tool_logits + prior_bonuses

        if legal_action_mask is not None:
            mask = legal_action_mask.to(dtype=torch.bool, device=raw_tool_logits.device)
            if mask.dim() == 1:
                mask = mask.unsqueeze(0).expand_as(raw_tool_logits)
            # Guard against an all-False mask row by permitting index 0 (abstain fallback)
            empty_rows = ~mask.any(dim=-1, keepdim=True)
            safe_mask = torch.where(
                empty_rows, torch.ones_like(mask), mask
            )
            masked_logits = raw_tool_logits.masked_fill(~safe_mask, -1e9)
        else:
            masked_logits = raw_tool_logits

        tool_probs = F.softmax(masked_logits, dim=-1)
        k_eff = min(max(1, int(top_k)), self.vocab_size)
        top_probs, top_ids = torch.topk(tool_probs, k=k_eff, dim=-1)

        slot_q = self.arg_slot_queries.expand(batch_size, -1, -1)
        arg_slot_vectors = self.arg_slot_decoder(slot_q, seq3d)

        abstain_idx = kind_list.index(ActionKind.ABSTAIN)
        return {
            "action_kind_logits": kind_logits,
            "action_kind_probs": kind_probs,
            "selected_action_kind": selected_kinds[0] if batch_size == 1 else selected_kinds,
            "abstention_prob": kind_probs[:, abstain_idx],
            "tool_logits": masked_logits,
            "top_tool_ids": top_ids,
            "top_tool_probs": top_probs,
            "argument_slot_vectors": arg_slot_vectors,
            "value_estimate": self.value_head(pooled).squeeze(-1),
            "uncertainty": self.uncertainty_head(pooled).squeeze(-1),
        }


class DeterministicVisualAttentionBridge(nn.Module):
    """
    Deterministic Set-of-Mark (SoM) Visual Attention Bridge (d_model=512).

    Connects VisualTool's deterministic UI grounding (bb7_ui_ground_screen &
    visual_cognition.db ui_grounding_marks) directly to Muad'Dib's canonical
    GQA+RoPE MultiHeadAttention without ViT pixel-CNN overhead or coordinate
    hallucination. Selects actionable mark_ids and verified one-use click
    evidence_tokens deterministically.
    """

    ELEMENT_TYPES: Tuple[str, ...] = (
        "button",
        "input",
        "terminal",
        "ocr_text",
        "contour_box",
        "widget",
        "unknown",
    )

    def __init__(self, config: Optional[NeuralNetConfig] = None) -> None:
        """Initialize spatial box projections and canonical cross-attention at d_model=512."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.d_model = self.config.d_model
        self.element_type_embed = nn.Embedding(len(self.ELEMENT_TYPES), self.d_model)
        self.spatial_box_proj = nn.Sequential(
            nn.Linear(12, self.d_model // 2),
            nn.SiLU(),
            nn.Linear(self.d_model // 2, self.d_model),
        )
        self.mark_norm = AeronRMSNorm(self.d_model, eps=self.config.rms_norm_eps)
        self.cross_attn = CanonicalBackboneDecoder(self.config, num_layers=1)
        self.pointer_query = nn.Linear(self.d_model, self.d_model, bias=False)
        self.pointer_key = nn.Linear(self.d_model, self.d_model, bias=False)

    @staticmethod
    def extract_marks_from_observation(
        visual_source: Any,
        visual_db_path: Optional[Path] = None,
    ) -> Tuple[List[Dict[str, Any]], Tuple[int, int], Optional[str]]:
        """Extract deterministic SoM marks from a BB7Response, dict, list, or visual_cognition.db."""
        screen_w, screen_h = 1280, 800
        grounding_id: Optional[str] = None
        marks: List[Dict[str, Any]] = []

        if hasattr(visual_source, "structured") and isinstance(visual_source.structured, dict):
            visual_source = visual_source.structured

        if isinstance(visual_source, dict):
            grounding_id = visual_source.get("grounding_id")
            dims = visual_source.get("screen_size") or visual_source.get("dimensions")
            if isinstance(dims, dict):
                screen_w = max(1, int(dims.get("width", 1280)))
                screen_h = max(1, int(dims.get("height", 800)))
            raw_marks = visual_source.get("marks") or visual_source.get("matches") or []
            if isinstance(raw_marks, list):
                marks = [dict(m) for m in raw_marks if isinstance(m, dict)]
        elif isinstance(visual_source, list):
            marks = [dict(m) for m in visual_source if isinstance(m, dict)]

        if not marks and visual_db_path is not None and Path(visual_db_path).is_file():
            conn = sqlite3.connect(str(visual_db_path), timeout=10.0)
            conn.row_factory = sqlite3.Row
            try:
                latest = conn.execute(
                    "SELECT grounding_id FROM ui_grounding_marks ORDER BY timestamp DESC LIMIT 1"
                ).fetchone()
                if latest is not None:
                    grounding_id = str(latest["grounding_id"])
                    rows = conn.execute(
                        """
                        SELECT mark_id, label, element_type, x, y, width, height,
                               center_x, center_y, confidence, evidence_token
                        FROM ui_grounding_marks
                        WHERE grounding_id = ?
                        ORDER BY mark_id ASC
                        """,
                        (grounding_id,),
                    ).fetchall()
                    marks = [dict(r) for r in rows]
            except sqlite3.Error as exc:
                logger.error("Failed reading ui_grounding_marks from %s: %s", visual_db_path, exc)
            finally:
                conn.close()

        return marks, (screen_w, screen_h), grounding_id

    def encode_marks(
        self,
        marks: Sequence[Dict[str, Any]],
        screen_size: Tuple[int, int] = (1280, 800),
        device: Optional[torch.device] = None,
        dtype: torch.dtype = torch.float32,
    ) -> torch.Tensor:
        """Encode deterministic UI marks [1]..[N] into [1, N, d_model=512] tokens."""
        dev = device or self.element_type_embed.weight.device
        sw = float(max(1, screen_size[0]))
        sh = float(max(1, screen_size[1]))
        token_rows: List[torch.Tensor] = []
        total_marks = max(1, len(marks))

        for rank_idx, mark in enumerate(marks):
            x = float(mark.get("x", 0.0))
            y = float(mark.get("y", 0.0))
            bbox = mark.get("bbox")
            if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
                w = float(bbox[2])
                h = float(bbox[3])
            else:
                w = float(mark.get("width", 32.0))
                h = float(mark.get("height", 24.0))
            cx = float(mark.get("center_x", x + 0.5 * w))
            cy = float(mark.get("center_y", y + 0.5 * h))
            conf = float(mark.get("confidence", 0.9))

            nx, ny = x / sw, y / sh
            nw, nh = w / sw, h / sh
            ncx, ncy = cx / sw, cy / sh
            log_area = math.log1p(max(0.0, w * h)) / math.log1p(sw * sh)
            rank_norm = float(rank_idx) / float(total_marks)
            geom = torch.tensor(
                [
                    nx,
                    ny,
                    nw,
                    nh,
                    ncx,
                    ncy,
                    log_area,
                    conf,
                    math.sin(ncx * math.pi),
                    math.cos(ncx * math.pi),
                    math.sin(ncy * math.pi),
                    rank_norm,
                ],
                dtype=torch.float32,
                device=dev,
            )
            etype = str(mark.get("element_type") or mark.get("method") or "unknown").lower()
            etype_idx = (
                self.ELEMENT_TYPES.index(etype)
                if etype in self.ELEMENT_TYPES
                else len(self.ELEMENT_TYPES) - 1
            )
            type_vec = self.element_type_embed(torch.tensor(etype_idx, device=dev))
            label_vec = _hash_token_to_vec(
                f"lbl:{mark.get('label', '')}|type:{etype}", self.d_model, dev
            )
            combined = self.spatial_box_proj(geom) + type_vec + label_vec
            token_rows.append(combined)

        stacked = torch.stack(token_rows, dim=0).unsqueeze(0).to(dtype=dtype)
        return self.mark_norm(stacked)

    def forward(
        self,
        hidden_states: torch.Tensor,
        marks: Sequence[Dict[str, Any]],
        *,
        screen_size: Tuple[int, int] = (1280, 800),
        goal_text: str = "",
    ) -> Dict[str, Any]:
        """Attend deterministically over grounded UI marks and select verified evidence."""
        seq_states = _ensure_seq3d(hidden_states)
        if not marks:
            return {
                "attended_states": seq_states,
                "mark_count": 0,
                "selected_mark_id": None,
                "selected_mark": None,
                "selected_evidence_token": None,
                "mark_attention_weights": None,
                "mark_logits": None,
            }

        mark_tokens = self.encode_marks(
            marks, screen_size=screen_size, device=seq_states.device, dtype=seq_states.dtype
        )
        batch_size = seq_states.shape[0]
        expanded_marks = mark_tokens.expand(batch_size, -1, -1)
        cross_out = self.cross_attn(seq_states, expanded_marks)

        pooled_q = self.pointer_query(seq_states.mean(dim=1))
        keys = self.pointer_key(expanded_marks)
        logits = torch.einsum("bd,bnd->bn", pooled_q, keys) / math.sqrt(float(self.d_model))

        if goal_text.strip():
            goal_words = {
                w.strip(".,:;!?'\"()[]{}").lower()
                for w in goal_text.split()
                if len(w.strip(".,:;!?'\"()[]{}")) >= 2
            }
            bonuses = torch.zeros_like(logits)
            for idx, m in enumerate(marks):
                lbl = str(m.get("label", "")).lower()
                etype = str(m.get("element_type", "")).lower()
                if lbl and lbl in goal_text.lower():
                    bonuses[:, idx] += 2.25
                else:
                    lbl_words = set(lbl.split())
                    overlap = len(goal_words & lbl_words)
                    if overlap > 0:
                        bonuses[:, idx] += 0.85 * float(overlap)
                if ("type" in goal_words or "input" in goal_words) and etype == "input":
                    bonuses[:, idx] += 0.65
                bonuses[:, idx] += 0.25 * float(m.get("confidence", 0.8))
            logits = logits + bonuses

        attn_weights = F.softmax(logits, dim=-1)
        best_idx = int(torch.argmax(attn_weights[0]).item())
        best_mark = dict(marks[best_idx])
        selected_mark_id = best_mark.get("mark_id", best_idx + 1)
        selected_token = best_mark.get("evidence_token")

        ranked = sorted(
            [
                {
                    "rank_index": i,
                    "mark_id": m.get("mark_id", i + 1),
                    "label": m.get("label", ""),
                    "element_type": m.get("element_type", "widget"),
                    "attention_weight": round(float(attn_weights[0, i].item()), 4),
                    "evidence_token": m.get("evidence_token"),
                    "center": (m.get("center_x", m.get("x")), m.get("center_y", m.get("y"))),
                }
                for i, m in enumerate(marks)
            ],
            key=lambda item: item["attention_weight"],
            reverse=True,
        )

        return {
            "attended_states": cross_out,
            "mark_tokens": mark_tokens,
            "mark_count": len(marks),
            "mark_logits": logits,
            "mark_attention_weights": attn_weights,
            "selected_index": best_idx,
            "selected_mark_id": selected_mark_id,
            "selected_mark": best_mark,
            "selected_evidence_token": selected_token,
            "ranked_marks": ranked[:10],
        }


class DocDBToolMemoryAdapter:
    """
    Native DocDB v1.5.0+ Memory Adapter for Muad'Dib's Tool Modality.

    Aligns UniversalToolControlOutputHead's memory conditioning, ToolGenome
    evolution registry, SystemProfile discovery cache, and execution outcomes
    directly onto EnhancedMemoryTool / DocDB (docdb.sqlite WAL + 512-D vectors +
    somnus://metadata/core/2.0.0 UUIDv7 URNs + HNFP swarm cells).
    """

    def __init__(
        self,
        data_dir: Optional[Union[str, Path]] = None,
        memory_tool: Optional[Any] = None,
        d_model: int = 512,
    ) -> None:
        """Bind to an existing EnhancedMemoryTool or lazily open one on data_dir."""
        self.data_dir: Path = _resolve_sovereign_data_dir(data_dir)
        self.docdb_path: Path = self.data_dir / "docdb.sqlite"
        self.d_model: int = d_model
        self._memory_tool: Optional[Any] = memory_tool
        self._lock = threading.RLock()

    @property
    def memory_tool(self) -> Any:
        """Lazily initialize in-process EnhancedMemoryTool backed by ./docdb."""
        with self._lock:
            if self._memory_tool is None:
                from tools.memory_tool import EnhancedMemoryTool

                self._memory_tool = EnhancedMemoryTool(data_dir=self.data_dir)
            return self._memory_tool

    def attach_memory_tool(self, memory_tool: Any) -> None:
        """Bind a shared one-plane EnhancedMemoryTool instance."""
        with self._lock:
            self._memory_tool = memory_tool
            doc_path = getattr(memory_tool, "docdb_path", None)
            if doc_path is not None:
                self.docdb_path = Path(doc_path)
                self.data_dir = self.docdb_path.parent

    @contextlib.contextmanager
    def _connect_docdb(self) -> Iterator[sqlite3.Connection]:
        """Open a WAL-configured SQLite connection to docdb.sqlite with guaranteed close."""
        _ = self.memory_tool
        conn = sqlite3.connect(str(self.docdb_path), timeout=15.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA foreign_keys=ON")
            with conn:
                yield conn
        finally:
            conn.close()

    def _unpack_512d_blob(
        self,
        blob: Optional[bytes],
        fallback_text: str,
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        """Decode a 512-float32 DocDB embedding blob or hash deterministically."""
        expected_bytes = self.d_model * 4
        if isinstance(blob, (bytes, bytearray)) and len(blob) == expected_bytes:
            vals = struct.unpack(f"<{self.d_model}f", bytes(blob))
            return torch.tensor(vals, dtype=dtype, device=device)
        return _hash_token_to_vec(fallback_text, self.d_model, device, dtype)

    def recall_conditioning_tensors(
        self,
        query_text: str,
        *,
        top_k: int = 4,
        device: Optional[torch.device] = None,
        dtype: torch.dtype = torch.float32,
    ) -> Tuple[Optional[torch.Tensor], List[Dict[str, Any]]]:
        """Recall 512-D DocDB memory embeddings + Somnus URN metadata for conditioning."""
        dev = device or torch.device("cpu")
        mem = self.memory_tool
        matched_keys: List[str] = []
        records_meta: List[Dict[str, Any]] = []

        if query_text.strip():
            sem_resp = mem.bb7_memory_semantic_search(
                query=query_text, max_results=max(1, int(top_k))
            )
            results = (
                sem_resp.structured.get("results", [])
                if hasattr(sem_resp, "structured") and isinstance(sem_resp.structured, dict)
                else []
            )
            for item in results:
                if isinstance(item, dict) and item.get("key"):
                    matched_keys.append(str(item["key"]))

        vecs: List[torch.Tensor] = []
        with self._connect_docdb() as conn:
            if matched_keys:
                placeholders = ",".join("?" for _ in matched_keys)
                rows = conn.execute(
                    f"""
                    SELECT memory_key, content, memory_type, importance, somnus_urn, embedding
                    FROM memories
                    WHERE memory_key IN ({placeholders})
                    LIMIT ?
                    """,
                    (*matched_keys, max(1, int(top_k))),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT memory_key, content, memory_type, importance, somnus_urn, embedding
                    FROM memories
                    ORDER BY importance DESC, timestamp DESC, id DESC
                    LIMIT ?
                    """,
                    (max(1, int(top_k)),),
                ).fetchall()

            for row in rows:
                key_str = str(row["memory_key"])
                content_str = str(row["content"] or "")
                vec = self._unpack_512d_blob(
                    row["embedding"], f"{key_str}:{content_str[:128]}", dev, dtype
                )
                vecs.append(vec)
                records_meta.append(
                    {
                        "key": key_str,
                        "category": str(row["memory_type"] or "technical"),
                        "importance": float(row["importance"] or 0.5),
                        "somnus_urn": row["somnus_urn"],
                    }
                )

        if not vecs:
            return None, []
        return torch.stack(vecs, dim=0).unsqueeze(0), records_meta

    def persist_tool_genome(self, genome: ToolGenome) -> Dict[str, Any]:
        """Persist a ToolGenome (including its exact 512-D vector) into DocDB + Somnus + HNFP."""
        key = f"tm_genome:{genome.genome_id}"
        payload = genome.to_dict(include_vector=True)
        resp = self.memory_tool.store(
            key=key,
            value=json.dumps(payload, sort_keys=True),
            category="technical",
            importance=max(0.55, min(0.98, float(genome.safety_rating))),
            tags=["tool_modality", "tool_genome", f"gen_{genome.evolution_generation}"],
        )
        urn = resp.structured.get("somnus_urn")
        docdb_id = resp.structured.get("docdb_id")
        genome.somnus_urn = urn
        genome.docdb_id = docdb_id

        vec_cpu = genome.functionality_vector.detach().cpu().to(dtype=torch.float32).view(-1)
        if int(vec_cpu.numel()) == self.d_model:
            blob = struct.pack(f"<{self.d_model}f", *vec_cpu.tolist())
            with self._connect_docdb() as conn:
                conn.execute(
                    "UPDATE memories SET embedding = ? WHERE memory_key = ?",
                    (blob, key),
                )
        return {"key": key, "somnus_urn": urn, "docdb_id": docdb_id}

    def persist_system_profile(self, profile: SystemProfile) -> Dict[str, Any]:
        """Persist a discovered SystemProfile into DocDB + Somnus + HNFP."""
        key = f"tm_system:{profile.system_id}"
        payload = profile.to_dict()
        resp = self.memory_tool.store(
            key=key,
            value=json.dumps(payload, sort_keys=True),
            category="technical",
            importance=max(0.5, min(0.95, float(profile.reliability_score))),
            tags=["tool_modality", "system_profile", *[d.name.lower() for d in profile.control_domains]],
        )
        urn = resp.structured.get("somnus_urn")
        docdb_id = resp.structured.get("docdb_id")
        profile.somnus_urn = urn
        profile.docdb_id = docdb_id
        return {"key": key, "somnus_urn": urn, "docdb_id": docdb_id}

    def persist_control_outcome(
        self,
        outcome_id: str,
        summary_payload: Dict[str, Any],
        importance: float = 0.7,
    ) -> Dict[str, Any]:
        """Persist a compiled tool-modality control/visual outcome into DocDB."""
        key = f"tm_outcome:{outcome_id}"
        resp = self.memory_tool.store(
            key=key,
            value=json.dumps(summary_payload, sort_keys=True, default=str),
            category="patterns",
            importance=max(0.4, min(0.95, float(importance))),
            tags=["tool_modality", "control_outcome"],
        )
        return {
            "key": key,
            "somnus_urn": resp.structured.get("somnus_urn"),
            "docdb_id": resp.structured.get("docdb_id"),
        }

    def hydrate_into_head(self, head: "UniversalToolControlOutputHead") -> Dict[str, int]:
        """Hydrate persisted ToolGenomes and SystemProfiles from DocDB into head registries."""
        genomes_loaded = 0
        systems_loaded = 0
        dev = next(head.parameters()).device

        with self._connect_docdb() as conn:
            rows = conn.execute(
                """
                SELECT id, memory_key, content, somnus_urn, embedding
                FROM memories
                WHERE memory_key LIKE 'tm_genome:%' OR memory_key LIKE 'tm_system:%'
                ORDER BY timestamp DESC, id DESC
                LIMIT 256
                """
            ).fetchall()

        for row in rows:
            mkey = str(row["memory_key"])
            raw_content = str(row["content"] or "").strip()
            json_start = raw_content.find("{")
            if json_start < 0:
                continue
            try:
                parsed = json.loads(raw_content[json_start:])
            except json.JSONDecodeError as exc:
                logger.error("Skipping malformed DocDB tool_modality record %s: %s", mkey, exc)
                continue
            if not isinstance(parsed, dict):
                continue
            parsed.setdefault("somnus_urn", row["somnus_urn"])
            parsed.setdefault("docdb_id", int(row["id"]))

            if mkey.startswith("tm_genome:") and "genome_id" in parsed:
                vec = self._unpack_512d_blob(
                    row["embedding"], mkey, dev, torch.float32
                )
                genome = ToolGenome.from_dict(parsed, vector_override=vec, d_model=self.d_model)
                head.tool_registry[genome.genome_id] = genome
                head.tool_synthesis.tool_genome_registry[genome.genome_id] = genome
                genomes_loaded += 1
            elif mkey.startswith("tm_system:") and "system_id" in parsed:
                prof = SystemProfile.from_dict(parsed)
                head.active_systems[prof.system_id] = prof
                head.system_discovery.discovered_systems[prof.system_id] = prof
                systems_loaded += 1

        return {"genomes_loaded": genomes_loaded, "systems_loaded": systems_loaded}


class UniversalToolControlOutputHead(nn.Module):
    """Universal tool synthesis, typed action proposal, visual attention, and 8-domain control head."""
    
    def __init__(
        self,
        config: Optional[NeuralNetConfig] = None,
        docdb_adapter: Optional[DocDBToolMemoryAdapter] = None,
    ) -> None:
        """Initialize UniversalToolControlOutputHead on NeuralNetConfig (d_model=512)."""
        super().__init__()
        self.config = config or NeuralNetConfig()
        self.hidden_size = self.config.d_model
        
        # Native typed action proposal head
        self.typed_action_head = TypedToolActionHead(self.config)

        # Deterministic Set-of-Mark visual attention bridge + DocDB 512-D cross-attention
        self.visual_attention_bridge = DeterministicVisualAttentionBridge(self.config)
        self.docdb_memory_attn = CanonicalBackboneDecoder(self.config, num_layers=1)
        self.docdb_adapter: Optional[DocDBToolMemoryAdapter] = docdb_adapter

        # Core synthesis & orchestration engines
        self.system_discovery = SystemDiscoveryEngine(self.config)
        self.interface_adaptation = InterfaceAdaptationEngine(self.config)
        self.tool_synthesis = ToolSynthesisEngine(self.config)
        self.command_synthesis = CommandSynthesisEngine(self.config)
        self.execution_orchestrator = ExecutionOrchestrator(self.config)
        self.protocol_synthesis = ProtocolSynthesisEngine(self.config)
        
        # Learned multi-probe subspace projection (replaces fake torch.randn probes)
        self.discovery_probe_proj = nn.Linear(self.hidden_size, self.hidden_size * 4, bias=False)

        # Complete 8-domain ControlDomain heads
        self.control_heads = nn.ModuleDict({
            'digital': DigitalControlHead(self.config),
            'mechanical': MechanicalControlHead(self.config),
            'analog': AnalogControlHead(self.config),
            'electromagnetic': ElectromagneticControlHead(self.config),
            'optical': OpticalControlHead(self.config),
            'chemical': ChemicalControlHead(self.config),
            'biological': BiologicalControlHead(self.config),
            'quantum': QuantumControlHead(self.config),
        })
        
        # Coordination and safety
        self.multi_system_coordinator = MultiSystemCoordinator(self.config)
        self.safety_validator = SafetyValidationEngine(self.config)
        
        # Universal projectors
        self.capability_router = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, len(ControlDomain)),
            nn.Softmax(dim=-1)
        )
        
        self.operation_mode_selector = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, len(OperationMode)),
            nn.Softmax(dim=-1)
        )
        
        # State management
        self.active_systems: Dict[str, SystemProfile] = {}
        self.tool_registry: Dict[str, ToolGenome] = {}
        self.execution_history: deque = deque(maxlen=100000)
        self.performance_metrics: Dict[str, float] = defaultdict(float)
        
        # Async execution support
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        self.execution_queue: queue.Queue = queue.Queue()

    def attach_docdb_memory(
        self,
        docdb_adapter: Optional[DocDBToolMemoryAdapter] = None,
        *,
        data_dir: Optional[Union[str, Path]] = None,
        memory_tool: Optional[Any] = None,
        hydrate: bool = True,
    ) -> Dict[str, Any]:
        """Attach DocDBToolMemoryAdapter and optionally hydrate persisted genomes/systems."""
        if docdb_adapter is not None:
            self.docdb_adapter = docdb_adapter
        else:
            self.docdb_adapter = DocDBToolMemoryAdapter(
                data_dir=data_dir, memory_tool=memory_tool, d_model=self.hidden_size
            )
        hydrated = self.docdb_adapter.hydrate_into_head(self) if hydrate else {"genomes_loaded": 0, "systems_loaded": 0}
        return {
            "docdb_attached": True,
            "docdb_path": str(self.docdb_adapter.docdb_path),
            **hydrated,
        }

    def enqueue_execution_plan(self, plan: Dict[str, Any]) -> int:
        """Enqueue a validated execution plan onto execution_queue and return queue depth."""
        self.execution_queue.put({"enqueued_at": time.time(), "plan": plan})
        return self.execution_queue.qsize()

    def drain_execution_queue(self, max_items: int = 32) -> List[Dict[str, Any]]:
        """Drain up to max_items queued execution plans in FIFO order."""
        drained: List[Dict[str, Any]] = []
        limit = max(1, int(max_items))
        while len(drained) < limit and not self.execution_queue.empty():
            drained.append(self.execution_queue.get_nowait())
            self.execution_queue.task_done()
        return drained

    def forward(
        self,
        hidden_states: torch.Tensor,
        *,
        config: Optional[UniversalControlConfig] = None,
        memory_network: Optional[NeuralMemoryNetwork] = None,
        docdb_memory_vectors: Optional[torch.Tensor] = None,
        visual_marks: Optional[Sequence[Dict[str, Any]]] = None,
        screen_size: Tuple[int, int] = (1280, 800),
        goal_text: str = "",
        legal_action_mask: Optional[torch.Tensor] = None,
        prior_bonuses: Optional[torch.Tensor] = None,
    ) -> Dict[str, Any]:
        """
        Differentiable forward pass for StillSuit / Cherry training across
        memory conditioning, deterministic visual attention, typed action
        proposals, mode selection, and 8-domain routing.
        """
        ctrl_cfg = config or UniversalControlConfig()
        seq_states = _ensure_seq3d(hidden_states)

        if memory_network is not None:
            mem_out, _ = memory_network(seq_states, mode="read")
            seq_states = seq_states + ctrl_cfg.memory_conditioning_weight * mem_out

        if docdb_memory_vectors is not None and docdb_memory_vectors.numel() > 0:
            doc_kv = _ensure_seq3d(docdb_memory_vectors).to(
                device=seq_states.device, dtype=seq_states.dtype
            )
            if doc_kv.shape[0] == 1 and seq_states.shape[0] > 1:
                doc_kv = doc_kv.expand(seq_states.shape[0], -1, -1)
            doc_attn = self.docdb_memory_attn(seq_states, doc_kv)
            seq_states = seq_states + ctrl_cfg.memory_conditioning_weight * doc_attn

        visual_out: Optional[Dict[str, Any]] = None
        if visual_marks:
            visual_out = self.visual_attention_bridge(
                seq_states,
                visual_marks,
                screen_size=screen_size,
                goal_text=goal_text,
            )
            seq_states = seq_states + ctrl_cfg.visual_conditioning_weight * visual_out["attended_states"]

        pooled = seq_states.mean(dim=1)
        typed_action = self.typed_action_head(
            seq_states,
            legal_action_mask=legal_action_mask,
            prior_bonuses=prior_bonuses,
        )
        operation_mode_probs = self.operation_mode_selector(pooled)
        capability_routing = self.capability_router(pooled)

        return {
            "conditioned_states": seq_states,
            "pooled_state": pooled,
            "typed_action": typed_action,
            "operation_mode_probs": operation_mode_probs,
            "capability_routing": capability_routing,
            "visual_attention": visual_out,
        }
    
    @torch.no_grad()
    def generate(self, hidden_states: torch.Tensor,
                 config: Optional[UniversalControlConfig] = None,
                 target_systems: Optional[List[str]] = None,
                 objectives: Optional[Dict[str, Any]] = None,
                 safety_constraints: Optional[Dict[str, Any]] = None,
                 memory_network: Optional[NeuralMemoryNetwork] = None,
                 legal_action_mask: Optional[torch.Tensor] = None,
                 prior_bonuses: Optional[torch.Tensor] = None,
                 visual_marks: Optional[Sequence[Dict[str, Any]]] = None,
                 screen_size: Tuple[int, int] = (1280, 800),
                 intent_query: str = "",
                 docdb_adapter: Optional[DocDBToolMemoryAdapter] = None,
                 stream_callback: Optional[Callable[..., Any]] = None) -> Dict[str, Any]:
        """
        Generate typed BB7 action proposals, DocDB-conditioned tool syntheses,
        deterministic visual attention targets, and 8-domain control plans from
        canonical d_model=512 hidden_states.
        """
        if config is None:
            config = UniversalControlConfig()
        if objectives is None:
            objectives = {'primary': intent_query or 'autonomous_operation'}
        if safety_constraints is None:
            safety_constraints = {'max_risk_level': 0.9}

        active_docdb = docdb_adapter or self.docdb_adapter
        docdb_vecs: Optional[torch.Tensor] = None
        docdb_recalled_meta: List[Dict[str, Any]] = []
        query_str = intent_query or str(objectives.get('primary', ''))
        if active_docdb is not None:
            docdb_vecs, docdb_recalled_meta = active_docdb.recall_conditioning_tensors(
                query_str,
                top_k=4,
                device=hidden_states.device,
                dtype=hidden_states.dtype,
            )

        fwd = self.forward(
            hidden_states,
            config=config,
            memory_network=memory_network,
            docdb_memory_vectors=docdb_vecs,
            visual_marks=visual_marks,
            screen_size=screen_size,
            goal_text=query_str,
            legal_action_mask=legal_action_mask,
            prior_bonuses=prior_bonuses,
        )
        seq_states = fwd["conditioned_states"]
        typed_action = fwd["typed_action"]
        operation_mode_probs = fwd["operation_mode_probs"]
        capability_routing = fwd["capability_routing"]
        visual_out = fwd["visual_attention"]

        selected_mode = (
            config.operation_mode
            if objectives.get("force_operation_mode")
            else OperationMode(torch.argmax(operation_mode_probs[0]).item() + 1)
        )
        primary_domains = [
            ControlDomain(i + 1)
            for i, prob in enumerate(capability_routing[0])
            if prob > 0.20
        ] or [ControlDomain.DIGITAL]
        if visual_out and ControlDomain.OPTICAL not in primary_domains:
            primary_domains.append(ControlDomain.OPTICAL)
        
        generation_result: Dict[str, Any] = {
            'typed_action': typed_action,
            'operation_mode': selected_mode,
            'primary_domains': primary_domains,
            'capability_routing': capability_routing,
            'docdb_recalled': docdb_recalled_meta,
            'visual_attention': visual_out,
            'timestamp': time.time()
        }
        
        if selected_mode in [OperationMode.TOOL_SYNTHESIS, OperationMode.HYBRID_OPERATION]:
            tool_result = self._handle_tool_synthesis(
                seq_states, objectives, config, stream_callback, active_docdb
            )
            generation_result['tool_synthesis'] = tool_result
        
        if selected_mode in [OperationMode.EXTERNAL_CONTROL, OperationMode.HYBRID_OPERATION]:
            control_result = self._handle_external_control(
                seq_states, list(target_systems) if target_systems else None,
                objectives, safety_constraints, config, stream_callback,
                visual_out, active_docdb
            )
            generation_result['external_control'] = control_result
        
        if selected_mode == OperationMode.AUTONOMOUS_DISCOVERY:
            discovery_result = self._handle_autonomous_discovery(
                seq_states, config, stream_callback, active_docdb
            )
            generation_result['autonomous_discovery'] = discovery_result
        
        if len(self.active_systems) > 1:
            coordination_result = self._coordinate_active_systems(seq_states)
            generation_result['coordination'] = coordination_result
        
        self.execution_history.append(generation_result)
        self._update_performance_metrics(generation_result)
        return generation_result
    
    def _handle_tool_synthesis(self, hidden_states: torch.Tensor,
                              objectives: Dict[str, Any],
                              config: UniversalControlConfig,
                              stream_callback: Optional[Callable[..., Any]],
                              active_docdb: Optional[DocDBToolMemoryAdapter] = None) -> Dict[str, Any]:
        existing_tools = list(self.tool_synthesis.tool_genome_registry.values())
        synthesized_tool = self.tool_synthesis.synthesize_tool(
            hidden_states, existing_tools[-5:] if existing_tools else None
        )
        docdb_receipt = None
        if active_docdb is not None and config.persist_to_docdb:
            docdb_receipt = active_docdb.persist_tool_genome(synthesized_tool)
        tool_contexts = [synthesized_tool.functionality_vector.unsqueeze(0)]
        execution_plan = self.execution_orchestrator.orchestrate_execution(
            tool_contexts, objectives
        )
        self.enqueue_execution_plan(execution_plan)
        self.tool_registry[synthesized_tool.genome_id] = synthesized_tool
        
        if stream_callback:
            stream_callback({
                'type': 'tool_synthesized',
                'tool_id': synthesized_tool.genome_id,
                'complexity': synthesized_tool.complexity_score,
                'somnus_urn': synthesized_tool.somnus_urn,
            })
        
        return {
            'synthesized_tool': synthesized_tool,
            'execution_plan': execution_plan,
            'docdb_receipt': docdb_receipt,
            'tool_count': len(self.tool_registry),
            'synthesis_successful': True
        }

    def _derive_probe_vectors(self, hidden_states: torch.Tensor, count: int) -> List[torch.Tensor]:
        """Derive deterministic subspace probe vectors from hidden_states (zero torch.randn)."""
        pooled = _pool_2d(hidden_states)[0]
        expanded = self.discovery_probe_proj(pooled).view(4, self.hidden_size)
        probes: List[torch.Tensor] = []
        for idx in range(max(1, count)):
            base = expanded[idx % 4]
            scale = 1.0 + 0.05 * float(idx)
            probes.append(F.normalize(base * scale + pooled * 0.25, dim=-1))
        return probes
    
    def _handle_external_control(self, hidden_states: torch.Tensor,
                                target_systems: Optional[List[str]],
                                objectives: Dict[str, Any],
                                safety_constraints: Dict[str, Any],
                                config: UniversalControlConfig,
                                stream_callback: Optional[Callable[..., Any]],
                                visual_attention: Optional[Dict[str, Any]] = None,
                                active_docdb: Optional[DocDBToolMemoryAdapter] = None) -> Dict[str, Any]:
        _ = objectives
        control_results = {}
        
        if not target_systems or config.auto_discovery:
            discovered_systems = self._auto_discover_systems(hidden_states, config, active_docdb)
            if target_systems:
                for sys_prof in discovered_systems:
                    if sys_prof.system_id not in target_systems:
                        target_systems.append(sys_prof.system_id)
            else:
                target_systems = [sys_prof.system_id for sys_prof in discovered_systems]
        
        probes = self._derive_probe_vectors(hidden_states, max(1, len(target_systems)))
        for idx, system_id in enumerate(target_systems):
            if system_id in self.active_systems:
                system_profile = self.active_systems[system_id]
            else:
                system_profile = self.system_discovery.discover_system(probes[idx])
                if active_docdb is not None and config.persist_to_docdb:
                    active_docdb.persist_system_profile(system_profile)
                self.active_systems[system_id] = system_profile
            
            interface_adaptation = self.interface_adaptation.adapt_interface(
                system_profile, hidden_states
            )
            command = self.command_synthesis.synthesize_command(
                system_profile, hidden_states, safety_constraints
            )
            safety_validation = self.safety_validator.validate_safety(
                hidden_states, system_profile, safety_constraints
            )
            
            active_domains = list(system_profile.control_domains)
            if visual_attention and ControlDomain.OPTICAL not in active_domains:
                active_domains.append(ControlDomain.OPTICAL)

            domain_controls = {}
            for domain in active_domains:
                dkey = domain.name.lower()
                if dkey in self.control_heads:
                    control_head = self.control_heads[dkey]
                    if dkey == 'digital':
                        domain_controls[domain.name] = control_head.generate_control_signals(
                            hidden_states, system_profile
                        )
                    elif dkey == 'mechanical':
                        domain_controls[domain.name] = control_head.generate_motion_control(
                            hidden_states, system_profile
                        )
                    elif dkey == 'analog':
                        domain_controls[domain.name] = control_head.generate_analog_control(
                            hidden_states, system_profile
                        )
                    elif dkey == 'electromagnetic':
                        domain_controls[domain.name] = control_head.generate_em_control(
                            hidden_states, system_profile
                        )
                    elif dkey == 'optical':
                        domain_controls[domain.name] = control_head.generate_optical_control(
                            hidden_states, system_profile, visual_attention=visual_attention
                        )
                    elif dkey == 'chemical':
                        domain_controls[domain.name] = control_head.generate_chemical_control(
                            hidden_states, system_profile
                        )
                    elif dkey == 'biological':
                        domain_controls[domain.name] = control_head.generate_biological_control(
                            hidden_states, system_profile
                        )
                    elif dkey == 'quantum':
                        domain_controls[domain.name] = control_head.generate_quantum_control(
                            hidden_states, system_profile
                        )
            
            control_results[system_id] = {
                'system_profile': system_profile,
                'interface_adaptation': interface_adaptation,
                'command': command,
                'safety_validation': safety_validation,
                'domain_controls': domain_controls,
                'control_ready': safety_validation['safe_to_execute']
            }
            
            if stream_callback:
                stream_callback({
                    'type': 'system_controlled',
                    'system_id': system_id,
                    'safety_score': safety_validation['overall_safety_score']
                })
        
        return {
            'controlled_systems': control_results,
            'total_systems': len(target_systems),
            'control_successful': all(
                result['control_ready'] for result in control_results.values()
            )
        }
    
    def _handle_autonomous_discovery(self, hidden_states: torch.Tensor,
                                   config: UniversalControlConfig,
                                   stream_callback: Optional[Callable[..., Any]],
                                   active_docdb: Optional[DocDBToolMemoryAdapter] = None) -> Dict[str, Any]:
        discovered_systems = self._auto_discover_systems(hidden_states, config, active_docdb)
        topology_embeddings = self.system_discovery.map_system_topology(discovered_systems)
        protocol = (
            self.protocol_synthesis.synthesize_protocol(hidden_states, discovered_systems)
            if len(discovered_systems) > 1
            else None
        )
        if len(discovered_systems) > 0:
            system_contexts = self._derive_probe_vectors(hidden_states, len(discovered_systems))
            coordination_plan = self.multi_system_coordinator.coordinate_systems(
                system_contexts, discovered_systems
            )
        else:
            coordination_plan = None
        
        if stream_callback:
            stream_callback({
                'type': 'discovery_complete',
                'systems_found': len(discovered_systems),
                'protocol_synthesized': protocol is not None
            })
        
        return {
            'discovered_systems': discovered_systems,
            'topology_embeddings': topology_embeddings,
            'communication_protocol': protocol,
            'coordination_plan': coordination_plan,
            'discovery_successful': len(discovered_systems) > 0
        }
    
    def _auto_discover_systems(self, hidden_states: torch.Tensor,
                              config: UniversalControlConfig,
                              active_docdb: Optional[DocDBToolMemoryAdapter] = None) -> List[SystemProfile]:
        discovered_systems: List[SystemProfile] = []
        max_discovery_attempts = min(config.max_concurrent_systems, 4)
        probes = self._derive_probe_vectors(hidden_states, max_discovery_attempts)
        for probe_data in probes:
            system_profile = self.system_discovery.discover_system(probe_data)
            if system_profile.system_id not in [sys.system_id for sys in discovered_systems]:
                if active_docdb is not None and config.persist_to_docdb:
                    active_docdb.persist_system_profile(system_profile)
                discovered_systems.append(system_profile)
                self.active_systems[system_profile.system_id] = system_profile
        return discovered_systems
    
    def _coordinate_active_systems(self, hidden_states: torch.Tensor) -> Dict[str, Any]:
        active_profiles = list(self.active_systems.values())
        system_contexts = self._derive_probe_vectors(hidden_states, len(active_profiles))
        return self.multi_system_coordinator.coordinate_systems(
            system_contexts, active_profiles
        )
    
    def _update_performance_metrics(self, generation_result: Dict[str, Any]) -> None:
        if 'tool_synthesis' in generation_result:
            self.performance_metrics['tools_synthesized'] += 1
            if generation_result['tool_synthesis']['synthesis_successful']:
                self.performance_metrics['successful_syntheses'] += 1
        
        if 'external_control' in generation_result:
            controlled_count = generation_result['external_control']['total_systems']
            self.performance_metrics['systems_controlled'] += controlled_count
            if generation_result['external_control']['control_successful']:
                self.performance_metrics['successful_controls'] += controlled_count
        
        if 'autonomous_discovery' in generation_result:
            discovered_count = len(generation_result['autonomous_discovery']['discovered_systems'])
            self.performance_metrics['systems_discovered'] += discovered_count

        if generation_result.get('visual_attention') and generation_result['visual_attention'].get('mark_count', 0) > 0:
            self.performance_metrics['visual_attentions_resolved'] += 1
        
        if self.performance_metrics['tools_synthesized'] > 0:
            self.performance_metrics['synthesis_success_rate'] = (
                self.performance_metrics['successful_syntheses'] / 
                self.performance_metrics['tools_synthesized']
            )
        
        if self.performance_metrics['systems_controlled'] > 0:
            self.performance_metrics['control_success_rate'] = (
                self.performance_metrics['successful_controls'] / 
                self.performance_metrics['systems_controlled']
            )
    
    async def generate_async(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Asynchronous generation for non-blocking operation."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, lambda: self.generate(*args, **kwargs))
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance, domain, queue, and DocDB binding summary."""
        return {
            'metrics': dict(self.performance_metrics),
            'active_systems_count': len(self.active_systems),
            'tool_registry_size': len(self.tool_registry),
            'execution_history_size': len(self.execution_history),
            'execution_queue_depth': self.execution_queue.qsize(),
            'control_domains_registered': sorted(self.control_heads.keys()),
            'docdb_attached': self.docdb_adapter is not None,
            'docdb_path': str(self.docdb_adapter.docdb_path) if self.docdb_adapter else None,
            'system_discovery_cache_size': len(self.system_discovery.discovered_systems),
            'interface_adaptation_cache_size': len(self.interface_adaptation.adaptation_memory)
        }
    
    def reset_state(self) -> None:
        """Reset all internal state for fresh operation."""
        self.active_systems.clear()
        self.tool_registry.clear()
        self.execution_history.clear()
        self.performance_metrics.clear()
        self.system_discovery.discovered_systems.clear()
        self.interface_adaptation.adaptation_memory.clear()
        self.drain_execution_queue(max_items=10000)

class ToolModalityOrgan:
    """
    Compiled BB7 Intelligence Surface for Muad'Dib's Universal Tool Modality.

    Calls and gathers multiple neural/symbolic subsystems across UniversalToolControlOutputHead,
    DocDBToolMemoryAdapter (docdb.sqlite WAL + Somnus 2.2.0 URNs + HNFP),
    DigitalTwinTool (Q-table & co-occurrence priors), and VisualTool (Set-of-Mark
    deterministic spatial UI grounding), returning dual-surface BB7Response envelopes.
    """

    def __init__(
        self,
        data_dir: Optional[Union[str, Path]] = None,
        config: Optional[NeuralNetConfig] = None,
        memory_tool: Optional[Any] = None,
        digital_twin: Optional[Any] = None,
        visual_tool: Optional[Any] = None,
        hydrate_on_init: bool = False,
    ) -> None:
        """Initialize ToolModalityOrgan with DocDB adapter and 8-domain control head."""
        self.logger = logging.getLogger(__name__)
        self.data_dir: Path = _resolve_sovereign_data_dir(data_dir)
        self.config: NeuralNetConfig = config or NeuralNetConfig()
        self.docdb_adapter = DocDBToolMemoryAdapter(
            data_dir=self.data_dir, memory_tool=memory_tool, d_model=self.config.d_model
        )
        self.head = UniversalToolControlOutputHead(
            config=self.config, docdb_adapter=self.docdb_adapter
        ).eval()
        self.digital_twin: Optional[Any] = digital_twin
        self.visual_tool: Optional[Any] = visual_tool
        self._plane_tools: Dict[str, Callable[..., Any]] = {}
        self._plane_modules: Dict[str, Any] = {}
        self._live_tool_invoker: Optional[Callable[..., Any]] = None
        if hydrate_on_init:
            self.docdb_adapter.hydrate_into_head(self.head)

    @staticmethod
    def _unpack_args(
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Normalize dual calling convention (fn(dict) and fn(**kwargs))."""
        merged: Dict[str, Any] = {}
        if isinstance(arguments, dict):
            merged.update(arguments)
        merged.update(kwargs)
        return merged

    def attach_tool_plane(
        self,
        tools: Dict[str, Callable[..., Any]],
        tool_modules: Dict[str, Any],
        live_tool_invoker: Optional[Callable[..., Any]] = None,
    ) -> Dict[str, Any]:
        """Bind ToolModalityOrgan to sibling DocDB memory, VisualTool, and DigitalTwinTool."""
        self._plane_tools = dict(tools or {})
        self._plane_modules = dict(tool_modules or {})
        self._live_tool_invoker = live_tool_invoker

        for key in ("tools.memory_tool", "memory_tool"):
            mem_mod = self._plane_modules.get(key)
            if mem_mod is not None:
                self.docdb_adapter.attach_memory_tool(mem_mod)
                break

        for key in ("tools.visual_tool", "visual_tool"):
            vis_mod = self._plane_modules.get(key)
            if vis_mod is not None:
                self.visual_tool = vis_mod
                break

        for key in ("tools.exoskeleton_tool", "exoskeleton_tool"):
            exo_mod = self._plane_modules.get(key)
            if exo_mod is not None and self.digital_twin is None:
                twin = getattr(exo_mod, "_digital_twin", None)
                if twin is not None:
                    self.digital_twin = twin
                break

        return {
            "success": True,
            "docdb_path": str(self.docdb_adapter.docdb_path),
            "visual_bound": self.visual_tool is not None,
            "digital_twin_bound": self.digital_twin is not None,
            "bound_tools": len(self._plane_tools),
        }

    def _resolve_visual_tool(self) -> Optional[Any]:
        """Return bound VisualTool or lazy-instantiate one isolated to self.data_dir."""
        if self.visual_tool is not None:
            return self.visual_tool
        try:
            from tools.visual_tool import VisualTool

            self.visual_tool = VisualTool(data_dir=self.data_dir)
            return self.visual_tool
        except (ImportError, OSError, RuntimeError) as exc:
            logger.error("VisualTool lazy resolution failed: %s", exc)
            return None

    def _build_prior_and_mask(
        self,
        candidate_tools: Optional[Sequence[str]],
        category: str = "misc",
        session_id: str = "default",
    ) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor], Dict[str, int]]:
        """Build legal_action_mask and Q/co-occur prior_bonuses from candidate_tools."""
        if not candidate_tools:
            return None, None, {}
        vocab_map: Dict[str, int] = {}
        for idx, name in enumerate(candidate_tools):
            if self.digital_twin is not None and hasattr(self.digital_twin, "_tool_id"):
                tid = int(self.digital_twin._tool_id(str(name)))
            else:
                digest = hashlib.blake2b(str(name).encode("utf-8"), digest_size=4).digest()
                tid = (int.from_bytes(digest, "little") % (self.config.vocab_size - 1)) + 1
            vocab_map[str(name)] = tid

        mask = torch.zeros((1, self.config.vocab_size), dtype=torch.bool)
        for tid in vocab_map.values():
            if 0 <= tid < self.config.vocab_size:
                mask[0, tid] = True

        bonuses = torch.zeros((1, self.config.vocab_size), dtype=torch.float32)
        if self.digital_twin is not None and hasattr(self.digital_twin, "bb7_dt_advanced_features"):
            adv = self.digital_twin.bb7_dt_advanced_features(
                candidates=list(vocab_map.keys()),
                category=category,
                session_id=session_id,
            )
            feats = adv.get("features", {}) if isinstance(adv, dict) else {}
            for tname, fdict in feats.items():
                tid = vocab_map.get(tname)
                if tid is not None and isinstance(fdict, dict):
                    bonuses[0, tid] = 0.20 * float(fdict.get("effective_score", 0.0))

        return mask, bonuses, vocab_map

    def bb7_tm_propose_action(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Compile a legal-masked typed action proposal by gathering DocDB 512-D
        memory conditioning, DigitalTwin Q/co-occurrence priors, optional
        Set-of-Mark visual attention, TypedToolActionHead, and SafetyValidationEngine.
        """
        params = self._unpack_args(arguments, **kwargs)
        intent = str(params.get("intent") or params.get("query") or "autonomous_operation").strip()
        candidates = [str(c) for c in (params.get("candidate_tools") or []) if str(c).strip()]
        category = str(params.get("category") or "misc")
        session_id = str(params.get("session_id") or "default")
        visual_source = params.get("visual_marks")

        seq_states = _text_to_canonical_sequence(intent, d_model=self.config.d_model)
        docdb_vecs, recalled_meta = self.docdb_adapter.recall_conditioning_tensors(
            intent, top_k=int(params.get("max_memories", 4))
        )
        mask, bonuses, vocab_map = self._build_prior_and_mask(
            candidates, category=category, session_id=session_id
        )
        reverse_vocab = {tid: name for name, tid in vocab_map.items()}

        marks: List[Dict[str, Any]] = []
        screen_sz = (1280, 800)
        if visual_source is not None:
            marks, screen_sz, _ = DeterministicVisualAttentionBridge.extract_marks_from_observation(
                visual_source
            )

        with torch.no_grad():
            fwd = self.head(
                seq_states,
                docdb_memory_vectors=docdb_vecs,
                visual_marks=marks or None,
                screen_size=screen_sz,
                goal_text=intent,
                legal_action_mask=mask,
                prior_bonuses=bonuses,
            )
            typed = fwd["typed_action"]
            probe_prof = self.head.system_discovery.discover_system(fwd["pooled_state"])
            safety = self.head.safety_validator.validate_safety(
                fwd["conditioned_states"],
                probe_prof,
                dict(params.get("safety_constraints") or {"max_risk_level": 0.9}),
            )

        top_ids = typed["top_tool_ids"][0].tolist()
        top_probs = [round(float(p), 4) for p in typed["top_tool_probs"][0].tolist()]
        ranked_proposals = [
            {
                "tool_id": int(tid),
                "tool_name": reverse_vocab.get(int(tid), f"tool_vocab_{tid}"),
                "probability": prob,
            }
            for tid, prob in zip(top_ids, top_probs)
        ]
        vis_summary = None
        if fwd["visual_attention"] is not None:
            vis_summary = {
                "selected_mark_id": fwd["visual_attention"]["selected_mark_id"],
                "selected_evidence_token": fwd["visual_attention"]["selected_evidence_token"],
                "mark_count": fwd["visual_attention"]["mark_count"],
            }

        structured = {
            "status": "ok",
            "intent": intent,
            "selected_action_kind": typed["selected_action_kind"],
            "top_proposals": ranked_proposals,
            "value_estimate": round(float(typed["value_estimate"].item()), 4),
            "uncertainty": round(float(typed["uncertainty"].item()), 4),
            "abstention_prob": round(float(typed["abstention_prob"].item()), 4),
            "arg_slot_shape": list(typed["argument_slot_vectors"].shape),
            "safe_to_execute": bool(safety["safe_to_execute"]),
            "safety_score": round(float(safety["overall_safety_score"]), 4),
            "docdb_memories_conditioned": len(recalled_meta),
            "visual_attention": vis_summary,
        }
        best_name = ranked_proposals[0]["tool_name"] if ranked_proposals else "none"
        narrative = (
            f"Typed Action Proposal for '{intent}': kind={typed['selected_action_kind']}, "
            f"top_tool={best_name}, safety={structured['safety_score']:.3f} "
            f"(DocDB memories={len(recalled_meta)})"
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=recalled_meta,
            sql_context={"docdb_path": str(self.docdb_adapter.docdb_path)},
            tool_name="bb7_tm_propose_action",
            modality="tool",
        )

    def bb7_tm_discover_systems(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Discover and profile capability systems across all 8 ControlDomains,
        map inter-system GNN topology, adapt interfaces, synthesize protocols,
        and persist profiles to DocDB with Somnus UUIDv7 URNs.
        """
        params = self._unpack_args(arguments, **kwargs)
        probe_context = str(params.get("context") or params.get("intent") or "system_discovery").strip()
        probe_count = max(1, min(8, int(params.get("probe_count", 3))))
        persist = bool(params.get("persist_to_docdb", True))

        seq_states = _text_to_canonical_sequence(probe_context, d_model=self.config.d_model)
        cfg = UniversalControlConfig(
            operation_mode=OperationMode.AUTONOMOUS_DISCOVERY,
            max_concurrent_systems=probe_count,
            persist_to_docdb=persist,
        )
        with torch.no_grad():
            probes = self.head._derive_probe_vectors(seq_states, probe_count)
            profiles: List[SystemProfile] = []
            receipts: List[Dict[str, Any]] = []
            for p_vec in probes:
                prof = self.head.system_discovery.discover_system(p_vec)
                if prof.system_id not in {s.system_id for s in profiles}:
                    if persist:
                        receipts.append(self.docdb_adapter.persist_system_profile(prof))
                    self.head.active_systems[prof.system_id] = prof
                    profiles.append(prof)

            topo = self.head.system_discovery.map_system_topology(profiles)
            adaptations = {
                prof.system_id: bool(
                    self.head.interface_adaptation.adapt_interface(prof, seq_states)["interface_ready"]
                )
                for prof in profiles
            }
            proto = (
                self.head.protocol_synthesis.synthesize_protocol(seq_states, profiles)
                if len(profiles) > 1
                else None
            )
            coord = (
                self.head.multi_system_coordinator.coordinate_systems(
                    probes[: len(profiles)], profiles
                )
                if len(profiles) > 1
                else {"coordination_needed": False}
            )

        structured = {
            "status": "ok",
            "context": probe_context,
            "systems_discovered": len(profiles),
            "profiles": [p.to_dict() for p in profiles],
            "topology_shape": list(topo.shape) if topo is not None else [],
            "interface_adaptations_ready": adaptations,
            "protocol_id": proto["protocol_id"] if proto else None,
            "coordination_needed": bool(coord.get("coordination_needed", False)),
            "docdb_receipts": receipts,
        }
        narrative = (
            f"Discovered {len(profiles)} system profile(s) for '{probe_context}'; "
            f"protocol={structured['protocol_id'] or 'single_node'}; persisted={len(receipts)} in DocDB."
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=receipts,
            sql_context={"docdb_path": str(self.docdb_adapter.docdb_path)},
            tool_name="bb7_tm_discover_systems",
            modality="tool",
        )

    def bb7_tm_synthesize_genome(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Synthesize or evolve a 512-D ToolGenome conditioned on DocDB parent recall,
        decode its 4096-D implementation blueprint, build its GNN ExecutionOrchestrator
        schedule, and persist the genome + Somnus URN into DocDB.
        """
        params = self._unpack_args(arguments, **kwargs)
        requirement = str(params.get("requirement") or params.get("intent") or "compositional_tool").strip()
        feedback = params.get("performance_feedback")
        base_genome_id = str(params.get("base_genome_id") or "").strip()
        persist = bool(params.get("persist_to_docdb", True))

        if not self.head.tool_registry:
            self.docdb_adapter.hydrate_into_head(self.head)

        seq_states = _text_to_canonical_sequence(requirement, d_model=self.config.d_model)
        docdb_vecs, recalled_meta = self.docdb_adapter.recall_conditioning_tensors(
            f"tool_genome {requirement}", top_k=3
        )
        if docdb_vecs is not None:
            with torch.no_grad():
                attn_out = self.head.docdb_memory_attn(seq_states, docdb_vecs)
                seq_states = seq_states + 0.30 * attn_out

        with torch.no_grad():
            if base_genome_id and base_genome_id in self.head.tool_synthesis.tool_genome_registry and isinstance(feedback, dict):
                base_g = self.head.tool_synthesis.tool_genome_registry[base_genome_id]
                genome = self.head.tool_synthesis.evolve_tool(base_g, feedback)
                action_taken = "evolved"
            else:
                parents = list(self.head.tool_synthesis.tool_genome_registry.values())[-5:]
                genome = self.head.tool_synthesis.synthesize_tool(
                    seq_states, parents if parents else None
                )
                action_taken = "synthesized"

            self.head.tool_registry[genome.genome_id] = genome
            plan = self.head.execution_orchestrator.orchestrate_execution(
                [genome.functionality_vector.unsqueeze(0)],
                {"primary": requirement, "max_parallel": int(params.get("max_parallel", 3))},
            )
            q_depth = self.head.enqueue_execution_plan(plan)

        receipt = self.docdb_adapter.persist_tool_genome(genome) if persist else None
        structured = {
            "status": "ok",
            "mode": action_taken,
            "requirement": requirement,
            "genome": genome.to_dict(include_vector=False),
            "execution_plan": {
                "tool_count": plan["tool_count"],
                "parallel_groups": plan["parallel_groups"],
                "estimated_duration": round(float(plan["estimated_duration"]), 4),
                "critical_path": plan["critical_path"],
            },
            "queue_depth": q_depth,
            "docdb_receipt": receipt,
        }
        narrative = (
            f"ToolGenome {action_taken}: id={genome.genome_id} (gen={genome.evolution_generation}, "
            f"call_mode={(genome.implementation_blueprint or {}).get('call_mode')}, "
            f"safety={genome.safety_rating:.3f}, urn={genome.somnus_urn})"
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=recalled_meta,
            sql_context={"docdb_path": str(self.docdb_adapter.docdb_path)},
            tool_name="bb7_tm_synthesize_genome",
            modality="tool",
        )

    def bb7_tm_universal_control(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Execute full UniversalToolControlOutputHead orchestration across all 8
        ControlDomains, SafetyValidationEngine, CommandSynthesisEngine, and DocDB
        outcome logging.
        """
        params = self._unpack_args(arguments, **kwargs)
        objective_str = str(params.get("objective") or params.get("intent") or "autonomous_operation").strip()
        mode_name = str(params.get("operation_mode") or "").strip().upper()
        safety_constraints = dict(params.get("safety_constraints") or {"max_risk_level": 0.9})
        candidates = [str(c) for c in (params.get("candidate_tools") or []) if str(c).strip()]

        ctrl_cfg = UniversalControlConfig(
            persist_to_docdb=bool(params.get("persist_to_docdb", True))
        )
        objectives: Dict[str, Any] = {"primary": objective_str}
        if mode_name in OperationMode.__members__:
            ctrl_cfg.operation_mode = OperationMode[mode_name]
            objectives["force_operation_mode"] = True

        mask, bonuses, _ = self._build_prior_and_mask(candidates)
        seq_states = _text_to_canonical_sequence(objective_str, d_model=self.config.d_model)
        result = self.head.generate(
            seq_states,
            config=ctrl_cfg,
            target_systems=params.get("target_systems"),
            objectives=objectives,
            safety_constraints=safety_constraints,
            legal_action_mask=mask,
            prior_bonuses=bonuses,
            intent_query=objective_str,
            docdb_adapter=self.docdb_adapter,
        )

        controlled = result.get("external_control", {}).get("controlled_systems", {})
        domains_engaged = sorted(
            {
                dom_name
                for sys_res in controlled.values()
                for dom_name in sys_res.get("domain_controls", {}).keys()
            }
        )
        outcome_id = hashlib.blake2b(
            f"{objective_str}:{time.time_ns()}".encode("utf-8"), digest_size=6
        ).hexdigest()
        outcome_summary = {
            "objective": objective_str,
            "operation_mode": result["operation_mode"].name,
            "primary_domains": [d.name for d in result["primary_domains"]],
            "domains_engaged": domains_engaged,
            "controlled_systems_count": len(controlled),
            "control_successful": bool(result.get("external_control", {}).get("control_successful", True)),
        }
        outcome_receipt = (
            self.docdb_adapter.persist_control_outcome(outcome_id, outcome_summary)
            if ctrl_cfg.persist_to_docdb
            else None
        )
        structured = {
            "status": "ok",
            **outcome_summary,
            "selected_action_kind": result["typed_action"]["selected_action_kind"],
            "synthesized_genome_id": (
                result["tool_synthesis"]["synthesized_tool"].genome_id
                if "tool_synthesis" in result
                else None
            ),
            "docdb_recalled_count": len(result.get("docdb_recalled", [])),
            "outcome_receipt": outcome_receipt,
        }
        narrative = (
            f"Universal Control Dispatch [{outcome_summary['operation_mode']}]: "
            f"domains={domains_engaged or [d.name for d in result['primary_domains']]}, "
            f"systems={len(controlled)}, ok={outcome_summary['control_successful']}"
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=result.get("docdb_recalled", []),
            sql_context={"docdb_path": str(self.docdb_adapter.docdb_path)},
            tool_name="bb7_tm_universal_control",
            modality="tool",
        )

    def bb7_tm_visual_attend(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Deterministic Visual Attention Compiler: grounds the screen via VisualTool's
        Set-of-Mark engine (or supplied marks / visual_cognition.db), runs canonical
        512-D DeterministicVisualAttentionBridge + OpticalControlHead, selects the
        target UI mark and verified one-use evidence_token, and optionally actuates.
        """
        params = self._unpack_args(arguments, **kwargs)
        goal = str(params.get("goal") or params.get("intent") or "Inspect Telemetry").strip()
        actuate = bool(params.get("actuate", False))
        click_type = str(params.get("click_type", "left")).strip().lower()
        supplied_marks = params.get("marks")

        vis_tool = self._resolve_visual_tool()
        grounding_resp = None
        if supplied_marks is not None:
            marks, screen_sz, grounding_id = DeterministicVisualAttentionBridge.extract_marks_from_observation(
                supplied_marks
            )
        elif vis_tool is not None:
            grounding_resp = vis_tool.bb7_ui_ground_screen(
                {"region": params.get("region", "fullscreen")}
            )
            marks, screen_sz, grounding_id = DeterministicVisualAttentionBridge.extract_marks_from_observation(
                grounding_resp, visual_db_path=getattr(vis_tool, "db_path", None)
            )
        else:
            return BB7Response(
                "Error: VisualTool unavailable and no marks provided.",
                structured={"status": "error", "reason": "visual_unavailable"},
                tool_name="bb7_tm_visual_attend",
                modality="mixed",
            )

        seq_states = _text_to_canonical_sequence(goal, d_model=self.config.d_model)
        docdb_vecs, recalled_meta = self.docdb_adapter.recall_conditioning_tensors(
            f"visual ui {goal}", top_k=3
        )
        with torch.no_grad():
            fwd = self.head(
                seq_states,
                docdb_memory_vectors=docdb_vecs,
                visual_marks=marks,
                screen_size=screen_sz,
                goal_text=goal,
            )
            vis_attn = fwd["visual_attention"] or {}
            ui_profile = SystemProfile(
                system_id="sovereign_ui_surface",
                system_type="deterministic_som_display",
                capabilities={"som_marks": float(len(marks))},
                interfaces=["visual_cognition_wal"],
                control_domains=[ControlDomain.OPTICAL, ControlDomain.DIGITAL],
                safety_constraints={"max_risk_level": 0.95},
                communication_protocols=["som_evidence_token"],
                resource_requirements={"cpu_usage": 0.05, "memory_mb": 32.0},
                reliability_score=0.98,
                last_updated=time.time(),
            )
            optical_ctrl = self.head.control_heads["optical"].generate_optical_control(
                fwd["conditioned_states"], ui_profile, visual_attention=vis_attn
            )

        actuation_result: Optional[Dict[str, Any]] = None
        selected_token = vis_attn.get("selected_evidence_token")
        selected_mark_id = vis_attn.get("selected_mark_id")
        if actuate and vis_tool is not None and (selected_token or selected_mark_id is not None):
            click_resp = vis_tool.bb7_click_element(
                {
                    "evidence_token": selected_token or "",
                    "mark_id": selected_mark_id,
                    "click_type": click_type,
                }
            )
            actuation_result = dict(click_resp.structured)

        structured = {
            "status": "ok",
            "goal": goal,
            "grounding_id": grounding_id,
            "mark_count": len(marks),
            "selected_mark_id": selected_mark_id,
            "selected_mark": vis_attn.get("selected_mark"),
            "selected_evidence_token": selected_token,
            "ranked_marks": vis_attn.get("ranked_marks", []),
            "roi_normalized_bbox": [
                round(float(v), 4) for v in optical_ctrl["roi_normalized_bbox"][0].tolist()
            ],
            "actuated": bool(actuation_result is not None),
            "actuation_result": actuation_result,
        }
        sel_lbl = (vis_attn.get("selected_mark") or {}).get("label", "none")
        narrative = (
            f"Deterministic Visual Attention for '{goal}': selected mark [{selected_mark_id}] "
            f"'{sel_lbl}' across {len(marks)} grounded marks (actuated={structured['actuated']})."
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=recalled_meta,
            sql_context={
                "docdb_path": str(self.docdb_adapter.docdb_path),
                "visual_db_path": str(getattr(vis_tool, "db_path", "")) if vis_tool else "",
            },
            tool_name="bb7_tm_visual_attend",
            modality="mixed",
        )

    def bb7_tm_status_and_memory_sync(
        self,
        arguments: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> BB7Response:
        """
        Synchronize persisted ToolGenomes and SystemProfiles with DocDB, drain
        pending queued execution plans if requested, and return full 8-domain
        Tool Modality + DocDB + DigitalTwin diagnostics.
        """
        params = self._unpack_args(arguments, **kwargs)
        hydrate = bool(params.get("hydrate", True))
        drain_queue = bool(params.get("drain_queue", False))

        hydration_stats = (
            self.docdb_adapter.hydrate_into_head(self.head)
            if hydrate
            else {"genomes_loaded": 0, "systems_loaded": 0}
        )
        drained = self.head.drain_execution_queue() if drain_queue else []
        summary = self.head.get_performance_summary()
        twin_vocab = (
            len(getattr(self.digital_twin, "_tool_vocab", {}))
            if self.digital_twin is not None
            else 0
        )

        structured = {
            "status": "ok",
            "d_model": self.config.d_model,
            "hydration": hydration_stats,
            "drained_queue_items": len(drained),
            "performance_summary": summary,
            "digital_twin_vocab_size": twin_vocab,
            "visual_tool_bound": self.visual_tool is not None,
        }
        narrative = (
            f"ToolModality Status (d_model={self.config.d_model}): "
            f"domains={len(summary['control_domains_registered'])}/8, "
            f"genomes={summary['tool_registry_size']} (hydrated={hydration_stats['genomes_loaded']}), "
            f"systems={summary['active_systems_count']} (hydrated={hydration_stats['systems_loaded']})."
        )
        return BB7Response(
            narrative,
            structured=structured,
            evidence=[],
            sql_context={"docdb_path": str(self.docdb_adapter.docdb_path)},
            tool_name="bb7_tm_status_and_memory_sync",
            modality="structured",
        )

    def get_tools(self) -> Dict[str, Dict[str, Any]]:
        """Return MCP/Exoskeleton-compatible definitions for all 6 compiled bb7_tm_* tools."""
        return {
            "bb7_tm_propose_action": {
                "function": self.bb7_tm_propose_action,
                "description": (
                    "Compile a legal-masked typed BB7 action proposal fusing DocDB 512-D "
                    "memory recall, DigitalTwin Q-priors, optional Set-of-Mark visual "
                    "attention, TypedToolActionHead, and SafetyValidationEngine."
                ),
                "parameters": [
                    {"name": "intent", "type": "string", "description": "Action intent or objective.", "required": True},
                    {"name": "candidate_tools", "type": "array", "description": "Legal candidate tool names.", "required": False},
                    {"name": "category", "type": "string", "description": "Capability category.", "required": False},
                    {"name": "session_id", "type": "string", "description": "Active session ID.", "required": False},
                ],
            },
            "bb7_tm_discover_systems": {
                "function": self.bb7_tm_discover_systems,
                "description": (
                    "Discover and profile external/internal systems across all 8 ControlDomains, "
                    "map GNN topology, adapt interfaces, synthesize protocols, and persist to DocDB."
                ),
                "parameters": [
                    {"name": "context", "type": "string", "description": "Target discovery domain/context.", "required": True},
                    {"name": "probe_count", "type": "integer", "description": "Subspace probes to run (1-8).", "required": False},
                    {"name": "persist_to_docdb", "type": "boolean", "description": "Persist discovered profiles to DocDB.", "required": False},
                ],
            },
            "bb7_tm_synthesize_genome": {
                "function": self.bb7_tm_synthesize_genome,
                "description": (
                    "Synthesize or evolve a 512-D compositional ToolGenome conditioned on DocDB "
                    "parent genomes, decode its executable blueprint, schedule dependencies, and persist to DocDB."
                ),
                "parameters": [
                    {"name": "requirement", "type": "string", "description": "Capability requirement to synthesize.", "required": True},
                    {"name": "base_genome_id", "type": "string", "description": "Optional parent genome_id to evolve.", "required": False},
                    {"name": "performance_feedback", "type": "object", "description": "Empirical feedback dict for evolution.", "required": False},
                ],
            },
            "bb7_tm_universal_control": {
                "function": self.bb7_tm_universal_control,
                "description": (
                    "Run UniversalToolControlOutputHead across all 8 ControlDomains (Digital, "
                    "Mechanical, Analog, Electromagnetic, Optical, Chemical, Biological, Quantum) "
                    "with safety validation and DocDB outcome persistence."
                ),
                "parameters": [
                    {"name": "objective", "type": "string", "description": "Primary control objective.", "required": True},
                    {"name": "operation_mode", "type": "string", "description": "TOOL_SYNTHESIS | EXTERNAL_CONTROL | HYBRID_OPERATION | AUTONOMOUS_DISCOVERY", "required": False},
                    {"name": "safety_constraints", "type": "object", "description": "Safety envelope limits.", "required": False},
                ],
            },
            "bb7_tm_visual_attend": {
                "function": self.bb7_tm_visual_attend,
                "description": (
                    "Deterministic Set-of-Mark Visual Attention Compiler: grounds UI elements via "
                    "VisualTool, runs canonical 512-D cross-attention + OpticalControlHead to select "
                    "the target mark and verified click evidence_token, and optionally actuates."
                ),
                "parameters": [
                    {"name": "goal", "type": "string", "description": "UI interaction target or goal.", "required": True},
                    {"name": "actuate", "type": "boolean", "description": "Execute verified click immediately when true.", "required": False},
                    {"name": "region", "type": "string", "description": "Screen region or 'fullscreen'.", "required": False},
                ],
            },
            "bb7_tm_status_and_memory_sync": {
                "function": self.bb7_tm_status_and_memory_sync,
                "description": (
                    "Hydrate persisted ToolGenomes and SystemProfiles from DocDB and inspect "
                    "8-domain UniversalToolControlOutputHead telemetry and queue state."
                ),
                "parameters": [
                    {"name": "hydrate", "type": "boolean", "description": "Hydrate genomes/systems from DocDB.", "required": False},
                    {"name": "drain_queue", "type": "boolean", "description": "Drain queued execution plans.", "required": False},
                ],
            },
        }


__all__ = [
    'BB7Response',
    'UniversalToolControlOutputHead',
    'TypedToolActionHead',
    'DeterministicVisualAttentionBridge',
    'DocDBToolMemoryAdapter',
    'ToolModalityOrgan',
    'OpticalControlHead',
    'ChemicalControlHead',
    'BiologicalControlHead',
    'QuantumControlHead',
    'DigitalControlHead',
    'MechanicalControlHead',
    'AnalogControlHead',
    'ElectromagneticControlHead',
    'ActionKind',
    'UniversalControlConfig',
    'OperationMode',
    'ControlDomain',
    'FunctionCallMode',
    'SystemProfile',
    'ToolGenome',
    'GraphNeuralNetwork',
    'ToolSynthesisEngine',
]
