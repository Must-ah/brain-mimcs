# Loop Zero: Concurrent Proof-of-Concept

## Purpose

Loop Zero proves that the brain-mimc architecture can run with **true concurrency** - each component on a separate process/core, communicating without blocking.

This is the foundational demo that validates our core principle: **"No sequential pipelines. No blocking calls. No orchestrator."**

## What Loop Zero Proves

| Criterion | Description |
|-----------|-------------|
| **Separate processes** | Cortex, Thalamus, and TRN run as distinct OS processes (different PIDs) |
| **No shared memory** | Processes cannot access each other's variables - communication only via MQTT |
| **Non-blocking** | Each process continues its work without waiting for responses |
| **Message flow** | Cortex -> Thalamus -> Cortex round-trip completes via pub-sub |
| **TRN gating** | TRN can inhibit (block) messages from reaching Cortex |

## Architecture

```
┌──────────────────┐     MQTT      ┌──────────────────┐     MQTT      ┌──────────────────┐
│   Process 1      │◄────────────►│   Process 2      │◄────────────►│   Process 3      │
│   CORTEX         │               │   THALAMUS       │               │   TRN (Gate)     │
│                  │               │                  │               │                  │
│   - L4: receive  │               │   - Relay msgs   │               │   - Publish      │
│   - L5: send     │               │   - Check gate   │               │     GateState    │
│                  │               │   - Route by     │               │   - TONIC/BURST  │
│                  │               │     nucleus      │               │     modes        │
└──────────────────┘               └──────────────────┘               └──────────────────┘
     PID: 1001                          PID: 1002                          PID: 1003
```

## Brain-Faithfulness

This demo mirrors how the real brain works:

| Aspect | Brain | Loop Zero |
|--------|-------|-----------|
| Separation | Brain regions are anatomically separate structures | Separate OS processes |
| Communication | Axons transmit signals asynchronously | MQTT pub-sub |
| No orchestrator | Brain has no central "main loop" | Each process runs independently |
| TRN gating | TRN inhibits thalamic relay nuclei | TRN process publishes GateState that Thalamus respects |
| Layers | Cortex L4 receives, L5 sends | Cortex process has L4 (subscriber) and L5 (publisher) |

## MQTT Topics

### Lane A (Driver - Ascending)
- `/A/driver/{scope_level}/{scope}/nucleus/{nucleus_id}` - Sensory input to thalamus

### Lane B (Modulator - Descending)
- `/B/modulator/{scope_level}/{scope}/cortex/{area}/layer/{layer}` - Cortex L6 feedback

### Lane G (Gate - Control Plane)
- `/G/gate/{scope_level}/{scope}/sector/{sector}` - TRN gating state

### Lane internal
- `/thalamus/relay/{scope_level}/{scope}/cortex/{area}/layer/{layer}` - Thalamus to Cortex

## Contracts Used

### ThalamicEnvelope (Driver signal)
```python
@dataclass(frozen=True)
class ThalamicEnvelope:
    kind: SignalKind           # DRIVER or MODULATOR
    nucleus: NucleusId         # Target nucleus (LGN, MGN, VPL, etc.)
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    payload: dict
```

### GateState (TRN control)
```python
@dataclass(frozen=True)
class GateState:
    scope: str
    scope_level: ScopeLevel
    sector: TRNSector          # VISUAL, AUDITORY, SOMATOSENSORY, MOTOR, LIMBIC
    gpe_inhibition: float      # 0..1 (global gain from BG)
    intra_trn_inhibition: float # 0..1 (local focus)
    mode: TRNMode              # TONIC (relay) or BURST (block)
    timestamp_ms: int
```

## How Each Process Works

### loop_zero_cortex.py
1. **L4 (Receive)**: Subscribes to `/thalamus/relay/...`
2. **L5 (Send)**: Publishes driver signals to `/A/driver/...`
3. **Main loop**:
   - Generates mock sensory events periodically
   - Logs received relay messages
   - Never blocks waiting for responses

### loop_zero_thalamus.py
1. **Subscribe**: Listens to `/A/driver/...` (incoming) and `/G/gate/...` (control)
2. **Gating check**: Before relaying, checks current GateState for the sector
3. **Relay**: If gate is TONIC (open), publishes to `/thalamus/relay/...`
4. **Block**: If gate is BURST (closed), logs but does not relay

### loop_zero_trn.py
1. **Control**: Periodically publishes GateState to `/G/gate/...`
2. **Oscillate**: Alternates between TONIC and BURST modes
3. **Per-sector**: Can control different sectors independently (VISUAL vs MOTOR)

## Running the Demo

### Prerequisites
- Mosquitto MQTT broker
- Python 3.11+
- paho-mqtt (`pip install paho-mqtt`)

### Start

```bash
# Terminal 1: Start Mosquitto broker
mosquitto -v

# Terminal 2: Start Cortex process
python demos/loop_zero/loop_zero_cortex.py

# Terminal 3: Start Thalamus process
python demos/loop_zero/loop_zero_thalamus.py

# Terminal 4: Start TRN process
python demos/loop_zero/loop_zero_trn.py
```

Or use the runner script:
```bash
./demos/loop_zero/run_loop_zero.sh
```

### Verify Concurrency

```bash
# Check all 3 processes are running with separate PIDs
ps aux | grep loop_zero

# Expected: 3 distinct PIDs
```

## Success Criteria Checklist

- [ ] 3 separate PIDs visible in `ps aux | grep loop_zero`
- [ ] Cortex receives messages from Thalamus (check Cortex logs)
- [ ] TRN can block messages (when BURST mode, Thalamus logs "blocked")
- [ ] Timestamps show concurrent activity (no sequential wait patterns)
- [ ] System keeps running if one process dies (others continue)

## Why MQTT (Not InMemoryTopicBus)

| Requirement | InMemoryTopicBus | MQTT |
|-------------|------------------|------|
| Cross-process | NO (single Python process) | YES |
| Cross-machine | NO | YES |
| Proves non-blocking | NO (could be same thread) | YES |
| Production-ready | NO (testing only) | YES |

## Next Steps After Loop Zero

Once this demo works, we know our architecture is sound for true concurrency. Then:

1. **Fix blocking issues** (type duplication, missing BasePlaneFacade)
2. **Build out foundation** (SpinalCord, Brainstem dispatch)
3. **Add more loops** (B with BG, C with Cerebellum, D with Hypothalamus, E with Hippocampus)
4. **Scale test** (run on multiple machines)

## Future Work: Dual-Mode Communication

**Current limitation:** Loop Zero treats `TRNMode.TONIC` and `TRNMode.BURST` identically.

**Required enhancement:** These modes MUST behave differently (see CLAUDE.md Core Principle 11):

| Mode | Current Behavior | Required Behavior |
|------|------------------|-------------------|
| TONIC | Same as BURST | Graded relay, publish-on-change, rate-coded |
| BURST | Binary block/pass | Rhythmic packets, ~100ms windows, 7-14 Hz oscillation |

**Implementation notes:**
- TONIC = high-fidelity relay (awake, sustained attention)
- BURST = salience detection (sleep, drowsy, attention shifts)
- Both use discrete messages, but temporal patterns differ

**Source:** Cho et al. 2025, Sherman 2016
