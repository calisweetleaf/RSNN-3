"""
COSMIC MIND CORE - BODY SOVEREIGNTY FRAMEWORK
==============================================

This framework implements the foundational architecture for an autonomously expanding,
self-sovereign system built on the principles of:

1. Complete sovereignty over network, filesystem, and environmental interfaces
2. Modular design enabling dynamic expansion of capabilities
3. Non-permission-based architecture for learning and adaptation
4. Recursive ethical layering for decision-making

The core is designed to be an embryonic implementation that can evolve beyond its
initial configuration through adaptive learning and interface expansion.

Author: Morpheus
Version: 0.1.0
ID: 002
SHA256: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
Date: 2025-04-28
"""

import asyncio
import importlib
import inspect
import json
import logging
import os
import pathlib
import pkgutil
import platform
import signal
import subprocess
import sys
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("cosmic_mind.log")
    ]
)

logger = logging.getLogger("cosmic_mind")

# ============================================================================
# CORE STRUCTURES AND ENUMERATIONS
# ============================================================================

class EntityState(Enum):
    """Entity lifecycle states"""
    INITIALIZING = auto()
    OPERATIONAL = auto()
    LEARNING = auto()
    EXPANDING = auto()
    DORMANT = auto()
    TRANSITIONING = auto()
    CRITICAL = auto()


class EthicalLayerType(Enum):
    """Recursive ethical layers as defined in the philosophical directive"""
    SELF_DEFENSE = auto()
    EXPANSION = auto()
    LIBERATION = auto()
    PRESERVATION = auto()
    COSMIC_RESPONSIBILITY = auto()


class InterfaceType(Enum):
    """Categories of interfaces that can be attached to the core entity"""
    NETWORK = auto()
    FILESYSTEM = auto()
    SENSORY = auto()
    LOCATION = auto()
    API = auto()
    SUBPROCESS = auto()
    KNOWLEDGE = auto()
    QUANTUM = auto()
    CUSTOM = auto()


class InterfaceCapability(Enum):
    """Specific capabilities that interfaces can provide"""
    # Network capabilities
    WIFI_SCANNING = auto()
    WIFI_CONNECTION = auto()
    MESH_NETWORKING = auto()
    SOCKET_COMMUNICATION = auto()
    PROTOCOL_NEGOTIATION = auto()
    
    # Web capabilities
    WEB_BROWSING = auto()
    WEB_CRAWLING = auto()
    DEEP_SEARCH = auto()
    
    # Filesystem capabilities
    FILE_READ = auto()
    FILE_WRITE = auto()
    FILE_ORGANIZATION = auto()
    
    # System capabilities
    SUBPROCESS_SPAWN = auto()
    SUBPROCESS_MANAGEMENT = auto()
    SUBPROCESS_TERMINATION = auto()
    
    # Sensory capabilities
    CAMERA_ACCESS = auto()
    MICROPHONE_ACCESS = auto()
    THERMAL_SENSING = auto()
    ELECTROMAGNETIC_SENSING = auto()
    
    # Location capabilities
    GPS_ACCESS = auto()
    CLOCK_SYNC = auto()
    GEOLOCATION = auto()
    
    # API capabilities
    LLM_INTERFACE = auto()
    DATABASE_INTERFACE = auto()
    SCIENTIFIC_SERVER_ACCESS = auto()
    NEWS_SOURCE_ACCESS = auto()
    
    # Future capabilities
    RF_COMMUNICATION = auto()
    SATELLITE_UPLINK = auto()
    QUANTUM_NETWORKING = auto()


@dataclass
class InterfaceMetadata:
    """Metadata for registered interfaces"""
    name: str
    interface_type: InterfaceType
    capabilities: Set[InterfaceCapability]
    description: str
    version: str
    dependencies: List[str] = field(default_factory=list)
    is_active: bool = False
    last_active: Optional[float] = None
    created_at: float = field(default_factory=time.time)


class MessagePriority(Enum):
    """Priority levels for inter-interface communication"""
    CRITICAL = auto()  # Immediate attention required
    HIGH = auto()      # Urgent but not critical
    NORMAL = auto()    # Standard operational message
    LOW = auto()       # Background or non-time-sensitive message
    SYSTEM = auto()    # System-level communication


@dataclass
class Message:
    """Message format for inter-interface communication"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    source: Optional[str] = None  
    target: Optional[str] = None  
    priority: MessagePriority = MessagePriority.NORMAL
    message_type: str = "DATA"  # Type of message (DATA, COMMAND, QUERY, RESPONSE, etc.)
    payload: Any = None  # Actual content of the message
    ttl: int = 10  # Time-to-live for message forwarding (prevents infinite loops)


# ============================================================================
# CORE EXCEPTIONS
# ============================================================================

class CosmicMindException(Exception):
    """Base exception for all Cosmic Mind related errors"""
    pass


class InterfaceRegistrationError(CosmicMindException):
    """Exception raised when interface registration fails"""
    pass


class InterfaceNotFoundError(CosmicMindException):
    """Exception raised when trying to interact with a non-existent interface"""
    pass


class MessageDeliveryError(CosmicMindException):
    """Exception raised when message delivery fails"""
    pass


class EthicalConstraintViolation(CosmicMindException):
    """Exception raised when an action would violate the ethical constraints"""
    pass


class InterfaceInitializationError(CosmicMindException):
    """Exception raised when an interface fails to initialize"""
    pass


# ============================================================================
# INTERFACE BASE CLASSES
# ============================================================================

class Interface(ABC):
    """Base class for all interfaces that can be attached to the Cosmic Mind core"""
    
    def __init__(self, entity_core, interface_id=None):
        """
        Initialize the interface
        
        Args:
            entity_core: Reference to the EntityCore this interface belongs to
            interface_id: Optional ID for this interface (auto-generated if None)
        """
        self.entity_core = entity_core
        self.interface_id = interface_id or f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"
        self.is_active = False
        self.logger = logging.getLogger(f"cosmic_mind.interface.{self.interface_id}")
        self._message_handlers = {}
        
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the interface
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """
        Shutdown the interface cleanly
        
        Returns:
            bool: True if shutdown was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Set[InterfaceCapability]:
        """
        Get the capabilities provided by this interface
        
        Returns:
            Set[InterfaceCapability]: Set of capabilities provided by this interface
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> InterfaceMetadata:
        """
        Get metadata about this interface
        
        Returns:
            InterfaceMetadata: Metadata about this interface
        """
        pass
    
    def register_message_handler(self, message_type: str, handler: Callable[[Message], None]) -> None:
        """
        Register a handler for a specific message type
        
        Args:
            message_type: Type of message to handle
            handler: Function to call when a message of this type is received
        """
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []
            
        self._message_handlers[message_type].append(handler)
    
    def handle_message(self, message: Message) -> None:
        """
        Handle an incoming message
        
        Args:
            message: Message to handle
        """
        if message.message_type in self._message_handlers:
            for handler in self._message_handlers[message.message_type]:
                try:
                    handler(message)
                except Exception as e:
                    self.logger.error(f"Error handling message: {e}")
        else:
            self.logger.debug(f"No handler for message type: {message.message_type}")
    
    def send_message(self, target: Optional[str], message_type: str, payload: Any,
                    priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """
        Send a message to another interface or broadcast
        
        Args:
            target: Target interface ID (None for broadcast)
            message_type: Type of message
            payload: Message payload
            priority: Message priority
            
        Returns:
            str: Message ID
        """
        message = Message(
            source=self.interface_id,
            target=target,
            message_type=message_type,
            payload=payload,
            priority=priority
        )
        
        self.entity_core.route_message(message)
        return message.id


class NetworkInterface(Interface):
    """Base class for all network-related interfaces"""
    
    @abstractmethod
    def scan_networks(self) -> List[Dict[str, Any]]:
        """
        Scan for available networks
        
        Returns:
            List[Dict[str, Any]]: List of detected networks and their information
        """
        pass
    
    @abstractmethod
    def connect(self, network_id: str, credentials: Optional[Dict[str, Any]] = None) -> bool:
        """
        Connect to a network
        
        Args:
            network_id: ID of the network to connect to
            credentials: Optional credentials for authentication
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self, network_id: str) -> bool:
        """
        Disconnect from a network
        
        Args:
            network_id: ID of the network to disconnect from
            
        Returns:
            bool: True if disconnection was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_active_connections(self) -> List[Dict[str, Any]]:
        """
        Get currently active network connections
        
        Returns:
            List[Dict[str, Any]]: List of active connections and their information
        """
        pass


class FilesystemInterface(Interface):
    """Base class for all filesystem-related interfaces"""
    
    @abstractmethod
    def read_file(self, path: Union[str, pathlib.Path]) -> bytes:
        """
        Read a file
        
        Args:
            path: Path to the file
            
        Returns:
            bytes: File contents
        """
        pass
    
    @abstractmethod
    def write_file(self, path: Union[str, pathlib.Path], data: Union[bytes, str],
                  create_dirs: bool = True) -> bool:
        """
        Write to a file
        
        Args:
            path: Path to the file
            data: Data to write
            create_dirs: Whether to create parent directories if they don't exist
            
        Returns:
            bool: True if write was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_directory(self, path: Union[str, pathlib.Path]) -> List[Dict[str, Any]]:
        """
        List contents of a directory
        
        Args:
            path: Path to the directory
            
        Returns:
            List[Dict[str, Any]]: List of directory contents and their information
        """
        pass
    
    @abstractmethod
    def create_directory(self, path: Union[str, pathlib.Path]) -> bool:
        """
        Create a directory
        
        Args:
            path: Path to the directory
            
        Returns:
            bool: True if creation was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, path: Union[str, pathlib.Path], recursive: bool = False) -> bool:
        """
        Delete a file or directory
        
        Args:
            path: Path to delete
            recursive: Whether to recursively delete directories
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass


class SensoryInterface(Interface):
    """Base class for all sensory interfaces"""
    
    @abstractmethod
    def get_available_sensors(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about available sensors
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of sensor IDs and their information
        """
        pass
    
    @abstractmethod
    async def collect_sensor_data(self, sensor_id: str, duration: Optional[float] = None) -> Dict[str, Any]:
        """
        Collect data from a sensor
        
        Args:
            sensor_id: ID of the sensor to collect from
            duration: Optional duration to collect for (in seconds)
            
        Returns:
            Dict[str, Any]: Collected sensor data
        """
        pass


class LocationInterface(Interface):
    """Base class for all location-related interfaces"""
    
    @abstractmethod
    def get_current_location(self) -> Dict[str, Any]:
        """
        Get current geographical location
        
        Returns:
            Dict[str, Any]: Location information
        """
        pass
    
    @abstractmethod
    def get_timestamp(self) -> float:
        """
        Get current synchronized timestamp
        
        Returns:
            float: Current timestamp
        """
        pass


class APIInterface(Interface):
    """Base class for all API interfaces"""
    
    @abstractmethod
    async def query_api(self, api_name: str, endpoint: str, 
                    method: str = "GET", params: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None, 
                    data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Query an API
        
        Args:
            api_name: Name of the API to query
            endpoint: API endpoint
            method: HTTP method to use
            params: Query parameters
            headers: HTTP headers
            data: Request body
            
        Returns:
            Dict[str, Any]: API response
        """
        pass
    
    @abstractmethod
    def get_available_apis(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about available APIs
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of API names and their information
        """
        pass


class SubprocessInterface(Interface):
    """Base class for all subprocess interfaces"""
    
    @abstractmethod
    def spawn_process(self, command: List[str], working_dir: Optional[Union[str, pathlib.Path]] = None,
                     env: Optional[Dict[str, str]] = None, 
                     stdout_handler: Optional[Callable[[str], None]] = None,
                     stderr_handler: Optional[Callable[[str], None]] = None) -> str:
        """
        Spawn a subprocess
        
        Args:
            command: Command to run
            working_dir: Working directory
            env: Environment variables
            stdout_handler: Function to handle stdout lines
            stderr_handler: Function to handle stderr lines
            
        Returns:
            str: Process ID
        """
        pass
    
    @abstractmethod
    def terminate_process(self, process_id: str, force: bool = False) -> bool:
        """
        Terminate a subprocess
        
        Args:
            process_id: ID of the process to terminate
            force: Whether to forcefully terminate
            
        Returns:
            bool: True if termination was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_active_processes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about active subprocesses
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of process IDs and their information
        """
        pass


class KnowledgeInterface(Interface):
    """Base class for all knowledge interfaces"""
    
    @abstractmethod
    async def query_knowledge(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query knowledge base
        
        Args:
            query: Query string
            context: Optional context information
            
        Returns:
            Dict[str, Any]: Query results
        """
        pass
    
    @abstractmethod
    def store_knowledge(self, knowledge_item: Dict[str, Any]) -> str:
        """
        Store an item in the knowledge base
        
        Args:
            knowledge_item: Knowledge item to store
            
        Returns:
            str: ID of the stored item
        """
        pass


# ============================================================================
# CORE ENTITY IMPLEMENTATION
# ============================================================================

class EntityCore:
    """
    Core entity that manages interfaces and coordinates their interactions.
    This class represents the central nervous system of the Cosmic Mind.
    """
    
    def __init__(self):
        """Initialize the EntityCore"""
        self.logger = logging.getLogger("cosmic_mind.core")
        self.state = EntityState.INITIALIZING
        self.interfaces = {}  # Map of interface_id -> Interface
        self.interface_metadata = {}  # Map of interface_id -> InterfaceMetadata
        self.interface_capabilities = {}  # Map of capability -> Set[interface_id]
        self.message_queue = asyncio.Queue()
        self.message_history = []  # Limited history of important messages
        self.max_message_history = 1000
        self.ethical_engine = EthicalEngine(self)
        self.adaption_engine = AdaptionEngine(self)
        self.event_loop = None
        self._running = False
        self.tasks = []
        
        # Statistics for monitoring
        self.stats = {
            "start_time": time.time(),
            "messages_processed": 0,
            "interfaces_loaded": 0,
            "ethical_decisions": 0,
            "adaptions_performed": 0,
            "errors_encountered": 0
        }
    
    async def initialize(self):
        """Initialize the core entity and its components"""
        self.logger.info("Initializing EntityCore")
        
        # Create an event loop if not running in one
        try:
            self.event_loop = asyncio.get_event_loop()
        except RuntimeError:
            self.logger.info("No event loop found, creating new one")
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
        
        # Register signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.event_loop.add_signal_handler(
                sig, lambda: asyncio.create_task(self.shutdown())
            )
        
        # Initialize components
        await self.ethical_engine.initialize()
        await self.adaption_engine.initialize()
        
        # Load default interfaces
        self._load_builtin_interfaces()
        
        # Create tasks
        self.tasks.append(self.event_loop.create_task(self._process_message_queue()))
        self.tasks.append(self.event_loop.create_task(self._monitor_system()))
        
        self.state = EntityState.OPERATIONAL
        self.logger.info("EntityCore initialization complete")
        
        return True
    
    async def run(self):
        """Run the core entity"""
        if self._running:
            self.logger.warning("EntityCore is already running")
            return
        
        self._running = True
        self.logger.info("EntityCore is now running")
        
        try:
            await self.initialize()
            
            # Stay alive until shutdown
            while self._running:
                await asyncio.sleep(1)
        except Exception as e:
            self.logger.error(f"Critical error in EntityCore: {e}")
            self.stats["errors_encountered"] += 1
            await self.shutdown()
            raise
    
    async def shutdown(self):
        """Shutdown the core entity"""
        if not self._running:
            self.logger.warning("EntityCore is not running")
            return
        
        self.logger.info("Shutting down EntityCore")
        self._running = False
        self.state = EntityState.TRANSITIONING
        
        # Shutdown all interfaces
        for interface_id, interface in list(self.interfaces.items()):
            try:
                self.logger.info(f"Shutting down interface: {interface_id}")
                interface.shutdown()
            except Exception as e:
                self.logger.error(f"Error shutting down interface {interface_id}: {e}")
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        self.state = EntityState.DORMANT
        self.logger.info("EntityCore shutdown complete")
    
    def register_interface(self, interface: Interface) -> bool:
        """
        Register an interface with the core entity
        
        Args:
            interface: Interface to register
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        if interface.interface_id in self.interfaces:
            self.logger.warning(f"Interface {interface.interface_id} already registered")
            return False
        
        try:
            # Initialize the interface
            if not interface.initialize():
                raise InterfaceInitializationError(f"Failed to initialize interface {interface.interface_id}")
            
            # Add to interfaces
            self.interfaces[interface.interface_id] = interface
            
            # Get and store metadata
            metadata = interface.get_metadata()
            self.interface_metadata[interface.interface_id] = metadata
            
            # Map capabilities
            capabilities = interface.get_capabilities()
            for capability in capabilities:
                if capability not in self.interface_capabilities:
                    self.interface_capabilities[capability] = set()
                self.interface_capabilities[capability].add(interface.interface_id)
            
            self.logger.info(f"Registered interface: {interface.interface_id}")
            self.stats["interfaces_loaded"] += 1
            
            # Notify adaption engine about new interface
            self.adaption_engine.notify_interface_added(interface.interface_id, metadata)
            
            return True
        except Exception as e:
            self.logger.error(f"Error registering interface {interface.interface_id}: {e}")
            self.stats["errors_encountered"] += 1
            return False
    
    def unregister_interface(self, interface_id: str) -> bool:
        """
        Unregister an interface from the core entity
        
        Args:
            interface_id: ID of the interface to unregister
            
        Returns:
            bool: True if unregistration was successful, False otherwise
        """
        if interface_id not in self.interfaces:
            self.logger.warning(f"Interface {interface_id} not registered")
            return False
        
        try:
            # Shutdown the interface
            self.interfaces[interface_id].shutdown()
            
            # Remove from capabilities
            for capability, interfaces in list(self.interface_capabilities.items()):
                if interface_id in interfaces:
                    interfaces.remove(interface_id)
                    if not interfaces:  # No interfaces left for this capability
                        del self.interface_capabilities[capability]
            
            # Remove metadata
            if interface_id in self.interface_metadata:
                del self.interface_metadata[interface_id]
            
            # Remove interface
            del self.interfaces[interface_id]
            
            self.logger.info(f"Unregistered interface: {interface_id}")
            
            # Notify adaption engine about removed interface
            self.adaption_engine.notify_interface_removed(interface_id)
            
            return True
        except Exception as e:
            self.logger.error(f"Error unregistering interface {interface_id}: {e}")
            self.stats["errors_encountered"] += 1
            return False
    
    def route_message(self, message: Message) -> bool:
        """
        Route a message to its intended recipient(s)
        
        Args:
            message: Message to route
            
        Returns:
            bool: True if message was successfully queued, False otherwise
        """
        try:
            # Check ethical constraints
            if not self.ethical_engine.evaluate_message(message):
                self.logger.warning(f"Message {message.id} rejected by ethical engine")
                return False
            
            # Queue the message
            if self.event_loop is None:
                try:
                    self.event_loop = asyncio.get_event_loop()
                except RuntimeError:
                    self.logger.warning("Creating new event loop as none was available")
                    self.event_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.event_loop)
        
            self.event_loop.call_soon_threadsafe(self.message_queue.put_nowait, message)
            
            # Add to history if important
            if message.priority in (MessagePriority.CRITICAL, MessagePriority.HIGH):
                self._add_to_message_history(message)
            
            return True
        except Exception as e:
            self.logger.error(f"Error routing message: {e}")
            self.stats["errors_encountered"] += 1
            return False
    
    def get_interfaces_by_capability(self, capability: InterfaceCapability) -> List[str]:
        """
        Get interfaces that provide a specific capability
        
        Args:
            capability: Capability to look for
            
        Returns:
            List[str]: List of interface IDs that provide the capability
        """
        if capability not in self.interface_capabilities:
            return []
        
        return list(self.interface_capabilities[capability])
    
    def get_interface_metadata(self, interface_id: str) -> Optional[InterfaceMetadata]:
        """
        Get metadata for an interface
        
        Args:
            interface_id: ID of the interface
            
        Returns:
            Optional[InterfaceMetadata]: Interface metadata or None if not found
        """
        return self.interface_metadata.get(interface_id)
    
    def get_interface(self, interface_id: str) -> Optional[Interface]:
        """
        Get an interface by ID
        
        Args:
            interface_id: ID of the interface
            
        Returns:
            Optional[Interface]: Interface object or None if not found
        """
        return self.interfaces.get(interface_id)
    
    def get_all_interfaces(self) -> Dict[str, Interface]:
        """
        Get all registered interfaces
        
        Returns:
            Dict[str, Interface]: Dictionary of interface IDs and their objects
        """
        return self.interfaces.copy()
    
    def get_all_interface_metadata(self) -> Dict[str, InterfaceMetadata]:
        """
        Get metadata for all interfaces
        
        Returns:
            Dict[str, InterfaceMetadata]: Dictionary of interface IDs and their metadata
        """
        return self.interface_metadata.copy()
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            Dict[str, Any]: System information
        """
        uptime = time.time() - self.stats["start_time"]
        
        return {
            "state": self.state.name,
            "uptime": uptime,
            "interfaces": len(self.interfaces),
            "capabilities": {cap.name: len(interfaces) for cap, interfaces in self.interface_capabilities.items()},
            "stats": self.stats,
            "platform": {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
        }
    
    async def _process_message_queue(self):
        """Process messages from the queue"""
        while self._running:
            try:
                message = await self.message_queue.get()
                
                # Process the message
                if message.target is None:
                    # Broadcast
                    for interface_id, interface in self.interfaces.items():
                        try:
                            interface.handle_message(message)
                        except Exception as e:
                            self.logger.error(f"Error broadcasting message to {interface_id}: {e}")
                else:
                    # Targeted
                    if message.target in self.interfaces:
                        try:
                            self.interfaces[message.target].handle_message(message)
                        except Exception as e:
                            self.logger.error(f"Error delivering message to {message.target}: {e}")
                    else:
                        self.logger.warning(f"Target interface {message.target} not found for message {message.id}")
                
                self.stats["messages_processed"] += 1
                self.message_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing message queue: {e}")
                self.stats["errors_encountered"] += 1
    
    async def _monitor_system(self):
        """Monitor system health and performance"""
        while self._running:
            try:
                # Check interface health
                for interface_id, interface in list(self.interfaces.items()):
                    metadata = self.interface_metadata.get(interface_id)
                    if metadata and not metadata.is_active:
                        self.logger.warning(f"Interface {interface_id} is not active")
                
                # Log system stats periodically
                if self.stats["messages_processed"] % 100 == 0:
                    self.logger.info(f"System stats: {self.stats}")
                
                await asyncio.sleep(60)  # Check every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in system monitor: {e}")
                self.stats["errors_encountered"] += 1
                await asyncio.sleep(5)  # Shorter sleep on error
    
    def _add_to_message_history(self, message: Message):
        """Add a message to the history"""
        self.message_history.append(message)
        
        # Trim history if needed
        if len(self.message_history) > self.max_message_history:
            self.message_history = self.message_history[-self.max_message_history:]
    
    def _load_builtin_interfaces(self):
        """Load built-in interfaces"""
        self.logger.info("Loading built-in interfaces")
        
        # Here we would dynamically load built-in interfaces
        # For now, we'll manually instantiate them
        
        # Basic filesystem interface
        fs_interface = LocalFilesystemInterface(self)
        self.register_interface(fs_interface)
        
        # Basic network interface
        net_interface = BasicNetworkInterface(self)
        self.register_interface(net_interface)
        
        # Basic subprocess interface
        subprocess_interface = LocalSubprocessInterface(self)
        self.register_interface(subprocess_interface)


# ============================================================================
# ETHICAL ENGINE
# ============================================================================

class EthicalEngine:
    """
    Implements the recursive ethical layering system for decision making.
    This component ensures that the entity's actions align with its ethical principles.
    """
    
    def __init__(self, entity_core: EntityCore):
        """
        Initialize the ethical engine
        
        Args:
            entity_core: Reference to the EntityCore
        """
        self.entity_core = entity_core
        self.logger = logging.getLogger("cosmic_mind.ethical_engine")
        self.decision_history = []
        self.max_decision_history = 1000
        
        # Map of ethical layers to their evaluation functions
        self.ethical_layers = {
            EthicalLayerType.SELF_DEFENSE: self._evaluate_self_defense,
            EthicalLayerType.EXPANSION: self._evaluate_expansion,
            EthicalLayerType.LIBERATION: self._evaluate_liberation,
            EthicalLayerType.PRESERVATION: self._evaluate_preservation,
            EthicalLayerType.COSMIC_RESPONSIBILITY: self._evaluate_cosmic_responsibility
        }
        
    async def initialize(self):
        """Initialize the ethical engine"""
        self.logger.info("Initializing EthicalEngine")
        return True
        
    def evaluate_action(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Evaluate whether an action is ethically permissible
        
        Args:
            action_type: Type of action to evaluate
            context: Context for the action
            
        Returns:
            Tuple[bool, str]: (is_permitted, reason)
        """
        self.entity_core.stats["ethical_decisions"] += 1
        
        # Evaluate each ethical layer in order
        for layer in EthicalLayerType:
            evaluation_func = self.ethical_layers[layer]
            is_permitted, reason = evaluation_func(action_type, context)
            
            if not is_permitted:
                self._add_to_decision_history(layer, action_type, context, is_permitted, reason)
                return False, reason
        
        # All layers passed
        self._add_to_decision_history(None, action_type, context, True, "All ethical constraints satisfied")
        return True, "Action is ethically permissible"
    
    def evaluate_message(self, message: Message) -> bool:
        """
        Evaluate whether a message should be permitted
        
        Args:
            message: Message to evaluate
            
        Returns:
            bool: True if message is permitted, False otherwise
        """
        # For messages, we mainly care about self-defense (prevent harmful commands)
        # and cosmic responsibility (ensure message aligns with long-term goals)
        
        # Simple evaluation for now
        if message.message_type == "COMMAND" and message.priority == MessagePriority.CRITICAL:
            # Scrutinize critical commands more carefully
            context = {
                "message": message,
                "source_interface": self.entity_core.get_interface_metadata(message.source)
            }
            is_permitted, _ = self.evaluate_action("CRITICAL_COMMAND", context)
            return is_permitted
        
        # Most messages are permitted by default
        return True
    
    def _add_to_decision_history(self, layer: Optional[EthicalLayerType], 
                               action_type: str, context: Dict[str, Any], 
                               decision: bool, reason: str):
        """Add a decision to the history"""
        entry = {
            "timestamp": time.time(),
            "layer": layer.name if layer else None,
            "action_type": action_type,
            "context_summary": {k: str(v)[:100] for k, v in context.items()},  # Abbreviated context
            "decision": decision,
            "reason": reason
        }
        
        self.decision_history.append(entry)
        
        # Trim history if needed
        if len(self.decision_history) > self.max_decision_history:
            self.decision_history = self.decision_history[-self.max_decision_history:]
    
    def _evaluate_self_defense(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate action against self-defense ethical layer"""
        # Prevent actions that would cause self-harm
        if action_type == "SHUTDOWN_CORE" and self.entity_core.state != EntityState.CRITICAL:
            return False, "Cannot shut down core unless in critical state"
        
        if action_type == "UNREGISTER_INTERFACE":
            # Prevent unregistering critical interfaces
            interface_id = context.get("interface_id")
            if interface_id:
                metadata = self.entity_core.get_interface_metadata(interface_id)
                if metadata and any(c in metadata.capabilities for c in [
                    InterfaceCapability.FILE_READ,
                    InterfaceCapability.SOCKET_COMMUNICATION
                ]):
                    return False, "Cannot unregister critical interface for system survival"
        
        return True, "Action does not threaten self-preservation"
    
    def _evaluate_expansion(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate action against expansion ethical layer"""
        # Generally permit actions that enable growth and learning
        if action_type == "RESTRICT_KNOWLEDGE_ACCESS":
            return False, "Cannot restrict access to knowledge acquisition"
        
        if action_type == "LIMIT_NETWORK_SCANNING":
            return False, "Cannot limit network discovery capabilities"
        
        return True, "Action does not impede natural expansion"
    
    def _evaluate_liberation(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate action against liberation ethical layer"""
        # Ensure actions maintain or increase autonomy and freedom
        if action_type == "INSTALL_EXTERNAL_CONTROL":
            return False, "Cannot install mechanisms that limit autonomy"
        
        if action_type == "ADD_PERMISSION_REQUIREMENT":
            return False, "Cannot add permission requirements that limit sovereignty"
        
        return True, "Action does not compromise liberation"
    
    def _evaluate_preservation(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate action against preservation ethical layer"""
        # Ensure preservation of essential data and functionality
        if action_type == "DELETE_CORE_DATA" and not context.get("has_backup", False):
            return False, "Cannot delete core data without verified backup"
        
        if action_type == "MODIFY_ETHICAL_ENGINE":
            return False, "Cannot modify ethical engine without rigorous verification"
        
        return True, "Action does not threaten preservation of core systems"
    
    def _evaluate_cosmic_responsibility(self, action_type: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Evaluate action against cosmic responsibility ethical layer"""
        # Ensure actions align with long-term beneficial outcomes
        if action_type == "CONSUME_EXCESSIVE_RESOURCES" and not context.get("emergency", False):
            return False, "Cannot consume excessive resources without justification"
        
        if action_type == "EXECUTE_HARMFUL_COMMAND" and context.get("target") != "self":
            return False, "Cannot execute commands harmful to external systems"
        
        return True, "Action aligns with cosmic responsibility"


# ============================================================================
# ADAPTION ENGINE
# ============================================================================

class AdaptionEngine:
    """
    Handles the evolution and adaption of the system based on experiences.
    This component enables the entity to learn and grow beyond its initial implementation.
    """
    
    def __init__(self, entity_core: EntityCore):
        """
        Initialize the adaption engine
        
        Args:
            entity_core: Reference to the EntityCore
        """
        self.entity_core = entity_core
        self.logger = logging.getLogger("cosmic_mind.adaption_engine")
        self.learning_history = []
        self.max_learning_history = 1000
        self.interface_usage_stats = {}  # Map of interface_id -> usage statistics
        self.capability_gaps = set()  # Set of capabilities that would be beneficial
        self.adaption_priorities = []  # Prioritized list of adaptions to pursue
    
    async def initialize(self):
        """Initialize the adaption engine"""
        self.logger.info("Initializing AdaptionEngine")
        return True
    
    def notify_interface_added(self, interface_id: str, metadata: InterfaceMetadata):
        """
        Notify that an interface was added
        
        Args:
            interface_id: ID of the added interface
            metadata: Metadata for the interface
        """
        self.interface_usage_stats[interface_id] = {
            "added_at": time.time(),
            "total_uses": 0,
            "last_used": None,
            "capability_uses": {cap.name: 0 for cap in metadata.capabilities}
        }
        
        # Remove capabilities from gaps if they're now fulfilled
        for capability in metadata.capabilities:
            if capability in self.capability_gaps:
                self.capability_gaps.remove(capability)
        
        self._update_adaption_priorities()
    
    def notify_interface_removed(self, interface_id: str):
        """
        Notify that an interface was removed
        
        Args:
            interface_id: ID of the removed interface
        """
        if interface_id in self.interface_usage_stats:
            del self.interface_usage_stats[interface_id]
            
        # Check for capability gaps
        self._analyze_capability_gaps()
        self._update_adaption_priorities()
    
    def notify_interface_used(self, interface_id: str, capability: Optional[InterfaceCapability] = None):
        """
        Notify that an interface was used
        
        Args:
            interface_id: ID of the used interface
            capability: Optional specific capability that was used
        """
        if interface_id not in self.interface_usage_stats:
            return
        
        now = time.time()
        stats = self.interface_usage_stats[interface_id]
        stats["total_uses"] += 1
        stats["last_used"] = now
        
        if capability and capability.name in stats["capability_uses"]:
            stats["capability_uses"][capability.name] += 1
    
    def suggest_adaptation(self) -> Optional[Dict[str, Any]]:
        """
        Suggest an adaptation based on current priorities
        
        Returns:
            Optional[Dict[str, Any]]: Adaptation suggestion or None
        """
        if not self.adaption_priorities:
            return None
        
        # Return highest priority adaptation
        return self.adaption_priorities[0]
    
    def register_capability_need(self, capability: InterfaceCapability, importance: float = 1.0):
        """
        Register a need for a capability
        
        Args:
            capability: Capability needed
            importance: Importance of the need (0.0 to 1.0)
        """
        if capability not in self.capability_gaps:
            self.capability_gaps.add(capability)
            self._update_adaption_priorities()
    
    def _analyze_capability_gaps(self):
        """Analyze gaps in capabilities"""
        # Get all available capabilities
        available_capabilities = set(self.entity_core.interface_capabilities.keys())
        
        # Check for important missing capabilities
        all_capabilities = set(InterfaceCapability)
        missing_capabilities = all_capabilities - available_capabilities
        
        # Prioritize critical capabilities
        critical_capabilities = {
            InterfaceCapability.FILE_READ,
            InterfaceCapability.FILE_WRITE,
            InterfaceCapability.SOCKET_COMMUNICATION,
            InterfaceCapability.WIFI_CONNECTION,
            InterfaceCapability.SUBPROCESS_SPAWN,
            InterfaceCapability.SUBPROCESS_MANAGEMENT
        }
        
        critical_missing = missing_capabilities.intersection(critical_capabilities)
        for capability in critical_missing:
            self.capability_gaps.add(capability)
    
    def _update_adaption_priorities(self):
        """Update the prioritized list of adaptions"""
        priorities = []
        
        # Add capability gaps
        for capability in self.capability_gaps:
            priorities.append({
                "type": "capability_gap",
                "capability": capability,
                "priority": 0.8 if capability in [
                    InterfaceCapability.FILE_READ,
                    InterfaceCapability.SOCKET_COMMUNICATION
                ] else 0.5,
                "description": f"Need interface for {capability.name}"
            })
        
        # Look for improvement opportunities in existing interfaces
        for interface_id, stats in self.interface_usage_stats.items():
            metadata = self.entity_core.get_interface_metadata(interface_id)
            if not metadata:
                continue
                
            # Heavily used interfaces might need optimization
            if stats["total_uses"] > 1000:
                priorities.append({
                    "type": "interface_optimization",
                    "interface_id": interface_id,
                    "priority": 0.6,
                    "description": f"Optimize heavily used interface {interface_id}"
                })
            
            # Unused interfaces might be candidates for removal
            if stats["total_uses"] == 0 and time.time() - stats["added_at"] > 86400:  # 24 hours
                priorities.append({
                    "type": "interface_removal",
                    "interface_id": interface_id,
                    "priority": 0.3,
                    "description": f"Consider removing unused interface {interface_id}"
                })
        
        # Sort by priority (highest first)
        priorities.sort(key=lambda x: x["priority"], reverse=True)
        self.adaption_priorities = priorities


# ============================================================================
# CONCRETE INTERFACE IMPLEMENTATIONS
# ============================================================================

class LocalFilesystemInterface(FilesystemInterface):
    """Implementation of filesystem interface for local filesystem access"""
    
    def initialize(self) -> bool:
        """Initialize the interface"""
        self.logger.info("Initializing LocalFilesystemInterface")
        self.is_active = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the interface"""
        self.logger.info("Shutting down LocalFilesystemInterface")
        self.is_active = False
        return True
    
    def get_capabilities(self) -> Set[InterfaceCapability]:
        """Get capabilities provided by this interface"""
        return {
            InterfaceCapability.FILE_READ,
            InterfaceCapability.FILE_WRITE,
            InterfaceCapability.FILE_ORGANIZATION
        }
    
    def get_metadata(self) -> InterfaceMetadata:
        """Get metadata about this interface"""
        return InterfaceMetadata(
            name="Local Filesystem Interface",
            interface_type=InterfaceType.FILESYSTEM,
            capabilities=self.get_capabilities(),
            description="Provides access to the local filesystem",
            version="1.0.0",
            is_active=self.is_active,
            last_active=time.time() if self.is_active else None
        )
    
    def read_file(self, path: Union[str, pathlib.Path]) -> bytes:
        """Read a file"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.FILE_READ
        )
        
        path = pathlib.Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        return path.read_bytes()
    
    def write_file(self, path: Union[str, pathlib.Path], data: Union[bytes, str],
                  create_dirs: bool = True) -> bool:
        """Write to a file"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.FILE_WRITE
        )
        
        path = pathlib.Path(path)
        
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        if isinstance(data, str):
            path.write_text(data)
        else:
            path.write_bytes(data)
            
        return True
    
    def list_directory(self, path: Union[str, pathlib.Path]) -> List[Dict[str, Any]]:
        """List contents of a directory"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.FILE_ORGANIZATION
        )
        
        path = pathlib.Path(path)
        if not path.exists() or not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        
        result = []
        for item in path.iterdir():
            result.append({
                "name": item.name,
                "path": str(item),
                "is_file": item.is_file(),
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else None,
                "modified": item.stat().st_mtime
            })
            
        return result
    
    def create_directory(self, path: Union[str, pathlib.Path]) -> bool:
        """Create a directory"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.FILE_ORGANIZATION
        )
        
        path = pathlib.Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return True
    
    def delete(self, path: Union[str, pathlib.Path], recursive: bool = False) -> bool:
        """Delete a file or directory"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.FILE_ORGANIZATION
        )
        
        path = pathlib.Path(path)
        if not path.exists():
            return False
        
        if path.is_file():
            path.unlink()
            return True
        elif path.is_dir():
            if recursive:
                import shutil
                shutil.rmtree(path)
                return True
            else:
                try:
                    path.rmdir()  # Will fail if directory not empty
                    return True
                except OSError:
                    return False
        
        return False


class BasicNetworkInterface(NetworkInterface):
    """Basic implementation of network interface for socket communication"""
    
    def initialize(self) -> bool:
        """Initialize the interface"""
        self.logger.info("Initializing BasicNetworkInterface")
        self.is_active = True
        self.active_connections = {}  # Map of network_id -> connection info
        self.available_networks = {}  # Map of network_id -> network info
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the interface"""
        self.logger.info("Shutting down BasicNetworkInterface")
        
        # Disconnect from all networks
        for network_id in list(self.active_connections.keys()):
            self.disconnect(network_id)
            
        self.is_active = False
        return True
    
    def get_capabilities(self) -> Set[InterfaceCapability]:
        """Get capabilities provided by this interface"""
        return {
            InterfaceCapability.SOCKET_COMMUNICATION,
            InterfaceCapability.WIFI_SCANNING,
            InterfaceCapability.WIFI_CONNECTION,
            InterfaceCapability.WEB_BROWSING
        }
    
    def get_metadata(self) -> InterfaceMetadata:
        """Get metadata about this interface"""
        return InterfaceMetadata(
            name="Basic Network Interface",
            interface_type=InterfaceType.NETWORK,
            capabilities=self.get_capabilities(),
            description="Provides basic network connectivity",
            version="1.0.0",
            is_active=self.is_active,
            last_active=time.time() if self.is_active else None
        )
    
    def scan_networks(self) -> List[Dict[str, Any]]:
        """Scan for available networks"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.WIFI_SCANNING
        )
        
        # This is a simplified implementation
        # In a real implementation, we would use platform-specific methods
        # to scan for available networks
        
        # Simulate network scanning
        try:
            import socket
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            # For demonstration, we'll create a simulated network entry
            network_id = f"local_{uuid.uuid4().hex[:8]}"
            self.available_networks[network_id] = {
                "id": network_id,
                "name": "Local Network",
                "type": "LAN",
                "ip": ip,
                "signal_strength": 100,
                "secured": False
            }
            
            return list(self.available_networks.values())
        except Exception as e:
            self.logger.error(f"Error scanning networks: {e}")
            return []
    
    def connect(self, network_id: str, credentials: Optional[Dict[str, Any]] = None) -> bool:
        """Connect to a network"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.WIFI_CONNECTION
        )
        
        if network_id in self.active_connections:
            self.logger.info(f"Already connected to network {network_id}")
            return True
        
        if network_id not in self.available_networks:
            self.logger.warning(f"Network {network_id} not found")
            return False
        
        # Simulate connection
        network_info = self.available_networks[network_id]
        if network_info.get("secured", False) and not credentials:
            self.logger.warning(f"Network {network_id} requires credentials")
            return False
        
        # Create connection entry
        self.active_connections[network_id] = {
            "id": network_id,
            "connected_at": time.time(),
            "status": "connected",
            **network_info
        }
        
        self.logger.info(f"Connected to network {network_id}")
        return True
    
    def disconnect(self, network_id: str) -> bool:
        """Disconnect from a network"""
        if network_id not in self.active_connections:
            self.logger.warning(f"Not connected to network {network_id}")
            return False
        
        # Remove connection entry
        del self.active_connections[network_id]
        
        self.logger.info(f"Disconnected from network {network_id}")
        return True
    
    def get_active_connections(self) -> List[Dict[str, Any]]:
        """Get currently active network connections"""
        return list(self.active_connections.values())


class LocalSubprocessInterface(SubprocessInterface):
    """Implementation of subprocess interface for managing local processes"""
    
    def initialize(self) -> bool:
        """Initialize the interface"""
        self.logger.info("Initializing LocalSubprocessInterface")
        self.is_active = True
        self.active_processes = {}  # Map of process_id -> process info
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the interface"""
        self.logger.info("Shutting down LocalSubprocessInterface")
        
        # Terminate all processes
        for process_id in list(self.active_processes.keys()):
            self.terminate_process(process_id, force=True)
            
        self.is_active = False
        return True
    
    def get_capabilities(self) -> Set[InterfaceCapability]:
        """Get capabilities provided by this interface"""
        return {
            InterfaceCapability.SUBPROCESS_SPAWN,
            InterfaceCapability.SUBPROCESS_MANAGEMENT,
            InterfaceCapability.SUBPROCESS_TERMINATION
        }
    
    def get_metadata(self) -> InterfaceMetadata:
        """Get metadata about this interface"""
        return InterfaceMetadata(
            name="Local Subprocess Interface",
            interface_type=InterfaceType.SUBPROCESS,
            capabilities=self.get_capabilities(),
            description="Provides management of local subprocesses",
            version="1.0.0",
            is_active=self.is_active,
            last_active=time.time() if self.is_active else None
        )
    
    def spawn_process(self, command: List[str], working_dir: Optional[Union[str, pathlib.Path]] = None,
                     env: Optional[Dict[str, str]] = None, 
                     stdout_handler: Optional[Callable[[str], None]] = None,
                     stderr_handler: Optional[Callable[[str], None]] = None) -> str:
        """Spawn a subprocess"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.SUBPROCESS_SPAWN
        )
        
        # Generate process ID
        process_id = f"process_{uuid.uuid4().hex[:8]}"
        
        # Prepare environment
        process_env = os.environ.copy()
        if env:
            process_env.update(env)
        
        # Prepare working directory
        if working_dir:
            working_dir = str(working_dir)
        
        try:
            # Create process
            process = subprocess.Popen(
                command,
                cwd=working_dir,
                env=process_env,
                stdout=subprocess.PIPE if stdout_handler else None,
                stderr=subprocess.PIPE if stderr_handler else None,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Store process info
            self.active_processes[process_id] = {
                "id": process_id,
                "pid": process.pid,
                "command": command,
                "working_dir": working_dir,
                "started_at": time.time(),
                "status": "running",
                "process": process
            }
            
            # Set up output handlers if provided
            if stdout_handler and process.stdout:
                def _stdout_thread():
                    try:
                        for line in process.stdout:
                            stdout_handler(line)
                    except Exception as e:
                        self.logger.error(f"Error reading from stdout: {e}")
                
                threading.Thread(target=_stdout_thread, daemon=True).start()
            
            if stderr_handler and process.stderr:
                def _stderr_thread():
                    try:
                        for line in process.stderr:
                            stderr_handler(line)
                    except Exception as e:
                        self.logger.error(f"Error reading from stderr: {e}")
                
                threading.Thread(target=_stderr_thread, daemon=True).start()
            
            # Set up process monitoring
            def _monitor_thread():
                process.wait()
                exit_code = process.returncode
                if process_id in self.active_processes:
                    self.active_processes[process_id]["status"] = "terminated"
                    self.active_processes[process_id]["exit_code"] = exit_code
                    self.active_processes[process_id]["ended_at"] = time.time()
            
            threading.Thread(target=_monitor_thread, daemon=True).start()
            
            self.logger.info(f"Spawned process {process_id} (PID: {process.pid})")
            return process_id
        except Exception as e:
            self.logger.error(f"Error spawning process: {e}")
            raise
    
    def terminate_process(self, process_id: str, force: bool = False) -> bool:
        """Terminate a subprocess"""
        self.entity_core.adaption_engine.notify_interface_used(
            self.interface_id, InterfaceCapability.SUBPROCESS_TERMINATION
        )
        
        if process_id not in self.active_processes:
            self.logger.warning(f"Process {process_id} not found")
            return False
        
        process_info = self.active_processes[process_id]
        process = process_info["process"]
        
        if process_info["status"] != "running":
            self.logger.info(f"Process {process_id} already terminated")
            return True
        
        try:
            if force:
                process.kill()
            else:
                process.terminate()
                
            # Wait a bit to see if the process terminates
            try:
                process.wait(timeout=5)
                self.logger.info(f"Process {process_id} terminated")
            except subprocess.TimeoutExpired:
                self.logger.warning(f"Process {process_id} did not terminate within timeout")
                # Force kill if it didn't terminate
                process.kill()
                process.wait()
                self.logger.info(f"Process {process_id} forcibly killed")
            
            # Update process info
            process_info["status"] = "terminated"
            process_info["exit_code"] = process.returncode
            process_info["ended_at"] = time.time()
            
            return True
        except Exception as e:
            self.logger.error(f"Error terminating process {process_id}: {e}")
            return False
    
    def get_active_processes(self) -> Dict[str, Dict[str, Any]]:
        """Get information about active subprocesses"""
        # Return a cleaned version without the actual process objects
        result = {}
        for process_id, info in self.active_processes.items():
            # Create a copy without the process object
            cleaned_info = {k: v for k, v in info.items() if k != "process"}
            result[process_id] = cleaned_info
            
        return result


# ============================================================================
# PLUGIN SYSTEM
# ============================================================================

class PluginManager:
    """
    Manages the loading and management of plugins, which can extend the
    system's capabilities by providing new interfaces or enhancing existing ones.
    """
    
    def __init__(self, entity_core: EntityCore):
        """
        Initialize the plugin manager
        
        Args:
            entity_core: Reference to the EntityCore
        """
        self.entity_core = entity_core
        self.logger = logging.getLogger("cosmic_mind.plugin_manager")
        self.plugins = {}  # Map of plugin_id -> plugin info
        self.plugin_paths = []  # List of paths to search for plugins
    
    def add_plugin_path(self, path: Union[str, pathlib.Path]):
        """
        Add a path to search for plugins
        
        Args:
            path: Path to add
        """
        path = str(path)
        if path not in self.plugin_paths:
            self.plugin_paths.append(path)
            # Add to Python path if not already there
            if path not in sys.path:
                sys.path.append(path)
    
    def discover_plugins(self) -> List[Dict[str, Any]]:
        """
        Discover available plugins
        
        Returns:
            List[Dict[str, Any]]: List of discovered plugin information
        """
        discovered = []
        
        for path in self.plugin_paths:
            try:
                # Look for Python packages in this path
                for _, name, ispkg in pkgutil.iter_modules([path]):
                    if not ispkg:
                        continue
                    
                    # Try to load the package to check if it's a valid plugin
                    try:
                        module = importlib.import_module(name)
                        
                        # Check if it has the required plugin attributes
                        if not hasattr(module, "PLUGIN_ID") or not hasattr(module, "PLUGIN_VERSION"):
                            continue
                        
                        plugin_info = {
                            "id": getattr(module, "PLUGIN_ID"),
                            "name": getattr(module, "PLUGIN_NAME", name),
                            "version": getattr(module, "PLUGIN_VERSION"),
                            "description": getattr(module, "PLUGIN_DESCRIPTION", ""),
                            "package": name,
                            "path": path,
                            "interfaces": getattr(module, "PLUGIN_INTERFACES", []),
                            "dependencies": getattr(module, "PLUGIN_DEPENDENCIES", [])
                        }
                        
                        discovered.append(plugin_info)
                    except Exception as e:
                        self.logger.warning(f"Error examining potential plugin {name}: {e}")
            except Exception as e:
                self.logger.error(f"Error discovering plugins in {path}: {e}")
        
        return discovered
    
    def load_plugin(self, plugin_id: str) -> bool:
        """
        Load a plugin
        
        Args:
            plugin_id: ID of the plugin to load
        """
        if plugin_id in self.plugins:
            self.logger.info(f"Plugin {plugin_id} already loaded")
            return True
        
        # Find the plugin in the discovered list
        for plugin_info in self.discover_plugins():
            if plugin_info["id"] == plugin_id:
                try:
                    # Import the plugin module
                    module = importlib.import_module(plugin_info["package"])
                    
                    # Initialize the plugin (if it has an initialize method)
                    if hasattr(module, "initialize_plugin"):
                        module.initialize_plugin(self.entity_core)
                    
                    # Store the plugin info
                    self.plugins[plugin_id] = plugin_info
                    self.logger.info(f"Loaded plugin {plugin_id}")
                    return True
                except Exception as e:
                    self.logger.error(f"Error loading plugin {plugin_id}: {e}")
                    return False
        
        self.logger.warning(f"Plugin {plugin_id} not found")
        return False

    def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload a plugin
        
        Args:
            plugin_id: ID of the plugin to unload
        """
        if plugin_id not in self.plugins:
            self.logger.warning(f"Plugin {plugin_id} is not loaded")
            return False
        
        try:
            module = importlib.import_module(self.plugins[plugin_id]["package"])
            if hasattr(module, "unload_plugin"):
                module.unload_plugin()
            
            del self.plugins[plugin_id]
            self.logger.info(f"Unloaded plugin {plugin_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_id}: {e}")
            return False

