# Communication Spec v2 (Brain-Like Lanes + Media Streams + Reflection)

This is a **transport-agnostic** communication contract for a brain-inspired system.
It defines:
- **Lanes** (like tracts),
- **Direction rules**,
- A common **envelope** for control/event traffic, and
- A **thalamus/TRN-style gating protocol**.

It also adds:
- **Separate audio/video streaming lanes** (data plane),
- A **reflection lane** for audit/observability/efference-copy,
- Guidance on using **different protocols by lane** without fragmenting the system.

---

## 1) Lanes and directions (the whole system)

### Lane A — DRIVER (payload / content)
- **Direction:** **SpinalCord → Brainstem → Thalamus(nucleus) → Cortex**
- **Carries:** sensor summaries, detected features, events (not policies).
- **Rule:** Drivers never change routing/gating; they are **subject to** it.

### Lane B — MODULATOR (feedback / attention / routing control)
- **Direction:** **Cortex → Thalamus/TRN** (+ optional Cortex↔Cortex)
- **Carries:** boost/suppress, precision/gain, “focus on X”, “ignore Y”.
- **Rule:** Modulators can change gating state for a nucleus/scope **for a time window**.

### Lane G — GATE (TRN inhibition state)
- **Direction:** control-plane only (distributed state)
- **Carries:** `GateState(scope, nucleus) = inhibition 0..1 (+ mode WTA/multi, expiry)`
- **Rule:** Every relay decision checks **GATE** before delivering Lane A to cortex.

### Lane C — COMMAND (motor / actuation)
- **Direction:** **Cortex → Brainstem → SpinalCord** (actuators)
- **Carries:** actions/commands.
- **Rule:** Send a **command copy** to Lane E for monitoring/learning.

### Lane D — GLOBAL MODES (neuromodulators / operating state)
- **Direction:** **Hypothalamus/Brainstem → ALL modules**
- **Carries:** high-alert, quiet-hours, energy-saving, circadian bias, stress index.
- **Rule:** D-lane shifts **baseline thresholds and defaults** (not per-message routing).

### Lane E — ERROR / OUTCOME / LEARNING
- **Direction:** mostly upward (**SpinalCord/Cerebellum/Limbic → Cortex/BG/Thalamus/Hypothalamus**)
- **Carries:** outcomes, prediction errors, corrections, salience tags.
- **Rule:** E-lane does not execute actions; it **biases** selection, gating, and future policy.

### Lane X — REFLECTION (efference copy / audit / observability)
- **Direction:** “sideways” copies from other lanes → observation/learning/audit sinks
- **Carries:** copies of selected messages (especially Commands, Gate changes, high-salience Drivers, Outcomes)
- **Rule:** X-lane must be **non-blocking**: reflection failures must not prevent primary flow.

> Brain analogy: “efference copy” + “re-entrant monitoring.” In software this is your **trace/audit lane** plus
> optional replay into learning components.

---

## 2) Media plane (separate from control lanes)

High-bandwidth audio/video streams should NOT share the same bus as event/control messages.

### Lane V — VIDEO STREAM (data plane)
- **Direction:** camera(s) → perception/cortex consumers
- **Carries:** raw/compressed video frames/streams
- **Rule:** established via a **session** negotiated on control lanes (A/B/D), not by blasting frames on the bus.

### Lane U — AUDIO STREAM (data plane)
- **Direction:** mic(s) → perception/cortex consumers
- **Carries:** raw/compressed audio streams
- **Rule:** same: negotiate sessions on control lanes; stream on media plane.

---

## 3) Extendability (more devices, more sensors)

To extend cleanly as devices grow:
- **Everything is scoped:** `{scope_level}/{scope}` (room/device/house/session).
- **Everything is channelized:** assign a nucleus lane where appropriate (LGN/MGN/etc.).
- **Discovery/registry:** devices publish capabilities on a well-known topic (e.g., `/D/capabilities/...`).
- **Schema versioning:** envelopes + payload schemas include a version tag and support additive evolution.

---

## 4) Protocol strategy (your “different protocols” idea, made coherent)

### Recommended: split by *plane*, not by *priority*
1) **Control + event plane** (A/B/G/C/D/E/X lanes):
   - Use ONE consistent messaging fabric with QoS tiers:
     - examples: MQTT (QoS 0/1/2), NATS (Core + JetStream), Kafka (if heavy persistence needed).
   - Encode priority/criticality in the **envelope**, not by picking a totally different protocol each time.

2) **Media plane** (V/U):
   - Use media-native protocols optimized for real-time:
     - **WebRTC** is great for low-latency interactive A/V, NAT traversal, adaptive bitrate.
     - Alternatives: RTSP/RTP, SRT, HLS/DASH (higher latency).

### Where XMPP fits (and where it doesn’t)
- XMPP is solid for **presence, chat-like messages, federated identity**, but it’s rarely the best choice for
high-rate IoT control/event traffic today.
- If you specifically need “chat-style federation” across domains, XMPP can be an additional integration edge.
- For in-home device/event messaging, MQTT/NATS-style pub-sub is typically simpler and lighter.

**Bottom line:**  
- **Use WebRTC for A/V streams.**  
- **Use a pub-sub fabric for lanes A/B/G/C/D/E/X** with reliability/QoS per lane/priority.

---

## 5) Topic taxonomy (transport-agnostic naming)

Control/event lanes (bus):
- `/A/driver/{scope_level}/{scope}/nucleus/{nucleus}`
- `/B/mod/{scope_level}/{scope}/nucleus/{nucleus}`
- `/G/gate/{scope_level}/{scope}/nucleus/{nucleus}`
- `/C/cmd/{scope_level}/{scope}/channel/{channel}/action/{action_id}`
- `/D/mode/{scope_level}/{scope}` and `/D/mode/global`
- `/E/outcome/{scope_level}/{scope}/action/{action_id}`
- `/X/reflect/{scope_level}/{scope}/lane/{lane}/...`

Media lanes (session-based):
- `/V/video/session/{session_id}`
- `/U/audio/session/{session_id}`

---

## 6) Minimal checklist (adopt now)
- Add Lane X (reflection) and decide what gets mirrored (at minimum: commands + outcomes + gate changes).
- Keep A/V off the control bus; negotiate WebRTC sessions via control messages.
- Choose one control/event pub-sub fabric and define QoS per lane.
