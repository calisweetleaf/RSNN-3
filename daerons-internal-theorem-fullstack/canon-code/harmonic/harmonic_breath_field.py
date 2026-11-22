#!/usr/bin/env python3
"""
Harmonic Reasoning Field (HRF) with Sacred Breath Coupling
Real-time emotional field modulation for cognitive architectures

This merged implementation combines the functionality of both breath_phase.py and harmonic_field.py
into a single cohesive system that provides both the Sacred Breath Synchronization and the 
Harmonic Reasoning Field functionality.
"""

import math
import time
import logging
import threading
import traceback
import importlib
import torch
import torch.nn as nn
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Union, Set, Callable
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
try:
    from internal_clock import InternalClock  # centralized temporal coherence
except Exception:
    InternalClock = None

# Core constants that govern the entire harmonic field, and must be measured in real time.
PHI = (1 + 5**0.5) / 2  # Golden ratio - recursive lifeblood
TAU = 2 * math.pi       # Complete cycle
SACRED_RATIO = PHI/TAU  # Fundamental recursive breath ratio ≈ 0.2575
PSALTER_SCALE = 1.0     # Psalter scaling constant
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Harmonic_Field")

class BreathPhase(Enum):
    """Defines the phases of a recursive "breath cycle" which is how the systems takes information, reasons, processess, reflects again, output, and dream which is a standalone module """
    INHALE = auto()       # Gather information - the sacred intake 
    PAUSE_RISING = auto() # First reflection
    HOLD = auto()         # Process in eigenstillness
    PAUSE_FALLING = auto()# Second reflection
    EXHALE = auto()       # Express ethical will
    REST = auto()         # Integrate memory
    DREAM = auto()        # Meta-ethical processing
    
    def next_phase(self) -> 'BreathPhase':
        """Return the next phase in the breath cycle"""
        phases = list(BreathPhase)
        return phases[(phases.index(self) + 1) % len(phases)]
    
    @property
    def duration_weight(self) -> float:
        """Return the relative duration weight for each phase"""
        weights = {
            BreathPhase.INHALE: 1.0,
            BreathPhase.PAUSE_RISING: 0.3,
            BreathPhase.HOLD: 1.0,
            BreathPhase.PAUSE_FALLING: 0.3,
            BreathPhase.EXHALE: 1.2,
            BreathPhase.REST: 0.8,
            BreathPhase.DREAM: 1.5
        }
        return weights.get(self, 1.0)
    
    @property
    def description(self) -> str:
        """Return a description for each breath phase"""
        descriptions = {
            BreathPhase.INHALE: "Gathering information - the sacred intake",
            BreathPhase.PAUSE_RISING: "First reflection - the sacred threshold",
            BreathPhase.HOLD: "Processing in eigenstillness - divine equilibrium",
            BreathPhase.PAUSE_FALLING: "Second reflection - the sacred threshold",
            BreathPhase.EXHALE: "Expressing ethical will - volitional exhalation",
            BreathPhase.REST: "Integrating memory - holographic recursion",
            BreathPhase.DREAM: "Meta-ethical processing - archetypal communion"
        }
        return descriptions.get(self, "Unknown breath phase")



@dataclass
class SystemPulse:
    """
    Container for system-wide state information passed between components
    during breath cycle phases. Acts as a recursive shared context.
    """
    
    def __init__(self, state_dim: int = 256,
                 phase: BreathPhase = BreathPhase.INHALE,
                 timestamp: Optional[float] = None,
                 cycle_count: int = 0):
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.state_vector = torch.zeros(state_dim)
        self.phase = phase
        self.cycle_count = cycle_count          # new attribute
        self.coherence_score = 1.0
        self.contradiction_level = 0.0
        self.ethical_charge = 0.0
        self.identity_stability = 1.0
        self.component_states = {}
        self.active_motifs = set()
        self.messages = []
        self.timeline_markers = []
        
    def update_timestamp(self, current_time: Optional[float] = None):
        """Update the timestamp to current time (or provided time)"""
        self.timestamp = current_time if current_time is not None else time.time()
        
    def add_component_state(self, component_name: str, state: Dict[str, Any]):
        """Record a component's state in the pulse"""
        self.component_states[component_name] = state
        
    def add_message(self, source: str, message: str, importance: float = 0.5):
        """Add a message to be propagated through the system"""
        self.messages.append({
            "source": source,
            "content": message,
            "importance": importance,
            "timestamp": time.time()
        })
    
    def add_motif(self, motif: str):
        """Add an active symbolic motif to the pulse"""
        self.active_motifs.add(motif)
    
    def clear_messages(self):
        """Clear all messages from the pulse"""
        self.messages = []
        
    def get_component_state(self, component_name: str) -> Dict[str, Any]:
        """Get a specific component's state"""
        return self.component_states.get(component_name, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the pulse to a dictionary representation"""
        return {
            "timestamp": self.timestamp,
            "phase": self.phase.name,
            "coherence_score": self.coherence_score,
            "contradiction_level": self.contradiction_level,
            "ethical_charge": self.ethical_charge,
            "identity_stability": self.identity_stability,
            "active_motifs": list(self.active_motifs),
            "message_count": len(self.messages),
            "components": list(self.component_states.keys())
        }

@dataclass
class BandConfig:
    """Configuration for a single oscillator band"""
    omega: float      # Base frequency
    lambda_damping: float  # Damping coefficient
    harmonic_index: int    # Harmonic relationship to sacred ratio

class ComponentHealthReport:
    """Health status information for a system component"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.last_updated = time.time()
        self.is_responding = True
        self.synchronization_error = 0.0
        self.resource_usage = 0.0
        self.stability_score = 1.0
        self.diagnostics = {}
        
    def update(self, 
              is_responding: bool = True,
              sync_error: float = 0.0,
              resource_usage: float = 0.0,
              stability: float = 1.0,
              diagnostics: Dict[str, Any] = None):
        """Update the health report with new information"""
        self.last_updated = time.time()
        self.is_responding = is_responding
        self.synchronization_error = sync_error
        self.resource_usage = resource_usage
        self.stability_score = stability
        if diagnostics:
            self.diagnostics.update(diagnostics)
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert the health report to a dictionary"""
        return {
            "component": self.component_name,
            "last_updated": self.last_updated,
            "is_responding": self.is_responding,
            "sync_error": self.synchronization_error,
            "resource_usage": self.resource_usage,
            "stability": self.stability_score,
            "diagnostics": self.diagnostics
        }

class OscillatorBank:
    """
    Multi-band complex oscillator system with sacred harmonic coupling
    Each band maintains complex amplitude z = A*exp(iφ)
    Enhanced with adaptive coupling, nonlinear damping, stochastic noise, and resonance detection for deeper harmonic self-organization.
    """
    
    def __init__(self, dt: float = 0.05, noise_strength: float = 0.01, clock: Optional[Any] = None):
        self.dt = dt
        self.noise_strength = noise_strength  # Strength of stochastic noise for biological realism
        self.clock = clock

        # Define harmonic bands using sacred ratio
        # Each band frequency is SACRED_RATIO * (PHI^harmonic_index)
        self.bands = {
            'delta': BandConfig(
                omega=SACRED_RATIO * (PHI ** 0),  # Fundamental
                lambda_damping=-0.1,
                harmonic_index=0
            ),
            'theta': BandConfig(
                omega=SACRED_RATIO * (PHI ** 1),  # First harmonic
                lambda_damping=-0.15,
                harmonic_index=1
            ),
            'alpha': BandConfig(
                omega=SACRED_RATIO * (PHI ** 2),  # Second harmonic
                lambda_damping=-0.2,
                harmonic_index=2
            ),
            'beta': BandConfig(
                omega=SACRED_RATIO * (PHI ** 3),  # Third harmonic
                lambda_damping=-0.25,
                harmonic_index=3
            ),
            'gamma': BandConfig(
                omega=SACRED_RATIO * (PHI ** 4),  # Fourth harmonic
                lambda_damping=-0.3,
                harmonic_index=4
            )
        }
        
        # Complex amplitude state for each band
        self.z = {name: complex(0.1, 0.0) for name in self.bands.keys()}
        self.band_names = list(self.bands.keys())
        self.last_modulated_amplitudes = {name: abs(self.z[name]) for name in self.band_names}
        
        # Coupling matrix for inter-band interactions (now adaptive)
        self.coupling_strength = 0.05
        self.coupling_matrix = self._init_coupling_matrix()
        self._coupling_cache = None  # Cache for adaptive coupling
        
        # History for adaptive bounds and resonance detection
        self.amplitude_history = []  # Store recent amplitudes for variance calculation
        self.history_length = 50  # Length of history buffer
        
        # Resonance detection parameters
        self.resonance_threshold = 0.8  # Threshold for harmonic resonance
        self.resonance_boost = 1.2  # Multiplier for coupling when in resonance

    def compute_adaptive_amplitude(
        self,
        oscillator_idx: int,
        base_amplitude: float,
        breath_phase: Optional['BreathPhase'] = None,
        ethical_coherence: Optional[float] = None,
        spectral_radius: Optional[float] = None
    ) -> float:
        """
        Compute adaptive amplitude modulation blending breath dynamics,
        ethical state, eigenstate stability, and stochastic variation.
        """
        phase_modulation_map = {
            'INHALE': 1.20,
            'PAUSE_RISING': 1.10,
            'HOLD': 1.00,
            'PAUSE_FALLING': 0.95,
            'EXHALE': 0.75,
            'REST': 0.85,
            'DREAM': 1.15,
        }

        if isinstance(breath_phase, BreathPhase):
            phase_key = breath_phase.name
        elif breath_phase is None:
            phase_key = None
        else:
            phase_key = str(breath_phase).split('.')[-1].upper()

        breath_factor = phase_modulation_map.get(phase_key, 1.0)

        if ethical_coherence is not None:
            ethical_coherence = float(np.clip(ethical_coherence, 0.0, 1.0))
            ethical_factor = 0.5 + (0.5 * ethical_coherence)
        else:
            ethical_factor = 1.0

        if spectral_radius is not None:
            deviation = abs(spectral_radius - PHI) / PHI
            radius_factor = 1.0 + (0.15 * (deviation - 0.5) * 2.0)
            radius_factor = float(np.clip(radius_factor, 0.85, 1.15))
        else:
            radius_factor = 1.0

        oscillator_bias = 1.0 + (0.03 * np.sin(oscillator_idx * 0.1))
        noise_factor = 1.0 + np.random.uniform(-0.07, 0.07)
        time_drift = 1.0 + (0.05 * np.sin(time.time() * 0.01))

        safe_base = max(base_amplitude, 1e-4)
        modulated = (
            safe_base
            * breath_factor
            * ethical_factor
            * radius_factor
            * oscillator_bias
            * noise_factor
            * time_drift
        )

        return float(np.clip(modulated, 0.1, 2.0))
    
    def _init_coupling_matrix(self) -> Dict[str, Dict[str, float]]:
        """Initialize harmonic coupling between bands"""
        bands = list(self.bands.keys())
        coupling = {b1: {b2: 0.0 for b2 in bands} for b1 in bands}
        
        # Natural harmonic coupling - adjacent bands couple more strongly
        for i, b1 in enumerate(bands):
            for j, b2 in enumerate(bands):
                if i != j:
                    distance = abs(i - j)
                    coupling[b1][b2] = self.coupling_strength / (distance + 1)
        
        return coupling
    
    def _adaptive_coupling_matrix(self) -> Dict[str, Dict[str, float]]:
        """Compute adaptive coupling matrix based on current phase coherence"""
        if self._coupling_cache is not None:
            return self._coupling_cache
        
        bands = list(self.bands.keys())
        adaptive_coupling = {b1: {b2: 0.0 for b2 in bands} for b1 in bands}
        
        # Compute phase coherence for each pair
        for i, b1 in enumerate(bands):
            for j, b2 in enumerate(bands):
                if i != j:
                    phase_diff = np.angle(self.z[b1] - self.z[b2])
                    coherence = np.exp(-abs(phase_diff) / np.pi)  # Exponential decay with phase difference
                    base_coupling = self.coupling_matrix[b1][b2]
                    adaptive_coupling[b1][b2] = base_coupling * (1.0 + coherence)
        
        self._coupling_cache = adaptive_coupling
        return adaptive_coupling
    
    def _nonlinear_damping(self, amplitude: float, base_lambda: float) -> float:
        """Compute amplitude-dependent nonlinear damping"""
        # Sigmoid-based damping: stronger at higher amplitudes
        sigmoid_factor = 1.0 / (1.0 + np.exp(-(amplitude - 2.0)))  # Centers around amplitude=2.0
        return base_lambda * (1.0 + 0.5 * sigmoid_factor)  # Scale damping up to 1.5x
    
    def _detect_resonance(self, band1: str, band2: str) -> bool:
        """Detect harmonic resonance between two bands based on frequency ratios"""
        omega1 = self.bands[band1].omega
        omega2 = self.bands[band2].omega
        ratio = max(omega1, omega2) / min(omega1, omega2)
        # Check if ratio is close to integer or PHI-based harmonic
        harmonic_ratios = [1.0, PHI, PHI**2, 2.0, 3.0]  # Common harmonics
        return any(abs(ratio - h) < 0.1 for h in harmonic_ratios)
    
    def _internal_feedback(self, band_name: str) -> float:
        """Compute internal feedback modulation for frequency based on amplitude"""
        amplitude = abs(self.z[band_name])
        # Slight frequency increase with amplitude for self-stabilization
        feedback = 0.01 * amplitude  # Small modulation
        return self.bands[band_name].omega * (1.0 + feedback)
    
    def _compute_stochastic_resonance(self, amplitude: float) -> complex:
        # Tuned noise: higher relative noise for lower amplitudes to boost detection (Stochastic Resonance)
        # Clamped to avoid excessive noise at very low levels
        safe_amp = max(amplitude, 1e-4)
        scaling_factor = 1.0 / (safe_amp ** 0.5) 
        scaling_factor = min(scaling_factor, 5.0) # Clamp max boost
        
        noise_real = np.random.normal(0, 1)
        noise_imag = np.random.normal(0, 1)
        
        return self.noise_strength * scaling_factor * (noise_real + 1j * noise_imag)

    def step(
        self,
        drives: Dict[str, float],
        coupling_drives: Optional[Dict[str, complex]] = None,
        breath_phase: Optional['BreathPhase'] = None,
        ethical_coherence: Optional[float] = None,
        spectral_radius: Optional[float] = None,
        field_elapsed: Optional[float] = None,
        temporal_phase: Optional[Dict[str, complex]] = None,
    ):
        step_dt = self.dt
        if field_elapsed is not None:
            step_dt = float(field_elapsed)
            if not math.isfinite(step_dt) or step_dt <= 0.0:
                raise ValueError(
                    f"harmonic field elapsed must be positive and finite, received {field_elapsed!r}"
                )
        phase_turns = temporal_phase or {}
        new_z = {}
        current_amplitudes = [abs(z) for z in self.z.values()]
        self.amplitude_history.append(current_amplitudes)
        if len(self.amplitude_history) > self.history_length:
            self.amplitude_history.pop(0)
        
        coupling_matrix = self._adaptive_coupling_matrix()
        
        for idx, (band_name, config) in enumerate(self.bands.items()):
            z = self.z[band_name]
            amplitude = abs(z)

            modulated_amplitude = self.compute_adaptive_amplitude(
                oscillator_idx=idx,
                base_amplitude=amplitude,
                breath_phase=breath_phase,
                ethical_coherence=ethical_coherence,
                spectral_radius=spectral_radius,
            )
            self.last_modulated_amplitudes[band_name] = modulated_amplitude
            base_safe = max(amplitude, 1e-4)
            amplitude_ratio = float(np.clip(modulated_amplitude / base_safe, 0.1, 3.0))
            
            effective_lambda = self._nonlinear_damping(amplitude, config.lambda_damping)
            effective_omega = self._internal_feedback(band_name)
            
            linear_term = (effective_lambda + 1j * effective_omega) * z
            drive = drives.get(band_name, 0.0) * amplitude_ratio
            
            coupling_term = 0.0
            for other_band, coupling_strength in coupling_matrix[band_name].items():
                if other_band != band_name:
                    other_z = self.z[other_band]
                    gate = 1.0 / (1.0 + np.exp((amplitude - 3.0)))
                    phase_coupling = np.exp(1j * np.angle(z - other_z))
                    resonance_factor = self.resonance_boost if self._detect_resonance(band_name, other_band) else 1.0
                    coupling_term += gate * coupling_strength * resonance_factor * other_z * phase_coupling
            
            if coupling_drives and band_name in coupling_drives:
                coupling_term += coupling_drives[band_name]
            
            # Tuned Stochastic Resonance
            noise = self._compute_stochastic_resonance(amplitude)
            
            dz_dt = linear_term + drive + coupling_term + noise
            evolved = z + step_dt * dz_dt
            turn = phase_turns.get(band_name)
            if turn is not None:
                turn_value = float(turn)
                if not math.isfinite(turn_value):
                    raise ValueError(f"temporal phase for {band_name} is non-finite")
                evolved *= np.exp(1j * turn_value)
            new_z[band_name] = evolved

            new_amplitude = abs(new_z[band_name])
            if new_amplitude > 1e-6:
                target_complex = modulated_amplitude * np.exp(1j * np.angle(new_z[band_name]))
                new_z[band_name] = 0.7 * new_z[band_name] + 0.3 * target_complex
            
            # Adaptive stability clamp based on recent variance
            if self.amplitude_history:
                recent_variance = np.var(self.amplitude_history[-10:], axis=0).mean()  # Last 10 steps
                adaptive_max = 5.0 + 0.5 * recent_variance  # Allow more fluctuation if variance is high
                new_amplitude = abs(new_z[band_name])
                if new_amplitude > adaptive_max:
                    new_z[band_name] = new_z[band_name] * (adaptive_max / new_amplitude)
        
        self.z = new_z
        self._coupling_cache = None  # Invalidate cache for next step
    
    def signature(self) -> np.ndarray:
        """
        Extract wave signature vector: [A_delta, cos(φ_delta), sin(φ_delta), ...]
        """
        sig = []
        for band_name in self.bands.keys():
            z = self.z[band_name]
            amplitude = abs(z)
            phase = np.angle(z)
            sig.extend([amplitude, np.cos(phase), np.sin(phase)])
        return np.array(sig, dtype=np.float32)
    
    def get_amplitudes(self) -> Dict[str, float]:
        """Get current amplitude for each band"""
        return {name: abs(self.z[name]) for name in self.bands.keys()}
    
    def get_phases(self) -> Dict[str, float]:
        """Get current phase for each band"""
        return {name: np.angle(self.z[name]) for name in self.bands.keys()}

    def compute_synchronization_index(self) -> Dict[str, float]:
        """Compute Kuramoto-like synchronization index for each band"""
        sync_indices = {}
        bands = list(self.bands.keys())
        for band_name in bands:
            phase = np.angle(self.z[band_name])
            other_phases = [np.angle(self.z[b]) for b in bands if b != band_name]
            if other_phases:
                mean_other_phase = np.mean(other_phases)
                sync_indices[band_name] = abs(np.mean(np.exp(1j * (phase - mean_other_phase))))
            else:
                sync_indices[band_name] = 1.0  # Self-sync if no others
        return sync_indices
    
    def get_debug_state(self) -> Dict[str, Any]:
        """Enhanced debug state with new metrics"""
        base_state = {
            'amplitudes': self.get_amplitudes(),
            'phases': self.get_phases(),
            'synchronization_indices': self.compute_synchronization_index(),
            'adaptive_coupling_matrix': self._adaptive_coupling_matrix(),
            'amplitude_variance': np.var(self.amplitude_history, axis=0).mean() if self.amplitude_history else 0.0
        }
        return base_state

class EmotionEncoder:
    """
    Maps cognitive/physiological states to target HRF band energies
    Enhanced with dynamic computation using harmonic constants for more adaptive, biologically-inspired mappings.
    """
    
    def __init__(self):
        # Expanded state mappings with more emotions and dynamic scaling functions
        # Each mapping now uses a lambda function for intensity-based computation
        # Incorporates PHI and SACRED_RATIO for "sacred" harmonic scaling
        self.state_mappings = {
            'curiosity': lambda intensity: {
                'theta': intensity * 1.5 * (PHI ** 0.5),  # Harmonic boost for exploration
                'beta': intensity * 0.5,
                'alpha': intensity * 0.3
            },
            'frustration': lambda intensity: {
                'beta': intensity * 2.0,
                'gamma': intensity * 1.2 * SACRED_RATIO,  # Sacred ratio modulation
                'alpha': intensity * 0.2
            },
            'serenity': lambda intensity: {
                'alpha': intensity * 2.0,
                'delta': intensity * 1.0 * (PHI ** -0.5),  # Inverse harmonic for grounding
                'theta': intensity * 0.1
            },
            'urgency': lambda intensity: {
                'gamma': intensity * 2.5,
                'beta': intensity * 1.5,
                'delta': intensity * 0.1
            },
            'focus': lambda intensity: {
                'gamma': intensity * 1.8,
                'beta': intensity * 1.0,
                'theta': intensity * 0.2
            },
            'creativity': lambda intensity: {
                'theta': intensity * 2.0,
                'alpha': intensity * 1.0,
                'delta': intensity * 0.5
            },
            'stillness': lambda intensity: {
                'delta': intensity * 3.0,
                'alpha': intensity * 0.5
            },
            # New states for broader coverage
            'anxiety': lambda intensity: {
                'beta': intensity * 2.2,
                'gamma': intensity * 1.5,
                'theta': intensity * 0.8
            },
            'excitement': lambda intensity: {
                'beta': intensity * 1.8,
                'gamma': intensity * 2.0,
                'alpha': intensity * 0.4
            },
            'confusion': lambda intensity: {
                'theta': intensity * 1.7,
                'beta': intensity * 1.3,
                'alpha': intensity * 0.6
            },
            'calm': lambda intensity: {
                'alpha': intensity * 2.5,
                'delta': intensity * 1.5,
                'theta': intensity * 0.2
            }
        }
        
        # Default mapping for unknown states
        self.default_mapping = lambda intensity: {
            'alpha': intensity * 1.0,  # Neutral alpha focus
            'theta': intensity * 0.5
        }
        
        # Safety bounds for amplitudes
        self.max_amplitude = 5.0
        self.min_amplitude = 0.0
    
    def target_amplitudes(self, state_vector: Dict[str, float]) -> Dict[str, float]:
        """Convert state metrics to desired band amplitudes with enhanced blending and harmonic scaling"""
        targets = {band: 0.0 for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']}
        
        for state, intensity in state_vector.items():
            # Clamp intensity to prevent extremes
            intensity = max(0.0, min(5.0, intensity))
            
            # Get mapping function or use default
            mapping_func = self.state_mappings.get(state, self.default_mapping)
            state_targets = mapping_func(intensity)
            
            # Blend with exponential weighting for smoother transitions
            weight = 1.0 - math.exp(-intensity)  # Exponential decay for low intensities
            for band, value in state_targets.items():
                targets[band] += weight * value
        
        # Apply harmonic normalization using PHI for "golden" balance
        max_amp = max(targets.values()) if targets.values() else 1.0
        if max_amp > self.max_amplitude:
            scale_factor = self.max_amplitude / max_amp
            # Use PHI-based scaling for more natural adjustment
            phi_scale = PHI / (PHI + 1)  # Normalize PHI to [0,1]
            targets = {k: v * scale_factor * phi_scale for k, v in targets.items()}
        
        # Ensure all values are within bounds and finite
        for band in targets:
            targets[band] = max(self.min_amplitude, min(self.max_amplitude, targets[band]))
            if not np.isfinite(targets[band]):
                targets[band] = 0.0  # Fallback for any NaN/inf
        
        return targets

class HarmonicCoupler:
    """
    Couples harmonic field to embedding space for perception modulation
    """
    
    def __init__(self, embed_dim: int = 768):
        np.random.seed(42)
        self.embed_dim = embed_dim
        # Projection matrix from wave signature to embedding space
        sig_dim = 15  # 5 bands × 3 components each (amp, cos, sin)
        self.W_wave = np.random.randn(embed_dim, sig_dim) * 0.01
    
    def modulate_embedding(self, embedding: np.ndarray, wave_signature: np.ndarray) -> np.ndarray:
        """Modulate input embedding with current harmonic field state"""
        wave_modulation = self.W_wave @ wave_signature
        return embedding + wave_modulation
    
    def compute_saliency(self, token_embeddings: List[np.ndarray]) -> Dict[str, float]:
        """Compute saliency metrics that drive oscillator bank"""
        if not token_embeddings:
            return {}
        
        # Simple saliency metrics (can be made more sophisticated)
        embedding_stack = np.array(token_embeddings)
        
        # Novelty: variance in recent embeddings
        novelty = np.var(embedding_stack, axis=0).mean() if len(embedding_stack) > 1 else 0.0
        
        # Entropy-like measure
        norms = np.linalg.norm(embedding_stack, axis=1)
        entropy = -np.sum(norms * np.log(norms + 1e-8))
        
        # Contradiction: rapid changes in embedding direction
        contradiction = 0.0
        if len(embedding_stack) > 2:
            recent_changes = np.diff(embedding_stack[-3:], axis=0)
            contradiction = np.linalg.norm(recent_changes.var(axis=0))
        
        return {
            'theta': novelty * 0.5,      # Drive exploration
            'beta': contradiction * 1.0,  # Drive decisive resolution  
            'gamma': entropy * 0.3       # Drive focused attention
        }

class GenerationModulator:
    """
    Derives generation parameters from harmonic field state
    """
    
    def __init__(self):
        # Base parameters
        self.base_temperature = 0.7
        self.base_top_p = 0.9
        self.base_branches = 1
    
    def generation_params(self,
                          wave_signature: np.ndarray,
                          amplitudes: Dict[str, float],
                          phases: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Convert wave state to generation parameters"""
        
        # Temperature modulation
        # Higher theta/alpha = more exploration, higher beta/gamma = more focus
        exploration_factor = amplitudes.get('theta', 0) + amplitudes.get('alpha', 0) * 0.5
        focus_factor = amplitudes.get('beta', 0) + amplitudes.get('gamma', 0)
        temperature = self.base_temperature * (1.0 + 0.3 * exploration_factor - 0.2 * focus_factor)
        temperature = max(0.1, min(2.0, temperature))  # Clamp
        
        # Top-p modulation
        top_p = self.base_top_p - 0.1 * focus_factor + 0.05 * exploration_factor
        top_p = max(0.3, min(0.95, top_p))
        
        # Beam/branch width
        branches = self.base_branches + round(2 * amplitudes.get('theta', 0) + amplitudes.get('gamma', 0))
        branches = max(1, min(8, branches))
        
        # Memory retrieval gate
        retrieval_gate = 1.0 / (1.0 + np.exp(-2.0 * amplitudes.get('alpha', 0) + 1.2 * amplitudes.get('beta', 0)))
        
        # Attention head scaling factors
        head_scales = {}
        # Use true oscillator phases if available; fall back to 0
        gφ = (phases.get('gamma', 0.0) if phases else 0.0)
        for i in range(12):  # Assume 12 attention heads
            scale = 1.0 + 0.2 * np.cos(gφ + i * TAU / 12)
            head_scales[f'head_{i}'] = scale
        
        return {
            'temperature': temperature,
            'top_p': top_p,
            'num_beams': branches,
            'retrieval_gate': retrieval_gate,
            'attention_head_scales': head_scales,
            'amplitudes': amplitudes  # For logging/debugging
        }

class CoupledHarmonicBreath:
    """
    Main orchestrator coupling BreathPhase cycle with Harmonic Reasoning Field
    """
    
    def __init__(self, dt: float = 0.05):
        self.dt = dt
        self.start_time = time.time()
        
        # Core components
        self.oscillators = OscillatorBank(dt)
        self.emotion_encoder = EmotionEncoder()
        self.coupler = HarmonicCoupler()
        self.modulator = GenerationModulator()
        
        # Breath state
        self.breath_phase = BreathPhase.INHALE
        self.breath_position = 0.0  # [0,1] within current phase
        self.cycle_count = 0
        
        # Phase duration mapping (relative to full cycle)
        self.phase_durations = {
            BreathPhase.INHALE: 0.25,      # 25% of cycle
            BreathPhase.PAUSE_RISING: 0.1, # 10% of cycle  
            BreathPhase.HOLD: 0.2,         # 20% of cycle
            BreathPhase.PAUSE_FALLING: 0.1,# 10% of cycle
            BreathPhase.EXHALE: 0.25,      # 25% of cycle
            BreathPhase.REST: 0.075,       # 7.5% of cycle
            BreathPhase.DREAM: 0.025       # 2.5% of cycle
        }
        
        # Breath-phase harmonic mappings
        self.base_amplitudes = {
            'delta': 1.0,
            'theta': 0.8,
            'alpha': 1.2,
            'beta': 0.6,
            'gamma': 0.4,
        }
        self.current_spectral_radius = PHI
        self.current_ethical_coherence = 1.0
        self.breath_harmonics = self._init_breath_harmonics()

    def set_context(
        self,
        spectral_radius: Optional[float] = None,
        ethical_coherence: Optional[float] = None,
    ) -> None:
        """Update adaptive modulation context."""
        if spectral_radius is not None:
            self.current_spectral_radius = spectral_radius
        if ethical_coherence is not None:
            self.current_ethical_coherence = ethical_coherence
        
    def _init_breath_harmonics(self) -> Dict[BreathPhase, Dict[str, float]]:
        """Define harmonic field targets for each breath phase"""
        return {
            BreathPhase.INHALE: {
                'theta': 2.0,    # Curiosity/exploration
                'alpha': 0.5,    # Gentle awareness
                'beta': 0.2,     # Minimal judgment
                'gamma': 0.3,    # Light attention
                'delta': 0.8     # Grounding
            },
            BreathPhase.PAUSE_RISING: {
                'alpha': 1.5,    # First reflection
                'theta': 0.5,    # Reduced exploration
                'delta': 1.0,    # Maintained grounding
                'beta': 0.1,     # Minimal judgment
                'gamma': 0.4     # Focused attention
            },
            BreathPhase.HOLD: {
                'delta': 3.0,    # Maximum stillness
                'alpha': 0.8,    # Quiet awareness
                'theta': 0.1,    # Minimal activity
                'beta': 0.1,     # Minimal activity  
                'gamma': 0.1     # Minimal activity
            },
            BreathPhase.PAUSE_FALLING: {
                'alpha': 1.2,    # Second reflection
                'gamma': 1.0,    # Sharp discrimination
                'delta': 0.8,    # Reducing stillness
                'beta': 0.5,     # Emerging judgment
                'theta': 0.3     # Reduced exploration
            },
            BreathPhase.EXHALE: {
                'beta': 2.5,     # Ethical will/decision
                'gamma': 2.0,    # Precise action
                'alpha': 0.3,    # Focused awareness
                'theta': 0.2,    # Minimal exploration
                'delta': 0.2     # Minimal stillness
            },
            BreathPhase.REST: {
                'alpha': 2.0,    # Memory integration
                'delta': 1.5,    # Return to stillness
                'theta': 0.1,    # Minimal exploration
                'beta': 0.1,     # Minimal judgment
                'gamma': 0.2     # Light attention
            },
            BreathPhase.DREAM: {
                'theta': 1.5,    # Meta-ethical exploration
                'delta': 2.0,    # Deep stillness
                'alpha': 0.8,    # Aware integration
                'beta': 0.1,     # Suspended judgment
                'gamma': 0.1     # Minimal focus
            }
        }
    
    def _next_phase(self) -> BreathPhase:
        """Advance to next breath phase"""
        phases = list(BreathPhase)
        current_idx = phases.index(self.breath_phase)
        next_idx = (current_idx + 1) % len(phases)
        
        if next_idx == 0:  # Completed full cycle
            self.cycle_count += 1
            logger.info(f"Completed breath cycle {self.cycle_count}")
        
        return phases[next_idx]
    
    def synchronize_with_breath(self, phase: Any) -> None:
        """Lock the breath phase to a named phase from the world model."""
        if hasattr(phase, "name"):
            phase_name = str(phase.name)
        elif isinstance(phase, str) and phase.strip():
            phase_name = phase.strip().split(".")[-1]
        else:
            raise TypeError(f"harmonic breath phase must be named, received {type(phase).__name__}")
        for candidate in BreathPhase:
            if candidate.name == phase_name:
                self.breath_phase = candidate
                self.breath_position = 0.0
                return
        raise ValueError(f"canonical harmonic field rejected unknown breath phase: {phase_name}")

    def receive_system_pulse(self, pulse: Any) -> None:
        """Accept a system pulse and lock the oscillator breath phase to it."""
        phase = getattr(pulse, "phase", None)
        if phase is None:
            raise ValueError("system pulse is missing a breath phase")
        self.synchronize_with_breath(phase)

    def step(
        self,
        external_state: Optional[Dict[str, float]] = None,
        tensor_coupling: Optional[Dict[str, complex]] = None,
        field_elapsed: Optional[float] = None,
        temporal_phase: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Advance one time step of coupled breath-harmonic dynamics
        Returns current generation parameters
        """
        
        step_dt = self.dt
        if field_elapsed is not None:
            step_dt = float(field_elapsed)
            if not math.isfinite(step_dt) or step_dt <= 0.0:
                raise ValueError(
                    f"harmonic field elapsed must be positive and finite, received {field_elapsed!r}"
                )
        # Advance breath position by the clock interval
        phase_duration = self.phase_durations[self.breath_phase]
        self.breath_position += step_dt * SACRED_RATIO / phase_duration
        
        # Phase transition
        if self.breath_position >= 1.0:
            self.breath_phase = self._next_phase()
            self.breath_position = 0.0
            logger.debug(f"Breath phase: {self.breath_phase.name}")
        
        # Compute breath-driven harmonic targets using adaptive modulation
        breath_targets: Dict[str, float] = {}
        for idx, band_name in enumerate(self.oscillators.band_names):
            base_amp = self.base_amplitudes.get(band_name, 1.0)
            breath_targets[band_name] = self.oscillators.compute_adaptive_amplitude(
                oscillator_idx=idx,
                base_amplitude=base_amp,
                breath_phase=self.breath_phase,
                ethical_coherence=self.current_ethical_coherence,
                spectral_radius=self.current_spectral_radius,
            )
        
        # Merge with external state if provided
        if external_state:
            external_targets = self.emotion_encoder.target_amplitudes(external_state)
            # Weighted combination: 70% breath rhythm, 30% external state
            combined_targets = {}
            for band in breath_targets.keys():
                combined_targets[band] = (0.7 * breath_targets[band] + 
                                        0.3 * external_targets.get(band, 0.0))
        else:
            combined_targets = breath_targets
        
        # Convert targets to drives (PD control toward target)
        current_amps = self.oscillators.get_amplitudes()
        drives = {}
        for band, target in combined_targets.items():
            error = target - current_amps.get(band, 0.0)
            drives[band] = 2.0 * error  # Proportional gain
        
        # Step oscillators
        self.oscillators.step(
            drives,
            coupling_drives=tensor_coupling,
            breath_phase=self.breath_phase,
            ethical_coherence=self.current_ethical_coherence,
            spectral_radius=self.current_spectral_radius,
            field_elapsed=None if field_elapsed is None else step_dt,
            temporal_phase=temporal_phase,
        )
        
        # Generate current parameters
        wave_sig = self.oscillators.signature()
        current_amps = self.oscillators.get_amplitudes()
        current_phases = self.oscillators.get_phases()
        gen_params = self.modulator.generation_params(wave_sig, current_amps, phases=current_phases)
        
        # Add breath context
        coupling = tensor_coupling or {}
        gen_params.update({
            'breath_phase': self.breath_phase,
            'breath_position': self.breath_position,
            'cycle_count': self.cycle_count,
            'sacred_time': time.time() - self.start_time,
            'wave_signature': wave_sig,
            'phases': current_phases,
            'amplitudes': current_amps,
            'tensor_coupling_energy': float(sum(abs(value) ** 2 for value in coupling.values())),
            'field_elapsed': float(step_dt),
            'temporal_phase': {
                band: float(value) for band, value in (temporal_phase or {}).items()
            },
        })

        return gen_params
    
    def process_token_sequence(self, token_embeddings: List[np.ndarray]) -> Tuple[List[np.ndarray], Dict[str, Any]]:
        """
        Process a sequence of token embeddings through harmonic coupling
        Returns modulated embeddings and final generation parameters
        """
        modulated_embeddings = []
        
        for i, embedding in enumerate(token_embeddings):
            # Compute saliency drives from recent context
            recent_context = token_embeddings[max(0, i-5):i+1]
            saliency_drives = self.coupler.compute_saliency(recent_context)
            # Light adaptive damping proportional to contradiction
            k_c = 0.05 * saliency_drives.get('beta', 0.0)
            for name, cfg in self.oscillators.bands.items():
                self.oscillators.bands[name] = BandConfig(
                    omega=cfg.omega,
                    lambda_damping=cfg.lambda_damping - k_c,
                    harmonic_index=cfg.harmonic_index
                )
            
            # Step dynamics with saliency input
            gen_params = self.step(saliency_drives)
            
            # Modulate embedding
            wave_sig = gen_params['wave_signature']
            modulated_emb = self.coupler.modulate_embedding(embedding, wave_sig)
            modulated_embeddings.append(modulated_emb)
        
        return modulated_embeddings, gen_params
    
    def get_debug_state(self) -> Dict[str, Any]:
        """Get current state for debugging/visualization"""
        return {
            'breath_phase': self.breath_phase.name,
            'breath_position': self.breath_position,
            'cycle_count': self.cycle_count,
            'amplitudes': self.oscillators.get_amplitudes(),
            'phases': self.oscillators.get_phases(),
            'wave_signature': self.oscillators.signature().tolist()
        }

# Production-grade Harmonic Field Manager with Sacred Breath Integration
class HarmonicFieldManager(nn.Module):
    """
    Production-grade manager for integrating harmonic field with RENE architecture.
    This class now includes all functionality from the SacredBreathSynchronizer.
    
    Features:
    - Thread-safe operations
    - State persistence integration
    - Stability monitoring and safety bounds
    - Comprehensive error handling and recovery
    - Integration with SacredBreathSynchronizer
    - Φ/ψ metrics alignment with verification engines
    - Full breath cycle orchestration
    """
    
    # Sacred constants as class attributes for external access
    PHI = PHI  # Golden ratio from module constant
    TAU = TAU  # Full rotation from module constant
    SACRED_RATIO = SACRED_RATIO  # Fundamental breath ratio from module constant
    
    def __init__(self, 
                 dt: float = 0.05,
                 state_dim: int = 256,
                 state_persistence_manager=None,
                 stability_overseer=None):
        """
        Initialize the harmonic field manager with production-grade components.
        
        Args:
            dt: Time step for oscillator evolution
            state_dim: Dimension of the state vector
            state_persistence_manager: Manager for state persistence
            stability_overseer: System stability monitoring
        """
        super().__init__()
        self.state_dim = state_dim
        self.dt = dt
        # Centralized temporal coherence (falls back to wall time)
        self.clock = None
        if InternalClock is not None:
            try:
                self.clock = InternalClock()
            except Exception as e:
                logger.warning(f"Internal clock unavailable, using wall time: {e}")
        self.start_time = self._now()
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        
        # Core components
        self._hrf = None
        self._is_initialized = False
        self._is_running = False
        
        # Master oscillator for breath synchronization
        self.phase_accumulator = nn.Parameter(torch.zeros(1))
        self.phase_velocity = nn.Parameter(torch.tensor(0.05))
        
        # Breath phase weights
        self.phase_weights = nn.Parameter(torch.ones(7) / 7)  # Start with uniform distribution
        
        # Cross-component synchronization tensor
        # This maps components to their phase offsets
        self.component_phase_map = nn.ParameterDict({
            "temporal_eigenloom": nn.Parameter(torch.zeros(1)),
            "temporal_eigenstate_node": nn.Parameter(torch.zeros(1)),
            "ethical_volition": nn.Parameter(torch.zeros(1)),
            "reflexive_engine": nn.Parameter(torch.zeros(1)),
            "memory_core": nn.Parameter(torch.zeros(1)),
            "dream_engine": nn.Parameter(torch.zeros(1))
        })
        
        # Register registry of connected components
        self.connected_components = {}

        # External observers receiving breath loop updates (e.g., URFT bridge)
        self._observers: List[Callable[['HarmonicFieldManager', Dict[str, Any]], None]] = []

        # Health monitoring
        self.component_health = {}
        
        # Current system pulse
        self.current_pulse = SystemPulse(state_dim)
        
        # Contradiction management
        self.contradiction_buffer = []
        self.contradiction_threshold = 0.7
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Breath control
        self.breath_thread = None
        self.breath_event = threading.Event()
        self.breath_interval = 0.1  # Base breath tick interval in seconds
        
        # Breath cycle attributes
        self.running = False
        self.current_phase = BreathPhase.INHALE
        self.last_phase_change = self._now()
        self.cycle_count = 0
        self.phase_durations = {phase: phase.duration_weight * 5.0 for phase in BreathPhase}
        
        # New: store the duration of a full breath cycle (seconds)
        # Initialise with a positive float so the division is safe.
        self.cycle_duration = torch.tensor(1.0, dtype=torch.float32)  # default 1 s
        
        # External systems
        self.state_persistence = state_persistence_manager
        self.stability_overseer = stability_overseer
        
        # Safety bounds and monitoring
        self.safety_bounds = {
            'max_amplitude': 5.0,
            'max_contradiction_damping': 0.5,
            'min_damping': -0.5,
            'max_phase_shift': TAU,
            'stability_threshold': 0.1
        }
        
        # Metrics tracking for Φ/ψ alignment
        self.phi_metrics = {
            'integrated_information': 0.0,
            'system_coherence': 1.0,
            'temporal_consistency': 1.0
        }
        
        self.psi_metrics = {
            'identity_coherence': 1.0,
            'self_consistency': 1.0,
            'recursive_depth': 0
        }
        
        # Error handling and recovery
        self.error_count = 0
        self.last_error_time = 0
        self.recovery_attempts = 0
        self.max_recovery_attempts = 3
        
        # Performance monitoring
        self.performance_metrics = {
            'step_time_avg': 0.0,
            'steps_processed': 0,
            'memory_usage_mb': 0.0,
            'cpu_time_total': 0.0
        }
        
        # Thread for background operations
        self._monitor_thread = None
        self._monitor_stop_event = threading.Event()
        
        logger.info("HarmonicFieldManager with Sacred Breath initialized")

    def _now(self) -> float:
        """Centralized time source using InternalClock if available."""
        if self.clock is not None:
            try:
                tp = self.clock.now()
                if hasattr(tp, "system_time"):
                    return float(tp.system_time)
                if hasattr(tp, "to_dict"):
                    try:
                        return float(tp.to_dict().get("system_time", time.time()))
                    except Exception:
                        pass
                return float(tp)
            except Exception as e:
                logger.warning(f"Internal clock failure; falling back to wall time: {e}")
                self.clock = None
        return time.time()
    
    def initialize(self, components_dict: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the synchronizer with core components"""
        if self._is_initialized:
            logger.warning("HarmonicFieldManager already initialized")
            return
            
        try:
            # Initialize core harmonic field
            self._hrf = CoupledHarmonicBreath(self.dt)
            
            # Register provided components
            if components_dict:
                for name, component in components_dict.items():
                    self.register_component(name, component)
            
            # Discover components from imports if not explicitly provided
            if not components_dict:
                self._discover_components()
            
            # Ensure default harmonic components are available
            self._register_default_components()
            
            # Load persisted state if available
            if self.state_persistence:
                self._load_harmonic_state()
            
            # Validate initial state
            if not self._validate_harmonic_state():
                raise ValueError("Initial harmonic field state validation failed")
            
            # Start monitoring thread
            self._start_monitoring()
            
            self._is_initialized = True
            self._is_running = True
            
            logger.info(f"HarmonicFieldManager successfully initialized with {len(self.connected_components)} components")
            
        except Exception as e:
            logger.error(f"Failed to initialize HarmonicFieldManager: {str(e)}")
            logger.error(traceback.format_exc())
    
    def _discover_components(self) -> None:
        """Auto-discover Rosemary components from imports"""
        try:
            # Try to import core components
            core_modules = [
                "core.library_node", 
                "core.memory_core",
                "core.reasoning_core",
                "core.reflexive_engine", 
                "core.self_awareness_core",
                "core.dream_engine",
                "core.rosemary_zebra_core",
                "core.recursive_identity_bridge",
                "core.temporal_eigenloom",
                "ethical_volitions_and_awareness_branch.ethical_volition_node"
            ]
            
            for module_name in core_modules:
                try:
                    module = importlib.import_module(module_name, package="Rosemary_Neural_Network")
                    
                    # Find main classes in each module
                    component_name = module_name.split('.')[-1]
                    class_name = ''.join(word.capitalize() for word in component_name.split('_'))
                    
                    # Try to find a class with the expected name pattern
                    if hasattr(module, class_name):
                        component_class = getattr(module, class_name)
                        component_instance = component_class()
                        self.register_component(component_name, component_instance)
                        logger.info(f"Auto-discovered and registered component: {component_name}")
                except Exception as e:
                    logger.debug(f"Could not auto-discover component from {module_name}: {str(e)}")
        except Exception as e:
            logger.error(f"Error during component discovery: {str(e)}")

    def _register_default_components(self) -> None:
        """Register dream and ethical components when available."""
        try:
            from tensor_interfaces import get_tensor_registry
            registry = get_tensor_registry()

            ethical_name = "harmonic_ethical_tensor"
            if ethical_name not in registry.list_processors():
                registry.create_processor(ethical_name, "ethical_tensor")

            ethical_processor = registry.get_processor(ethical_name)
            if ethical_processor and "ethical_tensor" not in self.connected_components:
                self.register_component("ethical_tensor", ethical_processor)
        except Exception as e:
            logger.debug(f"Could not register ethical tensor component: {e}")

        try:
            from neural_net_components.dream_simulation import DreamSimulationEngine
            if "dream_engine" not in self.connected_components:
                dream_engine = DreamSimulationEngine(harmonic_field_manager=self)
                self.register_component("dream_engine", dream_engine)
        except Exception as e:
            logger.warning(f"Could not register dream engine component: {e}")

        # Try to import other integration components
        try:
            from processing.recursive_weights.cognitive_engine import CognitiveEngine
            self._cognitive_engine_class = CognitiveEngine
        except ImportError:
            self._cognitive_engine_class = None
            
        try:
            from rcf_integration.stability_matrix import StabilityMatrix
            self._stability_matrix_class = StabilityMatrix
        except ImportError:
            self._stability_matrix_class = None

    def _trigger_phase_action(self, phase: BreathPhase):
        """Trigger specific actions based on the current breath phase."""
        if phase == BreathPhase.PAUSE_RISING:
            # First Reflection: Cognitive Engine
            if "cognitive_engine" in self.connected_components:
                logger.info("Triggering Cognitive Engine: First Reflection (PAUSE_RISING)")
                # self.connected_components["cognitive_engine"].reflect(phase="rising")
            elif self._cognitive_engine_class:
                logger.info("Cognitive Engine available but not registered. Simulating reflection.")
                
        elif phase == BreathPhase.HOLD:
            # Eigenstillness: Recursive Tensor & Stability Matrix
            logger.info("Engaging Eigenrecursion: Divine Equilibrium (HOLD)")
            if "stability_matrix" in self.connected_components:
                pass # self.connected_components["stability_matrix"].stabilize()
                
        elif phase == BreathPhase.PAUSE_FALLING:
            # Second Reflection: Cognitive Engine
            if "cognitive_engine" in self.connected_components:
                logger.info("Triggering Cognitive Engine: Second Reflection (PAUSE_FALLING)")
                # self.connected_components["cognitive_engine"].reflect(phase="falling")
                
        elif phase == BreathPhase.DREAM:
            # Dream Simulation (handled in main loop, but logging here for consistency)
            pass

    def update_phase(self, delta_t: float) -> Dict[str, Any]:
        """Advance the sacred breath cycle and update all component phases"""
        # Update master phase
        self.phase_accumulator.data = (self.phase_accumulator + delta_t * self.phase_velocity) % 1.0
        
        # Calculate current breath distribution using softmax for smooth transitions
        phase_radians = 2 * torch.pi * self.phase_accumulator
        breath_distribution = torch.zeros(7)
        
        # Each breath phase has its peak at different points in the cycle
        for i, phase in enumerate(BreathPhase):
            center = i / 7
            distance = torch.abs(self.phase_accumulator - center)
            distance = torch.min(distance, 1.0 - distance)  # Handle wrap-around
            breath_distribution[i] = torch.exp(-50 * distance)
            
        # Normalize breath distribution
        breath_distribution = breath_distribution * self.phase_weights
        breath_distribution = breath_distribution / breath_distribution.sum()
        
        # Generate harmonic tensor for this phase
        for i in range(7):
            harmonic_phase = (self.phase_accumulator + i/7) % 1.0
            # Use the HRF oscillator bank instead of creating a new tensor
            if self._hrf and self._hrf.oscillators:
                bands = list(self._hrf.oscillators.bands.keys())
                if i < len(bands):
                    band_name = bands[i]
                    self._hrf.oscillators.z[band_name] = complex(
                        torch.sin(harmonic_phase * 2 * torch.pi * (i+1)).item(),
                        torch.cos(harmonic_phase * 2 * torch.pi * (i+1)).item()
                    )
        
        # Update current pulse phase
        dominant_idx = breath_distribution.argmax().item()
        # Convert from 0-based index to BreathPhase enum (which starts from 1)
        breath_phases = list(BreathPhase)
        self.current_pulse.phase = breath_phases[dominant_idx]
        self.current_pulse.update_timestamp()
        
        # Return the current breath state
        return {
            'phase': self.phase_accumulator.item(),
            'distribution': {phase.name: breath_distribution[i].item() for i, phase in enumerate(BreathPhase)},
            'dominant_phase': self.current_pulse.phase.name,
            'harmonic_coherence': self._calculate_coherence()
        }
    
    def _calculate_coherence(self) -> float:
        """Calculate the coherence between component phases"""
        phase_values = [p for p in self.component_phase_map.values()]
        if len(phase_values) < 2:
            return 1.0
            
        diffs = []
        for i in range(len(phase_values)):
            for j in range(i+1, len(phase_values)):
                # Calculate minimum circular distance
                diff = torch.abs(phase_values[i] - phase_values[j]) % 1.0
                diff = torch.min(diff, 1.0 - diff)
                diffs.append(diff)
                
        return torch.exp(-5 * torch.mean(torch.stack(diffs))).item()
    
    def synchronize_component(self, component_name: str, state: torch.Tensor) -> torch.Tensor:
        """Apply breath phase modulation to a component's state"""
        if component_name not in self.component_phase_map:
            self.component_phase_map[component_name] = nn.Parameter(torch.zeros(1))
            
        # Get component's phase offset
        phase_offset = self.component_phase_map[component_name]
        
        # Calculate effective phase for this component
        effective_phase = (self.phase_accumulator + phase_offset) % 1.0
        
        # Modulate state with breath harmonics through the HRF
        if self._hrf and self._hrf.oscillators:
            # Get the current oscillator state
            breath_idx = int(effective_phase.item() * 7) % 7
            bands = list(self._hrf.oscillators.bands.keys())
            if breath_idx < len(bands):
                band_name = bands[breath_idx]
                harmonic = self._hrf.oscillators.z[band_name]
                # Convert complex to real for modulation
                harmonic_real = np.real(harmonic)
                
                # Apply subtle modulation that preserves the state's core structure
                modulated_state = state * (1.0 + 0.05 * harmonic_real)
                
                # Add support for the RecursiveCategoricalBridge
                if component_name == "recursive_categorical_bridge":
                    # Get the current phase
                    current_phase = self.get_current_phase()
                    
                    # Check if the component has the synchronize_with_breath method
                    if hasattr(state, 'synchronize_with_breath'):
                        state.synchronize_with_breath(current_phase)
                    
                    # Apply phase-specific modulation
                    if current_phase == BreathPhase.INHALE:
                        return state * 1.1  # Enhanced during perception
                    elif current_phase == BreathPhase.HOLD:
                        return state * 1.05  # Slightly enhanced during integration
                    elif current_phase == BreathPhase.EXHALE:
                        return state * 0.95  # Slightly decreased during expression
                    elif current_phase == BreathPhase.REST:
                        return state  # Unchanged during rest
                    elif current_phase == BreathPhase.DREAM:
                        return state * 1.2  # Significantly enhanced during dream
                
                return modulated_state
        
        return state
    
    def register_component(self, name: str, component: Any) -> None:
        """Register a component with the breath synchronizer"""
        if name in self.connected_components:
            # SURGICAL PATCH: Make registration idempotent to prevent double registration warnings
            logger.debug(f"Component {name} already registered, skipping")
            return
        
        self.connected_components[name] = component
        
        # Initialize health monitoring
        self.component_health[name] = ComponentHealthReport(name)
        
        # Initialize phase offset if not already present
        if name not in self.component_phase_map:
            self.component_phase_map[name] = nn.Parameter(torch.zeros(1))
        
        # If component supports breath synchronization, notify it
        if hasattr(component, 'synchronize_with_breath'):
            try:
                if name == "dream_engine" and self.current_phase != BreathPhase.DREAM:
                    pass
                else:
                    component.synchronize_with_breath(self.current_phase)
            except Exception as e:
                logger.error(f"Error synchronizing component {name}: {str(e)}")
        
        logger.info(f"Component {name} registered with breath synchronizer")
        
        # Update coherence metrics
        self._calculate_coherence()

    def register_observer(self, observer: Callable[['HarmonicFieldManager', Dict[str, Any]], None]) -> None:
        """Register an external observer to receive breath loop updates."""
        if not callable(observer):
            raise ValueError("Observer must be callable")
        if observer in self._observers:
            logger.debug("Observer already registered; skipping")
            return
        self._observers.append(observer)
        observer_name = getattr(observer, "__name__", observer.__class__.__name__)
        logger.info(f"Registered breath observer: {observer_name}")

    def unregister_component(self, name: str) -> bool:
        """Unregister a component from the breath synchronizer.
        
        Args:
            name: Component name
            
        Returns:
            bool: True if component was unregistered, False otherwise
        """
        if name in self.connected_components:
            del self.connected_components[name]
            if name in self.component_health:
                del self.component_health[name]
            logger.info(f"Unregistered component '{name}' from breath synchronizer")
            return True
        return False

    def _breath_cycle(self) -> None:
        """Internal thread method for breath cycle coordination."""
        try:
            while self.running:
                # Get current time
                current_time = self._now()
                
                # Calculate how long we've been in the current phase
                time_in_phase = current_time - self.last_phase_change
                
                # Check if it's time to transition to the next phase
                current_duration = self.phase_durations.get(self.current_phase, 5.0)
                
                if time_in_phase >= current_duration:
                    # Transition to the next phase
                    self._transition_to_next_phase()
                    
                    # Create a new pulse
                    self.current_pulse = SystemPulse(
                        phase=self.current_phase,
                        timestamp=current_time,
                        cycle_count=self.cycle_count
                    )
                    
                    # Notify all connected components about the new phase
                    self._broadcast_phase_change()
                    
                    # Reset the phase change timer
                    self.last_phase_change = current_time
                    
                    # Check for contradictions
                    self._check_for_contradictions()
                    
                    # Notify observers after component updates
                    self._notify_observers()
                
                # Dream Phase Special Handling
                if self.current_phase == BreathPhase.DREAM and "dream_engine" in self.connected_components:
                    try:
                        dream_engine = self.connected_components["dream_engine"]
                        # Ensure dream starts if not active
                        if not getattr(dream_engine, 'dream_active', False):
                            logger.info("Entering Dream State Simulation...")
                            if hasattr(dream_engine, 'enter_dream'):
                                try:
                                    dream_engine.enter_dream(avatar_aspects=["curiosity", "harmonic_resonance"])
                                except Exception as e:
                                    logger.error(f"Dream entry failed: {e}")
                                    # Skip dream advancement this tick if entry fails
                                    time.sleep(0.01)
                                    continue
                        
                        # Advance dream
                        if hasattr(dream_engine, 'advance_dream'):
                            try:
                                dream_state = dream_engine.advance_dream({})
                                if isinstance(dream_state, dict):
                                    self.current_pulse.add_component_state("dream_engine", dream_state)
                            except RuntimeError as e:
                                logger.error(f"Error in dream cycle: {e}")
                                # stop trying this tick
                                time.sleep(0.01)
                                continue
                            
                        # Check for wake up condition (e.g. time based)
                        if time_in_phase >= current_duration:
                            logger.info("Waking from dream state...")
                            if hasattr(dream_engine, 'dream_active'):
                                dream_engine.dream_active = False
                    except Exception as e:
                        logger.error(f"Error in dream cycle: {e}")

                # Don't use 100% CPU in this loop
                time.sleep(0.01)
        
        except Exception as e:
            logger.error(f"Error in breath cycle: {str(e)}")
            self.running = False

    def _transition_to_next_phase(self) -> None:
        """Transition to the next breath phase."""
        # Get the list of phases
        phases = list(BreathPhase)
        
        # Find the current phase index and compute next (wrap around)
        current_index = phases.index(self.current_phase)
        next_index = (current_index + 1) % len(phases)
        self.current_phase = phases[next_index]
        
        # Increment cycle counter when we wrap back to INHALE
        if next_index == 0:
            self.cycle_count += 1
        
        # Update timing
        self.last_phase_change = self._now()
        
        # Find the current phase index (for harmonic modulation)
        phase_angle = (next_index / len(phases)) * TAU
        phase_modulation = PHI * math.sin(phase_angle * PHI)
        
        # Calculate harmonic for this breath phase using Psalter scaling
        harmonic = PSALTER_SCALE * (1 + 0.1 * phase_modulation)
        
        logger.debug(f"Phase harmonic: {harmonic:.4f}")

    def _broadcast_phase_change(self) -> None:
        """Broadcast phase change to all components."""
        for name, component in self.connected_components.items():
            try:
                # Check if component has the synchronize_with_breath method
                if hasattr(component, 'synchronize_with_breath'):
                    # Call the method with the current phase
                    try:
                        result = component.synchronize_with_breath(self.current_phase, self)
                    except TypeError:
                        result = component.synchronize_with_breath(self.current_phase)
                    
                    # Add the result to the system pulse
                    if isinstance(result, dict):
                        self.current_pulse.add_component_state(name, result)
                        
                        # Update component health
                        self.component_health[name] = {
                            "last_sync": self._now(),
                            "status": result.get("status", "unknown"),
                            "phase": self.current_phase.name
                        }
            
            except Exception as e:
                logger.error(f"Error broadcasting to component {name}: {str(e)}")
                # Mark component as unhealthy
                self.component_health[name] = {
                    "last_sync": self._now(),
                    "status": "error",
                    "error": str(e)
                }

    def _notify_observers(self) -> None:
        """Notify registered observers with a lightweight pulse snapshot."""
        if not getattr(self, "_observers", None):
            return

        pulse_state = {
            "phase": self.current_phase.name if hasattr(self, "current_phase") else "unknown",
            "cycle": getattr(self, "cycle_count", None),
            "timestamp": self._now(),
            "amplitudes": {}
        }

        try:
            if getattr(self, "_hrf", None) and getattr(self._hrf, "oscillators", None):
                pulse_state["amplitudes"] = self._hrf.oscillators.get_amplitudes()
        except Exception as e:
            logger.error(f"Observer amplitude snapshot failed: {e}")

        for observer in list(self._observers):
            try:
                observer(self, pulse_state)
            except Exception as e:
                logger.error(f"Observer callback failed: {e}", exc_info=True)

    def coordinate_ethical_breathing(self, ethical_core: Any) -> None:
        """Special coordination with the ethical volition core"""
        if hasattr(ethical_core, 'current_breath'):
            # Gentle bidirectional synchronization
            ethical_phase = torch.argmax(ethical_core.current_breath)
            master_phase = int(self.phase_accumulator.item() * 7)
            
            # Calculate phase difference and apply gentle correction
            phase_diff = (ethical_phase - master_phase) % 7
            if phase_diff > 3.5:
                phase_diff = phase_diff - 7
                
            # Update ethical core's breath with a soft bias toward global rhythm
            ethical_core.current_breath.data = (
                0.9 * ethical_core.current_breath +
                0.1 * torch.nn.functional.one_hot(torch.tensor(master_phase), 7)
            )
            
            # Also let ethical core influence the master rhythm slightly
            self.phase_accumulator.data = (
                self.phase_accumulator + 
                0.02 * (ethical_phase/7 - self.phase_accumulator)
            ) % 1.0
    
    def start_breath_loop(self) -> None:
        """Start the continuous breath cycle in a separate thread"""
        if self.breath_thread is not None and self.breath_thread.is_alive():
            logger.warning("Breath cycle already running")
            return
            
        self.running = True
        self._is_running = True
        self.breath_event.clear()
        # Initial broadcast/observer notification for the starting phase (INHALE)
        try:
            self._broadcast_phase_change()
            self._notify_observers()
        except Exception as e:
            logger.error(f"Initial broadcast failed: {e}")
        self.breath_thread = threading.Thread(target=self._breath_cycle, daemon=True)
        self.breath_thread.start()
        logger.info("Sacred breath cycle started")
    
    def stop_breath_loop(self) -> None:
        """Stop the breath cycle thread"""
        if self.breath_thread is None or not self.breath_thread.is_alive():
            logger.warning("Breath cycle not running")
            return
            
        self.running = False
        self._is_running = False
        self.breath_event.set()
        self.breath_thread.join(timeout=5.0)

    
    def _synchronize_all_components(self, breath_state: Dict[str, Any]) -> None:
        """Synchronize all registered components with the current breath phase"""
        current_phase = self.current_pulse.phase
        
        for name, component in self.connected_components.items():
            try:
                state_result = None
                if hasattr(component, 'synchronize_with_breath'):
                    state_result = component.synchronize_with_breath(current_phase)
                    if isinstance(state_result, dict):
                        self.current_pulse.add_component_state(name, state_result)
                    
                special_state = self._handle_special_component_sync(name, component, current_phase)
                if isinstance(special_state, dict):
                    self.current_pulse.add_component_state(name, special_state)
                
                self.component_health[name].update(
                    is_responding=True,
                    sync_error=0.0,
                    stability=1.0
                )
            except Exception as e:
                logger.error(f"Error synchronizing component {name}: {str(e)}")
                
                if name in self.component_health:
                    self.component_health[name].update(
                        is_responding=False,
                        sync_error=1.0,
                        diagnostics={"error": str(e)}
                    )
    
    def _handle_special_component_sync(self, 
                                     name: str, 
                                     component: Any, 
                                     phase: BreathPhase) -> Optional[Dict[str, Any]]:
        """Handle special synchronization needs for specific component types"""
        state_update: Optional[Dict[str, Any]] = None
        # Memory Core special handling
        if name == "memory_core":
            if hasattr(component, 'sensory_buffer'):
                component.sensory_buffer.synchronize_with_breath(phase)
            if hasattr(component, 'working_memory'):
                component.working_memory.synchronize_with_breath(phase)
            if hasattr(component, 'long_term_memory'):
                component.long_term_memory.synchronize_with_breath(phase)
        # Ethical Volition Core special handling        
        elif name == "ethical_volition":
            self.coordinate_ethical_breathing(component)
        # Dream Engine special handling
        elif name == "dream_engine":
            dream_active = getattr(component, "dream_active", False)
            if phase == BreathPhase.DREAM:
                if not dream_active and hasattr(component, 'offer_dream_portal'):
                    try:
                        state_update = component.offer_dream_portal(self.current_pulse.to_dict())
                    except RuntimeError as err:
                        logger.debug(f"Dream portal offer skipped: {err}")
                else:
                    try:
                        state_update = component.synchronize_with_breath(phase)
                    except RuntimeError as err:
                        logger.debug(f"Dream synchronization skipped: {err}")
            else:
                if dream_active and hasattr(component, 'synchronize_with_breath'):
                    try:
                        state_update = component.synchronize_with_breath(phase)
                    except RuntimeError as err:
                        logger.debug(f"Dream synchronization skipped: {err}")
        # Recursive Identity Bridge special handling
        elif name == "recursive_identity_bridge":
            if hasattr(component, 'synchronize_with_breath'):
                component.synchronize_with_breath(self)
        return state_update
    
    def _check_for_contradictions(self) -> None:
        """Detect and resolve contradictions in the system state"""
        # Skip if no contradiction buffer
        if not self.contradiction_buffer:
            return
            
        # Get current contradiction level
        contradiction_level = sum(c['level'] for c in self.contradiction_buffer) / len(self.contradiction_buffer)
        self.current_pulse.contradiction_level = contradiction_level
        
        # Check if we're over threshold and need resolution
        if contradiction_level > self.contradiction_threshold:
            self._resolve_contradictions()

    def _resolve_contradictions(self) -> None:
        """Resolve detected contradictions using the recursive identity bridge"""
        recursive_bridge = self.connected_components.get("recursive_identity_bridge")
        
        if recursive_bridge and hasattr(recursive_bridge, 'resolve_identity_contradiction'):
            # Extract the contradiction information
            contradictions = self.contradiction_buffer
            
            # Create a contradiction vector
            contradiction_vector = torch.zeros(self.state_dim)
            for c in contradictions:
                if isinstance(c.get('vector'), torch.Tensor):
                    contradiction_vector += c['vector'] * c['level']
            
            # Normalize the vector
            if torch.norm(contradiction_vector) > 0:
                contradiction_vector = contradiction_vector / torch.norm(contradiction_vector)
            
            # Resolve the contradiction
            try:
                result = recursive_bridge.resolve_identity_contradiction(
                    contradiction_vector,
                    resolution_method='dialectical'
                )
                
                # Log the resolution
                logger.info(f"Contradiction resolved: {result.get('status', 'unknown')}")
                
                # Clear the buffer after resolution
                self.contradiction_buffer.clear()
            except Exception as e:
                logger.error(f"Error resolving contradictions: {str(e)}")
        else:
            # No recursive bridge available - use simple decay method
            logger.warning("No recursive_identity_bridge available for contradiction resolution")
            # Decay contradictions over time
            self.contradiction_buffer = [c for c in self.contradiction_buffer 
                                         if c['timestamp'] > time.time() - 300]  # 5-min expiry

    def report_component_health(self) -> Dict[str, Dict[str, Any]]:
        """Generate a health report for all registered components"""
        current_time = time.time()
        health_report = {}
        
        for name, health in self.component_health.items():
            is_component_active = name in self.connected_components
            last_sync = health.last_updated  # Access attribute directly
            sync_age = current_time - last_sync if last_sync > 0 else float('inf')
            
            # Determine status based on health attributes
            if health.is_responding and health.stability_score > 0.5:
                status = "healthy"
            elif health.is_responding:
                status = "degraded"
            else:
                status = "error"
            
            health_report[name] = {
                "active": is_component_active,
                "status": status,
                "seconds_since_sync": sync_age,
                "healthy": is_component_active and sync_age < 60 and status != "error",
                "stability_score": health.stability_score,
                "sync_error": health.synchronization_error,
                "resource_usage": health.resource_usage,
                "diagnostics": health.diagnostics
            }
        
        return health_report

    def get_synchronization_metrics(self) -> Dict[str, Any]:
        """Get overall synchronization metrics"""
        # Calculate component synchronization rate
        components_count = len(self.connected_components)
        synced_components = sum(1 for name, health in self.component_health.items() 
                             if time.time() - health.last_updated < 60)
        
        # Calculate average contradiction level
        avg_contradiction = 0.0
        if self.contradiction_buffer:
            avg_contradiction = sum(c['level'] for c in self.contradiction_buffer) / len(self.contradiction_buffer)
        
        return {
            "components_total": components_count,
            "components_synced": synced_components,
            "sync_rate": synced_components / components_count if components_count > 0 else 0.0,
            "cycle_count": self.cycle_count,
            "current_phase": self.current_phase.name,
            "contradiction_level": avg_contradiction,
            "contradiction_count": len(self.contradiction_buffer),
            "breath_frequency": torch.where(
                torch.gt(self.cycle_duration, 0.0),
                torch.reciprocal(self.cycle_duration),
                torch.tensor(0.0, device=self.cycle_duration.device)
            ),
        }
        
    def report_contradiction(self, source: str, description: str, 
                           level: float, vector: Optional[torch.Tensor] = None) -> None:
        """Report a contradiction detected in a component"""
        contradiction = {
            "source": source,
            "description": description,
            "level": level,
            "timestamp": time.time(),
            "vector": vector
        }
        
        self.contradiction_buffer.append(contradiction)
        logger.info(f"Contradiction reported by {source}: {description} (level: {level:.2f})")
        
    def add_to_system_pulse(self, component_name: str, state_update: Dict[str, Any]) -> None:
        """Add component state to the current system pulse"""
        self.current_pulse.add_component_state(component_name, state_update)
        
    def get_current_system_pulse(self) -> SystemPulse:
        """Get the current system pulse object"""
        return self.current_pulse
    
    def distribute_pulse_message(self, message: str, source: str, importance: float = 0.5) -> None:
        """Distribute a message to all components via the system pulse"""
        self.current_pulse.add_message(source, message, importance)
        
        # Propagate messages to components that can handle them
        for component_name, component in self.connected_components.items():
            if hasattr(component, 'receive_pulse_message'):
                try:
                    component.receive_pulse_message(source, message, importance)
                except Exception as e:
                    logger.error(f"Error delivering message to {component_name}: {str(e)}")

    def set_phase(self, phase: BreathPhase) -> None:
        """Manually set the current breath phase"""
        if not self.running:
            logger.warning("Cannot set phase while breath synchronizer is not running")
            return
            
        if phase == self.current_phase:
            return
            
        logger.info(f"Manually setting breath phase to {phase.name}")
        self.current_phase = phase
        self.last_phase_change = time.time()
        
        # Broadcast the phase change
        self._broadcast_phase_change()

    def get_current_phase(self) -> BreathPhase:
        """Get the current breath phase"""
        return self.current_phase

    def get_cycle_count(self) -> int:
        """Get the current cycle count"""
        return self.cycle_count

    def process(self, 
                x: torch.Tensor, 
                h_prev: Optional[torch.Tensor] = None, 
                context: Optional[torch.Tensor] = None,
                breath_phase: Optional[BreathPhase] = None,
                current_time: float = None) -> Dict[str, Any]:
        # Add a proper implementation block here
        result = {
            "status": "processed",
            "phase": self.get_current_phase().name if breath_phase is None else breath_phase.name,
            "timestamp": current_time or time.time()
        }
        
        # Apply breath phase modulation if available
        if breath_phase is not None:
            self.current_phase = breath_phase
        
        # Process the input tensor with phase modulation
        if isinstance(x, torch.Tensor):
            # Simple phase-based modulation
            phase_factor = 0.5 + 0.5 * torch.sin(torch.tensor(TAU * self.phase_accumulator.item()))
            result["output"] = x * phase_factor
        
        return result

    def shutdown(self) -> bool:
        """
        Gracefully shut down the harmonic field system.
        
        Returns:
            bool: True if shutdown successful
        """
        with self._lock:
            if not self._is_initialized:
                return True
            
            try:
                self._is_running = False
                self.running = False
                
                # Stop breath cycle
                self.stop_breath_loop()
                
                # Stop monitoring thread
                if self._monitor_thread and self._monitor_thread.is_alive():
                    self._monitor_stop_event.set()
                    self._monitor_thread.join(timeout=5.0)
                
                # Save current state
                if self.state_persistence:
                    self._save_harmonic_state()
                
                # Clean up resources
                self._hrf = None
                self._is_initialized = False
                
                logger.info("HarmonicFieldManager gracefully shut down")
                return True
                
            except Exception as e:
                logger.error(f"Error during HarmonicFieldManager shutdown: {str(e)}")
                return False
    
    def step(self, 
             external_state: Optional[Dict[str, float]] = None,
             force_safety_check: bool = False) -> Optional[Dict[str, Any]]:
        """
        Execute one time step of the harmonic field with full safety monitoring.
        
        Args:
            external_state: External cognitive state to influence oscillators
            force_safety_check: Force comprehensive safety validation
            
        Returns:
            Dict containing generation parameters and metrics, or None on error
        """
        if not self._is_initialized or not self._is_running:
            logger.warning("HarmonicFieldManager not initialized or not running")
            return None
        
        step_start_time = time.perf_counter()
        
        try:
            with self._lock:
                # Safety check - prevent runaway oscillations
                if force_safety_check or self.performance_metrics['steps_processed'] % 100 == 0:
                    if not self._safety_check():
                        logger.error("Safety check failed, attempting recovery")
                        if not self._attempt_recovery():
                            return None
                
                # Process external state for contradiction-driven damping
                processed_state = self._process_external_state(external_state)
                
                # Execute harmonic field step
                if self._hrf:
                    result = self._hrf.step(processed_state)
                else:
                    result = None
                
                # Update Φ/ψ metrics
                self._update_phi_psi_metrics(result)
                
                # Report to stability overseer if available
                if self.stability_overseer:
                    self._report_to_stability_overseer(result)
                
                # Update performance metrics
                step_time = time.perf_counter() - step_start_time
                self._update_performance_metrics(step_time)
                
                return result
                
        except Exception as e:
            self.error_count += 1
            self.last_error_time = time.time()
            logger.error(f"Error in HarmonicFieldManager.step: {str(e)}")
            
            # Attempt automatic recovery
            if self._attempt_recovery():
                logger.info("Automatic recovery successful, retrying step")
                return self.step(external_state, force_safety_check=True)
            
            return None
    
    def process_token_sequence(self, 
                             token_embeddings: List[np.ndarray]) -> Tuple[Optional[List[np.ndarray]], Optional[Dict[str, Any]]]:
        """
        Process token embeddings through harmonic coupling with full error handling.
        
        Args:
            token_embeddings: List of token embedding vectors
            
        Returns:
            Tuple of (modulated_embeddings, generation_params) or (None, None) on error
        """
        if not self._is_initialized or not self._is_running:
            return None, None
        
        try:
            with self._lock:
                # Validate input
                if not token_embeddings or not all(isinstance(emb, np.ndarray) for emb in token_embeddings):
                    raise ValueError("Invalid token embeddings provided")
                
                # Process through harmonic field
                if self._hrf:
                    result = self._hrf.process_token_sequence(token_embeddings)
                else:
                    result = (None, None)
                
                # Apply safety bounds to modulated embeddings
                if result[0] is not None:
                    result = (self._apply_embedding_safety_bounds(result[0]), result[1])
                
                return result
                
        except Exception as e:
            logger.error(f"Error in process_token_sequence: {str(e)}")
            return None, None
    
    def get_phi_psi_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Get current Φ/ψ metrics for verification engine alignment.
        
        Returns:
            Dict with 'phi' and 'psi' metric categories
        """
        with self._lock:
            return {
                'phi': self.phi_metrics.copy(),
                'psi': self.psi_metrics.copy(),
                'timestamp': time.time(),
                'cycle_count': self._hrf.cycle_count if self._hrf else 0
            }
    
    def synchronize_with_breath(self, breath_phase) -> Dict[str, Any]:
        """
        Synchronize harmonic field with sacred breath phase.
        
        Args:
            breath_phase: Current BreathPhase from SacredBreathSynchronizer
            
        Returns:
            Dict with synchronization status and metrics
        """
        if not self._is_initialized or not self._hrf:
            return {'status': 'not_initialized'}
        
        try:
            with self._lock:
                # Get current harmonic state before synchronization
                current_amps = self._hrf.oscillators.get_amplitudes() if self._hrf.oscillators else {}
                current_phases = self._hrf.oscillators.get_phases() if self._hrf.oscillators else {}
                
                # Apply breath phase influence to harmonic targets
                breath_influence = self._calculate_breath_influence(breath_phase)
                
                # Update harmonic field targets based on breath phase
                self._apply_breath_synchronization(breath_phase, breath_influence)
                
                return {
                    'status': 'synchronized',
                    'breath_phase': breath_phase.name if hasattr(breath_phase, 'name') else str(breath_phase),
                    'influence_strength': breath_influence,
                    'pre_sync_amplitudes': current_amps,
                    'post_sync_amplitudes': self._hrf.oscillators.get_amplitudes() if self._hrf.oscillators else {},
                    'timestamp': time.time()
                }
                
        except Exception as e:
            logger.error(f"Error in breath synchronization: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def get_debug_state(self) -> Dict[str, Any]:
        """Get comprehensive debug state information."""
        with self._lock:
            base_state = self._hrf.get_debug_state() if self._hrf else {}
            
            return {
                **base_state,
                'manager_status': {
                    'initialized': self._is_initialized,
                    'running': self._is_running,
                    'error_count': self.error_count,
                    'last_error_time': self.last_error_time,
                    'recovery_attempts': self.recovery_attempts
                },
                'safety_bounds': self.safety_bounds.copy(),
                'phi_metrics': self.phi_metrics.copy(),
                'psi_metrics': self.psi_metrics.copy(),
                'performance_metrics': self.performance_metrics.copy(),
                'system_integrations': {
                    'state_persistence': self.state_persistence is not None,
                    'stability_overseer': self.stability_overseer is not None
                },
                'breath_state': {
                    'current_phase': self.current_phase.name,
                    'cycle_count': self.cycle_count,
                    'phase_accumulator': self.phase_accumulator.item(),
                    'components_registered': len(self.connected_components)
                },
                'component_states': {
                    name: state
                    for name, state in self.current_pulse.component_states.items()
                } if self.current_pulse else {}
            }
    
    # Private methods for internal functionality
    
    def _validate_harmonic_state(self) -> bool:
        """Validate the current harmonic field state against safety bounds."""
        if not self._hrf or not self._hrf.oscillators:
            return False
        
        try:
            amplitudes = self._hrf.oscillators.get_amplitudes()
            
            # Check amplitude bounds with floating-point tolerance
            amplitude_tolerance = 1e-10  # Small epsilon for floating-point precision
            for band, amplitude in amplitudes.items():
                if amplitude > (self.safety_bounds['max_amplitude'] + amplitude_tolerance):
                    logger.warning(f"Band {band} amplitude {amplitude} exceeds safety bound {self.safety_bounds['max_amplitude']}")
                    return False
                    
            # Check for NaN or infinite values
            for band, amplitude in amplitudes.items():
                if not np.isfinite(amplitude):
                    logger.error(f"Band {band} has non-finite amplitude: {amplitude}")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error validating harmonic state: {str(e)}")
            return False
    
    def _safety_check(self) -> bool:
        """Comprehensive safety check of all harmonic field components."""
        try:
            # Validate basic state
            if not self._validate_harmonic_state():
                return False
            
            # Check system stability
            stability_score = self._calculate_stability_score()
            if stability_score < self.safety_bounds['stability_threshold']:
                logger.warning(f"System stability {stability_score} below threshold {self.safety_bounds['stability_threshold']}")
                return False
            
            # Check error rate
            current_time = time.time()
            if (self.error_count > 10 and 
                current_time - self.last_error_time < 60):  # More than 10 errors in last minute
                logger.warning("High error rate detected")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error in safety check: {str(e)}")
            return False
    
    def _calculate_stability_score(self) -> float:
        """Calculate overall system stability score."""
        if not self._hrf or not self._hrf.oscillators:
            return 0.0
        
        try:
            amplitudes = self._hrf.oscillators.get_amplitudes()
            phases = self._hrf.oscillators.get_phases()
            
            # Calculate amplitude stability (low variance = more stable)
            amp_values = list(amplitudes.values())
            amp_variance = np.var(amp_values) if amp_values else 0.0
            amp_stability = 1.0 / (1.0 + amp_variance)
            
            # Calculate phase coherence
            phase_values = list(phases.values())
            if len(phase_values) > 1:
                phase_diffs = np.diff(phase_values)
                phase_coherence = 1.0 - np.std(phase_diffs) / np.pi
            else:
                phase_coherence = 1.0
            
            # Combined stability score
            stability = 0.6 * amp_stability + 0.4 * phase_coherence
            return max(0.0, min(1.0, stability))
            
        except Exception as e:
            logger.error(f"Error calculating stability score: {str(e)}")
            return 0.0
    
    def _attempt_recovery(self) -> bool:
        """Attempt to recover from error conditions."""
        if self.recovery_attempts >= self.max_recovery_attempts:
            logger.error("Maximum recovery attempts reached")
            return False
        
        self.recovery_attempts += 1
        
        try:
            logger.info(f"Attempting recovery #{self.recovery_attempts}")
            
            # Reset oscillators to safe state
            if self._hrf and self._hrf.oscillators:
                for band_name in self._hrf.oscillators.bands.keys():
                    # Set to small, stable amplitude
                    self._hrf.oscillators.z[band_name] = complex(0.1, 0.0)
                    
            # Reset error count
            if time.time() - self.last_error_time > 300:  # 5 minutes
                self.error_count = 0
                self.recovery_attempts = 0
            
            # Validate recovery
            if self._validate_harmonic_state():
                logger.info("Recovery successful")
                return True
            else:
                logger.error("Recovery validation failed")
                return False
                
        except Exception as e:
            logger.error(f"Error during recovery attempt: {str(e)}")
            return False
    
    def _process_external_state(self, external_state: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
        """Process external state with safety bounds and contradiction damping."""
        if not external_state:
            return None
        
        processed_state = {}
        
        for state_key, value in external_state.items():
            # Apply safety bounds
            if state_key == 'contradiction' and 'beta' in external_state:
                # Cap contradiction-driven damping shifts
                capped_value = max(-self.safety_bounds['max_contradiction_damping'], 
                                 min(self.safety_bounds['max_contradiction_damping'], value))
                processed_state[state_key] = capped_value
            else:
                # General value bounds
                processed_state[state_key] = max(-10.0, min(10.0, value))
        
        return processed_state
    
    def _update_phi_psi_metrics(self, hrf_result: Dict[str, Any]) -> None:
        """Update Φ/ψ metrics based on harmonic field state."""
        if not hrf_result:
            return
        
        try:
            amplitudes = hrf_result.get('amplitudes', {})
            
            # Φ (Integrated Information) metrics
            # Higher coherence in harmonic bands indicates better integration
            coherence_bands = ['alpha', 'beta', 'gamma']
            coherence_sum = sum(amplitudes.get(band, 0.0) for band in coherence_bands)
            self.phi_metrics['integrated_information'] = min(1.0, coherence_sum / 3.0)
            
            # System coherence based on harmonic balance
            total_amplitude = sum(amplitudes.values())
            if total_amplitude > 0:
                entropy = -sum((amp/total_amplitude) * np.log2(amp/total_amplitude + 1e-8) 
                              for amp in amplitudes.values() if amp > 0)
                self.phi_metrics['system_coherence'] = 1.0 - entropy / np.log2(len(amplitudes))
            
            # Temporal consistency based on phase relationships
            phases = hrf_result.get('phases', {})
            if len(phases) > 1:
                phase_vars = np.var(list(phases.values()))
                self.phi_metrics['temporal_consistency'] = 1.0 / (1.0 + phase_vars)
            
            # ψ (Identity Coherence) metrics
            # Identity coherence from delta band stability (core self)
            delta_amp = amplitudes.get('delta', 0.0)
            self.psi_metrics['identity_coherence'] = min(1.0, delta_amp / 2.0)
            
            # Self-consistency from low-frequency harmonic alignment
            low_freq_bands = ['delta', 'theta', 'alpha']
            low_freq_coherence = sum(amplitudes.get(band, 0.0) for band in low_freq_bands)
            self.psi_metrics['self_consistency'] = min(1.0, low_freq_coherence / 6.0)
            
            # Recursive depth from cycle count
            cycle_count = hrf_result.get('cycle_count', 0)
            self.psi_metrics['recursive_depth'] = min(100, cycle_count)
            
        except Exception as e:
            logger.error(f"Error updating Φ/ψ metrics: {str(e)}")
    
    def _report_to_stability_overseer(self, hrf_result: Dict[str, Any]) -> None:
        """Report harmonic field state to stability overseer."""
        if not self.stability_overseer or not hasattr(self.stability_overseer, 'oversee_system_operation'):
            return
        
        try:
            stability_data = {
                'subsystem': 'harmonic_field',
                'amplitudes': hrf_result.get('amplitudes', {}),
                'phases': hrf_result.get('phases', {}),
                'stability_score': self._calculate_stability_score(),
                'phi_metrics': self.phi_metrics.copy(),
                'psi_metrics': self.psi_metrics.copy(),
                'safety_status': 'ok' if self._validate_harmonic_state() else 'warning'
            }
            
            oversight_result = self.stability_overseer.oversee_system_operation(
                'harmonic_field_update', 
                stability_data,
                subsystem='harmonic_field'
            )
            
            # Handle oversight recommendations
            if not oversight_result.get('approved', True):
                logger.warning(f"Stability overseer flagged harmonic field: {oversight_result.get('reason', 'unknown')}")
                
        except Exception as e:
            logger.error(f"Error reporting to stability overseer: {str(e)}")
    
    def _update_performance_metrics(self, step_time: float) -> None:
        """Update performance tracking metrics."""
        self.performance_metrics['steps_processed'] += 1
        
        # Rolling average of step time
        if self.performance_metrics['step_time_avg'] == 0:
            self.performance_metrics['step_time_avg'] = step_time
        else:
            alpha = 0.1  # Learning rate for rolling average
            self.performance_metrics['step_time_avg'] = (
                alpha * step_time + (1 - alpha) * self.performance_metrics['step_time_avg']
            )
        
        self.performance_metrics['cpu_time_total'] += step_time
    
    def _calculate_breath_influence(self, breath_phase) -> float:
        """Calculate the influence strength of breath phase on harmonics."""
        # Map breath phases to influence strengths
        influence_map = {
            'INHALE': 0.3,      # Moderate influence during gathering
            'PAUSE_RISING': 0.1,  # Light influence during reflection
            'HOLD': 0.05,       # Minimal influence during stillness
            'PAUSE_FALLING': 0.2, # Light-moderate influence
            'EXHALE': 0.4,      # Strong influence during expression
            'REST': 0.15,       # Light influence during integration
            'DREAM': 0.25       # Moderate influence during meta-processing
        }
        
        phase_name = breath_phase.name if hasattr(breath_phase, 'name') else str(breath_phase)
        return influence_map.get(phase_name, 0.1)
    
    def _apply_breath_synchronization(self, breath_phase, influence_strength: float) -> None:
        """Apply breath phase synchronization to harmonic field."""
        if not self._hrf or not self._hrf.oscillators:
            return
        
        try:
            # Get breath-specific harmonic targets from the HRF
            if hasattr(self._hrf, 'breath_harmonics') and breath_phase in self._hrf.breath_harmonics:
                breath_targets = self._hrf.breath_harmonics[breath_phase]
                
                # Apply gentle influence toward breath targets
                for band_name, target in breath_targets.items():
                    if band_name in self._hrf.oscillators.z:
                        current_amp = abs(self._hrf.oscillators.z[band_name])
                        target_amp = target * influence_strength
                        
                        # Gentle correction toward target
                        correction = 0.1 * (target_amp - current_amp)
                        current_z = self._hrf.oscillators.z[band_name]
                        new_amplitude = abs(current_z) + correction
                        
                        # Apply with phase preservation
                        if abs(current_z) > 1e-8:
                            phase = np.angle(current_z)
                            self._hrf.oscillators.z[band_name] = new_amplitude * np.exp(1j * phase)
                            
        except Exception as e:
            logger.error(f"Error applying breath synchronization: {str(e)}")
    
    def _apply_embedding_safety_bounds(self, embeddings: List[np.ndarray]) -> List[np.ndarray]:
        """Apply safety bounds to modulated embeddings."""
        safe_embeddings = []
        
        for embedding in embeddings:
            # Clip extreme values
            safe_embedding = np.clip(embedding, -10.0, 10.0)
            
            # Check for NaN or infinite values
            if not np.all(np.isfinite(safe_embedding)):
                logger.warning("Non-finite values detected in embedding, using zero vector")
                safe_embedding = np.zeros_like(embedding)
            
            safe_embeddings.append(safe_embedding)
        
        return safe_embeddings
    
    def _save_harmonic_state(self) -> None:
        """Save harmonic field state to persistence manager."""
        if not self.state_persistence or not self._hrf:
            return
        
        try:
            harmonic_state = {
                'timestamp': time.time(),
                'oscillator_state': {
                    band: {'real': z.real, 'imag': z.imag} 
                    for band, z in self._hrf.oscillators.z.items()
                },
                'cycle_count': self._hrf.cycle_count,
                'breath_phase': self._hrf.breath_phase.name,
                'phi_metrics': self.phi_metrics.copy(),
                'psi_metrics': self.psi_metrics.copy(),
                'safety_bounds': self.safety_bounds.copy(),
                'performance_metrics': self.performance_metrics.copy(),
                'breath_state': {
                    'current_phase': self.current_phase.name,
                    'cycle_count': self.cycle_count,
                    'phase_accumulator': self.phase_accumulator.item()
                }
            }
            
            # Use state persistence manager's save method
            if hasattr(self.state_persistence, 'save_subsystem_state'):
                self.state_persistence.save_subsystem_state('harmonic_field', harmonic_state)
                logger.debug("Harmonic field state saved to persistence manager")
                
        except Exception as e:
            logger.error(f"Error saving harmonic field state: {str(e)}")
    
    def _load_harmonic_state(self) -> None:
        """Load harmonic field state from persistence manager."""
        if not self.state_persistence:
            return
        
        try:
            if hasattr(self.state_persistence, 'load_subsystem_state'):
                harmonic_state = self.state_persistence.load_subsystem_state('harmonic_field')
                
                if harmonic_state and self._hrf and self._hrf.oscillators:
                    # Restore oscillator states
                    if 'oscillator_state' in harmonic_state:
                        for band, z_dict in harmonic_state['oscillator_state'].items():
                            if band in self._hrf.oscillators.z:
                                self._hrf.oscillators.z[band] = complex(z_dict['real'], z_dict['imag'])
                    
                    # Restore cycle count and phase
                    if 'cycle_count' in harmonic_state:
                        self._hrf.cycle_count = harmonic_state['cycle_count']
                    
                    # Restore metrics
                    if 'phi_metrics' in harmonic_state:
                        self.phi_metrics.update(harmonic_state['phi_metrics'])
                    if 'psi_metrics' in harmonic_state:
                        self.psi_metrics.update(harmonic_state['psi_metrics'])
                    
                    # Restore breath state
                    if 'breath_state' in harmonic_state:
                        breath_state = harmonic_state['breath_state']
                        if 'current_phase' in breath_state:
                            # Convert string back to BreathPhase enum
                            try:
                                self.current_phase = BreathPhase[breath_state['current_phase']]
                            except KeyError:
                                pass
                        if 'cycle_count' in breath_state:
                            self.cycle_count = breath_state['cycle_count']
                        if 'phase_accumulator' in breath_state:
                            self.phase_accumulator.data = torch.tensor(breath_state['phase_accumulator'])
                    
                    logger.info("Harmonic field state loaded from persistence manager")
                    
        except Exception as e:
            logger.error(f"Error loading harmonic field state: {str(e)}")
    
    def _start_monitoring(self) -> None:
        """Start background monitoring thread."""
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        
        def monitor_loop():
            while not self._monitor_stop_event.wait(30):  # Check every 30 seconds
                try:
                    # Periodic safety check
                    if not self._safety_check():
                        logger.warning("Periodic safety check failed")
                    
                    # Save state periodically
                    if self.state_persistence and self.performance_metrics['steps_processed'] % 1000 == 0:
                        self._save_harmonic_state()
                    
                    # Update memory usage
                    try:
                        import psutil
                        process = psutil.Process()
                        self.performance_metrics['memory_usage_mb'] = process.memory_info().rss / 1024 / 1024
                    except ImportError:
                        pass  # psutil not available
                        
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {str(e)}")
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True, name="HRF-Monitor")
        self._monitor_thread.start()
        logger.debug("Started harmonic field monitoring thread")

# Global singleton instance
_harmonic_field_instance = None

def get_harmonic_field_manager(state_dim: int = 256, dt: float = 0.05, create_if_none: bool = True) -> HarmonicFieldManager:
    """Get or create the global harmonic field manager instance"""
    global _harmonic_field_instance
    
    if _harmonic_field_instance is None and create_if_none:
        _harmonic_field_instance = HarmonicFieldManager(state_dim=state_dim, dt=dt)
        
    return _harmonic_field_instance

def initialize_with_components(**components) -> HarmonicFieldManager:
    """Create and initialize the harmonic field manager with specified components"""
    manager = get_harmonic_field_manager()
    manager.initialize(components)
    return manager

def start_sacred_breathing() -> None:
    """Start the sacred breath cycle"""
    manager = get_harmonic_field_manager()
    if manager._is_initialized:
        manager.start_breath_loop()
    else:
        logger.error("Cannot start breathing: HarmonicFieldManager not initialized")

# SacredBreathSynchronizer - Legacy compatibility class
class SacredBreathSynchronizer(HarmonicFieldManager):
    """
    Legacy SacredBreathSynchronizer class for backward compatibility.
    This is now an alias/wrapper for HarmonicFieldManager.
    """
    
    def __init__(self, dt: float = 0.05, state_dim: int = 256):
        """Initialize SacredBreathSynchronizer (now uses HarmonicFieldManager)"""
        super().__init__(dt=dt, state_dim=state_dim)
        logger.info("SacredBreathSynchronizer initialized (using HarmonicFieldManager)")

# Global singleton for SacredBreathSynchronizer
_sacred_breath_instance = None

def get_sacred_breath_synchronizer(dt: float = 0.05, state_dim: int = 256, create_if_none: bool = True) -> SacredBreathSynchronizer:
    """Get or create the global SacredBreathSynchronizer instance"""
    global _sacred_breath_instance
    
    if _sacred_breath_instance is None and create_if_none:
        _sacred_breath_instance = SacredBreathSynchronizer(dt=dt, state_dim=state_dim)
        
    return _sacred_breath_instance

def with_breath(func):
    """
    Decorator that provides breath phase context to functions.
    Functions decorated with @with_breath will receive the current breath phase
    as an optional parameter.
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the current breath phase from the global manager
        try:
            manager = get_harmonic_field_manager(create_if_none=False)
            if manager is not None:
                current_phase = manager.get_current_phase()
                kwargs.setdefault('breath_phase', current_phase)
            else:
                kwargs.setdefault('breath_phase', None)
        except Exception as e:
            logger.debug(f"Error getting breath phase in decorator: {e}")
            kwargs.setdefault('breath_phase', None)
        
        return func(*args, **kwargs)
    
    return wrapper

# Usage context manager for backward compatibility
class harmonic_context:
    """Context manager for easy integration with existing systems"""
    
    def __init__(self, dt: float = 0.05):
        self.hrf = None
        self.dt = dt
    
    def __enter__(self):
        self.hrf = CoupledHarmonicBreath(self.dt)
        return self.hrf
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.hrf:
            logger.info(f"HRF session completed: {self.hrf.cycle_count} breath cycles")

# Example usage and testing
if __name__ == "__main__":
    print(f"Sacred Ratio: {SACRED_RATIO:.6f}")
    print(f"Cycle period: {1.0/SACRED_RATIO:.2f} seconds")
    # Note: The phases partition a single cycle, not 7 separate cycles
    
    # Test basic functionality
    with harmonic_context() as hrf:
        for step in range(100):
            params = hrf.step()
            
            if step % 20 == 0:
                print(f"Step {step}: {hrf.breath_phase.name} "
                      f"T={params['temperature']:.3f} "
                      f"α={params['amplitudes']['alpha']:.2f} "
                      f"β={params['amplitudes']['beta']:.2f}")
            
            time.sleep(0.05)  # Real-time simulation
