# GateState Three-Way Discussion: 2026-01-11

**Participants:** neuro-expert + brain-software-arch-expert + User
**Topic:** GateState contract design for TRN (Thalamic Reticular Nucleus)
**Method:** True back-and-forth discussion (4 rounds)
**Outcome:** CONVERGED

---

## Background

The architecture audit (arch-audit-2026-01-11.md) found GateState defined in 3 files with INCOMPATIBLE definitions. The neuroscience audit (neuro-audit-2026-01-11.md) found the current single-inhibition model doesn't match the brain's dual inhibitory TRN architecture (Cho et al. 2025).

---

## Discussion Rounds

### Round 1: Neuro-Expert Opens

**Key Points:**
1. TRN has dual inhibitory inputs (not single):
   - **GPe→TRN**: Extrinsic, 100% prevalence, global gain control from BG
   - **Intra-TRN (SOM→PV)**: Intrinsic, sparse (8.7-18.6%), local sharpening

2. TRN is organized by SECTORS, not individual nuclei:
   - Visual sector → LGN
   - Auditory sector → MGN
   - Somatosensory sector → VPL, VPM
   - Motor sector → VL, VA
   - Limbic sector → MD, AN, Reuniens

3. TRN modes should be TONIC/BURST (not MULTI/WINNER_TAKE_ALL):
   - TONIC: Awake state, relay allowed
   - BURST: Sleep/deep attention, relay blocked

**Citation:** Cho et al. 2025 (LOCAL), Sherman & Usrey 2024 (LOCAL)

---

### Round 2: Arch-Expert Responds

**Agrees with neuro-expert on:**
- Dual inhibition model
- Sector organization
- TONIC/BURST modes

**Raises concerns:**
1. `effective_inhibition` is derived data - should NOT be stored in frozen dataclass
2. Type duplication must be resolved first - GateState exists in 3 files
3. Single source of truth needed in `src/shared/contracts_base_async.py`
4. Current NucleusId missing AN (anterior nucleus) and REUNIENS (midline)

**Questions for neuro-expert:**
1. Is there a formula for combining GPe + intra-TRN inhibition?
2. How do sectors map to nuclei? One-to-many or many-to-many?
3. Is GateMode per-sector or per-nucleus?
4. Is `expires_at_ms` brain-faithful?

---

### Round 3: Neuro-Expert Answers

**Q1: Formula for combining inhibition?**
A: NO formula. They have SEPARATE effects:
- GPe inhibition: Global gain (amplitude scaling)
- Intra-TRN inhibition: Local focus (winner-take-all sharpening)
Remove `effective_inhibition` - arch-expert is correct.

**Q2: Sector→nucleus mapping?**
A: One-to-many (sector contains multiple nuclei):
```
VISUAL → [LGN]
AUDITORY → [MGN]
SOMATOSENSORY → [VPL, VPM]
MOTOR → [VL, VA]
LIMBIC → [MD, AN, REUNIENS]
```

**Q3: Mode per-sector or per-nucleus?**
A: Per-SECTOR. TRN sectors operate as functional units.

**Q4: Is expires_at_ms brain-faithful?**
A: NO. TRN gating is EVENT-DRIVEN (stimulus-locked), not time-based expiry.
Remove `expires_at_ms`.

---

### Round 4: Arch-Expert Final Proposal

**AGREED design incorporating all findings:**

```python
class TRNSector(str, Enum):
    VISUAL = "visual"           # → LGN
    AUDITORY = "auditory"       # → MGN
    SOMATOSENSORY = "somatosensory"  # → VPL, VPM
    MOTOR = "motor"             # → VL, VA
    LIMBIC = "limbic"           # → MD, AN, Reuniens

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
    # NO effective_inhibition - derived, not stored
```

---

## Convergence Summary

| Aspect | OLD (Wrong) | NEW (Brain-Faithful) | Source |
|--------|-------------|----------------------|--------|
| Addressing | `nucleus: NucleusId` | `sector: TRNSector` | Cho et al. 2025 |
| Inhibition | Single `inhibition: float` | Dual: `gpe_inhibition` + `intra_trn_inhibition` | Cho et al. 2025 |
| Mode | `MULTI/WINNER_TAKE_ALL` | `TONIC/BURST` | Sherman 2016 |
| Expiry | `expires_at_ms` | Removed (event-driven) | Neuro-expert |
| Location | 3 incompatible files | Single source in shared/ | Arch-expert |

---

## Implementation Plan (Pending User Decision)

### Files to Modify

**DELETE duplicates:**
- `src/cerebrum/subcortical/thalamus/thalamus_async.py`: Remove GateState, GateMode
- `src/communication/contracts.py`: Remove GateState, GateMode
- `src/cerebrum/cortex/mock_cortex_async.py`: Remove GateState, GateMode

**ADD to `src/shared/contracts_base_async.py`:**
- `TRNSector` enum
- `TRNMode` enum
- New `GateState` dataclass

**UPDATE NucleusId:**
- Add `AN` (anterior nucleus)
- Add `REUNIENS` (midline)

---

## Scientific Sources

| Source | Type | Key Finding |
|--------|------|-------------|
| Cho et al. 2025 | LOCAL paper | TRN dual inhibitory network (GPe + intra-TRN) |
| Sherman & Usrey 2024 | LOCAL paper | Nucleus-based thalamic routing |
| Sherman 2016 | KB (VERIFIED) | TONIC/BURST firing modes |
| KB Thalamus | KB (VERIFIED) | TRN sector organization |

---

## Audit Metadata

- **Date:** 2026-01-11
- **Method:** True back-and-forth discussion (4 rounds)
- **Experts:** neuro-expert (Opus), brain-software-arch-expert (Opus)
- **Status:** CONVERGED - awaiting user decision to implement
