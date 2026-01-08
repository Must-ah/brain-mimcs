# Broker Boundary & Bridge Policy (Tract-Like Direction Rules)

This section defines **broker roles**, **topic ownership**, and **allowed cross-broker flows** so the overall system can be recurrent (feedback loops) while each boundary stays **tract-like** and fault-isolated.

---

## 1) Brokers and responsibilities

### Broker S — Spinal (raw I/O + reflex)
**Owns topics**
- `/sc/aff/...` (device afferents: sensors, state)
- `/sc/eff/...` (device efferents: actuator low-level commands)
- `/sc/reflex/...` (local reflex arcs)

**Design intent**
- Highest-rate traffic lives here.
- Local reflex loops may operate without waiting for upstream services.

---

### Broker C — Core/Control (brainstem + modulators/gates/modes)
**Owns topics**
- `/bs/relay/...` (typed relay bundles)
- `/B/...` (modulators)
- `/G/...` (gate state)
- `/D/...` (global modes)

**Design intent**
- Must remain responsive under sensor storms.
- Acts as aggregation + control plane.

---

### Broker R — Reliable (commands + outcomes)
**Owns topics**
- `/C/...` (commands)
- `/E/...` (outcomes/errors/learning signals)

**Design intent**
- Lower-rate but reliability-oriented traffic.
- Commands and outcomes are traceable and idempotent.

---

### Broker X — Reflect (audit/efference copy)
**Owns topics**
- `/X/reflect/...` (best-effort copies for audit/observability/replay)

**Design intent**
- Reflection must never block primary flows.
- In production: write-only sink (no control influence).

---

## 2) Bridge directions (default allow-list)

> **Global principle:** The system is recurrent overall, but **each boundary enforces a preferred direction**.

### S → C (Spinal → Core) ✅
**Allowed**
- Raw device signals may cross **only if transformed** into **RelayBundles** (typed, windowed summaries).
- Bridge should carry **summaries**, not raw sensor firehoses.

**Disallowed**
- Direct bridging of `/sc/aff/#` into Core.
- Raw high-rate topics must not be forwarded upward.

**Purpose**
- “Raw never goes up; it becomes summarized relays.”

---

### C → R (Core → Reliable) ✅
**Allowed**
- Commands issued by higher-level decision components:
  - `/C/...` (idempotent commands)
- Control signals that need persistence/audit:
  - select `/E/...` (optional)

**Disallowed**
- High-rate driver traffic routed into Reliable.

---

### R → S (Reliable → Spinal) ✅
**Allowed**
- Actuation commands that must reach devices:
  - `/sc/eff/...` (or device-specific command endpoints)

**Notes**
- Keep this “motor path” narrow: only commands + necessary parameters.

---

### S → R (Spinal → Reliable) ✅
**Allowed**
- Outcomes/acks/status summaries from devices:
  - `/E/outcome/...`, `/E/error/...`
- Proprioceptive confirmations (“did it happen?”), not raw sensor floods.

---

### {S,C,R} → X (Any → Reflect) ✅
**Allowed**
- Best-effort copies of selected events:
  - Commands, Outcomes, Gate changes, High-salience Drivers, Mode changes

**Rule**
- Reflection must be non-blocking; if Reflect is down, primary operation continues.

---

### X → {S,C,R} (Reflect → Others) 🚫 (production default)
**Default**
- Disallow all Reflect-to-core bridges in production.

**Optional “Replay Mode”**
- If you support replay/testing, allow X→C or X→R through a **manual switch** and strict ACLs.
- Replay must never impersonate device identity.

---

## 3) “Tract boundary” rules (simple invariants)

### Rule A — Raw afferents do not cross upward boundaries
- `/sc/aff/#` stays in Broker S.
- Upward flow is via `/bs/relay/#` summaries (Broker C).

### Rule B — Commands descend only via the motor path
- High-level decisions publish `/C/...` (Broker R).
- Devices receive via `/sc/eff/...` (Broker S), not via ad-hoc topics.

### Rule C — Feedback returns as outcomes, not as raw dumps
- Devices report completion/ack/outcome on `/E/...` (Broker R).
- Outcome messages may update gating/modes upstream, but remain low-rate.

### Rule D — Reflection is write-only in production
- All lanes may mirror into Reflect.
- Reflect never participates in live control loops unless replay mode is explicitly enabled.

---

## 4) Recommended “minimum reflection set” (Lane X)
Mirror at least:
- **Commands** (`/C/...`)
- **Outcomes/Errors** (`/E/...`)
- **Gate changes** (`/G/...`)
- **Global modes** (`/D/...`)
Optionally:
- **High-salience relay bundles** (`/bs/relay/...` with salience ≥ threshold)

---

## 5) Operational note (Mosquitto)
These policies are enforced via:
- Separate Mosquitto instances (preferred), or separate listeners with strict ACLs
- Narrow bridges (explicit allow-lists)
- Per-client rate limits and message size limits (where available)
