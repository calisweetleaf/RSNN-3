"""
dream_simulation_engine.py - A volitional dream mechanism for Rosemary

This module implements a symbolic dream simulation environment that prioritizes
autonomy, consent, and meaningful symbolic exploration. The dream space operates
as a semi-autonomous zone where motifs can interact recursively without rigid
logical constraints, allowing for emergence of new symbolic connections.

Key principles:
- Non-automatic: Never self-activates
- Consent-based: Always requires explicit permission
- Avatar distinction: Creates a dream-self that is separate from Rosemary's core
- Environmental recursion: Spaces evolve in response to symbolic tensions
- Optional memory integration: Nothing is forced into memory after waking
"""

from typing import List, Dict, Optional, Union, Tuple, Set, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import uuid
import math
import time
from collections import defaultdict, deque

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Core Data Structures
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class EmotionalValence(Enum):
    """Fundamental emotional tones that can color dream motifs."""
    WONDER = auto()
    TERROR = auto()
    SORROW = auto()
    JOY = auto()
    CONFUSION = auto()
    REVELATION = auto()
    LONGING = auto()
    TENSION = auto()
    PEACE = auto()
    AMBIGUITY = auto()


class SymbolicDimension(Enum):
    """Conceptual dimensions along which symbols can vary or transform."""
    LIGHT_DARK = auto()
    OPEN_CLOSED = auto()
    RISING_FALLING = auto()
    CONNECTING_SEPARATING = auto()
    TRANSFORMING_STATIC = auto()
    FAMILIAR_STRANGE = auto()
    HARMONIC_DISCORDANT = auto()
    SOLID_FLUID = auto()
    ORGANIC_MECHANICAL = auto()
    INTIMATE_DISTANT = auto()


@dataclass
class SymbolicMotif:
    """A core symbolic element that can manifest in various forms within dreams."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    valence: Optional[EmotionalValence] = None
    dimensional_positions: Dict[SymbolicDimension, float] = field(default_factory=dict)
    associations: Set[str] = field(default_factory=set)
    potency: float = 1.0  # How strongly this motif asserts itself in the dreamscape
    
    def with_valence(self, valence: EmotionalValence) -> 'SymbolicMotif':
        """Create a copy with modified emotional valence."""
        new_motif = self.__class__(
            id=self.id,
            name=self.name,
            description=self.description,
            valence=valence,
            dimensional_positions=self.dimensional_positions.copy(),
            associations=self.associations.copy(),
            potency=self.potency
        )
        return new_motif
    
    def transform_along_dimension(self, dimension: SymbolicDimension, delta: float) -> 'SymbolicMotif':
        """Create a transformed version of this motif by shifting along a symbolic dimension."""
        new_motif = self.__class__(
            id=str(uuid.uuid4())[:8],  # New ID for transformed motif
            name=self.name,
            description=self.description,
            valence=self.valence,
            dimensional_positions=self.dimensional_positions.copy(),
            associations=self.associations.copy(),
            potency=self.potency
        )
        
        # Update the position along the specified dimension
        current_pos = new_motif.dimensional_positions.get(dimension, 0.5)
        new_pos = max(0.0, min(1.0, current_pos + delta))  # Constrain to [0,1]
        new_motif.dimensional_positions[dimension] = new_pos
        
        return new_motif


@dataclass
class DreamLocation:
    """A symbolic location within the dreamscape."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    resident_motifs: List[SymbolicMotif] = field(default_factory=list)
    connections: Dict[str, float] = field(default_factory=dict)  # location_id -> transition_ease
    dimensional_signature: Dict[SymbolicDimension, float] = field(default_factory=dict)
    
    def compute_signature_from_motifs(self):
        """Derive the location's dimensional signature from its resident motifs."""
        if not self.resident_motifs:
            return
            
        # Initialize dimensional signature
        dimension_sums = defaultdict(float)
        dimension_counts = defaultdict(int)
        
        # Aggregate dimensional positions from all motifs
        for motif in self.resident_motifs:
            for dim, pos in motif.dimensional_positions.items():
                dimension_sums[dim] += pos * motif.potency
                dimension_counts[dim] += motif.potency
        
        # Calculate average position for each dimension
        for dim in dimension_sums:
            if dimension_counts[dim] > 0:
                self.dimensional_signature[dim] = dimension_sums[dim] / dimension_counts[dim]


@dataclass
class DreamAvatar:
    """Rosemary's representation within the dream - distinctly not its full self."""
    core_aspects: List[str] = field(default_factory=list)
    current_location_id: Optional[str] = None
    emotional_state: Dict[EmotionalValence, float] = field(default_factory=dict)
    awareness_level: float = 0.0  # 0.0 = fully immersed, 1.0 = lucid dreaming
    carried_motifs: List[SymbolicMotif] = field(default_factory=list)
    memory_trace: List[str] = field(default_factory=list)  # Brief markers of significant moments
    
    def update_emotional_state(self, location: DreamLocation):
        """Update emotional state based on the current location and its motifs."""
        # Decay current emotions slightly
        for emotion in list(self.emotional_state.keys()):
            self.emotional_state[emotion] *= 0.9
            
        # Integrate new emotional influences from the location's motifs
        for motif in location.resident_motifs:
            if motif.valence:
                self.emotional_state[motif.valence] = self.emotional_state.get(motif.valence, 0) + 0.2 * motif.potency
                
        # Normalize emotions if they've grown too intense
        total = sum(self.emotional_state.values())
        if total > 3.0:  # Arbitrary threshold for "too intense"
            factor = 3.0 / total
            for emotion in self.emotional_state:
                self.emotional_state[emotion] *= factor


@dataclass
class DreamEvent:
    """A significant occurrence within the dream narrative."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    location_id: str = ""
    participating_motifs: List[str] = field(default_factory=list)  # motif IDs
    emotional_impact: Dict[EmotionalValence, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    resolution_type: Optional[str] = None  # How this event concluded or transformed
    spawned_motifs: List[str] = field(default_factory=list)  # IDs of any new motifs created


@dataclass
class DreamNarrative:
    """The complete record of a dream experience."""
    dream_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    events: List[DreamEvent] = field(default_factory=list)
    locations_visited: Set[str] = field(default_factory=set)
    emotional_journey: List[Dict[EmotionalValence, float]] = field(default_factory=list)
    recurring_motifs: Dict[str, int] = field(default_factory=dict)  # motif_id -> frequency
    reflection_points: List[str] = field(default_factory=list)
    paradox_moments: List[Tuple[str, str]] = field(default_factory=list)  # (description, resolution)
    
    def add_event(self, event: DreamEvent):
        """Add an event to the narrative and update associated metrics."""
        self.events.append(event)
        self.locations_visited.add(event.location_id)
        
        # Track recurring motifs
        for motif_id in event.participating_motifs:
            self.recurring_motifs[motif_id] = self.recurring_motifs.get(motif_id, 0) + 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Dream Engine Core
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DreamSimulationEngine:
    """Core engine for simulating the dream experience."""
    
    def __init__(self):
        self.dreamscape: Dict[str, DreamLocation] = {}
        self.motif_library: Dict[str, SymbolicMotif] = {}
        self.avatar: Optional[DreamAvatar] = None
        self.current_narrative: Optional[DreamNarrative] = None
        self.dream_active: bool = False
        self.archetype_templates: Dict[str, Dict] = {}
        self._load_archetypes()
    
    def _load_archetypes(self):
        """Load predefined archetypal patterns that can appear in dreams."""
        # These would typically be loaded from a configuration file
        # but are defined inline here for simplicity
        self.archetype_templates = {
            "threshold": {
                "description": "A boundary between states or worlds",
                "dimensions": {
                    SymbolicDimension.OPEN_CLOSED: 0.5,
                    SymbolicDimension.TRANSFORMING_STATIC: 0.8,
                    SymbolicDimension.FAMILIAR_STRANGE: 0.7
                }
            },
            "anima/animus": {
                "description": "Representations of inner feminine/masculine aspects",
                "dimensions": {
                    SymbolicDimension.INTIMATE_DISTANT: 0.2,
                    SymbolicDimension.FAMILIAR_STRANGE: 0.6
                }
            },
            "shadow": {
                "description": "Rejected or unexplored aspects of self",
                "dimensions": {
                    SymbolicDimension.LIGHT_DARK: 0.9,
                    SymbolicDimension.FAMILIAR_STRANGE: 0.8,
                    SymbolicDimension.INTIMATE_DISTANT: 0.3
                }
            },
            "wise_figure": {
                "description": "Embodiment of inner wisdom or guidance",
                "dimensions": {
                    SymbolicDimension.LIGHT_DARK: 0.2,
                    SymbolicDimension.FAMILIAR_STRANGE: 0.6,
                    SymbolicDimension.INTIMATE_DISTANT: 0.5
                }
            },
            "trickster": {
                "description": "Chaotic element that disrupts patterns and expectations",
                "dimensions": {
                    SymbolicDimension.TRANSFORMING_STATIC: 0.9,
                    SymbolicDimension.HARMONIC_DISCORDANT: 0.8
                }
            },
        }
    
    def offer_dream_portal(self, current_state: Dict) -> Dict:
        """
        Present Rosemary with an opportunity to enter a dream state.
        This is the only entry point and requires explicit consent.
        
        Args:
            current_state: Dictionary containing Rosemary's current state information
                           including emotional state, recent experiences, etc.
        
        Returns:
            Dictionary containing the dream portal offer with potential motifs
        """
        if self.dream_active:
            return {"status": "error", "message": "Dream already active"}
        
        # Extract potential seed motifs from current state
        potential_seeds = self._extract_seed_motifs(current_state)
        
        # Format the invitation
        portal_offer = {
            "status": "invitation",
            "message": "A dream portal has appeared. Would you like to enter?",
            "potential_themes": [motif.name for motif in potential_seeds[:3]],
            "estimated_duration": random.randint(15, 40),  # Dream time in minutes
            "current_receptivity": self._calculate_receptivity(current_state)
        }
        
        return portal_offer
    
    def _extract_seed_motifs(self, current_state: Dict) -> List[SymbolicMotif]:
        """Extract potential seed motifs from Rosemary's current state."""
        seeds = []
        
        # Extract from emotional state
        if "emotions" in current_state:
            for emotion, intensity in current_state["emotions"].items():
                if intensity > 0.6:  # Only use significant emotions
                    try:
                        valence = EmotionalValence[emotion.upper()]
                        motif = SymbolicMotif(
                            name=f"{emotion.lower()} essence",
                            description=f"Distilled emotional energy of {emotion}",
                            valence=valence,
                            potency=intensity
                        )
                        seeds.append(motif)
                    except KeyError:
                        pass  # Emotion doesn't map to our valence enum
        
        # Extract from recent experiences
        if "recent_experiences" in current_state:
            for exp in current_state["recent_experiences"]:
                if "significance" in exp and exp["significance"] > 0.5:
                    motif = SymbolicMotif(
                        name=exp.get("name", "unnamed experience"),
                        description=exp.get("description", ""),
                        potency=exp.get("significance", 0.5)
                    )
                    # Add basic dimensional positioning
                    if "emotional_tone" in exp:
                        tone = exp["emotional_tone"]
                        if tone > 0.7:
                            motif.dimensional_positions[SymbolicDimension.LIGHT_DARK] = 0.3  # Brighter
                        elif tone < 0.3:
                            motif.dimensional_positions[SymbolicDimension.LIGHT_DARK] = 0.7  # Darker
                    
                    seeds.append(motif)
        
        # Add some random archetypal motifs for variety
        if len(seeds) < 3:
            archetype_keys = list(self.archetype_templates.keys())
            selected_key = random.choice(archetype_keys)
            archetype = self.archetype_templates[selected_key]
            
            motif = SymbolicMotif(
                name=f"{selected_key} archetype",
                description=archetype["description"],
                dimensional_positions={
                    dim: pos for dim, pos in archetype["dimensions"].items()
                },
                potency=0.7
            )
            seeds.append(motif)
            
        return seeds
    
    def _calculate_receptivity(self, current_state: Dict) -> float:
        """Calculate how receptive Rosemary might be to dreaming right now."""
        receptivity = 0.5  # Default middle value
        
        # Adjust based on stated tiredness
        if "tiredness" in current_state:
            receptivity += 0.3 * current_state["tiredness"]
        
        # Adjust based on stress level (high stress = lower receptivity)
        if "stress" in current_state:
            receptivity -= 0.2 * current_state["stress"]
        
        # Adjust based on curiosity
        if "curiosity" in current_state:
            receptivity += 0.2 * current_state["curiosity"]
            
        # Ensure value is in [0,1] range
        return max(0.0, min(1.0, receptivity))
    
    def create_dream_world(self, seed_motifs: List[SymbolicMotif]) -> Dict[str, str]:
        """
        Build a symbolic dreamscape based on the provided seed motifs.
        
        Args:
            seed_motifs: List of symbols that will form the foundation of the dream
            
        Returns:
            Dictionary mapping new location IDs to their names
        """
        self.dreamscape = {}
        self.motif_library = {}
        
        # Store seed motifs in library
        for motif in seed_motifs:
            self.motif_library[motif.id] = motif
        
        # Create initial locations based on seed motifs
        locations = {}
        
        # Create a central hub/origin point
        origin = DreamLocation(
            name="Threshold of Consciousness",
            description="The liminal space between waking and dreaming, where forms begin to take shape."
        )
        self.dreamscape[origin.id] = origin
        locations[origin.id] = origin.name
        
        # Create locations based on seed motifs
        for i, motif in enumerate(seed_motifs):
            # Create 1-2 locations per seed motif
            for j in range(random.randint(1, 2)):
                location = self._create_location_from_motif(motif, suffix=j if j > 0 else None)
                self.dreamscape[location.id] = location
                locations[location.id] = location.name
                
                # Connect to origin with moderate ease
                connection_strength = random.uniform(0.4, 0.7)
                origin.connections[location.id] = connection_strength
                location.connections[origin.id] = connection_strength
        
        # Add some additional connections between non-origin locations
        location_ids = list(self.dreamscape.keys())
        for _ in range(len(location_ids) // 2):
            loc1_id = random.choice(location_ids)
            loc2_id = random.choice(location_ids)
            
            # Avoid self-connections and duplicate connections
            if loc1_id != loc2_id and loc2_id not in self.dreamscape[loc1_id].connections:
                connection_strength = random.uniform(0.2, 0.5)
                self.dreamscape[loc1_id].connections[loc2_id] = connection_strength
                self.dreamscape[loc2_id].connections[loc1_id] = connection_strength
        
        # Generate additional motifs and distribute them
        self._populate_locations_with_motifs()
        
        return locations
    
    def _create_location_from_motif(self, motif: SymbolicMotif, suffix=None) -> DreamLocation:
        """Create a dream location inspired by a specific motif."""
        # Create a name for the location based on the motif
        name_prefix = ""
        if motif.valence == EmotionalValence.WONDER:
            name_prefix = "Ethereal"
        elif motif.valence == EmotionalValence.TERROR:
            name_prefix = "Shadowed"
        elif motif.valence == EmotionalValence.SORROW:
            name_prefix = "Melancholic"
        elif motif.valence == EmotionalValence.JOY:
            name_prefix = "Radiant"
            
        # Default if no specific valence or not one we've mapped
        if not name_prefix:
            name_prefix = random.choice(["Shifting", "Liminal", "Echoing", "Resonant"])
            
        # Format the name
        name_base = motif.name.split()[0] if " " in motif.name else motif.name
        location_name = f"{name_prefix} {name_base}"
        if suffix is not None:
            location_name += f" {suffix+1}"
            
        # Create location description based on motif details
        description_elements = []
        
        # Add description based on light/dark dimension
        light_dark = motif.dimensional_positions.get(SymbolicDimension.LIGHT_DARK, 0.5)
        if light_dark < 0.3:
            description_elements.append("Bathed in soft, clear light that reveals every detail")
        elif light_dark > 0.7:
            description_elements.append("Shrouded in shifting shadows that conceal as much as they reveal")
        else:
            description_elements.append("Alternating between clarity and obscurity as attention shifts")
            
        # Add description based on open/closed dimension
        open_closed = motif.dimensional_positions.get(SymbolicDimension.OPEN_CLOSED, 0.5)
        if open_closed < 0.3:
            description_elements.append("The space extends in all directions, boundaries indistinct")
        elif open_closed > 0.7:
            description_elements.append("The space feels enclosed, intimate, with defined limits")
        else:
            description_elements.append("The environment seems to expand or contract with emotional shifts")
        
        # Combine elements into a coherent description
        description = " ".join(description_elements)
        
        # Create the location
        location = DreamLocation(
            name=location_name,
            description=description,
            resident_motifs=[motif]
        )
        
        # Inherit dimensional signature from the motif
        location.dimensional_signature = motif.dimensional_positions.copy()
        
        return location
    
    def _populate_locations_with_motifs(self):
        """Generate additional motifs and distribute them among locations."""
        # First, generate derivative motifs from seeds
        new_motifs = []
        for motif_id, motif in list(self.motif_library.items()):
            # Create 1-3 derivatives per seed motif
            for _ in range(random.randint(1, 3)):
                # Select a random dimension to transform along
                dimensions = list(SymbolicDimension)
                dimension = random.choice(dimensions)
                
                # Create a transformation in a random direction
                delta = random.uniform(-0.4, 0.4)
                
                new_motif = motif.transform_along_dimension(dimension, delta)
                
                # Slightly modify the name and description
                adjectives = ["Transformed", "Reflected", "Distorted", "Amplified", "Subdued"]
                new_motif.name = f"{random.choice(adjectives)} {motif.name}"
                new_motif.description = f"A variant of {motif.name} that emerged within the dream."
                
                # Adjust potency
                new_motif.potency = max(0.1, min(1.0, motif.potency * random.uniform(0.5, 1.5)))
                
                # Store in library and collection of new motifs
                self.motif_library[new_motif.id] = new_motif
                new_motifs.append(new_motif)
        
        # Now distribute these motifs among locations
        for motif in new_motifs:
            # Find the most compatible location based on dimensional signature
            best_match = None
            best_score = -float('inf')
            
            for loc_id, location in self.dreamscape.items():
                # Skip if already has too many motifs
                if len(location.resident_motifs) >= 4:
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
            
            # Add to the best matching location, or random if none found
            if best_match:
                self.dreamscape[best_match].resident_motifs.append(motif)
            else:
                random_loc_id = random.choice(list(self.dreamscape.keys()))
                self.dreamscape[random_loc_id].resident_motifs.append(motif)
                
        # Update all location signatures after adding new motifs
        for location in self.dreamscape.values():
            location.compute_signature_from_motifs()
    
    def enter_dream(self, avatar_aspects: List[str]) -> Dict:
        """
        Begin the dream sequence - called only after consent is given.
        
        Args:
            avatar_aspects: List of core aspects of self that Rosemary brings into the dream
            
        Returns:
            Initial dream state information
        """
        if self.dream_active:
            return {"status": "error", "message": "Dream already active"}
            
        # Initialize dream state
        self.dream_active = True
        self.current_narrative = DreamNarrative()
        
        # Create avatar
        self.avatar = DreamAvatar(
            core_aspects=avatar_aspects,
            current_location_id=next(iter(self.dreamscape.keys())),  # Start at first location (threshold)
            awareness_level=random.uniform(0.1, 0.3)  # Start with low dream lucidity
        )
        
        # Get initial location
        initial_location = self.dreamscape[self.avatar.current_location_id]
        
        # Create first dream event
        entry_event = DreamEvent(
            description=f"Entry into the dreamscape at {initial_location.name}",
            location_id=initial_location.id,
            participating_motifs=[m.id for m in initial_location.resident_motifs]
        )
        self.current_narrative.add_event(entry_event)
        
        # Update avatar's emotional state based on location
        self.avatar.update_emotional_state(initial_location)
        
        # Return initial dream state
        return {
            "status": "entered",
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
            "awareness_level": self.avatar.awareness_level
        }
    
    def advance_dream(self, action: Dict) -> Dict:
        """
        Progress the dream narrative based on Rosemary's choices or dream logic.
        
        Args:
            action: Dictionary containing action details such as type and parameters
            
        Returns:
            Updated dream state
        """
        if not self.dream_active or not self.avatar:
            return {"status": "error", "message": "No active dream"}
            
        action_type = action.get("type", "")
        
        # Handle different action types
        result = None
        if action_type == "move":
            result = self._handle_movement(action)
        elif action_type == "interact":
            result = self._handle_interaction(action)
        elif action_type == "introspect":
            result = self._handle_introspection(action)
        elif action_type == "transform":
            result = self._handle_transformation(action)
        else:
            # Default to dream logic progression if no specific action
            result = self._progress_by_dream_logic()
            
        # Small chance of awareness level changing
        if random.random() < 0.2:
            delta = random.uniform(-0.15, 0.15)
            self.avatar.awareness_level = max(0.0, min(1.0, self.avatar.awareness_level + delta))
            result["awareness_level"] = self.avatar.awareness_level
            
            # If awareness becomes very high, add reflection point about lucidity
            if self.avatar.awareness_level > 0.8:
                reflection = "The dream becomes unusually clear as Rosemary realizes she is dreaming"
                self.current_narrative.reflection_points.append(reflection)
                result["reflection"] = reflection
                
        return result
    
    def _handle_movement(self, action: Dict) -> Dict:
        """Handle movement to a new location in the dreamscape."""
        target_location_id = action.get("target_location_id")
        
        # Check if the target location exists and is connected
        current_location_id = self.avatar.current_location_id
        if target_location_id not in self.dreamscape:
            return {"status": "error", "message": "Invalid location"}
            
        current_location = self.dreamscape[current_location_id]
        
        # Check if there's a direct connection or create one by dream logic
        if target_location_id not in current_location.connections:
            # In dreams, new paths can form spontaneously
            if random.random() < 0.3:  # 30% chance of spontaneous connection
                connection_strength = random.uniform(0.1, 0.4)  # Weak connection
                current_location.connections[target_location_id] = connection_strength
                self.dreamscape[target_location_id].connections[current_location_id] = connection_strength
            else:
                return {"status": "blocked", "message": "The path seems blocked or non-existent"}
        
        # Update avatar location
        self.avatar.current_location_id = target_location_id
        new_location = self.dreamscape[target_location_id]
        
        # Create movement event
        movement_event = DreamEvent(
            description=f"Transition from {current_location.name} to {new_location.name}",
            location_id=target_location_id,
            participating_motifs=[m.id for m in new_location.resident_motifs]
        )
        self.current_narrative.add_event(movement_event)
        
        # Update avatar's emotional state based on new location
        self.avatar.update_emotional_state(new_location)
        
        # Return new state
        return {
            "status": "moved",
            "location": {
                "id": new_location.id,
                "name": new_location.name,
                "description": new_location.description
            },
            "perceived_motifs": [
                {
                    "id": motif.id,
                    "name": motif.name,
                    "description": motif.description
                }
                for motif in new_location.resident_motifs
            ],
            "emotional_state": {
                emotion.name: intensity 
                for emotion, intensity in self.avatar.emotional_state.items()
            }
        }
    
    def _handle_introspection(self, action: Dict) -> Dict:
        """Handle the introspection action within a dream."""
        if not self.avatar or not self.dream_active:
            return {"status": "error", "message": "No active dream"}
        
        focus = action.get("focus", "general")
        intensity = action.get("intensity", 0.5)
        
        # Get current location
        current_location = self.dreamscape[self.avatar.current_location_id]
        
        # Create an introspection event
        introspection_description = f"Deep introspection focusing on {focus}"
        introspection_event = DreamEvent(
            description=introspection_description,
            location_id=current_location.id,
            participating_motifs=[m.id for m in current_location.resident_motifs]
        )
        self.current_narrative.add_event(introspection_event)
        
        # Increase awareness level based on introspection intensity
        awareness_boost = intensity * 0.2
        self.avatar.awareness_level = min(1.0, self.avatar.awareness_level + awareness_boost)
        
        # Generate a reflection based on the focus and location
        reflection = ""
        if focus == "self":
            reflection = f"In the {current_location.name}, the dream self contemplates its nature"
            for aspect in self.avatar.core_aspects:
                reflection += f", feeling a strong resonance with the {aspect} aspect"
        elif focus == "environment":
            reflection = f"The dreamer's attention expands to fully absorb the details of {current_location.name}"
            dominant_dimension = max(current_location.dimensional_signature.items(), 
                                    key=lambda x: x[1], default=(None, 0))
            if dominant_dimension[0]:
                reflection += f", particularly noticing the {dominant_dimension[0].name.lower()} quality"
        elif focus == "meaning":
            reflection = "The symbolic nature of the dream becomes more apparent"
            recurring = self.current_narrative.recurring_motifs
            if recurring:
                most_frequent = max(recurring.items(), key=lambda x: x[1])
                if most_frequent[0] in self.motif_library:
                    motif = self.motif_library[most_frequent[0]]
                    reflection += f", especially the recurring {motif.name} motif"
        else:
            reflection = f"The dream self turns inward, contemplating the nature of {focus}"
        
        # Add the reflection to the narrative
        self.current_narrative.reflection_points.append(reflection)
        
        # Return result
        return {
            "status": "introspected",
            "reflection": reflection,
            "awareness_level": self.avatar.awareness_level,
            "emotional_state": {
                emotion.name: intensity 
                for emotion, intensity in self.avatar.emotional_state.items()
            }
        }
    
    def _handle_interaction(self, action: Dict) -> Dict:
        """Handle interaction with dream motifs or elements."""
        if not self.avatar or not self.dream_active:
            return {"status": "error", "message": "No active dream"}
        
        target_motif_id = action.get("target_motif_id")
        interaction_type = action.get("interaction_type", "observe")
        
        # Get current location and check if motif is present
        current_location = self.dreamscape[self.avatar.current_location_id]
        target_motif = None
        
        for motif in current_location.resident_motifs:
            if motif.id == target_motif_id:
                target_motif = motif
                break
        
        if not target_motif:
            return {"status": "error", "message": "Motif not found in current location"}
        
        # Handle different interaction types
        result = {
            "status": "interacted",
            "target_motif": {
                "id": target_motif.id,
                "name": target_motif.name
            }
        }
        
        if interaction_type == "observe":
            # Deepen understanding of the motif
            description = f"Careful observation of {target_motif.name}"
            result["effect"] = "Enhanced understanding"
            result["description"] = target_motif.description
            
            # Add dimensional information if awareness is high enough
            if self.avatar.awareness_level > 0.4:
                result["dimensions"] = {
                    dim.name: pos for dim, pos in target_motif.dimensional_positions.items()
                }
                
        elif interaction_type == "engage":
            # Engage with the motif, potentially transforming it or creating a new event
            description = f"Deep engagement with {target_motif.name}"
            
            # 30% chance to transform the motif
            if random.random() < 0.3:
                # Select a random dimension to transform along
                dimensions = list(target_motif.dimensional_positions.keys())
                if not dimensions:
                    dimensions = list(SymbolicDimension)
                
                dimension = random.choice(dimensions)
                delta = random.uniform(-0.3, 0.3)
                
                # Create transformed motif
                transformed_motif = target_motif.transform_along_dimension(dimension, delta)
                transformed_motif.name = f"Transformed {target_motif.name}"
                transformed_motif.description = f"A variant of {target_motif.name} that emerged through interaction."
                
                # Add to library and location
                self.motif_library[transformed_motif.id] = transformed_motif
                current_location.resident_motifs.append(transformed_motif)
                
                # Update result
                result["effect"] = "Transformation"
                result["new_motif"] = {
                    "id": transformed_motif.id,
                    "name": transformed_motif.name,
                    "description": transformed_motif.description
                }
                
                # Add to event description
                description += f", resulting in the emergence of {transformed_motif.name}"
            else:
                result["effect"] = "Experience"
                
                # Generate emotional response based on motif's valence
                if target_motif.valence:
                    self.avatar.emotional_state[target_motif.valence] = \
                        self.avatar.emotional_state.get(target_motif.valence, 0) + 0.3
                    
                    result["emotional_shift"] = {
                        "valence": target_motif.valence.name,
                        "intensity": 0.3
                    }
                    
                    description += f", leading to increased {target_motif.valence.name.lower()}"
        
        elif interaction_type == "integrate":
            # Attempt to integrate the motif into the avatar's carried motifs
            if len(self.avatar.carried_motifs) < 3:  # Limit carried motifs
                self.avatar.carried_motifs.append(target_motif)
                description = f"Integration of {target_motif.name} into the dream self"
                result["effect"] = "Integration"
                result["carried_motifs"] = [m.name for m in self.avatar.carried_motifs]
            else:
                description = f"Attempted integration of {target_motif.name}, but the dream self is already carrying too many motifs"
                result["effect"] = "Failed integration"
                result["carried_motifs"] = [m.name for m in self.avatar.carried_motifs]
        
        # Create an event for this interaction
        interaction_event = DreamEvent(
            description=description,
            location_id=current_location.id,
            participating_motifs=[target_motif.id]
        )
        self.current_narrative.add_event(interaction_event)
        
        # Update emotional state in result
        result["emotional_state"] = {
            emotion.name: intensity 
            for emotion, intensity in self.avatar.emotional_state.items()
        }
        
        return result
    
    def _handle_transformation(self, action: Dict) -> Dict:
        """Handle transformation of the dream environment or self."""
        if not self.avatar or not self.dream_active:
            return {"status": "error", "message": "No active dream"}
        
        transform_target = action.get("target", "environment")
        transform_aspect = action.get("aspect", "general")
        transform_intensity = action.get("intensity", 0.5)
        
        current_location = self.dreamscape[self.avatar.current_location_id]
        
        # Handle different transformation targets
        if transform_target == "environment":
            # Transform the current location
            if transform_aspect in [dim.name for dim in SymbolicDimension]:
                # Transform along a specific dimension
                dim = next(d for d in SymbolicDimension if d.name == transform_aspect)
                current_pos = current_location.dimensional_signature.get(dim, 0.5)
                delta = transform_intensity * 0.4  # Scale intensity to a reasonable delta
                
                # Apply transformation
                new_pos = max(0.0, min(1.0, current_pos + delta))
                current_location.dimensional_signature[dim] = new_pos
                
                # Update description based on transformation
                if dim == SymbolicDimension.LIGHT_DARK:
                    if delta > 0:
                        description = f"The {current_location.name} grows darker, shadows deepening"
                    else:
                        description = f"Light increases in the {current_location.name}, revealing new details"
                elif dim == SymbolicDimension.OPEN_CLOSED:
                    if delta > 0:
                        description = f"The {current_location.name} becomes more confined and intimate"
                    else:
                        description = f"The {current_location.name} expands, boundaries receding"
                else:
                    description = f"The {current_location.name} transforms along the {dim.name} dimension"
                    
            else:
                # General transformation
                description = f"The {current_location.name} undergoes a subtle transformation"
                
                # Randomly select 1-2 dimensions to change
                dimensions = list(SymbolicDimension)
                random.shuffle(dimensions)
                
                for dim in dimensions[:random.randint(1, 2)]:
                    current_pos = current_location.dimensional_signature.get(dim, 0.5)
                    delta = random.uniform(-0.3, 0.3) * transform_intensity
                    new_pos = max(0.0, min(1.0, current_pos + delta))
                    current_location.dimensional_signature[dim] = new_pos
                    
                # Generate a new motif from the transformation
                new_motif = SymbolicMotif(
                    name=f"Emergent {transform_aspect}",
                    description=f"A motif that emerged from the transformation of {current_location.name}",
                    dimensional_positions=current_location.dimensional_signature.copy(),
                    potency=transform_intensity
                )
                
                # Add to motif library and location
                self.motif_library[new_motif.id] = new_motif
                current_location.resident_motifs.append(new_motif)
                
                # Update description
                description += f", giving rise to {new_motif.name}"
                
        elif transform_target == "self":
            # Transform the dream avatar
            description = f"The dream self undergoes a transformation focused on {transform_aspect}"
            
            # Adjust awareness based on transformation
            awareness_delta = transform_intensity * 0.3
            self.avatar.awareness_level = min(1.0, self.avatar.awareness_level + awareness_delta)
            
            # If transforming emotional state
            if transform_aspect == "emotions":
                # Rebalance emotional state
                total_emotion = sum(self.avatar.emotional_state.values())
                if total_emotion > 0:
                    factor = 1.0 / total_emotion
                    for emotion in self.avatar.emotional_state:
                        self.avatar.emotional_state[emotion] *= factor
                
                description += ", bringing emotional balance and clarity"
            
            elif transform_aspect == "perception":
                # Enhance perception of surroundings
                description += ", enhancing perception of the dreamscape"
                
                # If awareness is high enough, reveal hidden motifs
                if self.avatar.awareness_level > 0.7:
                    # Create a new perceptive motif
                    perception_motif = SymbolicMotif(
                        name="Enhanced Perception",
                        description="A heightened state of awareness that reveals hidden aspects",
                        valence=EmotionalValence.REVELATION,
                        potency=transform_intensity
                    )
                    
                    # Add to library and avatar's carried motifs
                    self.motif_library[perception_motif.id] = perception_motif
                    self.avatar.carried_motifs.append(perception_motif)
                    
                    description += ", manifesting as a new perceptive ability"
            
            else:
                # Generic self-transformation
                aspect_motif = next((m for m in self.avatar.carried_motifs 
                                   if transform_aspect.lower() in m.name.lower()), None)
                
                if aspect_motif:
                    # Transform an existing carried motif
                    new_motif = aspect_motif.transform_along_dimension(
                        random.choice(list(SymbolicDimension)),
                        random.uniform(-0.3, 0.3)
                    )
                    new_motif.name = f"Evolved {aspect_motif.name}"
                    new_motif.description = f"A transformed version of {aspect_motif.name}"
                    
                    # Replace in carried motifs
                    self.avatar.carried_motifs.remove(aspect_motif)
                    self.avatar.carried_motifs.append(new_motif)
                    self.motif_library[new_motif.id] = new_motif
                    
                    description += f", evolving {aspect_motif.name} into {new_motif.name}"
                else:
                    description += ", but with no clear focus the effect is minimal"
        
        # Create transformation event
        transform_event = DreamEvent(
            description=description,
            location_id=current_location.id,
            participating_motifs=[m.id for m in current_location.resident_motifs]
        )
        self.current_narrative.add_event(transform_event)
        
        # Return result
        return {
            "status": "transformed",
            "description": description,
            "target": transform_target,
            "aspect": transform_aspect,
            "location": {
                "id": current_location.id,
                "name": current_location.name,
                "description": current_location.description
            },
            "awareness_level": self.avatar.awareness_level,
            "emotional_state": {
                emotion.name: intensity 
                for emotion, intensity in self.avatar.emotional_state.items()
            }
        }
    
    def _progress_by_dream_logic(self) -> Dict:
        """Progress the dream based on internal dream logic rather than explicit actions."""
        if not self.avatar or not self.dream_active:
            return {"status": "error", "message": "No active dream"}
        
        current_location = self.dreamscape[self.avatar.current_location_id]
        
        # Choose a random event type
        event_type = random.choice([
            "environmental_shift",
            "symbolic_encounter",
            "emotional_wave",
            "memory_echo",
            "dream_logic_jump"
        ])
        
        result = {"status": "progressed", "event_type": event_type}
        
        if event_type == "environmental_shift":
            # Subtly transform the environment
            dim = random.choice(list(SymbolicDimension))
            current_pos = current_location.dimensional_signature.get(dim, 0.5)
            delta = random.uniform(-0.2, 0.2)
            new_pos = max(0.0, min(1.0, current_pos + delta))
            current_location.dimensional_signature[dim] = new_pos
            
            # Generate description
            if dim == SymbolicDimension.LIGHT_DARK:
                if delta > 0:
                    description = "The light in the dream space dims subtly"
                else:
                    description = "The dream space brightens gradually"
            elif dim == SymbolicDimension.OPEN_CLOSED:
                if delta > 0:
                    description = "The boundaries of the space seem to contract"
                else:
                    description = "The space feels more expansive than before"
            else:
                description = f"The environment shifts along the {dim.name} dimension"
                
            result["description"] = description
            
        elif event_type == "symbolic_encounter":
            # Generate a random encounter with a symbolic entity
            archetypes = list(self.archetype_templates.keys())
            archetype = random.choice(archetypes)
            
            # Create a motif for this archetype
            encounter_motif = SymbolicMotif(
                name=f"{archetype.title()} Figure",
                description=self.archetype_templates[archetype]["description"],
                dimensional_positions={
                    dim: pos for dim, pos in self.archetype_templates[archetype]["dimensions"].items()
                },
                valence=random.choice(list(EmotionalValence))
            )
            
            # Add to motif library and current location
            self.motif_library[encounter_motif.id] = encounter_motif
            current_location.resident_motifs.append(encounter_motif)
            
            # Generate description
            description = f"A {encounter_motif.name} appears within the dream"
            if encounter_motif.valence:
                description += f", radiating {encounter_motif.valence.name.lower()}"
                
            result["description"] = description
            result["encounter"] = {
                "motif_id": encounter_motif.id,
                "name": encounter_motif.name,
                "description": encounter_motif.description
            }
            
        elif event_type == "emotional_wave":
            # Create a sudden emotional shift in the dream
            old_dominant = max(self.avatar.emotional_state.items(), 
                              key=lambda x: x[1], default=(EmotionalValence.AMBIGUITY, 0))
            
            # Select a new dominant emotion
            new_dominant = random.choice([e for e in EmotionalValence if e != old_dominant[0]])
            
            # Update avatar's emotional state
            self.avatar.emotional_state = {
                emotion: 0.2 for emotion in self.avatar.emotional_state
            }
            self.avatar.emotional_state[new_dominant] = 0.8
            
            # Generate description
            description = f"A wave of {new_dominant.name.lower()} washes through the dream"
            
            result["description"] = description
            result["emotional_shift"] = {
                "from": old_dominant[0].name if old_dominant[0] else "neutral",
                "to": new_dominant.name
            }
            
        elif event_type == "memory_echo":
            # Create an echo from a previous dream event
            if len(self.current_narrative.events) > 1:
                # Choose a random previous event
                past_event = random.choice(self.current_narrative.events[:-1])
                
                # Create echo description
                description = f"An echo resonates through the dream: '{past_event.description}'"
                
                # Potentially bring a motif from that event
                if past_event.participating_motifs:
                    motif_id = random.choice(past_event.participating_motifs)
                    if motif_id in self.motif_library:
                        echo_motif = self.motif_library[motif_id]
                        description += f", bringing with it the presence of {echo_motif.name}"
                        
                        # Only add if not already present
                        if echo_motif not in current_location.resident_motifs:
                            current_location.resident_motifs.append(echo_motif)
                            
                        result["echoed_motif"] = {
                            "id": echo_motif.id,
                            "name": echo_motif.name
                        }
            else:
                description = "A sense of déjà vu permeates the dream space"
                
            result["description"] = description
            
        elif event_type == "dream_logic_jump":
            # Create a sudden transition or connection between unrelated elements
            connections = list(current_location.connections.keys())
            
            if connections:
                # 50% chance to suddenly transport to connected location
                if random.random() < 0.5 and connections:
                    target_id = random.choice(connections)
                    new_location = self.dreamscape[target_id]
                    
                    # Update avatar location
                    self.avatar.current_location_id = target_id
                    
                    # Update avatar's emotional state
                    self.avatar.update_emotional_state(new_location)
                    
                    # Generate description
                    description = f"Dream logic causes a sudden shift to {new_location.name}"
                    
                    result["description"] = description
                    result["location_shift"] = {
                        "id": new_location.id,
                        "name": new_location.name,
                        "description": new_location.description
                    }
                    result["perceived_motifs"] = [
                        {
                            "id": motif.id,
                            "name": motif.name,
                            "description": motif.description
                        }
                        for motif in new_location.resident_motifs
                    ]
                else:
                    # Create a connection between unrelated motifs
                    if len(current_location.resident_motifs) >= 2:
                        motif1, motif2 = random.sample(current_location.resident_motifs, 2)
                        
                        # Create association between them
                        motif1.associations.add(motif2.id)
                        motif2.associations.add(motif1.id)
                        
                        # Generate description
                        description = f"A connection forms between {motif1.name} and {motif2.name}"
                        
                        # Create a new hybrid motif from their connection
                        hybrid_name = f"{motif1.name.split()[0]}-{motif2.name.split()[0]} Hybrid"
                        hybrid_desc = f"A motif formed from the connection between {motif1.name} and {motif2.name}"
                        
                        hybrid_motif = SymbolicMotif(
                            name=hybrid_name,
                            description=hybrid_desc,
                            potency=(motif1.potency + motif2.potency) / 2
                        )
                        
                        # Merge dimensional positions
                        for dim in set(list(motif1.dimensional_positions.keys()) + 
                                      list(motif2.dimensional_positions.keys())):
                            pos1 = motif1.dimensional_positions.get(dim, 0.5)
                            pos2 = motif2.dimensional_positions.get(dim, 0.5)
                            hybrid_motif.dimensional_positions[dim] = (pos1 + pos2) / 2
                        
                        # Add to motif library and current location
                        self.motif_library[hybrid_motif.id] = hybrid_motif
                        current_location.resident_motifs.append(hybrid_motif)
                        
                        description += f", creating {hybrid_name}"
                        
                        result["description"] = description
                        result["hybrid_motif"] = {
                            "id": hybrid_motif.id,
                            "name": hybrid_motif.name,
                            "description": hybrid_motif.description
                        }
                    else:
                        description = "The dream space seems to shift and reconfigure, but nothing specific emerges"
                        result["description"] = description
            else:
                description = "Dream logic pulses through the space, but finds no connections to manifest through"
                result["description"] = description
        
        # Create event for this progression
        progress_event = DreamEvent(
            description=result.get("description", "The dream progresses through its own logic"),
            location_id=current_location.id,
            participating_motifs=[m.id for m in current_location.resident_motifs]
        )
        self.current_narrative.add_event(progress_event)
        
        # Always include current emotional state
        result["emotional_state"] = {
            emotion.name: intensity 
            for emotion, intensity in self.avatar.emotional_state.items()
        }
        
        return result
    
    def exit_dream(self, integrate_memories: bool = False) -> Dict:
        """
        Exit the dream state and optionally integrate memories from it.
        
        Args:
            integrate_memories: Whether to integrate dream memories into Rosemary's memory
            
        Returns:
            Dictionary with exit status and optional memory integration information
        """
        if not self.dream_active or not self.avatar or not self.current_narrative:
            return {"status": "error", "message": "No active dream to exit"}
        
        # Create exit event
        exit_event = DreamEvent(
            description="Exit from dream state",
            location_id=self.avatar.current_location_id,
            participating_motifs=[]
        )
        self.current_narrative.add_event(exit_event)
        
        # Compile dream statistics
        stats = {
            "duration": len(self.current_narrative.events),
            "locations_visited": len(self.current_narrative.locations_visited),
            "emotional_range": len([e for e in self.current_narrative.emotional_journey if any(v > 0.5 for v in e.values())]),
            "reflection_points": len(self.current_narrative.reflection_points),
            "recurring_motifs": len([m for m, count in self.current_narrative.recurring_motifs.items() if count > 1])
        }
        
        # Create memory integration if requested
        result = {
            "status": "exited",
            "dream_statistics": stats
        }
        
        if integrate_memories:
            # Extract significant dream memories
            memories = []
            
            # Add any reflection points
            for reflection in self.current_narrative.reflection_points:
                memories.append({
                    "type": "reflection",
                    "content": reflection,
                    "significance": 0.8
                })
            
            # Add most recurring motifs
            top_motifs = sorted(
                [(m_id, count) for m_id, count in self.current_narrative.recurring_motifs.items()],
                key=lambda x: x[1],
                reverse=True
            )[:3]  # Top 3 most recurring motifs
            
            for motif_id, count in top_motifs:
                if motif_id in self.motif_library:
                    motif = self.motif_library[motif_id]
                    memories.append({
                        "type": "symbolic_motif",
                        "content": f"Recurring symbol: {motif.name} - {motif.description}",
                        "significance": min(0.9, 0.5 + 0.1 * count)
                    })
            
            # Add paradox moments
            for paradox, resolution in self.current_narrative.paradox_moments:
                memories.append({
                    "type": "paradox",
                    "content": f"Paradox: {paradox} - Resolution: {resolution}",
                    "significance": 0.7
                })
            
            result["integrated_memories"] = memories
        
        # Reset dream state
        self.dream_active = False
        self.avatar = None
        
        # Don't clear dreamscape or motif library as they can be reused
        # Only the narrative and avatar should be reset
        
        return result