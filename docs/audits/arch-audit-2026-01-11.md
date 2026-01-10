# Architecture Audit: 2026-01-11

**Auditor:** brain-software-arch-expert (Mode A)
**Method:** Code -> Pattern compliance audit
**CLAUDE.md Status:** Issues found (type duplication not documented)
**Compliance Score:** 31% Compliant, 38% Partial, 31% Non-Compliant

---

## Summary

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 2 | Type duplication causing type safety issues |
| MAJOR | 9 | Pattern violations, incompatible definitions |
| MINOR | 3 | Documentation gaps |

---

## CRITICAL Findings

### C1: ScopeLevel Type Duplication (6 definitions)

**Pattern Violated:** Single source of truth for types

**Files with duplicate definitions:**
| File | Line | Status |
|------|------|--------|
| `src/shared/contracts_base_async.py` | 52-56 | CANONICAL |
| `src/communication/contracts.py` | 61-65 | DUPLICATE |
| `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py` | 24-28 | DUPLICATE |
| `src/cerebrum/subcortical/limbic/limbic_async.py` | 10-14 | DUPLICATE |
| `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py` | 49-53 | DUPLICATE |
| `src/cerebrum/cortex/mock_cortex_async.py` | 76-80 | DUPLICATE |

**Impact:**
- Type comparisons may fail (different enum instances)
- Changes to canonical definition won't propagate
- Breaks type consistency across components

**Verdict:** CRITICAL - DELETE all duplicates. Import from `src/shared/contracts_base_async.py`.

---

### C2: InMemoryTopicBus Type Duplication (3 definitions)

**Pattern Violated:** Single source of truth for implementations

**Files with duplicate definitions:**
| File | Line | Status |
|------|------|--------|
| `src/shared/contracts_base_async.py` | 121-159 | CANONICAL |
| `src/communication/contracts.py` | 199-230 | DUPLICATE |
| `src/cerebrum/cortex/mock_cortex_async.py` | 13-53 | DUPLICATE |

**Impact:**
- Bug fixes won't propagate
- Three nearly-identical implementations to maintain
- Inconsistent behavior possible

**Verdict:** CRITICAL - DELETE duplicates. Import from canonical location.

---

## MAJOR Findings

### M1: BasalGanglia Does NOT Inherit BasePlaneFacade

**File:** `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py`

**CLAUDE.md States:** "BasePlaneFacade Pattern: Planes inherit from `BasePlaneFacade`"

**Current Code:** Standalone class, no inheritance.

**Verdict:** Either BG is NOT a plane (internal processing) or it SHOULD inherit BasePlaneFacade. Needs clarification.

---

### M2: Limbic Does NOT Inherit BasePlaneFacade

**File:** `src/cerebrum/subcortical/limbic/limbic_async.py`

**Same issue as M1.**

---

### M3: Hypothalamus Does NOT Inherit BasePlaneFacade

**File:** `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py`

**Same issue as M1.**

---

### M4: NucleusId Type Duplication

**Files:**
- `src/cerebrum/subcortical/thalamus/thalamus_async.py` (CANONICAL)
- `src/communication/contracts.py` (DUPLICATE)
- `src/cerebrum/cortex/mock_cortex_async.py` (DUPLICATE)

**Verdict:** DELETE duplicates, import from thalamus_async.py.

---

### M5: SignalKind Type Duplication

**Files:**
- `src/cerebrum/subcortical/thalamus/thalamus_async.py` (CANONICAL)
- `src/communication/contracts.py` (DUPLICATE)
- `src/cerebrum/cortex/mock_cortex_async.py` (DUPLICATE)

**Verdict:** DELETE duplicates.

---

### M6: GateState INCOMPATIBLE Definitions

**Critical Difference:**
```python
# communication/contracts.py has:
expires_at_ms: int

# thalamus_async.py does NOT have expires_at_ms
```

**GateStore Protocol incompatibility:**
- Different method names (`get` vs `get_gate_state`)
- Different parameter order
- Different parameter sets

**Verdict:** MAJOR - Reconcile definitions, choose one canonical source.

---

### M7: CortexLayer Type Duplication

**Files:**
- `src/cerebrum/subcortical/thalamus/thalamus_async.py` (CANONICAL)
- `src/communication/contracts.py` (DUPLICATE)
- `src/cerebrum/cortex/mock_cortex_async.py` (DUPLICATE)

---

### M8: GateMode Type Duplication

**Files:**
- `src/cerebrum/subcortical/thalamus/thalamus_async.py` (CANONICAL)
- `src/communication/contracts.py` (DUPLICATE)
- `src/cerebrum/cortex/mock_cortex_async.py` (DUPLICATE)

---

### M9: Broken Import Paths

**File:** `src/cerebrum/subcortical/thalamus/thalamus_topics_channels_async.py`

```python
from contracts_base_async import ScopeLevel  # BROKEN - relative import fails
from channels_async import Channel, channel_selector  # BROKEN
```

**Verdict:** File has broken imports, will fail on import.

---

## MINOR Findings

### m1: Meta Field Missing in Subcortical Messages

BG, Limbic, Hypothalamus message types lack `meta: Meta` field that SpinalCord and Brainstem have.

### m2: Plane Enum Incomplete

`Plane` enum in contracts_base_async.py doesn't include BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS, CEREBELLUM.

### m3: Documentation Gap

CLAUDE.md doesn't specify where thalamic types (NucleusId, etc.) should be canonically defined.

---

## Compliance Verdicts by File

| File | Verdict | Issues |
|------|---------|--------|
| `src/shared/contracts_base_async.py` | COMPLIANT | Canonical source |
| `src/shared/plane_base_async.py` | COMPLIANT | Clean implementation |
| `src/shared/topics_async.py` | COMPLIANT | Simple, correct |
| `src/shared/channels_async.py` | NON-COMPLIANT | Should be deleted (neuro-audit) |
| `src/spinal_cord/contracts.py` | COMPLIANT | Proper imports |
| `src/brainstem/contracts.py` | COMPLIANT | Proper structure |
| `src/communication/contracts.py` | NON-COMPLIANT | 7 type duplications |
| `src/cerebrum/subcortical/thalamus/thalamus_async.py` | PARTIAL | Good types, empty dispatch |
| `src/cerebrum/subcortical/thalamus/channels_async.py` | NON-COMPLIANT | Delete (neuro-audit) |
| `src/cerebrum/subcortical/thalamus/thalamus_topics_channels_async.py` | NON-COMPLIANT | Broken imports, delete |
| `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py` | PARTIAL | Type duplication |
| `src/cerebrum/subcortical/limbic/limbic_async.py` | PARTIAL | Type duplication |
| `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py` | PARTIAL | Type duplication |
| `src/cerebrum/cortex/mock_cortex_async.py` | NON-COMPLIANT | 8 type duplications |

---

## Action Items Summary

### HIGH Priority

1. **Fix ScopeLevel duplication** - Delete 5 duplicate definitions
2. **Fix InMemoryTopicBus duplication** - Delete 2 duplicate definitions
3. **Delete channel files** (aligned with neuro-audit):
   - `src/shared/channels_async.py`
   - `src/cerebrum/subcortical/thalamus/channels_async.py`
   - `src/cerebrum/subcortical/thalamus/thalamus_topics_channels_async.py`

### MEDIUM Priority

4. **Reconcile GateState definitions** - Choose canonical, fix incompatibility
5. **Fix mock_cortex_async.py** - Import types instead of redefining
6. **Fix communication/contracts.py** - Import types instead of redefining
7. **Clarify BasePlaneFacade usage** - Are subcortical components "planes"?

### LOW Priority

8. **Add Meta field to subcortical messages**
9. **Extend Plane enum** for all components
10. **Document canonical type locations in CLAUDE.md**

---

## Cross-Reference with Neuro-Audit

| Issue | Neuro-Audit | Arch-Audit |
|-------|-------------|------------|
| Channel files | DELETE (not brain-faithful) | DELETE (broken imports) |
| Type duplication | Not covered | CRITICAL |
| BasePlaneFacade | Not covered | MAJOR |
| GateState fields | UPDATE (add dual inhibition) | MAJOR (reconcile versions) |

---

## Audit Metadata

- **Auditor:** brain-software-arch-expert (Mode A)
- **Date:** 2026-01-11
- **Files examined:** 14
- **Patterns checked:** BasePlaneFacade, Contract-first, Frozen dataclass, Single source of truth
