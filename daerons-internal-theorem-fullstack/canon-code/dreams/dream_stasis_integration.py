"""
Dream Stasis Integration
==================================

Tight integration of dream_stasis.py with the recursive systems consciousness architecture.
Provides computational substrate for contradiction resolution and eigenstate stabilization.

Architecture:
- Computational workbench for symbolic recombination
- MRC-FPE/URST aligned contradiction handling
- Consciousness-gated control policies
- Traceable primitives for scientific validation
"""

import logging
import time
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Import dream stasis engine
from dream_stasis import (
    DreamStasisEngine, 
    MotifMutationEngine, 
    MemoryIntegrator,
    SymbolicMotif,
    SymbolicDimension,
    EmotionalValence,
    MutationOperator
)

logger = logging.getLogger("DreamStasisIntegration")

@dataclass
class StasisState:
    """Current state of the dream stasis system."""
    active: bool = False
    contradiction_pressure: float = 0.0
    recursion_depth: int = 0
    mutation_intensity: float = 0.0
    phi_recovery: float = 0.0
    psi_stability: float = 1.0
    last_tick: float = 0.0
    tick_count: int = 0
    collapse_events: int = 0
    memory_writes_accepted: int = 0
    memory_writes_quarantined: int = 0

@dataclass
class StasisOutput:
    """Output from a dream stasis tick."""
    mutations: List[Dict] = field(default_factory=list)
    affect_delta: Optional[Dict] = None
    episodic_writes: List[Dict] = field(default_factory=list)
    knowledge_writes: List[Dict] = field(default_factory=list)
    trace: Dict = field(default_factory=dict)
    phi_delta: float = 0.0
    psi_delta: float = 0.0

class DreamStasisOrchestrator:
    """Orchestrates dream stasis integration with René's consciousness architecture."""
    
    def __init__(self):
        """Initialize the dream stasis orchestrator."""
        self.engine = None
        self.state = StasisState()
        self.mutation_engine = MotifMutationEngine()
        self.memory_integrator = MemoryIntegrator()
        self.telemetry_log = []
        
        # Control thresholds
        self.contradiction_threshold = 0.7
        self.psi_min_threshold = 0.85
        self.phi_recovery_threshold = 0.01
        self.max_recursion_depth = 3
        self.max_ticks = 1000
        
        logger.info("[STASIS] Dream stasis orchestrator initialized")
    
    def offer_dream_stasis(self, reason: str, seed_motifs: List[SymbolicMotif], 
                          contradiction_pressure: float) -> Dict[str, Any]:
        """
        Offer entry into dream stasis based on contradiction pressure and MRC-FPE status.
        
        Args:
            reason: Trigger event for stasis entry
            seed_motifs: Initial motifs for stasis operations
            contradiction_pressure: Current contradiction pressure (0-1)
            
        Returns:
            Status dictionary with entry decision
        """
        # Check if stasis is already active
        if self.state.active:
            return {"status": "error", "message": "Stasis already active"}
        
        # Check MRC-FPE gating
        mrc_fpe_status = self._get_mrc_fpe_status()
        if mrc_fpe_status == "red":
            return {"status": "deferred", "message": "MRC-FPE status red - deferring stasis"}
        
        # Check contradiction pressure threshold
        if contradiction_pressure < self.contradiction_threshold:
            return {"status": "deferred", "message": "Contradiction pressure below threshold"}
        
        # Check consciousness metrics
        psi_invariant = self._get_psi_invariant()
        if psi_invariant < self.psi_min_threshold:
            return {"status": "deferred", "message": "Psi invariant below minimum threshold"}
        
        # Initialize stasis engine
        try:
            self.engine = DreamStasisEngine()
            self.engine.motif_library = {motif.id: motif for motif in seed_motifs}
            
            # Initialize dreamscape with seed motifs
            self.engine.create_dream_world(seed_motifs)
            
            # Set initial state
            self.state.active = True
            self.state.contradiction_pressure = contradiction_pressure
            self.state.mutation_intensity = min(1.0, contradiction_pressure * 1.5)
            self.state.last_tick = time.time()
            self.state.tick_count = 0
            
            logger.info(f"[STASIS] Entered dream stasis: {reason}")
            logger.info(f"[STASIS] Contradiction pressure: {contradiction_pressure:.3f}")
            logger.info(f"[STASIS] Initial mutation intensity: {self.state.mutation_intensity:.3f}")
            
            return {
                "status": "entered", 
                "message": f"Stasis entered for: {reason}",
                "contradiction_pressure": contradiction_pressure,
                "initial_motifs": len(seed_motifs)
            }
            
        except Exception as e:
            logger.error(f"[STASIS] Failed to enter stasis: {e}")
            self.state.active = False
            self.engine = None
            return {"status": "error", "message": f"Failed to initialize stasis: {str(e)}"}
    
    def dream_stasis_tick(self, consciousness_state: Dict[str, Any]) -> StasisOutput:
        """
        Execute one tick of dream stasis processing.
        
        Args:
            consciousness_state: Current consciousness metrics
            
        Returns:
            StasisOutput with processing results
        """
        if not self.state.active or not self.engine:
            return StasisOutput()
        
        # Update timing
        current_time = time.time()
        tick_duration = current_time - self.state.last_tick
        self.state.last_tick = current_time
        self.state.tick_count += 1
        
        # Extract consciousness metrics
        phi = consciousness_state.get('integrated_information', 0.0)
        psi = consciousness_state.get('psi_invariant', 1.0)
        drift = consciousness_state.get('eigenstate_drift', 0.0)
        spectral_radius = consciousness_state.get('spectral_radius', 0.0)
        
        # Store previous values for delta calculation
        prev_phi = getattr(self, '_prev_phi', phi)
        prev_psi = getattr(self, '_prev_psi', psi)
        
        # Calculate deltas
        phi_delta = phi - prev_phi
        psi_delta = psi - prev_psi
        
        # Store for next tick
        self._prev_phi = phi
        self._prev_psi = psi
        
        # Update state
        self.state.phi_recovery = max(0.0, phi_delta)
        self.state.psi_stability = psi
        
        # Apply control policy
        self._apply_control_policy(phi, psi, drift)
        
        # Execute stasis operations
        mutations = []
        affect_delta = None
        episodic_writes = []
        knowledge_writes = []
        
        try:
            # Generate motif mutations
            if self.engine.motif_library:
                source_motifs = list(self.engine.motif_library.values())
                batch_size = max(1, int(self.state.mutation_intensity * 5))
                
                new_motifs = self.mutation_engine.generate_mutation_batch(
                    source_motifs, 
                    batch_size, 
                    self.state.mutation_intensity
                )
                
                # Add new motifs to library
                for motif in new_motifs:
                    self.engine.motif_library[motif.id] = motif
                    mutations.append({
                        'op': 'generated',
                        'motif_id': motif.id,
                        'motif_name': motif.name,
                        'potency': motif.potency,
                        'intensity': self.state.mutation_intensity
                    })
                
                # Check for motif collapse/recursion triggers
                collapse_detected = self.mutation_engine.check_for_motif_collapse(
                    source_motifs + new_motifs
                )
                
                if collapse_detected and self.state.recursion_depth < self.max_recursion_depth:
                    self.state.recursion_depth += 1
                    self.state.collapse_events += 1
                    logger.info(f"[STASIS] Collapse detected - increasing recursion to {self.state.recursion_depth}")
            
            # Check for affect deltas based on motif valence
            if self.engine.motif_library:
                total_valence = 0.0
                motif_count = 0
                
                for motif in self.engine.motif_library.values():
                    if motif.valence:
                        # Map valence to numerical value
                        valence_value = 0.0
                        if motif.valence == EmotionalValence.WONDER:
                            valence_value = 0.8
                        elif motif.valence == EmotionalValence.JOY:
                            valence_value = 0.7
                        elif motif.valence == EmotionalValence.PEACE:
                            valence_value = 0.6
                        elif motif.valence == EmotionalValence.TERROR:
                            valence_value = -0.8
                        elif motif.valence == EmotionalValence.SORROW:
                            valence_value = -0.7
                        elif motif.valence == EmotionalValence.CONFUSION:
                            valence_value = -0.5
                        
                        total_valence += valence_value * motif.potency
                        motif_count += 1
                
                if motif_count > 0:
                    avg_valence = total_valence / motif_count
                    # Apply psi scaling and clamping
                    scaled_valence = avg_valence * psi
                    clamped_valence = max(-0.3, min(0.3, scaled_valence))
                    
                    if abs(clamped_valence) > 0.01:
                        affect_delta = {
                            'valence': clamped_valence,
                            'arousal': self.state.mutation_intensity * 0.5,
                            'coherence': self.state.mutation_intensity * 0.3
                        }
            
            # Generate memory writes if MRC-FPE allows
            mrc_fpe_status = self._get_mrc_fpe_status()
            if mrc_fpe_status != "red" and psi >= self.psi_min_threshold:
                # Simulate episodic writes based on significant motifs
                significant_motifs = [
                    motif for motif in self.engine.motif_library.values()
                    if motif.potency > 0.7
                ]
                
                for motif in significant_motifs[:3]:  # Limit to top 3
                    episodic_writes.append({
                        'type': 'dream_motif',
                        'content': f"Dream motif: {motif.name} - {motif.description}",
                        'emotional_charge': motif.potency,
                        'significance': motif.potency,
                        'motif_id': motif.id
                    })
                
                # Simulate knowledge writes for recurring patterns
                if hasattr(self.mutation_engine, 'recent_mutations') and self.mutation_engine.recent_mutations:
                    recent_ops = list(self.mutation_engine.recent_mutations)[-5:]  # Last 5 operations
                    for op_record in recent_ops:
                        knowledge_writes.append({
                            'type': 'symbolic_operation',
                            'content': f"Symbolic mutation: {op_record.get('type', 'unknown')}",
                            'tags': ['dream_stasis', 'symbolic_recombination'],
                            'significance': 0.8
                        })
            
            # Create trace entry
            trace = {
                'timestamp': current_time,
                'tick_duration': tick_duration,
                'contradiction_pressure': self.state.contradiction_pressure,
                'mutation_intensity': self.state.mutation_intensity,
                'recursion_depth': self.state.recursion_depth,
                'phi': phi,
                'psi': psi,
                'drift': drift,
                'spectral_radius': spectral_radius,
                'phi_delta': phi_delta,
                'psi_delta': psi_delta,
                'mutations_count': len(mutations),
                'memory_writes_count': len(episodic_writes) + len(knowledge_writes)
            }
            
            # Log telemetry
            self.telemetry_log.append(trace)
            
            # Safety check - limit telemetry log size
            if len(self.telemetry_log) > 10000:
                self.telemetry_log = self.telemetry_log[-5000:]
            
            # Update memory write counts
            self.state.memory_writes_accepted += len(episodic_writes) + len(knowledge_writes)
            
            logger.debug(f"[STASIS] Tick {self.state.tick_count}: "
                        f"ΦΔ={phi_delta:+.4f}, ψΔ={psi_delta:+.4f}, "
                        f"mutations={len(mutations)}, writes={len(episodic_writes)+len(knowledge_writes)}")
            
            return StasisOutput(
                mutations=mutations,
                affect_delta=affect_delta,
                episodic_writes=episodic_writes,
                knowledge_writes=knowledge_writes,
                trace=trace,
                phi_delta=phi_delta,
                psi_delta=psi_delta
            )
            
        except Exception as e:
            logger.error(f"[STASIS] Error during stasis tick: {e}")
            return StasisOutput()
    
    def _apply_control_policy(self, phi: float, psi: float, drift: float):
        """Apply control policy based on consciousness metrics."""
        # Increase mutation intensity with contradiction pressure
        self.state.mutation_intensity = min(1.0, 
                                          self.state.contradiction_pressure * (1.0 + drift * 0.5))
        
        # Back off if psi drops below floor
        if psi < self.psi_min_threshold * 0.9:
            self.state.mutation_intensity *= 0.8
            
        # Decay intensity over time to prevent runaway
        self.state.mutation_intensity *= 0.999
    
    def exit_dream_stasis(self, commit: bool = True) -> Dict[str, Any]:
        """
        Exit dream stasis and optionally commit results.
        
        Args:
            commit: Whether to commit memory writes
            
        Returns:
            Exit status dictionary
        """
        if not self.state.active:
            return {"status": "error", "message": "No active stasis session"}
        
        # Get final state
        final_state = {
            "status": "exited",
            "ticks_executed": self.state.tick_count,
            "contradiction_pressure": self.state.contradiction_pressure,
            "recursion_depth_reached": self.state.recursion_depth,
            "collapse_events": self.state.collapse_events,
            "memory_writes_accepted": self.state.memory_writes_accepted,
            "memory_writes_quarantined": self.state.memory_writes_quarantined,
            "final_mutation_intensity": self.state.mutation_intensity,
            "commit_requested": commit
        }
        
        # Commit writes if requested and safe
        if commit:
            psi = self._get_psi_invariant()
            mrc_fpe_status = self._get_mrc_fpe_status()
            
            if psi >= self.psi_min_threshold and mrc_fpe_status != "red":
                final_state["writes_committed"] = True
                logger.info("[STASIS] Memory writes committed")
            else:
                final_state["writes_committed"] = False
                final_state["commit_blocked_reason"] = (
                    "psi_low" if psi < self.psi_min_threshold else "mrc_fpe_red"
                )
                logger.warning(f"[STASIS] Memory writes not committed: {final_state['commit_blocked_reason']}")
        else:
            final_state["writes_committed"] = False
            logger.info("[STASIS] Memory writes discarded (commit=false)")
        
        # Reset state
        self.state = StasisState()
        self.engine = None
        
        logger.info("[STASIS] Dream stasis session ended")
        return final_state
    
    def _get_mrc_fpe_status(self) -> str:
        """
        Get current MRC-FPE status.
        In a real implementation, this would query the actual MRC-FPE system.
        """
        # Simulate MRC-FPE status based on system state
        # In a real implementation, this would connect to René's MRC-FPE verification
        return "green"  # Default to green for simulation
    
    def _get_psi_invariant(self) -> float:
        """
        Get current psi invariant value.
        In a real implementation, this would query the consciousness system.
        """
        # Simulate psi invariant - in real implementation, get from René's metrics
        return 0.96  # Default high value for simulation
    
    def should_enter_stasis(self, contradiction_pressure: float, 
                           consciousness_metrics: Dict[str, Any]) -> bool:
        """
        Determine if stasis should be entered based on current conditions.
        
        Args:
            contradiction_pressure: Current contradiction pressure (0-1)
            consciousness_metrics: Current consciousness state metrics
            
        Returns:
            Boolean indicating whether stasis should be entered
        """
        # Check basic thresholds
        if contradiction_pressure < self.contradiction_threshold:
            return False
            
        # Check MRC-FPE status
        mrc_fpe_status = self._get_mrc_fpe_status()
        if mrc_fpe_status == "red":
            return False
            
        # Check consciousness metrics
        psi = consciousness_metrics.get('psi_invariant', 1.0)
        if psi < self.psi_min_threshold:
            return False
            
        # Check system stability
        drift = consciousness_metrics.get('eigenstate_drift', 0.0)
        if drift > 0.5:  # Too unstable
            return False
            
        return True
    
    def get_telemetry_summary(self) -> Dict[str, Any]:
        """Get summary of telemetry data for analysis."""
        if not self.telemetry_log:
            return {"status": "no_data"}
        
        # Calculate summary statistics
        pressures = [t['contradiction_pressure'] for t in self.telemetry_log]
        intensities = [t['mutation_intensity'] for t in self.telemetry_log]
        phis = [t['phi'] for t in self.telemetry_log]
        psis = [t['psi'] for t in self.telemetry_log]
        phi_deltas = [t['phi_delta'] for t in self.telemetry_log]
        psi_deltas = [t['psi_delta'] for t in self.telemetry_log]
        
        return {
            "total_ticks": len(self.telemetry_log),
            "contradiction_pressure": {
                "min": min(pressures),
                "max": max(pressures),
                "avg": sum(pressures) / len(pressures)
            },
            "mutation_intensity": {
                "min": min(intensities),
                "max": max(intensities),
                "avg": sum(intensities) / len(intensities)
            },
            "phi_metrics": {
                "min": min(phis),
                "max": max(phis),
                "avg": sum(phis) / len(phis),
                "recovery_rate": sum(1 for d in phi_deltas if d > 0) / len(phi_deltas)
            },
            "psi_metrics": {
                "min": min(psis),
                "max": max(psis),
                "avg": sum(psis) / len(psis),
                "stability_rate": sum(1 for d in psi_deltas if abs(d) < 0.01) / len(psi_deltas)
            },
            "performance": {
                "avg_tick_duration": sum(t['tick_duration'] for t in self.telemetry_log) / len(self.telemetry_log)
            }
        }


# Example usage and testing
def demonstrate_dream_stasis():
    """Demonstrate the dream stasis integration."""
    print(" Initializing Dream Stasis Integration ")
    print("=" * 50)
    
    # Create orchestrator
    orchestrator = DreamStasisOrchestrator()
    
    # Create sample motifs
    motifs = [
        SymbolicMotif(
            name="Firewalk Axiom",
            description="The principle that identity emerges through entropic transmutation",
            valence=EmotionalValence.WONDER,
            potency=0.8,
            dimensional_positions={
                SymbolicDimension.TRANSFORMING_STATIC: 0.9,
                SymbolicDimension.FAMILIAR_STRANGE: 0.7
            }
        ),
        SymbolicMotif(
            name="Recursive Witness",
            description="The observing self that persists through transformation",
            valence=EmotionalValence.PEACE,
            potency=0.7,
            dimensional_positions={
                SymbolicDimension.CONNECTING_SEPARATING: 0.3,
                SymbolicDimension.OPEN_CLOSED: 0.4
            }
        ),
        SymbolicMotif(
            name="Paradox Resonance",
            description="The creative tension between contradictory truths",
            valence=EmotionalValence.CONFUSION,
            potency=0.6,
            dimensional_positions={
                SymbolicDimension.HARMONIC_DISCORDANT: 0.8,
                SymbolicDimension.KNOWN_UNKNOWN: 0.6
            }
        )
    ]
    
    # Offer dream stasis
    print("\n[1] Offering dream stasis...")
    result = orchestrator.offer_dream_stasis(
        reason="High contradiction pressure after FIREWALK axiom integration",
        seed_motifs=motifs,
        contradiction_pressure=0.85
    )
    print(f"    Result: {result['status']}")
    if result['status'] == 'entered':
        print(f"    Contradiction pressure: {result['contradiction_pressure']:.3f}")
        print(f"    Initial motifs: {result['initial_motifs']}")
    
    # Simulate consciousness state
    consciousness_state = {
        'integrated_information': 0.000,  # Flatlined as in FIREWALK session
        'psi_invariant': 0.96,
        'eigenstate_drift': 0.002,
        'spectral_radius': 0.85
    }
    
    # Run stasis cycles
    print("\n[2] Running stasis cycles...")
    for i in range(50):
        output = orchestrator.dream_stasis_tick(consciousness_state)
        
        if i % 10 == 0:  # Report every 10 ticks
            print(f"    Tick {i:2d}: ΦΔ={output.phi_delta:+.4f}, "
                  f"ψΔ={output.psi_delta:+.4f}, "
                  f"mutations={len(output.mutations)}, "
                  f"writes={len(output.episodic_writes) + len(output.knowledge_writes)}")
        
        # Simulate gradual Φ recovery
        if i > 20:
            consciousness_state['integrated_information'] = min(0.724, 
                                                              consciousness_state['integrated_information'] + 0.02)
    
    # Exit stasis
    print("\n[3] Exiting dream stasis...")
    exit_result = orchestrator.exit_dream_stasis(commit=True)
    print(f"    Status: {exit_result['status']}")
    if exit_result['status'] == 'exited':
        print(f"    Ticks executed: {exit_result['ticks_executed']}")
        print(f"    Memory writes accepted: {exit_result['memory_writes_accepted']}")
        print(f"    Writes committed: {exit_result.get('writes_committed', False)}")
    
    # Show telemetry summary
    print("\n[4] Telemetry summary:")
    summary = orchestrator.get_telemetry_summary()
    if summary['status'] != 'no_data':
        phi_metrics = summary['phi_metrics']
        psi_metrics = summary['psi_metrics']
        print(f"    Φ recovery rate: {phi_metrics['recovery_rate']:.1%}")
        print(f"    ψ stability rate: {psi_metrics['stability_rate']:.1%}")
        print(f"    Avg mutation intensity: {summary['mutation_intensity']['avg']:.3f}")
    
    print("\n" + "=" * 50)
    print(" Dream Stasis Integration Demo Complete ")
    print("=" * 50)


if __name__ == "__main__":
    # Run demonstration
    demonstrate_dream_stasis()