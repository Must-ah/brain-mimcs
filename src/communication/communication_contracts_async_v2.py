from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# =============================================================================
# Lanes + envelope (control/event plane) + media identifiers (data plane)
# =============================================================================

class Lane(str, Enum):
    A_DRIVER = "A_DRIVER"
    B_MODULATOR = "B_MODULATOR"
    C_COMMAND = "C_COMMAND"
    D_GLOBAL = "D_GLOBAL"
    E_ERROR = "E_ERROR"
    G_GATE = "G_GATE"
    X_REFLECT = "X_REFLECT"

    # Media lanes (data plane): negotiated sessions, not raw bus flooding
    V_VIDEO = "V_VIDEO"
    U_AUDIO = "U_AUDIO"


class SignalKind(str, Enum):
    DRIVER = "driver"
    MODULATOR = "modulator"


class GateMode(str, Enum):
    MULTI = "multi"
    WINNER_TAKE_ALL = "winner_take_all"


class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class NucleusId(str, Enum):
    LGN = "lgn"
    MGN = "mgn"
    VPL = "vpl"
    VPM = "vpm"
    PULVINAR = "pulvinar"
    MD = "md"
    TRN = "trn"


@dataclass(frozen=True)
class Envelope:
    # Control/Event plane envelope
    lane: Lane
    kind: SignalKind
    scope_level: ScopeLevel
    scope: str
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]

    nucleus: Optional[NucleusId] = None

    priority: Optional[int] = None
    salience: Optional[float] = None
    deadline_ms: Optional[int] = None
    confidence: Optional[float] = None

    schema_version: str = "v1"
    payload: Mapping[str, Any] = None  # type: ignore[assignment]


@dataclass(frozen=True)
class GateState:
    scope_level: ScopeLevel
    scope: str
    nucleus: NucleusId
    inhibition: float                 # 0..1
    mode: Optional[GateMode] = None
    reason: Optional[str] = None
    timestamp_ms: int = 0
    expires_at_ms: Optional[int] = None


# =============================================================================
# Protocols (pure async)
# =============================================================================

class TopicBus(Protocol):
    async def publish(self, topic: str, msg: Any) -> None: ...
    def subscribe(self, topic: str) -> AsyncIterator[Any]: ...


class GateStore(Protocol):
    async def get(self, scope_level: ScopeLevel, scope: str, nucleus: NucleusId, now_ms: int) -> Optional[GateState]: ...
    async def put(self, state: GateState) -> None: ...


# =============================================================================
# Topic naming helpers
# =============================================================================

def topic_for(env: Envelope) -> str:
    """Transport-agnostic naming.

    Note: Media lanes (V_VIDEO/U_AUDIO) are session-based and not intended for the same bus.
    """
    if env.lane in (Lane.V_VIDEO, Lane.U_AUDIO):
        raise ValueError("Media lanes are session-based; do not route raw media via topic_for().")

    base = f"/{env.lane.value}/{env.kind.value}/{env.scope_level.value}/{env.scope}"

    if env.lane in (Lane.A_DRIVER, Lane.B_MODULATOR, Lane.G_GATE):
        if env.nucleus is None:
            raise ValueError("nucleus is required for A/B/G lanes")
        return f"{base}/nucleus/{env.nucleus.value}"

    if env.lane == Lane.X_REFLECT:
        src_lane = (env.payload or {}).get("src_lane", "unknown")
        return f"{base}/lane/{src_lane}"

    return base


def reflect_of(env: Envelope, now_ms: int, reflector: str = "reflector") -> Envelope:
    """Create a non-blocking reflection copy of a message into Lane X."""
    return Envelope(
        lane=Lane.X_REFLECT,
        kind=env.kind,
        scope_level=env.scope_level,
        scope=env.scope,
        timestamp_ms=now_ms,
        correlation_id=env.correlation_id,
        source=reflector,
        nucleus=env.nucleus,
        priority=env.priority,
        salience=env.salience,
        deadline_ms=env.deadline_ms,
        confidence=env.confidence,
        schema_version=env.schema_version,
        payload={
            "src_lane": env.lane.value,
            "src_source": env.source,
            "src_timestamp_ms": env.timestamp_ms,
            "envelope": {
                "lane": env.lane.value,
                "kind": env.kind.value,
                "scope_level": env.scope_level.value,
                "scope": env.scope,
                "nucleus": env.nucleus.value if env.nucleus else None,
                "priority": env.priority,
                "salience": env.salience,
                "deadline_ms": env.deadline_ms,
                "confidence": env.confidence,
                "schema_version": env.schema_version,
            },
            "payload_copy": dict(env.payload or {}),
        },
    )


# =============================================================================
# Reference in-memory bus + stores (for tests)
# =============================================================================

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


class InMemoryGateStore:
    def __init__(self) -> None:
        self._m: Dict[Tuple[ScopeLevel, str, NucleusId], GateState] = {}

    async def get(self, scope_level: ScopeLevel, scope: str, nucleus: NucleusId, now_ms: int) -> Optional[GateState]:
        st = self._m.get((scope_level, scope, nucleus))
        if st is None:
            return None
        if st.expires_at_ms is not None and now_ms >= st.expires_at_ms:
            return None
        return st

    async def put(self, state: GateState) -> None:
        self._m[(state.scope_level, state.scope, state.nucleus)] = state
