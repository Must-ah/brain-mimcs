from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol


# =============================================================================
# Path sanitization for topic construction
# =============================================================================

# Pattern for valid path components: alphanumeric, underscore, hyphen only
_VALID_PATH_COMPONENT = re.compile(r"^[a-zA-Z0-9_-]+$")


class PathValidationError(ValueError):
    """Raised when a path component fails validation."""
    pass


def sanitize_path_component(value: str, field_name: str = "value") -> str:
    """Validate and return a path component for use in topic construction.

    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)

    Returns:
        The validated string (unchanged if valid)

    Raises:
        PathValidationError: If the value contains invalid characters or patterns
    """
    if not value:
        raise PathValidationError(f"{field_name} cannot be empty")
    if ".." in value:
        raise PathValidationError(f"Path traversal pattern '..' not allowed in {field_name}: {value!r}")
    if "/" in value or "\\" in value:
        raise PathValidationError(f"Path separators not allowed in {field_name}: {value!r}")
    if not _VALID_PATH_COMPONENT.match(value):
        raise PathValidationError(
            f"{field_name} contains invalid characters (allowed: a-z, A-Z, 0-9, _, -): {value!r}"
        )
    return value


# =============================================================================
# Shared core types (Pattern A: single source of truth)
# =============================================================================

class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class Plane(str, Enum):
    SPINAL = "spinal"
    BRAINSTEM = "brainstem"
    THALAMUS = "thalamus"
    CORTEX = "cortex"
    RELIABLE = "reliable"
    REFLECT = "reflect"
    UNKNOWN = "unknown"


class MessageType(str, Enum):
    # Spinal
    AFFERENT_SIGNAL = "AfferentSignal"
    EFFERENT_COMMAND = "EfferentCommand"
    OUTCOME_EVENT = "OutcomeEvent"
    REFLEX_RULE = "ReflexRule"
    REFLEX_TRIGGER = "ReflexTrigger"
    REFLEX_EVENT = "ReflexEvent"

    # Brainstem
    RELAY_BUNDLE = "RelayBundle"
    PATTERN_TRIGGER = "PatternTrigger"
    PATTERN_RESPONSE = "PatternResponse"
    GLOBAL_BROADCAST = "GlobalBroadcast"

    # Ops
    REJECT_EVENT = "RejectEvent"


@dataclass(frozen=True)
class Meta:
    message_type: MessageType
    schema_version: str
    origin_plane: Plane
    timestamp_ms: int
    correlation_id: Optional[str] = None
    source: Optional[str] = None


@dataclass(frozen=True)
class RejectEvent:
    meta: Meta
    reason: str
    original_topic: str
    publisher_id: Optional[str]
    details: Mapping[str, Any]


# =============================================================================
# Shared bus protocol + reference in-memory bus (for tests/demos)
# =============================================================================

class TopicBus(Protocol):
    async def publish(self, topic: str, msg: Any) -> None: ...
    def subscribe(self, topic: str) -> AsyncIterator[Any]: ...


class InMemoryTopicBus:
    """Minimal async topic bus for local tests/demos (not a real MQTT broker).

    Rate limiting: Default max queue size of 1000 prevents memory exhaustion.
    When queue is full, oldest messages are dropped (backpressure).
    """
    DEFAULT_MAX_QUEUE_SIZE = 1000

    def __init__(self, max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE) -> None:
        import asyncio
        self._asyncio = asyncio
        self._subs: Dict[str, List[asyncio.Queue[Any]]] = {}
        self._max_queue_size = max_queue_size

    async def publish(self, topic: str, msg: Any) -> None:
        for q in self._subs.get(topic, []):
            if q.full():
                # Drop oldest message to make room (backpressure)
                try:
                    q.get_nowait()
                except self._asyncio.QueueEmpty:
                    pass
            await q.put(msg)

    def subscribe(self, topic: str, max_queue: Optional[int] = None) -> AsyncIterator[Any]:
        queue_size = max_queue if max_queue is not None else self._max_queue_size
        q: "self._asyncio.Queue[Any]" = self._asyncio.Queue(maxsize=queue_size)
        self._subs.setdefault(topic, []).append(q)

        async def _iter() -> AsyncIterator[Any]:
            try:
                while True:
                    yield await q.get()
            finally:
                subs = self._subs.get(topic, [])
                if q in subs:
                    subs.remove(q)

        return _iter()
