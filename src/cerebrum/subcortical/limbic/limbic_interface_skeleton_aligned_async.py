from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional, Protocol, Sequence, Tuple


# ---------- Core enums / types (aligned naming) ----------

class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class LimbicLane(str, Enum):
    MEMORY_CONTEXT = "memory_context"      # hippocampal formation analog
    SALIENCE_THREAT = "salience_threat"    # amygdala analog
    EXTINCTION_CONTROL = "extinction_control"
    CONSOLIDATION_REPLAY = "consolidation_replay"


class SignalClass(str, Enum):
    CORTICAL_PERCEPT = "cortical_percept"          # structured summaries (not raw)
    THALAMIC_FAST_CUE = "thalamic_fast_cue"        # fast, coarse cue
    CONTEXT_CUE = "context_cue"                    # partial cue for retrieval
    OUTCOME_FEEDBACK = "outcome_feedback"          # reward/punishment + success/failure
    TOP_DOWN_REGULATION = "top_down_regulation"    # vmPFC-like regulation
    DRIVE_STATE = "drive_state"                    # hypothalamus/brainstem-like state
    REPLAY_TICK = "replay_tick"                    # trigger consolidation scheduling


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


@dataclass(frozen=True)
class SignalEnvelope:
    signal_class: SignalClass
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    source: Optional[str]
    lane: Optional[LimbicLane]
    payload: Mapping[str, Any]


# ---------- Output contracts (aligned with other specs: decisions + profiles) ----------

@dataclass(frozen=True)
class EpisodicMemoryTrace:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    episode_id: str
    correlation_id: Optional[str]
    features: Mapping[str, Any]
    tags: Mapping[str, Any]
    salience: Optional[float]


@dataclass(frozen=True)
class RetrievalResult:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    query_id: str
    correlation_id: Optional[str]
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
    salience: float                # 0..1 (importance)
    valence: Optional[float]       # negative=threat, positive=reward
    confidence: Optional[float]
    rationale: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class DefensiveResponseRequest:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    severity: float                # 0..1
    reason: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class MotivationBias:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    channel: str                   # target action-selection channel
    bias: float                    # signed bias
    rationale: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ExtinctionGateUpdate:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    correlation_id: Optional[str]
    inhibition: float              # 0..1 (higher => more suppression of expression)
    reason: Optional[str]


@dataclass(frozen=True)
class LimbicDecision:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    encoded_episode: Optional[EpisodicMemoryTrace]
    retrieval: Optional[RetrievalResult]
    salience: Sequence[SalienceTag]
    defense: Optional[DefensiveResponseRequest]
    bias: Optional[MotivationBias]
    extinction: Optional[ExtinctionGateUpdate]
    replay: Optional[ReplayBatch]
    rationale: Optional[str]


# ---------- Ports (PURE ASYNC) ----------

class CortexMemoryPort(Protocol):
    async def publish_retrieval(self, result: RetrievalResult) -> None: ...
    async def publish_replay(self, batch: ReplayBatch) -> None: ...


class AutonomicDefensePort(Protocol):
    async def publish_defense(self, request: DefensiveResponseRequest) -> None: ...


class ActionSelectionBiasPort(Protocol):
    async def publish_bias(self, bias: MotivationBias) -> None: ...


class ExtinctionControlPort(Protocol):
    async def publish_extinction(self, update: ExtinctionGateUpdate) -> None: ...


# ---------- Stores (PURE ASYNC) ----------

class EpisodicStore(Protocol):
    async def put_episode(self, trace: EpisodicMemoryTrace) -> None: ...
    async def get_episode(self, episode_id: str) -> Optional[EpisodicMemoryTrace]: ...
    async def query(self, scope: str, scope_level: ScopeLevel, cue: Mapping[str, Any]) -> Sequence[EpisodicMemoryTrace]: ...


class SalienceStore(Protocol):
    async def put_salience(self, tag: SalienceTag) -> None: ...
    async def list_recent(
        self,
        scope: str,
        scope_level: ScopeLevel,
        window_ms: int,
        now_ms: int,
    ) -> Sequence[SalienceTag]: ...


class ExtinctionStore(Protocol):
    async def get_inhibition(self, scope: str, scope_level: ScopeLevel) -> float: ...
    async def set_inhibition(self, update: ExtinctionGateUpdate) -> None: ...


# ---------- Policies (PURE ASYNC) ----------

class MemoryPolicy(Protocol):
    async def encode(
        self,
        percepts: Sequence[SignalEnvelope],
        salience: Sequence[SalienceTag],
    ) -> Optional[EpisodicMemoryTrace]: ...

    async def retrieve(self, cue: SignalEnvelope) -> Optional[RetrievalResult]: ...

    async def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> Optional[ReplayBatch]: ...


class SaliencePolicy(Protocol):
    async def evaluate_fast(self, cue: SignalEnvelope) -> Optional[SalienceTag]: ...
    async def evaluate_slow(self, percept: SignalEnvelope) -> Optional[SalienceTag]: ...
    async def update_from_outcome(self, outcome: SignalEnvelope) -> None: ...


class DefensePolicy(Protocol):
    async def decide_defense(
        self,
        tags: Sequence[SalienceTag],
        extinction_inhibition: float,
    ) -> Optional[DefensiveResponseRequest]: ...


class BiasPolicy(Protocol):
    async def decide_bias(self, tags: Sequence[SalienceTag]) -> Optional[MotivationBias]: ...


class ExtinctionPolicy(Protocol):
    async def compute_update(
        self,
        top_down: SignalEnvelope,
        current_inhibition: float,
    ) -> Optional[ExtinctionGateUpdate]: ...


# ---------- Main Limbic class (single aligned façade) - PURE ASYNC ----------

class Limbic:
    """Contract-only skeleton for a Limbic interface package (pure async).

    - Accepts normalized SignalEnvelope inputs
    - Produces a LimbicDecision (memory + salience + defense + bias + extinction + replay)
    - Publishes via async ports (cortex replay/retrieval, defense, bias, extinction)
    """

    def __init__(
        self,
        episodic_store: EpisodicStore,
        salience_store: SalienceStore,
        extinction_store: ExtinctionStore,
        memory_policy: MemoryPolicy,
        salience_policy: SaliencePolicy,
        defense_policy: DefensePolicy,
        bias_policy: BiasPolicy,
        extinction_policy: ExtinctionPolicy,
        cortex_port: CortexMemoryPort,
        defense_port: AutonomicDefensePort,
        bias_port: ActionSelectionBiasPort,
        extinction_port: ExtinctionControlPort,
    ) -> None:
        ...

    # --- ingestion ---
    async def ingest(self, signal: SignalEnvelope) -> None:
        ...

    async def ingest_batch(self, signals: Sequence[SignalEnvelope]) -> None:
        ...

    # --- core functions ---
    async def encode_episode(self, percepts: Sequence[SignalEnvelope], now_ms: int) -> Optional[EpisodicMemoryTrace]:
        ...

    async def retrieve(self, cue: SignalEnvelope) -> Optional[RetrievalResult]:
        ...

    async def evaluate_salience_fast(self, cue: SignalEnvelope) -> Optional[SalienceTag]:
        ...

    async def evaluate_salience_slow(self, percept: SignalEnvelope) -> Optional[SalienceTag]:
        ...

    async def apply_top_down_regulation(self, signal: SignalEnvelope) -> Optional[ExtinctionGateUpdate]:
        ...

    async def ingest_outcome(self, outcome: SignalEnvelope) -> None:
        ...

    async def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> Optional[ReplayBatch]:
        ...

    # --- decision + publish ---
    async def decide(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> LimbicDecision:
        ...

    async def apply(self, decision: LimbicDecision) -> None:
        ...

    async def step(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> LimbicDecision:
        ...

    # --- governance / invariants ---
    async def validate_signal(self, signal: SignalEnvelope) -> None:
        ...

    async def validate_decision(self, decision: LimbicDecision) -> None:
        ...

    # --- introspection ---
    async def summarize(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]:
        ...
