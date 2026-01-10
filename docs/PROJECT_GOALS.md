# brain-mimc: Project Goals & Requirements

> **Status:** Living document. First draft - to be refined as project evolves.

## Vision

Build a **complete brain-inspired distributed computing architecture** that models the full hierarchy of neural processing. The system implements all major brain regions as independent, concurrent components communicating via typed async pub-sub.

This is not a simulation of a brain - it is a **software architecture inspired by how brains organize computation**: parallel, hierarchical, attention-gated, and safe-by-default.

## Core Principles

### 1. Full Parallelism (Non-Negotiable)

**Everything runs concurrently at every level of granularity.**

| Level | Parallel Units |
|-------|----------------|
| System | Cerebrum, Cerebellum, Brainstem, Spinal Cord |
| Region | Cortex, Thalamus, BG, Limbic, Hypothalamus |
| Sub-component | Each nucleus, each cortex layer, each pathway |
| Loop | A, B, C, D all run concurrently |
| Scope | Each room/device/session processes independently |

No sequential pipelines. No blocking calls. No orchestrator.

### 2. "Raw Never Goes Up"

Data is transformed into typed summaries at each level before ascending. Sensor floods stay at spinal cord; only structured RelayBundles reach thalamus.

### 3. Drivers vs Modulators

- **Drivers** carry content (what happened)
- **Modulators** carry control (how to treat it)

Drivers never change gates. Modulators influence but don't dictate.

### 4. Safe-by-Default

Basal ganglia suppresses all actions unless explicitly released. The system does nothing dangerous by default.

### 5. Attention Gating

TRN controls what reaches cortex. Not everything gets through - attention is a limited resource.

### 6. Contract-First

All communication via typed, versioned contracts. Components can run on different machines/languages if they share:
- MQTT topic conventions
- Wire contracts (schema + semantics)

## System Architecture

### Brain Regions

```
┌─────────────────────────────────────────────────────────────────┐
│                         CEREBRUM                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      CORTEX                              │    │
│  │   Multi-layer: L4 (receive) / L5 (HO driver) / L6 (mod) │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ║                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ THALAMUS │ │   BG     │ │  LIMBIC  │ │  HYPO-   │           │
│  │ (routing)│ │(selection│ │ (memory/ │ │ THALAMUS │           │
│  │          │ │  gating) │ │ salience)│ │(homeo-   │           │
│  │ LGN,MGN, │ │ Direct/  │ │ Amygdala │ │ stasis)  │           │
│  │ PULVINAR,│ │ Indirect/│ │ Hippo-   │ │          │           │
│  │ MD, TRN  │ │ Hyper-   │ │ campus   │ │          │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ║
┌─────────────────────────────────────────────────────────────────┐
│                       CEREBELLUM                                 │
│            Timing, calibration, motor learning                   │
│                    (Not yet implemented)                         │
└─────────────────────────────────────────────────────────────────┘
                              ║
┌─────────────────────────────────────────────────────────────────┐
│                        BRAINSTEM                                 │
│     Relay bundles, pattern triggers, neuromodulators            │
│              Arousal, alertness, global state                    │
└─────────────────────────────────────────────────────────────────┘
                              ║
┌─────────────────────────────────────────────────────────────────┐
│                       SPINAL CORD                                │
│        Edge I/O, afferent/efferent, fast reflexes               │
│                 Device-proximal processing                       │
└─────────────────────────────────────────────────────────────────┘
```

### The Four Major Loops (All Run Concurrently)

**Loop A: Cortex <-> Thalamus <-> Cortex** (Routing + Attention)
- Thalamus relays sensory/association signals to cortex
- Cortex L6 sends modulatory feedback
- Cortex L5 sends higher-order drivers for cortex-to-cortex routing
- TRN gates based on attention/salience

**Loop B: Cortex -> BG -> Thalamus -> Cortex** (Action Selection)
- Cortex proposes candidate actions
- BG selects/suppresses via direct/indirect/hyperdirect pathways
- Winner released to thalamus (VA/VL)
- Motor cortex executes

**Loop C: Cortex -> Cerebellum -> Thalamus -> Cortex** (Calibration)
- Cortex sends efference copy
- Cerebellum computes timing/error corrections
- Corrections relayed via thalamus (VL)
- Motor cortex adjusts

**Loop D: Limbic -> Hypothalamus -> Brainstem -> Body** (Regulation)
- Amygdala/hippocampus provide valence/context
- Hypothalamus sets autonomic + endocrine outputs
- Brainstem implements via spinal cord
- Body state changes

### Cross-Links

| Link | Mechanism |
|------|-----------|
| BG <-> Brainstem | SNr inhibits/releases superior colliculus (orienting) |
| Thalamus as choke-point | BG and cerebellum both influence cortex through thalamus |
| Limbic drives BG | Amygdala valuation biases action selection |
| Hypothalamus sets mode | Hunger/stress/circadian changes priorities |
| Neuromodulators | Brainstem tunes gating, processing, plasticity everywhere |

## Thalamus: Nucleus-Based Architecture

The thalamus requires nucleus-based addressing (not just channels) to support:

### Nucleus Classes

| Class | Nuclei | Input | Output | Role |
|-------|--------|-------|--------|------|
| First-order | LGN, MGN, VPL/VPM, VA/VL | Sensory/subcortical | Primary cortex L4 | Relay external world |
| Higher-order | Pulvinar, MD, LP/LD | Cortex L5 | Association cortex L4 | Cortex-to-cortex |
| Diffuse | CM, Pf, CL, PVT | Brainstem arousal | Widespread cortex | Arousal, state |
| Gate | TRN | Collaterals from all | Inhibits relay nuclei | Attention gating |

### Why Not Channels?

1. Higher-order routing required (L5 -> PULVINAR -> different cortex)
2. Layer-specific semantics (L4 receives, L6 modulates, L5 drives HO)
3. BG/Cerebellar integration needs nucleus addressing (GPi -> VA/VL)
4. Nucleus classes behave differently

## Development Phases (Brain-Faithful)

> Per V23: Brain never has "contracts only" - always concurrent operation. Integration is continuous, not a final phase.

### Phase 1: Contracts + Minimal Concurrent Stubs

Define all input/output types AND create minimal working stubs for every component. All components exist from day one.

### Phase 2: Concurrent Elaboration

All components grow in capability together. Integration happens continuously as part of this phase.

| Component | Status | Priority | Rationale |
|-----------|--------|----------|-----------|
| Spinal Cord | Partial | HIGH (Foundation) | I/O layer - everything depends on it |
| Brainstem | Partial | HIGH (Foundation) | Vital/arousal systems |
| Thalamus (nucleus-based) | Not started (restart) | HIGH (Gateway) | Cannot route without nucleus addressing |
| Basal Ganglia | Skeleton exists | MEDIUM (Processing) | Action selection |
| Cerebellum | Not started | MEDIUM (Processing) | Calibration |
| Limbic | Skeleton exists | MEDIUM (Integration) | Memory, emotion |
| Hypothalamus | Skeleton exists | MEDIUM (Integration) | Homeostasis |
| Cortex (multi-layer) | Mock exists | LOWER (Depends on all) | Requires all above |

> Per V24: Brain builds foundation-up. Cortex depends on all lower structures.

## Key Invariants

1. No component waits for another
2. No sequential dependencies between regions
3. Each component works standalone with mocked I/O
4. All communication is typed and versioned
5. Failures degrade gracefully, never cascade

---

## Open Questions

(To be filled in as project evolves)

---

## Verification Log

### Verified & Agreed

| # | Item | Source | Notes |
|---|------|--------|-------|
| V1 | Implement all regions: Cerebrum, Cerebellum, Brainstem, Spinal Cord | User stated | "we will implement cerebrum, cerebellum, brainstem and the spinal-cord" |
| V2 | Full parallelism is mandatory | User stated | "The whole project should be parallel it is forbidden to build it sequential" |
| V3 | Parallelism at all levels: components, sub-components, loops | User stated | "not only components but their sub-components also. The loops" |
| V4 | Four major loops (A, B, C, D) | User stated | User provided detailed loop diagrams |
| V5 | Cross-links between systems | User stated | User provided cross-links table |
| V6 | Thalamus needs nucleus-based model (not channel) | Discussed & agreed | Higher-order routing, layer semantics, BG integration require it |
| V7 | Cortex will have multi-layer (L4/L5/L6) | User stated | User described L4 receive, L5 HO driver, L6 modulator |
| V8 | "Raw never goes up" principle | In CLAUDE.md | User did not contradict |
| V9 | Drivers vs Modulators separation | In existing docs | User did not contradict |
| V10 | Safe-by-default (BG suppresses) | In CLAUDE.md | User did not contradict |
| V11 | Attention gating via TRN | Discussed | Part of thalamus deep-dive |
| V12 | Contract-first / typed pub-sub | In CLAUDE.md | User did not contradict (but see Item 7 - communication method may change) |
| V13 | Canonical microcircuit pattern repeats | User stated | Same 6-layer architecture across all cortex regions, differences in config not structure |
| V14 | Hardware heterogeneity at layer level | User confirmed | Each layer (I-VI) may run on different hardware; layer-to-layer communication must be network-capable |
| V15 | Hardware heterogeneity is a GENERAL principle | User confirmed | Applies to whole system, not just thalamus - any part may run on different hardware |
| V16 | Decide at lowest possible level | User stated | Decisions made at lowest region/hardware possible; only escalate to higher areas when lower cannot decide |
| V17 | Hardware mapping is TBD | User stated | What maps to hardware (layers vs regions vs areas) not yet decided |
| V18 | No central orchestrator | neuro-expert (KB) | Routes pre-wired in anatomy; broadcast modulation sets state but doesn't orchestrate |
| V19 | Components can function standalone | neuro-expert (KB) | Spinal reflexes, CPGs work in isolation; cortex survives spinal injury |
| V20 | Graceful degradation EXCEPT critical infrastructure | neuro-expert (KB) | Processing components degrade gracefully; critical infra (brainstem) = single point of failure |
| V21 | Pub-sub over continuous streaming | neuro-expert (KB) | Brain converts continuous input to discrete events at sensor level (retina, cochlea, mechanoreceptors) |
| V22 | "Raw never goes up" validated at sensor level | neuro-expert (KB) | Retina does edge detection, cochlea does frequency decomposition BEFORE transmitting |
| V23 | Phase structure: Contracts+Stubs → Concurrent Elaboration (no separate integration phase) | neuro-expert | Brain always has concurrent operation |
| V24 | Priority: Foundation-up (Brainstem/SpinalCord/Thalamus first, Cortex last) | neuro-expert | Cortex depends on all lower structures |
| V25 | Thalamus: Nucleus-based from scratch (Option A) | neuro-expert | Nucleus classes fundamental to driver/modulator, TRN gating, transthalamic routes |
| V26 | Communication: Discrete pub-sub (not continuous streaming) | neuro-expert | Brain uses discrete spikes; rate emerges from counting events |

### Items Requiring Discussion

| # | Item | Status | Original | Final | Rationale |
|---|------|--------|----------|-------|-----------|
| 1 | "Not a simulation" framing | RESOLVED | I added without discussion | "Simulates brain organization with neuroscience-accurate granularity (nuclei, layers, pathways) but not biological processes (neurons, neurotransmitters)" | User confirmed this framing |
| 2 | "No orchestrator" claim | RESOLVED | I inferred from parallelism | YES - Brain-faithful | See V18. Routes pre-wired, broadcast modulation sets state (not orchestration) |
| 3 | Phase 1/2/3 structure | RESOLVED | I invented this | Modified: Contracts+Stubs → Concurrent Elaboration (no Phase 3) | See V23. neuro-expert: brain never has "contracts only" |
| 4 | Priority assignments | RESOLVED | I invented this | CHANGED: Foundation-up (SpinalCord/Brainstem/Thalamus → BG/Cerebellum → Limbic/Hypothalamus → Cortex) | See V24. neuro-expert: brain builds foundation-up |
| 5 | "Each component works standalone" | RESOLVED | I inferred this | YES - Brain-faithful | See V19. Spinal reflexes, CPGs work in isolation |
| 6 | "Failures degrade gracefully" | RESOLVED | I inferred this | PARTIAL - Add exception | See V20. Critical infra (brainstem) = single point of failure |
| 7 | Continuous streaming vs pub/sub | RESOLVED | User raised | Pub-sub MORE brain-faithful | See V21-V22. Sensors transform to discrete events |
| 8 | Expert agent/skill creation | RESOLVED | User raised | See plan file | SEPARATE neuro + arch experts (accuracy-first) |
| 9 | Hardware heterogeneity at layer level | RESOLVED | User raised | See V14-V17 | Confirmed as general principle; hardware mapping TBD |

---

## Expert Agent Specification

> Full specification is maintained in the plan file: `~/.claude/plans/eager-beaming-barto.md`

### Overview

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Scope | SEPARATE experts | Accuracy-first: combined risks being "good enough" in both but deeply rigorous in neither |
| Type | Two Agents + Two Skills | Each domain needs full depth; quick checks for both |

### Four Components

| Component | Type | Domain | Purpose |
|-----------|------|--------|---------|
| `neuro-expert` | Agent | Neuroscience | KB verification, codebase audits, brain-faithfulness |
| `/neuro-check` | Skill | Neuroscience | Quick inline brain-faithfulness checks |
| `brain-software-arch-expert` | Agent | Architecture | 5 modes, pattern validation, bulletproof protocol |
| `/arch-check` | Skill | Architecture | Quick inline architecture pattern checks |

### Three-Way Discussion Model

```
neuro-expert ←→ brain-software-arch-expert
      ↓               ↓
         USER DECIDES
```

1. neuro-expert: "Brain does X" (with scientific citation)
2. arch-expert: "Implement X like this" (with pattern)
3. Both experts discuss before user decides
4. User makes final decision

### Key Principles

- Assume ALL KB files WRONG until verified against scientific papers
- Every line, comment, doc - no surface-level work
- Experts do NOT write code (advise only)
- Experts do NOT make final decisions (user decides)

### Knowledge Base

Location: `./docs/knowledgebase/brain/` (24 content files VERIFIED - see `verified.md`)
