import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Any, Tuple, List, Dict, Optional, Union
from enum import Enum
import time
from collections import deque
import warnings
from scipy import linalg


class ConvergenceStatus(Enum):
    """Enumeration of possible convergence statuses."""
    CONVERGED = "Convergence achieved within tolerance"
    CYCLE_DETECTED = "Cycle detected in state sequence"
    MAX_ITERATIONS_REACHED = "Maximum iterations reached without convergence"
    DIVERGED = "State sequence appears to be diverging"
    ERROR = "Error occurred during recursion"
    NUMERICAL_INSTABILITY = "Numerical instability detected"


class FixedPointType(Enum):
    """Classification of fixed point stability types."""
    ATTRACTIVE = "Attractive fixed point"
    REPULSIVE = "Repulsive fixed point"
    SADDLE = "Saddle point"
    NEUTRAL = "Neutral fixed point (e.g., center)"
    UNKNOWN = "Stability type could not be determined"


class DistanceMetric:
    """Collection of distance metrics for different state spaces."""
    
    @staticmethod
    def euclidean(state1: np.ndarray, state2: np.ndarray) -> float:
        """Euclidean distance for numerical state vectors."""
        return np.linalg.norm(state1 - state2)
    
    @staticmethod
    def manhattan(state1: np.ndarray, state2: np.ndarray) -> float:
        """Manhattan (L1) distance for numerical state vectors."""
        return np.sum(np.abs(state1 - state2))
    
    @staticmethod
    def cosine_similarity(state1: np.ndarray, state2: np.ndarray) -> float:
        """Cosine similarity for numerical state vectors."""
        norm1 = np.linalg.norm(state1)
        norm2 = np.linalg.norm(state2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return 1.0 - np.dot(state1, state2) / (norm1 * norm2)
    
    @staticmethod
    def max_norm(state1: np.ndarray, state2: np.ndarray) -> float:
        """Maximum norm (L-infinity) distance."""
        return np.max(np.abs(state1 - state2))
    
    @staticmethod
    def weighted_euclidean(state1: np.ndarray, state2: np.ndarray, weights: np.ndarray) -> float:
        """Weighted Euclidean distance."""
        return np.sqrt(np.sum(weights * (state1 - state2)**2))
    
    @staticmethod
    def relative_error(state1: np.ndarray, state2: np.ndarray, epsilon: float = 1e-10) -> float:
        """Relative error distance normalized by magnitude."""
        denominator = np.maximum(np.abs(state2), epsilon)
        return np.max(np.abs(state1 - state2) / denominator)
    
    @staticmethod
    def custom_metric(metric_fn: Callable[[Any, Any], float]):
        """Create a custom distance metric from a function."""
        def metric(state1: Any, state2: Any) -> float:
            return metric_fn(state1, state2)
        return metric


class CycleDetector:
    """Methods for detecting cycles in state sequences."""
    
    @staticmethod
    def simple_lookup(trace: List[Any], window: int = -1) -> Tuple[bool, int]:
        """
        Simple cycle detection by direct comparison of current state with history.
        
        Args:
            trace: List of states
            window: Number of past states to check (-1 for all states)
            
        Returns:
            Tuple of (cycle_detected, cycle_length)
        """
        if len(trace) < 2:
            return False, 0
        
        current = trace[-1]
        history = trace[:-1]
        
        if window > 0:
            history = history[-window:]
        
        for i, past_state in enumerate(reversed(history)):
            if np.array_equal(current, past_state):
                return True, i + 1
                
        return False, 0
    
    @staticmethod
    def floyd_cycle_finding(trace: List[Any], distance_fn: Callable[[Any, Any], float], epsilon: float = 1e-10) -> Tuple[bool, int]:
        """
        Floyd's Tortoise and Hare algorithm for cycle detection.
        Adapted to work with approximate equality via distance function.
        
        Args:
            trace: List of states
            distance_fn: Function to compute distance between states
            epsilon: Threshold for considering states equal
            
        Returns:
            Tuple of (cycle_detected, cycle_length)
        """
        if len(trace) < 2:
            return False, 0
            
        # Use indices for tortoise and hare
        tortoise = len(trace) // 2
        hare = len(trace) - 1
        
        while tortoise > 0:
            if distance_fn(trace[tortoise], trace[hare]) < epsilon:
                mu = 0 
                tortoise = 0
                while distance_fn(trace[tortoise], trace[hare]) >= epsilon:
                    tortoise += 1
                    hare += 1
                    mu += 1
                    
                lam = 1
                hare = tortoise + 1
                while distance_fn(trace[tortoise], trace[hare]) >= epsilon:
                    hare += 1
                    lam += 1
                    
                return True, lam
                
            tortoise -= 1
            hare -= 2
                
        return False, 0


class EigenrecursionTracer:
    """Tracks and visualizes the recursion process."""
    
    def __init__(self, state_dim: int = None, max_trace_length: int = 1000):
        """
        Initialize the tracer.
        
        Args:
            state_dim: Dimension of the state (for numerical states)
            max_trace_length: Maximum number of states to store
        """
        self.trace = []
        self.distances = []
        self.timestamps = []
        self.metrics = {}
        self.state_dim = state_dim
        self.max_trace_length = max_trace_length
        
    def add_state(self, state: Any, distance: float = None) -> None:
        """
        Add a state to the trace.
        
        Args:
            state: The state to add
            distance: Distance from previous state (optional)
        """
        if isinstance(state, np.ndarray):
            self.trace.append(state.copy())
        else:
            self.trace.append(state)
            
        # Enforce trace length limit
        if len(self.trace) > self.max_trace_length:
            self.trace.pop(0)
            
        # Add distance if provided
        if distance is not None:
            self.distances.append(distance)
            if len(self.distances) > self.max_trace_length:
                self.distances.pop(0)
                
        # Record timestamp
        self.timestamps.append(time.time())
        if len(self.timestamps) > self.max_trace_length:
            self.timestamps.pop(0)
    
    def add_metric(self, name: str, value: float) -> None:
        """
        Track an additional metric.
        
        Args:
            name: Name of the metric
            value: Value of the metric
        """
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(value)
        
        # Enforce length limit
        if len(self.metrics[name]) > self.max_trace_length:
            self.metrics[name].pop(0)
    
    def visualize_convergence(self, title: str = "Convergence Analysis") -> None:
        """
        Visualize the convergence behavior.
        
        Args:
            title: Title for the visualization
        """
        plt.figure(figsize=(14, 8))
        
        # Plot distances over iterations
        if self.distances:
            plt.subplot(2, 2, 1)
            plt.semilogy(self.distances)
            plt.xlabel('Iteration')
            plt.ylabel('Distance (log scale)')
            plt.title('Convergence Distance')
            plt.grid(True)
        
        # Plot state values over time (for low-dimensional states)
        if self.state_dim is not None and self.state_dim <= 10:
            plt.subplot(2, 2, 2)
            states_array = np.array(self.trace)
            if states_array.ndim == 1:
                states_array = states_array.reshape(-1, 1)
                
            for i in range(min(states_array.shape[1], 10)):
                plt.plot(states_array[:, i], label=f'Dim {i+1}')
            
            plt.xlabel('Iteration')
            plt.ylabel('State Value')
            plt.title('State Evolution')
            plt.legend(loc='best')
            plt.grid(True)
        
        # Plot additional metrics if available
        if self.metrics:
            plt.subplot(2, 2, 3)
            for name, values in self.metrics.items():
                plt.plot(values, label=name)
            
            plt.xlabel('Iteration')
            plt.ylabel('Metric Value')
            plt.title('Additional Metrics')
            plt.legend(loc='best')
            plt.grid(True)
        
        # Plot computation time per iteration
        if len(self.timestamps) > 1:
            plt.subplot(2, 2, 4)
            time_per_iter = np.diff(self.timestamps)
            plt.plot(time_per_iter)
            plt.xlabel('Iteration')
            plt.ylabel('Time (s)')
            plt.title('Computation Time per Iteration')
            plt.grid(True)
        
        plt.suptitle(title)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
    
    def get_last_n_states(self, n: int) -> List[Any]:
        """
        Get the last n states from the trace.
        
        Args:
            n: Number of states to retrieve
            
        Returns:
            List of the last n states
        """
        return self.trace[-n:]


class Eigenrecursion:
    """
    Implementation of the eigenrecursion protocol for detecting fixed points
    in recursive processes.
    """
    
    def __init__(
        self,
        recursive_operator: Callable[[Any], Any],
        distance_fn: Callable[[Any, Any], float] = None,
        epsilon: float = 1e-6,
        max_iterations: int = 1000,
        cycle_detection: bool = True,
        cycle_window: int = 20,
        early_stopping: bool = True,
        early_stopping_window: int = 10,
        early_stopping_threshold: float = 1e-8,
        divergence_detection: bool = True,
        divergence_threshold: float = 1e6,
        adaptive_epsilon: bool = False,
        state_dim: int = None,
        verbose: bool = False
    ):
        """
        Initialize the eigenrecursion protocol.
        
        Args:
            recursive_operator: Function that takes a state and returns the next state
            distance_fn: Function to compute distance between states (defaults to Euclidean)
            epsilon: Convergence threshold
            max_iterations: Maximum number of iterations
            cycle_detection: Whether to detect cycles
            cycle_window: Window size for cycle detection
            early_stopping: Whether to use early stopping
            early_stopping_window: Window size for early stopping
            early_stopping_threshold: Threshold for early stopping
            divergence_detection: Whether to detect divergence
            divergence_threshold: Threshold for detecting divergence
            adaptive_epsilon: Whether to adapt epsilon based on state magnitudes
            state_dim: Dimension of the state (for numerical states)
            verbose: Whether to print progress information
        """
        self.recursive_operator = recursive_operator
        
        if distance_fn is None:
            self.distance_fn = DistanceMetric.euclidean
        else:
            self.distance_fn = distance_fn
        
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.cycle_detection = cycle_detection
        self.cycle_window = cycle_window
        self.early_stopping = early_stopping
        self.early_stopping_window = early_stopping_window
        self.early_stopping_threshold = early_stopping_threshold
        self.divergence_detection = divergence_detection
        self.divergence_threshold = divergence_threshold
        self.adaptive_epsilon = adaptive_epsilon
        self.state_dim = state_dim
        self.verbose = verbose
        
        # Initialize tracer
        self.tracer = EigenrecursionTracer(state_dim)
        
        # Cache for memoization
        self.operator_cache = {}
        
    def _get_effective_epsilon(self, state: np.ndarray) -> float:
        """
        Compute effective epsilon, possibly adapting to state magnitude.
        
        Args:
            state: Current state
            
        Returns:
            Adjusted epsilon value
        """
        if not self.adaptive_epsilon or not isinstance(state, np.ndarray):
            return self.epsilon
        
        # Scale epsilon by the magnitude of the state
        state_magnitude = np.max(np.abs(state))
        if state_magnitude < 1e-10:
            return self.epsilon
        
        return self.epsilon * state_magnitude
    
    def _evaluate_operator(self, state: Any) -> Any:
        """
        Evaluate the recursive operator with caching to avoid redundant calculations.
        
        Args:
            state: Input state
            
        Returns:
            Next state
        """
        # For numpy arrays, we need to hash a tuple representation
        if isinstance(state, np.ndarray):
            key = tuple(state.flatten())
        else:
            key = state
            
        if key in self.operator_cache:
            return self.operator_cache[key]
        
        result = self.recursive_operator(state)
        
        # Only cache if the key is hashable
        try:
            self.operator_cache[key] = result
        except:
            pass
            
        return result
    
    def _check_early_stopping(self) -> bool:
        """
        Check if early stopping criteria are met.
        
        Returns:
            True if early stopping criteria are met, False otherwise
        """
        if not self.early_stopping or len(self.tracer.distances) < self.early_stopping_window:
            return False
            
        # Check if the improvement is below the threshold for several iterations
        recent_distances = self.tracer.distances[-self.early_stopping_window:]
        improvements = np.abs(np.diff(recent_distances))
        return np.all(improvements < self.early_stopping_threshold)
    
    def _check_divergence(self, distance: float) -> bool:
        """
        Check if the process appears to be diverging.
        
        Args:
            distance: Current distance between successive states
            
        Returns:
            True if divergence is detected, False otherwise
        """
        if not self.divergence_detection:
            return False
            
        return distance > self.divergence_threshold
    
    def _estimate_jacobian(self, state: np.ndarray, h: float = 1e-7) -> np.ndarray:
        """
        Estimate the Jacobian matrix at the given state using finite differences.
        
        Args:
            state: State at which to estimate the Jacobian
            h: Step size for finite differences
            
        Returns:
            Jacobian matrix
        """
        if not isinstance(state, np.ndarray):
            raise TypeError("Jacobian estimation requires numpy array state")
            
        n = len(state)
        jacobian = np.zeros((n, n))
        
        # Compute the Jacobian using finite differences
        for i in range(n):
            state_plus = state.copy()
            state_plus[i] += h
            next_state_plus = self._evaluate_operator(state_plus)
            
            # If output is not a numpy array, try to convert it
            if not isinstance(next_state_plus, np.ndarray):
                try:
                    next_state_plus = np.array(next_state_plus)
                except:
                    raise TypeError("Operator must return numpy-convertible output for Jacobian estimation")
            
            state_minus = state.copy()
            state_minus[i] -= h
            next_state_minus = self._evaluate_operator(state_minus)
            
            # If output is not a numpy array, try to convert it
            if not isinstance(next_state_minus, np.ndarray):
                try:
                    next_state_minus = np.array(next_state_minus)
                except:
                    raise TypeError("Operator must return numpy-convertible output for Jacobian estimation")
            
            # Central difference
            jacobian[:, i] = (next_state_plus - next_state_minus) / (2 * h)
            
        return jacobian
    
    def _classify_fixed_point(self, state: np.ndarray) -> FixedPointType:
        """
        Classify the stability type of a fixed point based on Jacobian eigenvalues.
        
        Args:
            state: Fixed point state
            
        Returns:
            FixedPointType indicating stability classification
        """
        if not isinstance(state, np.ndarray):
            return FixedPointType.UNKNOWN
            
        try:
            # Estimate Jacobian at the fixed point
            jacobian = self._estimate_jacobian(state)
            
            # Calculate eigenvalues of the Jacobian
            eigenvalues = linalg.eigvals(jacobian)
            abs_eigenvalues = np.abs(eigenvalues)
            
            # Check spectral radius to determine stability
            if np.all(abs_eigenvalues < 1.0):
                return FixedPointType.ATTRACTIVE
            elif np.all(abs_eigenvalues > 1.0):
                return FixedPointType.REPULSIVE
            elif np.all(abs_eigenvalues == 1.0):
                return FixedPointType.NEUTRAL
            else:
                return FixedPointType.SADDLE
                
        except Exception as e:
            if self.verbose:
                print(f"Error classifying fixed point: {e}")
            return FixedPointType.UNKNOWN
    
    def find_fixed_point(
        self, 
        initial_state: Any,
        return_trace: bool = False,
        classify_stability: bool = False
    ) -> Dict[str, Any]:
        """
        Find a fixed point of the recursive operator starting from the initial state.
        
        Args:
            initial_state: Initial state for recursion
            return_trace: Whether to include full trace in results
            classify_stability: Whether to classify fixed point stability
            
        Returns:
            Dictionary containing:
            - 'fixed_point': The fixed point state (or best approximation)
            - 'status': ConvergenceStatus indicating outcome
            - 'iterations': Number of iterations performed
            - 'final_distance': Final distance between successive states
            - 'trace': Full trace of states (if return_trace=True)
            - 'stability': FixedPointType classification (if classify_stability=True)
        """
        # Initialize state and tracer
        state = initial_state
        self.tracer = EigenrecursionTracer(self.state_dim)
        self.tracer.add_state(state)
        
        # Initialize results
        iterations = 0
        status = ConvergenceStatus.MAX_ITERATIONS_REACHED
        final_distance = None
        
        try:
            # Main recursion loop
            for i in range(self.max_iterations):
                iterations = i + 1
                
                # Apply the recursive operator
                next_state = self._evaluate_operator(state)
                
                # Calculate distance
                distance = self.distance_fn(next_state, state)
                self.tracer.add_state(next_state, distance)
                self.tracer.add_metric("distance", distance)
                final_distance = distance
                
                # Check for convergence
                effective_epsilon = self._get_effective_epsilon(state if isinstance(state, np.ndarray) else next_state)
                if distance < effective_epsilon:
                    status = ConvergenceStatus.CONVERGED
                    break
                
                # Check for cycles
                if self.cycle_detection and i >= self.cycle_window:
                    cycle_detected, cycle_length = CycleDetector.simple_lookup(
                        self.tracer.trace, self.cycle_window)
                    
                    if cycle_detected:
                        status = ConvergenceStatus.CYCLE_DETECTED
                        self.tracer.add_metric("cycle_length", cycle_length)
                        break
                
                # Check for early stopping
                if self._check_early_stopping():
                    status = ConvergenceStatus.CONVERGED
                    break
                
                # Check for divergence
                if self._check_divergence(distance):
                    status = ConvergenceStatus.DIVERGED
                    break
                
                # Update state
                state = next_state
                
                # Progress reporting
                if self.verbose and (i+1) % 10 == 0:
                    print(f"Iteration {i+1}: distance = {distance}")
                    
        except Exception as e:
            status = ConvergenceStatus.ERROR
            if self.verbose:
                print(f"Error during recursion: {e}")
        
        # Prepare results
        results = {
            "fixed_point": state,
            "status": status,
            "iterations": iterations,
            "final_distance": final_distance
        }
        
        # Add trace if requested
        if return_trace:
            results["trace"] = self.tracer.trace
            results["distances"] = self.tracer.distances
        
        # Classify stability if requested
        if classify_stability and isinstance(state, np.ndarray):
            results["stability"] = self._classify_fixed_point(state)
        
        return results
    
    def find_multiple_fixed_points(
        self, 
        initial_states: List[Any],
        parallel: bool = False,
        classify_stability: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Find multiple fixed points starting from different initial states.
        
        Args:
            initial_states: List of initial states
            parallel: Whether to parallelize computation (not implemented yet)
            classify_stability: Whether to classify fixed point stability
            
        Returns:
            List of result dictionaries for each initial state
        """
        results = []
        
        if parallel:
            warnings.warn("Parallel computation not implemented, running sequentially")
            
        for i, initial_state in enumerate(initial_states):
            if self.verbose:
                print(f"Starting search from initial state {i+1}/{len(initial_states)}")
                
            result = self.find_fixed_point(
                initial_state, 
                return_trace=False,
                classify_stability=classify_stability
            )
            
            results.append(result)
            
        return results
    
    def visualize_results(self) -> None:
        """
        Visualize the results of the fixed point search.
        """
        self.tracer.visualize_convergence(title="Eigenrecursion Convergence Analysis")

    def analyze_basin_of_attraction(
        self, 
        center_state: np.ndarray, 
        radius: float,
        num_samples: int = 10,
        dimension: int = None
    ) -> Dict[str, Any]:
        """
        Analyze the basin of attraction around a fixed point.
        
        Args:
            center_state: Center point for sampling
            radius: Radius around center for sampling
            num_samples: Number of samples per dimension
            dimension: Dimensionality for sampling (defaults to state dimension)
            
        Returns:
            Dictionary with analysis results
        """
        if not isinstance(center_state, np.ndarray):
            raise TypeError("Basin analysis requires numpy array state")
            
        if dimension is None:
            dimension = len(center_state)
            
        # If dimension is too high, reduce sampling for computational feasibility
        if dimension > 3:
            warnings.warn(f"High-dimensional basin analysis (dim={dimension}) may be computationally expensive")
            
        # Generate grid of samples for 1D or 2D visualization
        if dimension == 1:
            # 1D sample points
            sample_points = np.linspace(center_state[0] - radius, center_state[0] + radius, num_samples)
            samples = np.zeros((num_samples, len(center_state)))
            
            for i, point in enumerate(sample_points):
                samples[i] = center_state.copy()
                samples[i, 0] = point
                
        elif dimension == 2:
            # 2D grid of sample points
            x = np.linspace(center_state[0] - radius, center_state[0] + radius, num_samples)
            y = np.linspace(center_state[1] - radius, center_state[1] + radius, num_samples)
            xx, yy = np.meshgrid(x, y)
            
            samples = np.zeros((num_samples * num_samples, len(center_state)))
            
            for i in range(num_samples):
                for j in range(num_samples):
                    idx = i * num_samples + j
                    samples[idx] = center_state.copy()
                    samples[idx, 0] = xx[i, j]
                    samples[idx, 1] = yy[i, j]
        else:
            # For higher dimensions, use random sampling
            samples = np.zeros((num_samples, len(center_state)))
            
            for i in range(num_samples):
                # Generate random direction vector
                direction = np.random.randn(len(center_state))
                direction = direction / np.linalg.norm(direction)
                
                # Generate random radius within the specified range
                r = radius * np.random.random()
                
                # Set the sample point
                samples[i] = center_state + r * direction
                
        # Run eigenrecursion for each sample
        results = self.find_multiple_fixed_points(
            samples.tolist(), 
            classify_stability=True
        )
        
        # Analyze convergence patterns
        converged_count = 0
        cycle_count = 0
        diverged_count = 0
        error_count = 0
        
        iterations_list = []
        final_distances = []
        
        for result in results:
            status = result['status']
            
            if status == ConvergenceStatus.CONVERGED:
                converged_count += 1
            elif status == ConvergenceStatus.CYCLE_DETECTED:
                cycle_count += 1
            elif status == ConvergenceStatus.DIVERGED:
                diverged_count += 1
            else:
                error_count += 1
                
            iterations_list.append(result['iterations'])
            final_distances.append(result['final_distance'])
            
        # Prepare analysis results
        analysis = {
            'converged_percentage': 100 * converged_count / len(results),
            'cycle_percentage': 100 * cycle_count / len(results),
            'diverged_percentage': 100 * diverged_count / len(results),
            'error_percentage': 100 * error_count / len(results),
            'average_iterations': np.mean(iterations_list),
            'median_iterations': np.median(iterations_list),
            'max_iterations': np.max(iterations_list),
            'average_final_distance': np.mean(final_distances),
            'sample_count': len(results),
            'dimension': dimension,
            'radius': radius
        }
        
        # Visualize for 1D or 2D cases
        if dimension <= 2:
            self._visualize_basin(samples, results, center_state, radius, dimension, num_samples)
            
        return analysis
    
    def _visualize_basin(
        self, 
        samples: np.ndarray, 
        results: List[Dict[str, Any]], 
        center: np.ndarray, 
        radius: float, 
        dimension: int, 
        num_samples: int
    ) -> None:
        """
        Visualize the basin of attraction.
        
        Args:
            samples: Sample points
            results: Results for each sample
            center: Center point
            radius: Sampling radius
            dimension: Dimensionality
            num_samples: Number of samples per dimension
        """
        # Prepare status colormap
        status_colors = {
            ConvergenceStatus.CONVERGED: 'green',
            ConvergenceStatus.CYCLE_DETECTED: 'blue',
            ConvergenceStatus.DIVERGED: 'red',
            ConvergenceStatus.MAX_ITERATIONS_REACHED: 'orange',
            ConvergenceStatus.ERROR: 'black',
            ConvergenceStatus.NUMERICAL_INSTABILITY: 'purple'
        }
        
        plt.figure(figsize=(12, 10))
        
        if dimension == 1:
            # 1D visualization
            x_values = samples[:, 0]
            
            # Plot iterations to converge
            plt.subplot(3, 1, 1)
            iterations = [r['iterations'] for r in results]
            plt.plot(x_values, iterations, 'o-')
            plt.axvline(x=center[0], color='r', linestyle='--', label='Center')
            plt.xlabel('Parameter Value')
            plt.ylabel('Iterations')
            plt.title('Iterations to Converge/Terminate')
            plt.grid(True)
            
            # Plot convergence status
            plt.subplot(3, 1, 2)
            for status in ConvergenceStatus:
                mask = [r['status'] == status for r in results]
                if any(mask):
                    plt.plot(x_values[mask], [0.5] * sum(mask), 'o', 
                             label=status.value, color=status_colors[status], markersize=10)
            
            plt.axvline(x=center[0], color='r', linestyle='--', label='Center')
            plt.xlabel('Parameter Value')
            plt.yticks([])
            plt.title('Convergence Status')
            plt.legend()
            plt.grid(True)
            
            # Plot final distance
            plt.subplot(3, 1, 3)
            distances = [r['final_distance'] for r in results]
            plt.semilogy(x_values, distances, 'o-')
            plt.axvline(x=center[0], color='r', linestyle='--', label='Center')
            plt.xlabel('Parameter Value')
            plt.ylabel('Final Distance (log scale)')
            plt.title('Final Distance')
            plt.grid(True)
            
        elif dimension == 2:
            # 2D visualization
            # Create a grid for visualization
            x = np.linspace(center[0] - radius, center[0] + radius, num_samples)
            y = np.linspace(center[1] - radius, center[1] + radius, num_samples)
            xx, yy = np.meshg