# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

brain-mimc is a brain-inspired software architecture modeling hierarchical, asynchronous communication inspired by neural anatomy. It uses a pub-sub model with multiple "planes" (lanes) similar to neural tracts for IoT/home automation.

**Core Principle:** "Raw never goes up" - sensor data is transformed into typed summaries at each level before passing to higher layers.

## Core Principles (NON-NEGOTIABLE)

### 1. Full Parallelism

**Everything runs concurrently at every level of granularity.**

| Level | Parallel Units |
|-------|----------------|
| System | Cerebrum, Cerebellum, Brainstem, Spinal Cord |
| Region | Cortex, Thalamus, BG, Limbic, Hypothalamus |
| Sub-component | Each nucleus, each cortex layer, each pathway |
| Loop | A, B, C, D all run concurrently |
| Scope | Each room/device/session processes independently |

**No sequential pipelines. No blocking calls. No orchestrator.**

### 2. Four Major Loops (ALL CONCURRENT)

| Loop | Path | Purpose |
|------|------|---------|
| A | Cortex ↔ Thalamus ↔ Cortex | Routing + Attention |
| B | Cortex → BG → Thalamus → Cortex | Action Selection |
| C | Cortex → Cerebellum → Thalamus → Cortex | Calibration |
| D | Limbic → Hypothalamus → Brainstem → Body | Regulation |

### 3. Thalamus: Nucleus-Based Architecture

**NOT just channels - requires nucleus-based addressing:**

| Class | Nuclei | Role |
|-------|--------|------|
| First-order | LGN, MGN, VPL/VPM, VA/VL | Relay external world to primary cortex L4 |
| Higher-order | Pulvinar, MD, LP/LD | Cortex-to-cortex routing (L5 → association cortex) |
| Diffuse | CM, Pf, CL, PVT | Arousal, state (brainstem → widespread cortex) |
| Gate | TRN | Attention gating (inhibits relay nuclei) |

### 4. Cortex Layer Semantics

| Layer | Function |
|-------|----------|
| L4 | Receives input from thalamus |
| L5 | Sends higher-order drivers (to HO thalamic nuclei) |
| L6 | Sends modulatory feedback (to thalamus) |

### 5. Hardware Heterogeneity

- Any part may run on different hardware
- Layer-to-layer communication must be network-capable
- Decide at lowest possible level - only escalate when lower cannot decide

### 6. Drivers vs Modulators

- **Drivers** carry content (what happened)
- **Modulators** carry control (how to treat it)
- Drivers never change gates. Modulators influence but don't dictate.

### 7. Safe-by-Default

Basal ganglia suppresses all actions unless explicitly released.

## Commands

```bash
# Run demos (Python 3.11+ required)
python main.py --demo mock-cortex    # Run mock cortex demo
python main.py --demo comms-router   # Run communications router demo
```

## Architecture

### Data Flow Hierarchy

```
SpinalCord (Edge I/O + Reflex)
    ↓ AfferentSignals (raw sensor data)
Brainstem (Relay + Pattern + Global Broadcast)
    ↓ RelayBundles (typed summaries)
Thalamus (Gating/routing nucleus)
    ↓ RouteDecision (to cortex areas/layers)
Cortex (Decision/perception)
    ↓ Commands (via motor path)
SpinalCord (Efferent actuator commands)

Subcortical modules:
  - Hypothalamus: homeostasis regulation (fast autonomic vs slow endocrine)
  - Basal Ganglia: action selection with default suppression (safe-by-default)
  - Limbic: memory/salience/emotion
```

### Major Loops (Target Architecture)

See `src/cerebrum/subcortical/thalamus/ARCHITECTURE_GOALS.md` for full details.

- **Loop A**: Cortex <-> Thalamus <-> Cortex (routing + attention coordination)
- **Loop B**: Cortex -> Basal Ganglia -> Thalamus -> Cortex (action selection)
- **Loop C**: Cortex -> Cerebellum -> Thalamus -> Cortex (timing/calibration)
- **Loop D**: Limbic -> Hypothalamus -> Brainstem (body regulation)

### Communication Lanes

| Lane | Purpose | Direction |
|------|---------|-----------|
| A (DRIVER) | Payload/content | SpinalCord → Brainstem → Thalamus → Cortex |
| B (MODULATOR) | Feedback/attention control | Cortex → Thalamus/TRN |
| C (COMMAND) | Motor commands | Cortex → Brainstem → SpinalCord |
| D (GLOBAL MODES) | Neuromodulators | Hypothalamus/Brainstem → ALL |
| E (ERROR/OUTCOME) | Learning signals | SpinalCord/Limbic → Cortex/BG |
| G (GATE) | TRN inhibition state | Distributed control-plane |
| X (REFLECTION) | Audit/observability | Non-blocking copies |

### Key Contracts (`src/shared/`)

**contracts_base_async.py** - Core types:
- `ScopeLevel`: DEVICE, ROOM, HOUSE, USER_SESSION
- `Plane`: SPINAL, BRAINSTEM, THALAMUS, CORTEX, REFLECT
- `MessageType`: AFFERENT_SIGNAL, EFFERENT_COMMAND, RELAY_BUNDLE, etc.
- `TopicBus` Protocol: async publish/subscribe interface
- `InMemoryTopicBus`: reference implementation for testing
- `RejectEvent`: standard rejection message contract

**plane_base_async.py** - Base plane facade:
- `BasePlaneFacade`: common ingress validation and reject logic
  - Subclasses define: `ALLOWED_INBOUND`, `ORIGIN_PLANE`, `REJECT_HINT`
  - Override `dispatch(topic, msg)` for domain-specific handling
  - Base handles: type validation, RejectEvent emission to reflect bus

### Source Layout

```
src/
├── shared/
│   ├── contracts_base_async.py  # Core types, TopicBus, RejectEvent
│   ├── plane_base_async.py      # BasePlaneFacade (ingress/reject logic)
│   └── topics_async.py          # Shared topic helpers
├── spinal_cord/      # SpinalCord(BasePlaneFacade) + domain contracts
├── brainstem/        # Brainstem(BasePlaneFacade) + domain contracts
├── communication/    # Lane definitions, Envelope wrapper
└── cerebrum/
    ├── cortex/       # Decision layer with L4/L5/L6 feedback
    └── subcortical/
        ├── thalamus/     # ThalamicEnvelope, RouteDecision, GateState
        │                 # See ARCHITECTURE_GOALS.md for nucleus-based target design
        ├── hypothalamus/ # HomeostaticState, RegulationDecision
        ├── basal_ganglia/# CandidateAction, SelectionDecision, BGPathway
        └── limbic/       # EpisodicMemoryTrace, RetrievalResult
```

## Design Patterns

1. **Contract-First**: All modules define Protocol classes before implementations
2. **BasePlaneFacade Pattern**: Planes inherit from `BasePlaneFacade` for consistent ingress/reject
   - Base knows: envelope/meta, reject contract, reflect topic
   - Base does NOT know: domain topics, channels, device mappings
   - Subclasses override `dispatch()` for domain-specific handling
3. **Type Validation**: Each layer validates inbound message types and emits RejectEvent on violations
4. **Frozen Dataclasses**: Immutable message types throughout
5. **Scope-Based Organization**: Everything is scoped (device/room/house/session)
6. **Idempotency**: Commands use `action_id` for deduplication
7. **Non-blocking Reflection**: Lane X failures don't affect primary flows

## Infrastructure Notes

Designed for 3-broker Mosquitto topology (not yet implemented):
- Broker 1 (Control): Lanes B, G, D - Port 18831
- Broker 2 (Driver): Lane A - Port 18832
- Broker 3 (Reliable): Lanes C, E, X - Port 18833

Cross-broker rule: Only transformed RelayBundles cross boundaries (no raw sensor floods).

## Expert Agents & Skills

This project uses specialized agents and skills for quality assurance:

### Agents (Deep Analysis)

| Agent | Purpose |
|-------|---------|
| `neuro-expert` | Neuroscience verification - KB management, codebase audits, brain-faithfulness |
| `brain-software-arch-expert` | Architecture stress-testing - 5 modes, pattern validation, bulletproof protocol |

### Skills (Quick Checks)

| Skill | Purpose |
|-------|---------|
| `/neuro-check` | Quick inline brain-faithfulness validation |
| `/arch-check` | Quick inline architecture pattern validation |

### Three-Way Discussion Model

For architectural decisions, both experts discuss WITH EACH OTHER before user decides:
- neuro-expert provides scientific backing (with citations)
- brain-software-arch-expert provides implementation patterns
- User observes, guides, and makes final decision

### Key Boundaries

- Experts do NOT write code (advise only)
- Experts do NOT make final decisions (user decides)
- All KB content assumed WRONG until verified against scientific papers

### Knowledge Base Prerequisite

**CRITICAL:** Do NOT proceed with implementation until the knowledge base is verified.

**Before Any Implementation:**
1. Check `docs/knowledgebase/brain/verified.md` for KB status
2. If files are UNVERIFIED or PENDING:
   - STOP implementation work
   - Run `neuro-expert` agent to verify KB first
   - Wait for verification to complete
3. Only proceed with implementation after KB verification is complete

**KB Status Reference:**

| Status | Meaning | Action |
|--------|---------|--------|
| VERIFIED | Checked against papers | Safe to use |
| PARTIAL | Some parts checked | Use only verified sections |
| UNVERIFIED | Not checked | DO NOT USE - verify first |
| PENDING | Awaiting verification | DO NOT USE - wait for verification |
| REJECTED | Found inaccurate | DO NOT USE - needs correction |

Full specification: `~/.claude/plans/eager-beaming-barto.md`

## Git Workflow

**NEVER work directly on the main branch.**

- Always create a feature branch before making changes
- Branch naming: `feature/<description>` or `fix/<description>`
- Only merge to main via pull request after review

## Keeping This File Current

**CRITICAL:** This file defines Claude's behavior on this project.

When decisions are made or requirements change:
1. Update CLAUDE.md IMMEDIATELY - do not defer
2. Ensure PROJECT_GOALS.md and CLAUDE.md stay in sync
3. If a decision contradicts this file, UPDATE this file
4. Never let agreed requirements exist only in conversation or plan files

**If you notice CLAUDE.md is missing agreed requirements:**
- Stop current work
- Update CLAUDE.md first
- Then continue

This prevents behavior drift across sessions.

## Reference Documents

- **Full Project Goals:** `docs/PROJECT_GOALS.md` (verification log, detailed specs)
- **Plan File:** `~/.claude/plans/eager-beaming-barto.md` (expert agent specs)
