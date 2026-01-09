# Checkpoint v2: Brain-Inspired Architecture — SpinalCord/Brainstem + Topics/Contracts + Secure Media Sessions

This checkpoint captures **what we decided so far** so you can continue without rereading chat.

---

## 0) Status / what’s still undecided

### Decided

- **MQTT topics = routing (“where”)** and **wire contracts = meaning (“what”)**
- **Multi-language + internet-ready**: treat messages as a **wire protocol** (JSON now, CBOR later) validated by **JSON Schema**
- **Nested envelope**: `{ "meta": {…}, "payload": {…} }`
- **event vs state in topic**: `/.../event/...` (not retained) vs `/.../state/...` (retained)
- **Media is its own path** under **`/sc/media/...`** (not mixed with `/sc/aff/...`)
- **Media is pull-based**: MQTT only signals “something happened”; authorized clients pull WebRTC via gateway
- **HLC field reserved** for distributed causality + replay resistance

### Not decided yet

- Final **project name** (we only proposed candidates)
- Whether to use **one gateway** or **multiple gateways** from day 1 (we assumed gateway as default)
- Whether gateway returns **SDP directly** vs **offer endpoint URL** (both compatible with our contracts)

---

## 1) What SpinalCord and Brainstem “do” (in our architecture)

### SpinalCord (raw I/O + reflexes, device-proximal)

**Role:** edge-facing plane that:

- ingests **raw device signals** (sensors, device state)
- can execute **fast local reflex loops** (low latency, no higher-layer dependency)
- publishes **only raw/edge-typed signals** upward (never media streams; never high-level decisions)

**Key boundary rule:**

> If it’s **raw device I/O** or **reflex**, it lives in **SpinalCord topics**.

**Outputs:**

- Afferent sensor events (`AfferentSignal`)
- Efferent device commands (`EfferentCommand`) (often received from higher layers)
- Reflex reports/outcomes (what it fired, success/failure)
- **Media events** (not the stream) under `/sc/media/...`

### Brainstem (aggregation/relay + fast patterns + broadcasts, scope-level)

**Role:** mid-level plane that:

- subscribes to spinal signals and **aggregates / summarizes**
- emits **typed relay bundles** (low-rate, upward-ready)
- provides fast “pattern” behaviors and global broadcasts (like orienting/startle-like system responses)

**Key boundary rule:**

> Brainstem should not forward raw floods upward; it publishes **RelayBundles**.

**Outputs:**

- Relay bundles (`RelayBundle`) on `/bs/relay/...`
- Pattern triggers/reports on `/bs/pattern/...`
- Global broadcasts/states on `/bs/global/...`

---

## 2) Topic taxonomy (with event/state)

We adopted explicit **event vs state** in topics:

- `/.../event/...` = transient occurrences (not retained)
- `/.../state/...` = latest state (retained)

All topics are scoped by:

- `{scope_level}`: `device | room | house | user_session`
- `{scope}`: e.g. `living_room`, `house_1`

---

## 3) SpinalCord topics

### 3.1 Afferent sensors (events)

- `/sc/aff/event/{scope_level}/{scope}/sensor/{sensor_type}/device/{device_id}`

Example:

- `/sc/aff/event/room/living_room/sensor/motion/device/m1`

### 3.2 Efferent device commands (events)

- `/sc/eff/event/{scope_level}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}`

Example:

- `/sc/eff/event/room/living_room/act/light/device/lamp1/cmd/act-123`

### 3.3 Reflex (events)

- `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/configure`
- `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/trigger`
- optional execution/report:
  - `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/fire/{action_id}`
  - `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/report/{action_id}`

---

## 4) ✅ Media is its own path (Spinal only signals, never streams)

### 4.1 Media event (link-free spike)

**We decided media events do NOT include URLs/pointers**. They only say “something happened”.
Listeners already know how to connect (by convention or registry).

Event topic:

- `/sc/media/event/{scope_level}/{scope}/device/{device_id}/kind/{kind}`

Example:

- `/sc/media/event/room/living_room/device/cam3/kind/motion`

Contract: `MediaEvent` (minimal payload)

```json
{
  "meta": { "...": "..." },
  "payload": {
    "event": "motion_detected",
    "media_kind": "video",
    "confidence": 0.84
  }
}
```

### 4.2 Media registry state (retained)

Clients cache where to connect for each device (supports multiple gateways).

State topic (retained):

- `/sc/media/state/device/{device_id}`

Contract: `MediaRegistryState`

```json
{
  "payload": {
    "gateway_base": "https://edge-gw-2.local",
    "offer_path_template": "/webrtc/offer/{device_id}",
    "streams": ["cam3-main"],
    "updated_at": "2026-01-08T13:40:00.000Z"
  }
}
```

### 4.3 Why this is secure

MQTT never grants access.
Streaming starts only when an authorized viewer requests a WebRTC session from the gateway.

---

## 5) Brainstem topics

### 5.1 Relay bundles (events)

- `/bs/relay/event/{scope_level}/{scope}/channel/{channel}`

Example:

- `/bs/relay/event/room/living_room/channel/somatic`

### 5.2 Patterns (events)

- `/bs/pattern/event/{scope_level}/{scope}/{pattern_type}/trigger`

### 5.3 Global broadcast/state

- `/bs/global/state/{scope_level}/{scope}/alert` (retained state)
- `/bs/global/event/{scope_level}/{scope}/alert` (one-shot)

---

## 6) Reliable + Reflect topics

### Commands (Reliable)

- `/C/cmd/event/{scope_level}/{scope}/channel/{channel}/action/{action_id}`

### Outcomes/Errors

- `/E/outcome/event/{scope_level}/{scope}/action/{action_id}`
- `/E/error/event/{scope_level}/{scope}/action/{action_id}`

### Reject / quarantine (Reflect)

- `/X/reflect/event/{scope_level}/{scope}/lane/reject`

---

## 7) Universal wire envelope (nested meta)

All messages use:

```json
{ "meta": { ... }, "payload": { ... } }
```

### 7.1 Keep both `contract` and `message_type`

You wanted redundancy. We keep both.

**Strict v1 rule (avoid drift):**

- `meta.contract` MUST equal `meta.message_type` (exact match)
- if not → reject + emit `RejectEvent`

This prevents confusion if a producer accidentally sets them differently.

### 7.2 Identity: services vs hardware

- `meta.source` is always present (service or device): `"brainstem-1"` or `"device:m1"`
- `hardware_id` is optional and only included when relevant:
  - `meta.device: { device_id, hardware_id, ... }`

Aggregates should not pretend to have one hardware_id; use `payload.sources`.

---

## 8) Time + replay protection

### produced_at (for humans)

- ISO UTC timestamp in `meta.produced_at`

### HLC (for distributed causality; optional but recommended)

Reserve:

```json
"hlc": { "wall_ms": 1736..., "logical": 12, "node": "brainstem-1" }
```

### TTL/deadline semantics

- `ttl_ms` or `expires_at` for events (drop stale)
- `deadline_ms` for commands (hard cutoff)
- `priority` for scheduling
- optional `qos_hint`

Replay resistance:

- drop expired messages
- dedupe recent `message_id` per `source`

---

## 9) Secure WebRTC gateway session contracts (design only)

We assume an **edge gateway** to simplify NAT/authz/audit.

### Style A (start here): authorize at connect time

Viewer calls gateway; gateway authenticates+authorizes; returns session.

**Request contract:** `StreamSessionRequest`  
**Response contract:** `StreamSessionResponse`

(We kept this in v1 so you can implement without committing to tokens.)

### Style B (later): capability token (strongest)

Add a short-lived token flow to mitigate replay and constrain access windows.

---

## 10) Project name (not decided yet)

Candidates we discussed:

- TractStack
- NeuroWeave
- Cortical Fabric

If you want Swedish-flavored naming, we can also brainstorm names that sound good in Swedish/English.

---

## 11) Next steps (still design-only)

1. Turn these contracts into **JSON Schemas**:
   - `AfferentSignal`, `RelayBundle`, `Command`, `Outcome`, `RejectEvent`
   - `MediaEvent`, `MediaRegistryState`
   - `StreamSessionRequest`, `StreamSessionResponse`
2. Decide gateway response style:
   - returns SDP directly vs returns offer endpoint
3. Pick a final project name + tagline.

---

## Quick glossary (short)

- **SpinalCord** = raw I/O + reflex loops (device-proximal)
- **Brainstem** = aggregation + relay bundles + fast patterns (scope-proximal)
- **MediaEvent** = spike only (no URL), stream is pulled via gateway
- **Registry state** = retained mapping from device → gateway base/paths
