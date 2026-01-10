# Region-Centric Communication Map: Cerebrum — Subcortical Structures — Basal Ganglia

This document provides a complete communication map for every component of the basal ganglia. For each nucleus, it specifies what that region communicates with at every level: within the basal ganglia, with other subcortical structures, with the brainstem, with the cerebellum (via relay), with the spinal cord (via relay), and with specific cortical areas including layer-level connectivity.

The basal ganglia are a group of interconnected nuclei critical for action selection — choosing which action to perform while suppressing competing alternatives. They do not initiate movements; rather, they gate which cortically-generated motor programs are allowed to proceed. Beyond motor control, parallel basal ganglia circuits handle cognitive action selection (which thought to pursue), limbic action selection (which reward to seek), and oculomotor control (where to look).

---

## Part 1: Overview of Basal Ganglia Organization

### Anatomical Components

The basal ganglia consist of several interconnected nuclei:

**Input Nuclei (receive cortical input):**
- Striatum (caudate nucleus, putamen, nucleus accumbens)

**Intrinsic Nuclei (process within basal ganglia):**
- Globus pallidus external segment (GPe)
- Subthalamic nucleus (STN)

**Output Nuclei (send output to thalamus):**
- Globus pallidus internal segment (GPi)
- Substantia nigra pars reticulata (SNr)

**Modulatory Structure:**
- Substantia nigra pars compacta (SNc) — dopamine source

### Functional Organization

The basal ganglia operate through three parallel pathways:

**Direct Pathway (GO):** Facilitates selected actions
- Cortex → Striatum (D1) → GPi/SNr → Thalamus → Cortex
- Net effect: Disinhibition of thalamus → action proceeds

**Indirect Pathway (NO-GO):** Suppresses competing actions
- Cortex → Striatum (D2) → GPe → STN → GPi/SNr → Thalamus → Cortex
- Net effect: Increased inhibition of thalamus → action suppressed

**Hyperdirect Pathway (STOP):** Rapid global inhibition
- Cortex → STN → GPi/SNr → Thalamus → Cortex
- Net effect: Fast, broad inhibition → emergency stop

### Circuit Logic

The key insight is that **GPi/SNr tonically inhibit the thalamus**. The default state is suppression of all actions. For an action to occur:
1. The direct pathway must release inhibition on thalamus (for the selected action)
2. The indirect pathway must maintain inhibition (for competing actions)
3. Dopamine biases this competition based on reward history

### Parallel Loops

The basal ganglia form multiple parallel loops with different cortical territories:

| Loop | Cortical Areas | Striatal Territory | Function |
|------|---------------|-------------------|----------|
| Motor | M1, premotor, SMA | Putamen | Movement selection |
| Oculomotor | FEF, SEF | Caudate (body) | Eye movement selection |
| Cognitive | DLPFC, PPC | Caudate (head) | Cognitive action selection |
| Limbic | OFC, ACC, vmPFC | Nucleus accumbens | Reward-based selection |

---

## Part 2: Striatum — The Input Station

The striatum is the primary input structure of the basal ganglia, receiving projections from nearly the entire cerebral cortex. It is the largest component of the basal ganglia.

### Anatomical Subdivisions

#### Caudate Nucleus

**Location and Structure:** C-shaped structure following the curve of the lateral ventricle. Has a large head (anterior), body, and tail that curves into the temporal lobe.

**Within Basal Ganglia:**
- **To GPe:** D2 medium spiny neurons (MSNs); GABAergic
- **To GPi:** D1 MSNs; GABAergic
- **To SNr:** D1 MSNs; GABAergic
- **To SNc:** Both D1 and D2 MSNs; feedback to dopamine neurons

**Within Subcortical Structures:**
- **From thalamus (intralaminar nuclei):**
  - From centromedian (CM): Motor attention
  - From parafascicular (Pf): Cognitive attention, learning signals
  - From central lateral (CL): Arousal
  - Glutamatergic; thalamostriatal pathway
- **From amygdala:** To ventral caudate; emotional significance
- **From hippocampus (indirect):** Via entorhinal → ventral striatum

**From Brainstem:**
- **From SNc:** MAJOR dopaminergic input (nigrostriatal pathway)
  - D1 receptors: Excites direct pathway MSNs
  - D2 receptors: Inhibits indirect pathway MSNs
- **From VTA:** Dopaminergic; especially to ventromedial caudate
- **From dorsal raphe:** Serotonergic modulation
- **From locus coeruleus:** Noradrenergic modulation
- **From PPN:** Cholinergic and glutamatergic

**From Cerebral Cortex:**
- **From prefrontal cortex (DLPFC, OFC, ACC):** MAJOR input to head of caudate
  - **Layer V:** Primary source of corticostriatal projections
  - **Layer III:** Also contributes
  - Glutamatergic
  - Cognitive/executive information
- **From posterior parietal cortex:** Spatial, attentional
- **From frontal eye fields (FEF):** Oculomotor
- **From temporal cortex:** Visual object information

**To Cerebral Cortex:**
- No direct projection to cortex (output via GPi/SNr → thalamus → cortex)

**Topographic Organization:**
- Head: Cognitive/limbic (prefrontal input)
- Body: Oculomotor (FEF input)
- Tail: Visual (temporal cortex input)

**Functions:**
- Cognitive action selection
- Goal-directed behavior
- Learning action-outcome associations
- Oculomotor control (saccade selection)
- Cognitive flexibility

**Primary Inputs:**
- Prefrontal cortex Layer V: Cognitive
- Intralaminar thalamus (Pf): Attention, learning
- SNc: Dopamine modulation

**Primary Outputs:**
- GPe: Indirect pathway
- GPi/SNr: Direct pathway


#### Putamen

**Location and Structure:** Large, rounded structure lateral to the caudate, separated from it by the internal capsule. Together with the caudate, forms the dorsal striatum.

**Within Basal Ganglia:**
- **To GPe:** D2 MSNs; GABAergic; indirect pathway
- **To GPi:** D1 MSNs; GABAergic; direct pathway
- **To SNr:** D1 MSNs; GABAergic
- **To SNc:** Feedback to dopamine neurons

**Within Subcortical Structures:**
- **From thalamus (intralaminar nuclei):**
  - From centromedian (CM): MAJOR input; motor attention
  - Glutamatergic
- **From amygdala:** Emotional motor responses

**From Brainstem:**
- **From SNc:** MAJOR dopaminergic input (nigrostriatal pathway)
  - Motor loop dopamine
  - Loss in Parkinson's disease primarily affects putamen
- **From dorsal raphe:** Serotonergic
- **From PPN:** Cholinergic, glutamatergic

**From Cerebral Cortex:**
- **From primary motor cortex (M1):** MAJOR input
  - **Layer V:** Corticostriatal projection
  - Somatotopic organization preserved
  - Motor commands
- **From premotor cortex:** Motor planning
- **From SMA:** Motor sequences
- **From primary somatosensory cortex (S1):** Sensory feedback
  - **Layer V:** Corticostriatal
- **From posterior parietal cortex:** Sensorimotor integration

**To Cerebral Cortex:**
- No direct projection (via GPi → VL thalamus → motor cortex)

**Topographic Organization:**
- Somatotopic: Leg (dorsal), arm (middle), face (ventral)
- Mirrors motor cortex organization

**Functions:**
- Motor action selection
- Habitual/automatic movements
- Procedural learning (skills)
- Stimulus-response habits

**Primary Inputs:**
- Motor cortex Layer V: Motor commands
- Somatosensory cortex Layer V: Sensory feedback
- CM thalamus: Motor attention
- SNc: Dopamine

**Primary Outputs:**
- GPe: Indirect pathway
- GPi: Direct pathway


#### Nucleus Accumbens (Ventral Striatum)

**Location and Structure:** Located where the caudate and putamen meet anteriorly, at the base of the basal ganglia. Divided into core and shell subregions.

**Within Basal Ganglia:**
- **To ventral pallidum:** GABAergic; main output
- **To GPe (from core):** Some projections
- **To SNr:** Direct pathway
- **To VTA:** Feedback to dopamine neurons

**Within Subcortical Structures:**
- **From VTA:** MAJOR dopaminergic input (mesolimbic pathway)
  - Reward prediction error
  - Motivation, pleasure
  - Key target for drugs of abuse
- **From amygdala (basolateral):** MAJOR input
  - Emotional value, learned associations
  - Glutamatergic
- **From hippocampus (ventral):** Contextual information
  - Via subiculum
  - Glutamatergic
- **From thalamus (midline nuclei):**
  - Paraventricular, reuniens
  - Arousal, context

**From Brainstem:**
- **From VTA:** MAJOR dopaminergic (mesolimbic)
- **From dorsal raphe:** Serotonergic (mood)
- **From LDT/PPT:** Cholinergic (reward processing)
- **From locus coeruleus:** Noradrenergic

**From Cerebral Cortex:**
- **From orbitofrontal cortex (OFC):**
  - **Layer V:** Corticostriatal
  - Value information
- **From anterior cingulate cortex (ACC):**
  - **Layer V**
  - Effort, motivation
- **From ventromedial PFC (vmPFC):**
  - **Layer V**
  - Emotional regulation
- **From medial PFC (mPFC):**
  - Context, goals
- **From insula:**
  - Interoceptive information

**To Cerebral Cortex:**
- No direct projection (via ventral pallidum → MD thalamus → PFC)

**Subdivisions:**
- **Core:** More like dorsal striatum
  - Motor aspects of reward
  - Instrumental conditioning
  - Projects to ventral pallidum, SNr
- **Shell:** More like extended amygdala
  - Hedonic aspects of reward
  - Pavlovian conditioning
  - Projects to ventral pallidum, VTA, hypothalamus

**Functions:**
- Reward processing
- Motivation and drive
- Pleasure and hedonia
- Addiction (drugs hijack this system)
- Effort-based decision making
- Linking reward to action

**Primary Inputs:**
- VTA: Dopamine (reward prediction error)
- Amygdala: Emotional value
- Hippocampus: Context
- OFC, vmPFC, ACC: Value, effort

**Primary Outputs:**
- Ventral pallidum: Main output
- VTA: Feedback


### Striatal Microcircuitry

#### Medium Spiny Neurons (MSNs)

**Proportion:** ~95% of striatal neurons

**Two populations:**
- **D1 MSNs (direct pathway):**
  - Express D1 dopamine receptors
  - Express substance P, dynorphin
  - Project to GPi/SNr
  - Dopamine excites these neurons
  - Facilitate selected actions

- **D2 MSNs (indirect pathway):**
  - Express D2 dopamine receptors
  - Express enkephalin
  - Project to GPe
  - Dopamine inhibits these neurons
  - Suppress competing actions

**Both receive:**
- Cortical glutamatergic input
- Thalamic glutamatergic input
- Dopaminergic modulation
- Cholinergic modulation (from interneurons)

#### Striatal Interneurons

**Cholinergic Interneurons (ChIs):**
- ~1-2% of striatal neurons
- Tonically active neurons (TANs)
- Pause firing during learning
- Modulate MSN excitability
- Receive input from thalamus (intralaminar), cortex, SNc

**GABAergic Interneurons:**
- Fast-spiking (FS): Parvalbumin+; feedforward inhibition
- Low-threshold spiking (LTS): Somatostatin+; feedback inhibition
- Others: Calretinin+, NPY+

**Interneuron Function:**
- Shape temporal dynamics of MSN firing
- Create competition between MSN ensembles
- Critical for learning

---

## Part 3: Globus Pallidus — Processing Hub

The globus pallidus (pale globe) consists of two segments with different functions.

### Globus Pallidus External Segment (GPe)

**Location and Function:** Located medial to the putamen, lateral to GPi. Part of the indirect pathway — receives striatal input and projects to STN.

**Within Basal Ganglia:**
- **From striatum (D2 MSNs):** MAJOR input
  - From caudate: Cognitive
  - From putamen: Motor
  - GABAergic; inhibitory
- **To STN:** MAJOR output
  - GABAergic; inhibitory
  - Tonically active; constantly inhibits STN
- **To GPi:** Direct connection (arkypallidal neurons)
  - GABAergic
  - May provide feedback inhibition
- **To striatum (arkypallidal neurons):** Feedback
  - GABAergic
  - Regulates striatal activity
- **From STN:** Glutamatergic; reciprocal connection

**Within Subcortical Structures:**
- **To thalamic reticular nucleus (TRN):** Inhibitory
- **From thalamus (minor):** Some input

**From Brainstem:**
- **From SNc:** Dopaminergic modulation
- **From PPN:** Cholinergic, glutamatergic
- **From STN (considered brainstem by some):** Glutamatergic

**From Cerebral Cortex:**
- **From cortex (minor):** Some direct corticopallidal input
  - **Layer V**
  - Much less than corticostriatal

**To Cerebral Cortex:**
- No direct cortical projection

**Cell Types:**
- **Prototypic neurons (~70%):** Project to STN; classic indirect pathway
- **Arkypallidal neurons (~30%):** Project back to striatum; feedback

**Firing Properties:**
- Tonically active (~60 Hz at rest)
- GABAergic; constant inhibition of STN
- Pauses when indirect pathway activated

**Indirect Pathway Role:**
1. D2 MSNs activated by cortex
2. D2 MSNs inhibit GPe
3. GPe releases STN from inhibition
4. STN excites GPi
5. GPi increases inhibition of thalamus
6. Action suppressed

**Primary Inputs:**
- Striatum D2 MSNs: Indirect pathway
- STN: Reciprocal excitation

**Primary Outputs:**
- STN: Indirect pathway continuation
- GPi: Direct pallidal connection
- Striatum: Feedback (arkypallidal)


### Globus Pallidus Internal Segment (GPi)

**Location and Function:** Located medial to GPe. One of the two main OUTPUT nuclei of the basal ganglia (along with SNr). Tonically inhibits thalamus; release of this inhibition allows movement.

**Within Basal Ganglia:**
- **From striatum (D1 MSNs):** Direct pathway
  - GABAergic; inhibitory
  - Inhibits GPi → releases thalamus
- **From STN:** Hyperdirect and indirect pathways
  - Glutamatergic; excitatory
  - Excites GPi → increases thalamic inhibition
- **From GPe:** Some direct input
  - GABAergic

**Within Subcortical Structures:**
- **To thalamus (VL, VA):** MAJOR output
  - GABAergic; inhibitory
  - Tonically active; constant thalamic inhibition
  - VL → motor cortex
  - VA → premotor, prefrontal cortex
- **To thalamus (CM):** Feedback to intralaminar
- **To lateral habenula:** Reward-related signals
  - Encodes negative reward prediction error
  - Projects to structures that inhibit dopamine neurons

**From Brainstem:**
- **From PPN:** Cholinergic, glutamatergic
- **From SNc:** Dopaminergic modulation

**To Brainstem:**
- **To PPN:** Motor output; locomotion
- **To superior colliculus (minor):** Eye movements (SNr is primary)

**From Cerebral Cortex:**
- Minimal direct input

**To Cerebral Cortex:**
- No direct projection (via thalamus)

**Firing Properties:**
- Tonically active (~80-100 Hz at rest)
- GABAergic
- High spontaneous rate maintains thalamic inhibition
- Pauses allow movement

**Circuit Logic:**
- DEFAULT: GPi fires → thalamus inhibited → no movement
- DIRECT PATHWAY: D1 MSNs inhibit GPi → thalamus released → movement
- INDIRECT/HYPERDIRECT: STN excites GPi → more thalamic inhibition → no movement

**Primary Inputs:**
- Striatum D1 MSNs: Direct pathway (inhibitory)
- STN: Indirect/hyperdirect pathways (excitatory)

**Primary Outputs:**
- Thalamus VL/VA: Motor and cognitive relay


---

## Part 4: Subthalamic Nucleus (STN)

**Location and Function:** Located below the thalamus, above the substantia nigra. The ONLY excitatory nucleus in the basal ganglia circuit (uses glutamate, not GABA). Critical node in both indirect and hyperdirect pathways.

**Within Basal Ganglia:**
- **From GPe:** MAJOR input
  - GABAergic; inhibitory
  - Tonically inhibited by GPe
  - Release from GPe inhibition → STN fires → GPi excited
- **To GPi:** MAJOR output
  - Glutamatergic; excitatory
  - Broad divergent projection
  - Excites GPi → thalamic inhibition → suppresses movement
- **To SNr:** Glutamatergic; excitatory
  - Similar to GPi projection
- **To GPe:** Reciprocal connection
  - Glutamatergic
  - STN-GPe form oscillatory circuit (pathological in Parkinson's)

**Within Subcortical Structures:**
- **To thalamus (minor):** Some direct
- **From thalamus (CM, Pf):** Some input

**From Brainstem:**
- **From PPN:** Glutamatergic and cholinergic
  - Locomotion, arousal
- **From SNc:** Dopaminergic modulation
- **From dorsal raphe:** Serotonergic

**To Brainstem:**
- **To PPN:** Motor output
- **To SNc:** Influences dopamine neurons
- **To SNr:** Part of output pathway

**From Cerebral Cortex:**
- **From motor cortex (M1, premotor, SMA):** HYPERDIRECT pathway
  - **Layer V:** Direct corticosubthalamic projection
  - Glutamatergic
  - Fastest basal ganglia pathway (bypasses striatum)
  - Provides rapid "brake" on movement
- **From prefrontal cortex:** Cognitive hyperdirect
- **From frontal eye fields:** Oculomotor

**To Cerebral Cortex:**
- No direct projection

**Topographic Organization:**
- Motor territory (dorsolateral): Motor cortex input
- Associative territory (ventromedial): Prefrontal input
- Limbic territory (medial tip): ACC, OFC input

**Firing Properties:**
- Tonically active (~20-30 Hz at rest)
- Glutamatergic (excitatory)
- Burst firing in Parkinson's disease (pathological)

**Three Pathway Roles:**

**Indirect Pathway:**
1. Striatum D2 → inhibits GPe
2. GPe releases STN from inhibition
3. STN excites GPi
4. GPi inhibits thalamus
5. Action suppressed

**Hyperdirect Pathway:**
1. Cortex directly excites STN (bypasses striatum)
2. STN excites GPi broadly
3. GPi inhibits thalamus globally
4. All actions rapidly suppressed
5. Faster than direct pathway; "emergency stop"

**Clinical Significance:**
- Target for deep brain stimulation (DBS) in Parkinson's disease
- DBS disrupts pathological oscillations
- Dramatically reduces tremor, rigidity

**Primary Inputs:**
- GPe: Indirect pathway (inhibitory)
- Motor cortex Layer V: Hyperdirect pathway (excitatory)

**Primary Outputs:**
- GPi/SNr: Output nuclei (excitatory)
- GPe: Reciprocal


---

## Part 5: Substantia Nigra

Located in the midbrain (technically brainstem), the substantia nigra has two functionally distinct parts that are critical components of basal ganglia circuitry.

### Substantia Nigra Pars Compacta (SNc)

**Location and Function:** Dorsal part of substantia nigra. Contains dopamine neurons that project to the striatum. The modulatory component of basal ganglia — dopamine biases the competition between direct and indirect pathways.

**Within Basal Ganglia:**
- **To striatum (caudate and putamen):** MAJOR output — nigrostriatal pathway
  - Dopaminergic
  - To D1 MSNs: Excitatory (via D1 receptors, Gs-coupled)
  - To D2 MSNs: Inhibitory (via D2 receptors, Gi-coupled)
  - Net effect: Dopamine biases toward direct pathway (GO)
- **From striatum:** Feedback
  - From D1 MSNs: Substance P, GABA
  - From D2 MSNs: Enkephalin, GABA
- **To GPe, GPi, STN:** Minor dopaminergic modulation

**Within Subcortical Structures:**
- **To amygdala:** Minor; emotional processing
- **To thalamus (intralaminar):** Minor
- **Distinct from VTA:** VTA projects to limbic structures (mesolimbic); SNc projects to motor striatum (nigrostriatal)

**From Brainstem:**
- **From PPN:** Glutamatergic and cholinergic
  - Excites dopamine neurons
  - Locomotion-reward link
- **From LDT:** Cholinergic
- **From raphe nuclei:** Serotonergic modulation
- **From locus coeruleus:** Noradrenergic
- **From superior colliculus:** Visual salience

**To Brainstem:**
- **To PPN:** Feedback
- **To superior colliculus:** Modulation

**From Subcortical/Cortical:**
- **From striatum:** Feedback (as noted above)
- **From STN:** Glutamatergic; can drive dopamine release
- **From lateral habenula:** Inhibitory (via RMTg)
  - Encodes negative prediction error

**To Cerebral Cortex:**
- Minimal direct projection (striatum is main target)

**From Cerebral Cortex:**
- **From motor and prefrontal cortex:** Minor direct input

**Dopamine and Reward Prediction Error:**

SNc neurons encode **reward prediction error** (like VTA):
- **Unexpected reward:** Burst firing (positive prediction error)
- **Expected reward:** No change
- **Expected reward omitted:** Pause in firing (negative prediction error)

This signal teaches the striatum:
- Burst → strengthen recently active D1 synapses (LTP)
- Pause → strengthen recently active D2 synapses; weaken D1

**Clinical Significance:**
- **Parkinson's disease:** Death of SNc dopamine neurons
  - 60-80% loss before symptoms appear
  - Putamen most affected (motor symptoms)
  - Dopamine depletion → imbalanced pathways
  - Direct pathway weakened, indirect pathway strengthened
  - Result: Difficulty initiating movement (bradykinesia)

**Primary Inputs:**
- Striatum: Feedback
- PPN: Locomotion
- STN: Excitation
- Lateral habenula (via RMTg): Inhibition

**Primary Outputs:**
- Striatum: Nigrostriatal dopamine


### Substantia Nigra Pars Reticulata (SNr)

**Location and Function:** Ventral part of substantia nigra. One of the two OUTPUT nuclei of basal ganglia (along with GPi). Functionally similar to GPi but with different targets — particularly important for eye movements.

**Within Basal Ganglia:**
- **From striatum (D1 MSNs):** Direct pathway
  - GABAergic; inhibitory
  - From caudate (particularly body): Oculomotor
  - Inhibits SNr → releases superior colliculus → saccade
- **From STN:** Indirect and hyperdirect pathways
  - Glutamatergic; excitatory
  - Excites SNr → more collicular inhibition → no saccade

**Within Subcortical Structures:**
- **To thalamus (VA, MD):** GABAergic output
  - Similar to GPi but different thalamic nuclei
  - VA → prefrontal cortex
  - MD → prefrontal cortex (cognitive loops)
- **To superior colliculus:** MAJOR output
  - GABAergic; inhibitory
  - Tonically inhibits SC
  - Release → saccadic eye movement
  - Critical for voluntary gaze control

**To Brainstem:**
- **To superior colliculus:** Eye movement gating
- **To PPN:** Locomotion
- **To reticular formation:** Orienting

**From Brainstem:**
- **From PPN:** Glutamatergic, cholinergic
- **From superior colliculus:** Feedback

**From Cerebral Cortex:**
- Minimal direct input

**To Cerebral Cortex:**
- No direct projection (via thalamus)

**Firing Properties:**
- Tonically active (~60-80 Hz)
- GABAergic
- Constant inhibition of superior colliculus
- Pauses allow saccades

**Function — Oculomotor Control:**
1. FEF activates caudate D1 neurons (for desired saccade direction)
2. Caudate inhibits SNr
3. SNr releases superior colliculus from inhibition
4. Superior colliculus generates saccade

**Function — Cognitive:**
- Parallel to GPi for cognitive loops
- Projects to VA/MD thalamus → prefrontal cortex

**Primary Inputs:**
- Caudate D1 MSNs: Direct pathway (inhibitory)
- STN: Indirect/hyperdirect (excitatory)

**Primary Outputs:**
- Superior colliculus: Saccade gating
- Thalamus VA/MD: Cognitive output


---

## Part 6: Ventral Pallidum

**Location and Function:** Located below the anterior commissure, continuous with GPe/GPi. The output nucleus for the limbic/ventral basal ganglia loop (nucleus accumbens circuit).

**Within Basal Ganglia:**
- **From nucleus accumbens:** MAJOR input
  - GABAergic
  - D1 MSNs (direct pathway analog)
  - D2 MSNs (indirect pathway analog)
- **From STN (ventral):** Glutamatergic

**Within Subcortical Structures:**
- **To thalamus (MD):** MAJOR output
  - GABAergic
  - MD → prefrontal cortex (OFC, vmPFC, mPFC)
  - Limbic/reward output to cortex
- **To lateral habenula:** Reward prediction error
- **To VTA:** Feedback to dopamine neurons
- **From amygdala:** Emotional input

**To Brainstem:**
- **To VTA:** Modulates dopamine
- **To PPN:** Limbic motor output
- **To lateral hypothalamus:** Reward-related behavior

**From Cerebral Cortex:**
- Minimal direct

**To Cerebral Cortex:**
- Via MD thalamus → prefrontal cortex

**Functions:**
- Limbic action selection
- Reward-guided behavior
- Motivation and drive
- Hedonic processing

**Primary Inputs:**
- Nucleus accumbens: Limbic striatum

**Primary Outputs:**
- MD thalamus: Limbic relay to PFC
- VTA: Dopamine modulation


---

## Part 7: Basal Ganglia Pathways — Detailed Circuit Descriptions

### Direct Pathway (GO)

**Circuit:**
Cortex (Layer V) → Striatum (D1 MSNs) → GPi/SNr → Thalamus (VL/VA) → Cortex (Layer IV, III)

**Detailed Flow:**

1. **Cortex → Striatum:**
   - Layer V pyramidal neurons project to striatum
   - Glutamatergic (excitatory)
   - Activates specific ensemble of D1 MSNs
   - Topographically organized

2. **Striatum → GPi/SNr:**
   - D1 MSNs project to GPi (motor) or SNr (oculomotor, cognitive)
   - GABAergic (inhibitory)
   - Inhibits GPi/SNr neurons
   - Focused inhibition (specific to selected action)

3. **GPi/SNr → Thalamus:**
   - GPi/SNr normally tonically inhibit thalamus
   - When inhibited by striatum, GPi/SNr stops inhibiting thalamus
   - Double negative = disinhibition
   - Thalamus released for selected action only

4. **Thalamus → Cortex:**
   - VL/VA project to motor and premotor cortex
   - Glutamatergic (excitatory)
   - Layer IV (and III) primary termination
   - Completes the loop; facilitates selected action

**Net Effect:** Selected action facilitated

**Dopamine Modulation:**
- D1 receptors on D1 MSNs
- Dopamine excites D1 MSNs (Gs → increased cAMP)
- More dopamine → stronger direct pathway → more likely to act


### Indirect Pathway (NO-GO)

**Circuit:**
Cortex (Layer V) → Striatum (D2 MSNs) → GPe → STN → GPi/SNr → Thalamus → Cortex

**Detailed Flow:**

1. **Cortex → Striatum:**
   - Layer V pyramidal neurons project to striatum
   - Glutamatergic (excitatory)
   - Activates D2 MSNs representing competing actions

2. **Striatum → GPe:**
   - D2 MSNs project to GPe
   - GABAergic (inhibitory)
   - Inhibits GPe

3. **GPe → STN:**
   - GPe normally tonically inhibits STN
   - When GPe inhibited, STN released from inhibition
   - STN activity increases

4. **STN → GPi/SNr:**
   - STN projects broadly to GPi/SNr
   - Glutamatergic (excitatory)
   - Excites GPi/SNr
   - Broad excitation (affects multiple action channels)

5. **GPi/SNr → Thalamus:**
   - Increased GPi/SNr activity
   - More thalamic inhibition
   - Actions suppressed

6. **Thalamus → Cortex:**
   - Less thalamic excitation of cortex
   - Actions not facilitated

**Net Effect:** Competing actions suppressed

**Dopamine Modulation:**
- D2 receptors on D2 MSNs
- Dopamine inhibits D2 MSNs (Gi → decreased cAMP)
- More dopamine → weaker indirect pathway → less suppression
- Less dopamine → stronger indirect pathway → more suppression (Parkinson's)


### Hyperdirect Pathway (STOP)

**Circuit:**
Cortex (Layer V) → STN → GPi/SNr → Thalamus → Cortex

**Detailed Flow:**

1. **Cortex → STN:**
   - Direct projection from motor cortex Layer V to STN
   - Bypasses striatum entirely
   - Glutamatergic (excitatory)
   - FASTEST pathway (fewer synapses)

2. **STN → GPi/SNr:**
   - STN excites GPi/SNr broadly
   - Glutamatergic
   - Global excitation (all channels)

3. **GPi/SNr → Thalamus:**
   - Increased GPi/SNr activity
   - Global thalamic inhibition
   - ALL actions suppressed rapidly

**Net Effect:** Emergency stop; global action suppression

**Timing:**
- Hyperdirect: ~10 ms (cortex to GPi)
- Direct: ~20 ms (cortex to GPi via striatum)
- This timing difference allows hyperdirect to "brake" before direct can "go"

**Function:**
- Stopping initiated actions
- Response inhibition (stop-signal task)
- Impulse control
- Allows "reset" before selecting new action


### Pathway Interactions

**Action Selection Model:**

1. **Multiple actions represented in cortex**
2. **Hyperdirect provides global pause** (STN → GPi)
3. **Direct pathway selects winner** (D1 → GPi; focused disinhibition)
4. **Indirect pathway suppresses losers** (D2 → GPe → STN → GPi; broad inhibition)
5. **Winner emerges** (thalamus released only for selected action)
6. **Motor command executes**

**Center-Surround Organization:**
- Direct pathway: Focused facilitation (center)
- Indirect pathway: Broad suppression (surround)
- Like lateral inhibition in sensory systems


---

## Part 8: Basal Ganglia Loops with Cortex

### Motor Loop

**Cortical Areas:** Primary motor (M1), premotor, SMA

**Striatal Territory:** Putamen (somatotopic)

**Pallidal/Nigral:** GPi (motor territory)

**Thalamic Nuclei:** VL (VLp for motor)

**Function:** Movement selection and execution

**Layer Connectivity:**
- Motor cortex Layer V → Putamen
- VL → Motor cortex Layer IV, III


### Oculomotor Loop

**Cortical Areas:** Frontal eye fields (FEF), supplementary eye fields (SEF)

**Striatal Territory:** Caudate (body)

**Pallidal/Nigral:** SNr

**Thalamic Nuclei:** VA, MD

**Brainstem Output:** Superior colliculus

**Function:** Saccade selection; voluntary gaze

**Layer Connectivity:**
- FEF Layer V → Caudate
- VA/MD → FEF Layer IV


### Prefrontal/Cognitive Loop

**Cortical Areas:** DLPFC, posterior parietal cortex

**Striatal Territory:** Caudate (head, dorsolateral)

**Pallidal/Nigral:** GPi (associative territory), SNr

**Thalamic Nuclei:** VA, MD

**Function:** Cognitive action selection; working memory; planning

**Layer Connectivity:**
- DLPFC Layer V → Caudate
- VA/MD → DLPFC Layer IV, III


### Orbitofrontal Loop

**Cortical Areas:** OFC, vmPFC

**Striatal Territory:** Caudate (ventromedial), nucleus accumbens

**Pallidal/Nigral:** Ventral pallidum, GPi (ventral)

**Thalamic Nuclei:** MD

**Function:** Value-based decision making; reward

**Layer Connectivity:**
- OFC Layer V → Ventral striatum
- MD → OFC Layer IV


### Anterior Cingulate Loop

**Cortical Areas:** ACC, mPFC

**Striatal Territory:** Nucleus accumbens, ventral caudate

**Pallidal/Nigral:** Ventral pallidum

**Thalamic Nuclei:** MD

**Function:** Motivation; effort allocation; error monitoring

**Layer Connectivity:**
- ACC Layer V → Ventral striatum
- MD → ACC Layer IV


---

## Part 9: Neuromodulation of Basal Ganglia

### Dopamine (from SNc, VTA)

**Sources:**
- SNc → dorsal striatum (caudate, putamen): Nigrostriatal
- VTA → ventral striatum (NAc): Mesolimbic

**Receptors:**
- D1 (Gs): Excitatory; on direct pathway MSNs
- D2 (Gi): Inhibitory; on indirect pathway MSNs

**Function:**
- Biases direct vs indirect pathway balance
- Encodes reward prediction error
- Teaches striatum which actions lead to reward
- Modulates motivation and movement initiation

**Pathology:**
- Low dopamine (Parkinson's): Bradykinesia, rigidity
- Excess dopamine (L-DOPA, addiction): Dyskinesia, compulsive behavior


### Acetylcholine (from striatal interneurons, PPN)

**Sources:**
- Cholinergic interneurons (within striatum)
- PPN (external)

**Receptors:**
- Muscarinic (M1, M4) on MSNs
- Nicotinic on various targets

**Function:**
- Opposes dopamine (in some ways)
- Pause in ChI firing signals salience
- Modulates plasticity and learning
- PPN input promotes movement

**Pathology:**
- Parkinson's: Cholinergic/dopaminergic imbalance → tremor
- Anticholinergics can reduce tremor


### Serotonin (from raphe nuclei)

**Source:** Dorsal raphe nucleus

**Function:**
- Modulates MSN excitability
- Interacts with dopamine system
- May signal aversive prediction errors
- Implicated in impulse control


### Norepinephrine (from locus coeruleus)

**Source:** Locus coeruleus

**Function:**
- Arousal-dependent modulation
- May affect response vigor
- Less studied than dopamine


---

## Part 10: Summary Tables

### Structures and Neurotransmitters

| Structure | Neurotransmitter | Projection Target | Effect |
|-----------|-----------------|-------------------|--------|
| D1 MSNs | GABA | GPi/SNr | Inhibitory |
| D2 MSNs | GABA | GPe | Inhibitory |
| GPe | GABA | STN, GPi, striatum | Inhibitory |
| GPi | GABA | Thalamus (VL, VA) | Inhibitory |
| SNr | GABA | Thalamus, superior colliculus | Inhibitory |
| STN | Glutamate | GPi, SNr, GPe | Excitatory |
| SNc | Dopamine | Striatum | Modulatory |

### Pathway Summary

| Pathway | Route | Net Effect on Thalamus | Function |
|---------|-------|----------------------|----------|
| Direct | Cortex→Str(D1)→GPi→Thal | Disinhibition | Facilitate selected action |
| Indirect | Cortex→Str(D2)→GPe→STN→GPi→Thal | Increased inhibition | Suppress competing actions |
| Hyperdirect | Cortex→STN→GPi→Thal | Fast, broad inhibition | Emergency stop |

### Input and Output Summary

| Component | Main Inputs | Main Outputs |
|-----------|------------|--------------|
| Striatum | Cortex (Layer V), thalamus (intralaminar), SNc | GPe, GPi, SNr |
| GPe | Striatum (D2), STN | STN, GPi, striatum |
| STN | GPe, cortex (Layer V) | GPi, SNr, GPe |
| GPi | Striatum (D1), STN | Thalamus (VL, VA) |
| SNr | Striatum (D1), STN | Thalamus (VA, MD), superior colliculus |
| SNc | Striatum, PPN, STN | Striatum |
| Ventral pallidum | Nucleus accumbens | MD thalamus, VTA |

### Thalamic Relay

| Basal Ganglia Output | Thalamic Target | Cortical Target |
|---------------------|-----------------|-----------------|
| GPi (motor) | VL | M1, premotor, SMA |
| GPi (associative) | VA | Premotor, DLPFC |
| SNr (oculomotor) | VA, MD | FEF |
| SNr (cognitive) | MD | PFC |
| Ventral pallidum | MD | OFC, vmPFC, ACC |

---

*This document provides a complete region-centric communication map for the basal ganglia. Each nucleus is described in terms of what it communicates with at every level: within the basal ganglia, with other subcortical structures, with the brainstem, with the spinal cord (via relay), and with specific cortical areas including layer-level connectivity.*
