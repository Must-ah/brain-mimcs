# TractStack (working name)
*A brain-inspired software architecture that organizes perception, reflexes, attention, and action into region-like services connected by tract-like communication lanes and typed wire contracts.*

> **Name status:** not finalized. Replace “TractStack” with your chosen project name when ready.

---

## What this project is
This repository explores a **brain-inspired system architecture** where “regions” (modules) communicate through **tract-like lanes**:
- **SpinalCord**: raw device I/O + reflex loops (device-proximal)
- **Brainstem**: aggregation + relay bundles + fast patterns/broadcasts (scope-proximal)
- (Later) **Thalamus/Cortex**: attention, routing, decisions, planning
- **Reliable**: commands/outcomes (durable-ish intent + feedback)
- **Reflect**: quarantine/audit for rejects and observability

The design goal is to run parts on **different machines** and in **different languages** by sharing only:
- **MQTT topic conventions** (routing)
- **Wire contracts** (meaning + validation + versioning)

---

## Core rules
### Topics vs Contracts
- **Topic = “where”** (routing/addressing)
- **Contract = “what”** (meaning/semantics)

### Raw doesn’t go up
- Spinal carries **raw** signals.
- Brainstem publishes **summaries** upward (e.g., `RelayBundle`).
- Higher layers should not ingest raw floods.

### Media is pull-based
- MQTT never carries streams.
- MQTT carries **media events** (“something happened”).
- Authorized clients **pull** media via **WebRTC** through a gateway.
- If nobody connects, **no stream runs**.

---

## Topic taxonomy (event vs state)
We encode lifecycle in the topic:
- `/.../event/...` → transient occurrences (**not retained**)
- `/.../state/...` → latest value (**retained**)

All topics include:
- `{scope_level}`: `device | room | house | user_session`
- `{scope}`: e.g. `living_room`, `house_1`

---

## Topic prefixes (the “planes”)
### SpinalCord (`/sc/*`)
**Afferent sensors (event)**
- `/sc/aff/event/{scope_level}/{scope}/sensor/{sensor_type}/device/{device_id}`

**Efferent device commands (event)**
- `/sc/eff/event/{scope_level}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}`

**Reflex (event)**
- `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/configure`
- `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/trigger`
- (optional) `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/fire/{action_id}`
- (optional) `/sc/reflex/event/{scope_level}/{scope}/rule/{reflex_id}/report/{action_id}`

### ✅ Media is its own path (`/sc/media/*`)
**Media event (link-free spike)**
- `/sc/media/event/{scope_level}/{scope}/device/{device_id}/kind/{kind}`  
Example: `/sc/media/event/room/living_room/device/cam3/kind/motion`

**Media registry (retained state)**
- `/sc/media/state/device/{device_id}`  
Clients cache gateway mapping (supports multiple gateways).

### Brainstem (`/bs/*`)
**Relay bundles (event)**
- `/bs/relay/event/{scope_level}/{scope}/channel/{channel}`

**Patterns (event)**
- `/bs/pattern/event/{scope_level}/{scope}/{pattern_type}/trigger`

**Global broadcasts**
- `/bs/global/state/{scope_level}/{scope}/alert` (retained)
- `/bs/global/event/{scope_level}/{scope}/alert` (one-shot)

### Reliable (`/C/*`, `/E/*`)
**Commands**
- `/C/cmd/event/{scope_level}/{scope}/channel/{channel}/action/{action_id}`

**Outcomes / Errors**
- `/E/outcome/event/{scope_level}/{scope}/action/{action_id}`
- `/E/error/event/{scope_level}/{scope}/action/{action_id}`

### Reflect (`/X/*`)
**Reject / quarantine**
- `/X/reflect/event/{scope_level}/{scope}/lane/reject`

---

## Wire contract envelope (multi-language)
All messages use a nested envelope:
```json
{ "meta": { ... }, "payload": { ... } }
```

### `meta` (universal header)
**Identity + version**
- `message_id`
- `schema_version` (e.g., `v1`)
- `contract`
- `message_type`

**Strict v1 drift rule**
- `meta.contract` MUST equal `meta.message_type` (exact match)  
If not → reject + emit a `RejectEvent` to `/X/reflect/.../lane/reject`.

**Origin**
- `origin_plane` (spinal/brainstem/reliable/reflect/...)
- `source` (service or device, e.g., `brainstem-1` or `device:m1`)
- optional `device: { device_id, hardware_id, ... }` (only when relevant)

**Scope**
- `scope_level`, `scope`

**Time**
- `produced_at` (ISO UTC, for humans)
- optional `hlc: { wall_ms, logical, node }` (distributed causality; use when needed)

**Delivery**
- `ttl_ms` or `expires_at` (events)
- `deadline_ms` (commands)
- `priority`
- optional `qos_hint`

**Encoding + future security hooks**
- `content_type` (`application/json` now; `application/cbor` later)
- `content_encoding` (`identity` now)
- optional `auth` placeholder (reserved; enforced at gateways/services later)

**Tracing (recommended)**
- `trace_id`, `span_id`, optional `parent_span_id`

### Compact vs Full (lane profiles)
One schema, different **minimum required subsets**:
- **Compact** (Spinal high-rate): minimal required `meta` fields populated
- **Full** (Control/Reliable/Reflect): tracing + delivery fields consistently populated

---

## Media design (secure by default)
### MediaEvent (MQTT)
Media events contain **no URL**:
- They only announce: **event + kind + confidence**.
- Listeners derive connection info from the registry.

### MediaRegistryState (MQTT retained)
`/sc/media/state/device/{device_id}` provides:
- `gateway_base`
- `offer_path_template` (e.g., `/webrtc/offer/{device_id}`)
- available `streams`

### WebRTC gateway (pull)
The gateway must enforce:
- **TLS**
- **Authentication**
- **Authorization per device + scope**
- **Short-lived sessions**
- **Audit logs**

MQTT events must never grant access by themselves.

---

## Gateway session contracts (design-only)
Two compatible styles:

### Style A (start here): authorize at connect time
- `StreamSessionRequest` → gateway authenticates+authorizes → `StreamSessionResponse`

### Style B (later): capability token (strongest)
- short-lived, single-use tokens to mitigate replay and constrain access windows

---

## Validation and rejects
Each plane enforces an **ingress allow-list** of contracts it accepts. Anything else:
1) drop
2) publish `RejectEvent` to `/X/reflect/.../lane/reject`

Replay resistance:
- drop expired messages (`ttl_ms`)
- dedupe recent `message_id` per `source`

---

## Current project status
### What’s implemented (prototype)
- Async “contract-only” skeletons for Spinal/Brainstem/etc.
- In-memory demo buses to test routing/reject behavior

### What’s next (recommended)
1) Write **JSON Schemas** for core contracts:
   - `AfferentSignal`, `RelayBundle`, `Command`, `Outcome`, `RejectEvent`
   - `MediaEvent`, `MediaRegistryState`
   - `StreamSessionRequest`, `StreamSessionResponse`
2) Finalize project name + tagline
3) Decide gateway response style (SDP vs offer endpoint)

---

## Where to look in this repo (typical structure)
- `src/shared/` — shared enums/envelope helpers (prototype)
- `src/spinal_cord/` — spinal contracts + topic helpers (prototype)
- `src/brainstem/` — brainstem contracts + topic helpers (prototype)
- `broker_boundary_bridge_policy.md` — bridge/broker boundary rules
- `mosquitto_brain_like_communication.md` — Mosquitto guidance

> Long-term, treat Python models as **reference implementations**. The source of truth should become JSON Schemas.

---

## Glossary (short)
- **Plane**: architectural level (Spinal/Brainstem/…)
- **Afferent**: inbound sensory signal
- **Efferent**: outbound motor/actuation signal
- **RelayBundle**: summarized channel output from Brainstem
- **Reflex**: fast local loop in SpinalCord
- **HLC**: Hybrid Logical Clock for distributed causality
