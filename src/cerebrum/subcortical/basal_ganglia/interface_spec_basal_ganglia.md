# Basal Ganglia Interface Spec (Single Crisp Page, Implementation-Agnostic)

This spec defines a **Basal Ganglia** interface as a reusable contract bundle (types + semantics + invariants) for **action selection** and **suppression of competitors**, without assuming any topology, transport, or deployment model.

---

## 1) Purpose

**Select which candidate action/behavior/thought is allowed to proceed right now**, while **suppressing competing candidates**, and **learn** future selection preferences from reward/punishment feedback.

---

## 2) What it is (functional framing)

Basal ganglia act as a **gating system**:
- Default state: downstream “action channels” are **inhibited** (gate closed).
- Selection happens by **disinhibiting** one channel (“GO”) while maintaining/strengthening inhibition of others (“NO-GO”).
- A fast **global brake** (“STOP”) can transiently suppress many channels, then allow reselection.

---

## 3) Divisions (how it’s organized)

### 3.1 Core nodes (canonical set)
- **Striatum** (caudate + putamen; ventral striatum / nucleus accumbens)
- **GPe / GPi** (external/internal globus pallidus; ventral pallidum in limbic loop)
- **STN** (subthalamic nucleus)
- **SNr / SNc** (substantia nigra pars reticulata/compacta)

### 3.2 Pathways (3 functional routes)
- **Direct (“GO”)**: enables a selected channel (disinhibition downstream).
- **Indirect (“NO-GO”)**: suppresses competing channels (increases inhibition).
- **Hyperdirect (“STOP”)**: rapid global suppression via cortex → STN → output nuclei.

### 3.3 Parallel loops (“channels”)
Same motif repeated for different domains:
- **Motor** (movement selection/vigor)
- **Oculomotor** (gaze/target selection)
- **Cognitive/associative** (rule/plan selection)
- **Limbic** (value/motivation/habit)

**Spec guidance:** treat “channel” as a first-class addressable concept.

---

## 4) Interface: responsibilities

1) **Candidate arbitration**
   - Accept multiple action candidates and choose **one (or a small set)** to enable under current policy.

2) **Competition suppression**
   - Maintain inhibition on non-selected candidates to reduce interference.

3) **Emergency stop**
   - Provide a fast, broad suppression command that temporarily blocks selection.

4) **Reinforcement-driven adaptation**
   - Update future selection bias based on reward/punishment prediction errors and outcomes.

5) **Channelized operation**
   - Support parallel, mostly-independent selection across channels/scopes (e.g., room vs device vs house).

---

## 5) Interface: signal classes (contracts only)

### 5.1 Inputs
- **ActionCandidates**
  - A set of candidates with: channel id, preconditions, cost/utility estimate, urgency, deadline, confidence.
- **Context / State**
  - System mode biases (e.g., from Hypothalamus/Brainstem), resource constraints, safety/privacy rules.
- **StopSignals**
  - Immediate suppression request (global or channel-scoped).
- **Outcome / RewardFeedback**
  - Success/failure, user satisfaction signals, safety outcomes, reward/punishment scalar, prediction error.

### 5.2 Outputs
- **SelectionDecision**
  - Which candidate(s) are enabled now, with a confidence/priority score.
- **InhibitionProfile**
  - Which candidates/channels are actively suppressed and at what strength.
- **StopDecision**
  - A stop/brake instruction (global or scoped) with reason and timeout/decay.
- **LearningUpdate (optional as a contract)**
  - Bias updates for future selection (policy weights, value estimates, habit strength).

---

## 6) Invariants (must always hold)

1) **Default suppression**
   - If no decision is made, action channels remain inhibited (safe-by-default).

2) **Exact-one enablement (by default)**
   - For a given `(scope, channel)` window, the contract prefers **exactly one winner** unless explicitly configured for multi-winner.

3) **Stop dominates**
   - STOP overrides GO/NO-GO during its active window; selection resumes only after stop expires or is released.

4) **Separation from execution**
   - Basal ganglia **select**, they do not execute. Execution belongs to downstream “motor”/actuator systems.

5) **Learning is bounded**
   - Updates must be bounded to avoid runaway oscillation (no infinite bias amplification).

---

## 7) Non-goals (explicitly out of scope)

- Does not define the internal learning algorithm (RL variant, model-based vs model-free).
- Does not define transport (pub-sub vs RPC) or deployment (central vs replicated).
- Does not define perception or world-model construction (cortex-like responsibilities).
- Does not define detailed actuator drivers (spinal-cord-like responsibilities).

---

## 8) Extension points (future detail without breaking the contract)

- Add multiple **scopes** (device/room/house) with independent inhibition profiles.
- Add “habit” vs “goal-directed” selection modes (policy layering).
- Add multi-winner selection for safe, composable actions (e.g., enable both “audio” and “video” attention channels).
- Add explicit “value” stores (per channel) and confidence calibration.

---

## 9) Minimal checklist (what to decide next, still no implementation)

- Define the **candidate format** (fields required for arbitration).
- Define what constitutes **a channel** and what constitutes **a scope**.
- Define **STOP semantics** (who may request it, how long it lasts, decay/hysteresis).
- Decide whether selection is **exact-one** or **bounded multi-winner** by default.
- Define the **reward/outcome signals** available for learning (and privacy limits).

---



You’re right — here’s the **Basal Ganglia skeleton code** (classes + methods only, Python, no implementation):

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


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
    channel: str                  # competition channel / action family
    loop: BGLoop                  # motor/cognitive/limbic/etc.
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
    channel: Optional[str]        # None = global stop
    reason: str
    duration_ms: Optional[int]


@dataclass(frozen=True)
class OutcomeFeedback:
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    action_id: str
    success: bool
    reward: Optional[float]       # scalar reward/punishment
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
    inhibition_strength: float    # 0..1
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
    channel: Optional[str]        # None = global
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
    update_type: str              # e.g., "value", "policy_bias", "habit_strength"
    payload: Mapping[str, Any]


# ---------- Interface protocols (contracts) ----------

class CandidateStore(Protocol):
    def add(self, candidate: CandidateAction) -> None: ...
    def list(self, scope: str, scope_level: ScopeLevel, channel: str) -> Sequence[CandidateAction]: ...
    def remove(self, scope: str, scope_level: ScopeLevel, action_id: str) -> None: ...
    def clear_channel(self, scope: str, scope_level: ScopeLevel, channel: str) -> None: ...


class ContextStore(Protocol):
    def put(self, signal: ContextSignal) -> None: ...
    def get_snapshot(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]: ...


class StopStore(Protocol):
    def set(self, decision: StopDecision) -> None: ...
    def get(self, scope: str, scope_level: ScopeLevel, channel: Optional[str]) -> Optional[StopDecision]: ...
    def clear(self, scope: str, scope_level: ScopeLevel, channel: Optional[str]) -> None: ...


class SelectionPolicy(Protocol):
    def select(
        self,
        candidates: Sequence[CandidateAction],
        context: Mapping[str, Any],
        mode: DecisionMode,
    ) -> SelectionDecision: ...


class InhibitionPolicy(Protocol):
    def compute_inhibition(
        self,
        candidates: Sequence[CandidateAction],
        selection: SelectionDecision,
        context: Mapping[str, Any],
    ) -> InhibitionProfile: ...


class LearningPolicy(Protocol):
    def update(self, feedback: OutcomeFeedback, context: Mapping[str, Any]) -> Sequence[LearningUpdate]: ...


class DecisionPort(Protocol):
    def publish_selection(self, decision: SelectionDecision) -> None: ...
    def publish_inhibition(self, profile: InhibitionProfile) -> None: ...
    def publish_stop(self, decision: StopDecision) -> None: ...
    def publish_learning(self, updates: Sequence[LearningUpdate]) -> None: ...


# ---------- Main Basal Ganglia class skeleton ----------

class BasalGanglia:
    """
    Contract-only skeleton for a Basal Ganglia interface package:
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
    ) -> None:
        ...

    # --- candidate ingestion ---
    def submit_candidate(self, candidate: CandidateAction) -> None:
        ...

    def submit_candidates(self, candidates: Sequence[CandidateAction]) -> None:
        ...

    def withdraw_candidate(self, scope: str, scope_level: ScopeLevel, action_id: str) -> None:
        ...

    # --- context ingestion ---
    def ingest_context(self, signal: ContextSignal) -> None:
        ...

    # --- STOP / brake control ---
    def request_stop(self, signal: StopSignal) -> StopDecision:
        ...

    def release_stop(self, scope: str, scope_level: ScopeLevel, channel: Optional[str], now_ms: int, reason: str) -> StopDecision:
        ...

    def get_stop_state(self, scope: str, scope_level: ScopeLevel, channel: Optional[str]) -> Optional[StopDecision]:
        ...

    # --- selection (GO) and suppression (NO-GO) ---
    def decide(self, scope: str, scope_level: ScopeLevel, channel: str, now_ms: int) -> SelectionDecision:
        ...

    def compute_inhibition(self, scope: str, scope_level: ScopeLevel, channel: str, decision: SelectionDecision) -> InhibitionProfile:
        ...

    def apply(self, decision: SelectionDecision, inhibition: InhibitionProfile) -> None:
        ...

    def step(self, scope: str, scope_level: ScopeLevel, channel: str, now_ms: int) -> Tuple[SelectionDecision, InhibitionProfile]:
        ...

    # --- learning / reinforcement updates ---
    def ingest_outcome(self, feedback: OutcomeFeedback) -> Sequence[LearningUpdate]:
        ...

    def apply_learning(self, updates: Sequence[LearningUpdate]) -> None:
        ...

    # --- governance / invariants ---
    def validate_candidate(self, candidate: CandidateAction) -> None:
        ...

    def validate_selection(self, decision: SelectionDecision) -> None:
        ...

    def validate_invariants(self, decision: SelectionDecision, inhibition: InhibitionProfile, stop_state: Optional[StopDecision]) -> None:
        ...

    def set_decision_mode(self, mode: DecisionMode) -> None:
        ...

    # --- introspection ---
    def list_channels(self, scope: str, scope_level: ScopeLevel) -> List[str]:
        ...

    def list_candidates(self, scope: str, scope_level: ScopeLevel, channel: str) -> Sequence[CandidateAction]:
        ...

    def summarize(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]:
        ...
```
