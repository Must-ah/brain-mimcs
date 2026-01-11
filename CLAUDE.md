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
- Proposing changes to Core Principles (sections 1-10 below)
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

brain-mimc is a brain-inspired software framework modeling hierarchical, asynchronous communication inspired by neural anatomy. It uses a pub-sub model with multiple "planes" (lanes) similar to neural tracts.

**Core Principle:** "Raw never goes up" - sensor data is transformed into typed summaries at each level before passing to higher layers.

## Core Principles (NON-NEGOTIABLE)

### 1. Full Parallelism

**Everything runs concurrently at every level of granularity.**

| Level | Parallel Units |
|-------|----------------|
| System | Cerebrum, Cerebellum, Brainstem, Spinal Cord |
| Region | Cortex, Thalamus, BG, Limbic, Hypothalamus |
| Sub-component | Each nucleus, each cortex layer, each pathway |
| Loop | A, B, C, D, E all run concurrently |
| Scope | Each room/device/session processes independently |

**No sequential pipelines. No blocking calls. No orchestrator.**

### 2. Five Major Loops (ALL CONCURRENT)

| Loop | Path | Purpose |
|------|------|---------|
| A | Cortex - Thalamus - Cortex | Routing + Attention |
| B | Cortex - BG - Thalamus - Cortex | Action Selection |
| C | Cortex - Cerebellum - Thalamus - Cortex | Calibration |
| D | Limbic - Hypothalamus - Brainstem - Body | Regulation |
| E | Hippocampus - Mammillary - Ant. Thalamus - Cingulate - Hippocampus | Memory (Papez) |

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

### 6. Drivers vs Modulators

- **Drivers** carry content (what happened)
- **Modulators** carry control (how to treat it)
- Drivers never change gates. Modulators influence but don't dictate.

### 7. Safe-by-Default

Basal ganglia suppresses all actions unless explicitly released.

### 8. Communication Pattern (Brain-Faithful)

The brain does NOT use continuous streaming. Transformation to discrete events happens at the sensor:
- **Retina**: Edge detection, contrast, motion to RGC spikes (not raw pixels)
- **Cochlea**: Frequency decomposition to spike patterns (not raw audio)
- **Mechanoreceptors**: Adaptation (onset/offset only) to nerve spikes

This validates:
- Typed async pub-sub over continuous streaming
- "Raw never goes up" at every level including sensors
- Publish-on-change pattern (like receptor adaptation)

### 9. Failure Modes (Brain-Faithful)

- **Critical infrastructure** (brainstem equivalents): Failure = system down
- **Processing components** (cortical equivalents): Failure = degraded function, not cascade
- **Redundant pathways** exist for most functions
- **No cascading failures** from peripheral component loss

### 10. Development Order (Foundation-Up)

Build components in brain-faithful order (per V24):

| Priority | Components | Rationale |
|----------|------------|-----------|
| HIGH (Foundation) | Spinal Cord, Brainstem | I/O + vital/arousal - everything depends on them |
| HIGH (Gateway) | Thalamus (nucleus-based) | Cannot route without nucleus addressing |
| MEDIUM (Processing) | Basal Ganglia, Cerebellum | Action selection + calibration |
| MEDIUM (Integration) | Limbic, Hypothalamus | Memory, emotion, homeostasis |
| LOWER | Cortex | Depends on ALL above |

**Phase Structure (per V23):**
- Phase 1: Contracts + Minimal Concurrent Stubs (all components exist from day one)
- Phase 2: Concurrent Elaboration (integration is continuous, not a final phase)

### 11. Dual-Mode Communication (TONIC vs BURST)

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
- **Audit Files:** `docs/audits/` (neuro-expert and arch-expert findings)
- **Interface Specs:** `docs/interface_specs.md` (nucleus-based contracts, converged GateState)
- **Topics & Contracts:** `docs/topics_and_contracts.md` (MQTT topic structure)
- **Lane Profiles:** `docs/architecture/lane_profiles.md` (message envelope policies)
- **Broker Policy:** `docs/broker_boundary_bridge_policy.md` (tract boundary rules)
- **Mosquitto Guide:** `docs/mosquitto_brain_like_communication.md` (infrastructure)
