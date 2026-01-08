# Mosquitto Communication Design (Brain‑Like Lanes, Fault Isolation, and QoS)

This document adapts the **brain‑like lane model** (A/B/G/C/D/E/X plus U/V media) to a practical **Mosquitto** deployment, with the explicit goal:

> **If a component breaks, it should not overflow or destabilize the rest of the system.**

It does this by **isolation + quotas + ACLs + lane‑specific QoS/expiry rules**, not by mixing lots of protocols.

---

## 1) Recommended topology (Mosquitto)

### Best practice: 3 Mosquitto instances (or containers/VMs), each with its own listener/port

**Broker 1 — Control Plane**
- **Lanes:** `B` (Modulator), `G` (Gate), `D` (Global Modes)
- **Why:** must remain responsive even when sensors (Lane A) are noisy
- **Port example:** `18831`

**Broker 2 — Driver Plane**
- **Lane:** `A` (Driver)
- **Why:** high‑rate traffic is allowed to be lossy; isolate it so it can’t drown control
- **Port example:** `18832`

**Broker 3 — Reliable Plane**
- **Lanes:** `C` (Command), `E` (Outcome/Error/Learning), `X` (Reflection)
- **Why:** commands/outcomes need stronger delivery semantics without blocking control
- **Port example:** `18833`

> If you only want **two** brokers: keep **Control** separate, and combine Driver + Reliable on the other.

---

## 2) Lane rules mapped to MQTT (QoS, retain, expiry, drop policy)

### Lane A — DRIVER (payload / content)
- **QoS:** 0 (default)
- **Retain:** No
- **Expiry:** short (if your publisher supports MQTT v5 message expiry)
- **Drop policy:** OK to drop/downsample/coalesce under load
- **Reason:** high‑rate sensory inflow should not block the system

### Lane B — MODULATOR (feedback / attention)
- **QoS:** 0 or 1
- **Retain:** No
- **Expiry:** **very short** (stale modulators are worse than missing ones)
- **Reason:** attention/gating should reflect “now”

### Lane G — GATE (TRN inhibition state)
- **QoS:** 1
- **Retain:** **Yes** (latest gate state matters)
- **Expiry:** gate window duration (optional)
- **Reason:** consumers need “current inhibition” immediately

### Lane D — GLOBAL MODES (neuromodulators / operating state)
- **QoS:** 1
- **Retain:** **Yes**
- **Expiry:** optional/long
- **Reason:** “latest mode” should be available to late joiners

### Lane C — COMMAND (actuation)
- **QoS:** 1 (or 2 if you truly need it)
- **Retain:** usually No (unless you implement “desired state topics” separately)
- **Must include:** `action_id` / idempotency key in payload
- **Reason:** at‑least‑once delivery + idempotency is practical and reliable

### Lane E — OUTCOME / ERROR / LEARNING
- **QoS:** 1
- **Retain:** No
- **Batching:** allowed
- **Reason:** you want learning/audit signals to arrive, but they can lag slightly

### Lane X — REFLECTION (efference copy / audit)
- **QoS:** 0
- **Retain:** No
- **Must be non‑blocking:** reflection failures must not slow core lanes
- **Reason:** observability must never be a hard dependency

### Lanes U/V — AUDIO/VIDEO streaming (media plane)
- **Not MQTT.**
- Use **WebRTC** (recommended) or RTSP/RTP/SRT depending on your latency needs.
- Use MQTT lanes (A/B/D) only to **negotiate sessions** and publish stream metadata.

---

## 3) Topic namespace (lane + scope + nucleus)

A consistent, scoped topic scheme prevents hot topics and makes scaling predictable.

### Control/event lanes (on MQTT)
- Drivers (A):  
  `/A/driver/{scope_level}/{scope}/nucleus/{nucleus}/device/{device_id}`
- Modulators (B):  
  `/B/mod/{scope_level}/{scope}/nucleus/{nucleus}`
- Gate updates (G):  
  `/G/gate/{scope_level}/{scope}/nucleus/{nucleus}`
- Commands (C):  
  `/C/cmd/{scope_level}/{scope}/channel/{channel}/action/{action_id}`
- Global modes (D):  
  `/D/mode/{scope_level}/{scope}` and `/D/mode/global`
- Outcomes/errors (E):  
  `/E/outcome/{scope_level}/{scope}/action/{action_id}`  
  `/E/error/{scope_level}/{scope}/action/{action_id}`
- Reflection (X):  
  `/X/reflect/{scope_level}/{scope}/lane/{lane}/...`

### Media lanes (session-based, not MQTT)
- Video (V): `webrtc://...` (session_id in MQTT control message)
- Audio (U): `webrtc://...`

---

## 4) Mosquitto: hardening against overflow (what to configure)

You want both **publisher containment** and **broker containment**.

### 4.1 Broker containment
Configure conservative limits so one broken client cannot exhaust memory.

- **Max packet size** (to prevent huge payloads)
- **Inflight/queued message limits**
- **Client connection limits**
- **Persistence for reliable plane (optional)**

> Note: exact setting names vary by Mosquitto version. Use `mosquitto.conf` to enforce these and validate with your version’s docs.

### 4.2 Publisher containment (more important than broker limits)
Every publisher should implement:
- **rate limiting**
- **coalescing** (keep only last value for certain sensors)
- **sampling** (publish every N ms)
- **backoff** when publish fails

This is the software equivalent of “inhibition” and “gain control.”

---

## 5) ACLs: enforce lane boundaries (critical)

ACLs are your **anatomy**. They prevent “wrong lane” publishing and limit blast radius.

### Pattern
- Sensors can publish only to `/A/...` for their device_id
- Cortex can publish only to `/B/...` and subscribe to `/A/...`
- TRN-like gate service can publish only to `/G/...`
- Actuator services can subscribe only to `/C/...` and publish `/E/...`
- Reflection collector subscribes to many but publishes only to `/X/...`

### Example ACL sketch (illustrative)
Create separate users per component class (camera, cortex, gate, actuator, learner).

```
# camera_1
topic write /A/driver/+/+/nucleus/+/device/camera_1

# cortex
topic read  /A/driver/+/+/nucleus/+/device/+
topic write /B/mod/+/+/nucleus/+
topic read  /G/gate/+/+/nucleus/+
topic read  /D/mode/#
topic write /C/cmd/+/+/channel/+/action/+

# gate_service (TRN analog)
topic read  /B/mod/+/+/nucleus/+
topic write /G/gate/+/+/nucleus/+

# actuator
topic read  /C/cmd/+/+/channel/+/action/+
topic write /E/outcome/+/+/action/+
topic write /E/error/+/+/action/+

# reflector
topic read  /A/#
topic read  /B/#
topic read  /C/#
topic read  /D/#
topic read  /E/#
topic read  /G/#
topic write /X/reflect/#
```

---

## 6) Bridging between brokers (optional)

If you use **3 brokers**, you may want controlled cross‑lane visibility.

### Recommended bridge directions
- Driver Broker → Control Broker (only **summaries**, not raw floods)
- Reliable Broker → Control Broker (outcomes/errors that may affect gating)
- Control Broker → Driver Broker (rare; usually not needed)

Keep bridges **narrow and explicit** to prevent reintroducing the “one big broker” problem.

---

## 7) Fault handling patterns (brain-like behaviors)

### 7.1 Sensor storm (Lane A overload)
- Contain on Driver Broker
- Drop/downsample in publishers
- Gate (Lane G) can increase inhibition for noisy nuclei/scope
- Control Broker remains responsive

### 7.2 Broken modulator (Lane B spam)
- Contain on Control Broker with rate limits per client + ACLs
- Gate service can ignore modulators without correct auth/user

### 7.3 Command safety
- Commands must be idempotent (`action_id`)
- Actuators publish outcomes to Lane E
- Reflection lane records command + outcome for debugging

---

## 8) Minimal adoption checklist

1) Stand up **Control Broker** separate from **Driver Broker** (minimum isolation).
2) Enforce **ACLs by lane** and per-component identities.
3) Define per-lane **QoS + retain** rules (especially G and D retained).
4) Implement publisher-side **rate limiting + coalescing** for Lane A.
5) Add Lane X reflection as best-effort (never blocks).

---

## 9) Quick “why this matches the brain”

- **Lane A** = driver content (sensory payload).
- **Lane B** = cortical feedback modulation (attention/gain).
- **Lane G** = TRN-like inhibition state (gating).
- **Lane D** = neuromodulators (global operating mode).
- **Lane C** = motor commands (execution path).
- **Lane E** = error/outcome for learning (cerebellum/limbic/BG bias).
- **Lane X** = efference copy / monitoring (observability & learning).
- **U/V** = separate media “wiring” (streams), negotiated by control signals.

---

### If you want next
Tell me your expected scale (roughly):
- number of devices,
- typical Lane A message rate per device,
- whether you need persistence for Lane E (learning logs),
and I’ll propose a concrete **2-broker vs 3-broker** topology and a “lane QoS table” tuned to your traffic.
