# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

brain-mimc is a brain-inspired software architecture modeling hierarchical, asynchronous communication inspired by neural anatomy. It uses a pub-sub model with multiple "planes" (lanes) similar to neural tracts for IoT/home automation.

**Core Principle:** "Raw never goes up" - sensor data is transformed into typed summaries at each level before passing to higher layers.

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

### Key Contracts (`src/shared/contracts_base_async.py`)

- `ScopeLevel`: DEVICE, ROOM, HOUSE, USER_SESSION
- `Plane`: SPINAL, BRAINSTEM, THALAMIC, CORTICAL
- `MessageType`: AFFERENT_SIGNAL, EFFERENT_COMMAND, RELAY_BUNDLE, etc.
- `TopicBus` Protocol: async publish/subscribe interface
- `InMemoryTopicBus`: reference implementation for testing

### Source Layout

```
src/
├── shared/           # Base types, TopicBus protocol, topic helpers
├── spinal_cord/      # AfferentSignal, EfferentCommand, ReflexRule
├── brainstem/        # RelayBundle, PatternTrigger, GlobalBroadcast
├── communication/    # Lane definitions, Envelope wrapper
└── cerebrum/
    ├── cortex/       # Decision layer with L4/L5/L6 feedback
    └── subcortical/
        ├── thalamus/     # ThalamicEnvelope, RouteDecision, GateState
        ├── hypothalamus/ # HomeostaticState, RegulationDecision
        ├── basal_ganglia/# CandidateAction, SelectionDecision, BGPathway
        └── limbic/       # EpisodicMemoryTrace, RetrievalResult
```

## Design Patterns

1. **Contract-First**: All modules define Protocol classes before implementations
2. **Type Validation**: Each layer validates inbound message types and emits RejectEvent on violations
3. **Frozen Dataclasses**: Immutable message types throughout
4. **Scope-Based Organization**: Everything is scoped (device/room/house/session)
5. **Idempotency**: Commands use `action_id` for deduplication
6. **Non-blocking Reflection**: Lane X failures don't affect primary flows

## Infrastructure Notes

Designed for 3-broker Mosquitto topology (not yet implemented):
- Broker 1 (Control): Lanes B, G, D - Port 18831
- Broker 2 (Driver): Lane A - Port 18832
- Broker 3 (Reliable): Lanes C, E, X - Port 18833

Cross-broker rule: Only transformed RelayBundles cross boundaries (no raw sensor floods).
