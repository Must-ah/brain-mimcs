# Combined Audit: Three-Way Discussion (2026-01-11)

**Participants:** neuro-expert + brain-software-arch-expert + User
**Question:** Does this codebase follow how the human brain actually works?
**Method:** Parallel expert analysis with combined synthesis

---

## Executive Summary

| Aspect | Verdict |
|--------|---------|
| **Design Intent** | BRAIN-FAITHFUL |
| **Implementation** | HAS CRITICAL ISSUES |
| **Overall Score** | 7/10 (neuro) + 31% compliant (arch) |

---

## AGREED BY BOTH EXPERTS

| Issue | Neuro-Expert | Arch-Expert | Action |
|-------|--------------|-------------|--------|
| Nucleus-based thalamus | BRAIN-FAITHFUL | CORRECT pattern | KEEP |
| Driver/Modulator distinction | BRAIN-FAITHFUL | CORRECT pattern | KEEP |
| BG GO/NO-GO/STOP pathways | BRAIN-FAITHFUL | CORRECT design | KEEP |
| Cortex L4/L5/L6 semantics | BRAIN-FAITHFUL | CORRECT implementation | KEEP |
| channels_async.py | NOT BRAIN-FAITHFUL | REDUNDANT | DELETE |
| Four loops | Correct design | Not connected yet | WIRE |

---

## NEURO-EXPERT FINDINGS

### Brain-Faithful Components

| Component | Verdict | Scientific Basis |
|-----------|---------|------------------|
| Thalamus (thalamus_async.py) | BRAIN-FAITHFUL | Nucleus classes match Sherman & Usrey 2024 |
| Basal Ganglia | BRAIN-FAITHFUL | Three pathways per Nambu 2002, Graybiel 2025 |
| Limbic | BRAIN-FAITHFUL | Hippocampal subfields per Squire & Zola-Morgan |
| Hypothalamus | BRAIN-FAITHFUL | Modules and dual output correct |
| Brainstem | BRAIN-FAITHFUL | "Raw never goes up" principle correct |
| Spinal Cord | BRAIN-FAITHFUL | Afferent/efferent distinction correct |

### NOT Brain-Faithful

| Component | Problem | Scientific Basis |
|-----------|---------|------------------|
| channels_async.py | Brain uses NUCLEI, not channels | Sherman 2024: "Thalamus organized by nuclei with specific connectivity" |

### Sources Used
- LOCAL: Sherman & Usrey 2024 (Transthalamic Pathways)
- LOCAL: Cho et al. 2025 (TRN dual inhibitory network)
- LOCAL: Nguyen & Person 2025 (Cerebellar circuits)
- KB: All 24 verified files

---

## ARCH-EXPERT FINDINGS

### Correct Patterns

| Pattern | Files | Status |
|---------|-------|--------|
| BasePlaneFacade inheritance | thalamus_async.py | CORRECT |
| Nucleus-based addressing | thalamus_async.py | CORRECT |
| Driver vs Modulator | thalamus_async.py, mock_cortex_async.py | CORRECT |
| Frozen dataclasses | All | CORRECT |
| Async throughout | All | CORRECT |
| Lane definitions | communication/contracts.py | CORRECT |

### CRITICAL Violations

| Issue | Files Affected | Impact |
|-------|----------------|--------|
| ScopeLevel duplication | 6 files | Type safety broken |
| InMemoryTopicBus duplication | 3 files | Bug propagation risk |
| Missing BasePlaneFacade | BG, Limbic, Hypothalamus | No ingress validation |
| Plane enum incomplete | contracts_base_async.py | Can't register subcortical planes |

### Compliance Score
- Compliant: 4 files (31%)
- Partial: 5 files (38%)
- Non-Compliant: 4 files (31%)

---

## COMBINED RECOMMENDATIONS

### HIGH Priority (DELETE)

Both experts agree these files should be deleted:

1. `src/shared/channels_async.py`
   - Neuro: Not brain-faithful (brain uses nuclei)
   - Arch: Redundant, creates confusion

2. `src/cerebrum/subcortical/thalamus/channels_async.py`
   - Same reasoning

3. `src/cerebrum/subcortical/thalamus/thalamus_topics_channels_async.py`
   - Same reasoning, plus broken imports

### HIGH Priority (FIX)

Arch-expert identified critical pattern violations:

1. **Remove ScopeLevel duplicates** (5 files)
   - Keep only `src/shared/contracts_base_async.py`
   - All others must import from there

2. **Remove type duplicates** (NucleusId, SignalKind, GateState, etc.)
   - Canonical: `src/cerebrum/subcortical/thalamus/thalamus_async.py`
   - Others must import

3. **Add BasePlaneFacade inheritance**
   - `BasalGanglia(BasePlaneFacade)`
   - `Limbic(BasePlaneFacade)`
   - `Hypothalamus(BasePlaneFacade)`

4. **Extend Plane enum**
   - Add: BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS, CEREBELLUM

### MEDIUM Priority (UPDATE)

Neuro-expert identified brain-faithfulness gaps:

1. **TRN dual inhibition** - Add GPe→TRN and SOM→PV fields to GateState
2. **Missing cerebellum** - Create skeleton for Loop C
3. **Loop wiring** - Connect components for four concurrent loops

---

## TENSIONS / CONFLICTS

### GateState Definition Conflict

**Neuro-expert wants:** Add dual inhibition fields
```python
gpe_inhibition: Optional[float]  # Extrinsic (BG pathway)
intra_trn_inhibition: Optional[float]  # Intrinsic (SOM→PV)
```

**Arch-expert found:** Two incompatible GateState definitions exist
- `thalamus_async.py`: No `expires_at_ms`
- `communication/contracts.py`: Has `expires_at_ms`

**Resolution needed:** First reconcile the two definitions, then add neuro fields.

---

## SUMMARY TABLE

| Category | Count | Examples |
|----------|-------|----------|
| KEEP (brain-faithful + correct pattern) | 7 | Nucleus enums, BG pathways, layer semantics |
| DELETE (not brain-faithful) | 3 | Channel files |
| FIX (pattern violations) | 6 | Type duplication, BasePlaneFacade |
| UPDATE (incomplete) | 4 | TRN gating, cerebellum, loop wiring |

---

## NEXT STEPS (User Decision)

1. **Delete channel files?** Both experts: YES
2. **Fix type duplication?** Arch: CRITICAL priority
3. **Add BasePlaneFacade?** Arch: CRITICAL priority
4. **Add TRN dual inhibition?** Neuro: MEDIUM priority

---

## Audit Metadata

- **Date:** 2026-01-11
- **Auditors:** neuro-expert (Opus), brain-software-arch-expert (Opus)
- **Method:** Three-Way Discussion (parallel analysis)
- **Files examined:** 14 Python files
- **Sources:** Local papers + verified KB + CLAUDE.md
