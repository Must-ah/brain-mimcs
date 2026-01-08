# Communication Spec (Brain-Like Lanes, Directions, and Gating)

This is a **single-page, transport-agnostic** communication contract for a brain-inspired system.
It defines **lanes (like tracts)**, **direction rules**, a common **message envelope**, and **thalamus/TRN-style gating**.

> Design intent: **content flows forward**, **control flows backward/sideways**, and **global modulators broadcast state**.
> Gating is implemented as a **protocol (rules + shared state)** rather than a single central router.

---

## 1) Lanes (names, purpose, direction)

### Lane A — DRIVER (payload / content)
- **Purpose:** carry primary content (“what happened”): feature events, sensor summaries, scene fragments.
- **Direction:** **SpinalCord → Brainstem → Thalamus(nucleus lane) → Cortex**
- **Rule:** DRIVER messages **never change gating**; they are **subject to** gating.

### Lane B — MODULATOR (feedback / attention / gain control)
- **Purpose:** carry control signals that tune routing: boost, suppress, precision, focus, priorities.
- **Direction:** **Cortex → Thalamus/TRN** and **Cortex ↔ Cortex (optional)**
- **Rule:** MODULATORS **may update gate state** for (scope, nucleus) over a time window.

### Lane G — GATE (TRN inhibition state)
- **Purpose:** represent the current inhibitory “shell” around thalamic relay lanes.
- **Direction:** **control-plane only**
- **Rule:** every relay decision reads `GateState(scope, nucleus)` before delivering drivers.

### Lane C — COMMAND (motor / actuation)
- **Purpose:** actionable commands selected by cortex / basal ganglia.
- **Direction:** **Cortex → Brainstem → SpinalCord (actuators)**
- **Rule:** commands should emit a **copy** to Lane E for monitoring/learning.

### Lane D — GLOBAL MODES (neuromodulators / operating state)
- **Purpose:** low-rate global settings: arousal, energy-saving, quiet hours, threat level, circadian bias.
- **Direction:** **Hypothalamus/Brainstem → ALL**
- **Rule:** D-lane signals shift baseline bias (e.g., default inhibition thresholds), not per-message routing.

### Lane E — ERROR / OUTCOME / LEARNING
- **Purpose:** prediction errors, action outcomes, corrective deltas, reward/punishment signals.
- **Direction:** mostly **upward** (SpinalCord/Cerebellum/Limbic → Cortex/BG/Thalamus/Hypothalamus)
- **Rule:** E-lane **never directly executes** actions; it biases future selection, gating, or policies.

---

## 2) Addressing (brain-like “nuclei” + scope)

Every message MUST specify:
- **scope_level:** `{device, room, house, user_session}`
- **scope:** an identifier within that level (e.g., `living_room`, `thermostat_1`)
- **nucleus:** thalamic “lane channel” (e.g., `LGN`, `MGN`, `VPL`, `MD`, `PULVINAR`) when relevant
- **timestamp_ms** and **correlation_id** (for binding/fusion without serializing)

**Concurrency unit (recommended):**
`(scope_level, scope, nucleus, correlation_id)` is independently processable.

---

## 3) Message envelope (required fields)

### Common fields
- `lane`: one of `{A_DRIVER, B_MODULATOR, C_COMMAND, D_GLOBAL, E_ERROR, G_GATE}`
- `kind`: `{driver, modulator}` (driver/modulator is still useful even outside thalamus)
- `scope_level`, `scope`, `timestamp_ms`, `correlation_id`
- `source` (optional)
- `priority` (optional), `salience` (optional), `deadline_ms` (optional), `confidence` (optional)
- `payload` (opaque map)

---

## 4) Gating protocol (TRN-style inhibition)

### Gate state
`GateState(scope_level, scope, nucleus)` includes:
- `inhibition`: 0..1 (higher = more suppression)
- `mode`: `{multi, winner_take_all}` (optional)
- `expires_at_ms`: optional (windowed gating)

### Relay rule (core)
A DRIVER (Lane A) for a given `(scope, nucleus)` may be delivered to cortex **iff**
`GateState.inhibition < threshold`, where threshold can be:
- a lane default,
- overridden by global modes (Lane D),
- and/or overridden by a per-message priority/salience rule.

### Feedback rule (cortex L6-like)
MODULATORS (Lane B) may publish:
- `requested_inhibition` for `(scope, nucleus)` for the next window
- `competition_set` + `winner_take_all` hint (optional)

### Competition rule (winner-take-all)
When GateMode is `winner_take_all`, at most one nucleus in the competition set should be “open enough”
for the window; others are suppressed.

---

## 5) Topic taxonomy (transport-agnostic naming convention)

Recommended topic structure:

- Lane A (drivers):  
  `/A/driver/{scope_level}/{scope}/nucleus/{nucleus}`

- Lane B (modulators):  
  `/B/mod/{scope_level}/{scope}/nucleus/{nucleus}`

- Lane G (gate updates):  
  `/G/gate/{scope_level}/{scope}/nucleus/{nucleus}`

- Lane C (commands):  
  `/C/cmd/{scope_level}/{scope}/channel/{channel}/action/{action_id}`

- Lane D (global modes):  
  `/D/mode/{scope_level}/{scope}`  (and `/D/mode/global`)

- Lane E (error/outcomes):  
  `/E/error/{scope_level}/{scope}/action/{action_id}`  
  `/E/outcome/{scope_level}/{scope}/action/{action_id}`

---

## 6) Non-goals
- No commitment to Kafka/NATS/Redis Streams/etc.
- No commitment to centralized vs decentralized deployment.
- No fixed list of nuclei; the set can evolve as capabilities grow.

---

## 7) Minimal checklist to adopt immediately
- Choose your initial nucleus set (e.g., LGN/MGN/VPL + PULVINAR/MD).
- Implement GateState storage and update semantics (windowed).
- Enforce driver/modulator lane separation.
- Require (scope, nucleus, correlation_id, timestamp_ms) on every message.
