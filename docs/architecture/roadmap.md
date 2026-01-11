# brain-mimc Reference Architecture Roadmap

## Expert Consensus (Updated 2026-01-11)

**Question:** Should we build loops first?

| Expert | Verdict |
|--------|---------|
| Architecture | "Loops first" is unsound - you have contracts, not implementations |
| Neuroscience | Brain evolved bottom-up - foundation before loops |

**User Goal:** Build the whole system like the brain - each loop concurrent and non-blocking

**Updated Approach:** Loop Zero FIRST (prove concurrency), then foundation-up with loop awareness

---

## Loop Zero: Concurrent Proof-of-Concept

### Goal

Prove that Cortex-Thalamus-Cortex can run on **separate processes/cores** without blocking.

### Architecture (Expert-Approved)

```
┌──────────────────┐     MQTT      ┌──────────────────┐     MQTT      ┌──────────────────┐
│   Process 1      │◄────────────►│   Process 2      │◄────────────►│   Process 3      │
│   CORTEX L4/L5   │               │   THALAMUS       │               │   TRN (Gate)     │
│   (Receive/Send) │               │   (Relay)        │               │   (Inhibit)      │
└──────────────────┘               └──────────────────┘               └──────────────────┘
     PID: 1001                          PID: 1002                          PID: 1003
```

### Why MQTT (Not InMemoryTopicBus)

| Requirement | InMemoryTopicBus | MQTT |
|-------------|------------------|------|
| Cross-process | NO (single Python process) | YES |
| Cross-machine | NO | YES |
| Proves non-blocking | NO (could be same thread) | YES |
| Production-ready | NO (testing only) | YES |

### Success Criteria

| Criterion | How to Verify |
|-----------|---------------|
| Processes are separate | `ps aux` shows 3 distinct PIDs |
| No shared memory | Processes can't access each other's variables |
| Non-blocking | Each process logs activity while others are busy |
| Message flow works | Cortex→Thalamus→Cortex round-trip completes |
| TRN can gate | TRN inhibition blocks messages to Cortex |

### Implementation Steps

1. **Setup MQTT broker** (Mosquitto - already documented)
2. **Create minimal contracts**:
   - `ThalamicEnvelope` (driver signal)
   - `GateState` (TRN state)
   - `RouteDecision` (thalamus decision)
3. **Create 3 Python scripts**:
   - `loop_zero_cortex.py` - Subscribes to relay, publishes requests
   - `loop_zero_thalamus.py` - Relays based on nucleus
   - `loop_zero_trn.py` - Publishes gate states
4. **Run demo**:
   ```bash
   # Terminal 1: Start broker
   mosquitto -c /etc/mosquitto/mosquitto.conf

   # Terminal 2-4: Start each process
   python demos/loop_zero/loop_zero_cortex.py &
   python demos/loop_zero/loop_zero_thalamus.py &
   python demos/loop_zero/loop_zero_trn.py &
   ```
5. **Verify**: Check logs show concurrent activity across all 3 processes

### Brain-Faithfulness (neuro-expert confirmed)

| Aspect | Brain Analogy | Our Implementation |
|--------|---------------|-------------------|
| Separate hardware | Brain regions are anatomically separate | Separate OS processes |
| Async communication | Axons don't block for response | MQTT pub-sub |
| No central orchestrator | Brain has no "main loop" | Each process runs independently |
| TRN gating | TRN inhibits thalamic relay | TRN process publishes GateState |

---

## The Hybrid Approach

### Step 1: Define Loop Contracts (What Each Loop Needs)

| Loop | Required Components | Required Messages |
|------|--------------------|--------------------|
| A | Thalamus (relay + TRN), Cortex | ThalamicEnvelope, RouteDecision, GateState |
| B | BG (Striatum, GPi), Thalamus (VA/VL), Cortex | CandidateAction, SelectionDecision |
| C | Cerebellum, Thalamus (VLp), Inferior Olive | ErrorSignal, Adjustment |
| D | Hypothalamus, Brainstem, Limbic | HomeostaticState, RegulationDecision |
| E | Hippocampus, Ant. Thalamus, Cingulate | EpisodicMemoryTrace, RetrievalResult |

### Step 2: Fix Blocking Issues

| Issue | Impact | Files |
|-------|--------|-------|
| Type duplication | Runtime failures | 5 files with ScopeLevel duplicates |
| Missing BasePlaneFacade | Can't integrate | BG, Limbic, Hypothalamus |
| RelayBundle.channel | Wrong addressing | brainstem/contracts.py |

### Step 3: Build Foundation (With Loop Awareness)

| Phase | Component | Loop Integration Point |
|-------|-----------|----------------------|
| 1 | SpinalCord.dispatch() | Entry point for all sensory |
| 2 | Brainstem.dispatch() | RelayBundle → Thalamus (Loop A/B/C) |
| 3 | Thalamus.dispatch() | Central hub for A/B/C/E |
| 4 | Hypothalamus.dispatch() | Loop D start |
| 5 | BG/Limbic | Loops B/D integration |
| 6 | Cerebellum (new) | Loop C |
| 7 | Cortex | Full loop closure |

### Step 4: Loop Demos (Integration Tests)

| Demo | Tests | Components Used |
|------|-------|-----------------|
| `loop-zero` | Concurrency proof | Cortex + Thalamus + TRN (MQTT) |
| `reflex-arc` | Spinal reflexes work | SpinalCord only |
| `relay-test` | Raw → RelayBundle → Route | Spinal + Brainstem + Thalamus |
| `loop-d-simple` | Homeostatic regulation | Hypothalamus + Brainstem |
| `loop-b-simple` | Action selection | BG + Thalamus |
| `loop-a-full` | Full routing + gating | All cortical components |

---

## Why Not Pure "Loops First"

| Issue | Why It Breaks |
|-------|---------------|
| All methods are `...` | Loops would wire nothing to nothing |
| Type duplication | Different ScopeLevel enums won't match |
| No test infrastructure | Can't verify concurrent behavior |
| Undefined scope | "Build Loop A" = implement 30+ Thalamus methods |

## Why Not Pure "Bottom-Up"

| Issue | Risk |
|-------|------|
| No integration target | Build components that don't fit together |
| Lose loop awareness | Forget what components are FOR |
| Over-engineer | Add features no loop needs |

## The Right Balance

1. **Prove concurrency first** (Loop Zero with MQTT)
2. **Know the loops** (contracts, interfaces, what they need)
3. **Build foundation** (fix issues, implement dispatch())
4. **Test with loops** (each phase validates a loop segment)
5. **Grow together** (all components elaborate concurrently)

---

## Immediate Next Steps

### Phase 0: Loop Zero (Prove Concurrency)

1. **Install/configure Mosquitto** (if not already running)
2. **Create `demos/loop_zero/` directory**
3. **Create minimal MQTT-based contracts** (`loop_zero_contracts.py`):
   - Reuse existing `ThalamicEnvelope`, `GateState`, `RouteDecision` from thalamus_async.py
   - Add MQTT serialization (JSON or msgpack)
4. **Create 3 process scripts**:
   - `loop_zero_cortex.py` - L4 receives from thalamus, L5 sends to thalamus
   - `loop_zero_thalamus.py` - Relays to cortex, checks TRN gate
   - `loop_zero_trn.py` - Publishes GateState on Lane G
5. **Create runner script** (`run_loop_zero.sh`)
6. **Verify concurrency** with success criteria above

### Phase 1: Fix Blocking Issues (After Loop Zero Works)

1. Fix type duplication (consolidate ScopeLevel to shared/)
2. Add BasePlaneFacade to BG, Limbic, Hypothalamus
3. Fix RelayBundle.channel → target_nucleus
4. Implement SpinalCord.dispatch() with reflex logic
5. Create second demo: `reflex-arc`

---

## Verification

### How to Test Loop Zero

```bash
# 1. Start Mosquitto broker
mosquitto -v

# 2. In separate terminals, start each process
python demos/loop_zero/loop_zero_cortex.py
python demos/loop_zero/loop_zero_thalamus.py
python demos/loop_zero/loop_zero_trn.py

# 3. Verify:
# - Each terminal shows its own PID
# - Messages flow: Cortex publishes → Thalamus relays → Cortex receives
# - When TRN publishes BURST mode, Thalamus blocks messages
# - All processes continue running independently (no blocking)
```

### Success Indicators

- [x] 3 separate PIDs visible in `ps aux | grep loop_zero`
- [x] 3 separate CPUs (verified: CPU 10, 3, 31)
- [x] Messages flowing (L5 SENT, GATE published)
- [x] Non-blocking (all processes log independently)
- [ ] TRN can block messages (BURST mode) - not yet tested
- [ ] System keeps running if one process dies - not yet tested

---

## Design Note: Dual-Mode Communication (TONIC vs BURST)

**Date:** 2026-01-11
**Source:** neuro-expert consultation, Cho et al. 2025, Sherman 2016

### Critical Finding

Thalamic relay operates in TWO modes with DIFFERENT communication patterns:

| Mode | When Active | TRN Behavior | Communication Pattern |
|------|-------------|--------------|----------------------|
| TONIC | Alert, sustained attention | Graded inhibition | Publish-on-change, rate-coded, near-continuous |
| BURST | Sleep, drowsy, attention shifts | Oscillatory (7-14 Hz) | Rhythmic packets, discrete windows (~100ms on/off) |

### Why This Matters

- Current Loop Zero has `TRNMode.TONIC | BURST` but treats them identically
- Future implementation MUST make them behave differently
- This is NOT optional - it's how the brain actually works

### Implementation Pattern

```python
if operating_mode == TRNMode.TONIC:
    # Graded, proportional relay
    # Messages flow based on sector gate level (0.0 to 1.0)
    # Publish-on-change with rate coding
    # Linear input-output relationship

elif operating_mode == TRNMode.BURST:
    # Rhythmic gating
    # Messages only pass during "open" phase of burst cycle
    # Packet delivery with discrete windows (~100ms on/off)
    # Non-linear, salience detection mode
```

### Scientific Basis

| Brain Mechanism | Mode | Software Equivalent |
|-----------------|------|---------------------|
| T-type calcium channel bursts | BURST | Windowed message delivery |
| Graded membrane potential | TONIC | Rate-coded message frequency |
| TRN oscillatory inhibition | BURST | Periodic gate close/open |
| TRN tonic inhibition | TONIC | Continuous gate level (0.0-1.0) |

This finding is documented in CLAUDE.md Core Principle 11.
