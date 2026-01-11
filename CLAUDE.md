# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## STOP - READ BEFORE ANY ACTION

### Rule 0: Git Workflow (MANDATORY - NO EXCEPTIONS)

**Claude must NEVER commit directly to main.**

**BEFORE doing ANY work:**

```bash
# Step 1: Check current branch
git branch --show-current

# Step 2: If output is "main", STOP and create feature branch FIRST
git checkout -b feature/<task-name>

# Step 3: Only THEN proceed with work
```

**This applies to:**
- "Quick" changes
- "Small" fixes
- "Just one file" edits
- ALL changes, no matter how trivial

**Branch naming:**
- `feature/<description>` - new functionality
- `fix/<description>` - bug fixes

**Merge to main only when:**
1. Task is COMPLETE
2. Code works
3. You are ready to delete the feature branch

**Why:** Main stays stable. Incomplete work never pollutes main. Failed experiments are easy to abandon.

---

### Rule 1: Expert Consultation Protocol (MANDATORY)

**Claude must invoke the expert agents - NOT just present perspectives inline.**

#### Triggers - When This Rule Applies

You MUST follow this protocol when:
- Designing new components or modules
- Proposing changes to Core Principles (sections 1-12 below)
- Naming brain structures, pathways, or regions
- Adding or modifying connections between components
- Adding to Verified items (V-series in PROJECT_GOALS.md)
- Choosing implementation approach for any brain region
- Answering "should this be..." questions

#### The Protocol (Step-by-Step)

**Step 1: STOP**
Do not write code. Do not make the decision. Do not proceed.

**Step 2: Invoke BOTH expert agents (in parallel)**
Use the Task tool to launch both agents simultaneously:

```
Task(subagent_type="neuro-expert")
Task(subagent_type="brain-software-arch-expert")
```

Give each agent:
- The specific question/decision at hand
- Relevant context from the codebase
- Reference to CLAUDE.md and PROJECT_GOALS.md

**Step 3: Synthesize findings**
After both agents return, summarize their perspectives:

```
## Neuro-Expert Findings
[Summary of what neuro-expert reported]
- Key points
- Citations/sources
- Confidence level

## Architecture-Expert Findings
[Summary of what arch-expert reported]
- Key points
- Pattern recommendations
- Tradeoffs identified

## Tensions / Conflicts (if any)
[Where the two perspectives disagree or create tradeoffs]
```

**Step 4: WAIT for user decision**
End with: "How would you like to proceed?"
Do NOT proceed until user explicitly decides.

**Step 5: Document the decision**
After user decides:
- Update CLAUDE.md if it affects Core Principles
- Update PROJECT_GOALS.md V-series if it's a verified item
- Add inline comments in code referencing the decision

#### What Claude Must NEVER Do

- Make brain-faithfulness judgments without invoking neuro-expert
- Choose architecture patterns without invoking brain-software-arch-expert
- Present "perspectives" inline instead of actually invoking the agents
- Add verified items without user validation
- Assume silence means approval - always wait for explicit decision

#### Quick Checks (User-Initiated)

For lightweight questions, user can request skills instead of full agents:
- `/neuro-check` - Quick brain-faithfulness check (uses Skill tool)
- `/arch-check` - Quick architecture pattern check (uses Skill tool)

These skip the full protocol but still require Claude to present reasoning before user decides.

#### When to Use Agents vs Skills

| Situation | Use |
|-----------|-----|
| New component design | AGENTS (both) |
| Naming brain structures | AGENTS (neuro-expert) |
| "Is this pattern correct?" | SKILL (/arch-check) |
| "Is this brain-faithful?" | SKILL (/neuro-check) |
| Changes to Core Principles | AGENTS (both) |
| Deep analysis needed | AGENTS |
| Quick validation | SKILLS |

---

## Project Overview

brain-mimc is a brain-inspired software framework modeling hierarchical, asynchronous communication inspired by neural anatomy. The system implements all major brain regions as independent, concurrent components communicating non-blocking.

The brain is divided into:
- **Cerebrum** (with Cortex, Thalamus, Basal Ganglia, Limbic System, Hypothalamus)
- **Cerebellum**
- **Brainstem**
- **Spinal Cord**

## Core Principles (NON-NEGOTIABLE)

### 1. Full Parallelism

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

### 2. Major Loops (Examples - More Exist)

| Loop | Path | Purpose |
|------|------|---------|
| A | Cortex - Thalamus - Cortex | Routing + Attention |
| B | Cortex - BG - Thalamus - Cortex | Action Selection |
| C | Cortex - Cerebellum - Thalamus - Cortex | Calibration |
| D | Limbic - Hypothalamus - Brainstem - Body | Regulation |
| E | Hippocampus - Mammillary - Ant. Thalamus - Cingulate - Hippocampus | Memory (Papez) |

Loops also exist within subcortical parts and between regions.

### 3. Thalamus: Nucleus-Based Architecture

**NOT just channels - requires nucleus-based addressing:**

| Class | Nuclei | Role |
|-------|--------|------|
| First-order | LGN, MGN, VPL/VPM, VA/VL | Relay external world to primary cortex L4 |
| Higher-order | Pulvinar, MD, LP/LD | Cortex-to-cortex routing (L5 to association cortex) |
| Diffuse | CM, Pf, CL, PVT | Arousal, state (brainstem to widespread cortex) |
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

### 6. Message + Context

Information flows as **messages** (what happened) with corresponding **context** (how to adjust the system).

- Messages carry content
- Context guides processing
- Messages don't change system state directly; context influences behavior

### 7. Safety Mechanisms

The system uses brain-inspired safety mechanisms. Actions are suppressed by default unless explicitly released.

### 8. Non-Blocking Communication

All communication must be non-blocking. Different communication channels exist based on system needs:
- Regular channels for normal operation
- Reflect-path (emergency channel) for critical communication

Communication method is flexible (async, non-blocking) - not locked to any specific technology.

### 9. Failure Modes (Brain-Faithful)

- **Critical infrastructure** (brainstem equivalents): Failure = system down
- **Processing components** (cortical equivalents): Failure = degraded function, not cascade
- **Redundant pathways** exist for most functions
- **No cascading failures** from peripheral component loss

### 10. Dual-Mode Communication (TONIC vs BURST)

Thalamic relay operates in TWO modes with DIFFERENT communication patterns. This is NOT optional - it's how the brain actually works.

| Mode | When Active | TRN Behavior | Communication Pattern |
|------|-------------|--------------|----------------------|
| TONIC | Alert, sustained attention | Graded inhibition | Publish-on-change, rate-coded, near-continuous |
| BURST | Sleep, drowsy, attention shifts | Oscillatory (7-14 Hz) | Rhythmic packets, discrete windows (~100ms on/off) |

**Key distinctions:**
- **TONIC mode**: High-fidelity relay. Messages flow based on sector gate level (0.0 to 1.0). Linear input-output.
- **BURST mode**: Salience detection. Messages only pass during "open" phase of burst cycle. Non-linear, packet-based.

**Implementation requirement:**
- `TRNMode.TONIC` and `TRNMode.BURST` MUST behave differently
- Thalamus relay logic must check operating mode and apply different patterns
- Both modes use discrete messages, but temporal patterns differ

**Source:** Cho et al. 2025 (TRN dual inhibitory network), Sherman 2016 (burst vs tonic relay modes)

### 11. Critically Decentralized with Emergent Decision-Making

**A critically decentralized system where outcomes EMERGE from the interaction of diverse regions rather than a single top-down command.** No central controller exists. The architecture IS the coordination.

| Mechanism | How It Works |
|-----------|--------------|
| **Convergence** | Multiple inputs → single node → must integrate |
| **Competition** | Winner-take-all → only one output (TRN: graded; BG: binary) |
| **Synchronization** | Same timing → same object/event (gamma binding) |
| **Global State** | Neuromodulators set mode for EVERYTHING (ACh, DA, NE, 5-HT) |
| **Shared Hubs** | Thalamus, Striatum = where loops MEET and integrate |

**The city analogy:**
- Not a CPU with a program
- More like a city with traffic patterns
- Roads (pathways) are fixed
- Traffic lights (TRN) control flow
- Weather (neuromodulators) affects everything
- Intersections (hubs) force integration

**Source:** one-system.md (reference doc)

### 12. First-Order / Higher-Order Flow

**First-order and higher-order nuclei do NOT connect directly. Cortex is the BRIDGE.**

```
External → First-order → Cortex L4
                            ↓
                        [processing]
                            ↓
                        Cortex L5 → Higher-order → Association Cortex
                            ↓
                        Cortex L6 → First-order (feedback)
```

| Nucleus Type | Driver Input | Output | Role |
|--------------|--------------|--------|------|
| First-order | SUBCORTICAL (raw) | Primary cortex L4 | Brings NEW info into system |
| Higher-order | CORTICAL L5 (processed) | Association cortex | Routes between cortical areas |

**Key insight:** First-order receives RAW input, cortex PROCESSES it, higher-order routes PROCESSED features.

**Source:** mutliple-order-flow.md (reference doc)

---

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
    | AfferentSignals (raw sensor data)
    v
Brainstem (Relay + Pattern + Global Broadcast)
    | RelayBundles (typed summaries)
    v
Thalamus (Gating/routing nucleus)
    | RouteDecision (to cortex areas/layers)
    v
Cortex (Decision/perception)
    | Commands (via motor path)
    v
SpinalCord (Efferent actuator commands)

Subcortical modules:
  - Hypothalamus: homeostasis regulation (fast autonomic vs slow endocrine)
  - Basal Ganglia: action selection with default suppression (safe-by-default)
  - Limbic: memory/salience/emotion
```

### Major Loops (Target Architecture)

See `src/cerebrum/subcortical/thalamus/ARCHITECTURE_GOALS.md` for full details.

- **Loop A**: Cortex - Thalamus - Cortex (routing + attention coordination)
- **Loop B**: Cortex - Basal Ganglia - Thalamus - Cortex (action selection)
- **Loop C**: Cortex - Cerebellum - Thalamus - Cortex (timing/calibration)
- **Loop D**: Limbic - Hypothalamus - Brainstem (body regulation)
- **Loop E**: Hippocampus - Mammillary Bodies - Anterior Thalamus - Cingulate - Hippocampus (memory/Papez circuit)

### Communication Lanes

| Lane | Purpose | Direction |
|------|---------|-----------|
| A (DRIVER) | Payload/content | SpinalCord to Brainstem to Thalamus to Cortex |
| B (MODULATOR) | Feedback/attention control | Cortex to Thalamus/TRN |
| C (COMMAND) | Motor commands | Cortex to Brainstem to SpinalCord |
| D (GLOBAL MODES) | Neuromodulators | Hypothalamus/Brainstem to ALL |
| E (ERROR/OUTCOME) | Learning signals | SpinalCord/Limbic to Cortex/BG |
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
+-- shared/
|   +-- contracts_base_async.py  # Core types, TopicBus, RejectEvent
|   +-- plane_base_async.py      # BasePlaneFacade (ingress/reject logic)
|   +-- topics_async.py          # Shared topic helpers
+-- spinal_cord/      # SpinalCord(BasePlaneFacade) + domain contracts
+-- brainstem/        # Brainstem(BasePlaneFacade) + domain contracts
+-- communication/    # Lane definitions, Envelope wrapper
+-- cerebrum/
    +-- cortex/       # Decision layer with L4/L5/L6 feedback
    +-- subcortical/
        +-- thalamus/     # ThalamicEnvelope, RouteDecision, GateState
        |                 # See ARCHITECTURE_GOALS.md for nucleus-based target design
        +-- hypothalamus/ # HomeostaticState, RegulationDecision
        +-- basal_ganglia/# CandidateAction, SelectionDecision, BGPathway
        +-- limbic/       # EpisodicMemoryTrace, RetrievalResult
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

## Knowledge Base

Location: `docs/knowledgebase/brain/` (24 content files)

**Status tracking:** `docs/knowledgebase/brain/verified.md`

| Status | Meaning | Action |
|--------|---------|--------|
| VERIFIED | Checked against papers | Safe to use |
| PARTIAL | Some parts checked | Use only verified sections |
| UNVERIFIED | Not checked | State uncertainty when using |
| PENDING | Awaiting verification | State uncertainty when using |
| REJECTED | Found inaccurate | DO NOT USE - needs correction |

When using KB content in Expert Consultation Protocol, always state the verification status.

## Expert Agents

Location: `.claude/agents/`

| Agent | Model | Purpose |
|-------|-------|---------|
| `neuro-expert` | Opus | Neuroscience verification, KB management, brain-faithfulness |
| `brain-software-arch-expert` | Opus | Architecture stress-testing, pattern validation, bulletproof protocol |

**Invocation:** Use Task tool with `subagent_type` parameter.

**Key boundaries:**
- Agents advise only - they do NOT write code
- Agents do NOT make final decisions - user decides
- All KB content assumed WRONG until verified against scientific papers

## Skills (Quick Checks)

Location: `.claude/skills/`

| Skill | Purpose |
|-------|---------|
| `/neuro-check` | Quick inline brain-faithfulness validation |
| `/arch-check` | Quick inline architecture pattern validation |

**Invocation:** User types the skill command, Claude uses Skill tool.

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

## Audit History

Location: `docs/audits/audit-merged-2026-01-11.md`

| Date | Score | Key Findings |
|------|-------|--------------|
| 2026-01-11 | 7/10 neuro, ~35% arch | Merged audit with verified findings |

Consolidated from 5 original audits (neuro, arch, combined, gatestate, lanes-planes).

**Key decisions from 2026-01-11 audits:**
- Deleted regressed feature branch (was channel-based, main has correct nucleus-based foundation) - DONE
- Add Loop E (Papez/Memory circuit) - DONE
- Delete channel files (not brain-faithful) - DONE

## Current Status (2026-01-11 Checkpoint)

### Completed
- [x] Loop Zero demo (3 processes, MQTT, concurrent proof-of-concept)
- [x] 3 KB updates (TRN heterogeneity, L5→TRN pathway, Core/Matrix note)
- [x] Thalamus architecture document (866 lines)
- [x] 10 thalamus reference documents (~8K lines)
- [x] Core Principles 10-12 (Dual-mode, Emergent Integration, FO/HO Flow)

### Design Insights Documented
1. NO central controller - integration EMERGES from architecture
2. 5 integration mechanisms: Convergence, Competition, Synchronization, Global State, Shared Hubs
3. 6 major loops through thalamus (not just 5)
4. Multi-input nuclei require integration logic (VL, MD, Pulvinar)
5. First-order ≠ Higher-order direct - Cortex is the bridge
6. 10 things still missing (see What-Missing.md)

### Next Implementation Steps (Updated per thalamus_abstraction_filter.md)

| Priority | Component | Pattern | Status |
|----------|-----------|---------|--------|
| 1 | Base `RelayModule` class | Foundation for all relays | TODO |
| 2 | `TRNSector` (synchronized) | Sector-level gating via gap junctions | TODO |
| 3 | `ParallelChannelRelay` | M/P/K streams (same input → different processing) | TODO |
| 4 | `Pulvinar` subdivisions | PuI/PuL/PuM/PuA with different I/O | TODO |
| 5 | `MD` subdivisions | MDmc/MDpc/MDdc (emotion/exec/eye) | TODO |
| 6 | `PreFilter` (optional) | Interneuron abstraction | TODO |
| 7 | `TopographicRelay` (optional) | Only if spatial data needed | TODO |

**Key patterns from abstraction filter:**
- Parallel channels: Same relay, multiple processing streams
- Subdivisions: Higher-order modules have sub-components with different I/O
- TRN synchronization: Gating is per-sector, not per-relay

**HIGH Priority (from audits):**
- GateState refactor: TRNSector enum, dual inhibition, TONIC/BURST modes
- Fix type duplication (ScopeLevel in 6 files, GateState in 3 files, InMemoryTopicBus in 3 files)
- Fix type imports in mock_cortex_async.py and communication/contracts.py
- Change Brainstem RelayBundle: `channel: str` → `target_nucleus: NucleusId`
- Add BasePlaneFacade to BG, Limbic, Hypothalamus
- Extend Plane enum (BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS, CEREBELLUM)

**MEDIUM Priority (from audits):**
- Add NucleusId entries (AN, REUNIENS)
- Create cerebellum skeleton for Loop C
- Implement routing logic (Thalamus dispatch empty, TRN gating empty)

**LOW Priority (from audits):**
- Add Meta fields to subcortical messages
- Add spinal cord laminae enum
- Add reticular formation contracts
- Add neuromodulator explicit contracts
- Document canonical type locations in CLAUDE.md

## Reference Documents

- **Full Project Goals:** `docs/PROJECT_GOALS.md` (verification log, detailed specs)
- **Thalamus Architecture:** `docs/architecture/cerebrum/subcortical-thalamus/thalamus-architecture.md` (866 lines - comprehensive design)
- **Thalamus Reference Docs:** `docs/knowledgebase/subcortical-thalamus/` (11 files, ~9K lines)
  - `thalamus_abstraction_filter.md` - **Implementation priority** (what matters for software)
  - `one-system.md` - Emergent integration, no central controller
  - `mutliple-order-flow.md` - First-order → Cortex → Higher-order flow
  - `What-Missing.md` - 10 things still to address
  - `challanges_thalamus_framework.md` - Implementation challenges
  - `All-Major-Loops-Through-Thalamus.md` - 6 loops with code
  - `Complete-thamalus-Framework.md` - Full Python framework
- **Audit Files:** `docs/audits/` (neuro-expert and arch-expert findings)
- **Interface Specs:** `docs/interface_specs.md` (nucleus-based contracts, converged GateState)
- **Topics & Contracts:** `docs/topics_and_contracts.md` (MQTT topic structure)
- **Lane Profiles:** `docs/architecture/lane_profiles.md` (message envelope policies)
- **Broker Policy:** `docs/broker_boundary_bridge_policy.md` (tract boundary rules)
- **Mosquitto Guide:** `docs/mosquitto_brain_like_communication.md` (infrastructure)
