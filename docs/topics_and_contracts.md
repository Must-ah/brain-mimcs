# Brain‑Inspired Communication: Topics & Contracts (MQTT)

This repo models brain‑inspired system communication using **MQTT topics** as “tracts” and **typed contracts** as “signals”.
The goal is to run modules on different machines with minimal coupling: **only topics + contracts are shared**.

---

## Mental model

We separate the system into **planes** (like anatomical levels). Each plane owns a small set of topic prefixes and message types.

- **SpinalCord plane**: device **raw I/O** + **local reflex** loops  
- **Brainstem plane**: **relay/aggregation**, **fast patterns**, **global broadcast**  
- **(Upstream planes)**: Thalamus/Cortex decide attention/routing and produce higher-level behavior  
- **Reliable plane**: durable-ish **commands/outcomes**  
- **Reflect plane**: write‑only **audit / efference copy**

This yields a tract-like boundary:

> **Raw never goes up.** Spinal raw afferents are transformed into Brainstem **RelayBundles** before reaching higher layers.

---

## Brokers (recommended layout)

You can run a single broker at first, but for multi-machine robustness we assume separate brokers:

1. **Broker S (Spinal)**: `/sc/*`
2. **Broker C (Core/Control)**: `/bs/*`, `/B/*`, `/G/*`, `/D/*`
3. **Broker R (Reliable)**: `/C/*`, `/E/*`
4. **Broker X (Reflect)**: `/X/*`

See: `broker_boundary_bridge_policy.md` for boundary invariants and bridge allow-lists.

---

## Topic taxonomy (what each prefix means)

All topics are **scoped**:

- `scope_level`: `device | room | house | user_session`
- `scope`: identifier string (e.g., `living_room`, `house_1`)

### SpinalCord topics (Broker S) — device-addressed

**Afferents (sensors / device state)**
- `/sc/aff/{scope_level}/{scope}/sensor/{sensor_type}/device/{device_id}`
- `/sc/aff/{scope_level}/{scope}/state/{state_type}/device/{device_id}`

Meaning: raw readings or lightweight edge features (“afferent signals”).

**Efferents (device-level actuator commands)**
- `/sc/eff/{scope_level}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}`

Meaning: final motor output to devices (must be idempotent by `action_id`).

**Reflex (local fast loops)**
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/configure`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/trigger`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/fire/{action_id}`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/report/{action_id}`

Meaning: “spinal reflex arc” — fast local response without waiting for higher layers.

**Outcomes (optional edge outcome reporting)**
- `/sc/out/{scope_level}/{scope}/device/{device_id}/action/{action_id}`

Meaning: device acknowledgement / completion summary.

---

### Brainstem topics (Broker C) — scope-addressed summaries

**Relay bundles (typed summaries; upward-ready)**
- `/bs/relay/{scope_level}/{scope}/nucleus/{nucleus_id}`

Meaning: brainstem converts many raw afferents into summaries addressed to specific thalamic nuclei.
Typical nuclei: `lgn | mgn | vpl | vpm | pulvinar | md | ...` (see NucleusId enum).

**Pattern triggers / reports (fast patterned responses)**
- `/bs/pattern/{scope_level}/{scope}/{pattern_type}/trigger`
- `/bs/pattern/{scope_level}/{scope}/{pattern_type}/request`
- `/bs/pattern/{scope_level}/{scope}/{pattern_type}/report`

Meaning: startle/orient/stabilize-like fast responses.

**Global broadcasts**
- `/bs/global/{scope_level}/{scope}/alert`
- `/bs/global/{scope_level}/{scope}/arousal`

Meaning: fast “operating state” signals.

---

### Reliable topics (Broker R) — commands & learning-critical outcomes

**Commands**
- `/C/cmd/{scope_level}/{scope}/nucleus/{nucleus_id}/action/{action_id}`

Meaning: intentional actions (must be idempotent via `action_id`).

**Outcomes / Errors**
- `/E/outcome/{scope_level}/{scope}/action/{action_id}`
- `/E/error/{scope_level}/{scope}/action/{action_id}`

Meaning: success/failure feedback, prediction error, corrections.

---

### Reflect topics (Broker X) — audit / quarantine (write-only in prod)

**Reflection (efference copy / observability)**
- `/X/reflect/{scope_level}/{scope}/...`

**Quarantine / rejects (canonical)**
- `/X/reflect/{scope_level}/{scope}/lane/reject`

Meaning: “this message was ignored/rejected at ingress” for debugging and safety.

---

## Contract model (what each message means)

All messages carry a small **envelope** (`Meta`) and a typed payload.  
This is the minimum required to run services on different machines safely.

### Shared envelope (`Meta`)
Required fields:
- `message_type` — explicit type tag (e.g., `AfferentSignal`, `RelayBundle`)
- `schema_version` — version string (e.g., `v1`, `v1.1`)
- `origin_plane` — `spinal | brainstem | thalamus | cortex | reliable | reflect`
- `timestamp_ms` — producer time (for correlation, not strict ordering)

Optional fields:
- `correlation_id` — bind multi-step flows (sensor→relay→decision→command→outcome)
- `source` — producer identity (device/service)

### Spinal contracts (examples)
- **AfferentSignal**: a sensor reading or simple feature at the edge
- **EfferentCommand**: device-level command (must include `action_id`)
- **OutcomeEvent**: ack/done/failed for a given `action_id`
- **ReflexRule / ReflexTrigger / ReflexEvent**: reflex configuration and execution

### Brainstem contracts (examples)
- **RelayBundle**: summarized, windowed features addressed to a `target_nucleus`
- **PatternTrigger / PatternResponse**: urgent stereotyped response requests/results
- **GlobalBroadcast**: “operating state” with expiry/half-life

### Ops contract
- **RejectEvent**: emitted when a module rejects a message (wrong type, wrong direction, bad version)

---

## Versioning rules (contract stability)

- Producers may **add fields** (backward compatible).
- Consumers must **ignore unknown fields**.
- Breaking changes require a new `schema_version`.
- During upgrades: consumers should accept `{v1, v1.1}` before any producer emits `v1.1`.

---

## Type safety / rejection (how planes reject wrong types)

Each plane has an **ingress allow-list** of `message_type` values.

- **SpinalCord** accepts only: `AfferentSignal`, `EfferentCommand`, `ReflexRule`, `ReflexTrigger`
- **Brainstem** accepts only: `AfferentSignal` (for transformation), `RelayBundle`, `PatternTrigger`, `GlobalBroadcast`

If a message violates the plane’s allow-list (or has missing/invalid meta), it is **dropped** and a `RejectEvent` is published to:

- `/X/reflect/{scope_level}/{scope}/lane/reject`

This prevents one misconfigured machine from poisoning the rest of the system.

---

## Example flows

### A) Sensor → Brainstem summary (raw becomes relay)
1) Device publishes `AfferentSignal` on `/sc/aff/...`
2) Brainstem aggregates and publishes `RelayBundle` on `/bs/relay/...`

### B) Command → device actuation → outcome
1) Decision publishes a `Command` on `/C/cmd/.../action/{action_id}`
2) Motor path delivers `EfferentCommand` on `/sc/eff/.../cmd/{action_id}`
3) Device reports `OutcomeEvent` on `/E/outcome/.../action/{action_id}` (or `/sc/out/...` then bridged)

### C) Wrong-type rejection
A component publishes the wrong `message_type` to Brainstem ingress → Brainstem emits `RejectEvent` to Reflect.

---

## Where things live in code

Pattern A layout (single source of truth for shared types):
- `src/shared/contracts_base_async.py` — shared enums, `Meta`, `RejectEvent`, bus protocol + in-memory bus
- `src/shared/topics_async.py` — shared topic helpers (e.g., reject topic)
- `src/spinal_cord/spinal_contracts_async_refactored_v2.py` — spinal contracts + topic helpers + `SpinalCord` façade
- `src/brainstem/brainstem_contracts_async_refactored_v2.py` — brainstem contracts + topic helpers + `Brainstem` façade

Specs:
- `src/spinal_cord/spinalcord_spec.md`
- `src/brainstem/brainstem_spec.md`
- `broker_boundary_bridge_policy.md`
- `mosquitto_brain_like_communication.md`

---

## Running demos (local, in-memory)

These demos use an in-memory bus to validate contracts and rejection behavior before wiring to real MQTT.

- Spinal ↔ Brainstem demo:
  - `demo_spinal_brainstem.py` (or `demo_spinal_brainstem_fixed.py`)
- Runner:
  - `python main.py --demo spinal-brainstem`

If you run with `uv`:
- `uv run main.py --demo spinal-brainstem`

---

## Glossary

- **Plane**: an architectural level (Spinal/Brainstem/Thalamus/…)
- **Afferent**: inbound sensory signal (device→system)
- **Efferent**: outbound motor signal (system→device)
- **RelayBundle**: summarized, typed signal addressed to a thalamic nucleus (raw becomes relay)
- **Tract boundary**: rule that raw does not propagate upward; it is transformed into summaries
- **Reflection**: best-effort audit copy (must not block operations)
