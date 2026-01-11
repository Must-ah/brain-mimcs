# brain-mimc: Project Goals & Requirements

> **Status:** Living document.

## Vision

Build a **complete brain-inspired distributed computing framework** that models the full hierarchy of neural processing. The system implements all major brain regions as independent, concurrent components communicating non-blocking.

The brain is divided into:
- **Cerebrum** (with Cortex, Thalamus, Basal Ganglia, Limbic System, Hypothalamus)
- **Cerebellum**
- **Brainstem**
- **Spinal Cord**

This is not a simulation of a brain - it is a **software framework inspired by how brains organize computation**.

## Core Principles

### 1. Full Parallelism (Non-Negotiable)

**Everything runs concurrently at every level of granularity.**

| Level | Parallel Units |
|-------|----------------|
| System | Cerebrum, Cerebellum, Brainstem, Spinal Cord |
| Region | Cortex, Thalamus, BG, Limbic, Hypothalamus |
| Sub-component | Each nucleus, each cortex layer, each pathway |
| Loop | Multiple loops run concurrently (A-E are examples, more exist) |
| Scope | Each room/device/session processes independently |

**No sequential pipelines. No blocking calls. No orchestrator (like the brain).**

Different structures and regions may run on different hardware.

### 2. Message + Context

Information flows as **messages** (what happened) with corresponding **context** (how to adjust the system).

- Messages carry content
- Context guides processing
- Messages don't change system state directly; context influences behavior

### 3. Safety Mechanisms

The system uses brain-inspired safety mechanisms. Actions are suppressed by default unless explicitly released.

### 4. Attention Gating

TRN controls what reaches cortex. Not everything gets through - attention is a limited resource.

### 5. Non-Blocking Communication

All communication must be non-blocking. Different communication channels exist based on system needs:
- Regular channels for normal operation
- Reflect-path (emergency channel) for critical communication

### 6. Decide at Lowest Level

Decisions made at lowest region/hardware possible. Only escalate to higher areas when lower cannot decide.

## System Architecture

- **Cerebrum**
  - Cortex
  - Thalamus
  - Basal Ganglia
  - Limbic System
  - Hypothalamus
- **Cerebellum**
- **Brainstem**
- **Spinal Cord**

### Major Loops (Examples)

> These are examples. More loops exist, including loops within subcortical parts and between regions.

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

**Loop E: Hippocampus -> Mammillary Bodies -> Anterior Thalamus -> Cingulate -> Hippocampus** (Memory/Papez Circuit)
- Hippocampus encodes new declarative memories
- Mammillary bodies relay to anterior thalamus
- Anterior thalamus projects to cingulate cortex
- Cingulate provides emotional/contextual integration
- Essential for memory consolidation (damage causes amnesia)

### Cross-Links

| Link | Mechanism |
|------|-----------|
| BG <-> Brainstem | SNr inhibits/releases superior colliculus (orienting) |
| Thalamus as choke-point | BG and cerebellum both influence cortex through thalamus |
| Limbic drives BG | Amygdala valuation biases action selection |
| Hypothalamus sets mode | Hunger/stress/circadian changes priorities |
| Neuromodulators | Brainstem tunes gating, processing, plasticity everywhere |

## Key Invariants

1. **FORBIDDEN** for any component to wait for another
2. **STRICTLY FORBIDDEN** to write sequential code
3. Each structure and sub-structure must be mockable
4. All communication must be non-blocking
5. Failures handled like the brain (graceful degradation, redundancy)

---

## Open Questions

(To be filled in as project evolves)

---

## Verification Log

### Verified & Agreed

| # | Item | Notes |
|---|------|-------|
| V1 | Implement all regions: Cerebrum, Cerebellum, Brainstem, Spinal Cord | User stated |
| V2 | Full parallelism is mandatory | "The whole project should be parallel it is forbidden to build it sequential" |
| V3 | Parallelism at all levels: components, sub-components, loops | User stated |
| V5 | Regions interconnect like the brain | User stated |
| V14 | Hardware heterogeneity at layer level | Each layer may run on different hardware |
| V15 | Hardware heterogeneity is a GENERAL principle | Any part may run on different hardware |
| V16 | Decide at lowest possible level | Only escalate when lower cannot decide |
| V17 | Hardware mapping is TBD | Not yet decided |
| V18 | No one decides - structure forces outcome | Intelligence emerges from dumb parts following local rules. No module knows the whole plan. No module coordinates others. The architecture IS the coordination. |
| V19 | Components can function standalone | Each structure mockable; works in isolation |

> Detailed thalamus verification items (V27-V33) moved to `docs/architecture/cerebrum/subcortical-thalamus/thalamus-architecture.md`
