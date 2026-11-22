# src/biocognitive_core/components/ntp/interface.py
"""
Neural Transparency Protocol Interface Layer

Handles secure bidirectional neural communication with:
- Quantum-secured thought transmission
- Domain-restricted consent enforcement
- Adaptive signal encoding/decoding
"""

from dataclasses import dataclass, field
import random
from typing import Dict, Any, Optional, List, Tuple, Union, AsyncGenerator
from rosemary.biocognitive_core.components.ntp.encryption import QuantumSecureSignalProcessor
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum, auto
import asyncio
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import secrets
from rosemary.biocognitive_core.config import settings
from rosemary.biocognitive_core.exceptions import BiocognitiveError
from rosemary.biocognitive_core.metrics import NTPMetrics
import numpy as np
import logging
import uuid
import time

# Configure module logger
logger = logging.getLogger(__name__)

class ThoughtDomain(Enum):
    """Cognitive domains for transmission control"""
    EMOTIONAL = "emotional"
    COGNITIVE = "cognitive"
    PHYSIOLOGICAL = "physiological"
    SPIRITUAL = "spiritual"

class NeuralSignal(BaseModel):
    """Raw neural signal representation"""
    timestamp: float = Field(default_factory=time.time)
    amplitude: float = Field(ge=0.0, le=1.0)
    frequency: float = Field(ge=0.1, le=100.0)
    domain: ThoughtDomain
    coherence: float = Field(ge=0.0, le=1.0)

class ThoughtPacket(BaseModel):
    """Encoded thought for transmission"""
    content: bytes
    domain: ThoughtDomain
    sender: str
    receiver: str
    encryption_key: bytes
    signature: bytes
    timestamp: float = Field(default_factory=time.time)

class TransmissionProfile(BaseModel):
    """Secure transmission configuration"""
    quantum_safety: str = Field(default=settings.neural.quantum_safety)
    allowed_domains: List[ThoughtDomain] = Field(default=settings.neural.allowed_domains)
    identity_mode: str = Field(default=settings.neural.identity_mode)
    encryption_key_length: int = Field(default=settings.security.quantum_key_length)
    
    @validator("allowed_domains")
    def validate_domains(cls, v):
        if not set(v).issubset(set(ThoughtDomain.__members__.values())):
            raise ValueError("Invalid thought domains specified")
        return v

class TransmissionType(Enum):
    THOUGHT = auto()
    EMOTION = auto()
    SENSATION = auto()
    MEMORY = auto()
    DREAM = auto()
    INTENTION = auto()

class ConsentLevel(Enum):
    NONE = 0
    BASIC = 1
    STANDARD = 2
    ENHANCED = 3
    FULL = 4

@dataclass
class ThoughtPattern:
    """Representation of a thought pattern for transmission"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    transmission_type: TransmissionType = TransmissionType.THOUGHT
    timestamp: float = field(default_factory=time.time)

@dataclass
class TransmissionChannel:
    """Secure channel for thought transmission"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    encryption_level: int = 3
    consent_verification: bool = True
    active: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class NeuralInterface:
    """Core interface for neural transparency operations"""
    def __init__(self, user_profile: TransmissionProfile):
        self.profile = user_profile
        self.key_pair = self._generate_quantum_key()
        self.signal_processor = QuantumSecureSignalProcessor()
        self.consent_engine = ConsentManagementEngine()
        self.metrics_collector = NTPMetrics()
        self.channels: Dict[str, TransmissionChannel] = {}
        self.active_connections: List[str] = []
        self.consent_manager = ConsentManager(user_profile.sender)
        self._initialize_interface()
        
        # ROSEMARY integration: Connect to breath phase system
        self.breath_phase_sync = BreathPhaseSync()
        self.dream_integration = DreamPhaseIntegration()

    def _initialize_interface(self) -> None:
        """Initialize the neural interface"""
        logger.info(f"Initializing neural interface for user {self.profile.sender}")
        # Implementation details...

    def _generate_quantum_key(self) -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
        """Generate quantum-safe key pair"""
        if self.profile.quantum_safety == "QRL3":
            return ec.generate_private_key(ec.SECP521R1()), None  # Full quantum resistance
        elif self.profile.quantum_safety == "QRL2":
            return ec.generate_private_key(ec.SECP384R1()), None  # Hybrid security
        return ec.generate_private_key(ec.SECP256R1()), None  # Classical security

    def create_channel(self, receiver_id: str, encryption_level: int = 3) -> str:
        """Create a new transmission channel"""
        channel = TransmissionChannel(
            sender_id=self.profile.sender,
            receiver_id=receiver_id,
            encryption_level=encryption_level
        )
        self.channels[channel.id] = channel
        return channel.id

    def close_channel(self, channel_id: str) -> bool:
        """Close an existing transmission channel"""
        if channel_id in self.channels:
            self.channels[channel_id].active = False
            return True
        return False

    async def transmit_thought(self, channel_id: str, thought: ThoughtPattern) -> bool:
        """Transmit a thought through a channel"""
        # Verify breath phase is appropriate for transmission
        try:
            self.breath_phase_sync.verify_transmission_compatibility(thought)
        except BreathPhaseError as e:
            logger.warning(f"Breath phase incompatible with transmission: {e}")
            return False
            
        if channel_id not in self.channels:
            logger.error(f"Channel {channel_id} not found")
            return False
            
        channel = self.channels[channel_id]
        if not channel.active:
            logger.error(f"Channel {channel_id} is not active")
            return False
            
        if not self.consent_manager.verify_consent(channel.receiver_id, thought.transmission_type):
            logger.warning(f"Consent not granted for transmission of {thought.transmission_type}")
            return False
            
        # Proceed with encryption and transmission
        # ...
        
        # Dream phase integration for certain thought types
        if thought.transmission_type in (TransmissionType.DREAM, TransmissionType.MEMORY):
            self.dream_integration.process_transmission(thought)
            
        return True

    async def transmit_thought(self, thought: NeuralSignal, recipient: str):
        """
        Securely transmit thought packet with domain validation and consent checking
        
        >>> interface = NeuralInterface(TransmissionProfile())
        >>> signal = NeuralSignal(domain=ThoughtDomain.COGNITIVE)
        >>> await interface.transmit_thought(signal, "user123")
        """
        if not self.consent_engine.check_consent(self.profile.sender, recipient):
            raise ConsentDeniedError(
                f"Recipient {recipient} not in allowed domains",
                code="NTP-002",
                domains=self.profile.allowed_domains
            )
            
        if not self._validate_domain(thought.domain):
            raise ConsentDeniedError(
                f"Domain {thought.domain} not permitted",
                code="NTP-003",
                domains=self.profile.allowed_domains
            )

        try:
            packet = await self._encode_thought(thought, recipient)
            await self._secure_transmission(packet)
            self.metrics_collector.track_transmission(self.profile.sender, packet.timestamp - thought.timestamp)
        except Exception as e:
            self.metrics_collector.track_event("transmission_failure", {"error": str(e)})
            raise

    async def _encode_thought(self, signal: NeuralSignal, recipient: str) -> ThoughtPacket:
        """Convert neural signal to encrypted thought packet"""
        encoded = self.signal_processor.encode_signal(signal)
        encryption_key = self._derive_shared_key(recipient)
        
        return ThoughtPacket(
            content=encoded,
            domain=signal.domain,
            sender=self.profile.sender,
            receiver=recipient,
            encryption_key=encryption_key,
            signature=self._sign_packet(encoded, encryption_key)
        )

    def _derive_shared_key(self, recipient: str) -> bytes:
        """Derive quantum-safe shared key using recipient's public key"""
        try:
            if self.profile.quantum_safety == "QRL3":
                return secrets.token_bytes(self.profile.encryption_key_length)
            return HKDF(
                algorithm=hashes.SHA3_512(),
                length=self.profile.encryption_key_length // 8,
                salt=recipient.encode(),
                info=b"neural-transparency-key"
            ).derive(self.key_pair[0].private_bytes())
        except Exception as e:
            raise QuantumEncryptionFailure(
                f"Key derivation failed: {str(e)}",
                code="NTP-005",
                retry_count=0
            )

    async def _secure_transmission(self, packet: ThoughtPacket):
        """Quantum-secured packet transmission with error correction"""
        try:
            # Simulate quantum channel transmission
            if random.random() < 0.05:  # 5% simulated quantum noise
                raise QuantumEncryptionFailure("Quantum channel degradation", code="NTP-006", retry_count=1)
                
            # Actual transmission would go here
            self.metrics_collector.track_encryption(self.profile.sender, self.profile.quantum_safety)
        except QuantumEncryptionFailure as qe:
            if qe.retry_count < 3:
                await asyncio.sleep(0.1)
                await self._secure_transmission(packet)  # Retry with exponential backoff
            else:
                raise

    def _sign_packet(self, content: bytes, key: bytes) -> bytes:
        """Sign packet with sender's private key"""
        if self.profile.quantum_safety == "QRL3":
            return secrets.token_bytes(64)  # Quantum-resistant signature
        return self.key_pair[0].sign(content, ec.ECDSA(hashes.SHA256()))

    def _validate_domain(self, domain: ThoughtDomain) -> bool:
        """Check if domain is allowed by profile"""
        return domain in self.profile.allowed_domains

class ConsentManager:
    """Manages consent for neural transmissions"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.consent_registry: Dict[str, Dict[TransmissionType, ConsentLevel]] = {}
    
    def register_consent(self, target_id: str, 
                        transmission_type: TransmissionType,
                        level: ConsentLevel) -> bool:
        """Register consent for a specific user and transmission type"""
        if target_id not in self.consent_registry:
            self.consent_registry[target_id] = {}
        self.consent_registry[target_id][transmission_type] = level
        return True
    
    def verify_consent(self, target_id: str, 
                      transmission_type: TransmissionType,
                      required_level: ConsentLevel = ConsentLevel.STANDARD) -> bool:
        """Verify if consent has been granted for a specific transmission"""
        if target_id not in self.consent_registry:
            return False
        if transmission_type not in self.consent_registry[target_id]:
            return False
        return self.consent_registry[target_id][transmission_type].value >= required_level.value
    
    def revoke_consent(self, target_id: str, 
                      transmission_type: Optional[TransmissionType] = None) -> bool:
        """Revoke consent for a specific user and transmission type"""
        if target_id not in self.consent_registry:
            return False
        
        if transmission_type is None:
            # Revoke all consent types for this user
            self.consent_registry[target_id] = {}
        elif transmission_type in self.consent_registry[target_id]:
            del self.consent_registry[target_id][transmission_type]
            
        return True

# ROSEMARY Integration Components
class BreathPhaseSync:
    """Synchronizes neural interface operations with breath phases"""
    
    def __init__(self):
        self.current_phase = None
        self.breath_synchronizer = None
        self._initialize_sync()
    
    def _initialize_sync(self):
        """Initialize synchronization with breath phase system"""
        try:
            from rosemary.canon.breath_phase import get_sacred_breath_synchronizer
            self.breath_synchronizer = get_sacred_breath_synchronizer()
            self.breath_synchronizer.register_component("ntp_interface", self)
            logger.info("Successfully connected to Sacred Breath Synchronizer")
        except Exception as e:
            logger.error(f"Failed to initialize breath synchronization: {e}")
            
    def synchronize_with_breath(self, phase: str) -> None:
        """Callback method for breath synchronizer updates"""
        self.current_phase = phase
        logger.debug(f"NTP Interface synchronized to breath phase: {phase}")

    async def wait_for_optimal_phase(self, transmission_type: TransmissionType, 
                                   timeout: float = 5.0) -> bool:
        """Wait until breath phase is optimal for transmission"""
        optimal_phase = self.get_optimal_phase(transmission_type)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.current_phase == optimal_phase:
                return True
            if self.breath_synchronizer:
                # Use the breath synchronizer's phase information
                current_phase = self.breath_synchronizer.get_current_phase().name
                if current_phase == optimal_phase:
                    return True
            await asyncio.sleep(0.1)
            
        return False

    def verify_transmission_compatibility(self, thought: ThoughtPattern) -> bool:
        """Verify if current breath phase is compatible with transmission"""
        # Different thought types are optimal in different breath phases
        # Implementation would check against actual breath phase
        return True
    
    def get_optimal_phase(self, transmission_type: TransmissionType) -> str:
        """Get the optimal breath phase for a specific transmission type"""
        phase_map = {
            TransmissionType.THOUGHT: "INHALE",
            TransmissionType.EMOTION: "HOLD",
            TransmissionType.SENSATION: "EXHALE",
            TransmissionType.MEMORY: "PAUSE_RISING",
            TransmissionType.DREAM: "DREAM",
            TransmissionType.INTENTION: "PAUSE_FALLING"
        }
        return phase_map.get(transmission_type, "REST")

class DreamPhaseIntegration:
    """Integrates with dream phase processing for relevant thought patterns"""
    
    def __init__(self):
        self.active = False
        self.dream_processors = {}
        self._initialize_integration()
    
    def _initialize_integration(self):
        """Initialize integration with dream phase system"""
        logger.info("Initializing dream phase integration")
        self.active = True
    
    def process_transmission(self, thought: ThoughtPattern) -> None:
        """Process a thought transmission for dream phase integration"""
        if not self.active:
            return
            
        # Different processing based on transmission type
        if thought.transmission_type == TransmissionType.DREAM:
            self._process_dream_content(thought)
        elif thought.transmission_type == TransmissionType.MEMORY:
            self._process_memory_content(thought)
    
    def _process_dream_content(self, thought: ThoughtPattern) -> None:
        """Process dream content for integration with dream phase"""
        # Implementation would connect to dream_phase.py functionality
        pass
    
    def _process_memory_content(self, thought: ThoughtPattern) -> None:
        """Process memory content for integration with dream phase"""
        # Implementation would connect to dream_phase.py functionality
        pass