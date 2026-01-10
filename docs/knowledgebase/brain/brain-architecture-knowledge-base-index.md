# Brain Architecture Knowledge Base — Master Index

This document serves as the comprehensive index and navigation guide for the Brain Architecture Knowledge Base. It catalogs all documents, describes their contents, shows the organizational hierarchy, provides cross-references for key topics, and offers guidance on how to use the knowledge base effectively.

---

## How to Use This Knowledge Base

### Purpose

This knowledge base provides detailed, region-centric communication maps of the central nervous system. Each document answers: **"What does this region communicate with, and how?"** — specifying connections at every level from within-region to cross-division, with layer-level precision where applicable.

The primary purpose is to support **brain-inspired software architecture** by providing accurate, detailed reference material about how the brain organizes computation, routes information, and coordinates between specialized modules.

### Document Types

**Foundational Documents:** Establish core principles (e.g., canonical microcircuit, communication architecture)

**Region-Centric Documents:** Detail specific brain regions with complete connectivity maps

**Integration Documents:** Synthesize information across regions (pathways, networks)

### Reading Order for Newcomers

1. Start with **Brain Communication Architecture** for the big picture
2. Read **Canonical Cortical Microcircuit** to understand the six-layer template
3. Read **Brain Architecture Outline** (in project files) for structural overview
4. Then dive into specific regions as needed

### Finding Information

**By brain region:** Use the hierarchical catalog below
**By function:** Use the functional cross-reference section
**By pathway:** Use the major pathways cross-reference
**By network:** Use the functional networks cross-reference

---

## Document Catalog — Hierarchical Organization

### Foundational Documents

| Document | Filename | Description |
|----------|----------|-------------|
| Brain Communication Architecture | `brain-communication-architecture.md` | Master overview of brain organization, communication principles, information flow patterns, and architectural principles for software design. 9 parts covering divisions, pathways, loops, neuromodulation, and synthesis. |
| Brain Functional Pathways | `brain-functional-pathways.md` | Detailed coverage of major functional pathways: sensory systems, motor systems, limbic circuits, cognitive loops. 10 parts with complete pathway specifications. |
| Canonical Cortical Microcircuit | `cerebrum-Cerebral-Cortex-Canonical-Microcircuit.md` | **FOUNDATIONAL — READ FIRST FOR CORTEX.** Describes the six-layer cortical template, feedforward/feedback rules, layer functions, granular vs agranular cortex, and how to interpret cortical connectivity. |

---

### Cerebrum — Cerebral Cortex Documents

The cerebral cortex is organized into six lobes. Each document provides complete connectivity for all regions within that lobe.

| Lobe | Filename | Parts | Key Regions Covered |
|------|----------|-------|---------------------|
| Occipital | `cerebrum-Cerebral-Cortex-Occipital-Lobe.md` | ~12 | V1 (primary visual), V2, V3, V4 (color), V5/MT (motion), MST, dorsal/ventral stream origins |
| Parietal | `cerebrum-Cerebral-Cortex-Parietal-Lobe.md` | 16 | S1 (BA 3a/3b/1/2), S2, Area 5, Area 7, LIP, VIP, MIP/PRR, AIP, CIP, supramarginal gyrus, angular gyrus, precuneus |
| Temporal | `cerebrum-Cerebral-Cortex-Temporal-Lobe.md` | 14 | A1, belt/parabelt, STS, Wernicke's area, MTG, IT (TEO/TE), FFA, VWFA, PPA, perirhinal, entorhinal, temporal pole |
| Frontal | `cerebrum-Cerebral-Cortex-Frontal-Lobe.md` | 20 | M1, PMd, PMv, SMA, Pre-SMA, FEF, Broca's area, DLPFC, VLPFC, OFC, vmPFC, ACC, frontopolar, dmPFC |
| Insular | `cerebrum-Cerebral-Cortex-Insular-Lobe.md` | 9 | Posterior insula (interoceptive), mid-insula, anterior insula (emotional awareness), gustatory cortex |
| Limbic | `cerebrum-Cerebral-Cortex-Limbic-Lobe.md` | 14 | ACC (limbic perspective), MCC, PCC, retrosplenial cortex, parahippocampal (summary), Papez circuit |

#### Cortex Document Structure

Each cortex document follows a consistent structure:
1. Overview (location, boundaries, functions)
2. Region-by-region coverage with:
   - Cytoarchitecture (granular/agranular, layer characteristics)
   - Within-lobe connections
   - Connections with each other lobe
   - Thalamic connections (input nucleus, Layer IV target, Layer VI feedback)
   - Subcortical connections (basal ganglia, limbic)
   - Brainstem connections (where applicable)
   - Functional properties
3. Summary tables (thalamic, cortical, subcortical connections)
4. Clinical implications

---

### Cerebrum — Subcortical Documents

The subcortical structures are organized as nuclei rather than layers. Each document provides complete connectivity for all nuclei/subdivisions within that structure.

| Structure | Filename | Parts | Key Components Covered |
|-----------|----------|-------|------------------------|
| Thalamus | `cerebrum-Subcortical-Thalamus.md` | ~15 | ~60 nuclei organized by function: sensory relay (LGN, MGN, VPL/VPM), motor relay (VL, VA), association (MD, pulvinar, LP), limbic (anterior, LD), intralaminar (CM, Pf), TRN |
| Hypothalamus | `cerebrum-Subcortical-Hypothalamus.md` | ~12 | Anterior (SCN, preoptic, PVN, SON), tuberal (arcuate, VMN, DMN, LHA), posterior (mammillary bodies), HPA axis, autonomic control |
| Basal Ganglia | `cerebrum-Subcortical-Basal-Ganglia.md` | ~14 | Striatum (caudate, putamen, NAcc), GPe, GPi, STN, SNc, SNr; direct/indirect/hyperdirect pathways; motor/cognitive/limbic/oculomotor loops |
| Limbic Structures | `cerebrum-Subcortical-Limbic-Structures.md` | ~16 | Hippocampal formation (DG, CA3, CA1, subiculum, entorhinal), amygdala (LA, BA, CeA, MeA), fornix, septal nuclei |

#### Subcortical Document Structure

Each subcortical document follows a consistent structure:
1. Overview (location, organization, function)
2. Nucleus-by-nucleus coverage with:
   - Internal organization
   - Inputs (source, pathway)
   - Outputs (target, pathway)
   - Functional role
3. Circuit/pathway descriptions
4. Summary tables
5. Clinical implications

---

### Other CNS Divisions

| Division | Filename | Parts | Key Components Covered |
|----------|----------|-------|------------------------|
| Cerebellum | `cerebellum-comprehensive-guide.md` | 10 | Cerebellar cortex (3 layers, Purkinje cells), deep nuclei (dentate, interposed, fastigial), input (mossy fibers, climbing fibers), output pathways, functional divisions (vestibulo-, spino-, cerebro-cerebellum) |
| Brainstem | `brainstem-comprehensive-guide.md` | 5 | Midbrain (superior/inferior colliculus, PAG, red nucleus, VTA, SNc/SNr), pons (pontine nuclei, locus coeruleus, raphe), medulla (vital centers, inferior olive, pyramidal decussation), cranial nerves, reticular formation |
| Spinal Cord | `spinal-cord-comprehensive-guide.md` | 5 | Gray matter (Rexed laminae I-X, dorsal/ventral horn), white matter (ascending/descending tracts), reflexes, segments |

---

## Cross-Reference by Function

### Sensory Processing

| Modality | Primary Cortex | Document | Thalamic Relay | Document |
|----------|---------------|----------|----------------|----------|
| Vision | V1 (BA 17) | Occipital Lobe | LGN | Thalamus |
| Audition | A1 (BA 41) | Temporal Lobe | MGN | Thalamus |
| Somatosensation | S1 (BA 3,1,2) | Parietal Lobe | VPL/VPM | Thalamus |
| Gustation | Anterior insula | Insular Lobe | VPMpc | Thalamus |
| Olfaction | Piriform cortex | (not detailed) | (bypasses thalamus) | — |
| Vestibular | PIVC | Insular/Parietal | VPP | Thalamus |
| Interoception | Posterior insula | Insular Lobe | VMpo | Thalamus |

### Motor Control

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Primary motor output | M1 (Layer V Betz cells) | Frontal Lobe |
| Reach planning | PMd, MIP/PRR | Frontal Lobe, Parietal Lobe |
| Grasp planning | PMv, AIP | Frontal Lobe, Parietal Lobe |
| Movement sequences | SMA, Pre-SMA | Frontal Lobe |
| Eye movements | FEF, LIP, SC | Frontal Lobe, Parietal Lobe, Brainstem |
| Action selection | Basal ganglia (direct/indirect pathways) | Basal Ganglia |
| Motor coordination | Cerebellum | Cerebellum |
| Motor thalamus | VL (cerebellar), VA (BG) | Thalamus |

### Language

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Speech production | Broca's area (BA 44, 45) | Frontal Lobe |
| Speech comprehension | Wernicke's area (posterior STG) | Temporal Lobe |
| Phonological processing | Supramarginal gyrus (BA 40) | Parietal Lobe |
| Semantic processing | Angular gyrus (BA 39), MTG, temporal pole | Parietal Lobe, Temporal Lobe |
| Reading | VWFA (left fusiform) | Temporal Lobe |
| Dorsal stream (phonology) | Broca's ↔ Wernicke's via arcuate | Frontal, Temporal, Parietal |
| Ventral stream (semantics) | Anterior temporal ↔ IFG via uncinate/IFOF | Temporal, Frontal |

### Memory

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Encoding | Hippocampus (DG pattern separation) | Limbic Structures |
| Retrieval | Hippocampus (CA3 pattern completion) | Limbic Structures |
| Working memory | DLPFC | Frontal Lobe |
| Episodic memory | Hippocampus, PCC, RSC | Limbic Structures, Limbic Lobe |
| Semantic memory | Temporal pole, angular gyrus, MTG | Temporal Lobe, Parietal Lobe |
| Spatial memory | Hippocampus (place cells), RSC (head direction), entorhinal (grid cells) | Limbic Structures, Limbic Lobe, Temporal Lobe |
| Fear memory | Amygdala (BLA) | Limbic Structures |
| Procedural memory | Striatum, cerebellum | Basal Ganglia, Cerebellum |
| Papez circuit | Hippocampus → fornix → mammillary → anterior thalamus → cingulate | Limbic Lobe, Limbic Structures, Hypothalamus, Thalamus |

### Attention

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Top-down (dorsal attention) | FEF, IPS/SPL | Frontal Lobe, Parietal Lobe |
| Bottom-up (ventral attention) | TPJ, VLPFC | Parietal Lobe, Frontal Lobe |
| Salience detection | Anterior insula, dACC | Insular Lobe, Frontal/Limbic Lobe |
| Thalamic gating | TRN | Thalamus |
| Visual attention | V4, FEF, LIP | Occipital Lobe, Frontal Lobe, Parietal Lobe |

### Emotion

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Fear processing | Amygdala (LA → CeA) | Limbic Structures |
| Fear extinction | vmPFC → amygdala | Frontal Lobe, Limbic Structures |
| Disgust | Anterior insula | Insular Lobe |
| Emotional awareness | Anterior insula | Insular Lobe |
| Emotion regulation | sgACC, vmPFC → amygdala | Frontal/Limbic Lobe, Limbic Structures |
| Mood | sgACC (BA 25) | Frontal/Limbic Lobe |
| Reward | OFC, NAcc, VTA | Frontal Lobe, Basal Ganglia, Brainstem |
| Autonomic expression | Hypothalamus, PAG, brainstem nuclei | Hypothalamus, Brainstem |

### Executive Function

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Working memory | DLPFC | Frontal Lobe |
| Cognitive control | DLPFC, VLPFC | Frontal Lobe |
| Conflict monitoring | dACC | Frontal/Limbic Lobe |
| Error detection | dACC | Frontal/Limbic Lobe |
| Response inhibition | VLPFC (right), STN | Frontal Lobe, Basal Ganglia |
| Rule representation | DLPFC | Frontal Lobe |
| Value computation | OFC | Frontal Lobe |
| Planning | DLPFC, frontopolar | Frontal Lobe |
| Metacognition | Frontopolar (BA 10) | Frontal Lobe |

### Self and Social Cognition

| Function | Key Regions | Documents |
|----------|-------------|-----------|
| Self-referential | vmPFC, PCC, precuneus | Frontal Lobe, Limbic Lobe, Parietal Lobe |
| Theory of mind | dmPFC, TPJ, STS | Frontal Lobe, Parietal Lobe, Temporal Lobe |
| Face recognition | FFA (fusiform) | Temporal Lobe |
| Biological motion | STS | Temporal Lobe |
| Mirror system | PMv, AIP, STS | Frontal Lobe, Parietal Lobe, Temporal Lobe |
| Empathy | Anterior insula, ACC | Insular Lobe, Frontal/Limbic Lobe |

---

## Cross-Reference by Major Pathway

### Sensory Pathways

| Pathway | Course | Documents |
|---------|--------|-----------|
| Visual | Retina → LGN → V1 → dorsal/ventral streams | Thalamus, Occipital, Parietal, Temporal |
| Auditory | Cochlea → IC → MGN → A1 → belt/parabelt → streams | Brainstem, Thalamus, Temporal |
| Dorsal column-medial lemniscus | Spinal cord → DCN → VPL → S1 | Spinal Cord, Brainstem, Thalamus, Parietal |
| Spinothalamic | Spinal cord → VPL → S1/insula | Spinal Cord, Thalamus, Parietal, Insular |
| Gustatory | Tongue → NTS → VPMpc → insula/OFC | Brainstem, Thalamus, Insular, Frontal |

### Motor Pathways

| Pathway | Course | Documents |
|---------|--------|-----------|
| Corticospinal | M1 Layer V → pyramidal decussation → spinal cord | Frontal, Brainstem, Spinal Cord |
| Corticobulbar | M1 Layer V → brainstem motor nuclei | Frontal, Brainstem |
| Cerebellar loop | Cortex → pons → cerebellum → VL → cortex | Frontal, Brainstem, Cerebellum, Thalamus |
| Basal ganglia loop | Cortex → striatum → GPi → VA/VL → cortex | Frontal, Basal Ganglia, Thalamus |

### Association Pathways (White Matter Tracts)

| Tract | Connects | Relevant Documents |
|-------|----------|-------------------|
| Arcuate fasciculus | Broca's ↔ Wernicke's (dorsal language) | Frontal, Temporal |
| Superior longitudinal fasciculus | Frontal ↔ parietal | Frontal, Parietal |
| Inferior fronto-occipital fasciculus | Frontal ↔ occipital (ventral language) | Frontal, Temporal, Occipital |
| Uncinate fasciculus | OFC ↔ temporal pole | Frontal, Temporal |
| Cingulum | ACC ↔ PCC ↔ hippocampus | Limbic Lobe, Limbic Structures |
| Fornix | Hippocampus ↔ mammillary bodies, septal | Limbic Structures, Hypothalamus |
| Corpus callosum | Left ↔ right hemisphere | All cortical |

---

## Cross-Reference by Functional Network

### Default Mode Network (DMN)

| Component | Role | Document |
|-----------|------|----------|
| vmPFC | Core hub; self-referential | Frontal Lobe |
| PCC/Precuneus | Core hub; episodic memory | Limbic Lobe, Parietal Lobe |
| Angular gyrus | Semantic; episodic | Parietal Lobe |
| Lateral temporal | Semantic memory | Temporal Lobe |
| Hippocampus | Episodic memory | Limbic Structures |
| Temporal pole | Personal semantics | Temporal Lobe |

### Salience Network

| Component | Role | Document |
|-----------|------|----------|
| Anterior insula | Core hub; interoception, awareness | Insular Lobe |
| dACC | Core hub; conflict, error | Frontal/Limbic Lobe |
| Amygdala | Emotional salience | Limbic Structures |
| Ventral striatum | Motivational salience | Basal Ganglia |

### Central Executive Network (Frontoparietal Control)

| Component | Role | Document |
|-----------|------|----------|
| DLPFC | Working memory, control | Frontal Lobe |
| VLPFC | Inhibition, retrieval | Frontal Lobe |
| Posterior parietal (IPS/SPL) | Attention, spatial | Parietal Lobe |
| FEF | Attention, eye movements | Frontal Lobe |

### Dorsal Attention Network

| Component | Role | Document |
|-----------|------|----------|
| FEF | Eye movements, spatial attention | Frontal Lobe |
| IPS/SPL | Spatial maps, attention | Parietal Lobe |

### Ventral Attention Network

| Component | Role | Document |
|-----------|------|----------|
| TPJ | Reorienting | Parietal Lobe |
| VLPFC | Attention capture | Frontal Lobe |

### Language Network

| Component | Role | Document |
|-----------|------|----------|
| Broca's area (BA 44, 45) | Production, syntax | Frontal Lobe |
| Wernicke's area | Comprehension | Temporal Lobe |
| Supramarginal gyrus | Phonology | Parietal Lobe |
| Angular gyrus | Semantics | Parietal Lobe |
| MTG | Lexical semantics | Temporal Lobe |
| Temporal pole | Sentence meaning | Temporal Lobe |

### Motor Network

| Component | Role | Document |
|-----------|------|----------|
| M1 | Execution | Frontal Lobe |
| Premotor (PMd, PMv) | Planning | Frontal Lobe |
| SMA | Sequences | Frontal Lobe |
| Posterior parietal | Sensorimotor | Parietal Lobe |
| Basal ganglia | Selection | Basal Ganglia |
| Cerebellum | Coordination | Cerebellum |
| Motor thalamus (VL, VA) | Relay | Thalamus |

### Limbic/Emotion Network

| Component | Role | Document |
|-----------|------|----------|
| Amygdala | Fear, emotion | Limbic Structures |
| Hippocampus | Memory | Limbic Structures |
| vmPFC/OFC | Regulation, value | Frontal Lobe |
| ACC (sgACC) | Mood | Frontal/Limbic Lobe |
| Anterior insula | Feeling | Insular Lobe |
| Hypothalamus | Autonomic | Hypothalamus |

---

## Cross-Reference by Thalamic Nucleus

| Nucleus | Function | Cortical Target | Document |
|---------|----------|-----------------|----------|
| LGN | Vision | V1 | Thalamus, Occipital |
| MGN | Audition | A1 | Thalamus, Temporal |
| VPL | Body somatosensory | S1 | Thalamus, Parietal |
| VPM | Face somatosensory | S1 | Thalamus, Parietal |
| VPMpc | Taste | Insula | Thalamus, Insular |
| VMpo | Interoception | Insula | Thalamus, Insular |
| VL | Motor (cerebellar) | M1, premotor | Thalamus, Frontal |
| VA | Motor (BG) | Premotor, PFC | Thalamus, Frontal |
| MD | Association | PFC (all) | Thalamus, Frontal |
| Pulvinar | Visual attention | Parietal, temporal, frontal | Thalamus, Multiple |
| LP | Spatial | Parietal | Thalamus, Parietal |
| Anterior | Memory | Cingulate | Thalamus, Limbic Lobe |
| LD | Spatial memory | RSC, parietal | Thalamus, Limbic Lobe |
| Intralaminar | Arousal | Widespread | Thalamus |
| TRN | Gating | (inhibits thalamus) | Thalamus |

---

## Cross-Reference by Basal Ganglia Loop

| Loop | Cortical Origin | Striatal Target | Output | Returns To | Documents |
|------|-----------------|-----------------|--------|------------|-----------|
| Motor | M1, premotor, SMA | Putamen | GPi → VL | Motor cortex | Basal Ganglia, Frontal |
| Oculomotor | FEF, SEF | Caudate (body) | SNr → VA/MD | FEF | Basal Ganglia, Frontal |
| Cognitive | DLPFC, VLPFC | Caudate (head) | GPi → VA/MD | DLPFC | Basal Ganglia, Frontal |
| Limbic | OFC, ACC, vmPFC | NAcc | VP → MD | OFC/ACC | Basal Ganglia, Frontal |

---

## Cross-Reference by Brodmann Area

| BA | Name | Lobe | Document |
|----|------|------|----------|
| 1, 2, 3 | Primary somatosensory (S1) | Parietal | Parietal Lobe |
| 4 | Primary motor (M1) | Frontal | Frontal Lobe |
| 5 | Somatosensory association | Parietal | Parietal Lobe |
| 6 | Premotor, SMA | Frontal | Frontal Lobe |
| 7 | Superior parietal | Parietal | Parietal Lobe |
| 8 | Frontal eye fields | Frontal | Frontal Lobe |
| 9 | DLPFC | Frontal | Frontal Lobe |
| 10 | Frontopolar | Frontal | Frontal Lobe |
| 11 | OFC | Frontal | Frontal Lobe |
| 17 | Primary visual (V1) | Occipital | Occipital Lobe |
| 18 | Visual association (V2, V3) | Occipital | Occipital Lobe |
| 19 | Visual association (V4, V5) | Occipital | Occipital Lobe |
| 20 | Inferior temporal (IT) | Temporal | Temporal Lobe |
| 21 | Middle temporal (MTG) | Temporal | Temporal Lobe |
| 22 | Superior temporal (includes Wernicke's) | Temporal | Temporal Lobe |
| 23 | Posterior cingulate | Limbic | Limbic Lobe |
| 24 | Anterior cingulate | Limbic/Frontal | Limbic Lobe, Frontal Lobe |
| 25 | Subgenual cingulate | Limbic/Frontal | Limbic Lobe, Frontal Lobe |
| 28 | Entorhinal | Temporal/Limbic | Temporal Lobe, Limbic Structures |
| 29, 30 | Retrosplenial | Limbic | Limbic Lobe |
| 31 | Dorsal posterior cingulate | Limbic | Limbic Lobe |
| 32 | Anterior cingulate | Limbic/Frontal | Limbic Lobe, Frontal Lobe |
| 35, 36 | Perirhinal | Temporal | Temporal Lobe |
| 37 | Fusiform | Temporal | Temporal Lobe |
| 38 | Temporal pole | Temporal | Temporal Lobe |
| 39 | Angular gyrus | Parietal | Parietal Lobe |
| 40 | Supramarginal gyrus | Parietal | Parietal Lobe |
| 41 | Primary auditory (A1) | Temporal | Temporal Lobe |
| 42 | Auditory association | Temporal | Temporal Lobe |
| 44 | Broca's (pars opercularis) | Frontal | Frontal Lobe |
| 45 | Broca's (pars triangularis) | Frontal | Frontal Lobe |
| 46 | DLPFC | Frontal | Frontal Lobe |
| 47 | VLPFC/OFC | Frontal | Frontal Lobe |

---

## Clinical Cross-Reference

### Lesion → Deficit → Document

| Lesion Site | Deficit | Document |
|-------------|---------|----------|
| M1 | Hemiparesis, loss of fine motor | Frontal Lobe |
| Broca's area | Non-fluent aphasia | Frontal Lobe |
| Wernicke's area | Fluent aphasia, impaired comprehension | Temporal Lobe |
| DLPFC | Dysexecutive syndrome | Frontal Lobe |
| OFC | Poor decision-making, social inappropriateness | Frontal Lobe |
| Hippocampus | Anterograde amnesia | Limbic Structures |
| Amygdala | Impaired fear, emotion recognition | Limbic Structures |
| V1 | Cortical blindness | Occipital Lobe |
| FFA | Prosopagnosia | Temporal Lobe |
| RSC | Topographical disorientation | Limbic Lobe |
| Basal ganglia (SNc) | Parkinson's disease | Basal Ganglia |
| Striatum | Huntington's disease | Basal Ganglia |
| Cerebellum | Ataxia, dysmetria | Cerebellum |
| Anterior insula | Reduced emotional awareness | Insular Lobe |

---

## Document Statistics

| Category | Count | Total Parts |
|----------|-------|-------------|
| Foundational | 3 | ~25 |
| Cerebral Cortex | 7 (including Canonical) | ~90 |
| Subcortical | 4 | ~57 |
| Other Divisions | 3 | ~20 |
| **Total** | **17** | **~192** |

### Coverage Summary

**Cerebrum:**
- 6 cortical lobes fully documented
- 4 subcortical structures fully documented
- All major Brodmann areas covered
- All thalamic nuclei covered
- All basal ganglia components and pathways covered
- Hippocampal formation and amygdala fully detailed

**Brainstem:**
- All three divisions (midbrain, pons, medulla) covered
- All neuromodulatory systems covered
- Cranial nerves covered
- Reticular formation covered

**Cerebellum:**
- All three layers covered
- All deep nuclei covered
- All input/output pathways covered
- Functional divisions covered

**Spinal Cord:**
- All Rexed laminae covered
- All ascending/descending tracts covered
- Reflex circuits covered

---

## Quick Reference: Where to Find Common Topics

| Topic | Primary Document(s) |
|-------|---------------------|
| Layer IV input rule | Canonical Microcircuit |
| Feedforward vs feedback | Canonical Microcircuit |
| Corticospinal tract | Frontal Lobe (M1), Spinal Cord |
| Working memory | Frontal Lobe (DLPFC) |
| Dopamine system | Brainstem (VTA, SNc), Basal Ganglia |
| Serotonin system | Brainstem (Raphe) |
| Norepinephrine system | Brainstem (Locus coeruleus) |
| Acetylcholine system | Brainstem, Basal Forebrain (in Limbic Structures) |
| Direct/indirect pathways | Basal Ganglia |
| Place cells | Limbic Structures (Hippocampus) |
| Grid cells | Temporal Lobe (Entorhinal) |
| Head direction cells | Limbic Lobe (RSC), Thalamus (Anterior) |
| Default mode network | Limbic Lobe (PCC), Frontal (vmPFC) |
| Salience network | Insular Lobe, Frontal/Limbic (ACC) |
| Mirror neurons | Frontal Lobe (PMv) |
| Fear conditioning | Limbic Structures (Amygdala) |
| LTP/plasticity | Limbic Structures (Hippocampus) |
| Circadian rhythm | Hypothalamus (SCN) |
| Stress response (HPA) | Hypothalamus |
| Papez circuit | Limbic Lobe, Limbic Structures, Hypothalamus, Thalamus |

---

## Version History

| Date | Change |
|------|--------|
| Initial | Created foundational documents (Brain Communication Architecture, Brain Functional Pathways) |
| Session 2-5 | Created Spinal Cord, Brainstem, Cerebellum comprehensive guides |
| Session 6-7 | Created Thalamus, Hypothalamus, Basal Ganglia, Limbic Structures documents |
| Session 8 | Created Canonical Cortical Microcircuit |
| Session 9 | Created Occipital Lobe document |
| Session 10 | Created Parietal Lobe, Temporal Lobe documents; accuracy review and corrections |
| Session 11 | Created Frontal Lobe, Insular Lobe, Limbic Lobe documents; Master Index |

---

*This index is the navigation guide for the Brain Architecture Knowledge Base. Use it to find specific regions, pathways, functions, or networks across the comprehensive documentation.*
