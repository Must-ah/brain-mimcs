from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# ---------- Core enums / types ----------


class NucleusClass(str, Enum):
    FIRST_ORDER = "first_order"  # sensory relay to primary cortex
    HIGHER_ORDER = "higher_order"  # cortex-to-cortex via thalamus
    DIFFUSE = "diffuse"  # intralaminar/midline-style
    GATE = "gate"  # TRN-like gating


class NucleusId(str, Enum):
    # First-order sensory-style
    LGN = "lgn"  # visual relay
    MGN = "mgn"  # auditory relay
    VPL = "vpl"  # somatosensory (body)
    VPM = "vpm"  # somatosensory (face)

    # Motor-style
    VL = "vl"
    VA = "va"

    # Higher-order / association-style
    PULVINAR = "pulvinar"
    MD = "md"  # mediodorsal
    LP = "lp"

    # Diffuse / arousal-style
    CM = "cm"  # centromedian (intralaminar example)
    PF = "pf"  # parafascicular (intralaminar example)

    # Gate
    TRN = "trn"


class SignalKind(str, Enum):
    DRIVER = "driver"  # payload ("what happened")
    MODULATOR = "modulator"  # context/control ("how to treat it")


class CortexLayer(str, Enum):
    L4 = "l4"  # relay target (first-order)
    L6 = "l6"  # reciprocal feedback to same nucleus (modulation)
    L5 = "l5"  # higher-order driver to thalamus for transthalamic routing


class GateMode(str, Enum):
    MULTI = "multi"  # allow multiple channels
    WINNER_TAKE_ALL = "winner_take_all"


class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


@dataclass(frozen=True)
class ThalamicEnvelope:
    kind: SignalKind
    nucleus: NucleusId
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]

    # routing + attention metadata (transport-agnostic)
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


# ---------- Interface protocols (contracts) ----------


class ThalamusSignalSink(Protocol):
    def accept(self, envelope: ThalamicEnvelope) -> None: ...


class ThalamusSignalSource(Protocol):
    def subscribe(
        self,
        kind: SignalKind,
        nucleus: Optional[NucleusId] = None,
        scope: Optional[str] = None,
    ) -> None: ...
    def unsubscribe(
        self,
        kind: SignalKind,
        nucleus: Optional[NucleusId] = None,
        scope: Optional[str] = None,
    ) -> None: ...


class CortexRelayPort(Protocol):
    def publish_to_cortex(self, decision: RouteDecision) -> None: ...


class ThalamusFeedbackPort(Protocol):
    def publish_feedback(self, envelope: ThalamicEnvelope) -> None: ...


class TRNGatePort(Protocol):
    def publish_gate_state(self, state: GateState) -> None: ...


class GateStore(Protocol):
    def get_gate_state(
        self, scope: str, scope_level: ScopeLevel, nucleus: NucleusId
    ) -> Optional[GateState]: ...
    def put_gate_state(self, state: GateState) -> None: ...


class RoutingPolicy(Protocol):
    def compute_targets(self, envelope: ThalamicEnvelope) -> Sequence[RelayTarget]: ...


class GatingPolicy(Protocol):
    def evaluate(
        self, envelope: ThalamicEnvelope, current_gate: Optional[GateState]
    ) -> GateState: ...


# ---------- Main Thalamus class skeleton ----------


class Thalamus:
    """
    Contract-only skeleton for a 'Thalamus' interface package:
    - Addressing by nucleus + scope
    - Driver vs modulator signal classes
    - TRN-like gating semantics (inhibition)
    - Relay to cortex targets + feedback loops
    """

    def __init__(
        self,
        gate_store: GateStore,
        routing_policy: RoutingPolicy,
        gating_policy: GatingPolicy,
        cortex_port: CortexRelayPort,
        trn_port: TRNGatePort,
        feedback_port: ThalamusFeedbackPort,
    ) -> None: ...

    # --- ingestion ---
    def ingest(self, envelope: ThalamicEnvelope) -> None: ...

    def ingest_batch(self, envelopes: Sequence[ThalamicEnvelope]) -> None: ...

    # --- routing / relay (Thalamus -> Cortex) ---
    def route(self, envelope: ThalamicEnvelope) -> RouteDecision: ...

    def relay(self, decision: RouteDecision) -> None: ...

    def relay_step(self, envelope: ThalamicEnvelope) -> RouteDecision: ...

    # --- gating (TRN-like inhibition control plane) ---
    def get_gate_state(
        self, scope: str, scope_level: ScopeLevel, nucleus: NucleusId
    ) -> Optional[GateState]: ...

    def set_inhibition(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        inhibition: float,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState: ...

    def open_gate(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState: ...

    def close_gate(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState: ...

    def apply_attention_profile(
        self,
        scope: str,
        scope_level: ScopeLevel,
        timestamp_ms: int,
        allow: Sequence[Tuple[NucleusId, float]],
        suppress: Optional[Sequence[Tuple[NucleusId, float]]] = None,
        mode: GateMode = GateMode.MULTI,
        reason: Optional[str] = None,
    ) -> Sequence[GateState]: ...

    # --- feedback loops (Cortex -> Thalamus) ---
    def accept_cortex_feedback(self, envelope: ThalamicEnvelope) -> None: ...

    def publish_feedback(self, envelope: ThalamicEnvelope) -> None: ...

    # --- higher-order (transthalamic) routing semantics ---
    def route_higher_order(self, envelope: ThalamicEnvelope) -> RouteDecision: ...

    def register_cortex_mapping(
        self,
        nucleus: NucleusId,
        relay_targets: Sequence[RelayTarget],
    ) -> None: ...

    def unregister_cortex_mapping(self, nucleus: NucleusId) -> None: ...

    # --- governance / invariants ---
    def validate_envelope(self, envelope: ThalamicEnvelope) -> None: ...

    def validate_decision(self, decision: RouteDecision) -> None: ...

    def set_priority_rules(self, rules: Mapping[str, Any]) -> None: ...

    def set_backpressure_rules(self, rules: Mapping[str, Any]) -> None: ...

    # --- introspection / observability hooks (contract-level) ---
    def list_nuclei(self) -> List[NucleusId]: ...

    def describe_nucleus(self, nucleus: NucleusId) -> Mapping[str, Any]: ...

    def summarize_scope(
        self, scope: str, scope_level: ScopeLevel
    ) -> Mapping[str, Any]: ...
