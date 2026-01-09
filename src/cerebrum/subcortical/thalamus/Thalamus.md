# Thalamus (`/th/*`) — Channel-Gated Relay Plane (v1)

This folder defines how **Thalamus** works in our stack: **routing + gating** for parallel loops, using **Channel** as the stable partition key.

If you want to understand “how Thalamus works” here, read this file and nothing else.

---

## 1) What Thalamus does (software responsibilities)

Thalamus is a **policy-driven relay plane** that:

1. **Ingests driver streams** (typically Brainstem relay bundles).
2. **Partitions traffic by Channel** (the “parallel loop” key).
3. **Consults retained GateState** (TRN-like inhibition) for that `(scope_level, scope, channel)`.
4. **Relays / attenuates / drops** driver messages based on the current gate.
5. Optionally publishes **route audit** events for observability/learning.

Thalamus does **not** “decide the meaning.” It governs **what gets through**.

---

## 2) Core concept: Channels = software parallel loops

We model brain-style parallelism explicitly using **Channel**.

**Channel exists to mirror basal ganglia–thalamo–cortical “parallel loops”** (motor, cognitive, limbic, oculomotor, plus sensory relays). Each channel can run concurrently; there is no global clock.

### Channel enum (v1)

Channels include sensory, loop-like, and diffuse/association lanes:

- Sensory-style: `visual`, `audio`, `somatic`, `visceral` (optional)
- BG-loop style: `motor`, `oculomotor`, `cognitive`, `limbic`
- Association/diffuse: `association`, `attention`, `diffuse`
- Special: `media` (**events only**, never streaming)

### Canonical topic selector segment

Topics carry channel explicitly via:

- `channel_selector(channel) -> "channel/<channel_name>"`

So the on-wire topics include a literal `channel/...` segment.

---

## 3) TRN in software: “protocol/state”, not necessarily a separate service

We treat TRN as:

- **GateState retained state** (the authoritative “inhibitory shell”), and
- a **Gatekeeper role** that is the only authority allowed to publish GateState.

Deployment is flexible:

- Gatekeeper + Relay can run in one process, or separate services.
- The separation is by **role**, not by mandatory deployable.

**Invariant:** the Relay role reads GateState; it does not “self-authorize” gates.

---

## 4) Topic map (channel-based)

These are _wire routing topics_ (string builders). They define “where messages go.”

### A) Modulators (event)

Control signals that influence gates.

- **Topic:** `/th/mod/event/{scope_level}/{scope}/channel/{channel}`
- **Helper:** `th_modulator_event(scope_level, scope, channel)`

Example:

- `/th/mod/event/room/living_room/channel/attention`

### B) GateState (retained state)

Authoritative gating state (TRN-like inhibition).

- **Topic:** `/th/gate/state/{scope_level}/{scope}/channel/{channel}` (**retained**)
- **Helper:** `th_gate_state(scope_level, scope, channel)`

Example:

- `/th/gate/state/room/living_room/channel/audio`

**Keying rule:** GateState is typically keyed by `(scope_level, scope, channel)`.

### C) Gated relay output (event)

What passed the gate (consumers should subscribe here by default).

- **Topic:** `/th/relay/event/{scope_level}/{scope}/channel/{channel}`
- **Helper:** `th_relay_event(scope_level, scope, channel)`

Example:

- `/th/relay/event/house/house_1/channel/visual`

### D) Optional route/audit stream (event)

Debugging + learning: what got through and why.

- **Topic:** `/th/route/event/{scope_level}/{scope}/channel/{channel}`
- **Helper:** `th_route_audit_event(scope_level, scope, channel)`

---

## 5) Driver inputs (where Thalamus reads “content” from)

Preferred upstream source is Brainstem (already aggregated/summarized):

- **Topic:** `/bs/relay/event/{scope_level}/{scope}/channel/{channel}`
- **Helper:** `bs_relay_event(scope_level, scope, channel)`

This matches the checkpoint decision that Brainstem should emit low-rate, upward-ready relay bundles.

---

## 6) Media is special (Thalamus does not handle streams)

Media streaming is never routed through `/th/*`. MQTT only carries **link-free “something happened” events** under `/sc/media/...`.

- **Topic:** `/sc/media/event/{scope_level}/{scope}/device/{device_id}/kind/{kind}`
- **Helper:** `sc_media_event(scope_level, scope, device_id, kind)`

The `Channel.MEDIA` value exists only for **classification and event handling**, not for transporting streams.

---

## 7) Runtime behavior (how the loop runs)

Thalamus runs continuously and asynchronously:

1. A driver message arrives on `/bs/relay/event/.../channel/{c}`.
2. Thalamus determines its Channel `c` (already explicit in topic).
3. Thalamus reads GateState from cached retained state:

   - `/th/gate/state/.../channel/{c}`.

4. Thalamus applies gate policy:

   - **pass**, **attenuate/downsample**, **aggregate**, or **drop**.

5. If allowed:

   - publish to `/th/relay/event/.../channel/{c}`.

6. Optionally:

   - publish a route audit event to `/th/route/event/.../channel/{c}`.

Modulators arrive independently on `/th/mod/event/.../channel/{c}` and are consumed by the Gatekeeper role, which updates retained GateState.

**Important:** loops are parallel by design—each channel can be processed independently without waiting for others.

---

## 8) Contracts (what messages mean)

Thalamus topics route typed messages defined elsewhere (wire envelope remains `{meta,payload}` at the system level).

Thalamus-specific message types include (conceptually):

- `GateState`
- `RouteDecision`
- modulator events (often “ModulatorSignal”-like)

Your shared MessageType list includes GateState and RouteDecision as first-class thalamus message types.

---

## 9) Governance + safety invariants

### Authority

- Only the **Gatekeeper (TRN role)** may publish:

  - `/th/gate/state/**`

### Separation of concerns

- **Drivers carry content**; they never change gates.
- **Modulators carry control**; they can influence GateState updates.

### Expiry (recommended)

To avoid “stuck inhibition,” GateState should support expiry (e.g., `expires_at_ms`).
Your contracts include an expiry-capable GateState variant.

### Rejects / quarantine

When messages violate type expectations or invariants, they should be rejected into the Reflect lane using the shared reject topic helper.

---

## 10) Topic hygiene (important note)

`thalamus_topics_channels_async.py` is intentionally “pure string builders” and does **not** sanitize `scope`, `device_id`, etc.

In other parts of the system, topic path sanitization is enforced to prevent path traversal and accidental fanout.

**Rule:** ensure `scope` and other path components are sanitized/validated before constructing Thalamus topics (or update the helpers to sanitize in the same way as the shared topic builders).

---

## Quick reference (examples)

- Modulator event:

  - `/th/mod/event/room/living_room/channel/attention`

- Retained gate state:

  - `/th/gate/state/room/living_room/channel/audio`

- Gated relay output:

  - `/th/relay/event/room/living_room/channel/audio`

- Route audit:

  - `/th/route/event/room/living_room/channel/audio`

- Driver input from Brainstem:

  - `/bs/relay/event/room/living_room/channel/somatic`

- Media event (not via thalamus):

  - `/sc/media/event/room/living_room/device/cam3/kind/motion`
