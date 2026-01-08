from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional, Protocol, Sequence, Tuple


# ---------- Core enums / types ----------

class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class LimbicSubsystem(str, Enum):
    HIPPOCAMPUS = "hippocampus"
    AMYGDALA = "amygdala"


class HippocampalSubfield(str, Enum):
    ENTORHINAL = "entorhinal"
    DENTATE_GYRUS = "dentate_gyrus"
    CA3 = "ca3"
    CA2 = "ca2"
    CA1 = "ca1"
    SUBICULUM = "subiculum"


class AmygdalaNucleus(str, Enum):
    LATERAL = "lateral"
    BASAL = "basal"
    BASOLATERAL_COMPLEX = "bla"
    CENTRAL = "central"
    MEDIAL = "medial"
    INTERCALATED = "itc"


class LimbicPathway(str, Enum):
    FAST_THALAMIC = "fast_thalamic"    # low road
    SLOW_CORTICAL = "slow_cortical"    # high road
    EXTINCTION_GATE = "extinction_gate"
    PAPEZ_CIRCUIT = "papez_circuit"
    TRISYNAPTIC = "trisynaptic"


@dataclass(frozen=True)
class SignalEnvelope:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class EpisodicMemoryTrace:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    episode_id: str
    features: Mapping[str, Any]
    salience: Optional[float]
    tags: Mapping[str, Any]


@dataclass(frozen=True)
class RetrievalResult:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    query_id: str
    episode_ids: Sequence[str]
    confidence: Optional[float]
    context_summary: Mapping[str, Any]


@dataclass(frozen=True)
class ReplayBatch:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    episode_ids: Sequence[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class SalienceTag:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    salience: float
    valence: Optional[float]  # negative = threat, positive = reward
    rationale: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class DefensiveResponseRequest:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    severity: float
    reason: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class MotivationBias:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    channel: str
    bias: float
    rationale: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ExtinctionGateUpdate:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    inhibition: float  # 0..1 (higher = more suppression of expression)
    reason: Optional[str]


# ---------- Interface protocols (contracts) ----------

class CortexMemoryPort(Protocol):
    def publish_replay(self, batch: ReplayBatch) -> None: ...
    def publish_retrieval(self, result: RetrievalResult) -> None: ...


class AutonomicDefensePort(Protocol):
    def publish_defense(self, request: DefensiveResponseRequest) -> None: ...


class ActionSelectionBiasPort(Protocol):
    def publish_bias(self, bias: MotivationBias) -> None: ...


class LimbicStore(Protocol):
    def put_episode(self, trace: EpisodicMemoryTrace) -> None: ...
    def get_episode(self, episode_id: str) -> Optional[EpisodicMemoryTrace]: ...
    def query(self, scope: str, scope_level: ScopeLevel, cue: Mapping[str, Any]) -> Sequence[EpisodicMemoryTrace]: ...


class SalienceLearningPolicy(Protocol):
    def evaluate_fast(self, cue: SignalEnvelope) -> SalienceTag: ...
    def evaluate_slow(self, percept: SignalEnvelope) -> SalienceTag: ...
    def update_from_outcome(self, outcome: SignalEnvelope) -> None: ...


class MemoryPolicy(Protocol):
    def encode(self, percepts: Sequence[SignalEnvelope], salience: Optional[SalienceTag]) -> EpisodicMemoryTrace: ...
    def retrieve(self, cue: SignalEnvelope) -> RetrievalResult: ...
    def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> ReplayBatch: ...


class ExtinctionPolicy(Protocol):
    def compute_gate_update(self, top_down: SignalEnvelope) -> ExtinctionGateUpdate: ...


# ---------- Subsystem skeletons ----------

class Hippocampus:
    def __init__(self, store: LimbicStore, memory_policy: MemoryPolicy, cortex_port: CortexMemoryPort) -> None:
        ...

    # Encoding / binding
    def encode_episode(self, percepts: Sequence[SignalEnvelope], salience: Optional[SalienceTag] = None) -> EpisodicMemoryTrace:
        ...

    # Retrieval (pattern completion)
    def retrieve(self, cue: SignalEnvelope) -> RetrievalResult:
        ...

    # Pattern separation (conceptual hook)
    def pattern_separate(self, percepts: Sequence[SignalEnvelope]) -> Mapping[str, Any]:
        ...

    # Consolidation / replay
    def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> ReplayBatch:
        ...

    def publish_replay(self, batch: ReplayBatch) -> None:
        ...


class Amygdala:
    def __init__(
        self,
        salience_policy: SalienceLearningPolicy,
        extinction_policy: ExtinctionPolicy,
        autonomic_port: AutonomicDefensePort,
        bias_port: ActionSelectionBiasPort,
    ) -> None:
        ...

    # Fast (thalamic/low-road) salience check
    def evaluate_threat_fast(self, cue: SignalEnvelope) -> SalienceTag:
        ...

    # Slow (cortical/high-road) evaluation
    def evaluate_threat_slow(self, percept: SignalEnvelope) -> SalienceTag:
        ...

    # Trigger defensive/autonomic response requests
    def trigger_defense(self, tag: SalienceTag) -> Optional[DefensiveResponseRequest]:
        ...

    # Bias action selection / motivation
    def publish_motivation_bias(self, tag: SalienceTag, channel: str) -> MotivationBias:
        ...

    # Extinction (inhibitory gating of expression)
    def apply_top_down_regulation(self, top_down: SignalEnvelope) -> ExtinctionGateUpdate:
        ...

    # Learning update
    def ingest_outcome(self, outcome: SignalEnvelope) -> None:
        ...


# ---------- Orchestrator skeleton (optional, contract-level) ----------

class LimbicSystem:
    def __init__(self, hippocampus: Hippocampus, amygdala: Amygdala) -> None:
        ...

    def ingest_percepts(self, percepts: Sequence[SignalEnvelope]) -> Tuple[Optional[EpisodicMemoryTrace], Sequence[SalienceTag]]:
        ...

    def ingest_fast_cue(self, cue: SignalEnvelope) -> SalienceTag:
        ...

    def ingest_context_cue(self, cue: SignalEnvelope) -> RetrievalResult:
        ...

    def ingest_top_down(self, signal: SignalEnvelope) -> ExtinctionGateUpdate:
        ...

    def step_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> ReplayBatch:
        ...
