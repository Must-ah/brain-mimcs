# Neuroscience Audit: 2026-01-10

**Auditor:** neuro-expert
**KB Status:** FULLY VERIFIED (all 24 files)
**Brain-Faithfulness Score:** 7/10

## Summary

| Category | Count |
|----------|-------|
| KEEP | 12 |
| UPDATE | 8 |
| CHANGE | 5 |
| DELETE | 0 |
| RESTART | 0 |

---

## KEEP Findings (Brain-Faithful)

### Finding 1: Thalamus Nucleus Enumeration
**File:** `src/cerebrum/subcortical/thalamus/thalamus_async.py`
**Current:** `NucleusClass` enum with FIRST_ORDER, HIGHER_ORDER, DIFFUSE, GATE. `NucleusId` includes LGN, MGN, VPL/VPM, VA/VL, PULVINAR, MD, LP, CM, PF, TRN.
**Neuroscience:** Matches Sherman & Guillery (2006) classification.
**Category:** KEEP

### Finding 2: Driver/Modulator Distinction
**File:** `src/cerebrum/subcortical/thalamus/thalamus_async.py`
**Current:** `SignalKind` enum with DRIVER ("what happened") and MODULATOR ("how to treat it").
**Neuroscience:** Correct per Sherman (2016) - drivers carry content (5-10% synapses), modulators carry control (90-95%).
**Category:** KEEP

### Finding 3: Cortex Layer Semantics
**File:** `src/cerebrum/subcortical/thalamus/thalamus_async.py`, `src/cerebrum/cortex/mock_cortex_async.py`
**Current:** L4 = receive from thalamus, L5 = HO drivers, L6 = modulatory feedback.
**Neuroscience:** Correct per Purves et al. and Sherman & Usrey (2024).
**Category:** KEEP

### Finding 4: Basal Ganglia Pathways
**File:** `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py`
**Current:** DIRECT_GO, INDIRECT_NO_GO, HYPERDIRECT_STOP pathways.
**Neuroscience:** Matches Nambu et al. (2002) and Graybiel (2025).
**Category:** KEEP

### Finding 5: Basal Ganglia Four Loops
**File:** `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py`
**Current:** MOTOR, OCULOMOTOR, COGNITIVE, LIMBIC loops.
**Neuroscience:** Matches Alexander et al. (1986).
**Category:** KEEP

### Finding 6: Safe-by-Default BG Behavior
**File:** `src/cerebrum/subcortical/basal_ganglia/basal_ganglia_async.py`
**Current:** BG suppresses unless explicitly released.
**Neuroscience:** Correct - GPi/SNr tonically inhibit thalamus; action requires disinhibition.
**Category:** KEEP

### Finding 7: Hippocampal Subfields
**File:** `src/cerebrum/subcortical/limbic/limbic_async.py`
**Current:** ENTORHINAL -> DENTATE_GYRUS -> CA3 -> CA2 -> CA1 -> SUBICULUM.
**Neuroscience:** Correct trisynaptic circuit per Squire & Zola-Morgan (1991).
**Category:** KEEP

### Finding 8: Amygdala Nuclei Organization
**File:** `src/cerebrum/subcortical/limbic/limbic_async.py`
**Current:** LATERAL, BASAL, BASOLATERAL_COMPLEX, CENTRAL, MEDIAL, INTERCALATED.
**Neuroscience:** Correct per LeDoux (2000).
**Category:** KEEP

### Finding 9: Hypothalamus Dual Output
**File:** `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py`
**Current:** Fast autonomic vs slow endocrine pathways.
**Neuroscience:** Correct - autonomic (seconds) via brainstem, endocrine (minutes-hours) via pituitary.
**Category:** KEEP

### Finding 10: Hypothalamus Module Organization
**File:** `src/cerebrum/subcortical/hypothalamus/hypothalamus_async.py`
**Current:** SCN, PVN, SON, VLPO, LHA, TMN, ARCUATE, VMH, MAMMILLARY.
**Neuroscience:** Correct anatomical organization.
**Category:** KEEP

### Finding 11: Spinal Cord Afferent/Efferent Distinction
**File:** `src/spinal_cord/contracts.py`
**Current:** AfferentSignal (sensory in), EfferentCommand (motor out).
**Neuroscience:** Fundamental and correct.
**Category:** KEEP

### Finding 12: Communication Lanes Mapping
**File:** `src/communication/contracts.py`
**Current:** A_DRIVER (ascending), B_MODULATOR (feedback), C_COMMAND (descending), D_GLOBAL (neuromodulators).
**Neuroscience:** Maps correctly to neural tract organization.
**Category:** KEEP

---

## UPDATE Findings (Correct but Incomplete)

### Finding 13: TRN Gating Not Implemented
**File:** `src/cerebrum/subcortical/thalamus/thalamus_async.py`
**Current:** GateState dataclass exists, methods are skeleton (`pass`/`...`).
**Neuroscience:** TRN receives collaterals from ALL TC/CT axons, provides GABAergic inhibition.
**Category:** UPDATE
**Recommendation:** Implement gating logic - TRN should filter based on salience/attention.

### Finding 14: Thalamus Routing Logic Empty
**File:** `src/cerebrum/subcortical/thalamus/thalamus_async.py`
**Current:** `dispatch()` method is `pass`.
**Neuroscience:** Thalamus routes based on nucleus class (FO->L4, HO->association cortex).
**Category:** UPDATE
**Recommendation:** Implement routing based on NucleusClass.

### Finding 15: Cerebellum Missing Entirely
**File:** None
**Current:** No cerebellum directory exists.
**Neuroscience:** Required for Loop C (timing/calibration). 3-layer cortex, mossy/climbing fibers, Purkinje cells.
**Category:** UPDATE
**Recommendation:** Create cerebellum skeleton with basic contracts.

### Finding 16: Loop Integration Missing
**File:** Various
**Current:** Components exist but not wired together.
**Neuroscience:** All four loops must run concurrently.
**Category:** UPDATE
**Recommendation:** Wire stub connections for message flow.

### Finding 17: Neuromodulatory Systems Not Explicit
**File:** `src/brainstem/contracts.py`
**Current:** GlobalBroadcast exists but no explicit NE/5-HT/DA/ACh systems.
**Neuroscience:** Four major systems: locus coeruleus (NE), raphe (5-HT), VTA/SNc (DA), basal forebrain (ACh).
**Category:** UPDATE
**Recommendation:** Add explicit neuromodulator contracts or document mapping.

### Finding 18: Spinal Cord Missing Laminar Organization
**File:** `src/spinal_cord/contracts.py`
**Current:** No Rexed laminae modeling.
**Neuroscience:** Spinal cord has laminae I-X with distinct functions.
**Category:** UPDATE
**Recommendation:** Add laminae enum for proper routing.

### Finding 19: Brainstem Missing Reticular Formation
**File:** `src/brainstem/contracts.py`
**Current:** Pattern generators exist, no reticular formation.
**Neuroscience:** Reticular formation critical for arousal, gating ascending input.
**Category:** UPDATE
**Recommendation:** Add reticular formation contracts.

### Finding 20: Missing Meta Fields in Subcortical Messages
**File:** Various subcortical files
**Current:** BG, Limbic, Hypothalamus messages lack `meta: Meta` field.
**Neuroscience:** N/A (architectural issue) but impacts brain-faithful validation.
**Category:** UPDATE
**Recommendation:** Add Meta to all message types for consistent validation.

---

## CHANGE Findings (Needs Modification)

### Finding 21: Channel-Based vs Nucleus-Based Conflict
**File:** `src/cerebrum/subcortical/thalamus/channels_async.py`, `src/shared/channels_async.py`
**Current:** Channel-based routing exists alongside nucleus-based.
**Neuroscience:** Thalamus routes by nucleus, not abstract channels. V25 mandates nucleus-based.
**Category:** CHANGE
**Recommendation:** Remove channel files, use nucleus-based routing only.

### Finding 22: Brainstem Uses Channel Addressing
**File:** `src/brainstem/contracts.py`
**Current:** RelayBundle has `channel: str` field.
**Neuroscience:** Should target thalamic nuclei, not abstract channels.
**Category:** CHANGE
**Recommendation:** Change to `target_nucleus: NucleusId`.

### Finding 23: MockCortex Duplicates Thalamus Types
**File:** `src/cerebrum/cortex/mock_cortex_async.py`
**Current:** Re-defines NucleusId, SignalKind, GateState, etc.
**Neuroscience:** N/A (architectural) but creates brain-unfaithful inconsistencies.
**Category:** CHANGE
**Recommendation:** Import from canonical location.

### Finding 24: Superior Colliculus Not Modeled
**File:** None
**Current:** BG documentation mentions SNr->SC for orienting but SC not implemented.
**Neuroscience:** Superior colliculus critical for saccade/orienting control.
**Category:** CHANGE
**Recommendation:** Add SC contracts when implementing oculomotor loop.

### Finding 25: Limbic->BG Valuation Pathway Missing
**File:** `src/cerebrum/subcortical/limbic/limbic_async.py`
**Current:** Limbic has SalienceTag but no explicit BG connection.
**Neuroscience:** Amygdala valuation biases BG action selection via ventral striatum.
**Category:** CHANGE
**Recommendation:** Add explicit limbic->striatum pathway contract.

---

## Sources

- Sherman SM, Guillery RW (2006). Exploring the Thalamus and Its Role in Cortical Function
- Sherman SM, Usrey WM (2024). Transthalamic Pathways for Cortical Function
- Nambu A et al. (2002). Functional significance of the cortico-subthalamo-pallidal hyperdirect pathway
- Alexander GE et al. (1986). Parallel organization of functionally segregated circuits
- Graybiel AM (2025). Surprises From the Basal Ganglia
- Squire LR, Zola-Morgan S (1991). The medial temporal lobe memory system
- LeDoux JE (2000). Emotion circuits in the brain
- Purves D et al. Neuroscience (6th ed.)
- Kandel ER et al. Principles of Neural Science (6th ed.)
- Knowledge Base files (docs/knowledgebase/brain/) - all VERIFIED
