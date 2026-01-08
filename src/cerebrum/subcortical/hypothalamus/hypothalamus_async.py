from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional, Protocol, Sequence


# ---------- Core enums / types ----------


class HypothalamusRegion(str, Enum):
    PREOPTIC = "preoptic"
    ANTERIOR_CHIASMATIC = "anterior_chiasmatic"
    TUBERAL = "tuberal"
    MAMMILLARY = "mammillary"


class HypothalamusZone(str, Enum):
    PERIVENTRICULAR = "periventricular"
    MEDIAL = "medial"
    LATERAL = "lateral"


class HypothalamicModule(str, Enum):
    SCN = "scn"  # circadian timing
    PVN = "pvn"  # stress + autonomic/endocrine hub
    SON = "son"  # fluid balance hormones
    VLPO = "vlpo"  # sleep-promoting
    LHA = "lha"  # orexin/arousal/feeding
    TMN = "tmn"  # histamine/arousal
    ARCUATE = "arcuate"  # metabolic sensing
    VMH = "vmh"  # feeding/defense/sex behaviors
    MAMMILLARY = "mammillary_bodies"  # memory relay


class SignalClass(str, Enum):
    INTEROCEPTIVE = "interoceptive"  # internal state metrics
    SALIENCE_THREAT = "salience_threat"  # urgent/unsafe flags
    COGNITIVE_CONSTRAINT = "cognitive_constraint"  # user prefs/policies
    CIRCADIAN_ENTRAINMENT = "circadian_entrainment"  # time/light cues
    SLOW_TREND = "slow_trend"  # rolling trends (reliability/energy)


class OutputPathway(str, Enum):
    AUTONOMIC = "autonomic"  # fast, targeted control
    ENDOCRINE = "endocrine"  # slow, global modulation


class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


@dataclass(frozen=True)
class SignalEnvelope:
    signal_class: SignalClass
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class HomeostaticState:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    variables: Mapping[str, float]
    stress_index: Optional[float]
    notes: Optional[str]


@dataclass(frozen=True)
class RegulationDecision:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    autonomic_commands: Sequence[Mapping[str, Any]]
    endocrine_biases: Sequence[Mapping[str, Any]]
    state_summary: Optional[HomeostaticState]
    rationale: Optional[str]


# ---------- Interface protocols (contracts) - PURE ASYNC ----------


class SignalSink(Protocol):
    async def accept(self, signal: SignalEnvelope) -> None: ...


class SignalSource(Protocol):
    async def subscribe(self, signal_class: SignalClass, scope: Optional[str] = None) -> None: ...
    async def unsubscribe(self, signal_class: SignalClass, scope: Optional[str] = None) -> None: ...


class AutonomicOutputPort(Protocol):
    async def publish_autonomic(self, decision: RegulationDecision) -> None: ...


class EndocrineOutputPort(Protocol):
    async def publish_endocrine(self, decision: RegulationDecision) -> None: ...


class HomeostaticStateStore(Protocol):
    async def get_state(self, scope: str, scope_level: ScopeLevel) -> Optional[HomeostaticState]: ...
    async def put_state(self, state: HomeostaticState) -> None: ...


class PolicyEngine(Protocol):
    async def evaluate(self, state: HomeostaticState, signals: Sequence[SignalEnvelope]) -> RegulationDecision: ...


# ---------- Main Hypothalamus class skeleton - PURE ASYNC ----------


class Hypothalamus:
    def __init__(
        self,
        state_store: HomeostaticStateStore,
        policy_engine: PolicyEngine,
        autonomic_port: AutonomicOutputPort,
        endocrine_port: EndocrineOutputPort,
    ) -> None: ...

    # --- ingestion / sensing ---
    async def ingest(self, signal: SignalEnvelope) -> None: ...

    async def ingest_batch(self, signals: Sequence[SignalEnvelope]) -> None: ...

    # --- state estimation (closed-loop) ---
    async def update_state(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> HomeostaticState: ...

    async def get_state(self, scope: str, scope_level: ScopeLevel) -> Optional[HomeostaticState]: ...

    # --- regulation / outputs ---
    async def decide(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> RegulationDecision: ...

    async def apply(self, decision: RegulationDecision) -> None: ...

    async def step(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> RegulationDecision: ...

    # --- circadian / scheduling ---
    async def set_circadian_profile(self, scope: str, profile: Mapping[str, Any]) -> None: ...

    async def compute_circadian_phase(self, now_ms: int, scope: Optional[str] = None) -> Mapping[str, Any]: ...

    # --- stress handling ---
    async def compute_stress_index(self, state: HomeostaticState, signals: Sequence[SignalEnvelope]) -> float: ...

    async def enter_stress_mode(self, scope: str, scope_level: ScopeLevel, now_ms: int, reason: str) -> RegulationDecision: ...

    async def exit_stress_mode(self, scope: str, scope_level: ScopeLevel, now_ms: int, reason: str) -> RegulationDecision: ...

    # --- governance / invariants ---
    async def validate_invariants(self, decision: RegulationDecision) -> None: ...

    async def set_thresholds(self, thresholds: Mapping[str, float]) -> None: ...

    async def set_hysteresis(self, hysteresis: Mapping[str, float]) -> None: ...

    # --- extension points (optional module tagging) ---
    async def enable_module(self, module: HypothalamicModule) -> None: ...

    async def disable_module(self, module: HypothalamicModule) -> None: ...

    async def list_modules(self) -> List[HypothalamicModule]: ...
