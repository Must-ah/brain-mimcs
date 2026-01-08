from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# =============================================================================
# Minimal async "testing fabric" (in-memory pub/sub + queues)
# =============================================================================

class InMemoryTopicBus:
    """
    Tiny async pub/sub bus for tests.

    - publish(topic, msg): fan-out to all subscribers
    - subscribe(topic): async iterator yielding messages

    Rate limiting: Default max queue size of 1000 prevents memory exhaustion.
    When queue is full, oldest messages are dropped (backpressure).
    """
    DEFAULT_MAX_QUEUE_SIZE = 1000

    def __init__(self, max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE) -> None:
        self._subs: Dict[str, List[asyncio.Queue[Any]]] = {}
        self._max_queue_size = max_queue_size

    async def publish(self, topic: str, msg: Any) -> None:
        for q in self._subs.get(topic, []):
            if q.full():
                # Drop oldest message to make room (backpressure)
                try:
                    q.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            await q.put(msg)

    def subscribe(self, topic: str, max_queue: Optional[int] = None) -> AsyncIterator[Any]:
        queue_size = max_queue if max_queue is not None else self._max_queue_size
        q: asyncio.Queue[Any] = asyncio.Queue(maxsize=queue_size)
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
# Thalamus-side contracts (kept compatible with your async version)
# =============================================================================

class SignalKind(str, Enum):
    DRIVER = "driver"
    MODULATOR = "modulator"


class CortexLayer(str, Enum):
    L4 = "l4"
    L5 = "l5"
    L6 = "l6"


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
    VL = "vl"
    VA = "va"
    PULVINAR = "pulvinar"
    MD = "md"
    LP = "lp"
    CM = "cm"
    PF = "pf"
    TRN = "trn"


@dataclass(frozen=True)
class ThalamicEnvelope:
    kind: SignalKind
    nucleus: NucleusId
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]
    priority: Optional[int]
    salience: Optional[float]
    deadline_ms: Optional[int]
    confidence: Optional[float]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class RelayTarget:
    cortex_area: str
    layer: CortexLayer
    scope: str
    scope_level: ScopeLevel


@dataclass(frozen=True)
class RouteDecision:
    envelope: ThalamicEnvelope
    allowed: bool
    gate_inhibition: Optional[float]
    targets: Sequence[RelayTarget]
    rationale: Optional[str]


@dataclass(frozen=True)
class GateState:
    scope: str
    scope_level: ScopeLevel
    nucleus: NucleusId
    inhibition: float  # 0..1
    mode: Optional[GateMode]
    reason: Optional[str]
    timestamp_ms: int


# Ports match the async Protocols you defined
class CortexRelayPort(Protocol):
    async def publish_to_cortex(self, decision: RouteDecision) -> None: ...


class ThalamusFeedbackPort(Protocol):
    async def publish_feedback(self, envelope: ThalamicEnvelope) -> None: ...


class TRNGatePort(Protocol):
    async def publish_gate_state(self, state: GateState) -> None: ...


# =============================================================================
# Mock Cortex (async)
# =============================================================================

@dataclass(frozen=True)
class MockCortexConfig:
    cortex_area: str = "mock_cortex"
    attend_salience_threshold: float = 0.6
    boost_value: float = 0.2
    suppress_value: float = 0.8
    emit_higher_order: bool = True


class MockCortex(CortexRelayPort):
    """
    Minimal async Cortex mock to test subcortical modules.

    - Receives thalamic relay RouteDecisions via publish_to_cortex().
    - Emits Layer-6-like feedback modulators back to thalamus (via feedback_port).
    - Optionally emits Layer-5-like "higher-order" driver messages to association nuclei.
    - Exposes an async iterator of received decisions for assertions.
    """

    def __init__(
        self,
        config: MockCortexConfig,
        feedback_port: ThalamusFeedbackPort,
        bus: Optional[InMemoryTopicBus] = None,
    ) -> None:
        self._cfg = config
        self._feedback_port = feedback_port
        self._decisions: asyncio.Queue[RouteDecision] = asyncio.Queue()
        self._bus = bus

    async def publish_to_cortex(self, decision: RouteDecision) -> None:
        await self._decisions.put(decision)

        if self._bus is not None:
            await self._bus.publish(f"cortex/{self._cfg.cortex_area}/relay", decision)

        await self._emit_l6_feedback(decision)

        if self._cfg.emit_higher_order:
            await self._emit_l5_higher_order(decision)

    def decisions(self) -> AsyncIterator[RouteDecision]:
        async def _iter() -> AsyncIterator[RouteDecision]:
            while True:
                yield await self._decisions.get()
        return _iter()

    async def _emit_l6_feedback(self, decision: RouteDecision) -> None:
        env = decision.envelope

        if not decision.allowed:
            inhibition = self._cfg.suppress_value
            effect = "SUPPRESS"
        else:
            sal = env.salience if env.salience is not None else 0.0
            if sal >= self._cfg.attend_salience_threshold:
                inhibition = self._cfg.boost_value
                effect = "BOOST"
            else:
                inhibition = self._cfg.suppress_value
                effect = "SUPPRESS"

        feedback = ThalamicEnvelope(
            kind=SignalKind.MODULATOR,
            nucleus=env.nucleus,
            scope=env.scope,
            scope_level=env.scope_level,
            timestamp_ms=env.timestamp_ms,
            correlation_id=env.correlation_id,
            source=f"{self._cfg.cortex_area}:{CortexLayer.L6.value}",
            priority=env.priority,
            salience=env.salience,
            deadline_ms=env.deadline_ms,
            confidence=env.confidence,
            payload={
                "layer": CortexLayer.L6.value,
                "effect": effect,
                "requested_inhibition": inhibition,
                "rationale": decision.rationale or "mock_cortex_feedback",
            },
        )
        await self._feedback_port.publish_feedback(feedback)

        if self._bus is not None:
            await self._bus.publish(f"cortex/{self._cfg.cortex_area}/feedback", feedback)

    async def _emit_l5_higher_order(self, decision: RouteDecision) -> None:
        env = decision.envelope

        sal = env.salience if env.salience is not None else 0.0
        if (not decision.allowed) or (sal < self._cfg.attend_salience_threshold):
            return

        higher = ThalamicEnvelope(
            kind=SignalKind.DRIVER,
            nucleus=NucleusId.PULVINAR,
            scope=env.scope,
            scope_level=env.scope_level,
            timestamp_ms=env.timestamp_ms,
            correlation_id=env.correlation_id,
            source=f"{self._cfg.cortex_area}:{CortexLayer.L5.value}",
            priority=env.priority,
            salience=env.salience,
            deadline_ms=env.deadline_ms,
            confidence=env.confidence,
            payload={
                "layer": CortexLayer.L5.value,
                "from_nucleus": env.nucleus.value,
                "intent": "associate_or_route",
                "note": "synthetic higher-order driver from mock cortex",
            },
        )
        await self._feedback_port.publish_feedback(higher)

        if self._bus is not None:
            await self._bus.publish(f"cortex/{self._cfg.cortex_area}/higher_order", higher)


# =============================================================================
# Simple async ports for tests (in-memory)
# =============================================================================

class InMemoryFeedbackPort(ThalamusFeedbackPort):
    """Captures feedback envelopes and (optionally) publishes to a bus."""
    def __init__(self, bus: Optional[InMemoryTopicBus] = None, topic: str = "thalamus/feedback") -> None:
        self._q: asyncio.Queue[ThalamicEnvelope] = asyncio.Queue()
        self._bus = bus
        self._topic = topic

    async def publish_feedback(self, envelope: ThalamicEnvelope) -> None:
        await self._q.put(envelope)
        if self._bus is not None:
            await self._bus.publish(self._topic, envelope)

    def feedback(self) -> AsyncIterator[ThalamicEnvelope]:
        async def _iter() -> AsyncIterator[ThalamicEnvelope]:
            while True:
                yield await self._q.get()
        return _iter()


class InMemoryTRNGatePort(TRNGatePort):
    """Captures gate-state publications for assertions."""
    def __init__(self, bus: Optional[InMemoryTopicBus] = None, topic: str = "thalamus/gate") -> None:
        self._q: asyncio.Queue[GateState] = asyncio.Queue()
        self._bus = bus
        self._topic = topic

    async def publish_gate_state(self, state: GateState) -> None:
        await self._q.put(state)
        if self._bus is not None:
            await self._bus.publish(self._topic, state)

    def gate_states(self) -> AsyncIterator[GateState]:
        async def _iter() -> AsyncIterator[GateState]:
            while True:
                yield await self._q.get()
        return _iter()


# =============================================================================
# Optional demo
# =============================================================================

async def demo_mock_cortex_roundtrip() -> None:
    """Tiny demo: send a RouteDecision, observe feedback from cortex."""
    bus = InMemoryTopicBus()
    feedback_port = InMemoryFeedbackPort(bus=bus)
    cortex = MockCortex(MockCortexConfig(), feedback_port=feedback_port, bus=bus)

    env = ThalamicEnvelope(
        kind=SignalKind.DRIVER,
        nucleus=NucleusId.LGN,
        scope="living_room",
        scope_level=ScopeLevel.ROOM,
        timestamp_ms=123456,
        correlation_id="evt-1",
        source="camera",
        priority=5,
        salience=0.9,
        deadline_ms=None,
        confidence=0.8,
        payload={"frame_features": {"motion": 0.2}},
    )
    decision = RouteDecision(
        envelope=env,
        allowed=True,
        gate_inhibition=0.1,
        targets=[RelayTarget(cortex_area="V1", layer=CortexLayer.L4, scope="living_room", scope_level=ScopeLevel.ROOM)],
        rationale="demo",
    )

    await cortex.publish_to_cortex(decision)

    fb = await anext(feedback_port.feedback())
    print("Cortex feedback:", fb.kind, fb.nucleus, fb.payload)
