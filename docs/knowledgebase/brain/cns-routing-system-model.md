# CNS Message Routing System: Complete Conceptual Model

## Version 1.0 — Spinal Cord and Brainstem Routes

This document specifies a message routing system modeled on the human central nervous system. The system implements structural routing where signal type determines pathway, anatomical hierarchy where all signals must traverse the proper levels, and timing fidelity where conduction velocities and synaptic delays produce realistic transit times.

---

# PART 1: FOUNDATIONAL PRINCIPLES

## 1.1 The Core Insight

The brain does not route messages the way computer networks do. There is no packet switching, no routing tables consulted at runtime, no dynamic path discovery. Instead, the brain uses **structural routing** — the physical anatomy of the connection determines where a signal can go. A pain signal takes the spinothalamic tract not because some router decided that's the best path, but because pain-sensitive neurons in the dorsal horn are physically wired to project their axons into that tract and no other.

This is the foundational principle: **signal type determines anatomy, and anatomy determines route.**

## 1.2 The Communication Hierarchy

All signals in this system must traverse the anatomical hierarchy. There are no shortcuts, no direct connections that bypass levels.

### Ascending Direction (Sensory — Toward Brain)

```
PERIPHERAL RECEPTOR
        ↓
   SPINAL CORD (entry, local processing, first relay)
        ↓
    BRAINSTEM (relay nuclei, crossing points, collateral branching)
        ↓
     THALAMUS (gateway to cortex)
        ↓
      CORTEX (conscious perception, higher processing)
```

Every sensory signal (except olfaction) must pass through each level. The signal cannot jump from spinal cord directly to cortex.

### Descending Direction (Motor/Control — Toward Body)

```
      CORTEX (motor command generation)
        ↓
     THALAMUS (for some pathways)
        ↓
    BRAINSTEM (pyramids, motor nuclei)
        ↓
   SPINAL CORD (motor neuron pools)
        ↓
PERIPHERAL EFFECTOR (muscle, gland)
```

A motor command from motor cortex cannot directly reach a muscle. It must descend through the proper hierarchy.

### Local Processing Exception (Reflexes)

```
PERIPHERAL RECEPTOR
        ↓
   SPINAL CORD ──→ PERIPHERAL EFFECTOR
        ↓
   (continues ascending in parallel)
```

The spinal cord can generate local responses without brain involvement. The signal typically BOTH triggers the reflex AND continues ascending.

---

# PART 2: SYSTEM COMPONENTS

## 2.1 Signal

A signal carries properties that determine its routing fate.

### Signal Properties

| Property | Description | Examples |
|----------|-------------|----------|
| **type** | The kind of information; determines which highway | `pain_fast`, `pain_slow`, `temperature`, `fine_touch`, `crude_touch`, `proprioception_conscious`, `proprioception_unconscious`, `motor_voluntary`, `motor_postural`, `autonomic` |
| **origin** | Where the signal originated | Body segment (`C5_dermatome`, `L4_myotome`), cortical area (`M1_hand`, `S1_face`) |
| **laterality** | Left or right side | `left`, `right` |
| **intensity** | Signal strength (0.0 to 1.0) | Affects threshold detection, reflex triggering |
| **timestamp** | When signal was generated | Milliseconds, used for timing calculations |
| **payload** | The actual data content | Application-specific |

### Signal Type Categories

**Sensory Types (Ascending)**

| Type | Description | Fiber Class | Velocity |
|------|-------------|-------------|----------|
| `proprioception_conscious` | Joint position, muscle length (to cortex) | Aα, Aβ | 80-120 m/s |
| `proprioception_unconscious` | Same info but to cerebellum | Aα, Aβ | 80-120 m/s |
| `fine_touch` | Precise touch, two-point discrimination | Aβ | 35-75 m/s |
| `vibration` | Vibration sense | Aβ | 35-75 m/s |
| `pressure` | Deep pressure | Aβ | 35-75 m/s |
| `crude_touch` | Light touch, poorly localized | Aβ | 35-75 m/s |
| `pain_fast` | Sharp, well-localized pain | Aδ | 5-35 m/s |
| `pain_slow` | Dull, diffuse, aching pain | C | 0.5-2 m/s |
| `temperature_cold` | Cold sensation | Aδ | 5-35 m/s |
| `temperature_warm` | Warm sensation | C | 0.5-2 m/s |
| `itch` | Itch sensation | C | 0.5-2 m/s |
| `visceral` | Internal organ sensation | C, Aδ | 0.5-35 m/s |

**Motor Types (Descending)**

| Type | Description | Fiber Class | Velocity |
|------|-------------|-------------|----------|
| `motor_voluntary_distal` | Fine motor control (fingers, toes) | Large pyramidal | 70-120 m/s |
| `motor_voluntary_proximal` | Proximal limb, trunk | Large pyramidal | 70-120 m/s |
| `motor_postural` | Posture, antigravity | Reticulospinal | 50-80 m/s |
| `motor_balance` | Balance adjustments | Vestibulospinal | 50-80 m/s |
| `motor_reflex_modulation` | Reflex gain adjustment | Various | 30-60 m/s |
| `autonomic_sympathetic` | Fight-or-flight | B, C | 3-15 m/s |
| `autonomic_parasympathetic` | Rest-and-digest | B, C | 3-15 m/s |
| `pain_modulation` | Descending pain control | Various | 20-50 m/s |

## 2.2 Station

A station is a nucleus or anatomical structure where signals are processed.

### Station Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| **RELAY** | Pass signal forward with minimal transformation | LGN relaying to V1 |
| **TRANSFORM** | Change signal representation/encoding | Dorsal horn recoding pain |
| **MODULATE** | Adjust gain/priority without changing content | TRN modulating thalamic relay |
| **BRANCH** | Copy signal to multiple destinations | Spinothalamic collaterals |
| **TERMINATE** | Final destination; signal consumed | Motor neuron receiving command |
| **GATE** | Allow or block signal based on conditions | Pain gating in dorsal horn |
| **INTEGRATE** | Combine multiple inputs into single output | Interneuron pools |

### Station Timing

| Component | Duration | Description |
|-----------|----------|-------------|
| Synaptic delay | 0.5-5 ms | Neurotransmitter release, diffusion, receptor binding |
| Processing delay | 0-20 ms | Additional computation time |
| Total station delay | 1-25 ms | Sum of above |

### Station Properties

Each station has:
- **name**: Anatomical identifier
- **location**: CNS division (spinal_cord, brainstem, cerebrum, cerebellum)
- **level**: Specific location (e.g., `medulla`, `C5_segment`)
- **operations**: Map of signal_type → operation(s) performed
- **delay**: Processing time in milliseconds
- **connections_in**: Which highways arrive here
- **connections_out**: Which highways depart from here

## 2.3 Highway

A highway is a tract connecting stations.

### Highway Properties

| Property | Description |
|----------|-------------|
| **name** | Anatomical tract name |
| **origin_station** | Where the highway begins |
| **destination_station** | Where the highway ends |
| **fiber_type** | Aα, Aβ, Aδ, B, or C |
| **velocity** | Conduction velocity in m/s |
| **length** | Physical length in meters |
| **crossing** | Where decussation occurs (if any) |
| **signal_types** | Which signal types use this highway |
| **topography** | How spatial organization is maintained |

### Fiber Types and Velocities

| Fiber Type | Diameter (μm) | Velocity (m/s) | Myelination | Typical Signals |
|------------|---------------|----------------|-------------|-----------------|
| Aα | 13-20 | 80-120 | Heavy | Proprioception, motor |
| Aβ | 6-12 | 35-75 | Heavy | Fine touch, pressure |
| Aδ | 1-5 | 5-35 | Light | Fast pain, cold |
| B | 1-3 | 3-15 | Light | Autonomic preganglionic |
| C | 0.2-1.5 | 0.5-2 | None | Slow pain, warm, itch |

### Transit Time Calculation

```
transit_time = highway_length / conduction_velocity
```

For a 0.5 meter highway with Aδ fibers at 15 m/s:
```
transit_time = 0.5 / 15 = 0.033 seconds = 33 milliseconds
```

## 2.4 Reflex Arc

A reflex arc is a local spinal circuit that generates motor output without brain involvement.

### Reflex Arc Properties

| Property | Description |
|----------|-------------|
| **name** | Reflex identifier |
| **trigger_type** | Signal type that triggers this reflex |
| **threshold** | Minimum intensity to trigger (0.0-1.0) |
| **circuit_type** | `monosynaptic` or `polysynaptic` |
| **latency** | Time from input to output (ms) |
| **motor_pattern** | Which muscles activated/inhibited |
| **ascending_continues** | Whether signal continues to brain (usually true) |

### Standard Reflex Types

| Reflex | Trigger | Circuit | Latency | Pattern |
|--------|---------|---------|---------|---------|
| Stretch (myotatic) | `proprioception` from muscle stretch | Monosynaptic | 25 ms | Contract stretched muscle |
| Withdrawal | `pain_fast` or `pain_slow` above threshold | Polysynaptic | 30-50 ms | Flex ipsilateral limb |
| Crossed extensor | `pain` (accompanies withdrawal) | Polysynaptic | 35-55 ms | Extend contralateral limb |
| Golgi tendon | `proprioception` from tendon tension | Polysynaptic | 30 ms | Inhibit contracting muscle |

---

# PART 3: CROSSING LOGIC

Different pathways cross at different anatomical levels. This determines which side of the brain processes which side of the body.

## 3.1 Crossing Point Reference

| Pathway | Crosses At | Mechanism |
|---------|------------|-----------|
| Spinothalamic | Spinal cord (1-2 segments above entry) | Anterior white commissure |
| Dorsal column-medial lemniscus | Medulla | Internal arcuate fibers |
| Lateral corticospinal | Medulla | Pyramidal decussation (90%) |
| Anterior corticospinal | Spinal cord (segmental) | Anterior white commissure (10%) |
| Rubrospinal | Midbrain | Ventral tegmental decussation |
| Tectospinal | Midbrain | Dorsal tegmental decussation |
| Dorsal spinocerebellar | Does not cross | — |
| Ventral spinocerebellar | Double-crosses | Spinal cord, then cerebellar entry |
| Reticulospinal (pontine) | Does not cross | — |
| Reticulospinal (medullary) | Partial/variable | — |
| Vestibulospinal (lateral) | Does not cross | — |
| Vestibulospinal (medial) | Bilateral | — |

## 3.2 Laterality State Machine

A signal's laterality changes when it crosses:

```
Signal enters at: RIGHT
  ↓
Crosses in spinal cord?
  YES → laterality becomes LEFT
  NO  → laterality remains RIGHT
  ↓
Crosses in medulla?
  YES → laterality becomes opposite of current
  NO  → laterality unchanged
  ↓
Crosses in midbrain?
  YES → laterality becomes opposite of current
  NO  → laterality unchanged
```

Example for pain signal from right foot:
```
Origin: RIGHT
After spinal cord crossing: LEFT
Final processing: LEFT cortex perceives RIGHT body pain
```

Example for fine touch signal from right foot:
```
Origin: RIGHT
Through spinal cord: RIGHT (no crossing yet)
After medulla crossing: LEFT
Final processing: LEFT cortex perceives RIGHT body touch
```

---

# PART 4: COMPLETE ROUTE SPECIFICATIONS

This section defines every pathway in the spinal cord and brainstem inventory with complete station-by-station routing.

## 4.1 Route Specification Format

Each route is specified as:

```
ROUTE: [Pathway Name]
Signal Types: [which signals use this route]
Direction: [ascending/descending]
Fiber Type: [Aα/Aβ/Aδ/B/C]
Velocity: [m/s]

STATIONS:
[#] [Station Name]
    Location: [anatomical location]
    Operations: [RELAY/TRANSFORM/MODULATE/BRANCH/TERMINATE/GATE/INTEGRATE]
    Delay: [ms]
    Crossing: [yes/no, if yes specify details]
    Branches: [if BRANCH, list destinations]
    → [Next station via Highway Name]
```

---

## 4.2 ASCENDING ROUTES

### ROUTE A1: Dorsal Column-Medial Lemniscus (Lower Body)

```
ROUTE: Fasciculus Gracilis → Medial Lemniscus (Lower Body)
Signal Types: fine_touch, vibration, pressure, proprioception_conscious
Body Region: Lower body (T7 and below)
Direction: Ascending
Fiber Type: Aβ (touch), Aα (proprioception)
Velocity: 35-120 m/s

STATIONS:

[1] PERIPHERAL RECEPTOR
    Location: Skin, muscle spindle, joint capsule (lower body)
    Operations: TRANSFORM (mechanical → electrical)
    Delay: 1 ms
    → Peripheral nerve to Dorsal Root Ganglion

[2] DORSAL ROOT GANGLION (L1-S5, T7-T12)
    Location: Spinal nerve, adjacent to spinal cord
    Operations: RELAY (cell body of 1st order neuron, no synapse)
    Delay: 0.5 ms
    Note: Pseudounipolar neuron — signal passes through without synapse
    → Central process enters spinal cord dorsal column

[3] SPINAL CORD ENTRY (Dorsal Column)
    Location: Dorsal funiculus, medial position (gracile fasciculus)
    Operations: RELAY (axons ascend without synapse)
    Delay: 0 ms (passage only)
    Crossing: NO — ascends ipsilaterally
    Course: Ascends entire length of spinal cord in fasciculus gracilis
    → Fasciculus gracilis to Nucleus Gracilis

[4] NUCLEUS GRACILIS
    Location: Caudal medulla, dorsal surface
    Operations: TRANSFORM (1st synapse; 1st order → 2nd order neuron)
    Delay: 3 ms
    Processing: Somatotopic organization preserved; some integration
    → Internal arcuate fibers (CROSSING)

[5] INTERNAL ARCUATE FIBERS / SENSORY DECUSSATION
    Location: Medulla, crossing ventral to central canal
    Operations: RELAY (crossing axons)
    Delay: 0.5 ms
    Crossing: YES — signal crosses from ipsilateral to contralateral side
    → Forms medial lemniscus on opposite side

[6] MEDIAL LEMNISCUS (Medulla segment)
    Location: Medulla, ventromedial, near midline
    Operations: RELAY (ascending tract)
    Delay: 0 ms (passage only)
    Topography: Lower body represented laterally
    → Continues to pons

[7] MEDIAL LEMNISCUS (Pons segment)
    Location: Pons, medial tegmentum
    Operations: RELAY
    Delay: 0 ms (passage only)
    → Continues to midbrain

[8] MEDIAL LEMNISCUS (Midbrain segment)
    Location: Midbrain, lateral tegmentum
    Operations: RELAY
    Delay: 0 ms (passage only)
    → Projects to thalamus

[9] THALAMUS — VPL (Ventral Posterolateral Nucleus)
    Location: Thalamus, ventral posterior region
    Operations: RELAY, MODULATE, GATE
    Delay: 5 ms
    Processing: 2nd synapse (2nd order → 3rd order neuron)
    Modulation: Subject to TRN gating, cortical feedback, arousal state
    Somatotopy: Preserved (lower body in lateral VPL)
    → Thalamocortical radiations (posterior limb internal capsule)

[10] PRIMARY SOMATOSENSORY CORTEX (S1) — Leg area
    Location: Postcentral gyrus, medial surface (near midline)
    Operations: TERMINATE, TRANSFORM
    Delay: 20 ms (cortical processing)
    Processing: Conscious perception; feature extraction
    Layer: Input arrives Layer IV
    End: Signal terminates here for conscious perception

TOTAL ROUTE STATISTICS:
- Stations: 10
- Synapses: 3 (nucleus gracilis, VPL thalamus, cortex)
- Major crossing: Medulla (sensory decussation)
- Approximate length: 1.5 meters (foot to cortex)
- Approximate time: 25-45 ms (depending on fiber type and exact origin)
```

---

### ROUTE A2: Dorsal Column-Medial Lemniscus (Upper Body)

```
ROUTE: Fasciculus Cuneatus → Medial Lemniscus (Upper Body)
Signal Types: fine_touch, vibration, pressure, proprioception_conscious
Body Region: Upper body (T6 and above)
Direction: Ascending
Fiber Type: Aβ (touch), Aα (proprioception)
Velocity: 35-120 m/s

STATIONS:

[1] PERIPHERAL RECEPTOR
    Location: Skin, muscle spindle, joint capsule (upper body, arm, hand)
    Operations: TRANSFORM (mechanical → electrical)
    Delay: 1 ms
    → Peripheral nerve to Dorsal Root Ganglion

[2] DORSAL ROOT GANGLION (C1-T6)
    Location: Spinal nerve, adjacent to spinal cord
    Operations: RELAY
    Delay: 0.5 ms
    → Central process enters spinal cord

[3] SPINAL CORD ENTRY (Dorsal Column)
    Location: Dorsal funiculus, lateral position (cuneate fasciculus)
    Operations: RELAY
    Delay: 0 ms (passage only)
    Crossing: NO — ascends ipsilaterally
    → Fasciculus cuneatus to Nucleus Cuneatus

[4] NUCLEUS CUNEATUS
    Location: Caudal medulla, dorsal surface, lateral to nucleus gracilis
    Operations: TRANSFORM (1st synapse)
    Delay: 3 ms
    → Internal arcuate fibers (CROSSING)

[5] INTERNAL ARCUATE FIBERS / SENSORY DECUSSATION
    Location: Medulla
    Operations: RELAY
    Delay: 0.5 ms
    Crossing: YES
    → Joins medial lemniscus

[6-8] MEDIAL LEMNISCUS (Medulla → Pons → Midbrain)
    Same as Route A1, stations 6-8
    Topography: Upper body represented medially

[9] THALAMUS — VPL
    Location: Thalamus
    Operations: RELAY, MODULATE, GATE
    Delay: 5 ms
    Somatotopy: Upper body in medial VPL
    → Thalamocortical radiations

[10] PRIMARY SOMATOSENSORY CORTEX (S1) — Hand/Arm area
    Location: Postcentral gyrus, lateral surface
    Operations: TERMINATE, TRANSFORM
    Delay: 20 ms
    Note: Hand has disproportionately large cortical representation

TOTAL ROUTE STATISTICS:
- Stations: 10
- Synapses: 3
- Major crossing: Medulla
- Approximate length: 0.8 meters (hand to cortex)
- Approximate time: 15-25 ms
```

---

### ROUTE B1: Lateral Spinothalamic Tract (Pain and Temperature)

```
ROUTE: Lateral Spinothalamic Tract
Signal Types: pain_fast, pain_slow, temperature_cold, temperature_warm
Body Region: All body levels
Direction: Ascending
Fiber Type: Aδ (fast pain, cold), C (slow pain, warm)
Velocity: 0.5-35 m/s

STATIONS:

[1] PERIPHERAL RECEPTOR (Nociceptor / Thermoreceptor)
    Location: Skin, deep tissue
    Operations: TRANSFORM
    Delay: 1 ms
    Receptor types: Free nerve endings
    → Peripheral nerve to DRG

[2] DORSAL ROOT GANGLION
    Location: Adjacent to spinal cord
    Operations: RELAY
    Delay: 0.5 ms
    → Central process to dorsal horn

[3] DORSAL HORN (Laminae I, II, V)
    Location: Spinal cord, dorsal gray matter
    Operations: TRANSFORM, GATE, INTEGRATE, BRANCH
    Delay: 5 ms
    Processing: 
        - 1st synapse (1st order → 2nd order neuron)
        - Substantia gelatinosa (Lamina II) modulates pain
        - Gate control: non-painful input can inhibit pain transmission
        - Descending modulation from brainstem affects transmission
    Branches:
        - Main projection crosses and ascends
        - Local reflex connections (triggers withdrawal if intensity > threshold)
    → Anterior white commissure (CROSSING)

[4] ANTERIOR WHITE COMMISSURE
    Location: Spinal cord, anterior to central canal
    Operations: RELAY (crossing axons)
    Delay: 0.5 ms
    Crossing: YES — crosses within 1-2 segments of entry
    → Enters lateral spinothalamic tract on OPPOSITE side

[5] LATERAL SPINOTHALAMIC TRACT (Spinal Cord)
    Location: Lateral funiculus, anterolateral portion
    Operations: RELAY
    Delay: 0 ms (passage only)
    Topography: Sacral fibers lateral, cervical fibers medial (lamination)
    → Ascends to brainstem

[6] LATERAL SPINOTHALAMIC TRACT (Medulla)
    Location: Lateral medulla
    Operations: BRANCH
    Delay: 1 ms
    Branches:
        - Main tract continues to thalamus
        - Collaterals to RETICULAR FORMATION (arousal)
    → Continues ascending; collaterals to reticular formation

[7] RETICULAR FORMATION (Collateral Branch)
    Location: Medullary and pontine tegmentum
    Operations: TRANSFORM, BRANCH
    Delay: 3 ms
    Processing: Contributes to arousal, autonomic responses
    Output: Ascending reticular activating system
    Note: This is a collateral — main signal continues separately

[8] LATERAL SPINOTHALAMIC TRACT (Pons)
    Location: Lateral pontine tegmentum
    Operations: BRANCH
    Delay: 1 ms
    Branches:
        - Main tract continues
        - Collaterals to PARABRACHIAL NUCLEUS (autonomic, emotional)
    → Continues ascending

[9] LATERAL SPINOTHALAMIC TRACT (Midbrain)
    Location: Lateral midbrain tegmentum
    Operations: BRANCH
    Delay: 1 ms
    Branches:
        - Main tract continues to thalamus
        - Collaterals to PERIAQUEDUCTAL GRAY (pain modulation)
        - Collaterals to SUPERIOR COLLICULUS (orienting)
    → Main tract to thalamus

[10] PERIAQUEDUCTAL GRAY (Collateral Branch)
    Location: Midbrain, surrounding cerebral aqueduct
    Operations: INTEGRATE, OUTPUT
    Delay: 5 ms
    Processing: Initiates descending pain modulation
    Output: Activates descending inhibitory pathways
    Note: Collateral branch — can suppress further pain transmission

[11] SUPERIOR COLLICULUS (Collateral Branch)
    Location: Midbrain tectum
    Operations: INTEGRATE
    Delay: 3 ms
    Processing: Contributes to orienting toward painful stimulus
    Note: Collateral branch for reflexive orienting

[12] THALAMUS — VPL
    Location: Thalamus, ventral posterior lateral nucleus
    Operations: RELAY, MODULATE, BRANCH
    Delay: 5 ms
    Processing: 2nd synapse (2nd order → 3rd order neuron)
    Branches:
        - Main projection to S1 (sensory-discriminative)
        - Projection to S2 (further processing)
        - Projection to INSULA (affective component)
    → Thalamocortical radiations

[13] PRIMARY SOMATOSENSORY CORTEX (S1)
    Location: Postcentral gyrus
    Operations: TERMINATE, TRANSFORM
    Delay: 20 ms
    Processing: Conscious localization and intensity of pain
    Aspect: Sensory-discriminative (where, how much)

[14] INSULAR CORTEX (Parallel Branch from Thalamus)
    Location: Deep within lateral sulcus
    Operations: TERMINATE, TRANSFORM
    Delay: 25 ms
    Processing: Affective-emotional aspect of pain
    Aspect: Suffering, unpleasantness

[15] ANTERIOR CINGULATE CORTEX (Via Insula/Medial Thalamus)
    Location: Medial frontal lobe
    Operations: TERMINATE, INTEGRATE
    Delay: 30 ms
    Processing: Emotional response, motivation to act
    Aspect: Behavioral response to pain

TOTAL ROUTE STATISTICS:
- Stations: 15 (including all branches)
- Synapses: 3-4 (depending on branch)
- Major crossing: Spinal cord (within 1-2 segments of entry)
- Collateral branches: Reticular formation, PAG, superior colliculus, insula
- Approximate length: 1.5 meters
- Approximate time: 
    - Fast pain (Aδ): 50-100 ms
    - Slow pain (C): 750-3000 ms (nearly a second to several seconds)
```

---

### ROUTE B2: Anterior Spinothalamic Tract (Crude Touch, Pressure)

```
ROUTE: Anterior Spinothalamic Tract
Signal Types: crude_touch, pressure
Body Region: All body levels
Direction: Ascending
Fiber Type: Aβ
Velocity: 35-75 m/s

STATIONS:

[1-2] PERIPHERAL RECEPTOR → DRG
    Same as Route B1

[3] DORSAL HORN (Laminae IV-VI)
    Location: Spinal cord
    Operations: TRANSFORM
    Delay: 3 ms
    Processing: 1st synapse; less complex processing than pain
    → Anterior white commissure

[4] ANTERIOR WHITE COMMISSURE
    Operations: RELAY
    Crossing: YES — crosses in spinal cord
    → Anterior spinothalamic tract

[5-8] ANTERIOR SPINOTHALAMIC TRACT (Spinal → Medulla → Pons → Midbrain)
    Location: Anterior/anterolateral funiculus
    Operations: RELAY
    Fewer collaterals than lateral spinothalamic
    → Thalamus

[9] THALAMUS — VPL
    Operations: RELAY, MODULATE
    Delay: 5 ms
    → Cortex

[10] PRIMARY SOMATOSENSORY CORTEX (S1)
    Operations: TERMINATE
    Delay: 20 ms

TOTAL ROUTE STATISTICS:
- Stations: 10
- Synapses: 3
- Major crossing: Spinal cord
- Approximate time: 30-50 ms
```

---

### ROUTE C1: Dorsal Spinocerebellar Tract (Lower Body Proprioception to Cerebellum)

```
ROUTE: Dorsal Spinocerebellar Tract
Signal Types: proprioception_unconscious
Body Region: Lower body (T1 and below)
Direction: Ascending
Fiber Type: Aα
Velocity: 80-120 m/s (FASTEST tract in CNS)

STATIONS:

[1] PERIPHERAL RECEPTOR (Muscle Spindle, Golgi Tendon Organ)
    Location: Muscle, tendon
    Operations: TRANSFORM
    Delay: 1 ms
    → Peripheral nerve to DRG

[2] DORSAL ROOT GANGLION
    Operations: RELAY
    Delay: 0.5 ms
    → Spinal cord

[3] CLARKE'S COLUMN (Nucleus Dorsalis)
    Location: Spinal cord, medial Lamina VII, T1-L2 only
    Operations: TRANSFORM
    Delay: 3 ms
    Processing: 1st synapse; integrates proprioceptive input
    Note: Neurons for lower body input; sacral/lumbar info ascends to reach Clarke's column
    Crossing: NO — projects ipsilaterally
    → Dorsal spinocerebellar tract

[4] DORSAL SPINOCEREBELLAR TRACT (Spinal Cord)
    Location: Lateral funiculus, dorsal part
    Operations: RELAY
    Delay: 0 ms (passage only)
    Velocity: 80-120 m/s — fastest conduction in CNS
    → Ascends to medulla

[5] INFERIOR CEREBELLAR PEDUNCLE (Restiform Body)
    Location: Medulla/Cerebellar junction
    Operations: RELAY
    Delay: 0.5 ms
    Crossing: NO — enters cerebellum ipsilaterally
    → Cerebellar cortex

[6] CEREBELLAR CORTEX (Spinocerebellum — Vermis/Intermediate Zone)
    Location: Anterior and posterior lobes, midline and paravermal regions
    Operations: TRANSFORM, INTEGRATE
    Delay: 10 ms
    Processing: 
        - Mossy fiber input to granule cells
        - Parallel fibers to Purkinje cells
        - Purkinje cells inhibit deep nuclei
    → Deep cerebellar nuclei

[7] DEEP CEREBELLAR NUCLEI (Interposed/Fastigial)
    Location: Within cerebellar white matter
    Operations: INTEGRATE, OUTPUT
    Delay: 5 ms
    Processing: Integration with other cerebellar inputs
    Output: To brainstem motor centers (vestibular nuclei, reticular formation)
    Note: Does NOT go to cortex — unconscious processing

TOTAL ROUTE STATISTICS:
- Stations: 7
- Synapses: 4 (Clarke's column, granule cell, Purkinje, deep nuclei)
- Crossing: NONE — ipsilateral throughout
- Final destination: Cerebellar output to brainstem (unconscious motor coordination)
- Approximate time: 15-25 ms (very fast)
- Key feature: Information never reaches consciousness
```

---

### ROUTE C2: Ventral Spinocerebellar Tract (With Double-Crossing)

```
ROUTE: Ventral Spinocerebellar Tract
Signal Types: proprioception_unconscious + spinal interneuron activity (efference copy)
Body Region: Lower body
Direction: Ascending
Fiber Type: Aα
Velocity: 80-120 m/s

STATIONS:

[1-2] PERIPHERAL RECEPTOR → DRG
    Same as C1

[3] SPINAL BORDER CELLS (Laminae V-VII)
    Location: Spinal cord, lateral gray matter
    Operations: TRANSFORM, INTEGRATE
    Delay: 4 ms
    Processing: Integrates proprioception with spinal interneuron activity
    Special: Receives copy of motor commands (efference copy)
    Crossing: YES — axons cross in spinal cord
    → Anterior white commissure

[4] ANTERIOR WHITE COMMISSURE
    Operations: RELAY
    Crossing: FIRST CROSS
    → Ventral spinocerebellar tract (contralateral)

[5] VENTRAL SPINOCEREBELLAR TRACT (Spinal Cord)
    Location: Lateral funiculus, ventral part
    Operations: RELAY
    → Ascends to pons/midbrain

[6] SUPERIOR CEREBELLAR PEDUNCLE
    Location: Pons/Midbrain junction
    Operations: RELAY
    Crossing: SECOND CROSS (crosses back as it enters cerebellum)
    Net result: IPSILATERAL (double-cross = same side)
    → Cerebellar cortex

[7] CEREBELLAR CORTEX
    Operations: TRANSFORM, INTEGRATE
    Delay: 10 ms
    → Deep nuclei

[8] DEEP CEREBELLAR NUCLEI
    Operations: OUTPUT
    Delay: 5 ms
    Function: Compares motor commands with actual movement

TOTAL ROUTE STATISTICS:
- Stations: 8
- Crossings: 2 (net ipsilateral)
- Special feature: Carries efference copy — what the spinal cord "intended" to do
```

---

### ROUTE D: Spinoreticular Tract (Pain → Arousal)

```
ROUTE: Spinoreticular Tract
Signal Types: pain_fast, pain_slow (especially slow)
Body Region: All levels
Direction: Ascending
Fiber Type: Aδ, C
Velocity: 0.5-35 m/s

STATIONS:

[1-3] Same as Spinothalamic (Receptor → DRG → Dorsal Horn)
    Dorsal Horn Operations: TRANSFORM, BRANCH
    Branch: One projection to spinothalamic, one to spinoreticular

[4] ANTERIOR WHITE COMMISSURE
    Crossing: PARTIAL — some crossed, some uncrossed (bilateral projection)

[5] SPINORETICULAR TRACT (Mixed laterality)
    Location: Anterolateral funiculus, mixed with spinothalamic
    → Reticular formation

[6] RETICULAR FORMATION (Medullary and Pontine)
    Location: Core of brainstem tegmentum
    Operations: TRANSFORM, BRANCH, INTEGRATE
    Delay: 5 ms
    Processing:
        - Activates ascending reticular activating system (arousal)
        - Triggers autonomic responses (heart rate, blood pressure)
        - Emotional/motivational components of pain
    Branches:
        - Ascending to intralaminar thalamus
        - Connections to hypothalamus
        - Descending to autonomic centers
    → Intralaminar thalamic nuclei

[7] THALAMUS — Intralaminar Nuclei (CM, Pf)
    Location: Within internal medullary lamina
    Operations: RELAY, BRANCH
    Delay: 5 ms
    Branches:
        - Diffuse projections to cortex (arousal)
        - Projections to striatum
    → Widespread cortex

[8] CEREBRAL CORTEX (Diffuse)
    Location: Widespread cortical areas
    Operations: TERMINATE
    Processing: General arousal, attention to pain
    Note: Less precise localization than spinothalamic-VPL-S1 pathway

TOTAL ROUTE STATISTICS:
- Stations: 8
- Key feature: Does NOT go through VPL — goes through intralaminar nuclei
- Function: Arousal and emotional response, not precise localization
- Clinical: Lesion of VPL abolishes pain localization but not suffering (spinoreticular intact)
```

---

### ROUTE E: Spinotectal Tract (Pain → Orienting)

```
ROUTE: Spinotectal Tract
Signal Types: pain_fast, pain_slow, crude_touch
Body Region: All levels
Direction: Ascending
Fiber Type: Aδ, Aβ

STATIONS:

[1-4] Same as Spinothalamic through crossing

[5] SPINOTECTAL TRACT
    Location: Anterolateral funiculus
    → Superior colliculus

[6] SUPERIOR COLLICULUS
    Location: Midbrain tectum (dorsal)
    Operations: INTEGRATE, OUTPUT
    Delay: 5 ms
    Processing: Integrates with visual and auditory maps
    Output: 
        - Tectospinal tract (head turning)
        - Eye movement commands
        - Tectothalamic to pulvinar
    Function: Orient toward source of painful stimulus

[7] TECTOSPINAL TRACT (Descending response)
    Operations: OUTPUT
    → Cervical spinal cord → neck muscles
    Result: Head turns toward painful stimulus

TOTAL ROUTE STATISTICS:
- Key feature: Bypasses thalamus for rapid orienting
- Function: Reflexive orientation to stimulus location
```

---

### ROUTE F: Spinomesencephalic Tract (Pain → Modulation)

```
ROUTE: Spinomesencephalic Tract
Signal Types: pain_fast, pain_slow
Direction: Ascending
Fiber Type: Aδ, C

STATIONS:

[1-4] Same as Spinothalamic through crossing

[5] SPINOMESENCEPHALIC TRACT
    Location: Anterolateral funiculus
    → Midbrain

[6] PERIAQUEDUCTAL GRAY (PAG)
    Location: Midbrain, around cerebral aqueduct
    Operations: INTEGRATE, OUTPUT
    Delay: 5 ms
    Processing: Central pain modulation center
    Output:
        - Descending to raphe nuclei (serotonin)
        - Descending to locus coeruleus (norepinephrine)
        - Defensive behaviors (freeze, fight, flight)
    → Initiates descending pain modulation

[7] RAPHE MAGNUS (Descending arm)
    Location: Medulla
    Operations: OUTPUT
    Output: Raphespinal tract
    Neurotransmitter: Serotonin
    → Spinal cord dorsal horn

[8] DORSAL HORN (Descending modulation endpoint)
    Location: Spinal cord
    Operations: MODULATE
    Effect: Inhibits pain transmission at entry point
    Mechanism: Presynaptic inhibition of pain afferents

TOTAL ROUTE STATISTICS:
- Key feature: Creates feedback loop — pain activates its own inhibition
- Function: Descending pain modulation (endogenous analgesia)
- Clinical: PAG stimulation produces profound analgesia
```

---

## 4.3 DESCENDING ROUTES

### ROUTE G1: Lateral Corticospinal Tract (Voluntary Movement — Distal)

```
ROUTE: Lateral Corticospinal Tract
Signal Types: motor_voluntary_distal, motor_voluntary_proximal
Body Region: All levels (primarily distal muscles)
Direction: Descending
Fiber Type: Large myelinated (from Betz cells and other Layer V pyramidal)
Velocity: 70-120 m/s

STATIONS:

[1] PRIMARY MOTOR CORTEX (M1) — Precentral Gyrus
    Location: Frontal lobe, Layer V
    Operations: ORIGIN, TRANSFORM
    Delay: 5 ms
    Processing: 
        - Motor command generation from Layer V pyramidal neurons
        - Betz cells for largest/fastest fibers
        - Somatotopic organization (homunculus)
    → Corona radiata

[2] CORONA RADIATA
    Location: White matter, radiating from cortex
    Operations: RELAY
    Delay: 0 ms (passage)
    → Internal capsule

[3] INTERNAL CAPSULE (Posterior Limb)
    Location: Between thalamus and basal ganglia
    Operations: RELAY
    Delay: 0 ms (passage)
    Topography: Face anterior, arm middle, leg posterior
    → Cerebral peduncle

[4] CEREBRAL PEDUNCLE (Crus Cerebri)
    Location: Midbrain, anterior
    Operations: RELAY
    Delay: 0 ms (passage)
    → Basis pontis

[5] BASIS PONTIS
    Location: Pons, anterior
    Operations: RELAY, BRANCH
    Delay: 1 ms
    Branch: Some collaterals to pontine nuclei (for cerebellar copy)
    Note: Fibers scattered among pontine nuclei
    → Medullary pyramid

[6] PYRAMID
    Location: Medulla, anterior surface
    Operations: RELAY
    Delay: 0 ms (passage)
    → Pyramidal decussation

[7] PYRAMIDAL DECUSSATION
    Location: Caudal medulla / cervical junction
    Operations: RELAY
    Crossing: YES — 90% of fibers cross here
    Delay: 0.5 ms
    → Lateral corticospinal tract (contralateral)

[8] LATERAL CORTICOSPINAL TRACT (Spinal Cord)
    Location: Lateral funiculus, dorsal part
    Operations: RELAY
    Delay: 0 ms (passage)
    Course: Descends entire length of cord
    Topography: Cervical fibers medial, sacral fibers lateral
    → Exits at appropriate segment

[9] SPINAL GRAY MATTER (Laminae IV-VII, IX)
    Location: Intermediate zone and ventral horn
    Operations: INTEGRATE (via interneurons) or DIRECT (some direct to motor neurons)
    Delay: 3 ms
    Processing:
        - Most synapse on interneurons first
        - Some (especially for hand) synapse directly on motor neurons
        - Integration with other descending and sensory inputs
    → Motor neurons

[10] ALPHA MOTOR NEURONS (Lamina IX)
    Location: Ventral horn
    Operations: INTEGRATE, OUTPUT
    Delay: 2 ms
    Processing: Final common pathway — integrates all inputs
    → Ventral root

[11] VENTRAL ROOT → Peripheral Nerve
    Operations: RELAY
    Delay: 0 ms (passage)
    → Neuromuscular junction

[12] NEUROMUSCULAR JUNCTION
    Location: Muscle
    Operations: TERMINATE, TRANSFORM (electrical → mechanical)
    Delay: 1 ms (synaptic) + variable (muscle contraction)
    Result: Muscle contraction

TOTAL ROUTE STATISTICS:
- Stations: 12
- Synapses: 2-3 (cortex origin, spinal interneuron or direct, neuromuscular junction)
- Major crossing: Medulla (pyramidal decussation) — 90% of fibers
- Net effect: LEFT motor cortex controls RIGHT body
- Approximate time: 20-30 ms (cortex to muscle activation)
- Key feature: Most direct pathway; enables fine finger movements
```

---

### ROUTE G2: Anterior Corticospinal Tract (Voluntary Movement — Axial)

```
ROUTE: Anterior Corticospinal Tract
Signal Types: motor_voluntary_proximal (axial, bilateral movements)
Body Region: Trunk, proximal limbs (bilateral control)
Direction: Descending
Fiber Type: Large myelinated
Velocity: 70-120 m/s

STATIONS:

[1-6] Same as Lateral Corticospinal (M1 → Pyramid)

[7] PYRAMIDAL DECUSSATION
    Operations: RELAY
    Crossing: NO — 10% of fibers do NOT cross here
    → Anterior corticospinal tract (ipsilateral)

[8] ANTERIOR CORTICOSPINAL TRACT (Spinal Cord)
    Location: Anterior funiculus, near midline
    Operations: RELAY
    Course: Descends to cervical and upper thoracic levels primarily
    → Crosses at segmental level

[9] ANTERIOR WHITE COMMISSURE (Segmental)
    Operations: RELAY
    Crossing: YES — crosses at level of termination
    Delay: 0.5 ms
    → Contralateral ventral horn

[10-12] Same as Lateral Corticospinal (Spinal gray → Motor neuron → Muscle)

TOTAL ROUTE STATISTICS:
- Represents 10% of corticospinal fibers
- Crosses at segmental level rather than medulla
- Controls axial and proximal muscles
- Bilateral projections (some axons send branches to both sides)
- Function: Postural control, bilateral trunk movements
```

---

### ROUTE H: Rubrospinal Tract (Flexor Facilitation)

```
ROUTE: Rubrospinal Tract
Signal Types: motor_voluntary (flexor bias), motor_reflex_modulation
Body Region: Upper limbs primarily
Direction: Descending
Fiber Type: Large myelinated
Velocity: 50-80 m/s

STATIONS:

[1] RED NUCLEUS
    Location: Midbrain tegmentum
    Operations: ORIGIN, INTEGRATE
    Delay: 3 ms
    Input from: Motor cortex, cerebellum (interposed nuclei)
    Function: Integrates cortical and cerebellar motor signals
    → Ventral tegmental decussation

[2] VENTRAL TEGMENTAL DECUSSATION
    Location: Midbrain
    Operations: RELAY
    Crossing: YES — crosses immediately
    Delay: 0.5 ms
    → Rubrospinal tract

[3] RUBROSPINAL TRACT (Brainstem)
    Location: Lateral brainstem tegmentum
    Operations: RELAY
    → Spinal cord

[4] RUBROSPINAL TRACT (Spinal Cord)
    Location: Lateral funiculus, ventral to lateral corticospinal
    Operations: RELAY
    Course: Primarily to cervical and upper thoracic levels
    → Spinal gray

[5] SPINAL GRAY MATTER (Laminae V-VII)
    Location: Intermediate zone
    Operations: INTEGRATE
    Delay: 3 ms
    Processing: Facilitates flexor motor neurons, inhibits extensors
    → Motor neurons

[6-7] Same as Corticospinal (Motor neurons → Muscle)

TOTAL ROUTE STATISTICS:
- Stations: 7
- Major crossing: Midbrain (ventral tegmental decussation)
- Function: Flexor facilitation; backup to corticospinal for arm movements
- Clinical: Less important in humans than other mammals
```

---

### ROUTE I1: Pontine Reticulospinal Tract (Extensor Facilitation)

```
ROUTE: Pontine (Medial) Reticulospinal Tract
Signal Types: motor_postural (extensor/antigravity)
Body Region: Axial and proximal limb muscles
Direction: Descending
Fiber Type: Medium myelinated
Velocity: 50-70 m/s

STATIONS:

[1] PONTINE RETICULAR FORMATION
    Location: Pons, medial tegmentum (nucleus reticularis pontis caudalis/oralis)
    Operations: ORIGIN, INTEGRATE
    Delay: 3 ms
    Input from: Motor cortex, vestibular nuclei, sensory systems
    Function: Integrates postural commands
    Crossing: NO
    → Pontine reticulospinal tract

[2] PONTINE RETICULOSPINAL TRACT (Brainstem)
    Location: Medial brainstem
    Operations: RELAY
    → Spinal cord

[3] PONTINE RETICULOSPINAL TRACT (Spinal Cord)
    Location: Anterior funiculus, near midline
    Operations: RELAY
    Course: Descends entire length of cord, ipsilaterally
    Crossing: NONE — ipsilateral throughout
    → Spinal gray

[4] SPINAL GRAY MATTER (Laminae VII, VIII)
    Location: Medial ventral horn
    Operations: INTEGRATE
    Delay: 3 ms
    Processing: Facilitates extensor (antigravity) motor neurons
    → Motor neurons for axial and proximal muscles

[5-6] Motor neurons → Muscle

TOTAL ROUTE STATISTICS:
- Stations: 6
- Crossing: NONE — ipsilateral
- Function: Facilitates extensors; maintains upright posture against gravity
- Clinical: Damage causes hypotonia (reduced muscle tone)
```

---

### ROUTE I2: Medullary Reticulospinal Tract (Flexor Facilitation / Extensor Inhibition)

```
ROUTE: Medullary (Lateral) Reticulospinal Tract
Signal Types: motor_postural (flexor bias), motor_reflex_modulation
Body Region: All levels
Direction: Descending
Fiber Type: Medium myelinated
Velocity: 40-60 m/s

STATIONS:

[1] MEDULLARY RETICULAR FORMATION
    Location: Medulla, ventromedial (nucleus reticularis gigantocellularis)
    Operations: ORIGIN, INTEGRATE
    Delay: 3 ms
    Input from: Motor cortex, sensory systems
    Crossing: Variable — mostly ipsilateral with some bilateral
    → Medullary reticulospinal tract

[2-3] Tract through brainstem and spinal cord (lateral funiculus)

[4] SPINAL GRAY MATTER
    Operations: INTEGRATE
    Processing: Inhibits extensors, facilitates flexors
    Opposite effect to pontine reticulospinal

TOTAL ROUTE STATISTICS:
- Crossing: Mostly ipsilateral with some bilateral
- Function: Opposes pontine reticulospinal; enables voluntary movement
- Balance: Pontine (extensors) vs. Medullary (flexors) maintains postural tone
```

---

### ROUTE J1: Lateral Vestibulospinal Tract (Balance — Extensor)

```
ROUTE: Lateral Vestibulospinal Tract
Signal Types: motor_balance (extensor facilitation)
Body Region: All levels (especially lower limb extensors)
Direction: Descending
Fiber Type: Large myelinated
Velocity: 60-80 m/s

STATIONS:

[1] LATERAL VESTIBULAR NUCLEUS (Deiters' Nucleus)
    Location: Pontomedullary junction
    Operations: ORIGIN, INTEGRATE
    Delay: 3 ms
    Input from: 
        - Vestibular nerve (otolith organs — linear acceleration, gravity)
        - Cerebellum (fastigial nucleus)
        - Proprioceptive inputs
    Function: Processes balance/gravity information
    Crossing: NO
    → Lateral vestibulospinal tract

[2] LATERAL VESTIBULOSPINAL TRACT (Brainstem)
    Location: Lateral brainstem
    Operations: RELAY
    → Spinal cord

[3] LATERAL VESTIBULOSPINAL TRACT (Spinal Cord)
    Location: Anterior funiculus
    Operations: RELAY
    Course: Descends entire length of cord, ipsilaterally
    Crossing: NONE
    → Spinal gray

[4] SPINAL GRAY MATTER (Laminae VII, VIII)
    Operations: INTEGRATE
    Delay: 3 ms
    Processing: 
        - POWERFUL facilitation of extensor motor neurons
        - Inhibition of flexors
        - Mediates righting reflexes
    → Motor neurons

TOTAL ROUTE STATISTICS:
- Stations: 5
- Crossing: NONE — ipsilateral
- Function: Most powerful facilitator of extensors; anti-gravity, righting reflexes
- Trigger: Responds to head tilt (gravity via otoliths)
- Clinical: Damage causes postural instability
```

---

### ROUTE J2: Medial Vestibulospinal Tract (Head/Neck Stabilization)

```
ROUTE: Medial Vestibulospinal Tract
Signal Types: motor_balance (head/neck control)
Body Region: Cervical (neck muscles only)
Direction: Descending
Fiber Type: Medium myelinated
Velocity: 50-70 m/s

STATIONS:

[1] MEDIAL VESTIBULAR NUCLEUS
    Location: Pontomedullary junction
    Operations: ORIGIN, INTEGRATE
    Delay: 3 ms
    Input from: Semicircular canals (angular acceleration, head rotation)
    Function: Detects head rotation
    Crossing: BILATERAL (projects to both sides)
    → Medial vestibulospinal tract (within MLF)

[2] MEDIAL LONGITUDINAL FASCICULUS (Descending portion)
    Location: Near midline, ventral brainstem
    Operations: RELAY
    → Cervical spinal cord only

[3] MEDIAL VESTIBULOSPINAL TRACT (Cervical Spinal Cord)
    Location: Anterior funiculus
    Operations: RELAY
    Limit: Only descends to cervical and upper thoracic levels
    → Cervical ventral horn

[4] CERVICAL MOTOR NEURONS
    Operations: INTEGRATE, OUTPUT
    Function: Controls neck muscles for vestibulocollic reflex
    Reflex: Stabilizes head during body movement

TOTAL ROUTE STATISTICS:
- Stations: 4
- Crossing: BILATERAL
- Range: Cervical only (does not descend to trunk or limbs)
- Function: Vestibulocollic reflex (head stabilization during body movement)
- Works with: VOR (vestibulo-ocular reflex) to stabilize gaze
```

---

### ROUTE K: Tectospinal Tract (Visual Orienting)

```
ROUTE: Tectospinal Tract
Signal Types: motor_voluntary (head turning toward stimulus)
Body Region: Cervical (neck muscles)
Direction: Descending
Fiber Type: Medium myelinated
Velocity: 50-70 m/s

STATIONS:

[1] SUPERIOR COLLICULUS
    Location: Midbrain tectum (roof)
    Operations: ORIGIN, INTEGRATE
    Delay: 5 ms
    Input from:
        - Retina (direct visual input)
        - Visual cortex
        - Auditory (inferior colliculus)
        - Somatosensory (spinotectal)
    Processing: Multimodal integration; creates spatial map of environment
    → Dorsal tegmental decussation

[2] DORSAL TEGMENTAL DECUSSATION
    Location: Midbrain
    Operations: RELAY
    Crossing: YES
    Delay: 0.5 ms
    → Tectospinal tract (contralateral)

[3] TECTOSPINAL TRACT (Brainstem → Cervical Cord)
    Location: Anterior funiculus
    Operations: RELAY
    Limit: Only descends to cervical levels
    → Cervical ventral horn

[4] CERVICAL MOTOR NEURONS
    Operations: OUTPUT
    Function: Turns head toward visual/auditory stimulus

TOTAL ROUTE STATISTICS:
- Stations: 4
- Major crossing: Midbrain (dorsal tegmental decussation)
- Range: Cervical only
- Function: Orienting head toward sudden stimuli
- Speed: Fast (short pathway, rapid orienting response)
```

---

### ROUTE L: Hypothalamospinal Tract (Autonomic Control)

```
ROUTE: Hypothalamospinal Tract
Signal Types: autonomic_sympathetic, autonomic_parasympathetic
Body Region: All levels (to autonomic preganglionic neurons)
Direction: Descending
Fiber Type: Small myelinated (B) and unmyelinated (C)
Velocity: 3-15 m/s

STATIONS:

[1] HYPOTHALAMUS
    Location: Diencephalon, below thalamus
    Operations: ORIGIN, INTEGRATE
    Delay: 5 ms
    Nuclei involved: Paraventricular, lateral hypothalamus, posterior hypothalamus
    Input from: Limbic system, cortex, brainstem
    Function: Central autonomic control center
    → Descending autonomic fibers

[2] BRAINSTEM AUTONOMIC CENTERS
    Location: Midbrain, pons, medulla
    Operations: RELAY, INTEGRATE
    Delay: 3 ms
    Processing: Integration with brainstem autonomic reflexes
    → Hypothalamospinal tract

[3] HYPOTHALAMOSPINAL TRACT (Spinal Cord)
    Location: Lateral funiculus, near lateral horn
    Operations: RELAY
    Crossing: Mostly IPSILATERAL
    → Intermediolateral cell column

[4] INTERMEDIOLATERAL CELL COLUMN (T1-L2 for Sympathetic)
    Location: Lateral horn (only present T1-L2)
    Operations: INTEGRATE, OUTPUT
    Delay: 3 ms
    Neurons: Preganglionic sympathetic
    → Ventral root → Sympathetic chain ganglia

[5] SACRAL PARASYMPATHETIC NUCLEI (S2-S4)
    Location: Lateral gray matter
    Operations: INTEGRATE, OUTPUT
    Neurons: Preganglionic parasympathetic (for bladder, bowel, sexual function)
    → Ventral root → Pelvic ganglia

TOTAL ROUTE STATISTICS:
- Stations: 5
- Crossing: Mostly ipsilateral
- Function: Central control of sympathetic and parasympathetic outflow
- Clinical: Lesion causes Horner syndrome (ipsilateral ptosis, miosis, anhidrosis)
```

---

## 4.4 REFLEX ARC SPECIFICATIONS

### REFLEX R1: Monosynaptic Stretch Reflex (Knee-Jerk)

```
REFLEX: Monosynaptic Stretch Reflex
Trigger Type: proprioception_conscious (muscle spindle Ia afferent)
Threshold: Low (slight stretch sufficient)
Circuit Type: Monosynaptic
Latency: 20-25 ms

CIRCUIT:

[1] MUSCLE SPINDLE
    Location: Within muscle (e.g., quadriceps)
    Trigger: Muscle stretch (e.g., patellar tendon tap)
    Output: Ia afferent fiber fires
    → Dorsal root

[2] DORSAL ROOT → VENTRAL HORN (Direct)
    Course: Ia afferent enters dorsal horn, passes through gray matter
    Synapse: DIRECT monosynaptic connection to alpha motor neuron
    NO interneurons
    Delay: 0.5 ms (single synapse)
    → Alpha motor neuron

[3] ALPHA MOTOR NEURON (Same muscle)
    Location: Ventral horn
    Operations: INTEGRATE (but minimal processing), OUTPUT
    Delay: 1 ms
    → Ventral root

[4] NEUROMUSCULAR JUNCTION
    Delay: 1 ms
    Result: Muscle contracts (quadriceps contracts, leg kicks)

PARALLEL CIRCUITS:

[A] RECIPROCAL INHIBITION (via Ia Inhibitory Interneuron)
    Same Ia afferent → Ia inhibitory interneuron → Antagonist motor neuron (inhibited)
    Result: Antagonist (hamstrings) relaxes
    Latency: Add 1-2 ms for interneuron

[B] ASCENDING SIGNAL
    Same Ia afferent → ALSO sends collateral up dorsal column
    Signal continues to cortex (conscious perception of stretch)
    Does NOT interfere with reflex

TOTAL REFLEX STATISTICS:
- Synapses in reflex arc: 1 (monosynaptic)
- Latency: 20-25 ms total (includes peripheral conduction)
- Components: Muscle spindle → Ia afferent → alpha motor neuron → muscle
- Parallel: Reciprocal inhibition of antagonist
- Signal continues: YES — conscious perception follows reflex
```

---

### REFLEX R2: Withdrawal (Flexor) Reflex

```
REFLEX: Withdrawal Reflex
Trigger Type: pain_fast, pain_slow (above threshold)
Threshold: Moderate-High (must be noxious)
Circuit Type: Polysynaptic
Latency: 30-50 ms

CIRCUIT:

[1] NOCICEPTOR (Free Nerve Ending)
    Location: Skin, deep tissue
    Trigger: Painful stimulus (heat, sharp object, chemical)
    Threshold check: Intensity must exceed threshold
    → Aδ or C fiber to spinal cord

[2] DORSAL HORN (Laminae I, II, V)
    Operations: TRANSFORM, INTEGRATE, BRANCH
    Delay: 5 ms
    Processing:
        - Multiple interneurons engaged
        - Pattern generation for coordinated withdrawal
    Branches:
        - Local reflex circuit
        - Ascending spinothalamic (parallel)
    → Interneuron pool

[3] INTERNEURON POOL (Polysynaptic Chain)
    Location: Intermediate zone (Laminae V-VII)
    Operations: INTEGRATE
    Delay: 5-10 ms (multiple synapses)
    Processing:
        - Excitatory interneurons to flexor motor neurons
        - Inhibitory interneurons to extensor motor neurons
        - Pattern determines which flexors, how strongly
    → Flexor motor neurons

[4] FLEXOR MOTOR NEURONS
    Operations: INTEGRATE, OUTPUT
    Delay: 2 ms
    Output: Activation of flexor muscles in affected limb
    → Muscles (e.g., hip flexors, knee flexors, ankle dorsiflexors)

[5] FLEXOR MUSCLES
    Response: Withdrawal of limb from stimulus

PARALLEL PATHWAYS:

[A] RECIPROCAL INHIBITION
    Same circuit inhibits extensors in same limb
    Limb flexes cleanly without extensor resistance

[B] CROSSED EXTENSOR REFLEX (see R3)
    Engages opposite limb for balance

[C] ASCENDING PATHWAY (Spinothalamic)
    Continues to brain in parallel
    Conscious perception of pain follows withdrawal

TOTAL REFLEX STATISTICS:
- Synapses in reflex arc: 3-5 (polysynaptic)
- Latency: 30-50 ms
- Pattern: Flexion of affected limb
- Signal continues: YES — pain perceived after withdrawal
```

---

### REFLEX R3: Crossed Extensor Reflex

```
REFLEX: Crossed Extensor Reflex
Trigger Type: Same as withdrawal (pain)
Circuit Type: Polysynaptic
Latency: 35-55 ms (slightly longer than withdrawal)

CIRCUIT:

[1-2] Same as Withdrawal Reflex (Nociceptor → Dorsal Horn)

[3] INTERNEURON POOL (Commissural Projection)
    Processing: Some interneurons project across midline
    Course: Axons cross via anterior white commissure
    → Contralateral interneurons and motor neurons

[4] CONTRALATERAL EXTENSOR MOTOR NEURONS
    Operations: INTEGRATE, OUTPUT
    Processing: Facilitation of extensors in opposite limb
    → Extensor muscles (opposite limb)

[5] CONTRALATERAL EXTENSOR MUSCLES
    Response: Opposite limb extends to support body weight

PURPOSE:
- When you lift one foot due to pain, the other leg must support you
- Automatic postural compensation
- Enables maintained balance during withdrawal

TOTAL REFLEX STATISTICS:
- Always accompanies withdrawal reflex
- Latency slightly longer (adds crossing time)
- Function: Postural support during withdrawal
```

---

### REFLEX R4: Golgi Tendon Reflex (Autogenic Inhibition)

```
REFLEX: Golgi Tendon Reflex
Trigger Type: proprioception (Ib afferent from Golgi tendon organ)
Threshold: High tension in tendon
Circuit Type: Polysynaptic
Latency: 30-35 ms

CIRCUIT:

[1] GOLGI TENDON ORGAN
    Location: Muscle-tendon junction
    Trigger: High tension in tendon (strong contraction or stretch)
    → Ib afferent fiber

[2] DORSAL HORN → INTERNEURONS
    Synapse: Ib afferent → Ib inhibitory interneuron
    Processing: Interposes inhibitory interneuron

[3] Ib INHIBITORY INTERNEURON
    Operations: INTEGRATE
    Output: Inhibits motor neuron of SAME muscle
    → Alpha motor neuron (inhibited)

[4] ALPHA MOTOR NEURON (Inhibited)
    Response: Reduced firing → muscle relaxes

PURPOSE:
- Protective reflex prevents muscle/tendon damage from excessive force
- "Clasp-knife" response — sudden relaxation under high load
- Inverse of stretch reflex (stretch reflex excites, Golgi inhibits)

TOTAL REFLEX STATISTICS:
- Synapses: 2 (disynaptic)
- Latency: 30-35 ms
- Function: Protective relaxation under high tension
```

---

## 4.5 TIMING REFERENCE TABLES

### Conduction Velocity by Fiber Type

| Fiber | Diameter | Velocity | Signal Types |
|-------|----------|----------|--------------|
| Aα | 13-20 μm | 80-120 m/s | Proprioception (Ia, Ib), Motor (α) |
| Aβ | 6-12 μm | 35-75 m/s | Touch, pressure (II) |
| Aγ | 3-6 μm | 15-35 m/s | Motor to muscle spindles (γ) |
| Aδ | 1-5 μm | 5-35 m/s | Fast pain, cold, touch |
| B | 1-3 μm | 3-15 m/s | Autonomic preganglionic |
| C | 0.2-1.5 μm | 0.5-2 m/s | Slow pain, warm, itch, autonomic postganglionic |

### Synaptic Delays

| Synapse Type | Delay |
|--------------|-------|
| Fast chemical (glutamate, GABA) | 0.5-1 ms |
| Slow chemical (modulatory) | 1-5 ms |
| Electrical (gap junction) | <0.1 ms |
| Neuromuscular junction | 0.5-1 ms |

### Total Transit Time Examples

| Signal | Route | Distance | Velocity | Synapses | Total Time |
|--------|-------|----------|----------|----------|------------|
| Fine touch (hand) | DCML | 0.8 m | 60 m/s | 3 | ~25 ms |
| Fine touch (foot) | DCML | 1.5 m | 60 m/s | 3 | ~40 ms |
| Fast pain (hand) | Spinothalamic | 0.8 m | 15 m/s | 3 | ~70 ms |
| Fast pain (foot) | Spinothalamic | 1.5 m | 15 m/s | 3 | ~120 ms |
| Slow pain (hand) | Spinothalamic | 0.8 m | 1 m/s | 3 | ~820 ms |
| Slow pain (foot) | Spinothalamic | 1.5 m | 1 m/s | 3 | ~1520 ms |
| Motor command (hand) | Corticospinal | 0.8 m | 100 m/s | 2 | ~15 ms |
| Motor command (foot) | Corticospinal | 1.5 m | 100 m/s | 2 | ~25 ms |
| Withdrawal reflex | Local | 0.1 m | 15 m/s | 4 | ~40 ms |

---

# PART 5: INTEGRATION POINTS

## 5.1 Ascending Integration (To Higher Structures)

### Thalamic Destinations

| Thalamic Nucleus | Receives From | Projects To | Signal Types |
|------------------|---------------|-------------|--------------|
| VPL | Medial lemniscus, Spinothalamic | S1 (body) | Touch, pain, temperature, proprioception |
| VPM | Trigeminal lemniscus | S1 (face) | Face sensation |
| MGN | Inferior colliculus | A1 | Auditory |
| LGN | Optic tract | V1 | Visual |
| VA | Basal ganglia | Motor/Prefrontal | Motor selection |
| VL | Cerebellum, Basal ganglia | Motor cortex | Motor coordination |
| MD | Amygdala, Prefrontal | Prefrontal | Emotion, executive |
| Intralaminar | Reticular formation, Spinoreticular | Diffuse cortex, Striatum | Arousal |
| Pulvinar | Superior colliculus, Cortex | Parietal, Visual | Attention |

### Cerebellar Entry Points

| Peduncle | Carries | From |
|----------|---------|------|
| Inferior (Restiform) | Spinocerebellar, Olivocerebellar, Vestibulocerebellar | Spinal cord, Olive, Vestibular |
| Middle (Brachium Pontis) | Pontocerebellar | Pontine nuclei ← Cortex |
| Superior (Brachium Conjunctivum) | Ventral spinocerebellar (input), Cerebellar output | Spinal cord |

## 5.2 Descending Integration (From Higher Structures)

### Motor Cortex Entry Point

| Structure | Entry Point | Highway |
|-----------|-------------|---------|
| Motor cortex Layer V | Corona radiata | Corticospinal, Corticobulbar |
| Premotor cortex | Corona radiata | Corticopontine, Corticoreticular |
| Prefrontal cortex | Corona radiata | Corticopontine |

### Cerebellar Exit Point

| Nucleus | Exit Via | To | Then |
|---------|----------|-----|------|
| Dentate | Superior cerebellar peduncle | VL thalamus | Motor cortex |
| Interposed | Superior cerebellar peduncle | Red nucleus, VL thalamus | Rubrospinal, Motor cortex |
| Fastigial | Inferior cerebellar peduncle | Vestibular nuclei, Reticular formation | Vestibulospinal, Reticulospinal |

### Basal Ganglia Exit Point

| Nucleus | Projects To | Effect |
|---------|-------------|--------|
| GPi | VA/VL thalamus | Releases or maintains inhibition |
| SNr | VA thalamus, Superior colliculus | Motor selection, Eye movements |

## 5.3 Interface Contracts

Each integration point defines:

```
INTERFACE: [Name]
Accepts Signal Types: [list]
Entry Operation: [what happens when signal arrives]
Laterality Rule: [how laterality is handled]
Next Station: [where signal goes after crossing interface]
Timing: [any additional delays at interface]
```

Example:

```
INTERFACE: Thalamus_VPL_Entry
Accepts Signal Types: fine_touch, proprioception_conscious, pain_*, temperature_*
Entry Operation: RELAY, MODULATE, GATE
Laterality Rule: Maintains — signal already crossed in medulla or spinal cord
Next Station: S1_cortex (via posterior limb internal capsule)
Timing: 5 ms processing delay
Modulation: Subject to TRN gating, cortical feedback, arousal state
```

---

# PART 6: SUMMARY

## What This Model Captures

**Structural routing**: Signal type determines pathway. A pain signal takes the spinothalamic tract because that's how pain neurons are wired — not because of a routing decision.

**Anatomical fidelity**: Every highway and station corresponds to real anatomical structures with their actual names and properties.

**Mandatory hierarchy**: All signals traverse spinal cord → brainstem → thalamus → cortex. No shortcuts exist.

**Crossing logic**: Different pathways cross at different levels (spinal cord, medulla, midbrain), explicitly tracked.

**Local processing**: Reflex arcs handle time-critical responses locally while signals continue ascending in parallel.

**Timing fidelity**: Conduction velocities range from 0.5 m/s (C fibers) to 120 m/s (Aα fibers). Synaptic delays add 0.5-5 ms per synapse. Total transit times are realistic.

**Parallel pathways**: Same information travels multiple routes simultaneously (spinothalamic + spinoreticular + spinotectal for pain).

**Collateral branching**: Single pathways branch to send copies to multiple destinations (pain → VPL + reticular formation + PAG + superior colliculus).

**Integration hooks**: Defined interfaces for connecting cerebrum and cerebellum routing systems when implemented.

## Implementation Roadmap

**Phase 1 (This Document)**: Complete conceptual model with all spinal cord and brainstem routes specified.

**Phase 2**: Add cerebrum routes (cortical, subcortical, basal ganglia loops) connecting at defined thalamic and cortical interface points.

**Phase 3**: Add cerebellum routes (peduncle inputs, cerebellar cortex processing, deep nuclei outputs) connecting at defined peduncle and thalamic interface points.

**Phase 4**: Integrate all three systems into unified routing substrate where any signal can be traced from origin to destination through the complete CNS hierarchy.

---

*Document Version 1.0 — Spinal Cord and Brainstem Routes Complete*
*Next: Cerebrum and Cerebellum Route Specifications*
