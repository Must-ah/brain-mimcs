# SpinalCord Spec (Edge I/O + Reflex Plane)

**Role (brain analogy):** Entry/exit point for *raw device I/O* plus *fast local reflex loops*.  
**Goal:** Keep the edge fast, bounded, and safe. SpinalCord should **ignore/reject** non-spinal message types.

---

## 1) Responsibilities

### Must do
- **Ingest afferents (sensors):** accept raw readings and lightweight device-side features.
- **Emit efferents (actuation):** deliver device-level commands to actuators.
- **Support local reflex arcs:** optional fast “if X then Y” rules that can fire without waiting for upstream services.
- **Report outcomes:** publish actuator acknowledgements/outcomes (completion, failure, measured result).

### Must not do
- No global attention/gating logic (that’s Thalamus/TRN/Core).
- No global operating modes (that’s Hypothalamus/Brainstem/Core).
- No high-level planning or cross-room fusion (that’s Cortex).

---

## 2) Plane Type Safety (reject wrong types)

### Allowed inbound message types
1) **AfferentSignal** (sensor → spinal)
2) **EfferentCommand** (motor path → spinal → actuator)
3) **ReflexRule / ReflexTrigger** (local reflex control)

### Rejected inbound types (examples)
- **RelayBundle**, **GateState**, **Modulator**, **GlobalModeUpdate**
- Any message whose `origin_plane != "reliable"` when targeting efferents (to prevent bypass)

### Rejection behavior
- **Drop** without processing.
- Emit **RejectEvent** to Reflect plane (Broker X) with:
  - `reason` (`wrong_type`, `wrong_direction`, `bad_schema_version`, `unauthorized_topic`)
  - `original_topic`, `publisher_id`, `timestamp_ms`, `correlation_id` (if present)

---

## 3) Topics (MQTT prefixes owned by Spinal broker)

### Afferents (upward)
- `/sc/aff/{scope_level}/{scope}/sensor/{sensor_type}/device/{device_id}`
- `/sc/aff/{scope_level}/{scope}/state/{state_type}/device/{device_id}`  (proprioception-like)

### Efferents (downward to devices)
- `/sc/eff/{scope_level}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}`

### Reflex (local)
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/configure`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/trigger`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/fire/{action_id}`
- `/sc/reflex/{scope_level}/{scope}/rule/{reflex_id}/report/{action_id}`

### Outcomes / acknowledgements (upward to Reliable broker)
- `/sc/out/{scope_level}/{scope}/device/{device_id}/action/{action_id}`

> **Rule:** Spinal topics are **device-addressed**. High fan-in/out is expected.

---

## 4) Contract templates (transport-agnostic)

### 4.1 AfferentSignal
**Required**
- `message_type: "AfferentSignal"`
- `schema_version`
- `scope_level`, `scope`
- `device_id`, `sensor_type`
- `timestamp_ms`
- `payload` (reading/feature + units)

**Optional**
- `correlation_id`
- `confidence`, `salience` (if computed at edge)

### 4.2 EfferentCommand
**Required**
- `message_type: "EfferentCommand"`
- `schema_version`
- `scope_level`, `scope`
- `device_id`, `actuator_type`
- `action_id` (idempotency key)
- `timestamp_ms`
- `deadline_ms` (recommended)
- `payload` (desired setpoint/trajectory)

**Optional**
- `priority`
- `safety_constraints` (min/max, rate limits)

### 4.3 OutcomeEvent
**Required**
- `message_type: "OutcomeEvent"`
- `schema_version`
- `scope_level`, `scope`
- `device_id`
- `action_id`
- `timestamp_ms`
- `status` (`ack`, `in_progress`, `done`, `failed`)
- `payload` (measured result / error codes)

### 4.4 RejectEvent (for observability)
- `message_type: "RejectEvent"`
- `reason`, `original_topic`, `publisher_id`, `timestamp_ms`
- `correlation_id` (optional)
- `payload_hash` (optional)

---

## 5) QoS + expiry policy (recommendation)

- **AfferentSignal:** QoS 0, short expiry; allow drop/downsample/coalesce.
- **EfferentCommand:** QoS 1 (or 2 if needed), must be idempotent by `action_id`.
- **OutcomeEvent:** QoS 1, moderate expiry.
- **Reflex:** QoS 0/1 depending on criticality; keep payload tiny.

---

## 6) Broker boundary rules (default)

- **Upward:** Spinal does **not** forward raw floods; Brainstem/Core reads afferents and publishes summaries.
- **Downward:** Spinal accepts device-level efferents only from the motor path (Reliable broker / authorized identities).

---

## 7) Minimal checklist (to declare SpinalCord “done”)

- [ ] Topic prefixes fixed and ACL’d per device identity.
- [ ] Afferent schema + versioning published.
- [ ] Command idempotency (`action_id`) enforced.
- [ ] Outcome reporting standardized.
- [ ] RejectEvent emitted for wrong-type/wrong-direction messages.
