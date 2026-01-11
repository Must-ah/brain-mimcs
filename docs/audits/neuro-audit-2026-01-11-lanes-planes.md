# Neuroscience Audit: Lanes and Planes Brain-Faithfulness

**Date:** 2026-01-11
**Auditor:** Neuro-Expert Agent (Claude Opus 4.5)
**Scope:** Lane enum, Plane enum, Communication Lanes table

---

## Neuro-Expert Analysis

### Grounding Check
- CLAUDE.md reviewed: Yes
- PROJECT_GOALS.md reviewed: No (not required for this audit)
- Knowledge Base reviewed: Yes
- KB verification status checked: Yes - All 24 content files are VERIFIED
- Codebase examined: Yes (contracts.py, contracts_base_async.py)
- Relevant files:
  - `/mnt/private-projects/brain-mimc/src/communication/contracts.py` (Lane enum, lines 37-49)
  - `/mnt/private-projects/brain-mimc/src/shared/contracts_base_async.py` (Plane enum, lines 59-66)
  - `/mnt/private-projects/brain-mimc/docs/knowledgebase/brain/brain-communication-framework.md`
  - `/mnt/private-projects/brain-mimc/docs/knowledgebase/brain/region-centric-brainstem.md`
  - `/mnt/private-projects/brain-mimc/docs/knowledgebase/brain/cerebrum-Subcortical-Structures-Thalamus.md`
  - `/mnt/private-projects/brain-mimc/docs/knowledgebase/brain/verified.md`

### Validation Direction
- Mode: Audit (Code -> Papers)
- Scope: Lane enum, Plane enum, Communication Lanes table

### Confidence Level
- Overall: Certain (using VERIFIED KB content)
- Areas of certainty: All lane mappings, plane completeness
- Areas of uncertainty: None - KB files are all VERIFIED against 2025 literature

### Sources Used
- `brain-communication-framework.md`: 14 communication systems model (VERIFIED)
- `region-centric-brainstem.md`: Neuromodulatory systems, PAG-RVM pathway (VERIFIED)
- `cerebrum-Subcortical-Structures-Thalamus.md`: Driver/modulator distinction, TRN gating (VERIFIED)
- `verified.md`: KB verification status tracking

---

## Audit Summary

**Total Findings:** 11
- KEEP: 5 (brain-faithful)
- PARTIAL: 3 (partially brain-faithful, needs refinement)
- NOT BRAIN-FAITHFUL: 2 (software convenience, acceptable)
- UPDATE: 1 (missing representation)

**CLAUDE.md updates needed:** 1 (minor clarification)

---

## Finding 1: Lane A_DRIVER - Afferent Sensory Pathway

**Code:** `A_DRIVER = "A_DRIVER"` in contracts.py line 38
**CLAUDE.md:** "A (DRIVER) | Payload/content | SpinalCord to Brainstem to Thalamus to Cortex"

**Brain Anatomy:**
The brain has ascending sensory pathways (System 1 in KB framework):
- Dorsal column-medial lemniscus pathway: Fine touch, proprioception
- Spinothalamic tract: Pain, temperature
- Both are LINEAR, ONE-WAY UP pathways
- Driver inputs are defined as: "5-10% of synapses, large terminals, depressing synapses, carry primary information"

**Citation:** `brain-communication-framework.md` System 1; `cerebrum-Subcortical-Structures-Thalamus.md` Driver vs Modulator

**Verdict:** VERIFIED - Brain-faithful
- The DRIVER lane correctly represents ascending sensory pathways
- Direction (SpinalCord -> Brainstem -> Thalamus -> Cortex) matches linear ascending pathways
- "DRIVER" correctly uses neuroscience terminology for information-carrying signals

**Category:** KEEP

---

## Finding 2: Lane B_MODULATOR - Cortical Feedback

**Code:** `B_MODULATOR = "B_MODULATOR"` in contracts.py line 39
**CLAUDE.md:** "B (MODULATOR) | Feedback/attention control | Cortex to Thalamus/TRN"

**Brain Anatomy:**
- Layer VI corticothalamic neurons project back to thalamic nuclei (reciprocal feedback)
- Modulator inputs are: "90-95% of synapses, smaller terminals, facilitating synapses, adjust how driver information is processed"
- Layer VI feedback is MODULATOR, not DRIVER
- Cortex sends feedback to TRN via Layer VI collaterals

**Citation:** `cerebrum-Subcortical-Structures-Thalamus.md` - "Layer VI corticothalamic neurons project back to the thalamic nucleus that innervates them (reciprocal)"

**Verdict:** VERIFIED - Brain-faithful
- MODULATOR lane correctly represents cortical feedback
- Direction (Cortex -> Thalamus/TRN) matches corticothalamic feedback
- Uses correct driver/modulator terminology

**Category:** KEEP

---

## Finding 3: Lane C_COMMAND - Motor/Efferent Pathway

**Code:** `C_COMMAND = "C_COMMAND"` in contracts.py line 40
**CLAUDE.md:** "C (COMMAND) | Motor commands | Cortex to Brainstem to SpinalCord"

**Brain Anatomy:**
- Corticospinal tract: Voluntary motor commands from M1
- Corticobulbar tract: Motor commands to cranial nerve nuclei
- Reticulospinal, vestibulospinal, tectospinal, rubrospinal: Brainstem-origin motor
- All are LINEAR, ONE-WAY DOWN pathways (System 2 in KB framework)

**Citation:** `brain-communication-framework.md` System 2; `region-centric-brainstem.md` Motor Descending Tracts

**Verdict:** VERIFIED - Brain-faithful
- COMMAND lane correctly represents descending motor pathways
- Direction (Cortex -> Brainstem -> SpinalCord) matches corticospinal tract
- Note: Brainstem ALSO generates motor commands (reticulospinal, etc.), not just relays

**Category:** KEEP

**Minor Refinement Suggestion:** The brain has TWO sources of motor commands:
1. Cortex (corticospinal) - voluntary
2. Brainstem (reticulospinal, vestibulospinal, tectospinal, rubrospinal) - automatic

The current model captures cortical commands well but may want to distinguish brainstem-origin commands.

---

## Finding 4: Lane D_GLOBAL - Neuromodulatory Systems

**Code:** `D_GLOBAL = "D_GLOBAL"` in contracts.py line 41
**CLAUDE.md:** "D (GLOBAL MODES) | Neuromodulators | Hypothalamus/Brainstem to ALL"

**Brain Anatomy (System 8 in KB framework):**
- Locus coeruleus (LC): Norepinephrine to ENTIRE CNS
- Raphe nuclei: Serotonin to ENTIRE CNS
- VTA/SNc: Dopamine to limbic/cortical
- Basal forebrain: Acetylcholine to cortex/hippocampus

These are BROADCAST systems (one-to-many architecture):
- "One source sends signals to many targets simultaneously"
- "Do not carry specific information. They set GLOBAL STATE"

**Citation:** `brain-communication-framework.md` System 8; `region-centric-brainstem.md` Locus Coeruleus, Raphe Nuclei, VTA

**Verdict:** VERIFIED - Brain-faithful
- D_GLOBAL correctly represents neuromodulatory broadcast
- "Hypothalamus/Brainstem to ALL" matches broadcast architecture
- Correctly models global state signaling

**Category:** KEEP

---

## Finding 5: Lane E_ERROR - Error/Learning Signals

**Code:** `E_ERROR = "E_ERROR"` in contracts.py line 42
**CLAUDE.md:** "E (ERROR/OUTCOME) | Learning signals | SpinalCord/Limbic to Cortex/BG"

**Brain Anatomy:**
The brain has several error/learning signal pathways:

1. **Cerebellar Error Signals (System 4):**
   - Inferior olive -> Climbing fibers -> Purkinje cells
   - "EXCLUSIVE source of climbing fibers to the cerebellum. Critical for motor learning and error correction"
   - Spino-olivary tract carries "movement error signals about movement execution"

2. **Dopamine Reward Prediction Error:**
   - VTA dopamine neurons encode reward prediction error
   - "Better than expected" -> phasic dopamine increase
   - "Worse than expected" -> phasic dopamine decrease

3. **Limbic Emotional Salience:**
   - Amygdala signals emotional significance
   - Projects to basal ganglia, cortex

**Citation:** `region-centric-brainstem.md` Inferior Olive section; `cerebrum-Subcortical-Structures-Thalamus.md` VTA section

**Verdict:** PARTIALLY VERIFIED - Brain-faithful but incomplete
- E_ERROR captures real brain error signal mechanisms
- "SpinalCord to Cortex/BG" captures spino-olivary and ascending error pathways
- "Limbic to Cortex/BG" captures amygdala salience signaling

**Category:** PARTIAL

**Refinement Needed:**
- The inferior olive (brainstem) is the primary error signal source, not spinal cord
- The pathway is: Spinal cord -> Inferior Olive (error computation) -> Cerebellum (learning)
- Should include "Brainstem" as error signal source

---

## Finding 6: Lane G_GATE - TRN Gating

**Code:** `G_GATE = "G_GATE"` in contracts.py line 43
**CLAUDE.md:** "G (GATE) | TRN inhibition state | Distributed control-plane"

**Brain Anatomy:**
The TRN (Thalamic Reticular Nucleus) is the brain's attention gate:
- "Thin shell of GABAergic neurons surrounding the lateral and anterior thalamus"
- "Does NOT project to cortex. Instead, it gates thalamic relay to cortex"
- "Receives collaterals from both thalamocortical and corticothalamic axons"
- "Projects BACK to thalamic relay nuclei"

TRN Functions:
- Attentional Gating: "Cortex can activate TRN to inhibit unattended thalamic channels"
- Lateral Inhibition: "Creates winner-take-all dynamics"
- Sleep Spindles: "Generate 7-14 Hz oscillatory bursting during NREM sleep"

**Citation:** `cerebrum-Subcortical-Structures-Thalamus.md` Part 7: Thalamic Reticular Nucleus (TRN)

**Verdict:** VERIFIED - Brain-faithful
- G_GATE correctly represents TRN gating mechanism
- "Distributed control-plane" accurately describes TRN's role
- TRN is a control mechanism, not a data pathway

**Category:** KEEP

---

## Finding 7: Lane X_REFLECT - Audit/Observability

**Code:** `X_REFLECT = "X_REFLECT"` in contracts.py line 44
**CLAUDE.md:** "X (REFLECTION) | Audit/observability | Non-blocking copies"

**Brain Anatomy:**
The brain does have self-monitoring mechanisms, but NOT a dedicated "audit" pathway:

1. **Corollary Discharge / Efference Copy:**
   - Motor commands generate copies sent to sensory areas
   - Allows distinguishing self-generated from external stimuli
   - Example: Superior colliculus receives copy of saccade commands

2. **Metacognition:**
   - Prefrontal cortex monitors other cortical activity
   - Not a separate pathway but part of hierarchical processing

3. **Error Monitoring:**
   - Anterior cingulate cortex detects conflicts
   - Part of normal processing, not a separate lane

**Citation:** `region-centric-brainstem.md` Superior Colliculus (receives FEF saccade commands)

**Verdict:** NOT BRAIN-FAITHFUL but acceptable as software infrastructure
- The brain does NOT have a dedicated "reflection" or "audit" pathway
- Corollary discharge exists but is integrated into motor/sensory pathways
- X_REFLECT is a SOFTWARE pattern for observability, not a brain-faithful lane

**Category:** NOT BRAIN-FAITHFUL (Software convenience)

**Recommendation:** Keep as software infrastructure but document that it's not modeling a brain pathway. Consider renaming or marking as "infrastructure" to distinguish from brain-faithful lanes.

---

## Finding 8: Lane V_VIDEO and U_AUDIO - Media Lanes

**Code:**
```python
V_VIDEO = "V_VIDEO"
U_AUDIO = "U_AUDIO"
```
**Comment:** "Media lanes (data plane): negotiated sessions, not raw bus flooding"

**Brain Anatomy:**
The brain does NOT have separate "media" lanes for video/audio:
- Visual information uses the same pathway architecture as all sensory data (System 1)
- Auditory information follows the same linear ascending pathway pattern
- Retina -> LGN -> V1 (visual) uses Driver pathway
- Cochlea -> Inferior Colliculus -> MGN -> A1 (auditory) uses Driver pathway

The brain transforms sensory data at reception:
- Retina performs edge detection, contrast, motion processing BEFORE sending
- Cochlea performs frequency decomposition BEFORE sending
- "Raw never goes up" applies to all modalities

**Citation:** `brain-communication-framework.md` System 1, `cerebrum-Subcortical-Structures-Thalamus.md` LGN, MGN

**Verdict:** NOT BRAIN-FAITHFUL but acceptable as software infrastructure
- The brain does NOT have separate lanes for different media types
- All sensory modalities use the same pathway architecture
- V_VIDEO and U_AUDIO are SOFTWARE patterns for handling high-bandwidth data

**Category:** NOT BRAIN-FAITHFUL (Software convenience)

**Recommendation:** Keep as software infrastructure but document that they're not brain-faithful. The code correctly notes these are "negotiated sessions, not raw bus flooding" which aligns with "raw never goes up" - but they should be labeled as infrastructure, not brain pathways.

---

## Finding 9: Missing Lane - Interoceptive Pathway

**Brain Anatomy:**
System 11 (Interoceptive Ascending) is a distinct pathway:
- Vagus nerve (organs above diaphragm) -> NTS -> Parabrachial -> Insula
- Spinal visceral afferents (organs below diaphragm) -> NTS -> Parabrachial -> Insula
- Carries: gut feelings, heart rate awareness, hunger, thirst, pain

This is DIFFERENT from System 1 (Sensory Ascending):
- System 1 = exteroception (external world)
- System 11 = interoception (internal state)

**Citation:** `brain-communication-framework.md` System 11

**Verdict:** PARTIAL - Brain-faithful architecture is missing a key pathway
- The current Lane enum models exteroceptive sensing (A_DRIVER)
- Interoceptive sensing uses a different pathway (NTS, Parabrachial)
- This may be important for modeling homeostasis (Loop D)

**Category:** UPDATE

**Recommendation:** Consider adding `I_INTERO` lane for interoceptive signals, OR document that A_DRIVER includes interoceptive input. The brainstem (NTS) is the integration point for interoception.

---

## Finding 10: Plane Enum Completeness

**Code:**
```python
class Plane(str, Enum):
    SPINAL = "spinal"
    BRAINSTEM = "brainstem"
    THALAMUS = "thalamus"
    CORTEX = "cortex"
    RELIABLE = "reliable"
    REFLECT = "reflect"
    UNKNOWN = "unknown"
```

**Brain Anatomy:**
The brain's major processing levels are:
1. Spinal Cord - Gateway, local processing
2. Brainstem - Relay, origin, vital functions
3. Cerebellum - Timing, calibration, motor learning
4. Thalamus - Gateway to cortex, gating
5. Basal Ganglia - Action selection
6. Limbic (Hippocampus, Amygdala) - Memory, emotion
7. Hypothalamus - Homeostasis, autonomic
8. Cortex - Decision, perception

**Citation:** `brain-communication-framework.md` all 14 systems

**Verdict:** PARTIAL - Missing key processing regions

Current planes are anatomically incomplete:
- SPINAL: CORRECT - Matches spinal cord
- BRAINSTEM: CORRECT - Matches brainstem
- THALAMUS: CORRECT - Matches thalamus
- CORTEX: CORRECT - Matches cortex
- RELIABLE: NOT ANATOMICAL - Software infrastructure
- REFLECT: NOT ANATOMICAL - Software infrastructure
- UNKNOWN: NOT ANATOMICAL - Error handling

**Missing anatomical planes:**
1. **CEREBELLUM** - Essential for Loop C (calibration)
2. **BASAL_GANGLIA** - Essential for Loop B (action selection)
3. **LIMBIC** - Essential for Loop D (memory, emotion)
4. **HYPOTHALAMUS** - Essential for Loop D (homeostasis)

**Category:** PARTIAL

**Recommendation:** The Plane enum should distinguish between:
1. **Anatomical Planes:** SPINAL, BRAINSTEM, THALAMUS, CORTEX (+ CEREBELLUM, BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS)
2. **Infrastructure Planes:** RELIABLE, REFLECT

Current implementation conflates anatomical levels with infrastructure concerns. For brain-faithfulness, each major processing region should have its own plane.

---

## Finding 11: Nucleus-Based Addressing vs Channel-Based

**Code in contracts.py (lines 68-76):**
```python
class NucleusId(str, Enum):
    LGN = "lgn"
    MGN = "mgn"
    VPL = "vpl"
    VPM = "vpm"
    PULVINAR = "pulvinar"
    MD = "md"
    TRN = "trn"
```

**Brain Anatomy:**
The thalamus IS organized by nuclei, and this enum correctly represents key nuclei:
- LGN: Visual relay (first-order)
- MGN: Auditory relay (first-order)
- VPL/VPM: Somatosensory relay (first-order)
- PULVINAR: Higher-order visual/attention
- MD: Higher-order executive/memory
- TRN: Gating (not relay)

**Missing nuclei per CLAUDE.md:**
- VA/VL: Motor relay (cerebellum, basal ganglia output)
- CM/Pf/CL/PVT: Diffuse/intralaminar (arousal, attention)

**Citation:** `cerebrum-Subcortical-Structures-Thalamus.md` Parts 2-7

**Verdict:** PARTIAL - Good start, incomplete

**Category:** PARTIAL

**Recommendation:** Add missing nucleus classes:
1. **Motor nuclei:** VA, VL (essential for Loop B and C)
2. **Diffuse nuclei:** CM, Pf, CL (essential for arousal)
3. Consider organizing by nucleus CLASS as CLAUDE.md specifies:
   - First-order: LGN, MGN, VPL, VPM, VA, VL
   - Higher-order: Pulvinar, MD, LP, LD
   - Diffuse: CM, Pf, CL, PVT
   - Gate: TRN

---

## CLAUDE.md Finding 1: Communication Lanes Table

**Current CLAUDE.md table:**
| Lane | Purpose | Direction |
|------|---------|-----------|
| A (DRIVER) | Payload/content | SpinalCord to Brainstem to Thalamus to Cortex |
| B (MODULATOR) | Feedback/attention control | Cortex to Thalamus/TRN |
| C (COMMAND) | Motor commands | Cortex to Brainstem to SpinalCord |
| D (GLOBAL MODES) | Neuromodulators | Hypothalamus/Brainstem to ALL |
| E (ERROR/OUTCOME) | Learning signals | SpinalCord/Limbic to Cortex/BG |
| G (GATE) | TRN inhibition state | Distributed control-plane |
| X (REFLECTION) | Audit/observability | Non-blocking copies |

**Verdict:** PARTIAL - Mostly accurate, minor updates needed

**Proposed Updates:**
1. Lane E should include "Brainstem (Inferior Olive)" as error source
2. Lane X should note "(Software infrastructure, not brain pathway)"
3. Add note that V_VIDEO/U_AUDIO are software infrastructure

---

## Summary of Verdicts

| Lane/Plane | Status | Brain-Faithful? | Action |
|------------|--------|-----------------|--------|
| A_DRIVER | VERIFIED | YES | KEEP |
| B_MODULATOR | VERIFIED | YES | KEEP |
| C_COMMAND | VERIFIED | YES | KEEP |
| D_GLOBAL | VERIFIED | YES | KEEP |
| E_ERROR | PARTIAL | YES (incomplete) | UPDATE - add Brainstem source |
| G_GATE | VERIFIED | YES | KEEP |
| X_REFLECT | NOT FAITHFUL | NO (software) | Document as infrastructure |
| V_VIDEO | NOT FAITHFUL | NO (software) | Document as infrastructure |
| U_AUDIO | NOT FAITHFUL | NO (software) | Document as infrastructure |
| Plane SPINAL | VERIFIED | YES | KEEP |
| Plane BRAINSTEM | VERIFIED | YES | KEEP |
| Plane THALAMUS | VERIFIED | YES | KEEP |
| Plane CORTEX | VERIFIED | YES | KEEP |
| Plane RELIABLE | NOT FAITHFUL | NO (software) | Document as infrastructure |
| Plane REFLECT | NOT FAITHFUL | NO (software) | Document as infrastructure |
| Missing: Interoception | N/A | Missing | Consider adding |
| Missing: Cerebellum plane | N/A | Missing | Add for Loop C |
| Missing: Basal Ganglia plane | N/A | Missing | Add for Loop B |
| Missing: Limbic plane | N/A | Missing | Add for Loop D |
| Missing: Hypothalamus plane | N/A | Missing | Add for Loop D |
| NucleusId | PARTIAL | Incomplete | Add VA, VL, CM, Pf, CL |

---

## Recommendations

### High Priority (Brain-Faithfulness)
1. **Add missing anatomical planes:** CEREBELLUM, BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS
2. **Add missing nucleus IDs:** VA, VL (motor), CM, Pf, CL (diffuse)
3. **Separate anatomical vs infrastructure planes** in code and documentation

### Medium Priority (Completeness)
4. **Consider interoceptive lane** or document that A_DRIVER includes interoception
5. **Update Lane E sources** to include Brainstem (Inferior Olive)

### Low Priority (Documentation)
6. **Document X_REFLECT, V_VIDEO, U_AUDIO** as software infrastructure, not brain pathways
7. **Update CLAUDE.md Communication Lanes table** with refinements noted above

---

## User Decision Required

The audit is complete. Please decide:

1. **Plane enum completeness:** Should we add CEREBELLUM, BASAL_GANGLIA, LIMBIC, HYPOTHALAMUS planes?

2. **NucleusId completeness:** Should we add VA, VL, CM, Pf, CL nucleus IDs?

3. **Infrastructure separation:** Should we clearly separate anatomical planes from software infrastructure planes?

4. **Interoceptive pathway:** Should we add a separate interoceptive lane or document that A_DRIVER includes interoception?

5. **Documentation updates:** Should we update CLAUDE.md with the refinements noted?

I advise - you decide.
