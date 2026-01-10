# Architecture Audit Report (Mode A: Compliance)

**Date:** 2026-01-10
**Auditor:** brain-software-arch-expert
**Status:** PARTIAL COMPLIANCE

---

## Summary

| Category | Count |
|----------|-------|
| CRITICAL | 3 |
| MAJOR | 4 |
| MINOR | 4 |

---

## Critical Violations

### 1. Type Duplication - Contracts Source of Truth Violated

Multiple independent definitions of the same types exist:

| Type | Locations |
|------|-----------|
| `ScopeLevel` | `contracts_base_async.py`, `communication/contracts.py`, `basal_ganglia_async.py`, `limbic_async.py`, `hypothalamus_async.py`, `mock_cortex_async.py` |
| `NucleusId` | `communication/contracts.py`, `thalamus_async.py`, `mock_cortex_async.py` |
| `SignalKind` | `communication/contracts.py`, `thalamus_async.py`, `mock_cortex_async.py` |
| `GateState` | `communication/contracts.py`, `thalamus_async.py`, `mock_cortex_async.py` |
| `TopicBus` | `contracts_base_async.py`, `communication/contracts.py` |
| `InMemoryTopicBus` | `contracts_base_async.py`, `communication/contracts.py`, `mock_cortex_async.py` |

**Remediation:** Establish single canonical location in `src/shared/` for each shared type.

---

### 2. BasePlaneFacade Pattern NOT Applied to Most Components

| Component | Inherits BasePlaneFacade | File |
|-----------|-------------------------|------|
| SpinalCord | YES | `src/spinal_cord/contracts.py` |
| Brainstem | YES | `src/brainstem/contracts.py` |
| Thalamus | YES | `src/cerebrum/subcortical/thalamus/thalamus_async.py` |
| BasalGanglia | **NO** | `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py` |
| Limbic | **NO** | `src/cerebrum/subcortical/limbic/limbic_async.py` |
| Hypothalamus | **NO** | `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py` |
| MockCortex | **NO** | `src/cerebrum/cortex/mock_cortex_async.py` |

**Remediation:** All plane components must inherit from BasePlaneFacade.

---

### 3. Missing MessageType Definitions for Subcortical Components

The `MessageType` enum does not include types for:
- BasalGanglia (CandidateAction, SelectionDecision, StopDecision, etc.)
- Limbic (EpisodicMemoryTrace, RetrievalResult, SalienceTag, etc.)
- Hypothalamus (SignalEnvelope, HomeostaticState, RegulationDecision, etc.)

**Remediation:** Add all subcortical message types to the MessageType enum.

---

## Major Violations

### 4. Communication Lanes Not Integrated with Components

The `Lane` enum is defined but:
- None of the plane components reference or use the Lane enum
- Topic naming does not incorporate lanes
- Components don't use the Envelope wrapper

**Remediation:** Components must use Envelope wrapper and route based on Lane.

---

### 5. Four Concurrent Loops NOT Implemented

| Loop | Status |
|------|--------|
| A: Cortex <-> Thalamus <-> Cortex | Skeleton only |
| B: Cortex -> BG -> Thalamus -> Cortex | Skeleton only |
| C: Cortex -> Cerebellum -> Thalamus -> Cortex | Cerebellum MISSING |
| D: Limbic -> Hypothalamus -> Brainstem -> Body | Skeleton only |

Thalamus `dispatch` method is empty (`pass`).

**Remediation:** Implement dispatch logic. Start with Loop D (foundation-up per V24).

---

### 6. Cerebellum Component Missing Entirely

No `src/cerebellum/` directory exists. Loop C cannot function.

**Remediation:** Create cerebellum contracts skeleton following BasePlaneFacade pattern.

---

### 7. Channel vs Nucleus Addressing Conflict

Two competing models exist:
- Channel-based in `channels_async.py` (duplicate files in shared/ and thalamus/)
- Nucleus-based in `thalamus_async.py`

V25 states: "Thalamus: Nucleus-based from scratch (Option A)"

**Remediation:** Remove channel-based files or create channel-to-nucleus mapping layer.

---

## Minor Violations

### 8. Duplicate Channel Files

`src/shared/channels_async.py` and `src/cerebrum/subcortical/thalamus/channels_async.py` are identical.

### 9. No Test Files

`tests/` directory contains no tests. Cannot verify component isolation.

### 10. Idempotency Keys Not Consistently Applied

Only `EfferentCommand` has `action_id`. Other command types lack deduplication keys.

### 11. Meta Field Missing from Subcortical Dataclasses

SpinalCord/Brainstem messages have `meta: Meta`, subcortical messages do not.

---

## Compliance Summary

| Pattern | Status |
|---------|--------|
| BasePlaneFacade | PARTIAL (3/7) |
| Contracts-first | VIOLATED |
| Frozen dataclasses | COMPLIANT |
| Drivers vs Modulators | COMPLIANT |
| Scope-based organization | COMPLIANT |
| Idempotency | PARTIAL |
| No blocking in async | COMPLIANT |
| Communication Lanes | NOT IMPLEMENTED |
| Four Concurrent Loops | NOT IMPLEMENTED |
| Nucleus-based Thalamus | PARTIAL |

---

## Prioritized Remediation Plan

### Phase 1: Fix Foundation (CRITICAL)
1. Consolidate type definitions to `src/shared/`
2. Extend MessageType enum
3. Apply BasePlaneFacade to all components

### Phase 2: Enable Communication (MAJOR)
4. Integrate Lane routing
5. Resolve channel vs nucleus conflict
6. Create Cerebellum skeleton

### Phase 3: Implement Loops (MAJOR)
7. Implement Loop D first (foundation-up)
8. Implement Loop A
9. Implement Loop B
10. Implement Loop C

### Phase 4: Quality (MINOR)
11. Add unit tests
12. Add idempotency keys to all command types
13. Add Meta field to all message types
