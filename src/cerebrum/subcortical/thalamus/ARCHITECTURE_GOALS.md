# Thalamus Architecture Goals

> **Status:** This document describes the target architecture. The current implementation uses a simplified channel-based model. This document guides the evolution toward nucleus-based routing.

## Vision

Build a biologically-faithful thalamus that serves as the **central routing hub** for all cortical communication. The cortex will have multi-layer semantics (L4/L5/L6), and thalamus must support:

- First-order sensory relay to primary cortex
- Higher-order routing enabling cortex-to-cortex communication
- Attention gating via TRN
- Integration with basal ganglia, cerebellum, and limbic systems

## Thalamus Internal Structure

```
INPUTS (generated outside)                              OUTPUTS (end outside)

[Retina] --------------------------------->  +--------------------------------------------------+  -----> [Primary visual cortex (V1)]
[Auditory brainstem / inf. colliculus] ---> |                                                  |  -----> [Primary auditory cortex (A1)]
[Somatosensory spinal cord/brainstem] ----> |          SUBCORTICAL THALAMUS STRUCTURE          |  -----> [Primary somatosensory cortex (S1)]
[Brainstem arousal neuromodulators] ------> |                                                  |  -----> [Association cortex (PFC/PPC/temporal)]
[Cortex L6 feedback (modulatory)] --------> |  INTERNAL ORGANIZATION:                          |  -----> [Widespread cortical arousal/attention]
[Cortex L5 feedforward to HO nuclei] -----> |                                                  |  -----> [Striatum (thalamostriatal)]
[Cerebellar deep nuclei] -----------------> |  * Relay nuclei (first-order)                    |  -----> [Motor cortex via VA/VL loops]
[Basal ganglia output (GPi/SNr)] ---------> |    - LGN (vision) / MGN (audition)               |  -----> [Limbic cortex (cingulate, etc.)]
[Limbic structures (amygdala/hippocampus)]->|    - VPL/VPM (somatosensory)                     |  -----> [Hippocampal/limbic network targets]
[Hypothalamus / homeostatic signals] -----> |    - VA/VL (motor-related relays)                |  -----> [Behavioral state control via cortex]
                                            |                                                  |
                                            |  * Association / higher-order nuclei             |
                                            |    - Pulvinar, LP/LD (attention/association)     |
                                            |    - MD (prefrontal/cognitive loops)             |
                                            |                                                  |
                                            |  * Diffuse / "nonspecific" nuclei                |
                                            |    - Intralaminar (CM/Pf/CL)                     |
                                            |    - Midline (PVT/Reuniens)                      |
                                            |                                                  |
                                            |  * Thalamic Reticular Nucleus (TRN)              |
                                            |    - Inhibitory shell gating thalamic traffic    |
                                            +--------------------------------------------------+
```

## Nucleus Classes

| Class | Nuclei | Input | Output | Role |
|-------|--------|-------|--------|------|
| **First-order** | LGN, MGN, VPL/VPM, VA/VL | Sensory/subcortical | Primary cortex L4 | Relay external world to cortex |
| **Higher-order** | Pulvinar, MD, LP/LD | Cortex L5 | Association cortex L4 | Cortex-to-cortex routing |
| **Diffuse** | CM, Pf, CL, PVT, Reuniens | Brainstem arousal | Widespread cortex | Arousal, alertness, state |
| **Gate** | TRN | Collaterals from all | Inhibits relay nuclei | Attention gating |

## Major Loops

### Loop A: Cortex <-> Thalamus <-> Cortex (Routing + Coordination)

Thalamus relays sensory and association signals to cortex and receives cortical feedback, shaping gain/attention and which channels dominate.

```
Sensory Input --> First-order nucleus --> Cortex L4
                         ^                    |
                         |                    v
                        TRN <------------- Cortex L6 (modulatory feedback)

Cortex L5 --> Higher-order nucleus --> Different Cortex Area L4
```

### Loop B: Cortex -> Basal Ganglia -> Thalamus -> Cortex (Selection/Gating)

Cortex proposes options -> basal ganglia select/suppress -> thalamus relays the "winner" back to cortex for execution.

```
Cortex --> Striatum --> GPi/SNr ---(inhibition release)---> VA/VL --> Motor Cortex
```

### Loop C: Cortex -> Pons -> Cerebellum -> Thalamus -> Cortex (Calibration)

Cortex sends a "plan/copy" -> cerebellum computes timing/error corrections -> thalamus relays adjustments back to cortex.

```
Cortex --> Pons --> Cerebellum --> VL --> Motor Cortex
```

### Loop D: Limbic -> Hypothalamus -> Brainstem/Spinal (Body Regulation)

Amygdala/hippocampus provide meaning/context -> hypothalamus sets autonomic + endocrine outputs -> brainstem/spinal circuits implement changes.

```
Amygdala/Hippocampus --> Hypothalamus --> Brainstem --> Body
                              |
                              v
                         Pituitary (endocrine)
```

## Cross-Links

| Link | Mechanism |
|------|-----------|
| **BG <-> Brainstem orienting** | SNr inhibits/releases superior colliculus (where you look/attend) |
| **Thalamus as shared choke-point** | BG and cerebellum both influence cortex through thalamic relays |
| **Limbic drives selection** | Amygdala valuation + hippocampus context bias what BG will "choose" |
| **Hypothalamus sets mode** | Hunger/stress/circadian state changes cortex priorities via brainstem modulators |
| **Brainstem neuromodulators tune everything** | Arousal, vigilance, mood, pain sensitivity change gating, processing, plasticity |

## Why Nucleus Model (Not Channel Model)

The channel-based model in `thalamus_contracts_async.py` is insufficient for the full vision because:

1. **Higher-order routing required**: Cortex L5 -> PULVINAR/MD -> different cortex area
2. **Layer-specific semantics**: L4 receives, L6 modulates same nucleus, L5 drives different nucleus
3. **BG/Cerebellar integration**: GPi -> VA/VL -> Motor cortex needs nucleus addressing
4. **Nucleus classes behave differently**: First-order vs higher-order vs diffuse have different routing rules

## Key Use Cases

1. **Attention shift**: Cortex requests "also stream audio from kitchen" via L5 -> PULVINAR -> target cortex
2. **Motor selection**: BG selects action -> releases VA/VL -> motor cortex executes
3. **Sensory gating**: TRN suppresses MGN (audio) while boosting LGN (visual) during visual attention
4. **Arousal broadcast**: Intralaminar nuclei broadcast alertness state to widespread cortex
5. **Context routing**: MD relays PFC signals for working memory / cognitive control

## Implementation Path

The current channel-based implementation (`thalamus_contracts_async.py`) provides a working foundation. The nucleus model (`thalamus_async.py`) defines the target contracts but needs implementation.

### Recommended Approach

1. Keep the **two-role pattern** (TRNController + ThalamusRouter)
2. Replace channel addressing with nucleus addressing
3. Add nucleus class routing semantics (first-order vs higher-order)
4. Implement cortex layer targeting (L4/L5/L6)

### Related Files

- `thalamus_contracts_async.py` - Current channel-based implementation
- `thalamus_async.py` - Target nucleus-based contracts (skeleton)
- `Thalamus.md` - Channel-based documentation (current)
- `Thalamus1.md` - Additional channel-based documentation
