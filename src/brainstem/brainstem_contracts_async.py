from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# =============================================================================
# Shared enums + message contracts (transport-agnostic, pure async friendly)
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


# ---- Spinal contracts ----

@dataclass(frozen=True)
class AfferentSignal:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    sensor_type: str
    payload: Mapping[str, Any]
    units: Optional[str] = None
    confidence: Optional[float] = None
    salience: Optional[float] = None


@dataclass(frozen=True)
class EfferentCommand:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    actuator_type: str
    action_id: str  # idempotency key
    payload: Mapping[str, Any]
    deadline_ms: Optional[int] = None
    priority: Optional[int] = None
    safety_constraints: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class OutcomeEvent:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    action_id: str
    status: str  # ack|in_progress|done|failed
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexRule:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexTrigger:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexEvent:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    action_id: str
    payload: Mapping[str, Any]


# ---- Brainstem contracts ----

@dataclass(frozen=True)
class RelayBundle:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    channel: str               # somatic|auditory|visual_orient|visceral|...
    window_ms: int
    summary_features: Mapping[str, Any]
    sources: Optional[Sequence[str]] = None
    salience: Optional[float] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class PatternTrigger:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    pattern_type: str          # startle|orient|stabilize|...
    urgency: float             # 0..1
    deadline_ms: Optional[int]
    trigger: Mapping[str, Any]


@dataclass(frozen=True)
class PatternResponse:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    pattern_type: str
    request_id: Optional[str]
    status: str                # accepted|ignored|done|failed
    recommendation: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class GlobalBroadcast:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    state: Mapping[str, Any]   # e.g., {"high_alert": True}
    half_life_ms: Optional[int] = None
    expires_at_ms: Optional[int] = None


# ---- Reject / quarantine ----

@dataclass(frozen=True)
class RejectEvent:
    meta: Meta
    reason: str
    original_topic: str
    publisher_id: Optional[str]
    details: Mapping[str, Any]


# =============================================================================
# Topic helpers (names match the specs you downloaded)
# =============================================================================

def topic_sc_aff(scope_level: ScopeLevel, scope: str, sensor_type: str, device_id: str) -> str:
    return f"/sc/aff/{scope_level.value}/{scope}/sensor/{sensor_type}/device/{device_id}"


def topic_sc_eff(scope_level: ScopeLevel, scope: str, actuator_type: str, device_id: str, action_id: str) -> str:
    return f"/sc/eff/{scope_level.value}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}"


def topic_sc_out(scope_level: ScopeLevel, scope: str, device_id: str, action_id: str) -> str:
    return f"/sc/out/{scope_level.value}/{scope}/device/{device_id}/action/{action_id}"


def topic_sc_reflex_config(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    return f"/sc/reflex/{scope_level.value}/{scope}/rule/{reflex_id}/configure"


def topic_sc_reflex_trigger(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    return f"/sc/reflex/{scope_level.value}/{scope}/rule/{reflex_id}/trigger"


def topic_bs_relay(scope_level: ScopeLevel, scope: str, channel: str) -> str:
    return f"/bs/relay/{scope_level.value}/{scope}/channel/{channel}"


def topic_bs_pattern_trigger(scope_level: ScopeLevel, scope: str, pattern_type: str) -> str:
    return f"/bs/pattern/{scope_level.value}/{scope}/{pattern_type}/trigger"


def topic_bs_global_alert(scope_level: ScopeLevel, scope: str) -> str:
    return f"/bs/global/{scope_level.value}/{scope}/alert"


def topic_reflect_reject(scope_level: ScopeLevel, scope: str) -> str:
    return f"/X/reflect/{scope_level.value}/{scope}/lane/reject"


# =============================================================================
# Minimal async bus (for tests / local demos)
# =============================================================================

class TopicBus(Protocol):
    async def publish(self, topic: str, msg: Any) -> None: ...
    def subscribe(self, topic: str) -> AsyncIterator[Any]: ...


class InMemoryTopicBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[asyncio.Queue[Any]]] = {}

    async def publish(self, topic: str, msg: Any) -> None:
        for q in self._subs.get(topic, []):
            await q.put(msg)

    def subscribe(self, topic: str) -> AsyncIterator[Any]:
        q: asyncio.Queue[Any] = asyncio.Queue()
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



# =============================================================================
# Brainstem (transform + typed relay; reject-on-wrong-type)
# =============================================================================

class Brainstem:
    """Brainstem plane façade.

    - Ingests AfferentSignal (from Spinal) and transforms into RelayBundle (typed summaries)
    - Ingests PatternTrigger / GlobalBroadcast (if you choose)
    - Rejects device-level efferent commands and GateState-like messages by type
    """

    ALLOWED_INBOUND: Tuple[MessageType, ...] = (
        MessageType.AFFERENT_SIGNAL,
        MessageType.PATTERN_TRIGGER,
        MessageType.GLOBAL_BROADCAST,
        MessageType.RELAY_BUNDLE,  # optional internal coordination
    )

    def __init__(
        self,
        core_bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str = "brainstem",
        default_window_ms: int = 200,
    ) -> None:
        self._bus = core_bus
        self._reflect = reflect_bus
        self._publisher_id = publisher_id
        self._window_ms = default_window_ms

    async def ingest(self, topic: str, msg: Any) -> None:
        mt = getattr(getattr(msg, "meta", None), "message_type", None)
        if mt not in self.ALLOWED_INBOUND:
            await self._reject(topic, msg, reason="wrong_type_or_missing_meta")
            return

        # Contract-only skeleton: real implementation would aggregate/transform.
        # We still provide a *single* helper method to publish a RelayBundle.
        return

    async def publish_relay_bundle(self, bundle: RelayBundle) -> None:
        await self._bus.publish(topic_bs_relay(bundle.scope_level, bundle.scope, bundle.channel), bundle)

    async def _reject(self, topic: str, msg: Any, reason: str) -> None:
        now_ms = getattr(getattr(msg, "meta", None), "timestamp_ms", 0) or 0
        scope_level = getattr(msg, "scope_level", None) or ScopeLevel.HOUSE
        scope = getattr(msg, "scope", None) or "unknown"

        rej = RejectEvent(
            meta=Meta(
                message_type=MessageType.REJECT_EVENT,
                schema_version="v1",
                origin_plane=Plane.BRAINSTEM,
                timestamp_ms=int(now_ms),
                correlation_id=getattr(getattr(msg, "meta", None), "correlation_id", None),
                source=self._publisher_id,
            ),
            reason=reason,
            original_topic=topic,
            publisher_id=getattr(getattr(msg, "meta", None), "source", None),
            details={
                "observed_type": str(getattr(getattr(msg, "meta", None), "message_type", None)),
                "hint": "Brainstem accepts AfferentSignal (for transformation), RelayBundle, PatternTrigger, GlobalBroadcast.",
            },
        )
        await self._reflect.publish(topic_reflect_reject(scope_level, scope), rej)
