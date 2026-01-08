# Hypothalamus Interface Spec (General, Implementation-Agnostic)

This document defines a **crisp but general** “Hypothalamus” interface for a brain-inspired architecture: *what it is responsible for, what signals it consumes/produces, and what invariants must hold*—without assuming any specific topology, transport (pub-sub vs RPC), or component layout.

---

## 1) Purpose

**Maintain system “homeostasis”** by continuously sensing internal state and issuing **corrective regulation** via:
- **Fast, targeted control outputs** (autonomic-like), and
- **Slow, global modulation outputs** (endocrine-like).

In brain terms, this mirrors hypothalamic control over **autonomic** centers and the **pituitary/endocrine** axis.

---

## 2) Anatomical framing (for the analogy)

- Located **beneath the thalamus**, bordering the **3rd ventricle**, and connected to the pituitary via the **infundibulum** (stalk).
- Acts as a **controller** for internal stability (temperature, fluid balance, energy balance, stress, sleep–wake, circadian timing).

(Reference basis: your hypothalamus notes + standard neuroanatomy summaries.)

---

## 3) Divisions (how it’s organized)

To stay compatible with multiple sources, define divisions using a **two-axis scheme**:

### 3.1 Anterior–Posterior regions (3 or 4, depending on convention)
Common regional breakdown:
1) **Anterior / Chiasmatic (supraoptic) region**
2) **Middle / Tuberal region**
3) **Posterior / Mammillary region**

Some texts treat **Preoptic** as a separate anterior-most region, giving **4 regions**:
- **Preoptic**, **Supraoptic/Chiasmatic**, **Tuberal**, **Mammillary**

**Spec guidance:** support both by allowing a `region` label from {preoptic, anterior/chiasmatic, tuberal, mammillary}.

### 3.2 Medial–Lateral zones (3 zones)
- **Periventricular zone** (near ventricle; many hypophysiotropic/endocrine control neurons)
- **Medial zone** (many discrete nuclei)
- **Lateral zone** (diffuse lateral hypothalamic area; arousal/feeding related)

**Spec guidance:** treat `zone` as {periventricular, medial, lateral}.

---

## 4) Key nuclei/modules (what they “do” at a high level)

This spec does **not** require you to model every nucleus, but it defines stable *functional module labels* that can be used as routing keys, capability tags, or policy domains.

### Circadian timing
- **SCN (suprachiasmatic nucleus)**: master circadian clock; entrained by retinal light input.

### Stress + autonomic/endocrine hub
- **PVN (paraventricular nucleus)**: major integrator for **stress** and **autonomic regulation**; drives HPA-axis endocrine signaling and autonomic outputs.

### Fluid balance
- **SON + PVN (magnocellular neurons)**: release **vasopressin (ADH)** and **oxytocin** via posterior pituitary pathway.

### Sleep–wake regulation
- **VLPO**: sleep-promoting (inhibits arousal systems).
- **LHA (orexin/hypocretin)**: wake-stabilizing / arousal-promoting; also linked to feeding motivation.
- **TMN (histamine)**: wake-promoting arousal node.

### Energy balance / feeding circuits
- **Arcuate nucleus**: metabolic sensing (leptin/ghrelin/insulin inputs) and feeding-related control signals.
- **VMH/VMN**: key node in feeding/satiety and defensive/sexual behavior circuits (avoid “single satiety center” language—modern view is circuit-based).

### Memory relay (hypothalamic-associated)
- **Mammillary bodies**: part of a memory circuit (Papez circuit relay).

---

## 5) Interface: responsibilities

The Hypothalamus interface MUST support these responsibilities (contracts), without prescribing implementation:

1) **Internal-state estimation**
   - Maintain an estimate of “internal variables” (homeostatic state).
   - Accept updates from multiple sources (metrics, alerts, user context, learned models).

2) **Closed-loop regulation**
   - Convert state estimates into corrective signals.
   - Prefer proportional, bounded control (avoid oscillation/instability).

3) **Timescale separation**
   - Produce both **fast control** (seconds/sub-seconds) and **slow modulation** (minutes-hours) outputs.

4) **Priority under stress**
   - Detect overload/threat states and drive stabilizing actions (throttle, shed load, degrade gracefully).

5) **Rhythm and scheduling**
   - Provide circadian/time-based policies (quiet hours, energy schedules, maintenance windows).

6) **Conflict mediation between drives**
   - When goals compete (performance vs battery; privacy vs sensing; quiet hours vs alerting), publish a coherent bias policy rather than contradictory commands.

---

## 6) Interface: signal classes

### 6.1 Inputs (what Hypothalamus consumes)
Define inputs as **semantic signal classes** (implementation-agnostic):

- **Interoceptive signals** (internal state)
  - Energy/battery, thermal, compute load, queue pressure, reliability/error rate, network quality.
- **Affective salience / threat**
  - “This is urgent/unsafe” signals (e.g., security risk, safety hazard, repeated failures).
- **Cognitive constraints / preferences**
  - User policies, schedules, privacy rules, priority overrides.
- **Circadian entrainment**
  - Time-of-day, light/occupancy cues, calendar signals.
- **Physiological-like slow signals**
  - Trends: rolling reliability, long-term energy depletion, chronic overload.

### 6.2 Outputs (what Hypothalamus produces)
Two output “pathways” to preserve the biological analogy and enforce architectural clarity:

**A) AutonomicOutputs (fast, targeted control)**
- Scoped control signals directed to “body-facing” or “control-plane” subsystems (e.g., Brainstem/SpinalCord analogs).
- Examples (semantic): `throttle`, `shed_load`, `prioritize_safety`, `enter_degraded_mode`, `cooldown`, `pause_noncritical_tasks`.

**B) EndocrineOutputs (slow, global modulation)**
- System-wide biases that tune behavior rather than command specific actions.
- Examples (semantic): `energy_saving_bias`, `high_alert_bias`, `quiet_hours_bias`, `privacy_bias`, `maintenance_bias`.

**C) Reporting/telemetry (optional)**
- Publish a concise “homeostatic state summary” for other modules to interpret (not for direct control).

---

## 7) Invariants (must always hold)

These are the **stability guarantees** that keep the interface crisp and general:

1) **Closed-loop control**
   - Outputs are driven by measured state + feedback, not one-off rules only.

2) **No direct perception/planning**
   - Hypothalamus does not do heavy perception, scene understanding, or long-horizon planning.
   - It *regulates*; it does not “think.”

3) **Timescale separation is preserved**
   - AutonomicOutputs must be safe to apply quickly and frequently.
   - EndocrineOutputs change slowly and should not flap.

4) **Stress has recovery**
   - Stress escalation must include de-escalation conditions (avoid “permanent alarm”).

5) **Bias > command (for slow outputs)**
   - EndocrineOutputs are biases/modulators, not hard actuator commands.

---

## 8) Non-goals (explicitly out of scope)

To keep this general and future-proof, the interface does NOT decide:
- Transport (pub-sub vs RPC vs shared log).
- Exact deployment (central vs replicated vs embedded).
- Exact arbitration for “competing consumers” (that’s action-selection / basal ganglia territory).
- Data schemas for every sensor/actuator (that belongs to SpinalCord-like I/O normalization).

---

## 9) Extension points (how to evolve without breaking contracts)

You can add detail later by:
- Adding nucleus-scoped modules as capability tags (SCN, PVN, VLPO, LHA, TMN, Arcuate, VMH, SON).
- Introducing learned control policies while keeping the same input/output semantics.
- Adding additional “homeostatic variables” without changing the core separation of fast control vs slow modulation.

---

## 10) Minimal checklist (what to decide next, still without implementation)

- Define the **homeostatic variable set** (the “internal state vector”).
- Define **stress thresholds** and recovery rules (hysteresis to avoid flapping).
- Define a small set of **endocrine bias types** (3–7 max) so other modules can reliably respond.
- Define the allowed **scopes** (device / room / house / user session) for autonomic vs endocrine outputs.

---

## Notes on terminology used here

- **Interface package:** a shared “contract bundle” (types, signal classes, invariants) used by many components.
- **Contract template:** the repeatable structure used to specify modules crisply without committing to implementation:
  - Purpose → Responsibilities → Inputs/Outputs → Invariants → Non-goals → Extension points.
- **Control plane vs data plane:** control plane = modulators/biases/gating; data plane = payload content/streams.
- **Timescale separation:** fast control reacts quickly; slow modulation sets long-term bias (reduces instability).


```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Protocol, Sequence


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
    SCN = "scn"          # circadian timing
    PVN = "pvn"          # stress + autonomic/endocrine hub
    SON = "son"          # fluid balance hormones
    VLPO = "vlpo"        # sleep-promoting
    LHA = "lha"          # orexin/arousal/feeding
    TMN = "tmn"          # histamine/arousal
    ARCUATE = "arcuate"  # metabolic sensing
    VMH = "vmh"          # feeding/defense/sex behaviors
    MAMMILLARY = "mammillary_bodies"  # memory relay


class SignalClass(str, Enum):
    INTEROCEPTIVE = "interoceptive"      # internal state metrics
    SALIENCE_THREAT = "salience_threat"  # urgent/unsafe flags
    COGNITIVE_CONSTRAINT = "cognitive_constraint"  # user prefs/policies
    CIRCADIAN_ENTRAINMENT = "circadian_entrainment"  # time/light cues
    SLOW_TREND = "slow_trend"            # rolling trends (reliability/energy)


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


# ---------- Interface protocols (contracts) ----------

class SignalSink(Protocol):
    def accept(self, signal: SignalEnvelope) -> None: ...


class SignalSource(Protocol):
    def subscribe(self, signal_class: SignalClass, scope: Optional[str] = None) -> None: ...
    def unsubscribe(self, signal_class: SignalClass, scope: Optional[str] = None) -> None: ...


class AutonomicOutputPort(Protocol):
    def publish_autonomic(self, decision: RegulationDecision) -> None: ...


class EndocrineOutputPort(Protocol):
    def publish_endocrine(self, decision: RegulationDecision) -> None: ...


class HomeostaticStateStore(Protocol):
    def get_state(self, scope: str, scope_level: ScopeLevel) -> Optional[HomeostaticState]: ...
    def put_state(self, state: HomeostaticState) -> None: ...


class PolicyEngine(Protocol):
    def evaluate(self, state: HomeostaticState, signals: Sequence[SignalEnvelope]) -> RegulationDecision: ...


# ---------- Main Hypothalamus class skeleton ----------

class Hypothalamus:
    def __init__(
        self,
        state_store: HomeostaticStateStore,
        policy_engine: PolicyEngine,
        autonomic_port: AutonomicOutputPort,
        endocrine_port: EndocrineOutputPort,
    ) -> None:
        ...

    # --- ingestion / sensing ---
    def ingest(self, signal: SignalEnvelope) -> None:
        ...

    def ingest_batch(self, signals: Sequence[SignalEnvelope]) -> None:
        ...

    # --- state estimation (closed-loop) ---
    def update_state(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> HomeostaticState:
        ...

    def get_state(self, scope: str, scope_level: ScopeLevel) -> Optional[HomeostaticState]:
        ...

    # --- regulation / outputs ---
    def decide(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> RegulationDecision:
        ...

    def apply(self, decision: RegulationDecision) -> None:
        ...

    def step(self, scope: str, scope_level: ScopeLevel, now_ms: int) -> RegulationDecision:
        ...

    # --- circadian / scheduling ---
    def set_circadian_profile(self, scope: str, profile: Mapping[str, Any]) -> None:
        ...

    def compute_circadian_phase(self, now_ms: int, scope: Optional[str] = None) -> Mapping[str, Any]:
        ...

    # --- stress handling ---
    def compute_stress_index(self, state: HomeostaticState, signals: Sequence[SignalEnvelope]) -> float:
        ...

    def enter_stress_mode(self, scope: str, scope_level: ScopeLevel, now_ms: int, reason: str) -> RegulationDecision:
        ...

    def exit_stress_mode(self, scope: str, scope_level: ScopeLevel, now_ms: int, reason: str) -> RegulationDecision:
        ...

    # --- governance / invariants ---
    def validate_invariants(self, decision: RegulationDecision) -> None:
        ...

    def set_thresholds(self, thresholds: Mapping[str, float]) -> None:
        ...

    def set_hysteresis(self, hysteresis: Mapping[str, float]) -> None:
        ...

    # --- extension points (optional module tagging) ---
    def enable_module(self, module: HypothalamicModule) -> None:
        ...

    def disable_module(self, module: HypothalamicModule) -> None:
        ...

    def list_modules(self) -> List[HypothalamicModule]:
        ...
```