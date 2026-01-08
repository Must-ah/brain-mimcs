# Limbic Interface Spec (Single Crisp Page, Implementation-Agnostic)

This spec defines a **Limbic** interface as a contract bundle (signal classes + semantics + invariants) for **memory** and **emotional significance**—without assuming topology, transport (pub-sub vs RPC), or deployment.

The spec follows the “contract template” you’ve been using:
**Purpose → Responsibilities → Divisions → Inputs/Outputs → Invariants → Non-goals → Extension points**.

---

## 1) Verify (grounded in your source notes)

### What’s solid
- The limbic structures are treated as **two major components**: **hippocampal formation** (memory/context) and **amygdala** (emotion/threat learning), which interact bidirectionally and modulate cortex and subcortical systems.  
- The hippocampal formation is described with a **trisynaptic circuit**: EC → DG → CA3 → CA1 → Subiculum → back to EC, and with a **3-layer allocortical** organization.  
- The amygdala is described as **nuclei** (not layered cortex), with a fast thalamic input route and a slower cortical input route, and strong outputs to hypothalamus/brainstem/PAG for defensive responses.  
- Fear extinction is described via **vmPFC/infralimbic → ITC → inhibition of CeA**, preserving the fear memory but blocking expression (“extinction is not erasure”).

### Important nuance (your own limbic-lobe note)
- The “limbic system” concept is **imprecise** in modern neuroscience; emotion is distributed. The anatomical “limbic lobe” term remains useful as a cortical ring description.

(Reference basis: your limbic communication maps + limbic lobe overview + the architecture decisions doc.)

---

## 2) Purpose

**Assign meaning over time** by:
- **Encoding and retrieving episodic/contextual memory** (hippocampal formation), and
- **Assigning emotional salience / threat value** and driving urgent defensive/autonomic responses (amygdala),
so that the rest of the system can prioritize what matters and learn from experience.

---

## 3) Divisions (how it’s organized)

### 3.1 Hippocampal formation (memory/context subsystem)
Functional modules (labels, not mandatory components):
- **Entorhinal cortex (EC):** gateway to/from cortex
- **Dentate gyrus (DG):** pattern separation
- **CA3:** pattern completion / associative retrieval
- **CA1:** comparison / output stage
- **Subiculum:** major output stage (to EC and beyond)

### 3.2 Amygdala (salience/threat subsystem)
Functional modules (labels, not mandatory components):
- **Lateral nucleus (LA):** primary sensory input (thalamus + cortex)
- **Basal nucleus / BLA:** integration + learning; biases cortex/hippocampus; projects to motivated behavior circuits
- **Central nucleus (CeA):** output for defensive/autonomic expression (PAG/hypothalamus/brainstem)
- **Medial nucleus (MeA):** social/olfactory/reproductive-related outputs to hypothalamus
- **Intercalated cells (ITC):** inhibitory gate that can suppress CeA (key for extinction)

### 3.3 Canonical circuits (for interface semantics)
- **Trisynaptic hippocampal circuit** (EC→DG→CA3→CA1→Subiculum)
- **Papez circuit memory loop** (Hippocampus→Fornix→Mammillary→Anterior thalamus→Cingulate→Parahippocampal→Hippocampus)
- **Fear expression loop** (LA/BLA→CeA→PAG/Hypothalamus/Brainstem)
- **Extinction gating** (vmPFC→ITC→inhibit CeA)

---

## 4) Responsibilities

1) **Episodic binding & contextualization (Hippocampus)**
   - Bind multimodal cortical representations into episodes.
   - Provide context cues for decision-making (“where/when/what else was happening?”).

2) **Pattern separation / pattern completion (Hippocampus)**
   - Separate similar episodes to avoid interference.
   - Retrieve full episodes from partial cues.

3) **Consolidation / replay (Hippocampus)**
   - Provide replay-like outputs to support longer-term cortical learning.

4) **Salience tagging & threat learning (Amygdala)**
   - Rapidly flag potentially dangerous/important events.
   - Learn associations between cues and outcomes (fear conditioning / valence).

5) **Urgent response triggering (Amygdala outputs)**
   - Drive immediate defensive/autonomic responses and arousal escalation through downstream ports.

6) **Extinction / regulation channel (Amygdala + PFC)**
   - Support an inhibitory “expression block” pathway for de-escalation without erasing memory.

---

## 5) Interface: signal classes (contracts only)

### 5.1 Inputs
- **CorticalPercepts**: structured percept summaries (not raw streams) from cortex-like processors
- **ThalamicFastCue**: fast, coarse cues (for rapid salience checks)
- **ContextCue**: partial cues used for retrieval (“sounds like last time…”, “same room/time…”, etc.)
- **OutcomeFeedback**: success/failure, reward/punishment, safety outcomes
- **TopDownRegulation**: cognitive reappraisal / de-escalation signals (PFC-like)
- **Physio/DriveState**: internal-state context (hypothalamus/brainstem-like modulators)

### 5.2 Outputs
- **EpisodicMemoryTrace**: encoded episode references + metadata (time, scope, features)
- **RetrievalResult**: retrieved episode(s) + confidence + context summary
- **ReplayBatch**: consolidation signals to cortex-like learners
- **SalienceTag**: importance score + “why” features (threat/novelty/value)
- **DefensiveResponseRequest**: urgent outputs to hypothalamus/brainstem/PAG-analog targets
- **MotivationBias**: bias signal to action selection (basal-ganglia-like) based on valence
- **ExtinctionGateUpdate**: increase/decrease inhibition of expression pathways

---

## 6) Invariants (must always hold)

1) **Separation of roles**
   - Hippocampus: memory/context; Amygdala: salience/threat/valence.

2) **Fast vs slow pathway distinction (salience)**
   - Fast threat checks may be coarse and must be correctable by slower evaluation.

3) **Extinction is not erasure**
   - De-escalation blocks expression but preserves stored association.

4) **Outputs are advisory or triggering—not full planning**
   - Limbic does not do long-horizon planning; it biases and triggers.

5) **Scope-awareness**
   - All limbic outputs must be scoped (device/room/house/session) to prevent global overreaction.

---

## 7) Non-goals

- Does not define the full cortical hierarchy or perception pipeline.
- Does not define the exact learning algorithms (RL, supervised, self-supervised).
- Does not define transport or storage engines.

---

## 8) Extension points

- Add separate “semantic memory” vs “episodic memory” stores.
- Add explicit “novelty detector” or “anomaly detector” modules feeding amygdala-like salience.
- Add richer context models (spatial maps, user identity models).



from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Mapping, Optional, Protocol, Sequence, Tuple

----


```python
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


# ---------- Ports (aligned naming) ----------

class CortexMemoryPort(Protocol):
    def publish_retrieval(self, result: RetrievalResult) -> None: ...
    def publish_replay(self, batch: ReplayBatch) -> None: ...


class AutonomicDefensePort(Protocol):
    def publish_defense(self, request: DefensiveResponseRequest) -> None: ...


class ActionSelectionBiasPort(Protocol):
    def publish_bias(self, bias: MotivationBias) -> None: ...


class ExtinctionControlPort(Protocol):
    def publish_extinction(self, update: ExtinctionGateUpdate) -> None: ...


# ---------- Stores (aligned naming) ----------

class EpisodicStore(Protocol):
    def put_episode(self, trace: EpisodicMemoryTrace) -> None: ...
    def get_episode(self, episode_id: str) -> Optional[EpisodicMemoryTrace]: ...
    def query(self, scope: str, scope_level: ScopeLevel, cue: Mapping[str, Any]) -> Sequence[EpisodicMemoryTrace]: ...


class SalienceStore(Protocol):
    def put_salience(self, tag: SalienceTag) -> None: ...
    def list_recent(self, scope: str, scope_level: ScopeLevel, window_ms: int, now_ms: int) -> Sequence[SalienceTag]: ...


class ExtinctionStore(Protocol):
    def get_inhibition(self, scope: str, scope_level: ScopeLevel) -> float: ...
    def set_inhibition(self, update: ExtinctionGateUpdate) -> None: ...


# ---------- Policies (aligned naming) ----------

class MemoryPolicy(Protocol):
    def encode(self, percepts: Sequence[SignalEnvelope], salience: Sequence[SalienceTag]) -> Optional[EpisodicMemoryTrace]: ...
    def retrieve(self, cue: SignalEnvelope) -> Optional[RetrievalResult]: ...
    def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> Optional[ReplayBatch]: ...


class SaliencePolicy(Protocol):
    def evaluate_fast(self, cue: SignalEnvelope) -> Optional[SalienceTag]: ...
    def evaluate_slow(self, percept: SignalEnvelope) -> Optional[SalienceTag]: ...
    def update_from_outcome(self, outcome: SignalEnvelope) -> None: ...


class DefensePolicy(Protocol):
    def decide_defense(self, tags: Sequence[SalienceTag], extinction_inhibition: float) -> Optional[DefensiveResponseRequest]: ...


class BiasPolicy(Protocol):
    def decide_bias(self, tags: Sequence[SalienceTag]) -> Optional[MotivationBias]: ...


class ExtinctionPolicy(Protocol):
    def compute_update(self, top_down: SignalEnvelope, current_inhibition: float) -> Optional[ExtinctionGateUpdate]: ...


# ---------- Main Limbic class (single aligned façade) ----------

class Limbic:
    """Contract-only skeleton for a Limbic interface package.

    Aligned with other region specs:
    - Accepts normalized SignalEnvelope inputs
    - Produces a LimbicDecision (memory + salience + defense + bias + extinction + replay)
    - Publishes via ports (cortex replay/retrieval, defense, bias, extinction)
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
    def ingest(self, signal: SignalEnvelope) -> None:
        ...

    def ingest_batch(self, signals: Sequence[SignalEnvelope]) -> None:
        ...

    # --- core functions ---
    def encode_episode(self, percepts: Sequence[SignalEnvelope], now_ms: int) -> Optional[EpisodicMemoryTrace]:
        ...

    def retrieve(self, cue: SignalEnvelope) -> Optional[RetrievalResult]:
        ...

    def evaluate_salience_fast(self, cue: SignalEnvelope) -> Optional[SalienceTag]:
        ...

    def evaluate_salience_slow(self, percept: SignalEnvelope) -> Optional[SalienceTag]:
        ...

    def apply_top_down_regulation(self, signal: SignalEnvelope) -> Optional[ExtinctionGateUpdate]:
        ...

    def ingest_outcome(self, outcome: SignalEnvelope) -> None:
        ...

    def plan_replay(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> Optional[ReplayBatch]:
        ...

    # --- decision + publish ---
    def decide(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> LimbicDecision:
        ...

    def apply(self, decision: LimbicDecision) -> None:
        ...

    def step(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> LimbicDecision:
        ...

    # --- governance / invariants ---
    def validate_signal(self, signal: SignalEnvelope) -> None:
        ...

    def validate_decision(self, decision: LimbicDecision) -> None:
        ...

    # --- introspection ---
    def summarize(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]:
        ...


```
### Not aligned

``` python
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
```