# Thalamus (`/th/*`) — Routing + Gating Plane (v1)

This folder defines how the **Thalamus region** works in our brain-inspired stack: what it does, what it consumes/publishes, and the runtime rules that keep it safe and brain-faithful.

If you want to understand “how Thalamus works” in this system, this is the only document you should need.

---

## 1) What Thalamus is (in our system)

**Thalamus is a policy-driven relay plane.**

It sits between **driver streams** (main content signals) and **cortex-like consumers**, and forwards only what passes the current **GateState** (TRN-like inhibition).

Thalamus does **not** invent meaning. It applies **attention/gating** to decide:

- relay,
- throttle/downsample,
- aggregate,
- or drop.

---

## 2) The core idea (brain → software mapping)

### Drivers vs Modulators (non-negotiable boundary)

- **Drivers** carry _content_ (sensor signals, relay bundles, detected events).
- **Modulators** carry _control_ (boost/suppress/focus/policy pressure).

**Drivers can never change gates.**
Modulators can influence gates, but are **non-authoritative proposals**.

### TRN in software

**TRN is a protocol/state, not necessarily a separate deployable.**

We implement TRN as **retained GateState** plus a **Gatekeeper role** that is the only authority allowed to publish that state.

---

## 3) Roles (not services)

Thalamus is defined as **two roles** that may run as:

- one process (colocated), or
- two services (separate deployables).

### A) Relay role (“Thalamus Relay”)

Responsibilities:

1. Classify an incoming driver message to a **selector**
2. Read **GateState** for that selector (local cache fed from retained state topics)
3. Decide pass/attenuate/drop/aggregate
4. Publish allowed content to relay outputs
5. Optionally emit a RouteDecision audit event

**The relay role never writes gate state.**

### B) Gatekeeper role (“TRN role”)

Responsibilities:

1. Ingest **ModulatorSignal** events
2. Compute/update authoritative **GateState**
3. Publish GateState to retained state topics

**Only the gatekeeper role is allowed to publish GateState.**

---

## 4) Selector (what gates apply to)

Every gating decision is keyed by a **selector**:

`selector = (scope_level, scope, target_kind, target_id)`

Where:

- `scope_level`: `device | room | house | user_session`
- `scope`: e.g. `living_room`, `house_1`, `user:abc`
- `target_kind`: `channel | nucleus | topic_prefix`
- `target_id`: e.g. `audio`, `visual`, `motion`, `LGN`, `/sc/aff/event`

This is the main “make it crisp” rule that prevents later debates.

---

## 5) Topic plan (`/th/*`)

We use the same event/state semantics as the rest of the system:

- `/.../event/...` = not retained
- `/.../state/...` = retained

### Inputs to Thalamus

#### Driver inputs (content)

Typically from Brainstem summaries/bundles (preferred):

- `/bs/relay/event/{scope_level}/{scope}/channel/{channel}`

Optionally (advanced / careful) some raw spinal streams:

- `/sc/aff/event/...`
  …but default posture is: **keep raw out of Thalamus** unless there is a clear reason.

#### Modulator inputs (control)

From Cortex/Limbic/Hypothalamus policy/attention intent:

- `/th/mod/event/{scope_level}/{scope}/target/{target_kind}/{target_id}`

> Note: Hypothalamus/global modes belong here (modulators), not in the driver bucket.

---

### TRN gate state (authoritative, retained)

- `/th/gate/state/{scope_level}/{scope}/target/{target_kind}/{target_id}` (**retained**)

Published only by the **Gatekeeper (TRN role)**.

---

### Outputs

#### Gated relay output (what passed the gate)

- `/th/relay/event/{scope_level}/{scope}/channel/{channel}`

This is the simplest operational choice:

- consumers subscribe to a single “passed gate” stream,
- you can later add extra forwarding if needed.

#### Optional audit/learning stream

- `/th/route/event/{scope_level}/{scope}/channel/{channel}`

#### Rejects / quarantine (system lane)

- `/X/reflect/event/{scope_level}/{scope}/lane/reject`

Used for schema violations, forbidden publish attempts, contract/type mismatch, etc.

---

## 6) Contracts (Thalamus-specific)

All contracts use the universal wire envelope:

```text
{ "meta": { ... }, "payload": { ... } }
```

And the rule: `meta.contract == meta.message_type`.

### A) `ModulatorSignal` (event)

Purpose: “Propose attention knobs for this target for a short window.”

Typical payload fields:

- `target_kind` (`channel | nucleus | topic_prefix`)
- `target_id`
- `intent` (`boost | suppress | set_inhibition`)
- `strength` or `inhibition` (0..1)
- `expires_at` or `ttl_ms`
- optional `reason_codes[]`, `reason`

### B) `GateState` (state, retained)

Purpose: “Authoritative inhibition state and selection mode for this selector.”

Typical payload fields:

- `inhibition` (0..1)
- `mode` (`multi | winner_take_all | passthrough`)
- `expires_at` (or TTL semantics)
- `set_by` (identity of gatekeeper role instance)
- optional `policy_id` (debugging: which policy produced this)

### C) `RouteDecision` (event, optional)

Purpose: “What happened to this driver message and why.”

Typical payload fields:

- `input_ref`: `{ message_id, contract, source_topic }`
- `allowed` (bool)
- `decision` (`pass | attenuate | aggregate | drop`)
- `effective_inhibition`
- `routed_to[]`
- optional `rationale` / `reason_codes[]`

---

## 7) Runtime behavior (the loop)

For each driver message:

1. **Ingest driver** (e.g., from `/bs/relay/event/...`)
2. **Compute selector**
3. **Fetch GateState** from local cache (fed by retained `/th/gate/state/...`)
4. **Decide**:

   - inhibition high → drop or downsample/aggregate
   - inhibition low → relay
   - WTA → only the top channel(s) pass for the window

5. **Publish**:

   - allowed → `/th/relay/event/...`
   - optionally → `/th/route/event/...` (audit)

6. **Modulators arrive asynchronously**:

   - `/th/mod/event/...` → Gatekeeper updates retained `/th/gate/state/...`

7. Next driver uses the updated gate snapshot.

### Expiry safety (important)

If a GateState expires:

- Thalamus falls back to a **safe default policy** (e.g., pass critical state, aggregate high-rate events).
  No “stuck suppression”.

---

## 8) Security + governance rules (must-haves)

### Authority / ACL expectations

- Only the **Gatekeeper role** can publish:

  - `/th/gate/state/**`

- Relay role and all drivers **must be denied** publish rights to gate state topics.

### Wire semantics used for safety

- Events: require `ttl_ms` or `expires_at`
- Commands: require `deadline_ms` + `action_id` (idempotency)
- Optional HLC: supports ordering and replay resistance when needed

### Media posture reminder

Thalamus does not bypass media security:

- MQTT “spikes” never grant access
- streaming remains pull-based via gateway with authN/authZ

---

## 9) Deployment guidance (avoid bottlenecks)

- **No synchronous calls in the relay path** (gate state is cached).
- **Shard by selector** (scope/channel) across multiple instances if needed.
- **Backpressure policy**:

  - drop/attenuate low priority drivers first
  - keep modulators/control traffic highest priority

---

## 10) Invariants (the crisp rules)

1. **Drivers carry content; modulators carry control.**
2. **Drivers never change gates.**
3. **Only Gatekeeper publishes GateState (retained).**
4. **Relay decisions always consult GateState.**
5. **Relay output `/th/relay/event/...` is the canonical “passed gate” stream.**
