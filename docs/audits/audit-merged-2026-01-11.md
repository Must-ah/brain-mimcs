# Consolidated Audit: 2026-01-11

**Auditors:** neuro-expert + brain-software-arch-expert
**Method:** Three-way discussion with codebase verification
**Last Verified:** 2026-01-11

---

## Executive Summary

| Aspect | Score |
|--------|-------|
| Brain-Faithfulness | 7/10 |
| Architecture Compliance | ~35% |
| Design Intent | BRAIN-FAITHFUL |
| Implementation | HAS ISSUES |

---

## Brain-Faithful Components (KEEP)

| Component | File | Scientific Basis |
|-----------|------|------------------|
| Nucleus-based thalamus | `thalamus_async.py` | Sherman & Usrey 2024 |
| NucleusId enum (complete) | `thalamus_async.py:27-48` | First-order, higher-order, diffuse, gate classes |
| Driver/Modulator distinction | `thalamus_async.py:51-53` | Sherman 2016 |
| Cortex L4/L5/L6 semantics | `thalamus_async.py:56-59` | L4 receive, L5 HO driver, L6 modulator |
| BG GO/NO-GO/STOP pathways | `basal_ganglia_async.py:11-14` | Nambu 2002, Graybiel 2025 |
| Hippocampal subfields | `limbic_async.py:39-45` | Squire & Zola-Morgan 1991 |
| Hypothalamus modules | `hypothalamus_async.py:24-33` | SCN, PVN, LHA, etc. correct |
| Afferent/efferent distinction | `spinal_cord/contracts.py` | Fundamental sensory-in/motor-out |
| Lanes A-G | `communication/contracts.py` | Brain-faithful (see below) |

### Lanes Verification

| Lane | Purpose | Status |
|------|---------|--------|
| A_DRIVER | Ascending sensory | BRAIN-FAITHFUL |
| B_MODULATOR | Cortical feedback | BRAIN-FAITHFUL |
| C_COMMAND | Descending motor | BRAIN-FAITHFUL |
| D_GLOBAL | Neuromodulatory broadcast | BRAIN-FAITHFUL |
| E_ERROR | Error/learning signals | BRAIN-FAITHFUL (incomplete) |
| G_GATE | TRN gating | BRAIN-FAITHFUL |
| X_REFLECT | Audit/observability | Software infrastructure |
| V_VIDEO, U_AUDIO | Media lanes | Software infrastructure |

---

## DONE (Fixed)

| Item | Evidence |
|------|----------|
| Delete channel files | 3 files deleted, glob returns empty |
| Delete regressed feature branch | Branch deleted, only main exists |
| Add Loop E to docs | Added to CLAUDE.md and PROJECT_GOALS.md |

---

## Architecture Findings (CRITICAL)

### Type Duplication

| Type | Duplicates | Canonical Location |
|------|------------|-------------------|
| ScopeLevel | 6 files | `contracts_base_async.py:52` |
| InMemoryTopicBus | 3 files | `contracts_base_async.py:121` |
| GateState | 3 files (INCOMPATIBLE) | Needs reconciliation |
| NucleusId | 3 files | `thalamus_async.py:27` |
| SignalKind | 3 files | `thalamus_async.py:51` |
| GateMode | 3 files | `thalamus_async.py:62` |
| CortexLayer | 2 files | `thalamus_async.py:56` |

### Missing Patterns

| Issue | Files Affected |
|-------|----------------|
| BasePlaneFacade inheritance | basal_ganglia_async.py, limbic_async.py, hypothalamus_async.py |
| Plane enum incomplete | contracts_base_async.py (missing CEREBELLUM, BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS) |

---

## GateState Converged Design

Per expert discussion, the brain-faithful GateState should be:

```python
class TRNSector(str, Enum):
    VISUAL = "visual"           # -> LGN
    AUDITORY = "auditory"       # -> MGN
    SOMATOSENSORY = "somatosensory"  # -> VPL, VPM
    MOTOR = "motor"             # -> VL, VA
    LIMBIC = "limbic"           # -> MD, AN, Reuniens

class TRNMode(str, Enum):
    TONIC = "tonic"    # Awake: relay mode
    BURST = "burst"    # Sleep: block mode

@dataclass(frozen=True)
class GateState:
    scope: str
    scope_level: ScopeLevel
    sector: TRNSector              # Per-sector (not per-nucleus)
    gpe_inhibition: float          # Global gain from BG
    intra_trn_inhibition: float    # Local focus from lateral inhibition
    mode: TRNMode                  # TONIC/BURST
    reason: Optional[str]
    timestamp_ms: int
    # NO expires_at_ms - not brain-faithful
```

**Source:** Cho et al. 2025 (TRN dual inhibition), Sherman 2016 (TONIC/BURST)

---

## Action Items

### HIGH Priority

| Item | Details |
|------|---------|
| GateState refactor | Implement converged design with TRNSector, dual inhibition, TONIC/BURST |
| Fix type duplication | ScopeLevel (6 files), GateState (3 files), InMemoryTopicBus (3 files) |
| Fix type imports | mock_cortex_async.py, communication/contracts.py |
| Change Brainstem RelayBundle | `channel: str` -> `target_nucleus: NucleusId` |
| Add BasePlaneFacade | To BG, Limbic, Hypothalamus |
| Extend Plane enum | Add BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS, CEREBELLUM |

### MEDIUM Priority

| Item | Details |
|------|---------|
| Add NucleusId entries | AN, REUNIENS (for Papez circuit) |
| Create cerebellum skeleton | For Loop C (calibration) |
| Implement routing logic | Thalamus dispatch() is empty, TRN gating empty |
| Lane E sources | Add Brainstem (Inferior Olive) as error source |

### LOW Priority

| Item | Details |
|------|---------|
| Add Meta fields | To subcortical messages |
| Add spinal cord laminae | Enum for dorsal/ventral horn |
| Add reticular formation | Contracts for arousal systems |
| Add neuromodulator contracts | Explicit DA, NE, 5-HT, ACh |
| Consider interoceptive lane | I_INTERO or document A_DRIVER includes it |

---

## Sources

### Local Papers
- Cho et al. 2025: TRN dual inhibitory network (GPe + intra-TRN)
- Nguyen & Person 2025: Cerebellar circuit computations
- Sherman & Usrey 2024: Transthalamic pathways

### Knowledge Base (24 files VERIFIED)
- Sherman 2016: Thalamus central role
- Nambu 2002: BG hyperdirect pathway
- Alexander 1986: BG parallel loops
- Graybiel 2025: Basal ganglia surprises
- Squire & Zola-Morgan 1991: Medial temporal lobe memory
- LeDoux 2000: Emotion circuits

---

## Audit History

| Date | Action | Result |
|------|--------|--------|
| 2026-01-10 | Initial neuro audit | 7/10 brain-faithfulness |
| 2026-01-10 | Initial arch audit | 31% compliance |
| 2026-01-11 | Three-way discussion | Converged GateState design |
| 2026-01-11 | Channel files deleted | 3 files removed |
| 2026-01-11 | Re-verification | Findings confirmed, merged to single file |
