# src/infrastructure/observability.py
"""
Observability and Monitoring Infrastructure

Provides comprehensive monitoring and tracing capabilities with:
- Distributed tracing
- Anomaly detection
- Emergency response coordination
"""

from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, validator
import asyncio
from datetime import datetime
import json
import logging

_LOGGER = logging.getLogger("biocognitive_observability")
_EXCEPTION_REGISTRY: Dict[str, str] = {}


def register_exception_class(exc_type: type) -> None:
    """Register exception types for observability."""
    _EXCEPTION_REGISTRY[exc_type.__name__] = f"{exc_type.__module__}.{exc_type.__name__}"


def log_metric(payload: Any) -> None:
    """Log metric payloads emitted by collectors."""
    _LOGGER.info("metrics=%s", payload)


def log_trace(payload: Any) -> None:
    """Log tracing payloads."""
    _LOGGER.debug("trace=%s", payload)


def log_error(message: str, error: Exception) -> None:
    """Log errors with structured context."""
    _LOGGER.error("error=%s type=%s detail=%s", message, type(error).__name__, error)


def log_event(event_type: str, metadata: Dict[str, Any] = None) -> None:
    """Log events with structured context for observability."""
    if metadata is None:
        metadata = {}
    _LOGGER.info("event=%s metadata=%s timestamp=%s", event_type, metadata, datetime.utcnow().isoformat())


def log_exception(exc: Exception) -> None:
    """Log exception objects with structured context."""
    _LOGGER.error("exception=%s detail=%s", type(exc).__name__, exc)

class ObservabilityEngine:
    """Central monitoring and tracing system"""
    def __init__(self):
        self.logger = logging.getLogger("biocognitive_observability")
        self.tracing_enabled = True
        from rosemary.biocognitive_core.metrics import SISMetrics, NTPMetrics, SECTMetrics
        self.metrics_collector = {
            "SIS": SISMetrics(),
            "NTP": NTPMetrics(),
            "SECT": SECTMetrics(),
        }

    def log_event(self, event_type: str, metadata: Dict):
        """Standardized event logging"""
        log_record = {
            "type": event_type,
            "metadata": metadata,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._log(log_record)

    def log_error(self, message: str, error: Exception):
        """Standardized error logging"""
        log_record = {
            "type": "error",
            "message": message,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat()
        }
        self._log(log_record)

    def _log(self, record: Dict):
        """Internal logging implementation"""
        if self.tracing_enabled:
            # In production, this would send to distributed tracing system
            print(json.dumps(record))  # Placeholder for demonstration

    def get_metrics(self, component: str) -> Dict:
        """Retrieve component-specific metrics"""
        if component not in self.metrics_collector:
            raise ValueError(f"Unknown component: {component}")
            
        collector = self.metrics_collector[component]
        if hasattr(collector, 'get_all_metrics'):
            return collector.get_all_metrics()
        return {}

    async def start_tracing(self):
        """Initialize distributed tracing"""
        self.tracing_enabled = True
        self._flush_task = asyncio.create_task(self._periodic_metric_flush())

    async def stop_tracing(self):
        """Stop distributed tracing and cleanup"""
        self.tracing_enabled = False
        if hasattr(self, '_flush_task') and self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
            self._flush_task = None
        self.logger.info("Tracing stopped")

    async def _periodic_metric_flush(self):
        """Periodically flush metrics to monitoring system"""
        while self.tracing_enabled:
            try:
                for component, collector in self.metrics_collector.items():
                    if hasattr(collector, 'get_all_metrics'):
                        metrics = collector.get_all_metrics()
                        if metrics:
                            self.log_event(f"{component}_metrics", metrics)
                await asyncio.sleep(10)  # 10-second flush interval
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.warning(f"Metric flush error: {e}")


class LoggerFactory:
    """Factory for creating structured loggers"""
    _loggers: Dict[str, logging.Logger] = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger with the given name"""
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
                logger.addHandler(handler)
            cls._loggers[name] = logger
        return cls._loggers[name]


class Tracer:
    """Simple tracer for distributed tracing"""
    def __init__(self, name: str):
        self.name = name
        self.spans: List[Dict[str, Any]] = []
    
    def start_span(self, operation_name: str) -> 'SpanContext':
        return SpanContext(self, operation_name)
    
    def record_span(self, span_data: Dict[str, Any]):
        self.spans.append(span_data)

    def start_as_current_span(self, operation_name: str) -> '_SpanScope':
        """OpenTelemetry-compatible entry point: usable as ``with`` block or as a
        decorator on sync/async callables. Each entry records one span."""
        return _SpanScope(self, operation_name)


class _SpanScope:
    """Context manager + decorator; opens a fresh SpanContext per entry/call."""
    def __init__(self, tracer: 'Tracer', operation_name: str):
        self.tracer = tracer
        self.operation_name = operation_name
        self._active: List['SpanContext'] = []

    def __enter__(self) -> 'SpanContext':
        span = SpanContext(self.tracer, self.operation_name)
        self._active.append(span)
        return span.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._active.pop().__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        import functools
        import inspect
        tracer, name = self.tracer, self.operation_name
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with SpanContext(tracer, name):
                    return await func(*args, **kwargs)
            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with SpanContext(tracer, name):
                return func(*args, **kwargs)
        return wrapper


class SpanContext:
    """Context manager for tracing spans"""
    def __init__(self, tracer: Tracer, operation_name: str):
        self.tracer = tracer
        self.operation_name = operation_name
        self.start_time: Optional[float] = None
        self.attributes: Dict[str, Any] = {}
    
    def __enter__(self) -> 'SpanContext':
        import time
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        end_time = time.time()
        self.tracer.record_span({
            'operation': self.operation_name,
            'start_time': self.start_time,
            'end_time': end_time,
            'duration': end_time - self.start_time if self.start_time else 0,
            'attributes': self.attributes,
            'error': str(exc_val) if exc_val else None
        })
        return False
    
    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value


_TRACERS: Dict[str, Tracer] = {}


def get_tracer(name: str) -> Tracer:
    """Get or create a tracer with the given name"""
    if name not in _TRACERS:
        _TRACERS[name] = Tracer(name)
    return _TRACERS[name]