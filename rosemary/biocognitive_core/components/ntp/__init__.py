"""
Neural Transparency Protocol (NTP) Component.

This package implements the NTP component of the biocognitive framework,
which provides secure bidirectional brain-computer interfaces enabling
thought transmission.
"""

from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

__all__: List[str] = []


def _safe_import(module_name: str, symbols: List[str]) -> None:
    module = __import__(f"{__name__}.{module_name}", fromlist=symbols)
    missing = [s for s in symbols if not hasattr(module, s)]
    if missing:
        raise ImportError(f"NTP {module_name} does not define: {', '.join(missing)}")
    for symbol in symbols:
        globals()[symbol] = getattr(module, symbol)
        __all__.append(symbol)


_safe_import("encryption", ["QuantumSecureSignalProcessor", "QuantumEncryption"])

if os.getenv("BIOC_NTP_IMPORT_ALL") == "1":
    _safe_import(
        "interface",
        [
            "ThoughtDomain",
            "NeuralSignal",
            "ThoughtPacket",
            "TransmissionProfile",
            "NeuralInterface",
        ],
    )
    _safe_import(
        "consent",
        [
            "ConsentStatus",
            "ConsentScope",
            "ConsentRecord",
            "ConsentRepository",
            "DatabaseConsentRepository",
            "ConsentEngine",
        ],
    )
    _safe_import(
        "receiver",
        [
            "NeuralReceiver",
            "ReceiverMode",
            "SignalQuality",
            "ThoughtDecoder",
            "TransparencySession",
        ],
    )


def initialize_ntp() -> bool:
    """Initialize NTP component and verify correct setup."""
    from rosemary.biocognitive_core.metrics import NTPMetrics

    metrics = NTPMetrics()
    metrics.initialize_collectors()
    return True


if os.getenv("BIOC_NTP_VALIDATE_IMPORT") == "1":
    initialize_ntp()
