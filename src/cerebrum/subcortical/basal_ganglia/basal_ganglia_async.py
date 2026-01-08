from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional, Protocol, Sequence, Tuple


# ---------- Core enums / types ----------


class BGPathway(str, Enum):
    DIRECT_GO = "direct_go"
    INDIRECT_NO_GO = "indirect_no_go"
    HYPERDIRECT_STOP = "hyperdirect_stop"


class BGLoop(str, Enum):
    MOTOR = "motor"
    OCULOMOTOR = "oculomotor"
    COGNITIVE = "cognitive"
    LIMBIC = "limbic"


class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class DecisionMode(str, Enum):
    EXACT_ONE = "exact_one"
    BOUNDED_MULTI = "bounded_multi"


@dataclass(frozen=True)
class CandidateAction:
    action_id: str
    channel: str  # competition channel / action family
    loop: BGLoop  # motor/cognitive/limbic/etc.
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int

    # decision features (implementation-agnostic)
    utility: Optional[float]
    cost: Optional[float]
    urgency: Optional[float]
    deadline_ms: Optional[int]
    confidence: Optional[float]

    # optional metadata
    preconditions: Optional[Mapping[str, Any]]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ContextSignal:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    source: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class StopSignal:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    channel: Optional[str]  # None = global stop
    reason: str
    duration_ms: Optional[int]


@dataclass(frozen=True)
class OutcomeFeedback:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    action_id: str
    success: bool
    reward: Optional[float]  # scalar reward/punishment
    prediction_error: Optional[float]
    notes: Optional[str]
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class InhibitionProfile:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    channel: str
    inhibited_action_ids: Sequence[str]
    inhibition_strength: float  # 0..1
    rationale: Optional[str]


@dataclass(frozen=True)
class SelectionDecision:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    channel: str
    selected_action_ids: Sequence[str]
    mode: DecisionMode
    pathway: BGPathway
    confidence: Optional[float]
    rationale: Optional[str]


@dataclass(frozen=True)
class StopDecision:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    active: bool
    channel: Optional[str]  # None = global
    reason: str
    expires_at_ms: Optional[int]


@dataclass(frozen=True)
class LearningUpdate:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    loop: BGLoop
    channel: str
    action_id: str
    update_type: str  # e.g., "value", "policy_bias", "habit_strength"
    payload: Mapping[str, Any]


# ---------- Interface protocols (contracts) - PURE ASYNC ----------


class CandidateStore(Protocol):
    async def add(self, candidate: CandidateAction) -> None: ...

    async def list(
        self, scope: str, scope_level: ScopeLevel, channel: str
    ) -> Sequence[CandidateAction]: ...

    async def remove(self, scope: str, scope_level: ScopeLevel, action_id: str) -> None: ...

    async def clear_channel(
        self, scope: str, scope_level: ScopeLevel, channel: str
    ) -> None: ...


class ContextStore(Protocol):
    async def put(self, signal: ContextSignal) -> None: ...

    async def get_snapshot(
        self, scope: str, scope_level: ScopeLevel
    ) -> Mapping[str, Any]: ...


class StopStore(Protocol):
    async def set(self, decision: StopDecision) -> None: ...

    async def get(
        self, scope: str, scope_level: ScopeLevel, channel: Optional[str]
    ) -> Optional[StopDecision]: ...

    async def clear(
        self, scope: str, scope_level: ScopeLevel, channel: Optional[str]
    ) -> None: ...


class SelectionPolicy(Protocol):
    async def select(
        self,
        candidates: Sequence[CandidateAction],
        context: Mapping[str, Any],
        mode: DecisionMode,
    ) -> SelectionDecision: ...


class InhibitionPolicy(Protocol):
    async def compute_inhibition(
        self,
        candidates: Sequence[CandidateAction],
        selection: SelectionDecision,
        context: Mapping[str, Any],
    ) -> InhibitionProfile: ...


class LearningPolicy(Protocol):
    async def update(
        self, feedback: OutcomeFeedback, context: Mapping[str, Any]
    ) -> Sequence[LearningUpdate]: ...


class DecisionPort(Protocol):
    async def publish_selection(self, decision: SelectionDecision) -> None: ...
    async def publish_inhibition(self, profile: InhibitionProfile) -> None: ...
    async def publish_stop(self, decision: StopDecision) -> None: ...
    async def publish_learning(self, updates: Sequence[LearningUpdate]) -> None: ...


# ---------- Main Basal Ganglia class skeleton - PURE ASYNC ----------


class BasalGanglia:
    """Contract-only skeleton for a Basal Ganglia interface package (pure async).

    - Action selection by disinhibition (GO)
    - Suppression of competitors (NO-GO)
    - Fast global or channel stop (hyperdirect STOP)
    - Reinforcement-driven learning updates
    """

    def __init__(
        self,
        candidate_store: CandidateStore,
        context_store: ContextStore,
        stop_store: StopStore,
        selection_policy: SelectionPolicy,
        inhibition_policy: InhibitionPolicy,
        learning_policy: LearningPolicy,
        decision_port: DecisionPort,
        mode: DecisionMode = DecisionMode.EXACT_ONE,
    ) -> None: ...

    # --- candidate ingestion ---
    async def submit_candidate(self, candidate: CandidateAction) -> None: ...

    async def submit_candidates(self, candidates: Sequence[CandidateAction]) -> None: ...

    async def withdraw_candidate(
        self, scope: str, scope_level: ScopeLevel, action_id: str
    ) -> None: ...

    # --- context ingestion ---
    async def ingest_context(self, signal: ContextSignal) -> None: ...

    # --- STOP / brake control ---
    async def request_stop(self, signal: StopSignal) -> StopDecision: ...

    async def release_stop(
        self,
        scope: str,
        scope_level: ScopeLevel,
        channel: Optional[str],
        now_ms: int,
        reason: str,
    ) -> StopDecision: ...

    async def get_stop_state(
        self, scope: str, scope_level: ScopeLevel, channel: Optional[str]
    ) -> Optional[StopDecision]: ...

    # --- selection (GO) and suppression (NO-GO) ---
    async def decide(
        self, scope: str, scope_level: ScopeLevel, channel: str, now_ms: int
    ) -> SelectionDecision: ...

    async def compute_inhibition(
        self,
        scope: str,
        scope_level: ScopeLevel,
        channel: str,
        decision: SelectionDecision,
    ) -> InhibitionProfile: ...

    async def apply(
        self, decision: SelectionDecision, inhibition: InhibitionProfile
    ) -> None: ...

    async def step(
        self, scope: str, scope_level: ScopeLevel, channel: str, now_ms: int
    ) -> Tuple[SelectionDecision, InhibitionProfile]: ...

    # --- learning / reinforcement updates ---
    async def ingest_outcome(self, feedback: OutcomeFeedback) -> Sequence[LearningUpdate]: ...

    async def apply_learning(self, updates: Sequence[LearningUpdate]) -> None: ...

    # --- governance / invariants ---
    async def validate_candidate(self, candidate: CandidateAction) -> None: ...

    async def validate_selection(self, decision: SelectionDecision) -> None: ...

    async def validate_invariants(
        self,
        decision: SelectionDecision,
        inhibition: InhibitionProfile,
        stop_state: Optional[StopDecision],
    ) -> None: ...

    async def set_decision_mode(self, mode: DecisionMode) -> None: ...

    # --- introspection ---
    async def list_channels(self, scope: str, scope_level: ScopeLevel) -> List[str]: ...

    async def list_candidates(
        self, scope: str, scope_level: ScopeLevel, channel: str
    ) -> Sequence[CandidateAction]: ...

    async def summarize(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]: ...
