# Architecture Audit Report

**Date:** 2026-01-10
**Auditor:** brain-software-arch-expert (Mode B: Discover/Document)
**Status:** PARTIAL COMPLIANCE

---

## Executive Summary

The brain-mimc codebase is in **early Phase 1** - contracts and minimal stubs exist for most components. Architecture documentation (CLAUDE.md, PROJECT_GOALS.md) is comprehensive, but implementation has significant gaps.

---

## Critical Issues

### 1. Four Concurrent Loops NOT IMPLEMENTED

| Loop | Path | Status |
|------|------|--------|
| A | Cortex <-> Thalamus <-> Cortex | Contracts exist, no runner |
| B | Cortex -> BG -> Thalamus -> Cortex | Contracts exist, no runner |
| C | Cortex -> Cerebellum -> Thalamus -> Cortex | **CEREBELLUM DOES NOT EXIST** |
| D | Limbic -> Hypothalamus -> Brainstem -> Body | Contracts exist, no runner |

No `asyncio.gather()` or equivalent for concurrent loop execution exists.

### 2. Cerebellum Missing Entirely

```
src/cerebrum/subcortical/
├── basal_ganglia/
├── hypothalamus/
├── limbic/
└── thalamus/
# NO cerebellum/
```

Loop C cannot be implemented without Cerebellum.

### 3. No Test Coverage

`tests/` directory is empty - no test coverage exists.

---

## Major Issues

### 4. BasePlaneFacade Pattern - Partial Compliance

**Compliant (inherit BasePlaneFacade):**
- `SpinalCord` - `src/spinal_cord/contracts.py:139`
- `Brainstem` - `src/brainstem/contracts.py:95`
- `Thalamus` - `src/cerebrum/subcortical/thalamus/thalamus_async.py:175`

**Non-Compliant (do NOT inherit BasePlaneFacade):**
- `BasalGanglia` - `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py:207`
- `Hypothalamus` - `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py:120`
- `Limbic` - `src/cerebrum/subcortical/limbic/limbic_async.py:250`
- `MockCortex` - `src/cerebrum/cortex/mock_cortex_async.py:168`

### 5. Channel vs Nucleus Conflict

Two competing models exist in thalamus:

| Model | File | Approach |
|-------|------|----------|
| Nucleus-Based (correct per V25) | `thalamus_async.py` | Uses `NucleusId`, `NucleusClass` |
| Channel-Based (contradicts V25) | `channels_async.py` | Uses `Channel` enum |

V25 explicitly states: "Thalamus: Nucleus-based from scratch (Option A)"

### 6. Lane Usage Inconsistent

| Component | Topic Prefix | Uses Lane Enum? |
|-----------|--------------|-----------------|
| SpinalCord | `/sc/` | No |
| Brainstem | `/bs/` | No |
| Thalamus | `/th/` | No |
| communication | Uses Lane | Yes |

No unified topic convention across components.

---

## Minor Issues

### 7. ScopeLevel Duplication

`ScopeLevel` is defined in 6 different files instead of importing from `contracts_base_async.py`:

| File | Line |
|------|------|
| `contracts_base_async.py` | 52 (canonical) |
| `basal_ganglia_async.py` | 24 |
| `hypothalamus_async.py` | 49 |
| `limbic_async.py` | 10 |
| `mock_cortex_async.py` | 76 |
| `communication/contracts.py` | 61 |

---

## What Works Well

1. **Frozen Dataclasses** - All message types use `@dataclass(frozen=True)`
2. **Contracts-First** - Protocol classes defined before implementations
3. **BasePlaneFacade Pattern** - Correctly implemented for foundation components
4. **Driver/Modulator Separation** - `SignalKind` enum correctly differentiates
5. **"Raw Never Goes Up"** - Layer separation is correct in design
6. **Path Sanitization** - Topic construction validates path components

---

## Remediation Priority

Per V24 (Foundation-Up Development Order):

| Priority | Action | Severity |
|----------|--------|----------|
| 1 | Fix BasePlaneFacade inheritance for subcortical components | Major |
| 2 | Resolve Channel vs Nucleus conflict (nucleus wins per V25) | Major |
| 3 | Unify ScopeLevel imports | Minor |
| 4 | Create Cerebellum stub (at minimum contracts) | Critical |
| 5 | Implement Loop A as proof of concurrent pattern | Critical |
| 6 | Add tests for SpinalCord/Brainstem | Critical |

---

## Files Analyzed

- `src/shared/contracts_base_async.py`
- `src/shared/plane_base_async.py`
- `src/spinal_cord/contracts.py`
- `src/brainstem/contracts.py`
- `src/communication/contracts.py`
- `src/cerebrum/cortex/mock_cortex_async.py`
- `src/cerebrum/subcortical/thalamus/thalamus_async.py`
- `src/cerebrum/subcortical/thalamus/channels_async.py`
- `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py`
- `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py`
- `src/cerebrum/subcortical/limbic/limbic_async.py`
