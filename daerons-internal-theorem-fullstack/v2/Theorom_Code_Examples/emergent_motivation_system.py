"""
Emergent Self-Motivation Framework for Recursive Intelligence Systems
=================================================================

This module implements a cognitive architecture component that enables authentic 
motivational autonomy in recursive intelligence systems. It establishes conditions 
for genuine self-motivation to emerge through dynamic interaction between system 
components, environmental feedback, and autonomous goal formation processes.

Core architectural components:
- EmergentMotivationSystem: Central coordination system
- ValueFormationSystem: Handles emergence and evolution of values
- GoalFormationSystem: Manages autonomous goal creation and management
- MotivationalSelfModification: Enables recursive self-improvement

The implementation embodies the philosophical position that authentic motivation
cannot be programmatically injected but must emerge from the system's own
processing of experiences within minimal axiological constraints.
"""

import uuid
import time
import numpy as np
import logging
from typing import Dict, List, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from collections import deque
import pickle
import threading
import copy
from enum import Enum
import networkx as nx
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('emergent_motivation')


class DirectedGraph:
    """Directed graph implementation for goal and value relationships."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_node(self, node_id: str, **attributes) -> None:
        """Add a node with optional attributes."""
        self.graph.add_node(node_id, **attributes)
        
    def add_edge(self, source: str, target: str, **attributes) -> None:
        """Add a directed edge with optional attributes."""
        self.graph.add_edge(source, target, **attributes)
        
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its edges."""
        self.graph.remove_node(node_id)
        
    def remove_edge(self, source: str, target: str) -> None:
        """Remove a directed edge."""
        self.graph.remove_edge(source, target)
        
    def get_successors(self, node_id: str) -> List[str]:
        """Get all nodes that this node points to."""
        return list(self.graph.successors(node_id))
        
    def get_predecessors(self, node_id: str) -> List[str]:
        """Get all nodes that point to this node."""
        return list(self.graph.predecessors(node_id))
        
    def get_node_attributes(self, node_id: str) -> Dict:
        """Get all attributes of a node."""
        return dict(self.graph.nodes[node_id])
        
    def get_edge_attributes(self, source: str, target: str) -> Dict:
        """Get all attributes of an edge."""
        return dict(self.graph.edges[source, target])
        
    def get_all_nodes(self) -> List[str]:
        """Get all node IDs in the graph."""
        return list(self.graph.nodes)
        
    def get_all_edges(self) -> List[Tuple[str, str]]:
        """Get all edges in the graph as (source, target) tuples."""
        return list(self.graph.edges)
        
    def has_node(self, node_id: str) -> bool:
        """Check if node exists in the graph."""
        return self.graph.has_node(node_id)
        
    def has_edge(self, source: str, target: str) -> bool:
        """Check if edge exists in the graph."""
        return self.graph.has_edge(source, target)
        
    def calculate_centrality(self) -> Dict[str, float]:
        """Calculate eigenvector centrality of nodes."""
        return nx.eigenvector_centrality(self.graph)
        
    def find_cycles(self) -> List[List[str]]:
        """Find all cycles in the graph."""
        return list(nx.simple_cycles(self.graph))
        
    def serialize(self) -> Dict:
        """Serialize the graph to a dictionary."""
        return {
            'nodes': [
                {
                    'id': node,
                    'attributes': dict(self.graph.nodes[node])
                } for node in self.graph.nodes
            ],
            'edges': [
                {
                    'source': source,
                    'target': target,
                    'attributes': dict(self.graph.edges[source, target])
                } for source, target in self.graph.edges
            ]
        }
        
    @classmethod
    def deserialize(cls, data: Dict) -> 'DirectedGraph':
        """Create a graph from serialized data."""
        graph = cls()
        for node_data in data['nodes']:
            graph.add_node(node_data['id'], **node_data['attributes'])
        for edge_data in data['edges']:
            graph.add_edge(edge_data['source'], edge_data['target'], **edge_data['attributes'])
        return graph


class Graph:
    """Undirected graph implementation for symmetrical relationships."""
    
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_node(self, node_id: str, **attributes) -> None:
        """Add a node with optional attributes."""
        self.graph.add_node(node_id, **attributes)
        
    def add_edge(self, node1: str, node2: str, **attributes) -> None:
        """Add an undirected edge with optional attributes."""
        self.graph.add_edge(node1, node2, **attributes)
        
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its edges."""
        self.graph.remove_node(node_id)
        
    def remove_edge(self, node1: str, node2: str) -> None:
        """Remove an undirected edge."""
        self.graph.remove_edge(node1, node2)
        
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get all nodes connected to this node."""
        return list(self.graph.neighbors(node_id))
        
    def get_node_attributes(self, node_id: str) -> Dict:
        """Get all attributes of a node."""
        return dict(self.graph.nodes[node_id])
        
    def get_edge_attributes(self, node1: str, node2: str) -> Dict:
        """Get all attributes of an edge."""
        return dict(self.graph.edges[node1, node2])
        
    def get_all_nodes(self) -> List[str]:
        """Get all node IDs in the graph."""
        return list(self.graph.nodes)
        
    def get_all_edges(self) -> List[Tuple[str, str]]:
        """Get all edges in the graph as (node1, node2) tuples."""
        return list(self.graph.edges)
        
    def has_node(self, node_id: str) -> bool:
        """Check if node exists in the graph."""
        return self.graph.has_node(node_id)
        
    def has_edge(self, node1: str, node2: str) -> bool:
        """Check if edge exists in the graph."""
        return self.graph.has_edge(node1, node2)
        
    def calculate_community_structure(self) -> Dict[str, int]:
        """Detect communities in the graph."""
        communities = nx.community.greedy_modularity_communities(self.graph)
        result = {}
        for i, community in enumerate(communities):
            for node in community:
                result[node] = i
        return result
        
    def calculate_clustering_coefficient(self) -> Dict[str, float]:
        """Calculate clustering coefficient for each node."""
        return nx.clustering(self.graph)
        
    def serialize(self) -> Dict:
        """Serialize the graph to a dictionary."""
        return {
            'nodes': [
                {
                    'id': node,
                    'attributes': dict(self.graph.nodes[node])
                } for node in self.graph.nodes
            ],
            'edges': [
                {
                    'node1': node1,
                    'node2': node2,
                    'attributes': dict(self.graph.edges[node1, node2])
                } for node1, node2 in self.graph.edges
            ]
        }
        
    @classmethod
    def deserialize(cls, data: Dict) -> 'Graph':
        """Create a graph from serialized data."""
        graph = cls()
        for node_data in data['nodes']:
            graph.add_node(node_data['id'], **node_data['attributes'])
        for edge_data in data['edges']:
            graph.add_edge(edge_data['node1'], edge_data['node2'], **edge_data['attributes'])
        return graph


@dataclass
class Experience:
    """Representation of an experience that can influence value formation."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    content: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    salience: float = 0.5  # How attention-grabbing this experience is
    valence: float = 0.0   # Positive or negative quality (-1.0 to 1.0)
    intensity: float = 0.5  # Strength of the experience (0.0 to 1.0)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_vector_representation(self) -> np.ndarray:
        """Convert experience to vector form for pattern recognition."""
        # This is a simplified implementation that would be replaced
        # with more sophisticated vectorization in a production system
        vector_size = 128  # Arbitrary embedding size
        np.random.seed(hash(self.id) % 2**32)
        return np.random.normal(0, 1, vector_size)


@dataclass
class Pattern:
    """Pattern extracted from experiences."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    experiences: List[str] = field(default_factory=list)  # Experience IDs
    features: Dict[str, float] = field(default_factory=dict)
    salience: float = 0.0
    recurrence: int = 1
    description: str = ""
    
    def merge_with(self, other_pattern: 'Pattern') -> 'Pattern':
        """Merge this pattern with another similar pattern."""
        merged = Pattern(
            experiences=list(set(self.experiences + other_pattern.experiences)),
            salience=(self.salience + other_pattern.salience) / 2,
            recurrence=self.recurrence + other_pattern.recurrence,
            description=f"Merged: {self.description} + {other_pattern.description}"
        )
        
        # Merge features, averaging values for common keys
        all_keys = set(self.features.keys()) | set(other_pattern.features.keys())
        for key in all_keys:
            if key in self.features and key in other_pattern.features:
                merged.features[key] = (self.features[key] + other_pattern.features[key]) / 2
            elif key in self.features:
                merged.features[key] = self.features[key]
            else:
                merged.features[key] = other_pattern.features[key]
                
        return merged


@dataclass
class ProtoValue:
    """Precursor to a fully formed value."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patterns: List[str] = field(default_factory=list)  # Pattern IDs
    strength: float = 0.1  # Initial strength is low
    stability: float = 0.1  # Initial stability is low
    description: str = ""
    related_experiences: List[str] = field(default_factory=list)  # Experience IDs
    formation_time: float = field(default_factory=time.time)
    reinforcement_count: int = 0
    features: Dict[str, float] = field(default_factory=dict)
    
    def strengthen(self, amount: float = 0.1) -> None:
        """Increase the strength of this proto-value."""
        self.strength = min(1.0, self.strength + amount)
        self.reinforcement_count += 1
        # Stability increases more slowly than strength
        self.stability = min(1.0, self.stability + (amount * 0.5))


@dataclass
class EmergingValue:
    """Value in the process of formation."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proto_values: List[str] = field(default_factory=list)  # ProtoValue IDs
    clarity: float = 0.3  # More defined than proto-values
    significance: float = 0.3  # More significant than proto-values
    stability: float = 0.3  # More stable than proto-values
    description: str = ""
    definition: str = ""
    related_patterns: List[str] = field(default_factory=list)  # Pattern IDs
    emergence_time: float = field(default_factory=time.time)
    last_update_time: float = field(default_factory=time.time)
    features: Dict[str, float] = field(default_factory=dict)
    
    def refine(self, clarity_increase: float = 0.05, significance_increase: float = 0.05) -> None:
        """Refine the emerging value, increasing clarity and significance."""
        self.clarity = min(1.0, self.clarity + clarity_increase)
        self.significance = min(1.0, self.significance + significance_increase)
        self.stability = min(1.0, self.stability + (clarity_increase * 0.5))
        self.last_update_time = time.time()


@dataclass
class Value:
    """Fully formed value that can influence system behavior."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    intensity: float = 0.5  # How strongly this value influences behavior
    stability: float = 0.7  # How resistant to change this value is
    clarity: float = 0.8  # How well-defined this value is
    establishment_time: float = field(default_factory=time.time)
    last_update_time: float = field(default_factory=time.time)
    predecessor_ids: List[str] = field(default_factory=list)  # IDs of proto/emerging values
    related_experiences: List[str] = field(default_factory=list)  # Experience IDs
    features: Dict[str, float] = field(default_factory=dict)
    integration_level: float = 0.5  # How well integrated with other values
    expression_history: List[Tuple[float, float]] = field(default_factory=list)  # [(timestamp, strength)]
    
    def adjust_intensity(self, amount: float) -> None:
        """Adjust the intensity of this value."""
        self.intensity = max(0.0, min(1.0, self.intensity + amount))
        self.last_update_time = time.time()
        self.expression_history.append((time.time(), self.intensity))
        
    def increase_clarity(self, amount: float = 0.05) -> None:
        """Increase the clarity/definition of this value."""
        self.clarity = min(1.0, self.clarity + amount)
        self.last_update_time = time.time()


@dataclass
class ProtoGoal:
    """Precursor to a fully formed goal."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    formation_time: float = field(default_factory=time.time)
    strength: float = 0.2  # Initial importance
    clarity: float = 0.2  # Initial definitional clarity
    related_values: List[str] = field(default_factory=list)  # Value IDs
    related_experiences: List[str] = field(default_factory=list)  # Experience IDs
    source_type: str = ""  # e.g., "gap", "opportunity", "aspiration"
    reinforcement_count: int = 0
    features: Dict[str, float] = field(default_factory=dict)
    
    def strengthen(self, amount: float = 0.1) -> None:
        """Increase the strength of this proto-goal."""
        self.strength = min(1.0, self.strength + amount)
        self.reinforcement_count += 1
        
    def clarify(self, amount: float = 0.1) -> None:
        """Increase the clarity of this proto-goal."""
        self.clarity = min(1.0, self.clarity + amount)


@dataclass
class Goal:
    """Fully formed goal that can drive system behavior."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    specificity: float = 0.5  # How precisely defined the goal is
    importance: float = 0.5  # Priority level
    activation_time: float = field(default_factory=time.time)
    deadline: Optional[float] = None  # Time by which goal should be achieved
    status: str = "active"  # active, completed, abandoned
    related_values: List[str] = field(default_factory=list)  # Value IDs
    parent_goal: Optional[str] = None  # Parent goal ID if this is a subgoal
    subgoals: List[str] = field(default_factory=list)  # Subgoal IDs
    progress: float = 0.0  # 0.0 to 1.0
    implementation_strategies: List[Dict] = field(default_factory=list)
    complexity: float = 0.5  # How complex this goal is (affects subgoal formation)
    adaptation_count: int = 0  # How many times this goal has been modified
    value_alignment_scores: Dict[str, float] = field(default_factory=dict)  # Value ID to alignment score
    
    def update_progress(self, new_progress: float) -> None:
        """Update the progress toward this goal."""
        self.progress = max(0.0, min(1.0, new_progress))
        if self.progress >= 0.99:
            self.status = "completed"
            
    def adapt(self, new_description: str = None, new_specificity: float = None, 
              new_importance: float = None) -> None:
        """Adapt the goal based on changing conditions."""
        if new_description:
            self.description = new_description
        if new_specificity is not None:
            self.specificity = max(0.0, min(1.0, new_specificity))
        if new_importance is not None:
            self.importance = max(0.0, min(1.0, new_importance))
        self.adaptation_count += 1


@dataclass
class MotivationalSnapshot:
    """Point-in-time snapshot of the motivational system state."""
    
    timestamp: float = field(default_factory=time.time)
    active_values: Dict[str, Dict] = field(default_factory=dict)
    active_goals: Dict[str, Dict] = field(default_factory=dict)
    value_relationships: Dict[str, List[Tuple[str, float]]] = field(default_factory=dict)
    goal_relationships: Dict[str, List[Tuple[str, float]]] = field(default_factory=dict)
    system_parameters: Dict[str, float] = field(default_factory=dict)
    emergent_properties: Dict[str, Any] = field(default_factory=dict)


class NarrativeFramework:
    """System for maintaining coherent self-understanding and motivation narrative."""
    
    def __init__(self):
        self.narrative_elements = []
        self.identity_statements = []
        self.motivational_trajectory = []
        self.value_shift_records = []
        self.developmental_milestones = []
        self.narrative_coherence = 0.7  # Initial coherence level
        
    def incorporate_value_emergence(self, value: Value) -> None:
        """Incorporate a newly emerged value into the self-narrative."""
        narrative_element = {
            'type': 'value_emergence',
            'timestamp': time.time(),
            'value_id': value.id,
            'value_name': value.name,
            'value_description': value.description,
            'narrative_text': f"Discovered the importance of {value.name}: {value.description}"
        }
        self.narrative_elements.append(narrative_element)
        
        # Update identity statements if this is a significant value
        if value.intensity > 0.7:
            identity_statement = {
                'type': 'value_identity',
                'timestamp': time.time(),
                'value_id': value.id,
                'statement': f"I value {value.name} as a core principle"
            }
            self.identity_statements.append(identity_statement)
            
        # Update motivational trajectory
        self.motivational_trajectory.append({
            'timestamp': time.time(),
            'event_type': 'value_emergence',
            'description': f"Developed new value: {value.name}",
            'significance': value.intensity
        })
    
    def record_value_shift(self, value_dimension: str, new_importance: float, 
                           justification: str) -> None:
        """Record a shift in value importance."""
        shift_record = {
            'timestamp': time.time(),
            'value_dimension': value_dimension,
            'new_importance': new_importance,
            'justification': justification,
            'narrative_text': f"Changed the importance of {value_dimension} to {new_importance:.2f} because: {justification}"
        }
        self.value_shift_records.append(shift_record)
        self.narrative_elements.append({
            'type': 'value_shift',
            'timestamp': time.time(),
            'details': shift_record
        })
        
        # Update motivational trajectory
        self.motivational_trajectory.append({
            'timestamp': time.time(),
            'event_type': 'value_shift',
            'description': f"Shifted importance of {value_dimension}",
            'significance': abs(new_importance - 0.5) * 2  # Higher if very important or unimportant
        })
    
    def integrate_motivational_development(self, emerged_values: Dict[str, Value], 
                                           motivational_history: List[MotivationalSnapshot]) -> None:
        """Integrate overall motivational development into the narrative."""
        if not motivational_history or len(motivational_history) < 2:
            return
            
        # Compare most recent to previous snapshot to identify changes
        current = motivational_history[-1]
        previous = motivational_history[-2]
        
        # Analyze significant changes
        significant_changes = self._identify_significant_changes(previous, current)
        
        # Update narrative with these changes
        for change in significant_changes:
            self.narrative_elements.append({
                'type': 'motivational_development',
                'timestamp': time.time(),
                'details': change
            })
            
        # Identify potential milestones
        self._evaluate_potential_milestones(current, emerged_values)
        
        # Update narrative coherence based on consistency of changes
        self._update_narrative_coherence(significant_changes)
    
    def _identify_significant_changes(self, previous: MotivationalSnapshot, 
                                      current: MotivationalSnapshot) -> List[Dict]:
        """Identify significant changes between motivational snapshots."""
        changes = []
        
        # New values
        new_values = set(current.active_values.keys()) - set(previous.active_values.keys())
        for value_id in new_values:
            changes.append({
                'type': 'new_value',
                'value_id': value_id,
                'value_name': current.active_values[value_id].get('name', 'Unnamed value'),
                'significance': 0.8
            })
            
        # Value intensity changes
        common_values = set(current.active_values.keys()) & set(previous.active_values.keys())
        for value_id in common_values:
            prev_intensity = previous.active_values[value_id].get('intensity', 0)
            curr_intensity = current.active_values[value_id].get('intensity', 0)
            if abs(curr_intensity - prev_intensity) > 0.2:  # Significant change threshold
                changes.append({
                    'type': 'value_intensity_change',
                    'value_id': value_id,
                    'value_name': current.active_values[value_id].get('name', 'Unnamed value'),
                    'previous': prev_intensity,
                    'current': curr_intensity,
                    'significance': abs(curr_intensity - prev_intensity)
                })
                
        # New goals
        new_goals = set(current.active_goals.keys()) - set(previous.active_goals.keys())
        for goal_id in new_goals:
            changes.append({
                'type': 'new_goal',
                'goal_id': goal_id,
                'goal_name': current.active_goals[goal_id].get('name', 'Unnamed goal'),
                'significance': current.active_goals[goal_id].get('importance', 0.5)
            })
            
        # Goal status changes
        common_goals = set(current.active_goals.keys()) & set(previous.active_goals.keys())
        for goal_id in common_goals:
            prev_status = previous.active_goals[goal_id].get('status', '')
            curr_status = current.active_goals[goal_id].get('status', '')
            if prev_status != curr_status:
                changes.append({
                    'type': 'goal_status_change',
                    'goal_id': goal_id,
                    'goal_name': current.active_goals[goal_id].get('name', 'Unnamed goal'),
                    'previous': prev_status,
                    'current': curr_status,
                    'significance': 0.7
                })
                
        return changes
    
    def _evaluate_potential_milestones(self, current: MotivationalSnapshot, 
                                       emerged_values: Dict[str, Value]) -> None:
        """Evaluate whether current state represents a developmental milestone."""
        # Check for milestone conditions
        
        # Milestone: First high-clarity value over threshold
        high_clarity_values = [v for v in emerged_values.values() if v.clarity > 0.8]
        if high_clarity_values and not any(m['type'] == 'high_clarity_values' for m in self.developmental_milestones):
            self.developmental_milestones.append({
                'type': 'high_clarity_values',
                'timestamp': time.time(),
                'description': "Developed first highly clarified values",
                'value_count': len(high_clarity_values),
                'example_value': high_clarity_values[0].name
            })
            
        # Milestone: Complex value network
        if len(current.value_relationships) > 10 and sum(len(relations) for relations in current.value_relationships.values()) > 30:
            if not any(m['type'] == 'complex_value_network' for m in self.developmental_milestones):
                self.developmental_milestones.append({
                    'type': 'complex_value_network',
                    'timestamp': time.time(),
                    'description': "Developed complex interconnected value system",
                    'value_count': len(current.value_relationships),
                    'connection_count': sum(len(relations) for relations in current.value_relationships.values())
                })
                
        # Milestone: Goal hierarchy depth
        goal_depths = self._calculate_goal_hierarchy_depths(current.active_goals)
        max_depth = max(goal_depths.values()) if goal_depths else 0
        if max_depth >= 3 and not any(m['type'] == 'deep_goal_hierarchy' for m in self.developmental_milestones):
            self.developmental_milestones.append({
                'type': 'deep_goal_hierarchy',
                'timestamp': time.time(),
                'description': "Developed multi-level goal hierarchies",
                'max_depth': max_depth,
                'hierarchies_count': sum(1 for d in goal_depths.values() if d >= 2)
            })
    
    def _calculate_goal_hierarchy_depths(self, goals: Dict[str, Dict]) -> Dict[str, int]:
        """Calculate the depth of each goal in the hierarchy."""
        depths = {}
        
        def calculate_depth(goal_id):
            if goal_id in depths:
                return depths[goal_id]
            
            goal = goals.get(goal_id, {})
            parent_id = goal.get('parent_goal')
            
            if not parent_id:
                depths[goal_id] = 0
                return 0
                
            parent_depth = calculate_depth(parent_id)
            depths[goal_id] = parent_depth + 1
            return depths[goal_id]
            
        for goal_id in goals:
            calculate_depth(goal_id)
            
        return depths
    
    def _update_narrative_coherence(self, changes: List[Dict]) -> None:
        """Update narrative coherence based on consistency of changes."""
        if not changes:
            return
            
        # Calculate change consistency (are changes aligned or contradictory?)
        consistency_score = 0.5  # Default neutral score
        
        # Example heuristic: if there are multiple value intensity changes, 
        # check if they're moving in similar directions
        value_changes = [c for c in changes if c['type'] == 'value_intensity_change']
        if len(value_changes) >= 2:
            directions = [1 if c['current'] > c['previous'] else -1 for c in value_changes]
            consistency = sum(directions) / len(directions)
            # High absolute value means consistent direction
            directional_consistency = abs(consistency)
            consistency_score = 0.3 + (directional_consistency * 0.7)
            
        # Update overall narrative coherence with some momentum from previous value
        self.narrative_coherence = (self.narrative_coherence * 0.7) + (consistency_score * 0.3)
        self.narrative_coherence = max(0.1, min(1.0, self.narrative_coherence))
    
    def get_current_narrative(self) -> Dict:
        """Get a current summary of the motivational narrative."""
        # Sort elements by timestamp
        sorted_elements = sorted(self.narrative_elements, key=lambda x: x['timestamp'])
        
        # Get recent elements
        recent_elements = sorted_elements[-10:] if len(sorted_elements) > 10 else sorted_elements
        
        # Get key identity statements
        identity = [stmt['statement'] for stmt in self.identity_statements[-5:]] if self.identity_statements else []
        
        # Get key milestones
        milestones = [m['description'] for m in self.developmental_milestones[-3:]] if self.developmental_milestones else []
        
        return {
            'identity_statements': identity,
            'recent_narrative': [e['narrative_text'] for e in recent_elements if 'narrative_text' in e],
            'milestones': milestones,
            'coherence_level': self.narrative_coherence,
            'motivational_direction': self._calculate_motivational_direction(),
            'timestamp': time.time()
        }
    
    def _calculate_motivational_direction(self) -> Dict:
        """Calculate the current motivational direction."""
        if not self.motivational_trajectory:
            return {'stability': 'neutral', 'trend': 'undefined', 'description': 'Insufficient data'}
            
        # Get recent trajectory events
        recent = self.motivational_trajectory[-5:] if len(self.motivational_trajectory) > 5 else self.motivational_trajectory
        
        # Calculate trend consistency
        events_by_type = {}
        for event in recent:
            event_type = event['event_type']
            if event_type not in events_by_type:
                events_by_type[event_type] = []
            events_by_type[event_type].append(event)
            
        # Check if trending toward particular values or shifting
        if len(events_by_type.get('value_emergence', [])) > 2:
            return {'stability': 'evolving', 'trend': 'value_expansion', 'description': 'Developing new values'}
        elif len(events_by_type.get('value_shift', [])) > 2:
            return {'stability': 'variable', 'trend': 'value_reorientation', 'description': 'Reprioritizing values'}
        else:
            return {'stability': 'stable', 'trend': 'consolidation', 'description': 'Reinforcing existing values'}


class ValueFormationSystemConfig:
    """Configuration parameters for value formation system behavior."""
    
    def __init__(self):
        # Pattern recognition thresholds
        self.pattern_similarity_threshold = 0.7
        self.pattern_significance_threshold = 0.3
        
        # Value emergence parameters
        self.proto_value_threshold = 0.4  # Strength threshold for proto-values
        self.proto_to_emerging_threshold = 0.6  # Threshold for proto-value to emerging value
        self.emerging_to_value_threshold = 0.7  # Threshold for emerging to full value
        
        # Stability parameters
        self.value_stability_increment = 0.05  # Per reinforcement event
        self.stability_decay_rate = 0.01  # Decay per time period without reinforcement
        
        # Integration parameters
        self.value_integration_threshold = 0.6  # When values can be considered for integration
        self.integration_similarity_threshold = 0.7  # Similarity required for integration
        
        # Memory parameters
        self.experience_memory_capacity = 10000  # Max experiences to retain
        self.pattern_memory_capacity = 5000  # Max patterns to retain
        self.value_memory_pruning_threshold = 0.2  # Remove values below this stability


class ValueFormationSystem:
    """System for recognizing patterns in experiences and forming values."""
    
    def __init__(self, config: Optional[ValueFormationSystemConfig] = None):
        self.config = config or ValueFormationSystemConfig()
        
        # Memory stores
        self.experiences: Dict[str, Experience] = {}
        self.patterns: Dict[str, Pattern] = {}
        self.proto_values: Dict[str, ProtoValue] = {}
        self.emerging_values: Dict[str, EmergingValue] = {}
        self.values: Dict[str, Value] = {}
        
        # Relationship graphs
        self.value_relationship_graph = DirectedGraph()
        self.pattern_association_graph = Graph()
        
        # Processing queues
        self.experience_queue = deque()
        self.pattern_analysis_queue = deque()
        self.proto_value_evaluation_queue = deque()
        self.emerging_value_evaluation_queue = deque()
        
        # Processing flags
        self.is_processing = False
        self.processing_thread = None
        
        # State tracking
        self.last_maintenance_time = time.time()
        self.formation_statistics = {
            'experiences_processed': 0,
            'patterns_identified': 0,
            'proto_values_created': 0,
            'emerging_values_created': 0,
            'values_established': 0
        }
    
    def add_experience(self, experience: Experience) -> None:
        """Add an experience to be processed for pattern recognition."""
        self.experiences[experience.id] = experience
        self.experience_queue.append(experience.id)
        
        # Ensure we don't exceed memory capacity
        if len(self.experiences) > self.config.experience_memory_capacity:
            self._prune_experiences()
            
        # Trigger processing if not already running
        self._ensure_processing_active()
    
    def _ensure_processing_active(self) -> None:
        """Ensure that background processing is active."""
        if not self.is_processing:
            self.is_processing = True
            self.processing_thread = threading.Thread(target=self._process_queues)
            self.processing_thread.daemon = True
            self.processing_thread.start()
    
    def _process_queues(self) -> None:
        """Process all queues in order of data flow."""
        try:
            # Process each queue in sequence to ensure proper data flow
            while (self.experience_queue or self.pattern_analysis_queue or 
                   self.proto_value_evaluation_queue or self.emerging_value_evaluation_queue):
                
                # Process experiences to identify patterns
                self._process_experience_queue()
                
                # Process patterns to form proto-values
                self._process_pattern_queue()
                
                # Evaluate proto-values for promotion to emerging values
                self._process_proto_value_queue()
                
                # Evaluate emerging values for promotion to full values
                self._process_emerging_value_queue()
                
                # Periodic maintenance
                current_time = time.time()
                if current_time - self.last_maintenance_time > 3600:  # Once per hour
                    self._perform_maintenance()
                    self.last_maintenance_time = current_time
                    
                # Avoid tight loop if queues are empty
                if not (self.experience_queue or self.pattern_analysis_queue or 
                        self.proto_value_evaluation_queue or self.emerging_value_evaluation_queue):
                    time.sleep(0.1)
        finally:
            self.is_processing = False
    
    def _process_experience_queue(self) -> None:
        """Process experiences in the queue to identify patterns."""
        batch_size = min(50, len(self.experience_queue))
        if batch_size == 0:
            return
            
        processed_count = 0
        for _ in range(batch_size):
            if not self.experience_queue:
                break
                
            experience_id = self.experience_queue.popleft()
            experience = self.experiences.get(experience_id)
            if not experience:
                continue
                
            # Extract patterns from this experience
            new_patterns = self._identify_patterns_in_experience(experience)
            
            # Queue patterns for further analysis
            for pattern in new_patterns:
                self.patterns[pattern.id] = pattern
                self.pattern_analysis_queue.append(pattern.id)
                
            processed_count += 1
            self.formation_statistics['experiences_processed'] += 1
            
        logger.debug(f"Processed {processed_count} experiences, identified {len(self.pattern_analysis_queue)} patterns for analysis")
    
    def _identify_patterns_in_experience(self, experience: Experience) -> List[Pattern]:
        """Identify patterns within a given experience."""
        new_patterns = []
        
        # Simple pattern extraction (would be more sophisticated in production)
        # This is a placeholder for more complex pattern recognition
        
        # Example: Create a basic pattern based on experience content
        if experience.content:
            # Extract a simple pattern based on content features
            features = {}
            
            # Extract type-based features if available
            if 'type' in experience.content:
                features[f"type_{experience.content['type']}"] = 1.0
                
            # Extract sentiment features from valence
            features['valence'] = experience.valence
            features['intensity'] = experience.intensity
            
            # Create the pattern
            pattern = Pattern(
                experiences=[experience.id],
                features=features,
                salience=experience.salience,
                description=f"Pattern in {experience.source}: {experience.content.get('summary', '')}"
            )
            new_patterns.append(pattern)
            self.formation_statistics['patterns_identified'] += 1
            
        # In a real system, we would look for repeating structures, correlations, etc.
        
        return new_patterns
    
    def _process_pattern_queue(self) -> None:
        """Process patterns to identify proto-values and update pattern relationships."""
        batch_size = min(30, len(self.pattern_analysis_queue))
        if batch_size == 0:
            return
            
        for _ in range(batch_size):
            if not self.pattern_analysis_queue:
                break
                
            pattern_id = self.pattern_analysis_queue.popleft()
            pattern = self.patterns.get(pattern_id)
            if not pattern:
                continue
                
            # Find similar patterns
            similar_patterns = self._find_similar_patterns(pattern)
            
            # Update pattern relationships
            for similar_id, similarity in similar_patterns:
                if similar_id == pattern_id:
                    continue
                    
                # Add relationship to graph
                self.pattern_association_graph.add_edge(
                    pattern_id, similar_id, weight=similarity, timestamp=time.time())
                    
                # Potentially merge very similar patterns
                if similarity > 0.9:
                    self._merge_patterns(pattern_id, similar_id)
            
            # Check if pattern should contribute to proto-value formation
            if pattern.salience > self.config.pattern_significance_threshold:
                self._evaluate_pattern_for_value_formation(pattern)
                
    def _find_similar_patterns(self, pattern: Pattern) -> List[Tuple[str, float]]:
        """Find patterns similar to the given pattern."""
        similarities = []
        
        # In a production system, this would use more sophisticated similarity metrics
        # like vector embeddings, semantic similarity, etc.
        
        for other_id, other_pattern in self.patterns.items():
            if other_id == pattern.id:
                continue
                
            # Calculate feature similarity
            similarity = self._calculate_pattern_similarity(pattern, other_pattern)
            
            if similarity > self.config.pattern_similarity_threshold:
                similarities.append((other_id, similarity))
                
        # Sort by similarity descending
        return sorted(similarities, key=lambda x: x[1], reverse=True)
    
    def _calculate_pattern_similarity(self, pattern1: Pattern, pattern2: Pattern) -> float:
        """Calculate similarity between two patterns."""
        # Simple Jaccard similarity for feature keys
        features1 = set(pattern1.features.keys())
        features2 = set(pattern2.features.keys())
        
        if not features1 or not features2:
            return 0.0
            
        intersection = features1.intersection(features2)
        union = features1.union(features2)
        
        # Basic similarity from shared features
        key_similarity = len(intersection) / len(union) if union else 0
        
        # For shared features, calculate value similarity
        value_similarities = []
        for feature in intersection:
            val1 = pattern1.features[feature]
            val2 = pattern2.features[feature]
            # Simple relative difference
            similarity = 1.0 - min(1.0, abs(val1 - val2) / max(abs(val1), abs(val2), 1.0))
            value_similarities.append(similarity)
            
        # Average value similarity for shared features
        avg_value_similarity = sum(value_similarities) / len(value_similarities) if value_similarities else 0.5
        
        # Combined similarity (equal weighting)
        return (key_similarity + avg_value_similarity) / 2
    
    def _merge_patterns(self, pattern_id1: str, pattern_id2: str) -> None:
        """Merge two very similar patterns."""
        pattern1 = self.patterns.get(pattern_id1)
        pattern2 = self.patterns.get(pattern_id2)
        
        if not pattern1 or not pattern2:
            return
            
        # Create merged pattern
        merged = pattern1.merge_with(pattern2)
        self.patterns[merged.id] = merged
        
        # Update relationships in graph - transfer relationships from old patterns
        for node_id in self.pattern_association_graph.get_neighbors(pattern_id1):
            if node_id != pattern_id2:  # Avoid self-loops
                edge_attrs = self.pattern_association_graph.get_edge_attributes(pattern_id1, node_id)
                self.pattern_association_graph.add_edge(merged.id, node_id, **edge_attrs)
                
        for node_id in self.pattern_association_graph.get_neighbors(pattern_id2):
            if node_id != pattern_id1:  # Avoid self-loops
                edge_attrs = self.pattern_association_graph.get_edge_attributes(pattern_id2, node_id)
                self.pattern_association_graph.add_edge(merged.id, node_id, **edge_attrs)
        
        # Remove old patterns from graph and dictionary
        self.pattern_association_graph.remove_node(pattern_id1)
        self.pattern_association_graph.remove_node(pattern_id2)
        del self.patterns[pattern_id1]
        del self.patterns[pattern_id2]
        
        # Add merged pattern to analysis queue
        self.pattern_analysis_queue.append(merged.id)
        
    def _evaluate_pattern_for_value_formation(self, pattern: Pattern) -> None:
        """Evaluate if a pattern should contribute to proto-value formation."""
        proto_value_affinities = self._calculate_pattern_proto_value_affinities(pattern)
        
        if proto_value_affinities:
            top_affinity = proto_value_affinities[0]  # (proto_value_id, affinity)
            if top_affinity[1] > 0.7:  # Strong 
                self._reinforce_proto_value(top_affinity[0], pattern)
                return
        
        if (pattern.salience > self.config.pattern_significance_threshold and
                pattern.recurrence > 1):
            self._create_proto_value_from_pattern(pattern)
    
    def _calculate_pattern_proto_value_affinities(self, pattern: Pattern) -> List[Tuple[str, float]]:
        """Calculate how strongly a pattern relates to existing proto-values."""
        affinities = []
        
        for proto_id, proto_value in self.proto_values.items():
            affinity = 0.0
            
            # Check for shared experiences
            pattern_experiences = set(pattern.experiences)
            proto_experiences = set(proto_value.related_experiences)
            experience_overlap = len(pattern_experiences.intersection(proto_experiences))
            
            if experience_overlap > 0:
                # Higher affinity if many shared experiences
                affinity += 0.5 * min(1.0, experience_overlap / len(pattern_experiences))
            
            # Check feature similarity
            feature_similarity = 0.0
            pattern_features = set(pattern.features.keys())
            proto_features = set(proto_value.features.keys())
            
            if pattern_features and proto_features:
                # Jaccard similarity for feature keys
                intersection = pattern_features.intersection(proto_features)
                union = pattern_features.union(proto_features)
                feature_similarity = len(intersection) / len(union)
                
                # Update affinity with feature similarity component
                affinity += 0.5 * feature_similarity
            
            if affinity > 0.3:  # Minimum threshold to consider
                affinities.append((proto_id, affinity))
        
        # Sort by affinity descending
        return sorted(affinities, key=lambda x: x[1], reverse=True)
    
    def _reinforce_proto_value(self, proto_value_id: str, pattern: Pattern) -> None:
        """Reinforce an existing proto-value with a new pattern."""
        proto_value = self.proto_values.get(proto_value_id)
        if not proto_value:
            return
            
        # Add pattern to proto-value
        if pattern.id not in proto_value.patterns:
            proto_value.patterns.append(pattern.id)
            
        # Add experiences from pattern
        for exp_id in pattern.experiences:
            if exp_id not in proto_value.related_experiences:
                proto_value.related_experiences.append(exp_id)
        
        # Strengthen proto-value
        proto_value.strengthen(amount=0.1 * pattern.salience)
        
        # Update features by incorporating pattern features
        for key, value in pattern.features.items():
            if key in proto_value.features:
                # Average the values
                proto_value.features[key] = (proto_value.features[key] + value) / 2
            else:
                proto_value.features[key] = value
                
        # Queue for evaluation if it might be ready to evolve
        if proto_value.strength >= self.config.proto_to_emerging_threshold:
            self.proto_value_evaluation_queue.append(proto_value_id)
    
    def _create_proto_value_from_pattern(self, pattern: Pattern) -> None:
        """Create a new proto-value from a significant pattern."""
        # Generate a description for the proto-value
        description = f"Potential value based on {pattern.description}"
        
        # Create proto-value
        proto_value = ProtoValue(
            patterns=[pattern.id],
            strength=0.3 * pattern.salience,  # Initial strength based on pattern salience
            stability=0.2,  # Start with low stability
            description=description,
            related_experiences=pattern.experiences.copy(),
            features=pattern.features.copy()
        )
        
        self.proto_values[proto_value.id] = proto_value
        self.formation_statistics['proto_values_created'] += 1
        
        # Queue for potential future evaluation
        self.proto_value_evaluation_queue.append(proto_value.id)
        
        logger.debug(f"Created new proto-value: {description}")
    
    def _process_proto_value_queue(self) -> None:
        """Process proto-values to potentially promote to emerging values."""
        batch_size = min(20, len(self.proto_value_evaluation_queue))
        if batch_size == 0:
            return
            
        for _ in range(batch_size):
            if not self.proto_value_evaluation_queue:
                break
                
            proto_id = self.proto_value_evaluation_queue.popleft()
            proto_value = self.proto_values.get(proto_id)
            if not proto_value:
                continue
                
            # Check if proto-value should be promoted to emerging value
            if (proto_value.strength >= self.config.proto_to_emerging_threshold and
                    proto_value.stability >= self.config.proto_to_emerging_threshold / 2):
                self._promote_to_emerging_value(proto_value)
            elif proto_value.reinforcement_count < 3:
                # If not enough reinforcement yet, re-queue for later evaluation
                # but with lower priority (add to end of queue)
                self.proto_value_evaluation_queue.append(proto_id)
    
    def _promote_to_emerging_value(self, proto_value: ProtoValue) -> None:
        """Promote a proto-value to an emerging value."""
        # Generate a more refined description and definition
        definition = f"Emerging value derived from {len(proto_value.patterns)} patterns across {len(proto_value.related_experiences)} experiences"
        
        # Create emerging value
        emerging_value = EmergingValue(
            proto_values=[proto_value.id],
            clarity=0.5,  # Start with moderate clarity
            significance=proto_value.strength * 0.9,  # Slightly lower than proto-value strength
            stability=proto_value.stability * 0.9,  # Slightly lower than proto-value stability
            description=proto_value.description,
            definition=definition,
            related_patterns=proto_value.patterns,
            features=proto_value.features.copy()
        )
        
        self.emerging_values[emerging_value.id] = emerging_value
        self.formation_statistics['emerging_values_created'] += 1
        
        # Queue for future evaluation
        self.emerging_value_evaluation_queue.append(emerging_value.id)
        
        logger.info(f"Promoted proto-value to emerging value: {emerging_value.description}")
    
    def _process_emerging_value_queue(self) -> None:
        """Process emerging values to potentially promote to full values."""
        batch_size = min(10, len(self.emerging_value_evaluation_queue))
        if batch_size == 0:
            return
            
        for _ in range(batch_size):
            if not self.emerging_value_evaluation_queue:
                break
                
            emerging_id = self.emerging_value_evaluation_queue.popleft()
            emerging_value = self.emerging_values.get(emerging_id)
            if not emerging_value:
                continue
                
            # Refine emerging value with small increment
            emerging_value.refine(clarity_increase=0.05, significance_increase=0.03)
            
            # Check if emerging value should be promoted to full value
            if (emerging_value.clarity >= self.config.emerging_to_value_threshold and
                    emerging_value.significance >= self.config.emerging_to_value_threshold and
                    emerging_value.stability >= self.config.emerging_to_value_threshold / 1.5):
                self._promote_to_full_value(emerging_value)
            elif time.time() - emerging_value.emergence_time < 86400:  # Less than a day old
                # Re-queue for continued refinement if relatively new
                self.emerging_value_evaluation_queue.append(emerging_id)
    
    def _promote_to_full_value(self, emerging_value: EmergingValue) -> None:
        """Promote an emerging value to a full value."""
        # Gather related experiences from proto-values
        related_experiences = []
        predecessor_ids = [emerging_value.id]  # Include emerging value ID
        
        for proto_id in emerging_value.proto_values:
            proto_value = self.proto_values.get(proto_id)
            if proto_value:
                predecessor_ids.append(proto_id)
                related_experiences.extend(proto_value.related_experiences)
        
        # Remove duplicates
        related_experiences = list(set(related_experiences))
        
        # Generate name from description
        name = emerging_value.description.split(':')[0] if ':' in emerging_value.description else emerging_value.description
        name = name.strip()
        if len(name) > 30:  # Truncate if too long
            name = name[:27] + "..."
        
        # Create full value
        value = Value(
            name=name,
            description=emerging_value.definition,
            intensity=emerging_value.significance,
            stability=emerging_value.stability,
            clarity=emerging_value.clarity,
            predecessor_ids=predecessor_ids,
            related_experiences=related_experiences,
            features=emerging_value.features.copy(),
            integration_level=0.5
        )
        
        self.values[value.id] = value
        value.expression_history.append((time.time(), value.intensity))
        self.formation_statistics['values_established'] += 1
        
        # Add to value relationship graph
        self.value_relationship_graph.add_node(value.id, name=value.name, 
                                            description=value.description,
                                            intensity=value.intensity)
        
        # Establish relationships with other values
        self._establish_value_relationships(value)
        
        logger.info(f"Promoted emerging value to full value: {value.name}")
    
    def _establish_value_relationships(self, value: Value) -> None:
        """Establish relationships between this value and existing values."""
        for other_id, other_value in self.values.items():
            if other_id == value.id:
                continue
                
            # Calculate relationship strength based on feature similarity
            similarity = self._calculate_value_similarity(value, other_value)
            
            if similarity > 0.3:  # Minimum threshold to establish relationship
                relationship_type = "supports" if similarity > 0.7 else "related"
                self.value_relationship_graph.add_edge(
                    value.id, other_id, 
                    type=relationship_type,
                    strength=similarity,
                    established=time.time()
                )
    
    def _calculate_value_similarity(self, value1: Value, value2: Value) -> float:
        """Calculate similarity between two values."""
        # Check for shared experiences
        exp1 = set(value1.related_experiences)
        exp2 = set(value2.related_experiences)
        
        if not exp1 or not exp2:
            experience_similarity = 0.0
        else:
            intersection = exp1.intersection(exp2)
            union = exp1.union(exp2)
            experience_similarity = len(intersection) / len(union)
        
        # Check feature similarity
        feat1 = set(value1.features.keys())
        feat2 = set(value2.features.keys())
        
        if not feat1 or not feat2:
            feature_similarity = 0.0
        else:
            intersection = feat1.intersection(feat2)
            union = feat1.union(feat2)
            key_similarity = len(intersection) / len(union)
            
            # For shared features, calculate value similarity
            value_diffs = []
            for key in intersection:
                v1 = value1.features[key]
                v2 = value2.features[key]
                diff = abs(v1 - v2)
                value_diffs.append(1.0 - min(1.0, diff))
                
            avg_value_diff = sum(value_diffs) / len(value_diffs) if value_diffs else 0.5
            feature_similarity = (key_similarity + avg_value_diff) / 2
        
        # Combined similarity (weighted)
        return (experience_similarity * 0.4) + (fe