# Branch Decision Audit: 2026-01-11

**Auditor:** neuro-expert
**Question:** Use feature/thalamus-nucleus-refactor or stay with main?
**Verdict:** STAY WITH MAIN - DELETE FEATURE BRANCH

---

## Comparison

| Aspect | Main | Feature Branch | Winner |
|--------|------|----------------|--------|
| Addressing | Nucleus-based (NucleusId) | Channel-based (Channel) | **MAIN** |
| Time expiry | None | expires_at_iso | **MAIN** |
| Inhibition | Single | Single | TIE (both need update) |
| GateMode | MULTI/WINNER_TAKE_ALL | MULTI/WINNER_TAKE_ALL | TIE (both need update) |

---

## Critical Finding

**The feature branch REGRESSED from nucleus-based to channel-based addressing.**

Despite the commit message "wip: thalamus refactor from channel-based to nucleus-based", the code in `thalamus_contracts_async.py` uses:
- `channel: Channel` (not nucleus-based)
- `expires_at_iso` (time-based expiry - not brain-faithful)

This is the **opposite** of brain-faithful design.

---

## Recommendation

| Decision | Action |
|----------|--------|
| Which branch? | **MAIN** (has correct nucleus-based foundation) |
| Feature branch? | **DELETE** (regressed to channel-based) |
| Next steps? | Apply converged GateState design to main |

---

## Scientific Basis

- **Cho et al. 2025**: TRN organized by sectors, dual inhibitory network (GPe + intra-TRN)
- **Sherman & Usrey 2024**: Nucleus-based routing, tonic/burst firing modes
- **KB Thalamus (VERIFIED)**: Sector organization corresponds to relay nuclei

---

## Next Steps (from converged GateState design)

| Priority | Change | Rationale |
|----------|--------|-----------|
| HIGH | Add TRNSector enum | Cho 2025: TRN has modality-specific sectors |
| HIGH | Add gpe_inhibition field | Cho 2025: GPe->TRN (100% neurons) |
| HIGH | Add intra_trn_inhibition field | Cho 2025: SOM->PV (18% sparse) |
| HIGH | Change GateMode to TONIC/BURST | Sherman: TRN firing modes |
| MEDIUM | Delete channel files | No anatomical basis |

---

## Audit Metadata

- **Date:** 2026-01-11
- **Auditor:** neuro-expert (Opus)
- **Branches compared:** main vs feature/thalamus-nucleus-refactor
- **Method:** Code -> Papers verification
- **Sources:** Cho et al. 2025 (LOCAL), Sherman 2024 (LOCAL), KB Thalamus (VERIFIED)
