# Thalamus Architecture

This document consolidates the current thalamus design for brain-mimc, synthesized from knowledge base research and reference documents.

**Status:** Design Phase (not yet implemented)
**Last Updated:** 2026-01-11

---

## Table of Contents

1. [Core Insight](#core-insight)
2. [Emergent Integration (No Central Controller)](#emergent-integration-no-central-controller)
3. [Anatomical Structure](#anatomical-structure)
4. [Nucleus Classification](#nucleus-classification)
5. [TRN (Gatekeeper)](#trn-gatekeeper)
6. [Driver vs Modulator](#driver-vs-modulator)
7. [Cortical Layer Connections](#cortical-layer-connections)
8. [The 6 Major Loops](#the-6-major-loops)
9. [Multi-Input Nuclei](#multi-input-nuclei)
10. [Cross-Loop Communication](#cross-loop-communication)
11. [Challenges](#challenges)
12. [Software Architecture](#software-architecture)

---

## Core Insight

```
THALAMUS = Message Broker + Router + Gatekeeper + Synchronizer

It's NOT just a relay.
It's a FRAMEWORK for managing concurrent, independent modules.
```

The thalamus is the central hub for Loops A, B, C, and E. Nearly all information going to cortex passes through thalamus (except olfaction).

---

## Emergent Integration (No Central Controller)

**The brain has NO central controller.** Integration EMERGES from architecture.

### The Five Integration Mechanisms

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION MECHANISMS                              │
│                                                                             │
│   1. CONVERGENCE         Multiple inputs → single node → must integrate    │
│                                                                             │
│   2. COMPETITION         Winner-take-all → only one output                 │
│                                                                             │
│   3. SYNCHRONIZATION     Same timing → same object/event                   │
│                                                                             │
│   4. GLOBAL STATE        Neuromodulators set mode for EVERYTHING           │
│                                                                             │
│   5. SHARED STRUCTURES   Thalamus, Striatum = hubs where loops MEET        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                            GLOBAL STATE LAYER                               │
│                      (Neuromodulators — affects ALL)                        │
│                                                                             │
│   DOPAMINE ─────┬─────────────────────────────────────────────────────      │
│   ACh ──────────┼─────────────────────────────────────────────────────      │
│   NE ───────────┼─────────────────────────────────────────────────────      │
│   5-HT ─────────┴─────────────────────────────────────────────────────      │
│                 │                                                           │
│                 ↓ BROADCASTS TO EVERYTHING                                  │
│                                                                             │
│   ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│                           CONVERGENCE LAYER                                 │
│                    (Where loops MEET and INTEGRATE)                         │
│                                                                             │
│                          ┌─────────────────┐                                │
│        ┌─────────────────┤    THALAMUS     ├─────────────────┐              │
│        │                 │   (MAIN HUB)    │                 │              │
│        ↓                 └────────┬────────┘                 ↓              │
│   ┌─────────┐                     │                    ┌─────────┐          │
│   │STRIATUM │←───────────────────→│←──────────────────→│AMYGDALA │          │
│   │(action) │                     ↓                    │(emotion)│          │
│   └─────────┘              ┌─────────────┐             └─────────┘          │
│                            │ HIPPOCAMPUS │                                  │
│                            │  (memory)   │                                  │
│                            └─────────────┘                                  │
│                                                                             │
│   ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│                              LOOP LAYER                                     │
│                  (Independent loops, connected via hubs)                    │
│                                                                             │
│   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│   │ LOOP 1 │ │ LOOP 2 │ │ LOOP 3 │ │ LOOP 4 │ │ LOOP 5 │ │ LOOP 6 │        │
│   │cerebel.│ │ basal  │ │ papez  │ │hipp-pfc│ │arousal │ │emotion │        │
│   │ timing │ │ select │ │ memory │ │planning│ │ state  │ │salience│        │
│   └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
│        └────────┴────────┴────────┴────────┴────────┘                      │
│                              │                                              │
│                              ↓                                              │
│                   ALL CONNECT THROUGH HUBS                                  │
│                                                                             │
│   ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│                            CORTEX LAYER                                     │
│                    (Distributed processing areas)                           │
│                                                                             │
│   M1 ←→ PreM ←→ PFC ←→ V1 ←→ V2 ←→ V4 ←→ MT ←→ Parietal ←→ Temporal        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Competition Types

| Structure | Competition Type | Losers Get | Why |
|-----------|------------------|------------|-----|
| **TRN** | GRADED | Reduced (not zero) | Can perceive multiple modalities |
| **Basal Ganglia** | BINARY | Nothing (blocked) | Can only DO one action |

### Global State (Neuromodulators)

| State | ACh | DA | NE | Result |
|-------|-----|----|----|--------|
| Alert/Focused | HIGH | MED | MED | Tonic, detailed, engaged |
| Reward-seeking | MED | HIGH | MED | Motivated, action-oriented |
| Threat/Stress | HIGH | LOW | HIGH | Hypervigilant, reactive |
| Drowsy | LOW | LOW | LOW | Burst mode, less responsive |
| Sleep (NREM) | V.LOW | V.LOW | V.LOW | Disconnected, consolidating |

### The City Analogy

```
THE KEY INSIGHT:
═══════════════

There is NO central controller.

Integration EMERGES from:
• Shared structures that FORCE combination
• Competition that FORCES selection
• Timing that FORCES binding
• Global state that FORCES coherent mode


IT'S LIKE:
══════════

• Not a CPU with a program
• More like a city with traffic patterns
• Roads (pathways) are fixed
• Traffic lights (TRN) control flow
• Weather (neuromodulators) affects everything
• Intersections (hubs) force integration
• Rush hour patterns (synchronization) emerge
```

---

## Anatomical Structure

### Location and Organization

- Two egg-shaped masses at the center of the brain
- ~60 distinct nuclei + TRN (shell around it)
- Organized into anatomical subdivisions:

| Subdivision | Key Nuclei | Primary Function |
|-------------|------------|------------------|
| **Anterior** | AN, LD | Memory (Papez circuit) |
| **Medial** | MD | Executive, emotion |
| **Lateral** | VL, VA, VPL, VPM, LGN, MGN | Motor, sensory relay |
| **Intralaminar** | CM, Pf, CL | Arousal, attention |
| **Midline** | PVT, Reuniens | Limbic integration |
| **Posterior** | Pulvinar, LP | Higher-order visual |
| **Reticular** | TRN | Gating (inhibitory shell) |

### Diagram

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                      THALAMUS                           │
                    │                                                         │
                    │   ┌───────────────────────────────────────────────────┐ │
                    │   │                   TRN (Shell)                     │ │
                    │   │   Wraps around, gates ALL relay nuclei            │ │
                    │   │                                                   │ │
                    │   │   ┌───────────────────────────────────────────┐   │ │
                    │   │   │                                           │   │ │
                    │   │   │              RELAY NUCLEI (~60)           │   │ │
                    │   │   │                                           │   │ │
                    │   │   │  First-Order: LGN, MGN, VPL, VPM, VA, VL  │   │ │
                    │   │   │  Higher-Order: Pulvinar, MD, LP, LD       │   │ │
                    │   │   │  Diffuse: CM, Pf, CL, PVT                 │   │ │
                    │   │   │  Limbic: AN, Reuniens                     │   │ │
                    │   │   │                                           │   │ │
                    │   │   └───────────────────────────────────────────┘   │ │
                    │   │                                                   │ │
                    │   └───────────────────────────────────────────────────┘ │
                    │                                                         │
                    └─────────────────────────────────────────────────────────┘
```

---

## Nucleus Classification

### By Order (Sherman Framework)

| Class | Examples | Driver Input From | Projects To | Function |
|-------|----------|-------------------|-------------|----------|
| **First-Order** | LGN, MGN, VPL/VPM, VA, VL | Subcortical (retina, cochlea, spinal cord, BG, cerebellum) | Primary cortex L4 | Relay external world |
| **Higher-Order** | Pulvinar, MD, LP/LD | Cortex Layer V | Association cortex | Cortex-to-cortex routing (transthalamic) |
| **Diffuse** | CM, Pf, CL, PVT | Brainstem, hypothalamus | Widespread cortex L1 + Striatum | Arousal, global state |
| **Gate** | TRN | Collaterals from all nuclei + cortex L6 | Inhibits relay nuclei | Attention gating |

### By Modality/Function

| Function | Nucleus | Input | Output |
|----------|---------|-------|--------|
| Vision | LGN | Retina | V1 |
| Audition | MGN | Inferior colliculus | A1 |
| Somatosensory | VPL (body), VPM (face) | Spinal cord, trigeminal | S1 |
| Motor | VA, VL | Basal ganglia, cerebellum | Motor cortex |
| Executive | MD | Amygdala, BG, PFC L5 | PFC |
| Visual integration | Pulvinar | V1 L5, SC, parietal, temporal | Visual association areas |
| Memory | AN | Mammillary bodies | Cingulate |
| Memory-executive | Reuniens | Hippocampus, mPFC | mPFC, Hippocampus (bidirectional!) |
| Arousal | CM, Pf, CL | Brainstem reticular formation | Broad cortex + striatum |

---

## TRN (Gatekeeper)

The TRN is a thin shell of GABAergic neurons that wraps around the thalamus. It does NOT relay to cortex - it INHIBITS relay nuclei.

### Organization

TRN is organized by **MODALITY**, not per-nucleus:

| Sector | Gates | Location |
|--------|-------|----------|
| **Visual** | LGN + related visual nuclei | Caudal-lateral |
| **Auditory** | MGN | Caudal |
| **Somatosensory** | VPL, VPM | Middle |
| **Motor** | VA, VL | Rostral-lateral |
| **Limbic** | MD, AN, midline nuclei | Rostral-medial |

### TRN Heterogeneity (Cho et al. 2025)

| Property | Sensory TRN (Caudal) | Limbic TRN (Rostral) |
|----------|---------------------|----------------------|
| CaV3.3 expression | Higher | Lower |
| Burst firing | Stronger | Weaker |
| Sleep spindles | More | Fewer |
| Function | Controls sleep fragmentation | Controls sleep duration |

### Inputs to TRN

1. **Collaterals from thalamic relay outputs** (what's flowing)
2. **Collaterals from cortex Layer VI** (feedback modulation)
3. **Direct from frontal cortex Layer V** (UNIQUE - Hádinger 2022)
4. **GPe (basal ganglia)** (dual inhibition)
5. **Intra-TRN connections** (lateral inhibition between sectors)

### Gating Modes

| Mode | TRN Activity | Gate State | Communication Pattern |
|------|--------------|------------|----------------------|
| **TONIC** | Low (graded) | ~80% open | Near-continuous, rate-coded |
| **PARTIAL** | Medium | ~40% open | Reduced throughput |
| **BURST** | High (oscillatory 7-14 Hz) | ~10% open | Rhythmic packets, salience detection |

### TRN Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         TRN (GATEKEEPER)                        │
│                                                                 │
│   INPUTS:                                                       │
│   ├── Collaterals from ALL relay outputs (what's flowing)       │
│   ├── Collaterals from cortex L6 (what consumer wants)          │
│   ├── Direct from frontal L5 (unique executive control)         │
│   └── Control signals from attention controller                 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      SECTORS                            │   │
│   │                                                         │   │
│   │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐│   │
│   │   │ VISUAL │←→│AUDITORY│←→│ SOMATO │←→│ MOTOR │←→│LIMBIC ││   │
│   │   │        │  │        │  │        │  │       │  │       ││   │
│   │   │ gates  │  │ gates  │  │ gates  │  │ gates │  │ gates ││   │
│   │   │ LGN    │  │ MGN    │  │VPL/VPM │  │ VA/VL │  │ MD/AN ││   │
│   │   └────────┘  └────────┘  └────────┘  └───────┘  └───────┘│   │
│   │                                                         │   │
│   │   ←→ = lateral inhibition (compete for priority)        │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   OUTPUTS:                                                      │
│   └── Gate control signals to each relay module                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Driver vs Modulator

Every thalamic relay neuron receives two types of input:

| Type | Percentage | Synapses | Function | Source |
|------|------------|----------|----------|--------|
| **Driver** | 5-10% | Large, proximal | Content - "what happened" | Subcortical (FO) or Cortex L5 (HO) |
| **Modulator** | 90-95% | Small, distal | Control - "how to process" | Cortex L6, brainstem, TRN |

**Key insight:** Drivers define WHAT is being relayed. Modulators shape HOW it's relayed (gain, timing, mode).

---

## Cortical Layer Connections

| Layer | Direction | Function | Target |
|-------|-----------|----------|--------|
| **L4** | Thalamus → Cortex | Receives thalamic input | From first-order nuclei |
| **L5** | Cortex → Thalamus | Sends higher-order drivers | To higher-order nuclei (Pulvinar, MD) |
| **L6** | Cortex → Thalamus | Sends modulatory feedback | To same nucleus that projects to L4 |

### Special Cases

- **Frontal L5 → TRN (direct):** Unique to frontal cortex. Allows executive control over gating.
- **Intralaminar → L1:** Diffuse arousal projection to superficial layers.
- **Intralaminar → Striatum:** Also projects to striatum (not just cortex).

---

## The 6 Major Loops

All loops run **concurrently** and are **interdependent**.

### Loop 1: Cortico-Cerebellar (Motor Coordination)

```
Cortex (M1) → Pons → Cerebellum → Deep Nuclei → Thalamus (VL) → Cortex
```

- **Purpose:** Motor timing, trajectory, error correction
- **Timescale:** ~10-50ms
- **Thalamic nucleus:** VL

### Loop 2: Cortico-Basal Ganglia (Action Selection)

```
Cortex → Striatum → GPi/SNr → Thalamus (VA/VL) → Cortex
```

- **Purpose:** Select ONE action from candidates (winner-take-all)
- **Timescale:** ~100-500ms
- **Thalamic nucleus:** VA, VL (shared with cerebellar!)
- **Key feature:** Direct pathway (GO) vs Indirect pathway (NO-GO)

### Loop 3: Papez Circuit (Episodic Memory)

```
Hippocampus → Mammillary Bodies → Thalamus (AN) → Cingulate → Hippocampus
```

- **Purpose:** Memory consolidation, emotional tagging
- **Timescale:** ~seconds
- **Thalamic nucleus:** AN (Anterior Nucleus)
- **Damage anywhere:** Amnesia

### Loop 4: Hippocampal-Prefrontal (Memory-Executive)

```
mPFC ↔ Thalamus (Reuniens) ↔ Hippocampus
```

- **Purpose:** Use memories for planning, guide retrieval based on goals
- **Timescale:** ~minutes-hours
- **Thalamic nucleus:** Reuniens (BIDIRECTIONAL - unique!)
- **Key feature:** Both directions active simultaneously

### Loop 5: Arousal (Global State)

```
Brainstem → Thalamus (CM, Pf, CL) → Broad Cortex + Striatum
```

- **Purpose:** Set global state (awake/asleep/alert)
- **Thalamic nuclei:** Intralaminar (CM, Pf, CL)
- **Modulates:** ALL other loops via neuromodulators
- **Neuromodulators:** Acetylcholine (mode), Norepinephrine (alertness), Dopamine (motivation), Serotonin (mood)

### Loop 6: Emotional Salience (Threat Detection)

```
Sensory → Thalamus → Amygdala → Thalamus (MD, Pulvinar) → Priority boost
```

- **Purpose:** Detect threats FAST, boost processing for salient stimuli
- **Two pathways:**
  - **Low road (fast, ~12ms):** Thalamus → Amygdala (coarse)
  - **High road (slow, ~100ms):** Thalamus → Cortex → Amygdala (detailed)
- **Thalamic nuclei:** MD, Pulvinar (priority boost)

### Loop Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                             │
│                                       CORTEX                                                │
│   ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  M1  │ Premotor │  PFC  │  V1  │ Parietal │ Cingulate │ mPFC │ Temporal              │   │
│   └──┬───┴────┬─────┴───┬───┴───┬──┴────┬─────┴─────┬─────┴───┬──┴──────┬───────────────┘   │
│      │        │         │       │       │           │         │         │                   │
│   ═══╪════════╪═════════╪═══════╪═══════╪═══════════╪═════════╪═════════╪═════════════════  │
│      │        │         │       │       │           │         │         │                   │
│      ↓        ↓         ↓       ↓       ↓           ↓         ↓         ↓                   │
│   ┌──────────────────────────────────────────────────────────────────────────────────────┐  │
│   │                                    THALAMUS                                          │  │
│   │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌─────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌─────────┐ │  │
│   │  │ VL │ │ VA │ │ MD │ │LGN │ │Pulv │ │ LP │ │ AN │ │ LD │ │Reun│ │CM/Pf│ │   TRN   │ │  │
│   │  └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └──┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ │ (gates) │ │  │
│   └────┼──────┼──────┼──────┼───────┼──────┼──────┼──────┼──────┼──────┼────┴─────────┴─┘  │
│        ↑      ↑      ↑      ↑       ↑      ↑      ↑      ↑      ↑      ↑                   │
│        │      │      │      │       │      │      │      │      │      │                   │
│   ┌────┴──┐ ┌─┴──┐ ┌─┴──┐   │    ┌──┴──┐   │   ┌──┴──┐   │   ┌──┴──┐ ┌─┴───┐              │
│   │ CERE- │ │BAS-│ │AMYG│   │    │ SUP │   │   │MAMM-│   │   │HIPP-│ │BRAIN│              │
│   │ BELLUM│ │GAL │ │DALA│   │    │COLL │   │   │ILLRY│   │   │OCMP │ │STEM │              │
│   └───────┘ └────┘ └────┘   │    └─────┘   │   └─────┘   │   └─────┘ └─────┘              │
│                             │              │             │                                 │
│                          RETINA        PARIETAL     HIPPOCAMPUS                           │
│                                                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────┘

LOOP 1: CORTEX ──→ PONS ──→ CEREBELLUM ──→ VL ──→ CORTEX (Motor coordination)
LOOP 2: CORTEX ──→ STRIATUM ──→ GPi ──→ VA/VL ──→ CORTEX (Action selection)
LOOP 3: HIPPOCAMPUS ──→ MAMMILLARY ──→ AN ──→ CINGULATE ──→ HIPPOCAMPUS (Memory)
LOOP 4: mPFC ←──→ REUNIENS ←──→ HIPPOCAMPUS (Memory-executive, bidirectional)
LOOP 5: BRAINSTEM ──→ CM/Pf/CL ──→ BROAD CORTEX + STRIATUM (Arousal)
LOOP 6: SENSORY ──→ THALAMUS ──→ AMYGDALA ──→ MD/PULVINAR ──→ boost (Emotional)
```

---

## Multi-Input Nuclei

Some nuclei receive from MULTIPLE sources and must INTEGRATE, not just relay.

### VL: Cerebellum + Basal Ganglia

```
                              TO MOTOR CORTEX (M1)
                                      ↑
                           ┌──────────┴──────────┐
                           │         VL          │
                           │                     │
                           │   ┌─────────────┐   │
                           │   │ INTEGRATOR  │   │
                           │   │             │   │
                           │   │  WHAT + HOW │   │
                           │   └─────────────┘   │
                           └────┼───────────┼────┘
                                │           │
                    ┌───────────┴───┐   ┌───┴───────────┐
                    │  CEREBELLUM   │   │ BASAL GANGLIA │
                    │  "HOW to move"│   │ "WHAT to move"│
                    │   - timing    │   │  - selection  │
                    │   - trajectory│   │  - go/no-go   │
                    └───────────────┘   └───────────────┘
```

**Integration mode:** Combine (both needed for proper motor output)

### MD: Amygdala + Basal Ganglia + PFC

```
                              TO PFC
                                ↑
                           ┌────┴────┐
                           │   MD    │
                           │         │
                           │PRIORITY:│
                           │1. Threat│
                           │2. Reward│
                           │3. Cognit│
                           └─┬──┬──┬─┘
                             │  │  │
               ┌─────────────┘  │  └─────────────┐
               ↓                ↓                ↓
        ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
        │  AMYGDALA   │  │BASAL GANGLIA│  │    PFC L5   │
        │   THREAT    │  │   REWARD    │  │  COGNITION  │
        └─────────────┘  └─────────────┘  └─────────────┘
```

**Integration mode:** Priority (Threat > Reward > Cognition)

### Pulvinar: The Grand Orchestrator

```
                    TO MULTIPLE CORTICAL AREAS
                    (V2, V4, MT, Parietal, Temporal)
                              ↑
                    ┌─────────┴─────────┐
                    │     PULVINAR      │
                    │                   │
                    │  1. Integrate     │
                    │  2. Synchronize   │
                    │  3. Route         │
                    │  4. Prioritize    │
                    └─┬───┬───┬───┬───┬─┘
                      │   │   │   │   │
        ┌─────────────┘   │   │   │   └─────────────┐
        ↓         ┌───────┘   │   └───────┐         ↓
   ┌─────────┐ ┌──┴──────┐ ┌──┴──┐ ┌──────┴──┐ ┌─────────┐
   │  V1 L5  │ │ SUP.COLL│ │AMYG │ │PARIETAL │ │TEMPORAL │
   │ vision  │ │salience │ │emot │ │ where   │ │  what   │
   └─────────┘ └─────────┘ └─────┘ └─────────┘ └─────────┘
```

**Integration mode:** Orchestrate (integrate, sync, route, prioritize)

---

## Cross-Loop Communication

Loops are NOT isolated. They communicate through:

### 1. Shared Thalamic Nuclei

| Shared Nucleus | Loops |
|----------------|-------|
| VL | Cerebellar (Loop 1) + Basal Ganglia (Loop 2) |
| MD | Emotional (Loop 6) + Executive |
| Pulvinar | Emotional (Loop 6) + Visual processing |
| CM/Pf | Arousal (Loop 5) → affects ALL loops |

### 2. Event Bus (Cross-Loop Events)

| Event | Source Loop | Affects |
|-------|-------------|---------|
| `arousal_change` | Arousal (5) | ALL loops |
| `threat_detected` | Emotional (6) | BG (2), Arousal (5), Memory (3) |
| `action_selected` | BG (2) | Cerebellar (1) |
| `memory_retrieved` | Memory (3, 4) | BG (2), Visual (Pulvinar) |

### 3. Global Neuromodulators

| Modulator | Source | Affects |
|-----------|--------|---------|
| Dopamine | VTA/SNc | Striatum, PFC, ALL thalamic relays (gain) |
| Acetylcholine | BF, PPT | ALL thalamic relays (tonic/burst mode) |
| Norepinephrine | LC | ALL thalamic relays (gain), cortex (alertness) |
| Serotonin | Raphe | ALL structures (mood) |

---

## Challenges

### 1. Multi-Input Integration

How do nuclei that receive from multiple sources integrate?

| Nucleus | Integration Challenge |
|---------|----------------------|
| VL | Combine "WHAT to move" (BG) with "HOW to move" (Cerebellum) |
| MD | Priority hierarchy: Threat > Reward > Cognition |
| Pulvinar | Orchestrate: integrate, synchronize, route, prioritize |

### 2. Timing/Synchronization

Different loops run at different timescales:

| Loop | Timescale |
|------|-----------|
| Cerebellar | ~10-50ms |
| Thalamocortical | ~20-100ms |
| Basal ganglia | ~100-500ms |
| Emotional (fast) | ~12ms |
| Memory (Papez) | ~seconds |
| Hippocampal-PFC | ~minutes-hours |

### 3. Global State Modulation

Neuromodulators affect EVERYTHING - this is global configuration, not per-loop.

### 4. Priority/Arbitration

When multiple inputs compete:
- TRN gating (sector-level via lateral inhibition)
- Multi-input nuclei have priority hierarchies
- Pulvinar orchestration for binding

---

## Software Architecture

### Core Classes

```python
# Relay Module (single nucleus)
class RelayModule:
    name: str
    order: str  # "first" | "higher"
    sector: str  # "visual" | "auditory" | "motor" | "limbic" | etc.
    driver_input: Channel      # 5-10% - content
    modulator_input: Channel   # 90-95% - control
    gate: Gate                 # Controlled by TRN
    mode: str                  # "tonic" | "burst"

# TRN Gatekeeper
class TRN:
    sectors: Dict[str, Sector]  # visual, auditory, motor, limbic, etc.
    def receive_collateral(relay_name, data)  # From relay outputs
    def receive_control(priority_signal)       # From attention controller
    def update_gates()                         # Apply gating

# Thalamus Framework
class ThalamusFramework:
    relay_modules: Dict[str, RelayModule]
    trn: TRN
    attention_controller: AttentionController

    def register_first_order(name, external_input, output_target, sector)
    def register_higher_order(name, source_modules, output_targets, sector)
    def connect_feedback(relay_name, feedback_channel)  # L6 → relay
    def set_attention(priority_sector)                  # Top-down
    def handle_salience(salient_event)                  # Bottom-up
```

### Multi-Input Nuclei

```python
class VL_Nucleus(RelayModule):
    cerebellar_input: Channel   # HOW to move
    basal_ganglia_input: Channel  # WHAT to move
    integration_mode = "combine"

class MD_Nucleus(RelayModule):
    amygdala_input: Channel      # Threat/emotion
    basal_ganglia_input: Channel  # Reward/value
    pfc_input: Channel            # Cognitive/goals
    priority = ["amygdala", "basal_ganglia", "pfc"]
    integration_mode = "priority"

class Pulvinar(RelayModule):
    inputs: Dict[str, Channel]   # v1, sc, amygdala, parietal, temporal
    outputs: Dict[str, Channel]  # v2, v4, mt, parietal, temporal
    integration_mode = "orchestrate"
```

### Complete System

```python
class BrainArchitecture:
    # Global
    neuromodulators: NeuromodulatorSystem
    event_bus: EventBus

    # Central Hubs
    thalamus: ThalamusFramework
    striatum: StriatumFramework
    brainstem: BrainstemFramework

    # Processing Structures
    cortex: CortexFramework
    cerebellum: CerebellumFramework
    basal_ganglia: BasalGangliaFramework
    hippocampus: HippocampusFramework
    amygdala: AmygdalaFramework

    # Loops (all concurrent)
    loops: Dict[str, Loop]

    async def run():
        await asyncio.gather(
            *[loop.run() for loop in loops.values()],
            neuromodulators.run(),
            event_bus.run(),
            thalamus.run()
        )
```

---

## Mapping to brain-mimc

| Document Concept | brain-mimc Equivalent |
|------------------|----------------------|
| Relay nucleus | Independent async worker |
| TRN | Central gatekeeper with GateState |
| TRN sectors | TRNSector enum (VISUAL, AUDITORY, MOTOR, etc.) |
| Driver input | Lane A messages |
| Modulator input | Lane B messages |
| Tonic mode | TRNMode.TONIC |
| Burst mode | TRNMode.BURST |
| First-order | NucleusId (LGN, MGN, VPL, etc.) |
| Higher-order | NucleusId (PULVINAR, MD, LP) |
| Layer VI feedback | Lane B (MODULATOR) |
| Synchronization | Lane G (GATE) coordination |

---

## References

- `docs/knowledgebase/subcortical-thalamus/` - Source reference documents
- `docs/knowledgebase/brain/cerebrum-Subcortical-Structures-Thalamus.md` - Verified KB
- `docs/knowledgebase/brain/sources.md` - Citations (P31: Hádinger 2022)
- `src/cerebrum/subcortical/thalamus/` - Current implementation (stubs)

---

## Next Steps

1. **Define NucleusId enum** with all ~60 nuclei organized by class
2. **Implement TRNSector** with proper sector organization
3. **Design multi-input integration** for VL, MD, Pulvinar
4. **Implement cross-loop EventBus**
5. **Add NeuromodulatorSystem** for global state
6. **Wire up the 6 major loops**
