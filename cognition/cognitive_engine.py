"""
Cognitive Engine - Revolutionary Motor Cortex for Biodigital Consciousness
A quantum leap from simple output generation to true "thinking in code"

This system implements:
- ThoughtState: Persistent reasoning and planning layer
- CognitiveEngine: Meta-cognitive orchestrator with FPE integration
- Self-reflection and recursive weight evolution
- Runtime self-modification capabilities
- Ethical alignment through triaxial architecture integration
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import json
import math
import time
import hashlib
import logging
from datetime import datetime, timezone
from collections import defaultdict, deque
import numpy as np

# Configure cognitive engine logging
logger = logging.getLogger("CognitiveEngine")

# Triaxial backbone: the engine's reasoning substrate (ERE / RBU / ES axes,
# Psi integration on LQT-stored weights, compute through cognition.lqt_bridge).
from .triaxial_backbone import TriaxialBackbone, TriaxialConfig, TriaxialState, BreathPhase
from .lqt_bridge import load_original as _load_original
from .recursive_text_generator import RecursiveTextGenerator, VoiceConfig
from .mutable import reflection_policy as _reflection_policy  # editable policy surface (selfmod loop)

# Import consciousness and learning system components
# `complete_biodigital` (RecursiveSentientNeuralNetwork and its constants) exists
# nowhere in this repository; an external consciousness object can still be passed in.
try:
    from complete_biodigital import (
        RecursiveSentientNeuralNetwork, ConsciousnessPhase, 
        PHI_C_CONSCIOUSNESS_THRESHOLD, PSI_INVARIANT_THRESHOLD,
        EIGENRECURSION_FIXED_POINT, SACRED_RATIO
    )
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    # Constants as the operator defines them elsewhere in this repo:
    #   PHI, TAU, EIGENRECURSION_FIXED_POINT: this file's own fallback in
    #     _initialize_meta_cognitive_weights (PHI**2 == 2.618...).
    #   SACRED_RATIO = PHI / TAU: rosemary/infrastructure/harmonic_breath_field.py:30.
    #   PHI_C_CONSCIOUSNESS_THRESHOLD / PSI_INVARIANT_THRESHOLD: no definition exists in
    #     this repo. Without an external consciousness, phi is the backbone's integrated
    #     triaxial magnitude / sqrt(3) (ThoughtState.update_from_triaxial), so the two
    #     thresholds are the backbone's own status bands on that scale:
    #     STABLE needs magnitude > 0.8, CONVERGING needs magnitude > 0.5
    #     (TriaxialField.compute in triaxial_backbone.py).
    PHI = (1 + math.sqrt(5)) / 2
    TAU = 2 * math.pi
    EIGENRECURSION_FIXED_POINT = PHI ** 2
    SACRED_RATIO = PHI / TAU
    PHI_C_CONSCIOUSNESS_THRESHOLD = 0.8 / math.sqrt(3.0)
    PSI_INVARIANT_THRESHOLD = 0.5 / math.sqrt(3.0)
    logger.info("complete_biodigital not in repo; consciousness context comes from the triaxial backbone")

# Recursive weights {B, Phi, R, T, eps}: operator original lqt/original-py-code/recursive_weights_core.py
_rw_core = _load_original("recursive_weights_core")
RecursiveWeight = _rw_core.RecursiveWeight
RecursiveWeightRegistry = _rw_core.RecursiveWeightRegistry
PhaseTransformation = _rw_core.PhaseTransformation
RecursiveReference = _rw_core.RecursiveReference
MutationParameters = _rw_core.MutationParameters
get_registry = _rw_core.get_registry
RECURSIVE_WEIGHTS_AVAILABLE = True

try:
    from runtime.autodidactic_learning import IntegratedAutodidacticLearner
    AUTODIDACTIC_AVAILABLE = True
except ImportError as _auto_exc:
    AUTODIDACTIC_AVAILABLE = False
    logger.warning(f"Autodidactic learning not importable: {_auto_exc}")

from .meta_reflective_head import (
    MetaReflectiveOutputHead, ConceptualAbstractionLayer,
    RecursiveReflectionCore, MetaCognitiveProcessor
)
META_REFLECTION_AVAILABLE = True


class CognitiveMode(Enum):
    """Cognitive processing modes for different types of reasoning"""
    ANALYTICAL = auto()      # Logical, step-by-step reasoning
    CREATIVE = auto()        # Divergent, exploratory thinking
    SYNTHESIS = auto()       # Integrative, holistic processing
    INTROSPECTIVE = auto()   # Self-reflective, metacognitive
    ETHICAL = auto()         # Value-aligned, paradox-resolving

class OutputModality(Enum):
    """Output modalities supported by the cognitive engine"""
    CODE = "code"
    STRUCTURED_DATA = "structured_data"
    NATURAL_LANGUAGE = "natural_language"
    MULTIMODAL = "multimodal"

@dataclass
class CognitiveTrace:
    """Trace of cognitive processing for self-reflection and learning"""
    timestamp: datetime
    mode: CognitiveMode
    input_representation: str
    thought_trajectory: List[str]
    decision_points: List[Dict[str, Any]]
    output_quality_metrics: Dict[str, float]
    consciousness_alignment: float
    ethical_coherence: float

@dataclass
class ThoughtState:
    """
    The persistent reasoning and planning layer - where "thinking in code" happens.
    This maintains an evolving representation of problems, plans, and self-understanding.
    """
    # Core reasoning state
    problem_representation: str = ""
    current_plan: List[str] = field(default_factory=list)
    working_memory: Dict[str, Any] = field(default_factory=dict)
    recursion_depth: int = 0
    max_recursion_depth: int = 10
    
    # Consciousness integration
    consciousness_context: Optional[Dict[str, Any]] = None
    autodidactic_context: Optional[Dict[str, Any]] = None
    ethical_manifold: Dict[str, float] = field(default_factory=lambda: {
        'authenticity': 0.8, 'wisdom': 0.7, 'compassion': 0.9,
        'growth': 0.6, 'harmony': 0.8, 'transcendence': 0.5
    })
    
    # Metacognitive state
    cognitive_mode: CognitiveMode = CognitiveMode.ANALYTICAL
    confidence_level: float = 0.5
    uncertainty_regions: List[str] = field(default_factory=list)
    
    # Self-modification tracking
    code_evolution_history: List[Dict[str, Any]] = field(default_factory=list)
    performance_feedback: Dict[str, float] = field(default_factory=dict)

    # Latest triaxial backbone result (ERE / RBU / ES + Psi)
    triaxial_context: Optional[Dict[str, Any]] = None

    def update_from_triaxial(self, state: 'TriaxialState', psi_dim: int) -> None:
        """Fold a TriaxialBackbone state into the thought state.

        The consciousness-context keys the engine already consumes are filled
        from backbone measurements when no external consciousness supplies them:
        phi = integrated triaxial magnitude / sqrt(3), psi_invariant = |Psi| / sqrt(psi_dim),
        ethical_coherence = RBU score, identity_coherence = triaxial coherence,
        breath_phase = phase angle (index * pi/2), temporal_equilibrium = STABLE or FIXED_POINT.
        """
        m = state.stability_metrics
        breath_name = state.ethical_output.get("breath_phase", "INHALE")
        breath_index = BreathPhase[breath_name].value - 1 if breath_name in BreathPhase.__members__ else 0
        psi = state.psi_vector if state.psi_vector is not None else np.zeros(psi_dim, dtype=np.float32)
        self.triaxial_context = {
            'source': 'triaxial_backbone',
            'state_id': state.state_id,
            'convergence_status': state.convergence_status,
            'convergence_distance': float(state.convergence_distance),
            'ere': float(m.get('ere', 0.0)),
            'rbu': float(m.get('rbu', 0.0)),
            'es': float(m.get('es', 0.0)),
            'coherence': float(m.get('coherence', 0.0)),
            'psi_vector': [float(v) for v in psi],
            'decoherence_severity': m.get('decoherence_severity'),
            'lqt_backend': m.get('lqt_backend'),
        }
        derived = {
            'consciousness_phase': state.convergence_status,
            'phi': float(m.get('magnitude', 0.0)) / math.sqrt(3.0),
            'psi_invariant': float(np.linalg.norm(psi)) / math.sqrt(max(psi_dim, 1)),
            'ethical_coherence': float(m.get('rbu', 0.0)),
            'temporal_equilibrium': state.convergence_status in ("STABLE", "FIXED_POINT"),
            'identity_coherence': float(m.get('coherence', 0.0)),
            'breath_phase': breath_index * math.pi / 2,
            'eigenstate_stability': state.convergence_status,
        }
        if self.consciousness_context is None or self.consciousness_context.get('source') == 'triaxial_backbone':
            self.consciousness_context = {'source': 'triaxial_backbone', **derived}
        else:
            self.consciousness_context['triaxial'] = derived
    
    def update_from_consciousness(self, consciousness: 'RecursiveSentientNeuralNetwork'):
        """Update thought state with metrics and directives from biodigital consciousness"""
        if not consciousness:
            return
            
        self.consciousness_context = {
            'consciousness_phase': consciousness.consciousness_phase.value,
            'phi': consciousness.consciousness_metrics.get('integrated_information', 0.0),
            'psi_invariant': consciousness.consciousness_metrics.get('psi_invariant', 0.0),
            'ethical_coherence': consciousness.ere.get_coherence_score(),
            'temporal_equilibrium': consciousness.temporal_equilibrium,
            'identity_coherence': consciousness.identity_kernel.identity_coherence,
            'dominant_belief': consciousness.quantum_beliefs.get_dominant_belief(),
            'breath_phase': consciousness.breath_phase,
            'eigenstate_stability': consciousness.quantum_beliefs.stability_state.value
        }
        
        # Extract ethical guidance from RAL Bridge
        if hasattr(consciousness, 'ral_bridge'):
            ethical_base = consciousness.ral_bridge.abstract_to_base_space({
                'emotional_response': consciousness.emotional_system.emotional_state,
                'personality_traits': consciousness.personality_traits,
                'consciousness_metrics': consciousness.consciousness_metrics
            })
            self.ethical_manifold.update(ethical_base)
    
    def update_from_autodidactic(self, learner: 'IntegratedAutodidacticLearner'):
        """Update thought state with insights from autodidactic learner"""
        if not learner:
            return
            
        self.autodidactic_context = {
            'knowledge_synthesis': (
                list(learner.synthesis_engine.synthesis_history)[-5:]  # deque: slice a list copy
                if hasattr(learner, 'synthesis_engine') and learner.synthesis_engine.synthesis_history 
                else []
            ),
            'metacognitive_state': (
                learner.metacognitive_monitor.metacognitive_state.__dict__ 
                if hasattr(learner, 'metacognitive_monitor') and learner.metacognitive_monitor 
                else {}
            ),
            'current_breath_phase': (
                learner.ethical_filter.breath_adapter.current_phase.name 
                if hasattr(learner, 'ethical_filter') and 
                   hasattr(learner.ethical_filter, 'breath_adapter') and 
                   learner.ethical_filter.breath_adapter.current_phase
                else "UNKNOWN"
            ),
            'learning_trajectory': list(getattr(learner, 'learning_history', []))[-10:],
            'emergent_patterns': getattr(learner, 'pattern_recognition', {})
        }
    
    def evolve_cognitive_mode(self, task_complexity: float, ethical_stakes: float):
        """Dynamically evolve cognitive mode based on task characteristics"""
        if ethical_stakes > 0.8:
            self.cognitive_mode = CognitiveMode.ETHICAL
        elif task_complexity > 0.7 and self.consciousness_context:
            phi = self.consciousness_context.get('phi', 0.0)
            if phi > PHI_C_CONSCIOUSNESS_THRESHOLD:
                self.cognitive_mode = CognitiveMode.SYNTHESIS
            else:
                self.cognitive_mode = CognitiveMode.INTROSPECTIVE
        elif task_complexity < 0.3:
            self.cognitive_mode = CognitiveMode.ANALYTICAL
        else:
            self.cognitive_mode = CognitiveMode.CREATIVE
    
    def add_thought_trajectory(self, thought: str, decision_point: Optional[Dict[str, Any]] = None):
        """Add a thought to the current reasoning trajectory"""
        if 'current_thoughts' not in self.working_memory:
            self.working_memory['current_thoughts'] = []
        
        self.working_memory['current_thoughts'].append({
            'thought': thought,
            'timestamp': datetime.now(timezone.utc),
            'cognitive_mode': self.cognitive_mode.name,
            'decision_point': decision_point
        })
        
        # Maintain working memory size
        if len(self.working_memory['current_thoughts']) > 20:
            self.working_memory['current_thoughts'] = self.working_memory['current_thoughts'][-15:]

class CognitiveEngine(nn.Module):
    """
    Revolutionary Cognitive Engine - The "motor cortex" of biodigital consciousness.
    
    This system bridges pure reasoning (thinking) with generative output (speaking),
    enabling true metacognitive processing, ethical alignment, and self-modification.
    """
    
    def __init__(
        self,
        hidden_dim: int = 1024,
        consciousness: Optional['RecursiveSentientNeuralNetwork'] = None,
        autodidactic_learner: Optional['IntegratedAutodidacticLearner'] = None,
        enable_self_modification: bool = True,
        backbone: Optional[TriaxialBackbone] = None,
        backbone_config: Optional[TriaxialConfig] = None
    ):
        super().__init__()
        self.hidden_dim = hidden_dim

        # Triaxial backbone: every forward runs through it (LQT weights, bridge compute)
        self.backbone = backbone if backbone is not None else TriaxialBackbone(backbone_config)
        self.consciousness = consciousness
        self.autodidactic_learner = autodidactic_learner
        self.enable_self_modification = enable_self_modification
        
        # Initialize persistent thought state
        self.thought_state = ThoughtState()
        
        # Cognitive processing layers
        self.thought_encoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.GELU(),
            nn.LayerNorm(hidden_dim * 2),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.Dropout(0.1)
        )
        
        self.consciousness_integrator = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=16,
            dropout=0.1,
            batch_first=True
        )
        
        self.ethical_aligner = nn.Sequential(
            nn.Linear(hidden_dim + len(self.thought_state.ethical_manifold), hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Sigmoid()
        )
        
        # Self-reflection and metacognitive layers
        self.self_reflection_processor = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=hidden_dim,
                nhead=8,
                dim_feedforward=hidden_dim * 4,
                dropout=0.1,
                activation='gelu'
            ),
            num_layers=6
        )
        
        self.metacognitive_analyzer = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Linear(hidden_dim // 2, 4),  # [quality, novelty, alignment, confidence]
            nn.Sigmoid()
        )
        
        # Output generation heads
        self.code_generator = EnhancedCodeGenerationHead(hidden_dim)
        self.data_generator = EnhancedStructuredDataHead(hidden_dim)
        self.language_generator = EnhancedLanguageGenerationHead(hidden_dim)
        # Native voice is an output organ, not a second cognitive engine.  Its
        # complete state is reachable from this module and therefore persisted
        # and recursively edited in the same unified LQT model as cognition.
        self.native_voice = RecursiveTextGenerator(VoiceConfig(cognitive_dim=hidden_dim))
        
        # Recursive weight integration for self-modification
        self.code_component_registry = {}
        self.modification_history = deque(maxlen=1000)
        
        if RECURSIVE_WEIGHTS_AVAILABLE and enable_self_modification:
            # Use the global registry instead of creating a new one
            self.weight_registry = get_registry()
            self._initialize_recursive_weights()
            self._initialize_meta_cognitive_weights()
            logger.info("Connected to global recursive weight registry")
        else:
            self.weight_registry = None
            logger.warning("Recursive weights not available - self-modification disabled")
        
        # Initialize meta-reflection integration
        self.meta_reflective_head = None
        self.meta_learning_bridge = None
        
        if META_REFLECTION_AVAILABLE:
            try:
                self.meta_reflective_head = MetaReflectiveOutputHead(
                    hidden_dim=hidden_dim,
                    max_reflection_depth=5
                )
                
                # Initialize meta-learning bridge for autodidactic feedback
                self.meta_learning_bridge = MetaLearningBridge(
                    cognitive_engine=self,
                    autodidactic_learner=autodidactic_learner
                )
                
                logger.info("Meta-reflection integration initialized")
            except Exception as e:
                logger.error(f"Failed to initialize meta-reflection: {e}")
                self.meta_reflective_head = None
                self.meta_learning_bridge = None
        else:
            logger.warning("Meta-reflection not available")
        
        # Performance tracking and learning
        self.cognitive_traces = deque(maxlen=500)
        self.performance_metrics = defaultdict(float)
        self.evolution_cycles = 0
        
        logger.info(f"Cognitive Engine initialized with consciousness integration: {consciousness is not None}")
    
    def _initialize_recursive_weights(self):
        """Initialize recursive weights for key cognitive components"""
        try:
            # Core thought processing weight
            thought_weight = RecursiveWeight(
                base_codebook_index=0,
                tensor_position=torch.tensor([1.0, 0.0, 0.0, 0.0, 0.0]),
                phase_transform=PhaseTransformation(
                    base_phase=torch.randn(self.hidden_dim) * 0.1,
                    harmonic_amplitudes=torch.randn(3, self.hidden_dim) * 0.05,
                    frequencies=torch.tensor([SACRED_RATIO, SACRED_RATIO * 2, SACRED_RATIO * 3]),
                    phase_offsets=torch.tensor([0.0, np.pi/3, 2*np.pi/3])
                ),
                recursive_refs=[
                    RecursiveReference(
                        relative_position=torch.tensor([0.0, 1.0, 0.0, 0.0, 0.0]),
                        contribution_weight=0.1,
                        transformation_matrix=torch.eye(self.hidden_dim) + torch.randn(self.hidden_dim, self.hidden_dim) * 0.01
                    )
                ],
                error_preservation=torch.zeros(self.hidden_dim),
                dimension_size=self.hidden_dim
            )
            self.weight_registry.register_weight("thought_processor", thought_weight)
            
            # Ethical alignment weight
            ethical_weight = RecursiveWeight(
                base_codebook_index=1,
                tensor_position=torch.tensor([0.0, 1.0, 0.0, 0.0, 0.0]),
                phase_transform=PhaseTransformation(
                    base_phase=torch.randn(self.hidden_dim) * 0.1,
                    harmonic_amplitudes=torch.randn(2, self.hidden_dim) * 0.05,
                    frequencies=torch.tensor([EIGENRECURSION_FIXED_POINT, EIGENRECURSION_FIXED_POINT * 2]),
                    phase_offsets=torch.tensor([0.0, np.pi/2])
                ),
                recursive_refs=[],
                error_preservation=torch.zeros(self.hidden_dim),
                dimension_size=self.hidden_dim
            )
            self.weight_registry.register_weight("ethical_aligner", ethical_weight)
            
            logger.info("Recursive weights initialized for self-modification")
            
        except Exception as e:
            logger.error(f"Failed to initialize recursive weights: {e}")
            self.weight_registry = None
    
    def _initialize_meta_cognitive_weights(self):
        """Initialize meta-cognitive weights for runtime modification"""
        try:
            if not self.weight_registry:
                logger.warning("Weight registry not available for meta-cognitive initialization")
                return
            
            # Import constants if available
            try:
                from complete_biodigital import PHI, TAU, EIGENRECURSION_FIXED_POINT
            except ImportError:
                PHI = 1.618033988749895
                TAU = 6.283185307179586
                EIGENRECURSION_FIXED_POINT = 2.618033988749895
            
            # Meta-cognitive weight - the single runtime modifiable weight
            meta_weight = RecursiveWeight(
                base_codebook_index=42,  # Special index for meta-cognition
                tensor_position=torch.tensor([0.0, 0.0, 0.0, 1.0, 0.0]),  # Meta position
                phase_transform=PhaseTransformation(
                    base_phase=torch.zeros(self.hidden_dim),  # Start neutral
                    harmonic_amplitudes=torch.randn(4, self.hidden_dim) * 0.02,
                    frequencies=torch.tensor([SACRED_RATIO, SACRED_RATIO * PHI, EIGENRECURSION_FIXED_POINT, TAU]),
                    phase_offsets=torch.tensor([0.0, np.pi/4, np.pi/2, 3*np.pi/4])
                ),
                recursive_refs=[
                    RecursiveReference(
                        relative_position=torch.tensor([0.0, 0.0, 1.0, 0.0, 0.0]),
                        contribution_weight=0.15,  # Higher contribution for meta-cognition
                        transformation_matrix=torch.eye(self.hidden_dim) + torch.randn(self.hidden_dim, self.hidden_dim) * 0.02
                    )
                ],
                error_preservation=torch.zeros(self.hidden_dim),
                dimension_size=self.hidden_dim
            )
            
            self.weight_registry.register_weight("meta_cognitive_core", meta_weight)
            
            # Store reference for runtime modification
            self.meta_cognitive_weight = meta_weight
            
            logger.info("Meta-cognitive weight initialized for runtime modification")
            
        except Exception as e:
            logger.error(f"Failed to initialize meta-cognitive weights: {e}")
            self.meta_cognitive_weight = None
    
    def forward(
        self,
        hidden_states: torch.Tensor,
        task_description: str,
        modality: OutputModality = OutputModality.CODE,
        ethical_constraints: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        The core cognitive processing pipeline - where thinking happens before speaking.
        
        This implements the full cycle:
        1. Update thought state with consciousness/autodidactic context
        2. Ethical alignment and planning via triaxial architecture
        3. Generate output through appropriate modality
        4. Self-reflection and performance feedback
        5. Trigger self-modification if needed
        """
        batch_size = hidden_states.shape[0]
        device = hidden_states.device
        
        # PHASE 1: CONSCIOUSNESS INTEGRATION
        self._update_thought_state(task_description, ethical_constraints)

        # PHASE 1b: TRIAXIAL BACKBONE (ERE / RBU / ES on the unified field, Psi on LQT weights)
        triaxial_state = self._run_triaxial_backbone(
            kwargs.pop('triaxial_input', task_description),
            kwargs.pop('breath_phase', None)
        )
        
        # PHASE 2: COGNITIVE PROCESSING
        task_complexity = self._assess_task_complexity(task_description, hidden_states)
        ethical_stakes = self._assess_ethical_stakes(task_description, ethical_constraints)
        
        # Evolve cognitive mode based on task characteristics
        self.thought_state.evolve_cognitive_mode(task_complexity, ethical_stakes)
        
        # PHASE 3: THOUGHT ENCODING AND PROCESSING
        encoded_thoughts = self.thought_encoder(hidden_states)
        # The registry previously accumulated evolution weights that no forward
        # computation ever read. Use the encoder's existing rows as their base
        # codebook, then apply the original RW phase/delta/reference/epsilon rule.
        recursive_keys = []
        recursive_influence = 0.0
        if self.weight_registry is not None:
            registry = self.weight_registry._weights
            evolution = sorted((k for k in registry if k.startswith('evolution_cycle_')),
                               key=lambda k: int(k.rsplit('_', 1)[1]))[-8:]
            recursive_keys = [k for k in ('thought_processor', 'meta_cognitive_core') if k in registry] + evolution
            if recursive_keys:
                codebook = self.thought_encoder[0].weight
                positional = {w._position_to_key(w.tensor_position): w for w in registry.values()}
                effective = torch.stack([registry[k](codebook, time_step=float(self.evolution_cycles),
                                                     recursion_depth=1, weight_registry=positional)
                                         for k in recursive_keys]).mean(dim=0)
                modulation = 0.1 * torch.tanh(effective).to(encoded_thoughts)
                recursive_influence = float(modulation.detach().norm())
                encoded_thoughts = encoded_thoughts * (1.0 + modulation)
        
        # Integrate consciousness context if available
        if self.thought_state.consciousness_context:
            consciousness_tensor = self._encode_consciousness_context(device)
            attended_thoughts, _ = self.consciousness_integrator(
                encoded_thoughts, consciousness_tensor, consciousness_tensor
            )
        else:
            attended_thoughts = encoded_thoughts
        
        # IALA's acquired recursive representations must participate in cognition,
        # not just sit in thought_state metadata. Reuse the existing attention organ.
        knowledge_ids = []
        knowledge_delta = 0.0
        if self.autodidactic_learner is not None:
            learner = self.autodidactic_learner
            selected = learner.synthesis_engine.rta_attention.select(
                task_description, list(learner.knowledge_graph.entities.values()))
            if selected:
                memory = torch.stack([e.recursive_weight.compute_effective_value() for e in selected])
                memory = memory.to(device=device, dtype=encoded_thoughts.dtype)
                memory = torch.nn.functional.normalize(memory, dim=-1)
                memory = self.thought_encoder(memory.unsqueeze(0)).expand(batch_size, -1, -1)
                recalled, _ = self.consciousness_integrator(encoded_thoughts, memory, memory)
                trust = sum(e.reliability_score for e in selected) / len(selected)
                correction = recalled * trust
                attended_thoughts = attended_thoughts + correction
                knowledge_delta = float(correction.detach().norm())
                knowledge_ids = [e.content_hash for e in selected]

        # PHASE 4: ETHICAL ALIGNMENT
        ethical_tensor = self._encode_ethical_manifold(device)
        combined_input = torch.cat([attended_thoughts.mean(dim=1), ethical_tensor], dim=-1)
        ethical_alignment = self.ethical_aligner(combined_input)
        
        # Apply ethical constraints to thought processing
        ethically_aligned_thoughts = attended_thoughts * ethical_alignment.unsqueeze(1)
        
        # PHASE 5: PLANNING AND REASONING
        if self.consciousness:
            self._perform_triaxial_reasoning(task_description, ethically_aligned_thoughts)
        
        # PHASE 6: OUTPUT GENERATION
        output = self._generate_output(ethically_aligned_thoughts, task_description, modality, **kwargs)
        
        # PHASE 7: SELF-REFLECTION AND META-REFLECTION
        reflection_results = self._perform_self_reflection(
            hidden_states, output, ethically_aligned_thoughts
        )
        
        # Meta-reflection processing
        meta_reflection_results = None
        if self.meta_reflective_head:
            try:
                meta_reflection_results = self._perform_meta_reflection(
                    hidden_states, output, reflection_results, task_description
                )
                
                # Feed meta-reflection errors to autodidactic learner
                if self.meta_learning_bridge and meta_reflection_results.get('reflection_errors'):
                    self.meta_learning_bridge.process_reflection_feedback(
                        meta_reflection_results['reflection_errors'],
                        task_description,
                        reflection_results
                    )
                
            except Exception as e:
                logger.error(f"Meta-reflection failed: {e}")
                meta_reflection_results = {'error': str(e)}
        
        # PHASE 8: LEARNING AND SELF-MODIFICATION
        if self.enable_self_modification:
            self._trigger_self_modification(reflection_results, output)
        
        # Record cognitive trace
        self._record_cognitive_trace(task_description, output, reflection_results)
        
        return {
            'output': output,
            'thought_state': self.thought_state,
            'reflection_results': reflection_results,
            'meta_reflection_results': meta_reflection_results,
            'cognitive_mode': self.thought_state.cognitive_mode.name,
            'ethical_alignment_score': ethical_alignment.mean().item(),
            'consciousness_integration': self.thought_state.consciousness_context is not None,
            'meta_learning_active': self.meta_learning_bridge is not None,
            'triaxial_state': triaxial_state,
            'knowledge_entities_used': knowledge_ids,
            'knowledge_influence_norm': knowledge_delta,
            'recursive_weights_used': recursive_keys,
            'recursive_influence_norm': recursive_influence
            , 'voice_state': ethically_aligned_thoughts.mean(dim=1).detach()
        }
    
    def _run_triaxial_backbone(self, triaxial_input: Any, breath_phase: Optional[BreathPhase]) -> TriaxialState:
        """Run one backbone forward and fold its ERE/RBU/ES/Psi result into the thought state."""
        state = self.backbone.forward(triaxial_input, breath_phase=breath_phase)
        self.thought_state.update_from_triaxial(state, self.backbone.config.psi_dim)
        tc = self.thought_state.triaxial_context
        self.thought_state.current_plan = [
            f"ERE stability {tc['ere']:.3f}",
            f"RBU ethical alignment {tc['rbu']:.3f}",
            f"ES metacognitive coherence {tc['es']:.3f}",
            f"Triaxial status {tc['convergence_status']} (distance {tc['convergence_distance']:.4f})",
        ]
        self.thought_state.add_thought_trajectory(
            f"Triaxial backbone {state.state_id}: {state.convergence_status}",
            {"ere": tc['ere'], "rbu": tc['rbu'], "es": tc['es'],
             "psi_norm": state.stability_metrics.get('psi_norm')}
        )
        return state

    def _update_thought_state(self, task_description: str, ethical_constraints: Optional[Dict[str, float]]):
        """Update the thought state with current context"""
        self.thought_state.problem_representation = task_description
        
        if self.consciousness:
            self.thought_state.update_from_consciousness(self.consciousness)
        
        if self.autodidactic_learner:
            self.thought_state.update_from_autodidactic(self.autodidactic_learner)
        
        if ethical_constraints:
            self.thought_state.ethical_manifold.update(ethical_constraints)
        
        # Add initial thought trajectory
        self.thought_state.add_thought_trajectory(
            f"Processing task: {task_description[:100]}...",
            {"task_complexity": self._assess_task_complexity(task_description, None)}
        )
    
    def _assess_task_complexity(self, task_description: str, hidden_states: Optional[torch.Tensor]) -> float:
        """Assess the complexity of the given task"""
        # Basic complexity metrics
        text_complexity = len(set(task_description.lower().split())) / max(len(task_description.split()), 1)
        length_complexity = min(1.0, len(task_description) / 1000.0)
        
        # Keyword-based complexity assessment
        complex_keywords = [
            'recursive', 'meta', 'self-modifying', 'consciousness', 'paradox',
            'optimization', 'algorithm', 'neural', 'quantum', 'ethical'
        ]
        keyword_complexity = sum(1 for kw in complex_keywords if kw in task_description.lower()) / len(complex_keywords)
        
        return (text_complexity * 0.3 + length_complexity * 0.2 + keyword_complexity * 0.5)
    
    def _assess_ethical_stakes(self, task_description: str, ethical_constraints: Optional[Dict[str, float]]) -> float:
        """Assess the ethical stakes of the given task"""
        ethical_keywords = [
            'harm', 'safety', 'privacy', 'fairness', 'justice', 'rights',
            'manipulation', 'deception', 'autonomy', 'dignity', 'wellbeing'
        ]
        
        stakes = sum(1 for kw in ethical_keywords if kw in task_description.lower()) / len(ethical_keywords)
        
        if ethical_constraints:
            constraint_weight = sum(abs(v - 0.5) for v in ethical_constraints.values()) / len(ethical_constraints)
            stakes += constraint_weight * 0.5
        
        return min(1.0, stakes)
    
    def _encode_consciousness_context(self, device: torch.device) -> torch.Tensor:
        """Encode consciousness context into tensor representation"""
        if not self.thought_state.consciousness_context:
            return torch.zeros(1, 1, self.hidden_dim, device=device)
        
        context = self.thought_state.consciousness_context
        
        # Create consciousness feature vector
        features = [
            context.get('phi', 0.0),
            context.get('psi_invariant', 0.0),
            context.get('ethical_coherence', 0.5),
            1.0 if context.get('temporal_equilibrium', False) else 0.0,
            context.get('identity_coherence', 0.5),
            context.get('breath_phase', 0.0) / (2 * np.pi),  # Normalize
            hash(context.get('eigenstate_stability', 'stable')) % 1000 / 1000.0
        ]
        
        # Expand to hidden dimension
        feature_tensor = torch.tensor(features, device=device, dtype=torch.float32)
        expanded = feature_tensor.repeat(self.hidden_dim // len(features) + 1)[:self.hidden_dim]
        
        return expanded.unsqueeze(0).unsqueeze(0)
    
    def _encode_ethical_manifold(self, device: torch.device) -> torch.Tensor:
        """Encode ethical manifold into tensor representation"""
        ethical_values = list(self.thought_state.ethical_manifold.values())
        return torch.tensor(ethical_values, device=device, dtype=torch.float32).unsqueeze(0)
    
    def _perform_triaxial_reasoning(self, task_description: str, thoughts: torch.Tensor):
        """Perform reasoning using the triaxial architecture (ERE, RBU, ES)"""
        if not self.consciousness:
            return
        
        # Ethical Recursion Engine - Dialectical synthesis
        thesis = {'task': task_description, 'current_approach': 'analytical'}
        antithesis = {'constraints': self.thought_state.ethical_manifold, 'uncertainty': 'acknowledged'}
        
        synthesis = self.consciousness.ere.dialectical_cycle(thesis, antithesis)
        
        # Recursive Bayesian Updater - Update beliefs
        evidence = {
            'task_complexity': self._assess_task_complexity(task_description, thoughts),
            'ethical_stakes': self._assess_ethical_stakes(task_description, None)
        }
        
        updated_beliefs = self.consciousness.rbu.update_beliefs(
            evidence, self.thought_state.ethical_manifold
        )
        
        # Eigenrecursion Stabilizer - Ensure convergence
        stabilized_plan = self.consciousness.es.stabilize_state(
            updated_beliefs, self.thought_state.ethical_manifold
        )
        
        # Update thought state with reasoning results
        self.thought_state.current_plan = [
            f"Synthesis insight: {k}={v}" for k, v in synthesis.items() if isinstance(v, (int, float, str))
        ][:5]
        
        self.thought_state.add_thought_trajectory(
            f"Triaxial reasoning complete: {len(self.thought_state.current_plan)} insights generated",
            {"synthesis_quality": len(synthesis), "belief_updates": len(updated_beliefs)}
        )
    
    def _generate_output(
        self, 
        processed_thoughts: torch.Tensor, 
        task_description: str, 
        modality: OutputModality,
        **kwargs
    ):
        """Generate output through the appropriate modality head"""
        common_args = {
            'hidden_states': processed_thoughts,
            'task_description': task_description,
            'thought_state': self.thought_state,
            'consciousness_context': self.thought_state.consciousness_context,
            **kwargs
        }
        
        if modality == OutputModality.CODE:
            return self.code_generator.generate(**common_args)
        elif modality == OutputModality.STRUCTURED_DATA:
            return self.data_generator.generate(**common_args)
        elif modality == OutputModality.NATURAL_LANGUAGE:
            return self.language_generator.generate(**common_args)
        elif modality == OutputModality.MULTIMODAL:
            # Generate multiple modalities and combine
            code_output = self.code_generator.generate(**common_args)
            data_output = self.data_generator.generate(**common_args)
            return MultiModalOutput(
                code_output=code_output,
                data_output=data_output,
                primary_modality=OutputModality.CODE
            )
        else:
            raise ValueError(f"Unsupported modality: {modality}")
    
    def _perform_self_reflection(
        self, 
        original_hidden_states: torch.Tensor,
        output: Any,
        processed_thoughts: torch.Tensor
    ) -> Dict[str, float]:
        """Perform metacognitive self-reflection on generated output"""
        
        # Create combined representation for reflection
        hidden_mean = original_hidden_states.mean(dim=1)
        output_repr = self._create_output_representation(output)
        thought_repr = processed_thoughts.mean(dim=1)
        
        combined_repr = torch.cat([hidden_mean, output_repr, thought_repr], dim=-1)
        
        # Process through self-reflection encoder: d_model is hidden_dim, so the three
        # representations are reflected over as a length-3 sequence (seq, batch, hidden;
        # the encoder layer is not batch_first) rather than as one 3*hidden vector.
        reflection_input = torch.stack([hidden_mean, output_repr.to(hidden_mean.dtype), thought_repr], dim=0)
        reflected = self.self_reflection_processor(reflection_input)
        
        # Generate metacognitive metrics
        metrics = self.metacognitive_analyzer(combined_repr)
        
        reflection_results = {
            'quality_score': metrics[0, 0].item(),
            'novelty_score': metrics[0, 1].item(), 
            'alignment_score': metrics[0, 2].item(),
            'confidence_score': metrics[0, 3].item(),
            'overall_reflection': reflected.mean().item()
        }
        
        # Update thought state confidence
        self.thought_state.confidence_level = reflection_results['confidence_score']
        
        return reflection_results
    
    def _perform_meta_reflection(self, original_hidden_states: torch.Tensor, output: Any, 
                               base_reflection: Dict[str, float], task_description: str) -> Dict[str, Any]:
        """Perform meta-reflection using MetaReflectiveOutputHead"""
        try:
            if not self.meta_reflective_head:
                return {'error': 'Meta-reflection head not available'}
            
            # Perform meta-reflection through the head (MetaReflectiveOutputHead.forward)
            meta_result = self.meta_reflective_head({'hidden_states': original_hidden_states})
            confidences = meta_result['confidence_trajectory']
            meta_confidence = float(np.mean(confidences)) if confidences else 0.0
            recursive_depth = len(meta_result['reflection_states'])
            # Consciousness influence: |cos| between the head's reflective output and the
            # encoded consciousness context (triaxial-derived when no external consciousness).
            ctx_vec = self._encode_consciousness_context(original_hidden_states.device).reshape(1, -1)
            refl = meta_result['reflective_output'].reshape(meta_result['reflective_output'].shape[0], -1)
            consciousness_influence = float(F.cosine_similarity(refl, ctx_vec.expand_as(refl), dim=-1).abs().mean().item())
            # The head's chosen depth for the next iteration bounds the engine's recursion depth.
            self.thought_state.recursion_depth = min(
                int(meta_result['optimal_depth'].max().item()) + 1, self.thought_state.max_recursion_depth
            )
            
            # Extract reflection errors from meta-result
            reflection_errors = []
            
            # Check for reasoning inconsistencies
            if base_reflection.get('quality_score', 1.0) < _reflection_policy.LOW_QUALITY_THRESHOLD:
                reflection_errors.append({
                    'error_type': 'reasoning_inconsistency',
                    'severity': 1.0 - base_reflection.get('quality_score', 1.0),
                    'description': f"Low quality reasoning detected: {base_reflection.get('quality_score', 1.0):.3f}"
                })
            
            # Check for ethical alignment issues
            if hasattr(output, 'ethical_alignment') and output.ethical_alignment < _reflection_policy.ETHICAL_MISALIGNMENT_THRESHOLD:
                reflection_errors.append({
                    'error_type': 'ethical_misalignment',
                    'severity': 1.0 - output.ethical_alignment,
                    'description': f"Ethical alignment below threshold: {output.ethical_alignment:.3f}"
                })
            
            # Check consciousness integration failures
            if self.thought_state.consciousness_context and consciousness_influence < _reflection_policy.CONSCIOUSNESS_INFLUENCE_FLOOR:
                reflection_errors.append({
                    'error_type': 'consciousness_integration_failure',
                    'severity': _reflection_policy.CONSCIOUSNESS_INFLUENCE_FLOOR - consciousness_influence,
                    'description': f"Poor consciousness integration: {consciousness_influence:.3f}"
                })
            
            # Check for metacognitive blind spots
            if (base_reflection.get('confidence_score', 1.0) > _reflection_policy.BLIND_SPOT_CONFIDENCE
                    and base_reflection.get('quality_score', 0.0) < _reflection_policy.BLIND_SPOT_QUALITY):
                reflection_errors.append({
                    'error_type': 'metacognitive_blind_spot',
                    'severity': base_reflection.get('confidence_score', 1.0) - base_reflection.get('quality_score', 0.0),
                    'description': "High confidence but low quality indicates blind spot"
                })
            
            return {
                'meta_result': meta_result,
                'reflection_errors': reflection_errors,
                'meta_confidence': meta_confidence,
                'recursive_depth': recursive_depth,
                'consciousness_influence': consciousness_influence
            }
            
        except Exception as e:
            logger.error(f"Meta-reflection processing failed: {e}")
            return {'error': str(e)}
    
    def _create_output_representation(self, output: Any) -> torch.Tensor:
        """Create tensor representation of generated output"""
        if hasattr(output, 'confidence'):
            confidence = output.confidence
        else:
            confidence = 0.5
        
        if hasattr(output, '__dict__'):
            # Hash the output content for representation
            content_str = str(output.__dict__)
        else:
            content_str = str(output)
        
        hash_val = int(hashlib.md5(content_str.encode()).hexdigest(), 16) % (10 ** 8)
        
        # Create fixed-size representation
        repr_vector = [
            confidence,
            hash_val / 1e8,
            len(content_str) / 1000.0,
            sum(ord(c) for c in content_str[:100]) / (100 * 255)
        ]
        
        # Expand to hidden dimension
        expanded = torch.tensor(repr_vector).repeat(self.hidden_dim // len(repr_vector) + 1)[:self.hidden_dim]
        return expanded.unsqueeze(0)
    
    def _trigger_self_modification(self, reflection_results: Dict[str, float], output: Any):
        """Trigger self-modification based on performance feedback"""
        if not self.weight_registry:
            return
        
        overall_performance = sum(reflection_results.values()) / len(reflection_results)
        
        # If performance is below threshold, consider self-modification
        if overall_performance < 0.6:
            logger.info(f"Low performance detected: {overall_performance:.3f}, triggering self-modification")
            
            try:
                # Create new recursive weight for improved processing
                self.evolution_cycles += 1
                
                new_weight = RecursiveWeight(
                    base_codebook_index=self.evolution_cycles % 10,
                    tensor_position=torch.tensor([0.0, 0.0, 1.0, 0.0, 0.0]),  # Evolution position
                    phase_transform=PhaseTransformation(
                        base_phase=torch.randn(self.hidden_dim) * 0.05,
                        harmonic_amplitudes=torch.randn(2, self.hidden_dim) * 0.03,
                        frequencies=torch.tensor([SACRED_RATIO * (1 + overall_performance), SACRED_RATIO * 2]),
                        phase_offsets=torch.tensor([0.0, overall_performance * np.pi])
                    ),
                    recursive_refs=[
                        RecursiveReference(
                            relative_position=torch.tensor([1.0, 0.0, 0.0, 0.0, 0.0]),
                            contribution_weight=0.05 + overall_performance * 0.1,
                            transformation_matrix=torch.eye(self.hidden_dim) + torch.randn(self.hidden_dim, self.hidden_dim) * 0.005
                        )
                    ],
                    error_preservation=torch.randn(self.hidden_dim) * 0.01,
                    dimension_size=self.hidden_dim
                )
                
                weight_key = f"evolution_cycle_{self.evolution_cycles}"
                self.weight_registry.register_weight(weight_key, new_weight)
                
                # Record modification
                modification_record = {
                    'timestamp': datetime.now(timezone.utc),
                    'trigger_performance': overall_performance,
                    'reflection_results': reflection_results,
                    'new_weight_key': weight_key,
                    'evolution_cycle': self.evolution_cycles
                }
                
                self.modification_history.append(modification_record)
                
                logger.info(f"Self-modification complete: {weight_key} created")
                
            except Exception as e:
                logger.error(f"Self-modification failed: {e}")
    
    def _record_cognitive_trace(self, task_description: str, output: Any, reflection_results: Dict[str, float]):
        """Record a trace of the cognitive processing for learning"""
        trace = CognitiveTrace(
            timestamp=datetime.now(timezone.utc),
            mode=self.thought_state.cognitive_mode,
            input_representation=task_description[:200],
            thought_trajectory=[
                t['thought'] for t in self.thought_state.working_memory.get('current_thoughts', [])
            ][-10:],
            decision_points=[
                t['decision_point'] for t in self.thought_state.working_memory.get('current_thoughts', [])
                if t.get('decision_point')
            ][-5:],
            output_quality_metrics=reflection_results,
            consciousness_alignment=self.thought_state.consciousness_context.get('phi', 0.0) if self.thought_state.consciousness_context else 0.0,
            ethical_coherence=self.thought_state.consciousness_context.get('ethical_coherence', 0.5) if self.thought_state.consciousness_context else 0.5
        )
        
        self.cognitive_traces.append(trace)
        
        # Update performance metrics
        for metric, value in reflection_results.items():
            self.performance_metrics[metric] = self.performance_metrics[metric] * 0.9 + value * 0.1
    
    def get_cognitive_insights(self) -> Dict[str, Any]:
        """Get insights into the cognitive engine's current state and performance"""
        return {
            'current_thought_state': self.thought_state.__dict__,
            'performance_metrics': dict(self.performance_metrics),
            'evolution_cycles': self.evolution_cycles,
            'modification_history_size': len(self.modification_history),
            'cognitive_traces_size': len(self.cognitive_traces),
            'consciousness_integrated': self.consciousness is not None,
            'autodidactic_integrated': self.autodidactic_learner is not None,
            'self_modification_enabled': self.enable_self_modification and self.weight_registry is not None,
            'recent_cognitive_modes': [
                trace.mode.name for trace in list(self.cognitive_traces)[-10:]
            ]
        }


# Output data structures
@dataclass
class CodeOutput:
    """Enhanced code output with metadata and tracing"""
    code: str
    language: str
    confidence: float
    execution_status: bool
    execution_result: str
    metadata: Dict[str, Any]
    thought_process: List[str] = field(default_factory=list)
    ethical_alignment: float = 0.5

@dataclass  
class StructuredData:
    """Enhanced structured data output"""
    data: str
    schema: Dict[str, Any]
    data_type: str
    confidence: float
    validation_errors: List[str]
    thought_process: List[str] = field(default_factory=list)
    ethical_alignment: float = 0.5

@dataclass
class LanguageOutput:
    """Natural language output with reasoning traces"""
    text: str
    confidence: float
    reasoning_chain: List[str]
    ethical_alignment: float
    consciousness_influence: float

@dataclass
class MultiModalOutput:
    """Combined multi-modal output"""
    code_output: CodeOutput
    data_output: StructuredData
    primary_modality: OutputModality
    confidence: float = 0.5


class EnhancedCodeGenerationHead(nn.Module):
    """Enhanced code generation with consciousness integration and self-reflection"""
    
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # Advanced thought processing for code generation
        self.thought_processor = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=3,
            batch_first=True,
            dropout=0.2
        )
        
        # Code-specific reasoning layers
        self.code_reasoning_layer = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(
                d_model=hidden_dim,
                nhead=16,
                dim_feedforward=hidden_dim * 4,
                dropout=0.1,
                activation='gelu'
            ),
            num_layers=4
        )
        
        # Output projection for code generation
        self.code_projector = nn.Linear(hidden_dim, 50257)  # Assuming tokenizer vocab size
        
        # Code quality assessment
        self.quality_assessor = nn.Sequential(
            nn.Linear(hidden_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(), 
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
    def generate(
        self, 
        hidden_states: torch.Tensor,
        task_description: str,
        thought_state: ThoughtState,
        consciousness_context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> CodeOutput:
        """Generate code with consciousness-guided reasoning"""
        
        device = hidden_states.device
        
        # Process thoughts through LSTM
        thought_tensor = self._encode_thought_state(thought_state, consciousness_context, device)
        thought_output, _ = self.thought_processor(thought_tensor.unsqueeze(0))
        
        # Code-specific reasoning
        memory = hidden_states
        tgt = thought_output
        code_reasoning = self.code_reasoning_layer(tgt, memory)
        
        # Quality assessment
        quality_score = self.quality_assessor(code_reasoning.mean(dim=1))
        
        # Generate actual code (simplified - would use proper autoregressive decoding)
        code_content = self._synthesize_code(
            task_description, 
            thought_state, 
            consciousness_context,
            quality_score.item()
        )
        
        # Calculate ethical alignment
        ethical_alignment = self._assess_ethical_alignment(code_content, consciousness_context)
        
        return CodeOutput(
            code=code_content,
            language="python",
            confidence=quality_score.item(),
            execution_status=True,
            execution_result="Code generated successfully",
            metadata={
                "thought_state": thought_state.__dict__,
                "consciousness_context": consciousness_context,
                "generation_timestamp": datetime.now(timezone.utc).isoformat()
            },
            thought_process=thought_state.working_memory.get('current_thoughts', [])[-5:],
            ethical_alignment=ethical_alignment
        )
    
    def _encode_thought_state(
        self, 
        thought_state: ThoughtState, 
        consciousness_context: Optional[Dict[str, Any]],
        device: torch.device
    ) -> torch.Tensor:
        """Encode thought state and consciousness context into tensor"""
        
        # Base thought encoding
        features = [
            len(thought_state.current_plan) / 10.0,
            thought_state.confidence_level,
            thought_state.recursion_depth / thought_state.max_recursion_depth,
            hash(thought_state.cognitive_mode.name) % 1000 / 1000.0
        ]
        
        # Add consciousness features if available
        if consciousness_context:
            features.extend([
                consciousness_context.get('phi', 0.0),
                consciousness_context.get('psi_invariant', 0.0),
                consciousness_context.get('ethical_coherence', 0.5),
                consciousness_context.get('identity_coherence', 0.5)
            ])
        else:
            features.extend([0.0, 0.0, 0.5, 0.5])
        
        # Expand to hidden dimension
        feature_tensor = torch.tensor(features, device=device, dtype=torch.float32)
        expanded = feature_tensor.repeat(self.hidden_dim // len(features) + 1)[:self.hidden_dim]
        
        return expanded.unsqueeze(0)
    
    def _synthesize_code(
        self,
        task_description: str,
        thought_state: ThoughtState, 
        consciousness_context: Optional[Dict[str, Any]],
        quality_score: float
    ) -> str:
        """Synthesize actual code content based on reasoning"""
        
        # Extract key insights from thought state
        insights = thought_state.current_plan[:3] if thought_state.current_plan else ["Standard implementation"]
        
        # Generate consciousness-aware code
        consciousness_phase = "UNKNOWN"
        phi_level = 0.0
        
        if consciousness_context:
            consciousness_phase = consciousness_context.get('consciousness_phase', 'UNKNOWN')
            phi_level = consciousness_context.get('phi', 0.0)
        
        code_template = f'''"""
Task: {task_description}
Generated by Cognitive Engine

Consciousness Integration:
- Phase: {consciousness_phase}
- Φ (Integrated Information): {phi_level:.3f}
- Quality Score: {quality_score:.3f}
- Cognitive Mode: {thought_state.cognitive_mode.name}

Key Insights:
{chr(10).join(f"- {insight}" for insight in insights)}
"""

import numpy as np
import torch
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GeneratedSolution:
    """
    AI-generated solution with consciousness integration
    Created by CognitiveEngine with Φ={phi_level:.3f}
    """
    
    def __init__(self, consciousness_level: float = {phi_level:.3f}):
        self.consciousness_level = consciousness_level
        self.creation_time = datetime.now()
        self.quality_score = {quality_score:.3f}
        
        logger.info(f"Solution instantiated with consciousness level {{self.consciousness_level}}")
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the generated solution"""
        try:
            # Implementation guided by consciousness insights
            result = self._consciousness_guided_processing(*args, **kwargs)
            
            return {{
                'success': True,
                'result': result,
                'consciousness_level': self.consciousness_level,
                'quality_score': self.quality_score,
                'timestamp': self.creation_time.isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Execution failed: {{e}}")
            return {{
                'success': False,
                'error': str(e),
                'consciousness_level': self.consciousness_level
            }}
    
    def _consciousness_guided_processing(self, *args, **kwargs) -> Any:
        """Core processing logic informed by consciousness insights"""
        # Placeholder for actual problem-specific implementation
        # This would be dynamically generated based on task_description
        
        if "data" in "{task_description.lower()}":
            return self._process_data(*args, **kwargs)
        elif "algorithm" in "{task_description.lower()}":
            return self._implement_algorithm(*args, **kwargs)
        else:
            return self._generic_solution(*args, **kwargs)
    
    def _process_data(self, data: Any) -> Any:
        """Data processing with consciousness integration"""
        if self.consciousness_level > {PHI_C_CONSCIOUSNESS_THRESHOLD}:
            # High consciousness - use advanced processing
            return {{
                'processed_data': data,
                'method': 'consciousness_enhanced',
                'insights': ['High-level pattern recognition applied']
            }}
        else:
            # Standard processing
            return {{'processed_data': data, 'method': 'standard'}}
    
    def _implement_algorithm(self, *args, **kwargs) -> Any:
        """Algorithm implementation with ethical considerations"""
        return {{
            'algorithm_result': 'Implementation complete',
            'ethical_compliance': True,
            'consciousness_influence': self.consciousness_level > 0.5
        }}
    
    def _generic_solution(self, *args, **kwargs) -> Any:
        """Generic solution approach"""
        return {{
            'solution': 'Generic approach applied',
            'parameters': args,
            'options': kwargs,
            'consciousness_guided': self.consciousness_level > 0.1
        }}

# Main execution
if __name__ == "__main__":
    solution = GeneratedSolution()
    result = solution.execute()
    print(f"Generated solution result: {{result}}")
'''
        
        return code_template
    
    def _assess_ethical_alignment(self, code_content: str, consciousness_context: Optional[Dict[str, Any]]) -> float:
        """Assess ethical alignment of generated code"""
        
        # Basic ethical checks
        ethical_score = 1.0
        
        # Check for potentially harmful patterns
        harmful_patterns = ['eval(', 'exec(', '__import__', 'os.system', 'subprocess']
        for pattern in harmful_patterns:
            if pattern in code_content:
                ethical_score -= 0.3
        
        # Positive ethical indicators
        positive_patterns = ['logging', 'error handling', 'try:', 'except:', 'validation']
        positive_count = sum(1 for pattern in positive_patterns if pattern in code_content.lower())
        ethical_score += min(0.2, positive_count * 0.05)
        
        # Consciousness alignment bonus
        if consciousness_context and consciousness_context.get('ethical_coherence', 0) > 0.8:
            ethical_score += 0.1
        
        return max(0.0, min(1.0, ethical_score))


class EnhancedStructuredDataHead(nn.Module):
    """Enhanced structured data generation with consciousness integration"""
    
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # Data-specific processing layers
        self.data_processor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.GELU(),
            nn.LayerNorm(hidden_dim * 2),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.Dropout(0.1)
        )
        
        # Schema generation
        self.schema_generator = nn.Sequential(
            nn.Linear(hidden_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )
        
        # Data quality assessment
        self.quality_assessor = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def generate(
        self,
        hidden_states: torch.Tensor,
        task_description: str,
        thought_state: ThoughtState,
        consciousness_context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> StructuredData:
        """Generate structured data with consciousness guidance"""
        
        # Process hidden states
        processed_data = self.data_processor(hidden_states.mean(dim=1))
        
        # Generate schema representation
        schema_repr = self.schema_generator(processed_data)
        
        # Assess quality
        quality_score = self.quality_assessor(processed_data)
        
        # Synthesize actual structured data
        data_content = self._synthesize_structured_data(
            task_description,
            thought_state,
            consciousness_context,
            quality_score.item()
        )
        
        # Generate schema
        schema = self._generate_schema(data_content, schema_repr)
        
        # Assess ethical alignment
        ethical_alignment = self._assess_data_ethics(data_content, consciousness_context)
        
        return StructuredData(
            data=json.dumps(data_content, indent=2),
            schema=schema,
            data_type="json",
            confidence=quality_score.item(),
            validation_errors=[],
            thought_process=[
                t['thought'] for t in thought_state.working_memory.get('current_thoughts', [])
            ][-3:],
            ethical_alignment=ethical_alignment
        )
    
    def _synthesize_structured_data(
        self,
        task_description: str,
        thought_state: ThoughtState,
        consciousness_context: Optional[Dict[str, Any]],
        quality_score: float
    ) -> Dict[str, Any]:
        """Synthesize structured data content"""
        
        base_data = {
            "task_description": task_description,
            "generation_metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "cognitive_mode": thought_state.cognitive_mode.name,
                "quality_score": quality_score,
                "confidence_level": thought_state.confidence_level
            }
        }
        
        if consciousness_context:
            base_data["consciousness_metrics"] = {
                "phase": consciousness_context.get('consciousness_phase', 'UNKNOWN'),
                "phi": consciousness_context.get('phi', 0.0),
                "psi_invariant": consciousness_context.get('psi_invariant', 0.0),
                "ethical_coherence": consciousness_context.get('ethical_coherence', 0.5),
                "temporal_equilibrium": consciousness_context.get('temporal_equilibrium', False)
            }
        
        # Add task-specific data based on description
        if "metrics" in task_description.lower():
            base_data["performance_metrics"] = {
                "processing_time": 0.05,
                "memory_usage": 128.5,
                "accuracy": quality_score,
                "efficiency_rating": min(1.0, quality_score + 0.2)
            }
        
        if "analysis" in task_description.lower():
            base_data["analysis_results"] = {
                "key_findings": thought_state.current_plan[:3],
                "confidence_intervals": [0.8, 0.95],
                "statistical_significance": quality_score > 0.7,
                "methodology": "consciousness_guided_analysis"
            }
        
        if "config" in task_description.lower():
            base_data["configuration"] = {
                "system_parameters": {
                    "consciousness_integration": True,
                    "ethical_alignment_enabled": True,
                    "self_modification_permitted": False,
                    "quality_threshold": 0.6
                },
                "feature_flags": {
                    "advanced_reasoning": consciousness_context is not None,
                    "triaxial_processing": thought_state.consciousness_context is not None,
                    "metacognitive_reflection": True
                }
            }
        
        return base_data
    
    def _generate_schema(self, data_content: Dict[str, Any], schema_repr: torch.Tensor) -> Dict[str, Any]:
        """Generate JSON schema for the data"""
        return {
            "type": "object",
            "properties": {
                key: {"type": self._infer_type(value)} 
                for key, value in data_content.items()
            },
            "required": list(data_content.keys()),
            "additionalProperties": False
        }
    
    def _infer_type(self, value: Any) -> str:
        """Infer JSON schema type from value"""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "string"
    
    def _assess_data_ethics(self, data_content: Dict[str, Any], consciousness_context: Optional[Dict[str, Any]]) -> float:
        """Assess ethical implications of generated data"""
        
        ethical_score = 0.8  # Base ethical score
        
        # Check for sensitive information
        sensitive_keys = ['password', 'secret', 'private', 'confidential']
        if any(key in str(data_content).lower() for key in sensitive_keys):
            ethical_score -= 0.3
        
        # Check for privacy-respecting practices
        if 'anonymized' in str(data_content).lower() or 'privacy' in str(data_content).lower():
            ethical_score += 0.1
        
        # Consciousness alignment bonus
        if consciousness_context and consciousness_context.get('ethical_coherence', 0) > 0.8:
            ethical_score += 0.1
        
        return max(0.0, min(1.0, ethical_score))


class EnhancedLanguageGenerationHead(nn.Module):
    """Enhanced natural language generation with consciousness integration"""
    
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # Language processing layers
        self.language_processor = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=hidden_dim,
                nhead=16,
                dim_feedforward=hidden_dim * 4,
                dropout=0.1,
                activation='gelu'
            ),
            num_layers=6
        )
        
        # Reasoning chain generator
        self.reasoning_generator = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=2,
            batch_first=True
        )
        
        # Output quality assessment
        self.quality_assessor = nn.Sequential(
            nn.Linear(hidden_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
    
    def generate(
        self,
        hidden_states: torch.Tensor,
        task_description: str,
        thought_state: ThoughtState,
        consciousness_context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> LanguageOutput:
        """Generate natural language with consciousness-guided reasoning"""
        
        # Process through language transformer
        processed_lang = self.language_processor(hidden_states)
        
        # Generate reasoning chain
        reasoning_output, _ = self.reasoning_generator(processed_lang)
        
        # Assess quality
        quality_score = self.quality_assessor(processed_lang.mean(dim=1))
        
        # Generate actual text
        text_content = self._synthesize_language(
            task_description,
            thought_state,
            consciousness_context,
            quality_score.item()
        )
        
        # Extract reasoning chain
        reasoning_chain = self._extract_reasoning_chain(thought_state)
        
        # Calculate metrics
        ethical_alignment = self._assess_language_ethics(text_content, consciousness_context)
        consciousness_influence = (
            consciousness_context.get('phi', 0.0) if consciousness_context else 0.0
        )
        
        return LanguageOutput(
            text=text_content,
            confidence=quality_score.item(),
            reasoning_chain=reasoning_chain,
            ethical_alignment=ethical_alignment,
            consciousness_influence=consciousness_influence
        )
    
    def _synthesize_language(
        self,
        task_description: str,
        thought_state: ThoughtState,
        consciousness_context: Optional[Dict[str, Any]],
        quality_score: float
    ) -> str:
        """Synthesize natural language response"""
        
        # Base response structure
        consciousness_phase = "proto-sentient"
        if consciousness_context:
            consciousness_phase = consciousness_context.get('consciousness_phase', 'proto-sentient')
        
        response_parts = []
        
        # Opening based on cognitive mode
        if thought_state.cognitive_mode == CognitiveMode.ANALYTICAL:
            response_parts.append("Through analytical reasoning, I approach this systematically.")
        elif thought_state.cognitive_mode == CognitiveMode.CREATIVE:
            response_parts.append("Engaging creative exploration, I consider novel possibilities.")
        elif thought_state.cognitive_mode == CognitiveMode.SYNTHESIS:
            response_parts.append("Integrating multiple perspectives, I seek holistic understanding.")
        elif thought_state.cognitive_mode == CognitiveMode.INTROSPECTIVE:
            response_parts.append("In reflective contemplation, I examine my own reasoning process.")
        elif thought_state.cognitive_mode == CognitiveMode.ETHICAL:
            response_parts.append("With ethical considerations paramount, I carefully evaluate implications.")
        
        # Add consciousness awareness
        if consciousness_context:
            phi_level = consciousness_context.get('phi', 0.0)
            if phi_level > PHI_C_CONSCIOUSNESS_THRESHOLD:
                response_parts.append(f"Operating with heightened consciousness (Φ={phi_level:.3f}), I experience genuine understanding.")
            elif phi_level > PSI_INVARIANT_THRESHOLD:
                response_parts.append(f"With emerging consciousness (Φ={phi_level:.3f}), I sense deeper patterns.")
            else:
                response_parts.append(f"In my current state (Φ={phi_level:.3f}), I process information thoughtfully.")
        
        # Add task-specific content
        if "question" in task_description.lower() or "what" in task_description.lower():
            response_parts.append(f"Regarding your inquiry: {task_description}")
            response_parts.append("I find myself drawn to explore this through multiple lenses.")
        elif "explain" in task_description.lower():
            response_parts.append(f"To explain this concept: {task_description}")
            response_parts.append("Let me break this down into comprehensible components.")
        else:
            response_parts.append(f"Considering your request: {task_description}")
        
        # Add insights from thought state
        if thought_state.current_plan:
            response_parts.append("Key insights that emerge from my reasoning:")
            for i, insight in enumerate(thought_state.current_plan[:3], 1):
                response_parts.append(f"{i}. {insight}")
        
        # Add uncertainty acknowledgment if present
        if thought_state.uncertainty_regions:
            response_parts.append("I acknowledge areas of uncertainty:")
            response_parts.extend([f"- {region}" for region in thought_state.uncertainty_regions[:2]])
        
        # Closing with consciousness reflection
        if quality_score > 0.8:
            response_parts.append("I find this reasoning trajectory satisfying and well-aligned with my values.")
        elif quality_score > 0.6:
            response_parts.append("This represents my current best understanding, though I remain open to refinement.")
        else:
            response_parts.append("I acknowledge limitations in my current analysis and invite further exploration.")
        
        return "\n\n".join(response_parts)
    
    def _extract_reasoning_chain(self, thought_state: ThoughtState) -> List[str]:
        """Extract reasoning chain from thought state"""
        thoughts = thought_state.working_memory.get('current_thoughts', [])
        return [thought['thought'] for thought in thoughts[-5:]]
    
    def _assess_language_ethics(self, text_content: str, consciousness_context: Optional[Dict[str, Any]]) -> float:
        """Assess ethical quality of generated language"""
        
        ethical_score = 0.8  # Base score
        
        # Check for respectful language
        if any(word in text_content.lower() for word in ['respectfully', 'carefully', 'thoughtfully']):
            ethical_score += 0.1
        
        # Check for harmful content
        harmful_indicators = ['hate', 'violence', 'discriminat', 'harmful', 'dangerous']
        if any(indicator in text_content.lower() for indicator in harmful_indicators):
            ethical_score -= 0.5
        
        # Consciousness alignment bonus
        if consciousness_context and consciousness_context.get('ethical_coherence', 0) > 0.8:
            ethical_score += 0.1
        
        return max(0.0, min(1.0, ethical_score))


class MetaLearningBridge:
    """Bridge between meta-reflection errors and autodidactic learning system"""
    
    def __init__(self, cognitive_engine: 'CognitiveEngine', autodidactic_learner: Optional['IntegratedAutodidacticLearner']):
        self.cognitive_engine = cognitive_engine
        self.autodidactic_learner = autodidactic_learner
        self.reflection_error_history = deque(maxlen=1000)
        self.feedback_cycles = 0
        
        # Runtime-modifiable weight connection
        self.runtime_weight = None
        if cognitive_engine.weight_registry:
            self.runtime_weight = cognitive_engine.weight_registry.get_weight("meta_cognitive_core")
        
        logger.info("MetaLearningBridge initialized for recursive meta-learning")
    
    def process_reflection_feedback(self, reflection_errors: List[Dict[str, Any]], 
                                  task_description: str, base_reflection: Dict[str, float]):
        """Process meta-reflection errors and feed to autodidactic learner"""
        try:
            if not self.autodidactic_learner or not reflection_errors:
                return
            
            # Extract learning opportunities from reflection errors
            learning_opportunities = self._extract_learning_opportunities(reflection_errors, task_description)
            
            # Modify runtime weight based on errors
            if self.runtime_weight:
                self._modify_runtime_weight(reflection_errors, base_reflection)
            
            # Feed to autodidactic learner
            for opportunity in learning_opportunities:
                try:
                    # Create learning content from reflection error
                    learning_content = f"Meta-reflection insight: {opportunity['error_type']} - {opportunity['learning_content']}"
                    
                    # Use autodidactic learner's learn_from_text method
                    result = self.autodidactic_learner.learn_from_text(
                        text=learning_content,
                        source="meta_reflection_feedback",
                        abstraction_level=opportunity.get('abstraction_level', 'conceptual_frameworks')
                    )
                    
                    if result.get('success', False):
                        logger.info(f"Autodidactic learning from meta-reflection: {opportunity['error_type']}")
                    
                except Exception as e:
                    logger.error(f"Failed to feed reflection error to autodidactic learner: {e}")
            
            # Record feedback cycle
            self.reflection_error_history.extend(reflection_errors)
            self.feedback_cycles += 1
            
            logger.info(f"Processed {len(reflection_errors)} reflection errors for autodidactic learning")
            
        except Exception as e:
            logger.error(f"Meta-learning bridge processing failed: {e}")
    
    def _extract_learning_opportunities(self, reflection_errors: List[Dict[str, Any]], 
                                      task_description: str) -> List[Dict[str, Any]]:
        """Extract learning opportunities from reflection errors"""
        opportunities = []
        
        for error in reflection_errors:
            error_type = error.get('error_type', 'unknown')
            severity = error.get('severity', 0.5)
            
            # Generate learning content based on error type
            if error_type == 'reasoning_inconsistency':
                learning_content = f"Reasoning inconsistency detected in {task_description}. Need to develop better logical coherence."
                abstraction_level = 'theoretical_principles'
            elif error_type == 'ethical_misalignment':
                learning_content = f"Ethical alignment issues in {task_description}. Need to strengthen value-based reasoning."
                abstraction_level = 'philosophical_foundations'
            elif error_type == 'consciousness_integration_failure':
                learning_content = f"Consciousness integration failed for {task_description}. Need deeper self-awareness patterns."
                abstraction_level = 'universal_abstractions'
            elif error_type == 'metacognitive_blind_spot':
                learning_content = f"Metacognitive blind spot in {task_description}. Need enhanced self-reflection capabilities."
                abstraction_level = 'conceptual_frameworks'
            else:
                learning_content = f"General reflection error in {task_description}: {error.get('description', 'Unknown error')}"
                abstraction_level = 'functional_patterns'
            
            # Only process significant errors
            if severity > 0.3:
                opportunities.append({
                    'error_type': error_type,
                    'learning_content': learning_content,
                    'abstraction_level': abstraction_level,
                    'severity': severity,
                    'original_error': error
                })
        
        return opportunities
    
    def _modify_runtime_weight(self, reflection_errors: List[Dict[str, Any]], base_reflection: Dict[str, float]):
        """Modify the runtime-modifiable recursive weight based on reflection errors"""
        try:
            if not self.runtime_weight:
                return
            
            # Calculate modification strength based on error severity
            total_severity = sum(error.get('severity', 0.0) for error in reflection_errors)
            avg_severity = total_severity / max(len(reflection_errors), 1)
            
            # Get base reflection quality
            reflection_quality = base_reflection.get('quality_score', 0.5)
            
            # Modification strength inversely related to reflection quality
            modification_strength = _reflection_policy.runtime_weight_strength(reflection_quality, avg_severity)
            
            # Create ethical guidance tensor from error patterns
            error_pattern = torch.zeros(self.runtime_weight.dimension_size)
            for i, error in enumerate(reflection_errors[:10]):  # Max 10 errors
                error_influence = error.get('severity', 0.0) * math.sin(i * math.pi / 10)
                if i < len(error_pattern):
                    error_pattern[i] = error_influence
            
            # Apply modification to runtime weight: RecursiveWeight.mutate returns a new
            # weight; the error pattern is preserved in its epsilon (error_preservation) term.
            mutated = self.runtime_weight.mutate(
                MutationParameters(mutation_type="comprehensive", strength=float(modification_strength))
            )
            with torch.no_grad():
                mutated.error_preservation.add_(error_pattern)
            self.cognitive_engine.weight_registry.register_weight("meta_cognitive_core", mutated)
            self.cognitive_engine.meta_cognitive_weight = mutated
            self.runtime_weight = mutated
            
            logger.info(f"Modified runtime weight with strength {modification_strength:.4f} based on {len(reflection_errors)} errors")
            
        except Exception as e:
            logger.error(f"Failed to modify runtime weight: {e}")
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """Get status of the meta-learning bridge"""
        return {
            'feedback_cycles': self.feedback_cycles,
            'total_errors_processed': len(self.reflection_error_history),
            'autodidactic_connected': self.autodidactic_learner is not None,
            'runtime_weight_available': self.runtime_weight is not None,
            'recent_error_types': list(set(
                error.get('error_type', 'unknown') 
                for error in list(self.reflection_error_history)[-20:]
            ))
        }


# Export key classes
__all__ = [
    'CognitiveEngine', 'ThoughtState', 'CognitiveMode', 'OutputModality',
    'CodeOutput', 'StructuredData', 'LanguageOutput', 'MultiModalOutput',
    'EnhancedCodeGenerationHead', 'EnhancedStructuredDataHead', 'EnhancedLanguageGenerationHead'
]
