# Brain Communication Model

This document describes a model for how signals travel through the brain. The model was developed by analyzing actual brain pathways and verified against neuroscience reference documents. It captures both the structural aspects (what connects to what) and the dynamic aspects (how signals flow and are processed).

---

## Core Insight: Routes Are Pre-Wired

The brain does not "decide" where signals go. Routes are physically built into the anatomy. When a neuron fires, the signal follows a path that was determined by how that neuron is wired.

A signal's route is determined by two factors:

**Origin** — Where the signal comes from. This could be a sensor in the body (thermoreceptor in fingertip), a structure in the brain (motor cortex), or any station that creates a new signal (cerebellum generating error correction).

**Type** — What kind of signal it is. Pain signals take different routes than fine touch signals. Motor commands take different routes than sensory information. Error corrections take different routes than motor plans.

Given an origin and a type, the route is a lookup — the anatomical wiring determines where the signal goes. There is no routing decision; there is only following the pre-built path.

```
ROUTE = lookup(ORIGIN, TYPE)

Examples:
  lookup(fingertip, pain)        → Peripheral nerve → Spinal cord → Spinothalamic → VPL → S1
  lookup(fingertip, fine touch)  → Peripheral nerve → Spinal cord → Dorsal columns → Brainstem → VPL → S1
  lookup(motor cortex, motor)    → Corticospinal tract → Brainstem → Spinal cord → Motor nerve
  lookup(cerebellum, correction) → Deep nuclei → VL thalamus → Motor cortex
```

---

## Highway Segments and Routes

A route is composed of multiple highway segments. Each segment is a named anatomical bundle of axons (a tract) that connects two points.

The complete journey of a signal is a route. The individual named pathways that make up that route are highway segments.

**Example: Pain from fingertip to conscious awareness**

| Segment | Name | Location | Carries |
|---------|------|----------|---------|
| 1 | Peripheral nerve (median nerve) | Outside CNS | First-order neuron axon |
| 2 | Spinothalamic tract | Spinal cord + Brainstem | Second-order neuron axon |
| 3 | Thalamocortical radiations | Cerebrum (internal capsule) | Third-order neuron axon |

The "spinothalamic tract" is not the whole route — it is one segment of the route. The route is the complete path; the segments are the named components.

Highway segments are bundles containing many parallel axons. Multiple signals can travel the same highway segment simultaneously, each using one axon within the bundle. Signals from different body locations (hand, foot, trunk) can all use the spinothalamic tract — they enter at different on-ramps (spinal levels) but share the same highway.

---

## Stations: Where Processing Happens

Stations are structures where signals are processed. Processing happens IN structures, not between them. While a signal travels along a highway segment, it is just transmitting — no processing occurs during transit.

Processing occurs when:
- A synapse happens (chemical handoff between neurons)
- Signals are compared or integrated
- Signals are gated or modulated
- Local effects are triggered

Every structure that a signal passes through is a potential station, but not all passages involve synapses. The spinothalamic tract passes through the brainstem without synapsing, but processing still occurs via collaterals to the reticular formation.

---

## Station Operations

A station can perform one or more operations on signals. The five operations are:

### RELAY (Active)

The signal continues with the same identity. Its origin and type remain unchanged. Its route continues as determined by the original lookup.

However, relay is NOT passive. The receiving station performs active processing:
- Only 5-10% of inputs to relay neurons are "drivers" (carrying the main information)
- 90-95% of inputs are "modulators" (affecting HOW the signal is processed)
- Gating can block or pass the signal
- Gain can amplify or attenuate the signal

The thalamus is the primary example. It relays sensory signals to cortex, but it actively filters them based on attention, predictions, and arousal state. A signal that enters the thalamus may or may not reach cortex, and if it does, its strength may be changed.

```
RELAY:
  Input signal  → [Active Processing] → Same signal continues
  (origin, type)   (gating, gain)       (same origin, same type)
                                        Route continues unchanged
```

### TRANSFORM

The station creates a NEW signal from one or more inputs. The output is not a continuation of any input — it is something computed from them.

The new signal has:
- New origin = the station that created it
- New type = the result of the computation
- New route = lookup(new origin, new type)

Examples:

**Cerebellum:** Receives motor plan (from cortex) and proprioception (from body). Compares them. Outputs error correction signal. The error correction is not present in either input — it is computed. Its route (to VL thalamus, then motor cortex) is different from either input route.

**Spinal cord reflex:** Receives pain signal. Creates motor command for withdrawal. The motor command is a new signal with its own route (to motor neurons, then muscle).

**Amygdala:** Receives sensory input. Evaluates threat. Creates multiple new signals: autonomic commands (to hypothalamus), freeze commands (to brainstem), emotional tags (to hippocampus). Each output has its own route.

```
TRANSFORM:
  Input(s)      → [Computation]  → NEW signal(s)
  (various)                        (new origin = this station)
                                   (new type = computed output)
                                   (new route = lookup for each)
```

### MODULATE

A context signal changes how another signal is processed, without changing that signal's identity. The main signal continues with the same origin, type, and route — but its strength, gain, or probability of passing has been changed.

Examples:

**Predictive coding at thalamus:** Cortex sends predictions down. Sensory signals come up. Thalamus compares them. If they match (expected), suppress. If they mismatch (unexpected), amplify. The sensory signal is still "pain from fingertip" — its identity hasn't changed. But its strength has been modulated by the prediction.

**Attention via TRN:** Attention commands from prefrontal/parietal cortex reach the thalamic reticular nucleus. TRN adjusts gating of thalamic relay nuclei. Attended signals pass; unattended signals are blocked. The signals themselves aren't changed — the gate is changed.

**Neuromodulation (norepinephrine, dopamine, etc.):** Broadcast signals from brainstem nuclei change the excitability of neurons everywhere. High norepinephrine = everything louder, more responsive. The neuromodulator doesn't carry specific information — it changes how all information is processed.

```
MODULATE:
  Main signal   → [Processing with   → Same signal continues
  (origin, type)   changed parameters]  (same origin, same type)
                        ↑                Route unchanged
  Context signal ───────┘                Strength/gain changed
  (attention, prediction, arousal)
```

### BRANCH

The signal is copied to multiple outputs. Each copy maintains the same identity (origin and type). Each copy follows its own route.

Examples:

**Pain signal at spinal cord:** The ascending path (to brain for conscious awareness) and collaterals to reticular formation (for arousal) are branches of the same pain signal.

**Sensory signal at thalamus:** The path to cortex and the fast path directly to amygdala are branches.

```
BRANCH:
  Input signal  → [Copy]  → Same signal on Route A
  (origin, type)          → Same signal on Route B
                          → Same signal on Route C
                Each copy: same origin, same type
```

### TERMINATE

The signal ends. No output signal continues. Instead, a local effect is triggered.

Examples:

**Motor neuron to muscle:** The motor command terminates by causing muscle contraction. There is no "signal" that continues from the muscle — the signal became a physical action.

**Cortex for conscious perception:** The pain signal terminates in conscious awareness. The ascending path ends here. (The cortex may generate NEW signals in response, but those are TRANSFORM operations, not continuation of the original signal.)

```
TERMINATE:
  Input signal  → [Local effect]  → No output signal
  (origin, type)   (muscle contraction, perception, hormone release)
```

---

## Stations Perform Multiple Operations

Most stations are hybrid — they perform multiple operations on the same input or on different inputs.

**Spinal cord receiving pain signal:**
- RELAY: Pain continues ascending (spinothalamic tract)
- BRANCH: Copy goes to reticular formation (spinoreticular tract)
- TRANSFORM: Creates motor command for reflex
- (Receives) MODULATE: Descending signals can suppress pain

**Thalamus receiving sensory signal:**
- RELAY: Signal continues to cortex
- BRANCH: Copy may go to amygdala (fast path)
- (Receives) MODULATE: Predictions from cortex, attention from TRN, arousal from brainstem

**Cortex receiving sensory signal:**
- TERMINATE: Conscious perception
- TRANSFORM: May create new signals (motor plans, memory encoding commands)

The station is not defined by one operation — it is a processing point where multiple operations can occur.

---

## Complete Example: Touch Hot Cup

Tracing all signals when fingertip touches a hot cup:

### SIGNAL 1: Pain

**Created:** Fingertip thermoreceptor (transduction)
**Origin:** Fingertip
**Type:** Pain/temperature
**Route:** lookup(fingertip, pain)

**STATION: Spinal cord (dorsal horn)**
- RELAY: Pain continues → spinothalamic tract
- BRANCH: Copy → spinoreticular tract (to reticular formation)
- TRANSFORM: Creates SIGNAL 2 (reflex motor command)
- Receives modulation: Descending NE can affect gain

### SIGNAL 2: Reflex Motor Command (NEW — created by spinal cord)

**Origin:** Spinal cord interneuron
**Type:** Motor command
**Route:** lookup(spinal cord, motor command) → motor neuron

**STATION: Motor neuron**
- TERMINATE: Muscle contracts, hand withdraws
- **Timing: 25-50 ms** (before conscious awareness)

### SIGNAL 1 continues: Pain

**STATION: Brainstem**
- RELAY: Pain continues (passes through, no synapse on main path)
- BRANCH: Collaterals to reticular formation

**STATION: Reticular formation (receives branch)**
- TRANSFORM: Creates SIGNAL 3 (arousal signal)

### SIGNAL 3: Arousal (NEW — created by reticular formation)

**Origin:** Reticular formation
**Type:** Arousal alert
**Route:** Activates locus coeruleus

**STATION: Locus coeruleus**
- TRANSFORM: Creates SIGNAL 4 (norepinephrine broadcast)

### SIGNAL 4: Norepinephrine Broadcast (NEW — created by LC)

**Origin:** Locus coeruleus
**Type:** Neuromodulator (NE)
**Route:** Broadcast to cortex, thalamus, amygdala, hippocampus, cerebellum, spinal cord

This signal MODULATES processing everywhere — it doesn't carry information, it changes how information is processed.

### SIGNAL 1 continues: Pain

**STATION: Thalamus (VPL)**
- Receives MODULATION: Predictions from cortex, attention from TRN, arousal from NE (Signal 4)
- RELAY: Pain continues → thalamocortical radiations
- BRANCH: Copy to amygdala (fast path)

**STATION: Amygdala (receives branch)**
- TRANSFORM: Creates SIGNAL 5 (autonomic command)

### SIGNAL 5: Autonomic Command (NEW — created by amygdala)

**Origin:** Amygdala (central nucleus)
**Type:** Autonomic command
**Route:** → Hypothalamus → Brainstem → Spinal cord → Sympathetic ganglia → Organs

**Results:** Heart rate increases, pupils dilate, sweating begins

### SIGNAL 1 continues: Pain

**STATION: Cortex (S1 → pain matrix)**
- TERMINATE: Conscious perception — "OW! HOT!"
- **Timing: 100-200 ms** (after reflex already fired)
- TRANSFORM: May create SIGNAL 6 (voluntary motor plan)

### SIGNAL 6: Voluntary Motor Plan (NEW — created by motor cortex)

**Origin:** Motor cortex
**Type:** Motor intention
**Route:** lookup(motor cortex, motor intention)

Path 1: → Corticospinal tract → Brainstem → Spinal cord → Motor neurons → Muscle (voluntary withdrawal, more controlled than reflex)

Path 2: → Pontine nuclei → Cerebellum (enters cerebellar loop for coordination)

**STATION: Cerebellum (receives motor plan)**
- Also receives: Proprioception (from spinocerebellar tract) — where body actually is
- TRANSFORM: Compares plan vs. actual, creates SIGNAL 7 (error correction)

### SIGNAL 7: Error Correction (NEW — created by cerebellum)

**Origin:** Cerebellum (dentate nucleus)
**Type:** Motor correction
**Route:** lookup(cerebellum, motor correction) → VL thalamus → Motor cortex

This correction updates the motor plan, making the movement more accurate.

---

## Signal Flow Summary for Hot Cup

| Signal | Origin | Type | Key Stations | Timing |
|--------|--------|------|--------------|--------|
| 1 | Fingertip | Pain | Spinal cord → Brainstem → Thalamus → Cortex | 100-200 ms to awareness |
| 2 | Spinal cord | Motor command (reflex) | Motor neuron → Muscle | 25-50 ms |
| 3 | Reticular formation | Arousal | Locus coeruleus | 50-80 ms |
| 4 | Locus coeruleus | NE broadcast | Everywhere (modulation) | 100-300 ms spread |
| 5 | Amygdala | Autonomic command | Hypothalamus → Organs | 200-500 ms |
| 6 | Motor cortex | Motor intention | Corticospinal + Cerebellum | 200-300 ms |
| 7 | Cerebellum | Error correction | VL thalamus → Motor cortex | Continuous loop |

One stimulus (hot cup) creates at least 7 distinct signals, each with its own origin, type, and route.

---

## Key Principles

### 1. Route = Pre-Wired Lookup

The route is determined by (origin + type). There is no routing decision — only anatomical wiring.

### 2. Processing Happens at Stations, Not During Transit

Signals traveling along highway segments are just transmitting. Processing (synapses, comparison, gating) happens at stations.

### 3. Transform Creates New Signals with New Routes

When a station transforms inputs into a new output, that output has a new origin (the station) and potentially a new type. Its route is determined by lookup(new origin, new type).

### 4. Modulation Changes Processing, Not Identity

Context signals (predictions, attention, neuromodulators) change HOW signals are processed — they don't change WHAT the signal represents. The signal continues with the same origin, type, and route.

### 5. Relay Is Active, Not Passive

Even relay stations (like thalamus) perform active processing. Only 5-10% of inputs carry the main signal; 90-95% modulate how that signal is processed.

### 6. Parallel Processing Is the Norm

One stimulus typically activates multiple pathways simultaneously. Reflexes, arousal, conscious perception, and autonomic responses all run in parallel.

### 7. Consciousness Arrives Late

Reflexes fire at 25-50 ms. Conscious awareness arrives at 100-200 ms. The protective response happens before you know why.

---

## Model Structure

```
SIGNAL
├── origin: structure that created/detected it
├── type: what kind of signal (pain, motor, correction, etc.)
└── route: lookup(origin, type) → sequence of highway segments

HIGHWAY SEGMENT
├── name: anatomical tract name (spinothalamic, corticospinal, etc.)
├── location: which structures it runs through
├── carries: which neuron order (first-order, second-order, etc.)
└── on-ramps/off-ramps: where signals can enter/exit

STATION
├── structure: anatomical name (spinal cord, thalamus, S1, etc.)
└── operations: list of [RELAY, TRANSFORM, MODULATE, BRANCH, TERMINATE]
    │
    ├── RELAY
    │   ├── input: signal (origin, type)
    │   ├── processing: gating, gain (active, not passive)
    │   └── output: same signal continues (same origin, same type)
    │
    ├── TRANSFORM
    │   ├── inputs: one or more signals
    │   ├── computation: what is computed
    │   └── outputs: NEW signal(s) (new origin = this station, new type)
    │
    ├── MODULATE
    │   ├── main signal: continues unchanged in identity
    │   ├── context signal: changes processing parameters
    │   └── effect: gain, threshold, gating changed
    │
    ├── BRANCH
    │   ├── input: signal (origin, type)
    │   └── outputs: copies of same signal to multiple routes
    │
    └── TERMINATE
        ├── input: signal (origin, type)
        └── effect: local action (muscle, perception, hormone release)

ROUTE
├── signal: which signal is traveling
└── path: sequence of [highway segment → station → highway segment → ...]
```

---

## Verification Against Source Documents

This model was verified against the project neuroscience documents:

| Claim | Document Evidence | Status |
|-------|-------------------|--------|
| Route = (Origin + Type) | Explicit pathway descriptions in architecture outline | ✓ Confirmed |
| RELAY is active processing | "Thalamus performs active processing, not passive relay" — 5-10% drivers, 90-95% modulators | ✓ Confirmed |
| TRANSFORM creates new signals | Cerebellum "compares motor plans with sensory feedback and sends corrections" | ✓ Confirmed |
| MODULATE changes processing | "Precision weighting — modulating prediction errors by confidence/certainty" | ✓ Confirmed |
| BRANCH copies signals | "Two pathways: slow pathway through cortex... fast pathway through thalamus directly to amygdala" | ✓ Confirmed |
| TERMINATE ends signals | "Reflexes... occur entirely within the spinal cord" — terminate in muscle contraction | ✓ Confirmed |
| Transform creates new route | Cerebellar output goes via VL thalamus (different from input route) | ✓ Confirmed |
| Modulate preserves identity | "Bias signals to other brain structures guiding activity flow" — changes flow, not content | ✓ Confirmed |

---

## Next Steps

This model provides the foundation for understanding brain communication. To complete it, we need:

1. **Enumerate all highway segments** — List all named tracts in the brain with their locations and connections

2. **Map all stations** — Document which operations each major structure performs

3. **Build route lookup tables** — For each (origin, type) pair, document the complete route

4. **Add timing data** — Document transmission times for each segment and processing times at each station

5. **Map modulation pathways** — Document which context signals affect which stations and how

---

## Related Documents

| Document | Content |
|----------|---------|
| sensory-pathway-walkthrough.md | Detailed trace of pain signal from fingertip to cortex |
| brain-communication-framework.md | Categories of communication systems (type, architecture, role) |
| brain-communication-systems-overview.md | All 14 communication systems |

---

*This model describes how signals travel through the brain based on pre-wired anatomical routes, with processing at stations that can relay, transform, modulate, branch, or terminate signals.*
