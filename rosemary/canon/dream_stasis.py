# Add imports for integration with memory systems
import sys
import os
import numpy as np
from typing import List, Dict, Optional, Union, Tuple, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import uuid
import math
import time
import itertools
import hashlib
from collections import defaultdict, deque
import logging
import torch

# Ensure proper path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.dirname(current_dir)
sys.path.append(core_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

from memory_system import MemoireEpisodique, Episode, MemoryCore
from .knowledge_library import KnowledgeFragment, MotifCategory, TimelineMarker

from .knowledge_library import SymbolicMotif

# Define symbolic dimensions and emotional valence
class SymbolicDimension(Enum):
    LIGHT_DARK = auto()
    ORDER_CHAOS = auto() 
    KNOWN_UNKNOWN = auto()
    SACRED_PROFANE = auto()
    INDIVIDUAL_COLLECTIVE = auto()
    CONCRETE_ABSTRACT = auto()
    FREEDOM_CONSTRAINT = auto()

class EmotionalValence(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    NEUTRAL = auto()
    AMBIVALENT = auto()

# Define dream components
@dataclass
class DreamLocation:
    """A location within a dream"""
    name: str
    description: str
    atmosphere: str = "neutral"
    motifs: List[str] = field(default_factory=list)
    
@dataclass
class DreamAvatar:
    """The dreamer's representation within the dream"""
    form: str
    abilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
@dataclass
class DreamEvent:
    """A significant event within the dream narrative"""
    description: str
    location: str
    participants: List[str] = field(default_factory=list)
    motifs: List[str] = field(default_factory=list)
    emotional_charge: float = 0.0
    
@dataclass
class DreamNarrative:
    """The complete narrative structure of a dream"""
    title: str
    events: List[DreamEvent] = field(default_factory=list)
    locations: Dict[str, DreamLocation] = field(default_factory=dict)
    avatar: Optional[DreamAvatar] = None
    reflection_points: List[str] = field(default_factory=list)
    recurring_motifs: Dict[str, int] = field(default_factory=dict)
    paradox_moments: List[Tuple[str, str]] = field(default_factory=list)

# Get the parent directory to import from other modules


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Motif Mutation Engine
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MutationOperator(Enum):
    """Types of symbolic mutations that can occur in dream motifs."""
    BLEND = auto()        # Combine two motifs into a new hybrid
    INVERT = auto()       # Create the symbolic opposite
    AMPLIFY = auto()      # Intensify certain qualities
    FRAGMENT = auto()     # Break into constituent elements
    TRANSFORM = auto()    # Change along a symbolic dimension
    ASSOCIATE = auto()    # Create new associations
    RECURSE = auto()      # Create self-referential version


class MotifMutationEngine:
    """
    Engine for symbolic recombination of motifs during dream cycles.
    Creates novel motifs through various mutation operations.
    """
    
    def __init__(self):
        self.mutation_history = []
        self.recent_mutations = deque(maxlen=10)
        self.mutation_depth = 0
        self.contradiction_pressure = 0.0
        self.recursion_threshold = 0.7  # Threshold for triggering recursive dreams
        
        # Mutation probability weights
        self.operator_weights = {
            MutationOperator.BLEND: 0.3,
            MutationOperator.INVERT: 0.1,
            MutationOperator.AMPLIFY: 0.15,
            MutationOperator.FRAGMENT: 0.1,
            MutationOperator.TRANSFORM: 0.2,
            MutationOperator.ASSOCIATE: 0.1,
            MutationOperator.RECURSE: 0.05
        }
        
    def mutate_motif(self, motif: SymbolicMotif, 
                    context_motifs: List[SymbolicMotif] = None, 
                    intensity: float = 0.5) -> SymbolicMotif:
        """
        Apply a mutation operation to create a new motif.
        
        Args:
            motif: Source motif to mutate
            context_motifs: Other motifs that influence the mutation
            intensity: Strength of mutation (0.0-1.0)
            
        Returns:
            A new mutated SymbolicMotif
        """
        # Select mutation operator based on weights
        operator = self._select_weighted_operator()
        
        # If no context motifs provided, create an empty list
        context_motifs = context_motifs or []
        
        # Apply selected operator
        if operator == MutationOperator.BLEND and context_motifs:
            return self._blend_motifs(motif, random.choice(context_motifs), intensity)
        elif operator == MutationOperator.INVERT:
            return self._invert_motif(motif, intensity)
        elif operator == MutationOperator.AMPLIFY:
            return self._amplify_motif(motif, intensity)
        elif operator == MutationOperator.FRAGMENT:
            return self._fragment_motif(motif, intensity)
        elif operator == MutationOperator.TRANSFORM:
            return self._transform_motif(motif, intensity)
        elif operator == MutationOperator.ASSOCIATE and context_motifs:
            return self._associate_motifs(motif, random.choice(context_motifs), intensity)
        elif operator == MutationOperator.RECURSE:
            return self._recurse_motif(motif, intensity)
        else:
            # Default to transform if the selected operation can't be performed
            return self._transform_motif(motif, intensity)
        
    def _select_weighted_operator(self) -> MutationOperator:
        """Select a mutation operator based on weighted probabilities."""
        operators = list(self.operator_weights.keys())
        weights = list(self.operator_weights.values())
        
        # Adjust RECURSE weight based on mutation depth
        if self.mutation_depth > 2:
            recurse_index = operators.index(MutationOperator.RECURSE)
            weights[recurse_index] = min(0.5, weights[recurse_index] * (1.0 + self.mutation_depth * 0.1))
            
        # Adjust FRAGMENT weight based on contradiction pressure
        if self.contradiction_pressure > 0.5:
            fragment_index = operators.index(MutationOperator.FRAGMENT)
            weights[fragment_index] = min(0.5, weights[fragment_index] * (1.0 + self.contradiction_pressure))
            
        return random.choices(operators, weights=weights, k=1)[0]
    
    def _blend_motifs(self, motif1: SymbolicMotif, motif2: SymbolicMotif, 
                     intensity: float) -> SymbolicMotif:
        """Blend two motifs to create a new hybrid."""
        # Create name from components
        name_parts = motif1.name.split()[:1] + motif2.name.split()[-1:]
        new_name = f"Hybrid {' '.join(name_parts)}"
        
        # Blend descriptions
        desc1 = motif1.description.split(".")
        desc2 = motif2.description.split(".")
        new_desc = f"{desc1[0]}. {desc2[0] if desc2 else ''}"
        
        # Create new motif
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=motif2.valence if random.random() > 0.5 else motif1.valence,
            potency=(motif1.potency + motif2.potency) / 2
        )
        
        # Blend dimensional positions
        for dim in set(list(motif1.dimensional_positions.keys()) + 
                      list(motif2.dimensional_positions.keys())):
            pos1 = motif1.dimensional_positions.get(dim, 0.5)
            pos2 = motif2.dimensional_positions.get(dim, 0.5)
            # Blend based on intensity - higher intensity means more equal blend
            if intensity > 0.7:
                new_pos = (pos1 + pos2) / 2
            else:
                # Favor motif1 more when intensity is lower
                new_pos = pos1 * (1 - intensity) + pos2 * intensity
            new_motif.dimensional_positions[dim] = new_pos
        
        # Combine associations with preference for stronger ones
        new_assoc = set()
        assoc1 = motif1.associations
        assoc2 = motif2.associations
        
        # Add shared associations always
        new_assoc.update(assoc1.intersection(assoc2))
        
        # Add some unique associations based on intensity
        unique1 = list(assoc1 - assoc2)
        unique2 = list(assoc2 - assoc1)
        
        # More intensity = more associations
        num_to_take1 = max(1, int(len(unique1) * intensity * 0.7))
        num_to_take2 = max(1, int(len(unique2) * intensity * 0.7))
        
        if unique1:
            new_assoc.update(random.sample(unique1, min(num_to_take1, len(unique1))))
        if unique2:
            new_assoc.update(random.sample(unique2, min(num_to_take2, len(unique2))))
            
        new_motif.associations = new_assoc
        
        # Record mutation
        self.recent_mutations.append({
            "type": "blend", 
            "source": [motif1.id, motif2.id], 
            "result": new_motif.id
        })
        
        return new_motif
    
    def _invert_motif(self, motif: SymbolicMotif, intensity: float) -> SymbolicMotif:
        """Create an inverted/opposing version of a motif."""
        new_name = f"Inverted {motif.name}"
        new_desc = f"The symbolic opposite of {motif.name}"
        
        # Create new motif
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=EmotionalValence.NEGATIVE if motif.valence == EmotionalValence.POSITIVE else EmotionalValence.POSITIVE,
            potency=motif.potency * intensity  # Reduce potency for inversions
        )
        
        # Invert dimensional positions
        for dim, pos in motif.dimensional_positions.items():
            new_motif.dimensional_positions[dim] = 1.0 - pos
        
        # Keep some associations but fewer based on intensity
        retain_count = max(1, int(len(motif.associations) * (1.0 - intensity)))
        new_motif.associations = set(random.sample(list(motif.associations), min(retain_count, len(motif.associations))))
        
        # Record mutation
        self.recent_mutations.append({
            "type": "invert", 
            "source": motif.id, 
            "result": new_motif.id
        })
        
        return new_motif
    
    def _amplify_motif(self, motif: SymbolicMotif, intensity: float) -> SymbolicMotif:
        """Amplify certain qualities of a motif."""
        new_name = f"Amplified {motif.name}"
        new_desc = f"An intensified version of {motif.name}"
        
        # Create new motif with increased potency
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=motif.valence,
            potency=min(1.0, motif.potency * (1.0 + intensity))  # Increase potency
        )
        
        # Amplify dimensional positions (push toward extremes)
        for dim, pos in motif.dimensional_positions.items():
            if pos > 0.5:
                new_motif.dimensional_positions[dim] = min(1.0, pos + (1.0 - pos) * intensity)
            else:
                new_motif.dimensional_positions[dim] = max(0.0, pos - pos * intensity)
        
        # Keep all associations
        new_motif.associations = motif.associations.copy()
        
        # Record mutation
        self.recent_mutations.append({
            "type": "amplify", 
            "source": motif.id, 
            "result": new_motif.id
        })
        
        return new_motif
    
    def _fragment_motif(self, motif: SymbolicMotif, intensity: float) -> SymbolicMotif:
        """Break a motif into a constituent element."""
        # Extract a fragment from the name or description
        name_parts = motif.name.split()
        
        if len(name_parts) > 1:
            # Use a fragment of the original name
            fragment_name = random.choice(name_parts)
            new_name = f"Fragment: {fragment_name}"
        else:
            # Add a qualifier if name has only one word
            qualifiers = ["Essence of", "Shard of", "Element of", "Aspect of"]
            new_name = f"{random.choice(qualifiers)} {motif.name}"
            
        # Create a simpler description
        new_desc = f"A fragmented element derived from {motif.name}"
        
        # Create new motif with reduced potency
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=motif.valence,
            potency=motif.potency * max(0.3, 1.0 - intensity * 0.5)
        )
        
        # Simplify dimensional positioning - keep only strongest dimensions
        sorted_dims = sorted(
            motif.dimensional_positions.items(),
            key=lambda x: abs(x[1] - 0.5),
            reverse=True
        )
        
        # Keep only a few dimensions based on intensity
        dims_to_keep = max(1, int(len(sorted_dims) * (1.0 - intensity * 0.7)))
        for dim, pos in sorted_dims[:dims_to_keep]:
            new_motif.dimensional_positions[dim] = pos
            
        # Reduce associations - keep only a subset
        if motif.associations:
            assoc_count = max(1, int(len(motif.associations) * (1.0 - intensity * 0.7)))
            new_motif.associations = set(random.sample(list(motif.associations), 
                                                     min(assoc_count, len(motif.associations))))
        
        # Record mutation
        self.recent_mutations.append({
            "type": "fragment", 
            "source": [motif.id], 
            "result": new_motif.id
        })
        
        # Reduce contradiction pressure as fragmentation releases tension
        self.contradiction_pressure = max(0.0, self.contradiction_pressure - 0.15)
        
        return new_motif
    
    def _transform_motif(self, motif: SymbolicMotif, intensity: float) -> SymbolicMotif:
        """Transform a motif along one or more symbolic dimensions."""
        # Choose 1-2 dimensions to transform based on intensity
        dimensions = list(SymbolicDimension)
        num_dims = 1 if intensity < 0.5 else 2
        transform_dims = random.sample(dimensions, min(num_dims, len(dimensions)))
        
        # Create transformation description
        transform_desc = []
        for dim in transform_dims:
            if dim.name == "LIGHT_DARK":
                transform_desc.append("luminosity")
            elif dim.name == "OPEN_CLOSED":
                transform_desc.append("containment")
            else:
                transform_desc.append(dim.name.lower().replace("_", "-"))
                
        transform_text = " and ".join(transform_desc)
        
        new_name = f"Transformed {motif.name}"
        new_desc = f"A version of {motif.name} that has shifted in {transform_text}"
        
        # Create new motif
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=motif.valence,
            potency=motif.potency
        )
        
        # Copy dimensional positions from original
        new_motif.dimensional_positions = motif.dimensional_positions.copy()
        
        # Apply transformations
        for dim in transform_dims:
            # Get current position or default
            current = new_motif.dimensional_positions.get(dim, 0.5)
            
            # Calculate transformation - high intensity means bigger shift
            delta = (random.random() * 2 - 1) * intensity * 0.5  # Range: -0.5 to 0.5 scaled by intensity
            new_pos = max(0.0, min(1.0, current + delta))
            new_motif.dimensional_positions[dim] = new_pos
            
        # Copy associations
        new_motif.associations = motif.associations.copy()
        
        # Record mutation
        self.recent_mutations.append({
            "type": "transform", 
            "source": [motif.id], 
            "result": new_motif.id, 
            "dimensions": [d.name for d in transform_dims]
        })
        
        return new_motif
    
    def _associate_motifs(self, motif1: SymbolicMotif, motif2: SymbolicMotif, 
                         intensity: float) -> SymbolicMotif:
        """Create a new motif that represents an association between two others."""
        new_name = f"Association: {motif1.name}→{motif2.name}"
        new_desc = f"A symbolic connection between {motif1.name} and {motif2.name}"
        
        # Create new motif
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            potency=min(motif1.potency, motif2.potency) * (0.7 + intensity * 0.3)
        )
        
        # Mix emotional valence based on intensity
        if motif1.valence and motif2.valence and motif1.valence != motif2.valence:
            # Higher intensity means more likely to take second motif's valence
            if random.random() < intensity:
                new_motif.valence = motif2.valence
            else:
                new_motif.valence = motif1.valence
        else:
            # Keep existing valence if both are the same or one is None
            new_motif.valence = motif2.valence if motif2.valence else motif1.valence
            
        # Create intermediate dimensional positions
        all_dims = set(list(motif1.dimensional_positions.keys()) + 
                      list(motif2.dimensional_positions.keys()))
                      
        for dim in all_dims:
            pos1 = motif1.dimensional_positions.get(dim, 0.5)
            pos2 = motif2.dimensional_positions.get(dim, 0.5)
            
            # Instead of averaging, create a position that represents connection
            # Higher intensity means position is closer to the midpoint
            if intensity > 0.7:
                # Strong association - create midpoint
                new_motif.dimensional_positions[dim] = (pos1 + pos2) / 2
            else:
                # Weaker association - create a position that's between but weighted
                weight = 0.3 + intensity * 0.4  # Range: 0.3-0.7
                new_motif.dimensional_positions[dim] = pos1 * (1-weight) + pos2 * weight
        
        # Create new association combining both (prefer shared ones)
        new_assoc = motif1.associations.intersection(motif2.associations)
        if len(new_assoc) < 2:  # If not enough shared associations
            # Add some from each source
            assoc1 = list(motif1.associations - motif2.associations)
            assoc2 = list(motif2.associations - motif1.associations)
            
            # Select based on intensity
            count1 = max(1, int(len(assoc1) * intensity * 0.5))
            count2 = max(1, int(len(assoc2) * intensity * 0.5))
            
            if assoc1:
                new_assoc.update(random.sample(assoc1, min(count1, len(assoc1))))
            if assoc2:
                new_assoc.update(random.sample(assoc2, min(count2, len(assoc2))))
                
        new_motif.associations = new_assoc
        
        # Record mutation
        self.recent_mutations.append({
            "type": "associate", 
            "source": [motif1.id, motif2.id], 
            "result": new_motif.id
        })
        
        return new_motif
    
    def _recurse_motif(self, motif: SymbolicMotif, intensity: float) -> SymbolicMotif:
        """Create a self-referential version of the motif."""
        new_name = f"Recursive {motif.name}"
        new_desc = f"A self-referential version of {motif.name} that contains itself"
        
        # Create new motif with increased potency
        new_motif = SymbolicMotif(
            name=new_name,
            description=new_desc,
            valence=motif.valence,
            potency=motif.potency * (1.0 + intensity * 0.3)  # Self-reference increases potency
        )
        
        # Copy and intensify dimensional positions
        for dim, pos in motif.dimensional_positions.items():
            # Intensify deviation from center
            deviation = pos - 0.5
            intensified = 0.5 + deviation * (1.0 + intensity * 0.5)
            new_motif.dimensional_positions[dim] = max(0.0, min(1.0, intensified))
            
        # Add self-reference to associations
        new_motif.associations = motif.associations.copy()
        new_motif.associations.add(motif.id)  # Self-reference
        
        # Record mutation
        self.recent_mutations.append({
            "type": "recurse", 
            "source": [motif.id], 
            "result": new_motif.id
        })
        
        # Increase recursion depth counter
        self.mutation_depth += 1
        
        # If depth exceeds threshold, flag for potential dream recursion
        if self.mutation_depth >= 3:
            self.contradiction_pressure = min(1.0, self.contradiction_pressure + 0.25)
        
        return new_motif
    
    def check_for_motif_collapse(self, motifs: List[SymbolicMotif]) -> bool:
        """
        Check if current motif state indicates a collapse that should trigger recursion.
        
        A collapse occurs when:
        1. Contradiction pressure is high
        2. There are multiple recursive motifs
        3. There are opposing motifs with high potency
        
        Args:
            motifs: List of active motifs to check
            
        Returns:
            True if conditions for motif collapse are present
        """
        if not motifs or len(motifs) < 2:
            return False
            
        # Count recursive motifs
        recursive_count = sum(1 for m in motifs if "Recursive" in m.name)
        
        # Check for high potency opposing motifs
        high_potency = [m for m in motifs if m.potency > 0.7]
        
        # Check dimensional opposition
        dimensional_tension = 0
        for dim in SymbolicDimension:
            positions = [m.dimensional_positions.get(dim, 0.5) for m in motifs]
            if len(positions) >= 2:
                # Calculate max distance between positions
                max_dist = max(positions) - min(positions)
                dimensional_tension += max_dist
                
        # Normalize tension
        if len(list(SymbolicDimension)) > 0:
            dimensional_tension /= len(list(SymbolicDimension))
            
        # Calculate collapse probability
        collapse_chance = 0.0
        collapse_chance += self.contradiction_pressure * 0.4  # 40% from contradiction pressure
        collapse_chance += min(0.3, recursive_count * 0.1)  # Up to 30% from recursive motifs
        collapse_chance += dimensional_tension * 0.3  # Up to 30% from dimensional tension
        
        # Add contribution from high potency motifs
        if len(high_potency) >= 2:
            collapse_chance += min(0.2, (len(high_potency) - 1) * 0.1)  # Up to 20%
            
        # Check if above threshold
        return collapse_chance >= self.recursion_threshold
    
    def generate_mutation_batch(self, 
                              source_motifs: List[SymbolicMotif], 
                              batch_size: int = 3,
                              intensity: float = 0.5) -> List[SymbolicMotif]:
        """
        Generate a batch of mutations from source motifs.
        
        Args:
            source_motifs: List of motifs to mutate
            batch_size: Number of mutations to generate
            intensity: Strength of mutations
            
        Returns:
            List of new mutated motifs
        """
        if not source_motifs:
            return []
            
        new_motifs = []
        
        for _ in range(batch_size):
            # Select random source motif
            source = random.choice(source_motifs)
            
            # Select random context motifs (excluding source)
            context = [m for m in source_motifs if m.id != source.id]
            
            # Generate mutation
            new_motif = self.mutate_motif(source, context, intensity)
            new_motifs.append(new_motif)
            
        return new_motifs
    
    def reset(self):
        """Reset the mutation engine state."""
        self.mutation_history.extend(list(self.recent_mutations))
        self.recent_mutations.clear()
        self.mutation_depth = 0
        self.contradiction_pressure = 0.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Memory Integration Components
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MemoryIntegrator:
    """
    Handles integration of dream motifs with episodic memory and knowledge library.
    Allows dream experiences to influence long-term memory structures.
    """
    
    def __init__(self, episodic_memory=None, knowledge_library=None):
        self.episodic_memory = episodic_memory
        self.knowledge_library = knowledge_library
        self.pending_motifs = []
        self.integration_history = []
        
        # Configure integration settings
        self.settings = {
            "min_importance": 0.4,        # Minimum importance for integration
            "memory_encoding_dim": 64,    # Encoding dimension for memory vectors
            "narrative_threshold": 0.6,   # Min coherence for narrative integration
            "motif_vector_size": 16       # Size of motif vectors
        }
        
        # Track memory merging statistics
        self.merge_statistics = {}
        
    def register_episodic_memory(self, memory_system: MemoireEpisodique):
        """Register an episodic memory system for integration."""
        self.episodic_memory = memory_system
        
    def register_knowledge_library(self, library_system):
        """Register a knowledge library system for integration."""
        self.knowledge_library = library_system
        
    def store_dream_experience(self, 
                              dream_narrative: DreamNarrative, 
                              motif_library: Dict[str, SymbolicMotif]) -> Dict:
        """
        Store a complete dream experience in memory systems.
        
        Args:
            dream_narrative: The complete dream narrative
            motif_library: Dictionary of motifs from the dream
            
        Returns:
            Dictionary with integration results
        """
        results = {
            "episodic_memories": [],
            "knowledge_fragments": [],
            "motifs_integrated": 0,
            "status": "success"
        }
        
        if not self.episodic_memory and not self.knowledge_library:
            return {"status": "error", "message": "No memory systems registered"}
        
        # 1. Convert significant events to episodic memories
        if self.episodic_memory:
            memories = self._create_episodic_memories(dream_narrative, motif_library)
            for memory_content, encoding in memories:
                try:
                    memory_id = self.episodic_memory.store(memory_content, encoding)
                    results["episodic_memories"].append(memory_id)
                except Exception as e:
                    results["status"] = "partial"
                    results["errors"] = results.get("errors", []) + [str(e)]
        
        # 2. Store significant motifs in knowledge library
        if self.knowledge_library:
            fragments = self._create_knowledge_fragments(dream_narrative, motif_library)
            for fragment in fragments:
                try:
                    # Add fragment to library
                    if hasattr(self.knowledge_library, "add_fragment"):
                        success = self.knowledge_library.add_fragment(fragment)
                        if success:
                            results["knowledge_fragments"].append(fragment.identifier)
                    elif hasattr(self.knowledge_library, "create_fragment_from_text"):
                        # Alternative API
                        tags = set(fragment.get("tags", []))
                        frag = self.knowledge_library.create_fragment_from_text(
                            fragment.get("content", ""),
                            fragment.get("identifier", None),
                            tags
                        )
                        results["knowledge_fragments"].append(frag.identifier)
                except Exception as e:
                    results["status"] = "partial"
                    results["errors"] = results.get("errors", []) + [str(e)]
                    
        # Count integrated motifs
        results["motifs_integrated"] = len(results["episodic_memories"]) + len(results["knowledge_fragments"])
        
        return results
    
    def _create_episodic_memories(self, 
                                dream_narrative: DreamNarrative, 
                                motif_library: Dict[str, SymbolicMotif]) -> List[Tuple[Dict, np.ndarray]]:
        """
        Create episodic memory entries from dream narrative.
        
        Returns list of (content, encoding) tuples.
        """
        memories = []
        
        # Process significant events
        for event in dream_narrative.events:
            # Skip if not significant enough
            if not event.emotional_impact or sum(event.emotional_impact.values()) < self.settings["min_importance"]:
                continue
                
            # Create memory content
            memory_content = {
                "type": "dream_event",
                "description": event.description,
                "dream_id": dream_narrative.dream_id,
                "timestamp": event.timestamp,
                "emotional_charge": max(event.emotional_impact.values()) if event.emotional_impact else 0.0,
                "importance": sum(event.emotional_impact.values()) / max(1, len(event.emotional_impact)),
                "recursive_depth": 1,  # Dreams are inherently recursive
                "motif_ids": event.participating_motifs,
                "motif_names": [
                    motif_library[mid].name for mid in event.participating_motifs 
                    if mid in motif_library
                ]
            }
            
            # Generate encoding vector from motifs and description
            encoding = self._generate_memory_encoding(event, motif_library)
            
            memories.append((memory_content, encoding))
        
        # Add significant reflection points
        for i, reflection in enumerate(dream_narrative.reflection_points):
            memory_content = {
                "type": "dream_reflection",
                "description": reflection,
                "dream_id": dream_narrative.dream_id,
                "timestamp": time.time() - (len(dream_narrative.reflection_points) - i),
                "emotional_charge": 0.5,  # Reflections have moderate emotional charge
                "importance": 0.7,        # But high importance
                "recursive_depth": 2,     # Reflections are more recursive
                "motif_ids": [],          # No specific motifs
                "is_reflection": True
            }
            
            # Generate encoding for reflection
            encoding = self._generate_reflection_encoding(reflection)
            
            memories.append((memory_content, encoding))
            
        # Add memory of recurring motifs
        if dream_narrative.recurring_motifs:
            top_recurring = sorted(
                [(m_id, count) for m_id, count in dream_narrative.recurring_motifs.items()],
                key=lambda x: x[1],
                reverse=True
            )[:3]  # Top 3 recurring motifs
            
            recurring_desc = "Recurring symbols in dream: " + ", ".join([
                motif_library[mid].name for mid, _ in top_recurring if mid in motif_library
            ])
            
            memory_content = {
                "type": "dream_motifs",
                "description": recurring_desc,
                "dream_id": dream_narrative.dream_id,
                "timestamp": time.time(),
                "emotional_charge": 0.3,
                "importance": 0.6,
                "recursive_depth": 1,
                "motif_ids": [mid for mid, _ in top_recurring],
                "recurring_counts": dict(top_recurring)
            }
            
            # Generate encoding for recurring motifs
            motif_encodings = [
                self._generate_motif_encoding(motif_library[mid]) 
                for mid, _ in top_recurring if mid in motif_library
            ]
            
            if motif_encodings:
                encoding = np.mean(motif_encodings, axis=0)
            else:
                encoding = np.random.randn(self.settings["memory_encoding_dim"])
                
            memories.append((memory_content, encoding))
        
        return memories
    
    def _create_knowledge_fragments(self, 
                                  dream_narrative: DreamNarrative,
                                  motif_library: Dict[str, SymbolicMotif]) -> List[Dict]:
        """
        Create knowledge library fragments from dream narrative.
        
        Returns a list of KnowledgeFragment objects or dictionaries.
        """
        fragments = []
        
        # Only create fragments from significant motifs
        significant_motifs = {}
        
        # Add recurring motifs
        for motif_id, count in dream_narrative.recurring_motifs.items():
            if count >= 2 and motif_id in motif_library:  # Only if appeared multiple times
                significant_motifs[motif_id] = motif_library[motif_id]
                
        # Add motifs with high potency
        for motif_id, motif in motif_library.items():
            if motif.potency >= 0.7 and motif_id not in significant_motifs:
                significant_motifs[motif_id] = motif
                
        # Create fragments from significant motifs
        for motif_id, motif in significant_motifs.items():
            # Create a rich content description of the motif
            content = f"# Dream Motif: {motif.name}\n\n"
            content += f"{motif.description}\n\n"
            content += "## Symbolic Properties\n\n"
            
            # Add dimensional information
            if motif.dimensional_positions:
                content += "### Dimensional Positions\n\n"
                for dim, pos in motif.dimensional_positions.items():
                    content += f"- {dim.name}: {pos:.2f}\n"
            
            # Add emotional valence if present
            if motif.valence:
                content += f"\n### Emotional Valence\n\n- {motif.valence.name}\n"
                
            # Add associations
            if motif.associations:
                content += "\n### Associations\n\n"
                for assoc in motif.associations:
                    content += f"- {assoc}\n"
            
            # Add dream context
            content += f"\n## Dream Context\n\nEncountered in dream {dream_narrative.dream_id}.\n"
            content += f"Potency: {motif.potency:.2f}\n"
            content += f"Recurrence: {dream_narrative.recurring_motifs.get(motif_id, 1)} times\n"
            
            # Generate tags
            tags = set()
            tags.add("dream_motif")
            
            # Add dimensional tags
            for dim, pos in motif.dimensional_positions.items():
                if pos > 0.7:
                    tags.add(f"high_{dim.name.lower()}")
                elif pos < 0.3:
                    tags.add(f"low_{dim.name.lower()}")
            
            # Add emotional tag
            if motif.valence:
                tags.add(motif.valence.name.lower())
            
            # Add potency tag
            if motif.potency > 0.8:
                tags.add("high_potency")
            elif motif.potency < 0.4:
                tags.add("low_potency")
                
            # Create a unique identifier
            identifier = f"dream_motif_{motif_id}_{int(time.time())}"
            
            # Different implementations based on what's available
            try:
                # Try to create a KnowledgeFragment directly if we have the class
                from .knowledge_library import KnowledgeFragment, MotifCategory, TimelineMarker, SymbolicMotif as LibraryMotif
                
                # Adapt dream motif to library motif
                library_motif = self._convert_to_library_motif(motif)
                
                # Create timeline marker for dream
                timeline = TimelineMarker(
                    symbolic_markers={"dream", "unconscious"},
                    recursive_depth=1
                )
                
                fragment = KnowledgeFragment(
                    identifier=identifier,
                    content=content,
                    tags=tags,
                    associations={motif.name, "dream", "symbolic"},
                    motifs=[library_motif],
                    timeline=timeline,
                    fragment_type="dream_motif",
                    content_sample=f"Dream Motif: {motif.name} - {motif.description[:50]}..."
                )
                
                fragments.append(fragment)
                
            except (ImportError, AttributeError):
                # Fallback to dictionary representation
                fragment = {
                    "identifier": identifier,
                    "content": content,
                    "tags": list(tags),
                    "associations": [motif.name, "dream", "symbolic"],
                    "type": "dream_motif",
                    "sample": f"Dream Motif: {motif.name} - {motif.description[:50]}..."
                }
                
                fragments.append(fragment)
        
        # Add significant paradox moments
        for paradox, resolution in dream_narrative.paradox_moments:
            content = f"# Dream Paradox\n\n"
            content += f"Paradox: {paradox}\n\n"
            content += f"Resolution: {resolution}\n\n"
            content += f"From dream: {dream_narrative.dream_id}\n"
            
            identifier = f"dream_paradox_{dream_narrative.dream_id}_{int(time.time())}"
            
            fragment = {
                "identifier": identifier,
                "content": content,
                "tags": ["dream_paradox", "paradox", "contradiction", "dream"],
                "associations": ["paradox", "resolution", "dream"],
                "type": "dream_paradox"
            }
            
            fragments.append(fragment)
        
        return fragments
    
    def _convert_to_library_motif(self, dream_motif: SymbolicMotif):
        """Convert a dream motif to a knowledge library motif."""
        try:
            from .knowledge_library import SymbolicMotif as LibraryMotif, MotifCategory
            
            # Map dream dimensions to motif categories
            category_map = {
                SymbolicDimension.LIGHT_DARK: MotifCategory.ELEMENTAL,
                SymbolicDimension.OPEN_CLOSED: MotifCategory.STRUCTURAL,
                SymbolicDimension.RISING_FALLING: MotifCategory.TEMPORAL,
                SymbolicDimension.CONNECTING_SEPARATING: MotifCategory.PROCEDURAL,
                SymbolicDimension.TRANSFORMING_STATIC: MotifCategory.PROCEDURAL,
                SymbolicDimension.FAMILIAR_STRANGE: MotifCategory.ARCHETYPAL,
                SymbolicDimension.HARMONIC_DISCORDANT: MotifCategory.RESONANT,
                SymbolicDimension.SOLID_FLUID: MotifCategory.ELEMENTAL,
                SymbolicDimension.ORGANIC_MECHANICAL: MotifCategory.STRUCTURAL,
                SymbolicDimension.INTIMATE_DISTANT: MotifCategory.RESONANT
            }
            
            # Determine primary category based on strongest dimensional position
            strongest_dim = max(
                dream_motif.dimensional_positions.items(),
                key=lambda x: abs(x[1] - 0.5),
                default=(None, 0)
            )[0]
            
            category = category_map.get(strongest_dim, MotifCategory.THEMATIC)
            
            # Convert associations to standard format
            associations = dream_motif.associations.copy()
            
            # Create roots from name components
            name_parts = dream_motif.name.split()
            roots = {part.lower() for part in name_parts if len(part) > 3}
            
            # Create library motif
            library_motif = LibraryMotif(
                name=dream_motif.name,
                category=category,
                associations=associations,
                description=dream_motif.description,
                archetypal_roots=roots,
                symbolic_charge=0.0,  # Default neutral charge
                recurrence_depth=1    # Dreams start at depth 1
            )
            
            return library_motif
            
        except (ImportError, AttributeError):
            # Return original if conversion not possible
            return dream_motif
    
    def _generate_memory_encoding(self, event: DreamEvent, motif_library: Dict[str, SymbolicMotif]) -> np.ndarray:
        try:
            # Initialize encoding
            encoding_size = self.settings["memory_encoding_dim"]
            encoding = np.zeros(encoding_size)
            
            # Add motif components
            motif_components = []
            for motif_id in event.participating_motifs:
                if motif_id in motif_library:
                    motif = motif_library[motif_id]
                    motif_vec = self._generate_motif_encoding(motif)
                    motif_components.append(motif_vec)
            
            # Add event description component
            description_vec = self._text_to_vector(event.description, encoding_size)
            
            # Add emotional impact component
            emotion_vec = np.zeros(encoding_size)
            for emotion, intensity in event.emotional_impact.items():
                # Convert emotion enum to index and set that part of vector
                try:
                    emotion_idx = emotion.value % (encoding_size // 2)
                    emotion_vec[emotion_idx] = intensity
                    emotion_vec[emotion_idx + encoding_size // 2] = intensity * 0.5  # Echo
                except (AttributeError, TypeError):
                    pass
            
            # Combine components with weighting
            if motif_components:
                motif_vec = np.mean(motif_components, axis=0)
                encoding += motif_vec * 0.5  # 50% from motifs
                
            encoding += description_vec * 0.3  # 30% from description
            encoding += emotion_vec * 0.2     # 20% from emotions
            
            # Normalize
            norm = np.linalg.norm(encoding)
            if norm > 0:
                encoding = encoding / norm
                
            return encoding
        except Exception as e:
            logger.error(f"Error generating memory encoding: {e}")
            return np.zeros(self.settings["memory_encoding_dim"])
    
    def _generate_reflection_encoding(self, reflection: str) -> np.ndarray:
        """Generate a vector encoding for a dream reflection."""
        encoding_size = self.settings["memory_encoding_dim"]
        
        # Start with text encoding
        encoding = self._text_to_vector(reflection, encoding_size)
        
        # Add a reflection signature - slight boost to specific dimensions
        reflection_signature = np.zeros(encoding_size)
        reflection_signature[encoding_size // 2:encoding_size // 2 + 8] = 0.2
        
        # Combine
        encoding = encoding * 0.8 + reflection_signature
        
        # Normalize
        norm = np.linalg.norm(encoding)
        if norm > 0:
            encoding = encoding / norm
            
        return encoding
    
    def _generate_motif_encoding(self, motif: SymbolicMotif) -> np.ndarray:
        """Generate a vector encoding for a motif."""
        encoding_size = self.settings["memory_encoding_dim"]
        motif_vec_size = min(self.settings["motif_vector_size"], encoding_size // 4)
        
        # Start with base vector from motif name
        encoding = np.zeros(encoding_size)
        name_hash = int(hashlib.md5(motif.name.encode()).hexdigest(), 16)
        np.random.seed(name_hash)
        name_vec = np.random.randn(motif_vec_size)
        
        # Place name vector at start of encoding
        encoding[:motif_vec_size] = name_vec
        
        # Add dimensional positions
        dim_start = motif_vec_size
        dim_count = min(len(list(SymbolicDimension)), (encoding_size - dim_start) // 2)
        
        for i, dim in enumerate(list(SymbolicDimension)[:dim_count]):
            if dim in motif.dimensional_positions:
                pos = motif.dimensional_positions[dim]
                idx = dim_start + i * 2
                encoding[idx] = pos
                encoding[idx + 1] = 1.0 - pos  # Complement
        
        # Add emotional valence if present
        if motif.valence:
            try:
                emotion_idx = (motif.valence.value * 3) % (encoding_size // 4)
                emotion_idx += encoding_size // 2  # Place in second half
                encoding[emotion_idx] = motif.potency
            except (AttributeError, TypeError):
                pass
        
        # Normalize
        norm = np.linalg.norm(encoding)
        if norm > 0:
            encoding = encoding / norm
            
        return encoding
    
    def _text_to_vector(self, text: str, vector_size: int) -> np.ndarray:
        """Convert text to a vector representation."""
        # Simple deterministic vector encoding of text
        # In a real implementation, this would use a proper text embedding model
        
        # Create a hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Use hash to seed random number generator
        seed = int(text_hash, 16) % (2**32 - 1)
        np.random.seed(seed)
        
        # Generate a random vector
        vec = np.random.randn(vector_size)
        
        # Normalize
        return vec / np.linalg.norm(vec)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Dream Engine Core Updates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DreamStasisEngine:
    """Core engine for simulating the dream experience."""
    
    def __init__(self):
        self.dreamscape: Dict[str, DreamLocation] = {}
        self.motif_library: Dict[str, SymbolicMotif] = {}
        self.avatar: Optional[DreamAvatar] = None
        self.current_narrative: Optional[DreamNarrative] = None
        self.dream_active: bool = False
        self.archetype_templates: Dict[str, Dict] = {}
        
        # Add motif mutation engine
        self.mutation_engine = MotifMutationEngine()
        
        # Add memory integrator
        self.memory_integrator = MemoryIntegrator()
        
        # Add recursion tracking
        self.recursion_depth = 0
        self.max_recursion_depth = 3
        self.recursion_history = []
        
        # Add contradiction tracking
        self.contradiction_pressure = 0.0
        self.contradiction_threshold = 0.75
        self.contradiction_sources = []
        
        self._load_archetypes()

    # [Existing methods remain unchanged]
    
    # Add new methods for motif mutation and recursive dream triggers
    
    def mutate_dreamscape_motifs(self, intensity: float = 0.5, 
                               batch_size: int = 3) -> Dict[str, Any]:
        """
        Apply mutations to motifs in the current dreamscape.
        
        Args:
            intensity: Strength of mutations (0.0-1.0)
            batch_size: Number of mutations to perform
            
        Returns:
            Dictionary with mutation results
        """
        if not self.dream_active or not self.dreamscape:
            return {"status": "error", "message": "No active dream"}
            
        # Collect all motifs from current locations
        all_motifs = []
        for location in self.dreamscape.values():
            all_motifs.extend(location.resident_motifs)
            
        # Filter to unique motifs
        unique_motifs = {}
        for motif in all_motifs:
            unique_motifs[motif.id] = motif
        all_motifs = list(unique_motifs.values())
        
        # Generate mutations
        new_motifs = self.mutation_engine.generate_mutation_batch(
            all_motifs, batch_size, intensity
        )
        
        # Add new motifs to library
        for motif in new_motifs:
            self.motif_library[motif.id] = motif
            
        # Distribute new motifs to locations
        self._distribute_motifs_to_locations(new_motifs)
        
        # Check for potential motif collapse
        collapse_detected = self.mutation_engine.check_for_motif_collapse(all_motifs + new_motifs)
        
        # Update contradiction pressure
        self.contradiction_pressure = self.mutation_engine.contradiction_pressure
        
        # Create event for mutations
        if self.avatar and self.current_narrative:
            mutation_event = DreamEvent(
                description=f"{len(new_motifs)} motif mutations occurred in the dreamscape",
                location_id=self.avatar.current_location_id,
                participating_motifs=[m.id for m in new_motifs],
                spawned_motifs=[m.id for m in new_motifs]
            )
            self.current_narrative.add_event(mutation_event)
            
            # Add emotional impact from new motifs
            for motif in new_motifs:
                if motif.valence:
                    if self.avatar.emotional_state.get(motif.valence, 0) < 0.7:
                        self.avatar.emotional_state[motif.valence] = max(
                            self.avatar.emotional_state.get(motif.valence, 0),
                            motif.potency * 0.5
                        )
        
        # Return results
        result = {
            "status": "success",
            "mutations": [
                {
                    "id": motif.id,
                    "name": motif.name, 
                    "description": motif.description
                }
                for motif in new_motifs
            ],
            "collapse_detected": collapse_detected,
            "contradiction_pressure": self.contradiction_pressure
        }
        
        # If collapse detected and we haven't exceeded recursion depth,
        # add recursion trigger information
        if collapse_detected and self.recursion_depth < self.max_recursion_depth:
            result["recursion_triggered"] = True
            result["recursion_depth"] = self.recursion_depth + 1
            
        return result
    
    def _distribute_motifs_to_locations(self, motifs: List[SymbolicMotif]):
        """Distribute new motifs to appropriate dreamscape locations."""
        if not motifs or not self.dreamscape:
            return
            
        for motif in motifs:
            # Find best matching location based on dimensional signature
            best_match = None
            best_score = -float('inf')
            
            for loc_id, location in self.dreamscape.items():
                # Skip if already has too many motifs
                if len(location.resident_motifs) >= 5:
                    continue
                    
                # Calculate compatibility score
                score = 0
                for dim, pos in motif.dimensional_positions.items():
                    loc_pos = location.dimensional_signature.get(dim, 0.5)
                    # Higher score for closer positions
                    score -= abs(pos - loc_pos) * 2
                
                if score > best_score:
                    best_score = score
                    best_match = loc_id
            
            # Add to the best matching location, or avatar's current location if none found
            if best_match:
                self.dreamscape[best_match].resident_motifs.append(motif)
            elif self.avatar and self.avatar.current_location_id in self.dreamscape:
                self.dreamscape[self.avatar.current_location_id].resident_motifs.append(motif)
            else:
                # If no suitable location, add to a random one
                random_loc_id = random.choice(list(self.dreamscape.keys()))
                self.dreamscape[random_loc_id].resident_motifs.append(motif)
                
        # Update all location signatures after adding new motifs
        for location in self.dreamscape.values():
            location.compute_signature_from_motifs()
    
    def trigger_recursive_dream(self) -> Dict[str, Any]:
        if self.recursion_depth >= self.max_recursion_depth:
            return {"status": "error", "message": "Maximum recursion depth reached"}
        if not self.dream_active or not self.dreamscape:
            return {"status": "error", "message": "No active dream"}
            
        # Save current dream state for return
        saved_dreamscape = self.dreamscape.copy()
        saved_avatar = self.avatar
        saved_narrative = self.current_narrative
        
        # Extract key motifs for recursion
        key_motifs = []
        
        # Start with avatar's carried motifs
        if self.avatar and self.avatar.carried_motifs:
            key_motifs.extend(self.avatar.carried_motifs)
            
        # Add recurring motifs from current narrative
        if self.current_narrative and self.current_narrative.recurring_motifs:
            recurring_ids = sorted(
                self.current_narrative.recurring_motifs.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]  # Top 3 most recurring
            
            for motif_id, _ in recurring_ids:
                if motif_id in self.motif_library:
                    key_motifs.append(self.motif_library[motif_id])
        
        # If not enough key motifs, add some random ones from active location
        if len(key_motifs) < 3 and self.avatar and self.avatar.current_location_id in self.dreamscape:
            current_loc = self.dreamscape[self.avatar.current_location_id]
            for motif in current_loc.resident_motifs[:3]:  # Up to 3 more
                if motif not in key_motifs:
                    key_motifs.append(motif)
        
        # Ensure we have motifs for the recursive dream
        if not key_motifs:
            return {"status": "error", "message": "No motifs for recursive dream"}
            
        # Transform motifs for the recursive dream
        recursive_motifs = []
        for motif in key_motifs:
            # Apply recursion
            recursive_motif = self.mutation_engine._recurse_motif(motif, 0.8)
            recursive_motif.name = f"Recursive {motif.name}"
            recursive_motif.description = f"A deeper recursive manifestation of {motif.name}"
            recursive_motifs.append(recursive_motif)
            
        # Create a new dream world with these motifs
        self.dreamscape = {}
        self.motif_library = {}
        locations = self.create_dream_world(recursive_motifs)
        
        # Create new avatar with awareness of recursion
        core_aspects = self.avatar.core_aspects.copy() if self.avatar else ["recursive"]
        if "recursive" not in core_aspects:
            core_aspects.append("recursive")
            
        self.avatar = DreamAvatar(
            core_aspects=core_aspects,
            current_location_id=next(iter(self.dreamscape.keys())),
            awareness_level=min(1.0, (self.avatar.awareness_level if self.avatar else 0.3) + 0.2),
            carried_motifs=[]  # Start with no carried motifs
        )
        
        # Create new narrative for the recursive dream
        self.current_narrative = DreamNarrative(
            dream_id=f"recursive_{saved_narrative.dream_id if saved_narrative else str(uuid.uuid4())}"
        )
        
        # Add a reality breach paradox to the narrative
        self.current_narrative.paradox_moments.append((
            "The dreamer realizes they are dreaming within a dream",
            "Through recursive awareness, deeper symbolic patterns emerge"
        ))
        
        # Increment recursion depth
        self.recursion_depth += 1
        
        # Create entry event for recursive dream
        initial_location = self.dreamscape[self.avatar.current_location_id]
        entry_event = DreamEvent(
            description=f"Entry into a deeper recursive dream at {initial_location.name}",
            location_id=initial_location.id,
            participating_motifs=[m.id for m in initial_location.resident_motifs]
        )
        self.current_narrative.add_event(entry_event)
        
        # Update avatar's emotional state based on location
        self.avatar.update_emotional_state(initial_location)
        
        # Add reflection point about recursion
        reflection = f"The dream folds inward, creating a dream within a dream at depth {self.recursion_depth}"
        self.current_narrative.reflection_points.append(reflection)
        
        # Save recursion state
        self.recursion_history.append({
            "original_dreamscape": saved_dreamscape,
            "original_avatar": saved_avatar,
            "original_narrative": saved_narrative,
            "recursion_depth": self.recursion_depth,
            "entry_event": entry_event
        })
        
        # Reset contradiction pressure
        self.contradiction_pressure = 0.0
        self.mutation_engine.contradiction_pressure = 0.0
        
        # Return recursive dream state
        return {
            "status": "recursive_dream_entered",
            "recursion_depth": self.recursion_depth,
            "location": {
                "id": initial_location.id,
                "name": initial_location.name,
                "description": initial_location.description
            },
            "perceived_motifs": [
                {
                    "id": motif.id,
                    "name": motif.name,
                    "description": motif.description
                }
                for motif in initial_location.resident_motifs
            ],
            "emotional_state": {
                emotion.name: intensity 
                for emotion, intensity in self.avatar.emotional_state.items()
            },
            "awareness_level": self.avatar.awareness_level,
            "reflection": reflection
        }
    
    def return_from_recursive_dream(self) -> Dict[str, Any]:
        """Return from a recursive dream to the previous dream level."""
        if not self.dream_active:
            return {"status": "error", "message": "No active dream"}
            
        if self.recursion_depth <= 0 or not self.recursion_history:
            return {"status": "error", "message": "Not in a recursive dream"}
            
        # Get the previous dream state
        previous_state = self.recursion_history.pop()
        
        # Store current recursive dream state for memory integration
        recursive_narrative = self.current_narrative
        recursive_motifs = self.motif_library
        
        # Restore previous dream state
        self.dreamscape = previous_state["original_dreamscape"]
        self.avatar = previous_state["original_avatar"]
        self.current_narrative = previous_state["original_narrative"]
        
        # Decrease recursion depth
        self.recursion_depth -= 1
        
        # Create re-entry event
        if self.avatar and self.current_narrative:
            reentry_event = DreamEvent(
                description=f"Return from recursive dream to depth {self.recursion_depth}",
                location_id=self.avatar.current_location_id,
                participating_motifs=[]
            )
            self.current_narrative.add_event(reentry_event)
            
            # Add reflection point about return
            reflection = "The nested dream dissolves, returning to the higher dream layer"
            self.current_narrative.reflection_points.append(reflection)
        
        # Extract insights from recursive dream for integration
        insights = self._extract_recursive_insights(recursive_narrative, recursive_motifs)
        
        # Add new motifs from recursive dream
        if insights["key_motifs"]:
            for motif in insights["key_motifs"]:
                # Check if similar motif already exists
                exists = False
                for existing_id, existing in self.motif_library.items():
                    if existing.name == motif.name or (
                        motif.name.replace("Recursive ", "") == existing.name.replace("Recursive ", "")
                    ):
                        exists = True
                        break
                
                # Add if unique
                if not exists:
                    self.motif_library[motif.id] = motif
                    
            # Distribute to locations
            self._distribute_motifs_to_locations(insights["key_motifs"])
            
            # Add an integration event to the narrative
            integration_event = DreamEvent(
                description=f"Insights from the recursive dream manifest as {len(insights['key_motifs'])} symbolic motifs",
                location_id=self.avatar.current_location_id,
                participating_motifs=[m.id for m in insights["key_motifs"]],
                spawned_motifs=[m.id for m in insights["key_motifs"]]
            )
            self.current_narrative.add_event(integration_event)
        
        # Return results of the integration
        return {
            "status": "returned_from_recursive_dream",
            "recursion_depth": self.recursion_depth,
            "insights": {
                "motifs_integrated": len(insights["key_motifs"]),
                "motif_names": [m.name for m in insights["key_motifs"]],
                "reflections": insights["reflections"]
            },
            "location": {
                "id": self.avatar.current_location_id,
                "name": self.dreamscape[self.avatar.current_location_id].name if self.avatar.current_location_id in self.dreamscape else "Unknown"
            }
        }
    
    def _extract_recursive_insights(self, 
                                   recursive_narrative: DreamNarrative,
                                   recursive_motifs: Dict[str, SymbolicMotif]) -> Dict[str, Any]:
        """Extract insights and key motifs from a recursive dream."""
        insights = {
            "key_motifs": [],
            "reflections": [],
        }
        
        # Extract motifs that appeared frequently
        if recursive_narrative and recursive_narrative.recurring_motifs:
            recurring = sorted(
                recursive_narrative.recurring_motifs.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]  # Top 3 recurring motifs
            
            for motif_id, count in recurring:
                if motif_id in recursive_motifs:
                    motif = recursive_motifs[motif_id]
                    # Transform the motif to indicate it came from a recursive dream
                    transformed = SymbolicMotif(
                        name=f"Recursive Echo: {motif.name}",
                        description=f"A motif that emerged from a deeper dream layer: {motif.description}",
                        valence=motif.valence,
                        potency=motif.potency * 1.2  # Increased potency from recursion
                    )
                    # Copy dimensional positions with slight intensification
                    for dim, pos in motif.dimensional_positions.items():
                        deviation = pos - 0.5
                        transformed.dimensional_positions[dim] = 0.5 + deviation * 1.3  # Intensify
                    
                    # Copy associations
                    transformed.associations = motif.associations.copy()
                    transformed.associations.add("recursive")
                    transformed.associations.add("dream_within_dream")
                    
                    insights["key_motifs"].append(transformed)
        
        # Extract significant reflections
        if recursive_narrative and recursive_narrative.reflection_points:
            # Select the most significant reflections
            for reflection in recursive_narrative.reflection_points[-2:]:  # Last 2 reflections
                insights["reflections"].append(reflection)
                
        # Extract paradox resolutions
        if recursive_narrative and recursive_narrative.paradox_moments:
            for _, resolution in recursive_narrative.paradox_moments:
                insights["reflections"].append(f"Paradox Resolution: {resolution}")
                
        return insights
    
    def check_contradiction_trigger(self) -> Dict[str, Any]:
        """
        Check if contradiction pressure has reached the threshold for recursion.
        
        Returns:
            Dictionary with trigger status and information
        """
        result = {
            "trigger_active": False,
            "contradiction_pressure": self.contradiction_pressure,
            "threshold": self.contradiction_threshold,
            "sources": self.contradiction_sources
        }
        
        # Check if pressure exceeds threshold
        if self.contradiction_pressure >= self.contradiction_threshold:
            result["trigger_active"] = True
            result["message"] = "Contradiction pressure has triggered recursive dream potential"
            
            # Reset pressure after triggering
            self.contradiction_pressure = 0.0
            self.mutation_engine.contradiction_pressure = 0.0
            self.contradiction_sources = []
        
        return result
    
    def add_contradiction_pressure(self, amount: float, source: str) -> float:
        """
        Add contradiction pressure from a named source.
        
        Args:
            amount: Pressure amount to add (0.0-1.0)
            source: Source of the contradiction pressure
            
        Returns:
            New total contradiction pressure
        """
        self.contradiction_pressure = min(1.0, self.contradiction_pressure + amount)
        self.mutation_engine.contradiction_pressure = self.contradiction_pressure
        
        # Track source
        self.contradiction_sources.append({
            "source": source,
            "amount": amount,
            "timestamp": time.time()
        })
        
        # If we have too many sources, keep only the most recent
        if len(self.contradiction_sources) > 10:
            self.contradiction_sources = self.contradiction_sources[-10:]
            
        return self.contradiction_pressure
    
    def hook_memory_systems(self, 
                          episodic_memory: Optional[MemoireEpisodique] = None,
                          knowledge_library: Optional[Any] = None) -> Dict[str, Any]:
        """
        Connect dream simulation to memory systems for integration.
        
        Args:
            episodic_memory: Episodic memory system
            knowledge_library: Knowledge library system
            
        Returns:
            Status of connection
        """
        result = {"status": "partial", "connections": []}
        
        if episodic_memory:
            self.memory_integrator.register_episodic_memory(episodic_memory)
            result["connections"].append("episodic_memory")
            
        if knowledge_library:
            self.memory_integrator.register_knowledge_library(knowledge_library)
            result["connections"].append("knowledge_library")
            
        if result["connections"]:
            result["status"] = "success"
            
        return result
    
    def integrate_dream_to_memory(self) -> Dict[str, Any]:
        """
        Integrate the current dream experience into connected memory systems.
        Should be called when a dream ends.
        
        Returns:
            Integration results
        """
        if not self.dream_active or not self.current_narrative:
            return {"status": "error", "message": "No active dream to integrate"}
            
        # Perform integration
        results = self.memory_integrator.store_dream_experience(
            self.current_narrative,
            self.motif_library
        )
        
        # Add integration reflection
        if self.current_narrative:
            integration_reflection = "As the dream fades, its symbolic patterns integrate into the deeper memory landscape"
            self.current_narrative.reflection_points.append(integration_reflection)
        
        return results
    
    def end_dream(self) -> Dict[str, Any]:
        """
        End the current dream and integrate its contents to memory.
        
        Returns:
            Dictionary with dream summary
        """
        if not self.dream_active:
            return {"status": "error", "message": "No active dream"}
            
        # Integrate dream to memory before ending
        integration_results = self.integrate_dream_to_memory()
        
        # Generate summary stats
        summary = {
            "status": "dream_ended",
            "dream_id": self.current_narrative.dream_id if self.current_narrative else None,
            "duration": self.current_narrative.duration if self.current_narrative else 0,
            "event_count": len(self.current_narrative.events) if self.current_narrative else 0,
            "location_count": len(self.dreamscape),
            "motif_count": len(self.motif_library),
            "recursion_depth": self.recursion_depth,
            "memory_integration": integration_results,
            "key_motifs": [],
            "final_reflections": []
        }
        
        # Add key motifs
        if self.current_narrative and self.current_narrative.recurring_motifs:
            top_motifs = sorted(
                self.current_narrative.recurring_motifs.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]  # Top 5 recurring motifs
            
            for motif_id, count in top_motifs:
                if motif_id in self.motif_library:
                    motif = self.motif_library[motif_id]
                    summary["key_motifs"].append({
                        "id": motif_id,
                        "name": motif.name,
                        "recurrence": count,
                        "potency": motif.potency
                    })
        
        # Add final reflections
        if self.current_narrative and self.current_narrative.reflection_points:
            summary["final_reflections"] = self.current_narrative.reflection_points[-3:]  # Last 3 reflections
        
        # Reset dream state
        self.dream_active = False
        self.recursion_depth = 0
        self.recursion_history = []
        self.mutation_engine.reset()
        
        return summary