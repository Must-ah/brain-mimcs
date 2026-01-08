from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol


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
    """Minimal async topic bus for local tests/demos (not a real MQTT broker)."""

    def __init__(self) -> None:
        import asyncio
        self._asyncio = asyncio
        self._subs: Dict[str, List[asyncio.Queue[Any]]] = {}

    async def publish(self, topic: str, msg: Any) -> None:
        for q in self._subs.get(topic, []):
            await q.put(msg)

    def subscribe(self, topic: str) -> AsyncIterator[Any]:
        q: "self._asyncio.Queue[Any]" = self._asyncio.Queue()
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
