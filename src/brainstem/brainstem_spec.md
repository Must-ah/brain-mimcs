# Brainstem Spec (Relay + Pattern + Global Broadcast Plane)

**Role (brain analogy):** Fast relay/aggregation layer that transforms raw afferents into typed summaries, triggers fast patterned responses, and broadcasts global operating state.  
**Goal:** Prevent raw sensor floods from reaching higher layers; keep control plane stable.

---

## 1) Responsibilities

### Must do
- **Subscribe to Spinal afferents** for a scope and **transform** them into *typed relay bundles*.
- **Rate-limit/coalesce** noisy sources (protect upstream).
- **Trigger fast pattern responses** (startle/orient/stabilize equivalents) when urgent.
- **Publish global broadcasts** (alert/arousal equivalents) when appropriate.
- **Provide a stable interface upward** to Thalamus/Cortex: low-rate, typed, windowed summaries.

### Must not do
- No thalamic gating/TRN state ownership (that’s GATE plane).
- No long-horizon planning (cortex).
- No direct device actuation outside the motor path (commands belong to Reliable→Spinal).

---

## 2) Plane Type Safety (reject wrong types)

### Allowed inbound message types
1) **AfferentSignal** (from Spinal broker; used only for transformation)
2) **PatternTrigger** (from authorized sources; urgent reflex-like triggers)
3) **GlobalModeUpdate** (from Hypothalamus/authorized core modules)
4) **RelayBundle** (internal brainstem-to-brainstem coordination, optional)

### Rejected inbound types (examples)
- Raw **EfferentCommand** targeting devices (brainstem shouldn’t bypass motor path)
- **GateState** (owned by thalamus/TRN plane)
- Arbitrary high-rate raw streams forwarded “as-is” upward

### Rejection behavior
- Drop and emit **RejectEvent** to Reflect plane with reason + metadata.

---

## 3) Topics (MQTT prefixes owned by Core/Control broker)

### Inbound (read)
- From Spinal broker:
  - `/sc/aff/{scope_level}/{scope}/...` (read-only by Brainstem identities)
- Optional triggers:
  - `/bs/pattern/{scope_level}/{scope}/{pattern_type}/trigger`
- Optional modes:
  - `/D/mode/{scope_level}/{scope}` and `/D/mode/global`

### Outbound (write)
#### Relay bundles (upward-ready)
- `/bs/relay/{scope_level}/{scope}/channel/{channel}`

Recommended `channel` values (extendable):
- `somatic` (environment & body-like sensors)
- `auditory` (audio-derived features)
- `visual_orient` (vision-derived orienting features; not raw frames)
- `visceral` (homeostasis-like internal state)

#### Pattern responses (to motor path / or to core decisioning)
- `/bs/pattern/{scope_level}/{scope}/{pattern_type}/request`
- `/bs/pattern/{scope_level}/{scope}/{pattern_type}/report`

#### Global broadcasts (fast operating state)
- `/bs/global/{scope_level}/{scope}/alert`
- `/bs/global/{scope_level}/{scope}/arousal`

> **Rule:** Brainstem topics are **scope-addressed** and **typed** (lower volume than Spinal).

---

## 4) Contract templates

### 4.1 RelayBundle
**Required**
- `message_type: "RelayBundle"`
- `schema_version`
- `scope_level`, `scope`
- `channel`
- `timestamp_ms`
- `window_ms` (integration window)
- `payload.summary_features` (typed features, counts, max/min, etc.)

**Optional**
- `correlation_id` (for binding across channels)
- `salience`, `confidence`
- `sources` (device ids included in the bundle)

**Invariant**
- RelayBundle must not contain raw high-bandwidth payloads (no frames, no long waveforms).

### 4.2 PatternTrigger / PatternResponse
**PatternTrigger required**
- `message_type: "PatternTrigger"`
- `pattern_type` (e.g., `startle`, `orient`, `stabilize`)
- `timestamp_ms`, `scope_level`, `scope`
- `trigger` (what caused it), `urgency`, `deadline_ms`

**PatternResponse required**
- `message_type: "PatternResponse"`
- `pattern_type`
- `request_id` / `correlation_id`
- `recommendation` (what to do next) or `status`

### 4.3 GlobalBroadcast
**Required**
- `message_type: "GlobalBroadcast"`
- `schema_version`
- `scope_level`, `scope`
- `timestamp_ms`
- `state` (e.g., `high_alert`, `quiet_hours`, `energy_save`)
- `half_life_ms` or `expires_at_ms`

### 4.4 RejectEvent
Same as Spinal spec.

---

## 5) Transform rules (Spinal → Brainstem → Upward)

### Afferent → RelayBundle (required transformation)
- Brainstem MUST transform raw afferents into typed summaries:
  - coalesce repeated values
  - downsample high-rate sources
  - compute simple features (counts, max, moving average)
- Brainstem MUST NOT forward raw afferents upward as RelayBundles.

### “Raw never goes up” invariant
- `/sc/aff/#` stays on Spinal broker.
- Upward-facing interfaces are `/bs/relay/#` only.

---

## 6) QoS + retain policy

- **RelayBundle:** QoS 0 or 1 (prefer 0 for frequent; 1 for critical), short expiry.
- **Global broadcasts:** QoS 1 + retained (latest state), moderate expiry.
- **Pattern triggers:** QoS 1 (time-sensitive), short expiry.
- **RejectEvent:** QoS 0, best-effort.

---

## 7) Broker boundary rules (default)

- Brainstem reads from Spinal broker; publishes to Core/Control broker.
- Device actuation still goes **Reliable → Spinal**, not Brainstem → Spinal.
- Brainstem influences behavior via:
  - relay bundles (upward)
  - pattern requests (to motor path or decision layers)
  - global broadcasts (fast mode)

---

## 8) Minimal checklist (to declare Brainstem “done”)

- [ ] RelayBundle schema + channel registry defined.
- [ ] Transformation invariants documented (“raw never goes up”).
- [ ] Pattern trigger types enumerated and ACL’d.
- [ ] Global broadcast states enumerated and retained policy set.
- [ ] RejectEvent emitted for wrong-type/wrong-direction messages.
