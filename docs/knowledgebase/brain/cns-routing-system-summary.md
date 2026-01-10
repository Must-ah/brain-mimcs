# CNS Message Routing System: Summary

## A Brain-Inspired Software Architecture for Signal Routing

This document summarizes the conceptual model for a message routing system based on the human central nervous system. The system implements structural routing where signal type determines pathway, anatomical hierarchy where all signals traverse proper levels, and timing fidelity where delays emerge from physical properties rather than arbitrary scheduling.

---

# Part 1: The Core Principle

## Structural Routing

The brain does not route messages the way computer networks do. There is no packet switching, no routing tables consulted at runtime, no dynamic path discovery. Instead, the brain uses structural routing — the physical anatomy of the connection determines where a signal can go.

A pain signal takes the spinothalamic tract not because some router decided that's the best path, but because pain-sensitive neurons in the dorsal horn are physically wired to project their axons into that tract and no other. The neuron that generates the signal is pre-wired to a specific pathway. There is no decision point. The pain receptor cannot suddenly decide to send its signal up the dorsal columns instead — it's not connected to that pathway.

This is the foundational principle: **signal type determines anatomy, and anatomy determines route.**

## The Communication Hierarchy

All signals must traverse the anatomical hierarchy. There are no shortcuts, no direct connections that bypass levels.

**Ascending (sensory, toward brain):**

```
Peripheral Receptor
       ↓
   Spinal Cord
       ↓
    Brainstem
       ↓
     Thalamus
       ↓
      Cortex
```

Every sensory signal (except olfaction) must pass through each level. A signal cannot jump from spinal cord directly to cortex. It must traverse the brainstem. It must relay through thalamus.

**Descending (motor, toward body):**

```
      Cortex
       ↓
    Brainstem
       ↓
   Spinal Cord
       ↓
Peripheral Effector
```

A motor command from motor cortex cannot directly reach a muscle. It must descend through the proper hierarchy.

**Local Processing (reflexes):**

The one exception to the "must go all the way up" rule is the spinal reflex. When time-critical processing is needed, the spinal cord can generate a response locally without involving the brain. However, the sensory signal typically ALSO continues ascending in parallel. You pull your hand from the flame before you consciously feel pain, but you do eventually feel the pain because the signal continued up to cortex while the reflex was executing.

---

# Part 2: How Signals Connect to Routes

## The Connection Mechanism

In the brain, a signal doesn't "discover" or "choose" its route. The route is determined the moment the signal is born, because the neuron that generates the signal is physically wired to a specific pathway.

A nociceptor (pain receptor neuron) in your foot has an axon that enters the spinal cord and synapses on second-order neurons in the dorsal horn. Those second-order neurons send their axons across the midline and into the spinothalamic tract. There is no decision point. The anatomy permits no other option.

## Route Binding Through Signal Type

The signal's type determines which neurons are activated, and those neurons are pre-wired to specific highways. When a signal is created, it carries its type. The type is intrinsic — a pain receptor can only create pain signals, just as a touch receptor can only create touch signals.

The type binds to a route through a fixed lookup. This lookup represents the anatomical wiring:

```
ROUTE_BINDINGS = {
    "pain_fast":                  ["lateral_spinothalamic"],
    "pain_slow":                  ["lateral_spinothalamic"],
    "fine_touch":                 ["dorsal_column_medial_lemniscus"],
    "proprioception_conscious":   ["dorsal_column_medial_lemniscus"],
    "proprioception_unconscious": ["dorsal_spinocerebellar", "ventral_spinocerebellar"],
    "motor_voluntary":            ["lateral_corticospinal", "anterior_corticospinal"],
    ...
}
```

Some signal types bind to multiple pathways. Proprioception goes BOTH to cortex (conscious) AND cerebellum (unconscious) via different routes. This represents the anatomical reality that the same peripheral receptor activates multiple neuron populations projecting through different pathways.

## Station Traversal

Once bound to a pathway, the signal traverses each station in sequence. Each station is a processing node that performs operations on the signal:

**RELAY**: Pass signal forward with minimal transformation.

**TRANSFORM**: Change signal representation or encoding.

**MODULATE**: Adjust gain or priority without changing content.

**BRANCH**: Copy signal to multiple destinations.

**GATE**: Allow or block signal based on conditions.

**INTEGRATE**: Combine multiple inputs into single output.

**TERMINATE**: Final destination where signal is consumed.

At each station, the signal's laterality may change (if the highway crosses at that level). The signal accumulates delay. The signal may be modulated based on system state. This process is entirely deterministic given the signal type and origin.

## Key Insight

The "connection" between a signal and its route is not a runtime decision. It's a structural fact established before any signal ever fires. The routing table is the anatomy itself. When you model this in software, you make the implicit explicit: you create a lookup table that maps signal types to pathways, and you represent pathways as ordered sequences of stations. But in the real brain, there IS no lookup — there's just neurons connected to other neurons, and activation propagating along those connections.

The structure IS the router.

---

# Part 3: How Priority Works

## Priority Is Not a Message Property

In a typical software message queue, priority works like this:

```
message = {
    payload: data,
    priority: HIGH
}

// Central dispatcher reads priority and acts accordingly
message = queue.pop_highest_priority()
```

The priority is metadata attached to the message. A central dispatcher reads that metadata and decides what to process first.

**The brain does not work this way.**

There is no central dispatcher reading priority tags. There is no queue where urgent messages cut in line. Instead, priority is embedded in the physical structure of the pathway itself.

## Priority Through Velocity

The most direct form of priority is conduction velocity. High-priority signals travel on fast highways. Low-priority signals travel on slow highways.

| Fiber Type | Diameter | Velocity | Typical Signals |
|------------|----------|----------|-----------------|
| Aα | 13-20 μm | 80-120 m/s | Proprioception, motor commands |
| Aβ | 6-12 μm | 35-75 m/s | Fine touch, pressure |
| Aδ | 1-5 μm | 5-35 m/s | Fast pain, cold temperature |
| C | 0.2-1.5 μm | 0.5-2 m/s | Slow pain, warm temperature, itch |

Consider two pain signals from the same injury. Fast pain (Aδ fibers) is sharp, localized, and immediate — it travels at 15-35 m/s as the "warning" signal. Slow pain (C fibers) is dull, diffuse, and persistent — it travels at 0.5-2 m/s as the "damage assessment" signal.

Both signals originate from the same injury at the same instant. But fast pain arrives at the brain 500-1000 ms before slow pain. The fast signal wins the race not because it had a priority tag, but because it traveled on a faster highway.

This is structural priority. The receptor that fires determines the fiber type. The fiber type determines the velocity. The velocity determines arrival time. No dispatcher needed.

## Priority Through Architecture

Some signals get priority through shorter, more direct pathways.

The hyperdirect pathway in the basal ganglia (cortex → STN → GPi) is faster than the direct pathway (cortex → striatum → GPi) because it has fewer synapses. When you need to suddenly stop an action, the hyperdirect pathway wins because it's architecturally shorter.

The reflex arc gives protective responses priority by keeping them entirely local. A pain signal that triggers withdrawal doesn't wait for the brain to process it. The reflex completes in 40 ms while the signal is still traveling toward conscious perception. The local path is structurally prioritized over the long path.

## Priority Through Dedicated Hardware

The brain dedicates its most expensive hardware — thick, heavily myelinated axons — to its highest-priority signals.

Proprioception from muscle spindles travels on Aα fibers (80-120 m/s). These are the fattest, most heavily myelinated axons in the body. Why? Because knowing where your limbs are RIGHT NOW is critical for motor control. A 100 ms delay in proprioception would make coordinated movement impossible.

By contrast, itch travels on thin, unmyelinated C fibers (0.5-2 m/s). Itch is not time-critical. The brain doesn't waste expensive myelinated axons on it.

## Concrete Example: Same Event, Multiple Priorities

You step on a nail. At the instant of tissue damage, multiple receptor types fire simultaneously:

| Signal Type | Fiber | Velocity | Time to Brain (1m) |
|-------------|-------|----------|-------------------|
| Proprioception | Aα | 100 m/s | 10 ms |
| Pressure | Aβ | 50 m/s | 20 ms |
| Fast pain | Aδ | 20 m/s | 50 ms |
| Slow pain | C | 1 m/s | 1000 ms |

The proprioceptive signal arrives 990 ms before the slow pain signal. The brain gets almost a full second of lead time to know something is wrong with foot position before the full pain hits. The priority ordering is not determined by any tag on the messages — it's determined by which highways those signals were born onto.

## What About Modulation?

Attention and arousal affect priority, but not by reordering a queue. Modulation affects gain, not sequence.

When you attend to something, the thalamic reticular nucleus adjusts which thalamic channels are open. Attended signals get through with full strength. Unattended signals are attenuated. This is like adjusting the volume knob on different channels, not like reordering a queue. An unattended signal still arrives when it arrives — it's just quieter.

When you're highly aroused, the locus coeruleus releases norepinephrine throughout the brain, increasing gain on sensory processing globally. But this doesn't change when signals arrive. A slow pain signal is still slow. Arousal just makes the system more responsive when that signal finally arrives.

## Key Insight

Priority is not a tag that a dispatcher reads. Priority is the physics of the pathway — how fast signals propagate, how many synapses they cross, how long the path is. In the model, priority emerges from highway properties (velocity, length, synapse count), not from message metadata.

---

# Part 4: How Time Works

## The Brain Has No Clock

The brain does not have a central clock. There is no master oscillator ticking away, no global timestamp being distributed to all neurons, no synchronized frame rate.

Each neuron is an independent processor operating on its own local time. When input arrives, the neuron processes it. When threshold is reached, the neuron fires. The neuron doesn't know or care what "time" it is globally. It just responds to input.

What we perceive as "time" in the brain emerges from physical delays:

**Propagation delays**: Signals take time to travel along axons. A signal from your foot takes longer to reach your brain than a signal from your neck, simply because the foot is farther away.

**Synaptic delays**: Each synapse introduces a delay of 0.5-5 ms for neurotransmitter release, diffusion, and receptor binding.

**Processing delays**: Complex computations at stations take time — integration of multiple inputs, threshold detection, pattern completion.

**Causal ordering**: Event A causes Event B, and B cannot happen before A completes. This creates a partial ordering of events even without a global clock.

The brain's "time" is not a ticking clock. It's the accumulation of physical delays as signals propagate through the system.

## Three Sources of Delay

**Transit Delay (Highway Property)**

This is the time for a signal to propagate along an axon bundle. It depends on the highway's length and conduction velocity.

```
transit_time = length / velocity
```

For the spinothalamic tract (spinal cord to thalamus):
- Length: ~0.3 m
- Velocity: ~20 m/s (Aδ fibers)
- Transit time: 15 ms

**Synaptic Delay (Connection Property)**

This is the time for signal transmission across a synapse. It occurs at every station where a synapse exists.

- Fast chemical synapses (glutamate, GABA): 0.5-1 ms
- Slow chemical synapses (modulatory): 1-5 ms
- Electrical synapses (gap junctions): <0.1 ms
- Neuromuscular junction: 0.5-1 ms

**Processing Delay (Station Property)**

This is additional time for computation at the station.

- Simple relay: 0-1 ms
- Integration station: 2-5 ms
- Complex processing (cortex): 10-30 ms

**Total Delay Calculation**

When a signal traverses from Station A to Station B via Highway H:

```
total_delay = A.processing_delay + A.synaptic_delay + H.transit_time
arrival_time = current_time + total_delay
```

## Discrete Event Simulation

To model time without a central clock, we use discrete event simulation. Instead of advancing time continuously by fixed intervals, we advance time by jumping from event to event.

**The Event Queue**

The central data structure is a priority queue ordered by time. Each entry is an event scheduled for a specific future time.

```
EventQueue:
    events: PriorityQueue ordered by delivery_time (ascending)
    
    schedule(delivery_time, signal, destination_station):
        events.push({time: delivery_time, signal: signal, destination: destination_station})
    
    pop_next():
        return events.pop()  // Returns event with earliest time
```

**The Simulation Clock**

The simulation maintains a current time that jumps forward to match each event as we process it.

```
Simulation:
    current_time: float = 0
    event_queue: EventQueue
    
    run():
        while event_queue.not_empty():
            event = event_queue.pop_next()
            current_time = event.time  // Time jumps to this event
            event.destination.receive(event.signal, current_time)
```

When we process an event at t=56 ms and the next event is at t=85 ms, we don't simulate what happens at t=57, t=58, t=59... We jump directly from 56 to 85. Nothing was scheduled in between, so nothing happens in between.

**Scheduling New Events**

When a station processes a signal, it generates new events — output signals that will arrive at downstream stations in the future. The station calculates when those signals will arrive and schedules them.

```
Station:
    process(signal, current_time):
        processed_signal = self.transform(signal)
        
        for connection in self.output_connections:
            transit_time = connection.length / connection.velocity
            arrival_time = current_time + self.processing_delay + transit_time
            
            event_queue.schedule(arrival_time, processed_signal, connection.target_station)
```

The station doesn't "send" the signal immediately. It calculates when the signal will arrive at the next station and schedules an event for that future time.

## Parallel Signals

Multiple signals can be in flight simultaneously. The event queue processes them in chronological order based on when each is scheduled to arrive.

Imagine two signals originating at t=0:
- Signal A from hand (pain, Aδ fiber, 20 m/s, 0.7 m to spinal cord)
- Signal B from foot (touch, Aβ fiber, 50 m/s, 1.0 m to spinal cord)

Schedule their first arrivals:
- Signal A arrives at dorsal horn: t = 0.7/20 = 35 ms
- Signal B arrives at dorsal horn: t = 1.0/50 = 20 ms

The event queue contains:
```
[t=20ms: Signal B arrives at lumbar dorsal horn]
[t=35ms: Signal A arrives at cervical dorsal horn]
```

We process events in chronological order. Both signals are "in flight" simultaneously. The touch signal from the foot arrives before the pain signal from the hand, even though the hand is closer, because touch fibers are faster than pain fibers.

## Reflexes vs Conscious Perception

Let's trace the withdrawal reflex versus conscious perception for a painful stimulus to the foot.

**t=0 ms**: Nociceptor in foot fires.

**Ascending pathway:**
- Peripheral nerve to dorsal horn: 1.0 m / 20 m/s = 50 ms → arrives t=50 ms
- Dorsal horn processing: 5 ms → ready at t=55 ms
- Spinothalamic to thalamus: 0.6 m / 20 m/s = 30 ms → arrives t=85 ms
- Thalamus processing: 5 ms → ready at t=90 ms
- Thalamocortical: 0.05 m / 30 m/s = 1.7 ms → arrives t=92 ms
- Cortical processing: 30 ms → conscious perception at t=122 ms

**Reflex pathway:**
- Peripheral nerve to dorsal horn: same → arrives t=50 ms
- Dorsal horn reflex circuit: 10 ms → ready at t=60 ms
- Motor neurons to muscle: 1.0 m / 100 m/s = 10 ms → arrives t=70 ms
- Neuromuscular junction: 2 ms → muscle activation at t=72 ms

**Event sequence:**
```
t=50ms:  Signal arrives at dorsal horn → Schedule ascending (t=85ms) and reflex (t=60ms)
t=60ms:  Reflex signal ready → Schedule motor neuron activation (t=70ms)
t=70ms:  Signal arrives at motor neurons → Schedule muscle activation (t=72ms)
t=72ms:  FOOT WITHDRAWS
t=85ms:  Ascending signal arrives at thalamus → Schedule cortical arrival (t=92ms)
t=92ms:  Signal arrives at cortex → Schedule conscious perception (t=122ms)
t=122ms: CONSCIOUS PERCEPTION OF PAIN
```

You withdraw your foot at t=72 ms. You feel the pain at t=122 ms. The 50 ms gap between action and awareness emerges from the structural difference between the short local reflex path and the long ascending path to cortex.

## What Time Is NOT

**Time is not a global tick.** We do not step forward by fixed increments. We jump from event to event.

**Time is not attached to messages.** Signals do not carry a "timestamp" that determines when they're processed. Arrival time is calculated from physical properties when the signal is sent.

**Time is not managed centrally.** No coordinator is "running" time. Each station schedules its own downstream events. Time emerges from the accumulation of these scheduled events.

**Time is not synchronized.** Different signals are at different points in their journeys simultaneously. A fast signal from far away can overtake a slow signal from nearby.

## Key Insight

The brain's time emerges from physical delays — conduction velocity, synaptic transmission, processing duration. The model's time is simulated through discrete event simulation where an event queue holds scheduled signal arrivals ordered by time. Timing differences between pathways (fast vs. slow fibers, short vs. long routes) produce priority effects automatically because faster pathways produce earlier scheduled arrivals.

---

# Part 5: System Components

## Signal

A signal carries properties that determine its routing fate:

| Property | Description | Examples |
|----------|-------------|----------|
| type | The kind of information; determines which highway | pain_fast, fine_touch, motor_voluntary |
| origin | Where the signal originated | L5_dermatome, M1_hand_area |
| laterality | Left or right side | left, right |
| intensity | Signal strength (0.0 to 1.0) | Affects thresholds, reflex triggering |
| timestamp | When signal was generated | Used for timing calculations |
| payload | The actual data content | Application-specific |

## Station

A station is an independent processor. It receives signals, performs operations, and schedules output. Each station has:

- **name**: Anatomical identifier
- **location**: CNS division and level
- **operations**: Map of signal_type → operation(s) performed
- **synaptic_delay**: Time for neurotransmitter transmission
- **processing_delay**: Time for computation
- **connections_in**: Which highways arrive here
- **connections_out**: Which highways depart from here

Stations know nothing about the global system. They just respond to input and schedule output.

## Highway

A highway connects stations. Each has:

| Property | Description |
|----------|-------------|
| name | Anatomical tract name |
| origin_station | Where the highway begins |
| destination_station | Where the highway ends |
| fiber_type | Aα, Aβ, Aδ, B, or C |
| velocity | Conduction velocity in m/s |
| length | Physical length in meters |
| crossing | Where decussation occurs (if any) |
| signal_types | Which signal types use this highway |

Transit time = length / velocity

## Reflex Arc

A reflex arc is a local circuit that generates motor output without brain involvement:

| Property | Description |
|----------|-------------|
| trigger_type | Signal type that triggers this reflex |
| threshold | Minimum intensity to trigger |
| circuit_type | Monosynaptic or polysynaptic |
| latency | Time from input to output |
| motor_pattern | Which muscles activated/inhibited |
| ascending_continues | Whether signal continues to brain (usually true) |

Reflexes run in parallel with ascending transmission — they don't consume the signal.

---

# Part 6: Comparison with Traditional Software

| Traditional Software | This Model (Brain-Like) |
|---------------------|------------------------|
| Central router dispatches messages | No central router — topology IS routing |
| Priority is message metadata | Priority is highway velocity |
| Time advances by fixed tick | Time emerges from event scheduling |
| Sequential processing loop | Parallel, event-driven, distributed |
| One message processed at a time | Millions of signals in flight simultaneously |
| Router consults routing table | Signal type determines route at birth |
| Priority queue reorders messages | Arrival order determined by physics |
| Global clock synchronizes processing | No global clock — stations respond to input |

---

# Part 7: Implementation Architecture

## Event-Driven Model

```
// Each station is an independent processor
Station:
    inputs: Queue
    outputs: List[Connection]
    
    on_input_received(signal, current_time):
        processed = this.process(signal)
        
        for connection in this.outputs:
            arrival_time = current_time + this.delay + connection.transit_time
            event_queue.schedule(arrival_time, processed, connection.target)

// Connections have real propagation delays
Connection:
    source: Station
    target: Station
    velocity: float  // m/s
    length: float    // meters
    
    transit_time = length / velocity

// Global event queue ordered by time
EventQueue:
    events: PriorityQueue[time, event]
    
    schedule(delivery_time, signal, destination):
        events.push(delivery_time, {signal, destination})
    
    run():
        while events.not_empty():
            time, event = events.pop()
            current_time = time
            event.destination.on_input_received(event.signal, current_time)
```

## Key Properties

**No central loop controlling stations**: Each station just responds to input.

**Multiple signals propagate simultaneously**: The event queue handles them all.

**Timing emerges from actual delays**: Propagation time is length / velocity.

**Parallel pathways work correctly**: Pain and touch signals travel independently.

**No central router**: The routing is the topology. Once wired, signals flow automatically.

---

# Part 8: Integration Points

The spinal cord and brainstem routing connects to higher structures at defined interface points.

## Ascending Integration (To Higher Structures)

| Thalamic Nucleus | Receives From | Projects To | Signal Types |
|------------------|---------------|-------------|--------------|
| VPL | Medial lemniscus, Spinothalamic | S1 (body) | Touch, pain, temperature, proprioception |
| VPM | Trigeminal lemniscus | S1 (face) | Face sensation |
| MGN | Inferior colliculus | A1 | Auditory |
| LGN | Optic tract | V1 | Visual |
| VL | Cerebellum, Basal ganglia | Motor cortex | Motor coordination |

## Descending Integration (From Higher Structures)

| Structure | Entry Point | Highway |
|-----------|-------------|---------|
| Motor cortex Layer V | Corona radiata | Corticospinal, Corticobulbar |
| Cerebellar output | Superior cerebellar peduncle | Via red nucleus and thalamus |
| Basal ganglia output | Via thalamus | Influences motor cortex |

## Interface Contract

Each integration point defines:
- What signal types it accepts
- What transformations occur at the boundary
- What the signal's next station is after crossing the boundary
- How laterality is handled at the boundary

---

# Part 9: What This Model Captures

**Structural routing**: Signal type determines pathway. A pain signal takes the spinothalamic tract because that's how pain neurons are wired.

**Anatomical fidelity**: Every highway and station corresponds to real anatomical structures.

**Mandatory hierarchy**: All signals traverse spinal cord → brainstem → thalamus → cortex. No shortcuts.

**Crossing logic**: Different pathways cross at different levels, explicitly tracked.

**Local processing**: Reflex arcs handle time-critical responses locally while signals continue ascending in parallel.

**Timing fidelity**: Conduction velocities range from 0.5 m/s to 120 m/s. Synaptic delays add 0.5-5 ms per synapse.

**Parallel pathways**: Same information can travel multiple routes simultaneously.

**Collateral branching**: Single pathways can branch to send copies to multiple destinations.

**Priority through structure**: Fast fibers and short paths win, not priority tags.

**Emergent time**: No central clock — timing emerges from physical delays and event scheduling.

---

# Part 10: Implementation Roadmap

**Phase 1 (Complete)**: Conceptual model with all spinal cord and brainstem routes specified. Integration points defined.

**Phase 2**: Add cerebrum routes (cortical, subcortical, basal ganglia loops) connecting at defined thalamic and cortical interface points.

**Phase 3**: Add cerebellum routes (peduncle inputs, cerebellar cortex processing, deep nuclei outputs) connecting at defined peduncle and thalamic interface points.

**Phase 4**: Integrate all three systems into unified routing substrate where any signal can be traced from origin to destination through the complete CNS hierarchy.

---

# Appendix: Timing Reference

## Conduction Velocity by Fiber Type

| Fiber | Diameter | Velocity | Signal Types |
|-------|----------|----------|--------------|
| Aα | 13-20 μm | 80-120 m/s | Proprioception, motor |
| Aβ | 6-12 μm | 35-75 m/s | Touch, pressure |
| Aδ | 1-5 μm | 5-35 m/s | Fast pain, cold |
| B | 1-3 μm | 3-15 m/s | Autonomic preganglionic |
| C | 0.2-1.5 μm | 0.5-2 m/s | Slow pain, warm, itch |

## Total Transit Time Examples

| Signal | Route | Distance | Velocity | Synapses | Total Time |
|--------|-------|----------|----------|----------|------------|
| Fine touch (hand) | DCML | 0.8 m | 60 m/s | 3 | ~25 ms |
| Fine touch (foot) | DCML | 1.5 m | 60 m/s | 3 | ~40 ms |
| Fast pain (hand) | Spinothalamic | 0.8 m | 15 m/s | 3 | ~70 ms |
| Fast pain (foot) | Spinothalamic | 1.5 m | 15 m/s | 3 | ~120 ms |
| Slow pain (foot) | Spinothalamic | 1.5 m | 1 m/s | 3 | ~1520 ms |
| Motor command (hand) | Corticospinal | 0.8 m | 100 m/s | 2 | ~15 ms |
| Withdrawal reflex | Local | 0.1 m | 15 m/s | 4 | ~40 ms |

---

*Document Version 1.0*
*Companion to: cns-routing-system-model.md (complete route specifications)*
