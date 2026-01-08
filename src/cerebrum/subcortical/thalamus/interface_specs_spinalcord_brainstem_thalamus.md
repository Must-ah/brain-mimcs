# Interface Specs (General, Crisp, Implementation-Agnostic)

This document defines **three core interface packages** for a brain-inspired system:
- **SpinalCord** (physical I/O + reflexes)
- **Brainstem** (global state / modulation)
- **Thalamus** (routing + gating semantics)

These are **contracts** (shared agreements) that other modules can implement or depend on, without committing to a specific deployment, broker, language, or topology.

---

## How to read this: the “contract template” (explained)

A **contract template** is a repeatable structure for defining an interface *clearly and safely* before you know the full system design.

Each interface below follows the same sections:

1) **Purpose**  
   One sentence: what this interface exists to do.

2) **Responsibilities**  
   A short list of what the interface *must* cover.

3) **Inputs & Outputs (Signal Classes)**  
   The kinds of messages or calls allowed—described as *types of information*, not implementation details.

4) **Invariants (Rules that must always hold)**  
   Non-negotiable truths that keep the architecture coherent (e.g., “no direct actuator writes outside SpinalCord”).

5) **Non-goals (Explicitly out of scope for now)**  
   What this interface will *not* decide yet—so you stay general and avoid premature commitments.

6) **Extension Points**  
   Places where future decisions can plug in (e.g., transport choice, discovery mechanism, arbitration algorithm).

---

## Glossary (new terminology)

- **Interface package**: a shared specification of names, message shapes, and rules that multiple components can use.
- **Contract**: the agreement: “if you send this kind of signal with these fields and respect these rules, others will understand and behave correctly.”
- **Signal class**: a category of information (e.g., sensor observation, actuator command, modulator).
- **Data plane**: high-volume “payload” information (e.g., sensor features, observations).
- **Control plane**: low-volume “control/modulation” information (e.g., global modes, gating signals).
- **Coordination plane**: routing/gating/selection semantics that help modules interact without centralizing everything.
- **Invariant**: always-true architectural rule.
- **Non-goal**: intentionally deferred decision.
- **Extension point**: a controlled place where the system can evolve without breaking contracts.
- **Driver** (thalamic term): the main content/payload (“what happened”).
- **Modulator** (thalamic term): context/knobs (“how strongly, prioritize, suppress, synchronize”).
- **Gating**: allowing/suppressing information flow based on state/goals (TRN-inspired).
- **Scope**: the “sphere of influence” of a signal (device, room, household, user session, etc.).
- **Correlation**: linking multiple signals that belong to the same episode/event window (e.g., audio+video for the same moment).

---

# 1) SpinalCord Interface Spec

## Purpose
Normalize **physical sensors/actuators** into system signals and execute actuator commands, supporting **fast local reflexes**.

## Responsibilities
- Provide a uniform way to represent **sensor observations** (raw or feature-level).
- Provide a uniform way to issue **actuator commands** with acknowledgements.
- Support **reflex-class behaviors** that must run locally/fast (e.g., safety stop, basic stabilization).
- Expose device **capabilities** (what this sensor/actuator can do) in a discoverable form.

## Inputs & Outputs (Signal Classes)
**Inputs to SpinalCord**
- Actuator command requests (with scope, safety constraints, desired state).
- Reflex policies (small, local rules; optional, may be configured by higher levels).

**Outputs from SpinalCord**
- Sensor observations (with timestamps, confidence/quality metadata).
- Actuator state + acknowledgements (applied, rejected, failed, partial).
- Capability descriptors (static + dynamic health status).

## Invariants
- **All physical I/O passes through SpinalCord contracts** (no “side channel” actuator writes).
- Reflexes must remain **bounded**: local, fast, and safe (no long-running planning).
- Every emitted observation includes a **timestamp** and **source identity**.

## Non-goals (for now)
- No decision on device discovery method (mDNS, registry, QR pairing, etc.).
- No decision on transport (MQTT, gRPC, CAN, custom bus, etc.).
- No global arbitration logic (that belongs to action selection / basal ganglia analog).

## Extension Points
- Plug-in model for new device types and drivers.
- Choice of observation level (raw vs features) per modality.
- Policy mechanism for reflex rules (static config vs learned).

---

# 2) Brainstem Interface Spec

## Purpose
Publish and maintain **global operating state** (“system physiology”) that modulates how all modules behave.

## Responsibilities
- Broadcast global **modes** (awake/asleep, focus, privacy, safety, power-saving).
- Publish **arousal/priority context** (e.g., “urgent event ongoing”, “quiet hours”).
- Provide “vital function” signals: timebase/heartbeat, health summaries, degraded-mode flags.
- Coordinate *cross-cutting constraints* (e.g., “do not use microphone”, “limit power draw”).

## Inputs & Outputs (Signal Classes)
**Inputs to Brainstem**
- Global state updates from trusted sources (user intent, schedule, safety subsystem, power manager).
- Health/telemetry summaries from modules (aggregated, not raw streams).

**Outputs from Brainstem**
- Mode signals (global context).
- Priority/emergency level signals.
- Health/degradation signals (e.g., “network partition”, “battery low”).

## Invariants
- Brainstem signals are **modulators** (control plane), not payload perception results.
- Brainstem is **authoritative for global mode** at a given scope (household/user/session).
- Must degrade safely: if uncertain, prefer conservative defaults (privacy/safety).

## Non-goals (for now)
- No decision on who is “trusted” (authn/authz system not specified yet).
- No decision on how modes are computed (rules vs learning).
- No detailed policy language (only signal semantics).

## Extension Points
- Add new modes without breaking existing consumers (versioned mode taxonomy).
- Plug-in sources of global context (calendar, occupancy, manual override, safety sensors).

---

# 3) Thalamus Interface Spec

## Purpose
Define **routing + relay + gating semantics** so information can move between modules in an organized, attention-like way—without a central hub.

## Responsibilities
- Provide addressable **relay domains** (“nuclei”) that partition traffic by modality/domain.
- Define **Driver vs Modulator** signal classes and their allowed effects.
- Define **gating semantics** (TRN-inspired inhibition / attention profiles) per nucleus and scope.
- Define loop semantics:
  - Relay up to processors (cortex-like consumers),
  - Feedback modulation back to relay domains,
  - Higher-order routing between processors via association relay domains.

## Inputs & Outputs (Signal Classes)
**Inputs**
- Driver signals: payload observations or action-relevant content.
- Modulator signals: context knobs (gain, suppress, prioritize, synchronize, stop).
- Gate-control signals: inhibition levels / attention profiles.

**Outputs**
- Relayed driver streams to the appropriate processing domains.
- Gate state notifications (optional) so consumers can explain behavior (“why was this suppressed?”).

## Invariants
- Thalamus is a **protocol/contract**, not a single physical service (no required central node).
- Every signal declares:
  - **nucleus** (relay domain),
  - **scope**,
  - **timestamp**,
  - **correlation-id** (optional but recommended for multi-source binding).
- Gating is applied **per (scope, nucleus)** so concurrency scales naturally.
- Modulators may change *how* signals flow; they must not mutate driver payload history.

## Non-goals (for now)
- No decision on transport, brokers, or topic technology.
- No decision on discovery (how participants find nuclei streams).
- No decision on “exactly one executor” (action selection/arbitration belongs elsewhere).

## Extension Points
- Expand nucleus taxonomy (add new relay domains) without breaking old ones.
- Plug-in gating policies (simple rules → learned attention).
- Optional “association/binding event” schema to reference multiple sources (audio+video) without merging raw streams.

---

# How these three fit together (one sentence each)

- **SpinalCord**: “talk to the body” (sensors/actuators, reflex speed).
- **Brainstem**: “state of the organism” (global mode + priority context).
- **Thalamus**: “who hears what, when” (routing + gating + attention semantics).

---

## Next decisions (kept outside the contracts)
When you’re ready, you can add ADRs for:
- Discovery (how modules find each other)
- Trust/security (who can publish modulators/gate controls)
- Action selection arbitration (basal ganglia analog)
- Fusion strategy (where and how audio+video are combined)



---


```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple


# ---------- Core enums / types ----------

class NucleusClass(str, Enum):
    FIRST_ORDER = "first_order"     # sensory relay to primary cortex
    HIGHER_ORDER = "higher_order"   # cortex-to-cortex via thalamus
    DIFFUSE = "diffuse"             # intralaminar/midline-style
    GATE = "gate"                   # TRN-like gating


class NucleusId(str, Enum):
    # First-order sensory-style
    LGN = "lgn"      # visual relay
    MGN = "mgn"      # auditory relay
    VPL = "vpl"      # somatosensory (body)
    VPM = "vpm"      # somatosensory (face)

    # Motor-style
    VL = "vl"
    VA = "va"

    # Higher-order / association-style
    PULVINAR = "pulvinar"
    MD = "md"        # mediodorsal
    LP = "lp"

    # Diffuse / arousal-style
    CM = "cm"        # centromedian (intralaminar example)
    PF = "pf"        # parafascicular (intralaminar example)

    # Gate
    TRN = "trn"


class SignalKind(str, Enum):
    DRIVER = "driver"       # payload ("what happened")
    MODULATOR = "modulator" # context/control ("how to treat it")


class CortexLayer(str, Enum):
    L4 = "l4"  # relay target (first-order)
    L6 = "l6"  # reciprocal feedback to same nucleus (modulation)
    L5 = "l5"  # higher-order driver to thalamus for transthalamic routing


class GateMode(str, Enum):
    MULTI = "multi"                 # allow multiple channels
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
    def subscribe(self, kind: SignalKind, nucleus: Optional[NucleusId] = None, scope: Optional[str] = None) -> None: ...
    def unsubscribe(self, kind: SignalKind, nucleus: Optional[NucleusId] = None, scope: Optional[str] = None) -> None: ...


class CortexRelayPort(Protocol):
    def publish_to_cortex(self, decision: RouteDecision) -> None: ...


class ThalamusFeedbackPort(Protocol):
    def publish_feedback(self, envelope: ThalamicEnvelope) -> None: ...


class TRNGatePort(Protocol):
    def publish_gate_state(self, state: GateState) -> None: ...


class GateStore(Protocol):
    def get_gate_state(self, scope: str, scope_level: ScopeLevel, nucleus: NucleusId) -> Optional[GateState]: ...
    def put_gate_state(self, state: GateState) -> None: ...


class RoutingPolicy(Protocol):
    def compute_targets(self, envelope: ThalamicEnvelope) -> Sequence[RelayTarget]: ...


class GatingPolicy(Protocol):
    def evaluate(self, envelope: ThalamicEnvelope, current_gate: Optional[GateState]) -> GateState: ...


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
    ) -> None:
        ...

    # --- ingestion ---
    def ingest(self, envelope: ThalamicEnvelope) -> None:
        ...

    def ingest_batch(self, envelopes: Sequence[ThalamicEnvelope]) -> None:
        ...

    # --- routing / relay (Thalamus -> Cortex) ---
    def route(self, envelope: ThalamicEnvelope) -> RouteDecision:
        ...

    def relay(self, decision: RouteDecision) -> None:
        ...

    def relay_step(self, envelope: ThalamicEnvelope) -> RouteDecision:
        ...

    # --- gating (TRN-like inhibition control plane) ---
    def get_gate_state(self, scope: str, scope_level: ScopeLevel, nucleus: NucleusId) -> Optional[GateState]:
        ...

    def set_inhibition(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        inhibition: float,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState:
        ...

    def open_gate(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState:
        ...

    def close_gate(
        self,
        scope: str,
        scope_level: ScopeLevel,
        nucleus: NucleusId,
        timestamp_ms: int,
        reason: Optional[str] = None,
    ) -> GateState:
        ...

    def apply_attention_profile(
        self,
        scope: str,
        scope_level: ScopeLevel,
        timestamp_ms: int,
        allow: Sequence[Tuple[NucleusId, float]],
        suppress: Optional[Sequence[Tuple[NucleusId, float]]] = None,
        mode: GateMode = GateMode.MULTI,
        reason: Optional[str] = None,
    ) -> Sequence[GateState]:
        ...

    # --- feedback loops (Cortex -> Thalamus) ---
    def accept_cortex_feedback(self, envelope: ThalamicEnvelope) -> None:
        ...

    def publish_feedback(self, envelope: ThalamicEnvelope) -> None:
        ...

    # --- higher-order (transthalamic) routing semantics ---
    def route_higher_order(self, envelope: ThalamicEnvelope) -> RouteDecision:
        ...

    def register_cortex_mapping(
        self,
        nucleus: NucleusId,
        relay_targets: Sequence[RelayTarget],
    ) -> None:
        ...

    def unregister_cortex_mapping(self, nucleus: NucleusId) -> None:
        ...

    # --- governance / invariants ---
    def validate_envelope(self, envelope: ThalamicEnvelope) -> None:
        ...

    def validate_decision(self, decision: RouteDecision) -> None:
        ...

    def set_priority_rules(self, rules: Mapping[str, Any]) -> None:
        ...

    def set_backpressure_rules(self, rules: Mapping[str, Any]) -> None:
        ...

    # --- introspection / observability hooks (contract-level) ---
    def list_nuclei(self) -> List[NucleusId]:
        ...

    def describe_nucleus(self, nucleus: NucleusId) -> Mapping[str, Any]:
        ...

    def summarize_scope(self, scope: str, scope_level: ScopeLevel) -> Mapping[str, Any]:
        ...
```
