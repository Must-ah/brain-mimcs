from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# =============================================================================
# Lane + Envelope contracts
# =============================================================================

class Lane(str, Enum):
    A_DRIVER = "A_DRIVER"
    B_MODULATOR = "B_MODULATOR"
    C_COMMAND = "C_COMMAND"
    D_GLOBAL = "D_GLOBAL"
    E_ERROR = "E_ERROR"
    G_GATE = "G_GATE"


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
    # Keep extensible; start with a small set
    LGN = "lgn"
    MGN = "mgn"
    VPL = "vpl"
    VPM = "vpm"
    VL = "vl"
    VA = "va"
    PULVINAR = "pulvinar"
    MD = "md"
    LP = "lp"
    CM = "cm"
    PF = "pf"
    TRN = "trn"


@dataclass(frozen=True)
class Envelope:
    lane: Lane
    kind: SignalKind
    scope_level: ScopeLevel
    scope: str
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]

    # thalamus-like addressing (optional for non-thalamic lanes)
    nucleus: Optional[NucleusId]

    # transport-agnostic metadata
    priority: Optional[int] = None
    salience: Optional[float] = None
    deadline_ms: Optional[int] = None
    confidence: Optional[float] = None

    payload: Mapping[str, Any] = None  # type: ignore[assignment]


@dataclass(frozen=True)
class GateState:
    scope_level: ScopeLevel
    scope: str
    nucleus: NucleusId
    inhibition: float                 # 0..1 (higher => more suppression)
    mode: Optional[GateMode] = None
    reason: Optional[str] = None
    timestamp_ms: int = 0
    expires_at_ms: Optional[int] = None


@dataclass(frozen=True)
class RelayTarget:
    cortex_area: str
    scope_level: ScopeLevel
    scope: str


@dataclass(frozen=True)
class RelayDecision:
    envelope: Envelope
    allowed: bool
    applied_inhibition: Optional[float]
    targets: Sequence[RelayTarget]
    rationale: Optional[str]


# =============================================================================
# Protocols (pure async)
# =============================================================================

class TopicBus(Protocol):
    async def publish(self, topic: str, msg: Any) -> None: ...
    def subscribe(self, topic: str) -> AsyncIterator[Any]: ...


class GateStore(Protocol):
    async def get(self, scope_level: ScopeLevel, scope: str, nucleus: NucleusId, now_ms: int) -> Optional[GateState]: ...
    async def put(self, state: GateState) -> None: ...


class CortexPort(Protocol):
    async def publish_to_cortex(self, decision: RelayDecision) -> None: ...


class GatePort(Protocol):
    async def publish_gate(self, state: GateState) -> None: ...


class RoutingPolicy(Protocol):
    async def targets_for(self, env: Envelope) -> Sequence[RelayTarget]: ...


class ThresholdPolicy(Protocol):
    async def threshold_for(self, env: Envelope, global_modes: Mapping[str, Any]) -> float: ...


class GlobalModeStore(Protocol):
    async def get_modes(self, scope_level: ScopeLevel, scope: str) -> Mapping[str, Any]: ...


# =============================================================================
# Topic helpers (transport-agnostic naming)
# =============================================================================

def topic_for(env: Envelope) -> str:
    base = f"/{env.lane.value}"
    if env.lane in (Lane.A_DRIVER, Lane.B_MODULATOR, Lane.G_GATE):
        if env.nucleus is None:
            raise ValueError("nucleus is required for A/B/G lanes")
        return f"{base}/{env.kind.value}/{env.scope_level.value}/{env.scope}/nucleus/{env.nucleus.value}"
    return f"{base}/{env.kind.value}/{env.scope_level.value}/{env.scope}"


# =============================================================================
# Reference in-memory implementations (for testing only)
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
            # expired: treat as absent
            return None
        return st

    async def put(self, state: GateState) -> None:
        self._m[(state.scope_level, state.scope, state.nucleus)] = state


class InMemoryGlobalModeStore:
    def __init__(self) -> None:
        self._m: Dict[Tuple[ScopeLevel, str], Dict[str, Any]] = {}

    async def get_modes(self, scope_level: ScopeLevel, scope: str) -> Mapping[str, Any]:
        return dict(self._m.get((scope_level, scope), {}))

    async def put_modes(self, scope_level: ScopeLevel, scope: str, modes: Mapping[str, Any]) -> None:
        self._m[(scope_level, scope)] = dict(modes)


# =============================================================================
# Brain-like Thalamus/TRN router (pure async)
# =============================================================================

class ThalamicRouter:
    """Applies GateState to Lane A drivers and relays to cortex targets.

    Inputs:
      - Lane A DRIVER envelopes (payload)
      - Lane B MODULATOR envelopes (feedback; may request inhibition updates)

    Outputs:
      - RelayDecision to CortexPort
      - GateState updates to GatePort (optional)
    """

    def __init__(
        self,
        gate_store: GateStore,
        global_modes: GlobalModeStore,
        routing: RoutingPolicy,
        thresholds: ThresholdPolicy,
        cortex: CortexPort,
        gate_port: Optional[GatePort] = None,
    ) -> None:
        self._gate_store = gate_store
        self._global_modes = global_modes
        self._routing = routing
        self._thresholds = thresholds
        self._cortex = cortex
        self._gate_port = gate_port

    async def ingest(self, env: Envelope) -> Optional[RelayDecision]:
        if env.lane == Lane.A_DRIVER:
            return await self._handle_driver(env)
        if env.lane == Lane.B_MODULATOR:
            await self._handle_modulator(env)
            return None
        if env.lane == Lane.G_GATE:
            await self._handle_gate_update(env)
            return None
        # other lanes ignored by this router
        return None

    async def _handle_driver(self, env: Envelope) -> RelayDecision:
        if env.nucleus is None:
            raise ValueError("Driver env must include nucleus")
        modes = await self._global_modes.get_modes(env.scope_level, env.scope)
        threshold = await self._thresholds.threshold_for(env, modes)

        gate = await self._gate_store.get(env.scope_level, env.scope, env.nucleus, env.timestamp_ms)
        inhibition = gate.inhibition if gate is not None else 0.0

        allowed = inhibition < threshold
        targets: Sequence[RelayTarget] = []
        if allowed:
            targets = await self._routing.targets_for(env)
        decision = RelayDecision(
            envelope=env,
            allowed=allowed,
            applied_inhibition=inhibition,
            targets=targets,
            rationale=f"inhibition={inhibition:.2f} threshold={threshold:.2f}",
        )
        await self._cortex.publish_to_cortex(decision)
        return decision

    async def _handle_modulator(self, env: Envelope) -> None:
        """Interpret a modulator payload as a request to update inhibition for a nucleus window."""
        if env.nucleus is None:
            return
        requested = env.payload.get("requested_inhibition") if env.payload else None
        if requested is None:
            return

        window_ms = env.payload.get("window_ms", 200) if env.payload else 200
        state = GateState(
            scope_level=env.scope_level,
            scope=env.scope,
            nucleus=env.nucleus,
            inhibition=float(requested),
            mode=None,
            reason=env.payload.get("reason") if env.payload else "modulator",
            timestamp_ms=env.timestamp_ms,
            expires_at_ms=env.timestamp_ms + int(window_ms),
        )
        await self._gate_store.put(state)
        if self._gate_port is not None:
            await self._gate_port.publish_gate(state)

    async def _handle_gate_update(self, env: Envelope) -> None:
        """Allow direct publishing of GateState via Lane G (useful for tests or dedicated TRN modules)."""
        if env.nucleus is None or not env.payload:
            return
        state = GateState(
            scope_level=env.scope_level,
            scope=env.scope,
            nucleus=env.nucleus,
            inhibition=float(env.payload.get("inhibition", 0.0)),
            mode=GateMode(env.payload["mode"]) if "mode" in env.payload else None,
            reason=env.payload.get("reason"),
            timestamp_ms=env.timestamp_ms,
            expires_at_ms=env.payload.get("expires_at_ms"),
        )
        await self._gate_store.put(state)
        if self._gate_port is not None:
            await self._gate_port.publish_gate(state)


# =============================================================================
# Minimal policies (for runnable demos / tests)
# =============================================================================

class SimpleRoutingPolicy:
    def __init__(self, cortex_area: str = "V1") -> None:
        self._area = cortex_area

    async def targets_for(self, env: Envelope) -> Sequence[RelayTarget]:
        return [RelayTarget(cortex_area=self._area, scope_level=env.scope_level, scope=env.scope)]


class SimpleThresholdPolicy:
    def __init__(self, base_threshold: float = 0.5) -> None:
        self._base = base_threshold

    async def threshold_for(self, env: Envelope, global_modes: Mapping[str, Any]) -> float:
        # Example: global mode can shift the threshold
        # - high_alert => tolerate more traffic (raise threshold)
        # - quiet_hours => suppress more (lower threshold)
        th = self._base
        if global_modes.get("high_alert"):
            th = min(1.0, th + 0.2)
        if global_modes.get("quiet_hours"):
            th = max(0.0, th - 0.2)
        return th


class InMemoryCortex(CortexPort):
    """A test cortex that stores decisions for assertions."""
    def __init__(self) -> None:
        self._q: asyncio.Queue[RelayDecision] = asyncio.Queue()

    async def publish_to_cortex(self, decision: RelayDecision) -> None:
        await self._q.put(decision)

    def decisions(self) -> AsyncIterator[RelayDecision]:
        async def _iter() -> AsyncIterator[RelayDecision]:
            while True:
                yield await self._q.get()
        return _iter()


class InMemoryGatePort(GatePort):
    def __init__(self) -> None:
        self._q: asyncio.Queue[GateState] = asyncio.Queue()

    async def publish_gate(self, state: GateState) -> None:
        await self._q.put(state)

    def gates(self) -> AsyncIterator[GateState]:
        async def _iter() -> AsyncIterator[GateState]:
            while True:
                yield await self._q.get()
        return _iter()


# =============================================================================
# Runnable demo (optional)
# =============================================================================

async def demo_router() -> None:
    gate_store = InMemoryGateStore()
    mode_store = InMemoryGlobalModeStore()
    cortex = InMemoryCortex()
    gate_port = InMemoryGatePort()

    router = ThalamicRouter(
        gate_store=gate_store,
        global_modes=mode_store,
        routing=SimpleRoutingPolicy("V1"),
        thresholds=SimpleThresholdPolicy(base_threshold=0.5),
        cortex=cortex,
        gate_port=gate_port,
    )

    # Initial: no gate => inhibition=0 => allowed
    env = Envelope(
        lane=Lane.A_DRIVER,
        kind=SignalKind.DRIVER,
        scope_level=ScopeLevel.ROOM,
        scope="living_room",
        timestamp_ms=1000,
        correlation_id="evt-1",
        source="camera",
        nucleus=NucleusId.LGN,
        salience=0.8,
        payload={"feature": "motion"},
    )
    await router.ingest(env)
    d1 = await anext(cortex.decisions())
    print("decision1 allowed:", d1.allowed, d1.rationale)

    # Send a modulator requesting high inhibition for 200ms => should block next driver
    mod = Envelope(
        lane=Lane.B_MODULATOR,
        kind=SignalKind.MODULATOR,
        scope_level=ScopeLevel.ROOM,
        scope="living_room",
        timestamp_ms=1100,
        correlation_id="evt-1",
        source="cortex:L6",
        nucleus=NucleusId.LGN,
        payload={"requested_inhibition": 0.9, "window_ms": 500, "reason": "suppress"},
    )
    await router.ingest(mod)
    _ = await anext(gate_port.gates())

    env2 = Envelope(
        lane=Lane.A_DRIVER,
        kind=SignalKind.DRIVER,
        scope_level=ScopeLevel.ROOM,
        scope="living_room",
        timestamp_ms=1200,
        correlation_id="evt-2",
        source="camera",
        nucleus=NucleusId.LGN,
        salience=0.3,
        payload={"feature": "static"},
    )
    await router.ingest(env2)
    d2 = await anext(cortex.decisions())
    print("decision2 allowed:", d2.allowed, d2.rationale)


# Note: don't call asyncio.run() at import time in real projects.
