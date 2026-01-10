# Brain Communication Software Architecture

This document translates the brain's communication framework into software architecture patterns. It defines how to implement components, ports, and connections using the communication types identified in the conceptual framework.

This document supplements:
- **brain-communication-framework.md** — Conceptual categories (communication types, architectures, structural roles)
- **brain-communication-systems-overview.md** — Detailed descriptions of all 14 communication systems

---

## Overview: From Brain to Software

The brain's communication architecture maps to software concepts as follows:

| Brain Concept | Software Concept | What It Defines |
|---------------|------------------|-----------------|
| Structure (spinal cord, brainstem, etc.) | Component | A module with defined interfaces |
| Structural Role | Component Capability | What the component can do |
| Port | Interface | What can connect to the component |
| Communication Type | Connection Protocol | How information flows between components |
| Architecture (topology) | Connection Pattern | The shape of connections |

The key insight is that **communication types do not live in components**. They live in the **connections between components**. Components expose ports; connections define how information flows through those ports.

---

## Core Abstractions

Before implementing specific brain structures, we need to define the core abstractions that all components and connections will use.

### Signal: The Basic Unit of Communication

All communication in the brain involves signals. A signal carries information from one place to another.

```python
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Any, Optional
from datetime import datetime
from enum import Enum, auto

# Generic type for signal payloads
T = TypeVar('T')

@dataclass
class Signal(Generic[T]):
    """
    The basic unit of communication between components.
    
    Every signal has:
    - payload: The actual information being transmitted
    - timestamp: When the signal was generated
    - source: Where the signal came from
    - priority: How urgent the signal is (for routing decisions)
    """
    payload: T
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    priority: int = 0  # Higher = more urgent
    
    def __repr__(self):
        return f"Signal({self.payload}, from={self.source}, priority={self.priority})"
```

### Port: The Connection Interface

Ports define what can connect to a component. There are different types of ports for different connection patterns.

```python
from abc import ABC, abstractmethod
from typing import Callable, List, Set
import asyncio

class Port(ABC):
    """
    Base class for all ports.
    
    A port is a connection point on a component. It defines:
    - What type of signals it handles
    - Whether it sends, receives, or both
    - How it processes signals
    """
    def __init__(self, name: str, owner: str):
        self.name = name
        self.owner = owner  # The component that owns this port
        self.connected = False
    
    def __repr__(self):
        return f"{self.owner}.{self.name}"


class InputPort(Port, Generic[T]):
    """
    A port that receives signals.
    
    Used for:
    - Gateway entry points (sensory input)
    - Receiving broadcast signals
    - Receiving from upstream components in a pathway
    """
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self._handlers: List[Callable[[Signal[T]], None]] = []
    
    def on_receive(self, handler: Callable[[Signal[T]], None]):
        """Register a handler to be called when a signal is received."""
        self._handlers.append(handler)
    
    def receive(self, signal: Signal[T]):
        """
        Called when a signal arrives at this port.
        Invokes all registered handlers.
        """
        for handler in self._handlers:
            handler(signal)


class OutputPort(Port, Generic[T]):
    """
    A port that sends signals.
    
    Used for:
    - Gateway exit points (motor output)
    - Sending to downstream components
    - Broadcasting (when connected to multiple destinations)
    """
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self._destinations: List[InputPort[T]] = []
    
    def connect_to(self, destination: InputPort[T]):
        """Connect this output to an input port."""
        self._destinations.append(destination)
        self.connected = True
        destination.connected = True
    
    def send(self, signal: Signal[T]):
        """Send a signal to all connected destinations."""
        for dest in self._destinations:
            dest.receive(signal)


class RelayPort(Port, Generic[T]):
    """
    A port that receives signals and forwards them (possibly transformed).
    
    Used for:
    - Relay stations that pass signals through
    - Components that are "on the pathway" but not the final destination
    
    A relay port is essentially an InputPort + OutputPort with optional transformation.
    """
    def __init__(self, name: str, owner: str, 
                 transform: Optional[Callable[[Signal[T]], Signal[T]]] = None):
        super().__init__(name, owner)
        self._input = InputPort[T](f"{name}_in", owner)
        self._output = OutputPort[T](f"{name}_out", owner)
        self._transform = transform or (lambda x: x)  # Identity if no transform
        
        # Wire input to output with transformation
        self._input.on_receive(self._relay)
    
    def _relay(self, signal: Signal[T]):
        """Receive, transform, and forward."""
        transformed = self._transform(signal)
        self._output.send(transformed)
    
    def connect_from(self, source: OutputPort[T]):
        """Connect an upstream output to this relay's input."""
        source.connect_to(self._input)
    
    def connect_to(self, destination: InputPort[T]):
        """Connect this relay's output to a downstream input."""
        self._output.connect_to(destination)


class BidirectionalPort(Port, Generic[T]):
    """
    A port that both sends and receives.
    
    Used for:
    - Two-node exchanges (thalamocortical, amygdala-PFC)
    - Loop components that receive from one node and send to another
    
    Note: In the brain, bidirectional communication typically uses
    SEPARATE ascending and descending pathways, not a single channel.
    This port models that by having separate input and output sub-ports.
    """
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self.input = InputPort[T](f"{name}_in", owner)
        self.output = OutputPort[T](f"{name}_out", owner)
    
    def on_receive(self, handler: Callable[[Signal[T]], None]):
        """Register handler for incoming signals."""
        self.input.on_receive(handler)
    
    def send(self, signal: Signal[T]):
        """Send signal to connected components."""
        self.output.send(signal)


class ModulatorPort(Port, Generic[T]):
    """
    A port that sends modulatory signals affecting HOW other components process.
    
    Unlike regular signals that carry information, modulatory signals change
    the processing parameters of the receiver (gain, threshold, mode, etc.).
    
    Used for:
    - Neuromodulatory effects (dopamine on striatum, NE on cortex)
    - Sleep state control
    - Attention modulation
    """
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self._targets: List['ModulatableComponent'] = []
    
    def connect_to(self, target: 'ModulatableComponent'):
        """Connect to a component that can be modulated."""
        self._targets.append(target)
        self.connected = True
    
    def modulate(self, signal: Signal[T]):
        """Send modulatory signal to all targets."""
        for target in self._targets:
            target.receive_modulation(signal)
```

---

## Component Base Classes

Components are the building blocks of the system. Each component has ports and capabilities.

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass, field

class Component(ABC):
    """
    Base class for all brain-inspired components.
    
    A component represents a distinct processing unit (spinal cord, brainstem,
    thalamus, cortex, etc.). Each component:
    - Has a unique name
    - Exposes ports for connections
    - Has internal processing capabilities
    - Can be modulated by other components
    """
    def __init__(self, name: str):
        self.name = name
        self._ports: Dict[str, Port] = {}
        self._state: Dict[str, Any] = {}
        
    def add_port(self, port: Port):
        """Register a port on this component."""
        self._ports[port.name] = port
    
    def get_port(self, name: str) -> Port:
        """Get a port by name."""
        return self._ports[name]
    
    @property
    def ports(self) -> Dict[str, Port]:
        """All ports on this component."""
        return self._ports
    
    def __repr__(self):
        port_list = ", ".join(self._ports.keys())
        return f"{self.__class__.__name__}({self.name}, ports=[{port_list}])"


class ModulatableComponent(Component):
    """
    A component that can be modulated by neuromodulatory signals.
    
    Modulation changes HOW the component processes, not WHAT it processes.
    Examples:
    - Dopamine increases gain in striatum
    - Norepinephrine increases alertness in cortex
    - Acetylcholine shifts encoding vs retrieval mode in hippocampus
    """
    def __init__(self, name: str):
        super().__init__(name)
        self._modulation_state: Dict[str, float] = {
            'gain': 1.0,        # Multiplicative factor on signal strength
            'threshold': 0.5,   # Activation threshold
            'noise': 0.1,       # Processing noise level
        }
        self._modulation_handlers: List[Callable[[Signal], None]] = []
    
    def receive_modulation(self, signal: Signal):
        """
        Receive a modulatory signal that affects processing parameters.
        """
        for handler in self._modulation_handlers:
            handler(signal)
    
    def on_modulation(self, handler: Callable[[Signal], None]):
        """Register a handler for modulatory signals."""
        self._modulation_handlers.append(handler)
    
    @property
    def gain(self) -> float:
        return self._modulation_state['gain']
    
    @gain.setter
    def gain(self, value: float):
        self._modulation_state['gain'] = value


class LocalProcessor(Component):
    """
    A component that can process signals entirely locally.
    
    Used for components like the spinal cord that can execute reflexes
    without involving other CNS structures.
    """
    def __init__(self, name: str):
        super().__init__(name)
        self._local_circuits: Dict[str, Callable[[Signal], Signal]] = {}
    
    def add_local_circuit(self, name: str, 
                          process: Callable[[Signal], Signal]):
        """
        Add a local processing circuit.
        
        A local circuit takes an input signal and produces an output signal
        without needing to communicate with other components.
        """
        self._local_circuits[name] = process
    
    def process_locally(self, circuit_name: str, signal: Signal) -> Signal:
        """Execute a local processing circuit."""
        if circuit_name not in self._local_circuits:
            raise ValueError(f"Unknown circuit: {circuit_name}")
        return self._local_circuits[circuit_name](signal)
```

---

## Connection Types

Connections define how information flows between components. Each communication type has a corresponding connection class.

### One-Way Connection

Information flows in one direction only. Used for ascending (sensory) and descending (motor) pathways.

```python
class OneWayConnection(Generic[T]):
    """
    A one-way connection between components.
    
    Information flows from source to destination with no return path.
    
    Used for:
    - Sensory ascending pathways (System 1, 11)
    - Motor descending pathways (System 2, 9)
    
    Properties:
    - Unidirectional: source sends, destination receives
    - No response channel: fire and forget
    - Can be chained: A → B → C → D
    """
    def __init__(self, name: str, 
                 source: OutputPort[T], 
                 destination: InputPort[T]):
        self.name = name
        self.source = source
        self.destination = destination
        
        # Wire the connection
        source.connect_to(destination)
    
    def __repr__(self):
        return f"OneWay({self.source} → {self.destination})"


class Pathway:
    """
    A chain of one-way connections forming a complete pathway.
    
    Used for linear pathways like:
    - Sensory: receptor → spinal cord → brainstem → thalamus → cortex
    - Motor: cortex → brainstem → spinal cord → muscle
    """
    def __init__(self, name: str):
        self.name = name
        self.segments: List[OneWayConnection] = []
    
    def add_segment(self, connection: OneWayConnection):
        """Add a segment to the pathway."""
        self.segments.append(connection)
    
    def trace(self) -> List[str]:
        """Return the path as a list of component names."""
        if not self.segments:
            return []
        
        path = [str(self.segments[0].source)]
        for seg in self.segments:
            path.append(str(seg.destination))
        return path
    
    def __repr__(self):
        return f"Pathway({self.name}: {' → '.join(self.trace())})"
```

### Bidirectional Connection

Information flows both ways between two structures. Implemented as paired one-way connections.

```python
@dataclass
class BidirectionalConnection(Generic[T]):
    """
    A bidirectional connection between two components.
    
    Information flows both ways, but typically through SEPARATE channels
    (not a single bidirectional pipe). This matches brain anatomy where
    ascending and descending pathways are physically separate.
    
    Used for:
    - Thalamocortical loop (System 3)
    - Amygdala-PFC regulation (System 13)
    - Hippocampal-neocortical consolidation (System 14)
    
    Properties:
    - Two separate channels (ascending and descending)
    - Each channel can carry different signal types
    - Channels can have different properties (bandwidth, latency)
    """
    name: str
    node_a: str  # Name of first component
    node_b: str  # Name of second component
    
    # The two channels
    a_to_b: OneWayConnection = None
    b_to_a: OneWayConnection = None
    
    # Optional: ratio of traffic (brain has ~10:1 descending:ascending)
    a_to_b_weight: float = 1.0
    b_to_a_weight: float = 1.0
    
    def __repr__(self):
        return f"Bidirectional({self.node_a} ↔ {self.node_b})"


def create_bidirectional_connection(
    name: str,
    port_a: BidirectionalPort,
    port_b: BidirectionalPort
) -> BidirectionalConnection:
    """
    Create a bidirectional connection between two bidirectional ports.
    
    This creates two one-way connections:
    - A's output → B's input
    - B's output → A's input
    """
    a_to_b = OneWayConnection(
        name=f"{name}_a_to_b",
        source=port_a.output,
        destination=port_b.input
    )
    
    b_to_a = OneWayConnection(
        name=f"{name}_b_to_a",
        source=port_b.output,
        destination=port_a.input
    )
    
    return BidirectionalConnection(
        name=name,
        node_a=port_a.owner,
        node_b=port_b.owner,
        a_to_b=a_to_b,
        b_to_a=b_to_a
    )
```

### Broadcast Connection

One source sends to many destinations simultaneously. Used for neuromodulatory and hormonal systems.

```python
class BroadcastConnection(Generic[T]):
    """
    A broadcast connection from one source to many destinations.
    
    The source publishes signals; all subscribers receive them.
    The source doesn't know or care how many subscribers there are.
    
    Used for:
    - Neuromodulatory broadcast (System 8)
    - Hormonal communication (System 12)
    
    Properties:
    - One-to-many: single source, multiple destinations
    - Decoupled: source doesn't track subscribers
    - Uniform: all subscribers receive the same signal
    - State-setting: changes HOW receivers process, not WHAT they process
    """
    def __init__(self, name: str, source: OutputPort[T]):
        self.name = name
        self.source = source
        self._subscribers: Set[InputPort[T]] = set()
    
    def subscribe(self, subscriber: InputPort[T]):
        """Add a subscriber to receive broadcasts."""
        self._subscribers.add(subscriber)
        self.source.connect_to(subscriber)
    
    def unsubscribe(self, subscriber: InputPort[T]):
        """Remove a subscriber."""
        self._subscribers.discard(subscriber)
        # Note: In a real implementation, you'd also disconnect the port
    
    def broadcast(self, signal: Signal[T]):
        """Send signal to all subscribers."""
        self.source.send(signal)
    
    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)
    
    def __repr__(self):
        return f"Broadcast({self.source} → [{self.subscriber_count} subscribers])"
```

### Loop Connection

Information cycles through multiple structures and returns to origin. Used for processing pipelines.

```python
@dataclass
class LoopSegment:
    """A single segment in a processing loop."""
    source_component: str
    source_port: str
    destination_component: str
    destination_port: str
    transform: Optional[Callable[[Signal], Signal]] = None


class LoopConnection:
    """
    A circular connection through multiple components.
    
    Information enters the loop, is processed through multiple stages,
    and returns to the origin (transformed).
    
    Used for:
    - Cortico-cerebellar loop (System 4): motor plan → error-corrected plan
    - Cortico-basal ganglia loop (System 5): action candidates → selected action
    - Papez circuit (System 7): memory → consolidated memory
    
    Properties:
    - Multi-node: passes through 3+ components
    - Transformative: output differs from input
    - Cyclic: returns to origin component
    """
    def __init__(self, name: str):
        self.name = name
        self.segments: List[LoopSegment] = []
        self._connections: List[OneWayConnection] = []
    
    def add_segment(self, segment: LoopSegment):
        """Add a segment to the loop."""
        self.segments.append(segment)
    
    def build(self, components: Dict[str, Component]):
        """
        Build the actual connections from segment definitions.
        
        Args:
            components: Dictionary mapping component names to instances
        """
        for seg in self.segments:
            source_comp = components[seg.source_component]
            dest_comp = components[seg.destination_component]
            
            source_port = source_comp.get_port(seg.source_port)
            dest_port = dest_comp.get_port(seg.destination_port)
            
            if not isinstance(source_port, OutputPort):
                raise TypeError(f"Source port must be OutputPort: {source_port}")
            if not isinstance(dest_port, InputPort):
                raise TypeError(f"Dest port must be InputPort: {dest_port}")
            
            conn = OneWayConnection(
                name=f"{seg.source_component}_to_{seg.destination_component}",
                source=source_port,
                destination=dest_port
            )
            self._connections.append(conn)
    
    def trace(self) -> List[str]:
        """Return the loop path as a list of component names."""
        if not self.segments:
            return []
        
        path = [self.segments[0].source_component]
        for seg in self.segments:
            path.append(seg.destination_component)
        return path
    
    def is_closed(self) -> bool:
        """Check if the loop returns to its origin."""
        if len(self.segments) < 2:
            return False
        return self.segments[-1].destination_component == self.segments[0].source_component
    
    def __repr__(self):
        path = " → ".join(self.trace())
        closed = " (closed)" if self.is_closed() else " (open)"
        return f"Loop({self.name}: {path}{closed})"
```

### Bypass Connection

Fast connection that skips intermediate processing. Used for emergency responses.

```python
class BypassConnection(Generic[T]):
    """
    A fast connection that bypasses normal processing stages.
    
    Exists in parallel with normal pathways. When urgency is high,
    signals can take the bypass path for faster (but less precise) processing.
    
    Used for:
    - Spinal reflexes (bypass brain entirely)
    - Hyperdirect pathway (bypass striatum)
    - Amygdala fast route (bypass cortical analysis)
    
    Properties:
    - Parallel: exists alongside normal pathway
    - Faster: fewer processing stages
    - Less precise: skips analysis/refinement
    - Priority-based: activated by urgency
    """
    def __init__(self, name: str,
                 normal_path: Pathway,
                 bypass_path: Pathway,
                 urgency_threshold: float = 0.8):
        self.name = name
        self.normal_path = normal_path
        self.bypass_path = bypass_path
        self.urgency_threshold = urgency_threshold
    
    def route(self, signal: Signal[T]) -> str:
        """
        Decide which path to use based on signal priority.
        
        Returns the name of the path used.
        """
        # Normalize priority to 0-1 range (assuming max priority is 10)
        urgency = signal.priority / 10.0
        
        if urgency >= self.urgency_threshold:
            # Use bypass path
            return "bypass"
        else:
            # Use normal path
            return "normal"
    
    def __repr__(self):
        return f"Bypass({self.name}, threshold={self.urgency_threshold})"
```

---

## Implementing Brain Structures

Now we can implement the actual brain structures using these abstractions.

### Spinal Cord

```python
# Define signal types for spinal cord
@dataclass
class BodySensation:
    """Sensory signal from the body (touch, pain, temperature, proprioception)."""
    modality: str  # 'touch', 'pain', 'temperature', 'proprioception'
    location: str  # Body part
    intensity: float
    
@dataclass
class MotorCommand:
    """Motor command to body muscles."""
    target_muscle: str
    activation: float  # 0.0 to 1.0
    
@dataclass
class Proprioception:
    """Proprioceptive signal (body position sense)."""
    joint: str
    angle: float
    velocity: float

@dataclass
class VisceralSignal:
    """Signal from internal organs."""
    organ: str
    signal_type: str  # 'stretch', 'chemical', 'temperature'
    value: float

@dataclass
class ReflexTrigger:
    """Signal that can trigger a reflex."""
    stimulus_type: str  # 'nociceptive', 'stretch', 'thermal'
    intensity: float
    location: str


class SpinalCord(LocalProcessor, ModulatableComponent):
    """
    The spinal cord component.
    
    Primary role: Body interface (gateway for body sensory/motor)
    Secondary role: Local processor (reflexes)
    
    Ports:
    - Gateway Entry: sensory_entry, interoceptive_entry
    - Gateway Exit: motor_exit, autonomic_exit
    - Input Provider: proprioception_out (to cerebellum)
    - Receiver: neuromodulation_in
    
    Capabilities:
    - Local reflex processing (withdrawal reflex, stretch reflex)
    """
    def __init__(self):
        LocalProcessor.__init__(self, "spinal_cord")
        ModulatableComponent.__init__(self, "spinal_cord")
        
        # === GATEWAY ENTRY PORTS ===
        # Where body sensations enter the CNS
        self.sensory_entry = InputPort[BodySensation](
            "sensory_entry", self.name
        )
        
        # Where visceral (organ) signals enter
        self.interoceptive_entry = InputPort[VisceralSignal](
            "interoceptive_entry", self.name
        )
        
        # === GATEWAY EXIT PORTS ===
        # Where motor commands leave to body muscles
        self.motor_exit = OutputPort[MotorCommand](
            "motor_exit", self.name
        )
        
        # Where autonomic (sympathetic) commands leave
        self.autonomic_exit = OutputPort[Any](
            "autonomic_exit", self.name
        )
        
        # === INPUT PROVIDER PORT ===
        # Sends proprioception to cerebellum (not part of loop, just provides input)
        self.proprioception_out = OutputPort[Proprioception](
            "proprioception_out", self.name
        )
        
        # === RELAY PORT ===
        # Sensory signals that continue up to brainstem
        self.sensory_relay = RelayPort[BodySensation](
            "sensory_relay", self.name,
            transform=self._process_ascending_sensory
        )
        
        # === RECEIVER PORT ===
        # Receives neuromodulatory broadcast (NE, 5-HT)
        self.neuromodulation_in = InputPort[Any](
            "neuromodulation_in", self.name
        )
        
        # === LOCAL REFLEX PORTS ===
        # Input that triggers reflexes
        self.reflex_trigger = InputPort[ReflexTrigger](
            "reflex_trigger", self.name
        )
        # Output from reflex processing
        self.reflex_output = OutputPort[MotorCommand](
            "reflex_output", self.name
        )
        
        # Register all ports
        for port in [self.sensory_entry, self.interoceptive_entry,
                     self.motor_exit, self.autonomic_exit,
                     self.proprioception_out, self.sensory_relay,
                     self.neuromodulation_in, self.reflex_trigger,
                     self.reflex_output]:
            self.add_port(port)
        
        # === LOCAL CIRCUITS (REFLEXES) ===
        self.add_local_circuit("withdrawal_reflex", self._withdrawal_reflex)
        self.add_local_circuit("stretch_reflex", self._stretch_reflex)
        
        # Wire reflex trigger to local processing
        self.reflex_trigger.on_receive(self._handle_reflex_trigger)
        
        # Wire neuromodulation to affect processing
        self.neuromodulation_in.on_receive(self._handle_neuromodulation)
    
    def _process_ascending_sensory(self, signal: Signal[BodySensation]) -> Signal[BodySensation]:
        """
        Process sensory signals before relaying to brainstem.
        
        The spinal cord does some preprocessing:
        - Modulates signal based on current gain (affected by neuromodulation)
        - May amplify or suppress based on descending control
        """
        # Apply gain modulation
        processed_payload = BodySensation(
            modality=signal.payload.modality,
            location=signal.payload.location,
            intensity=signal.payload.intensity * self.gain
        )
        return Signal(
            payload=processed_payload,
            timestamp=signal.timestamp,
            source=self.name,
            priority=signal.priority
        )
    
    def _withdrawal_reflex(self, signal: Signal[ReflexTrigger]) -> Signal[MotorCommand]:
        """
        Execute withdrawal reflex locally.
        
        This happens BEFORE the brain knows about the stimulus.
        Takes ~25-50ms total.
        """
        trigger = signal.payload
        
        # Generate motor command to withdraw from stimulus
        command = MotorCommand(
            target_muscle=f"flexors_{trigger.location}",
            activation=min(1.0, trigger.intensity * 1.5)  # Strong response
        )
        
        return Signal(
            payload=command,
            timestamp=datetime.now(),
            source=self.name,
            priority=10  # Maximum priority for reflex
        )
    
    def _stretch_reflex(self, signal: Signal[ReflexTrigger]) -> Signal[MotorCommand]:
        """
        Execute stretch reflex (e.g., knee-jerk).
        
        Monosynaptic - only one synapse, very fast (~25ms).
        """
        trigger = signal.payload
        
        # Contract the stretched muscle
        command = MotorCommand(
            target_muscle=f"extensor_{trigger.location}",
            activation=trigger.intensity * 0.8
        )
        
        return Signal(
            payload=command,
            timestamp=datetime.now(),
            source=self.name,
            priority=9
        )
    
    def _handle_reflex_trigger(self, signal: Signal[ReflexTrigger]):
        """Handle incoming reflex trigger - execute appropriate reflex."""
        trigger = signal.payload
        
        if trigger.stimulus_type == 'nociceptive':
            result = self.process_locally("withdrawal_reflex", signal)
        elif trigger.stimulus_type == 'stretch':
            result = self.process_locally("stretch_reflex", signal)
        else:
            return  # Unknown reflex type
        
        # Send motor command out
        self.reflex_output.send(result)
    
    def _handle_neuromodulation(self, signal: Signal):
        """
        Handle neuromodulatory signals.
        
        Neuromodulation affects HOW the spinal cord processes:
        - Norepinephrine: increases motor readiness
        - Serotonin: modulates pain transmission
        """
        modulator = signal.payload
        
        if hasattr(modulator, 'type'):
            if modulator.type == 'norepinephrine':
                # Increase gain - motor responses become stronger
                self.gain = min(2.0, self.gain + 0.2)
            elif modulator.type == 'serotonin':
                # Modulate pain - can increase or decrease sensitivity
                pass  # Implementation depends on context
```

### Brainstem

```python
# Additional signal types for brainstem
@dataclass
class SpecialSense:
    """Special sense signal (vision, hearing, taste, balance)."""
    modality: str  # 'visual', 'auditory', 'gustatory', 'vestibular'
    data: Any

@dataclass  
class CranialMotorCommand:
    """Motor command for head/face muscles via cranial nerves."""
    target: str  # 'eye', 'face', 'jaw', 'tongue', 'throat'
    command: Any

@dataclass
class Neuromodulator:
    """Neuromodulatory signal."""
    type: str  # 'norepinephrine', 'serotonin', 'dopamine', 'acetylcholine'
    level: float  # Concentration/intensity

@dataclass
class AlertSignal:
    """Global alert signal from locus coeruleus."""
    urgency: float
    source_event: str

@dataclass
class PosturalCommand:
    """Command for posture/balance (reticulospinal, vestibulospinal)."""
    adjustment_type: str
    parameters: Dict[str, float]


class Brainstem(LocalProcessor, ModulatableComponent):
    """
    The brainstem component.
    
    The brainstem is architecturally critical - it serves as:
    - Gateway for head sensory/motor
    - Relay for body signals
    - SOURCE of most automatic motor control and ALL neuromodulation
    - Loop component in cerebellar circuit
    - Local processor for vital functions and startle responses
    
    This is a complex component with many ports and capabilities.
    """
    def __init__(self):
        LocalProcessor.__init__(self, "brainstem")
        ModulatableComponent.__init__(self, "brainstem")
        
        # === GATEWAY ENTRY PORTS (head/special senses) ===
        self.special_senses_entry = InputPort[SpecialSense](
            "special_senses_entry", self.name
        )
        
        # === GATEWAY EXIT PORTS (head motor, parasympathetic) ===
        self.cranial_motor_exit = OutputPort[CranialMotorCommand](
            "cranial_motor_exit", self.name
        )
        self.parasympathetic_exit = OutputPort[Any](
            "parasympathetic_exit", self.name  # Vagus nerve
        )
        
        # === RELAY PORTS (body signals passing through) ===
        self.body_sensory_relay = RelayPort[BodySensation](
            "body_sensory_relay", self.name,
            transform=self._process_body_sensory
        )
        self.corticospinal_relay = RelayPort[MotorCommand](
            "corticospinal_relay", self.name
        )
        self.interoceptive_relay = RelayPort[VisceralSignal](
            "interoceptive_relay", self.name,
            transform=self._process_interoceptive
        )
        
        # === SOURCE/ORIGIN PORTS (brainstem GENERATES these signals) ===
        
        # Neuromodulatory broadcast - brainstem is the SOURCE
        self.norepinephrine_out = OutputPort[Neuromodulator](
            "norepinephrine_out", self.name  # From locus coeruleus
        )
        self.serotonin_out = OutputPort[Neuromodulator](
            "serotonin_out", self.name  # From raphe nuclei
        )
        self.dopamine_out = OutputPort[Neuromodulator](
            "dopamine_out", self.name  # From VTA/SNc
        )
        
        # Motor tract origins - brainstem GENERATES these (not relay)
        self.reticulospinal_out = OutputPort[PosturalCommand](
            "reticulospinal_out", self.name  # Posture, locomotion
        )
        self.vestibulospinal_out = OutputPort[PosturalCommand](
            "vestibulospinal_out", self.name  # Balance
        )
        self.tectospinal_out = OutputPort[Any](
            "tectospinal_out", self.name  # Orienting
        )
        
        # Emergency alert signal
        self.alert_out = OutputPort[AlertSignal](
            "alert_out", self.name  # From locus coeruleus phasic firing
        )
        
        # === LOOP COMPONENT PORTS (cerebellar circuit) ===
        # Pontine nuclei - receives from cortex, sends to cerebellum
        self.pontine_input = InputPort[Any](
            "pontine_input", self.name  # From cortex layer V
        )
        self.pontine_output = OutputPort[Any](
            "pontine_output", self.name  # To cerebellum
        )
        
        # Inferior olive - sends error signals to cerebellum
        self.olive_output = OutputPort[Any](
            "olive_output", self.name  # Climbing fibers to cerebellum
        )
        
        # === MODULATOR PORTS ===
        self.dopamine_modulation = ModulatorPort[Neuromodulator](
            "dopamine_modulation", self.name  # To striatum (System 5)
        )
        self.sleep_state_control = ModulatorPort[Any](
            "sleep_state_control", self.name  # Affects consolidation (System 14)
        )
        
        # === RECEIVER PORTS ===
        self.hormonal_input = InputPort[Any](
            "hormonal_input", self.name  # Responds to hormonal feedback
        )
        
        # Register all ports
        all_ports = [
            self.special_senses_entry,
            self.cranial_motor_exit, self.parasympathetic_exit,
            self.body_sensory_relay, self.corticospinal_relay, 
            self.interoceptive_relay,
            self.norepinephrine_out, self.serotonin_out, self.dopamine_out,
            self.reticulospinal_out, self.vestibulospinal_out, 
            self.tectospinal_out,
            self.alert_out,
            self.pontine_input, self.pontine_output, self.olive_output,
            self.dopamine_modulation, self.sleep_state_control,
            self.hormonal_input
        ]
        for port in all_ports:
            self.add_port(port)
        
        # === LOCAL CIRCUITS ===
        self.add_local_circuit("startle_response", self._startle_response)
        self.add_local_circuit("orienting_response", self._orienting_response)
        
        # Internal state
        self._arousal_level = 0.5  # 0 = sleep, 1 = maximum arousal
        self._sleep_state = "awake"  # 'awake', 'nrem', 'rem'
        
        # Wire pontine relay (cortex → cerebellum)
        self.pontine_input.on_receive(self._handle_pontine_input)
    
    def _process_body_sensory(self, signal: Signal[BodySensation]) -> Signal[BodySensation]:
        """Process body sensory signals passing through."""
        # Brainstem can modulate signals based on arousal
        processed = signal.payload
        # Could apply arousal-based modulation here
        return Signal(
            payload=processed,
            timestamp=signal.timestamp,
            source=self.name,
            priority=signal.priority
        )
    
    def _process_interoceptive(self, signal: Signal[VisceralSignal]) -> Signal[VisceralSignal]:
        """
        Process interoceptive signals in NTS and parabrachial nucleus.
        
        The brainstem does significant processing of visceral signals,
        not just relay.
        """
        # Nucleus of Solitary Tract (NTS) processing
        processed = signal.payload
        return Signal(
            payload=processed,
            timestamp=signal.timestamp,
            source=f"{self.name}_NTS",
            priority=signal.priority
        )
    
    def _handle_pontine_input(self, signal: Signal):
        """Handle input to pontine nuclei, forward to cerebellum."""
        # Transform cortical motor plan into cerebellar input format
        self.pontine_output.send(signal)
    
    def _startle_response(self, signal: Signal) -> Signal:
        """
        Execute startle response locally.
        
        Handled by reticular formation without cortical involvement.
        Very fast (~50-150ms).
        """
        # Generate startle motor pattern
        return Signal(
            payload={"response": "startle", "intensity": signal.payload.get("intensity", 1.0)},
            timestamp=datetime.now(),
            source=self.name,
            priority=10
        )
    
    def _orienting_response(self, signal: Signal) -> Signal:
        """
        Execute orienting response (turn toward stimulus).
        
        Handled by superior colliculus without cortical involvement.
        """
        return Signal(
            payload={"response": "orient", "direction": signal.payload.get("direction")},
            timestamp=datetime.now(),
            source=self.name,
            priority=8
        )
    
    # === NEUROMODULATORY BROADCAST METHODS ===
    
    def fire_locus_coeruleus(self, mode: str = "phasic"):
        """
        Fire locus coeruleus to broadcast norepinephrine.
        
        Phasic: Brief burst in response to salient event (alert signal)
        Tonic: Sustained firing affecting overall arousal
        """
        if mode == "phasic":
            # Send alert signal - "something important happened"
            alert = AlertSignal(urgency=1.0, source_event="salient_stimulus")
            self.alert_out.send(Signal(payload=alert, source=self.name, priority=10))
        
        # Send norepinephrine broadcast
        ne = Neuromodulator(type="norepinephrine", level=1.0 if mode == "phasic" else 0.5)
        self.norepinephrine_out.send(Signal(payload=ne, source=self.name))
    
    def fire_raphe(self, level: float = 0.5):
        """Fire raphe nuclei to broadcast serotonin."""
        serotonin = Neuromodulator(type="serotonin", level=level)
        self.serotonin_out.send(Signal(payload=serotonin, source=self.name))
    
    def fire_dopamine_system(self, signal_type: str, level: float):
        """
        Fire VTA/SNc to release dopamine.
        
        VTA: reward prediction error → prefrontal, limbic
        SNc: movement modulation → striatum
        """
        da = Neuromodulator(type="dopamine", level=level)
        self.dopamine_out.send(Signal(payload=da, source=self.name))
        
        # Also send modulation to striatum
        self.dopamine_modulation.modulate(Signal(payload=da, source=self.name))
```

---

## Building a Complete System

Here's how to wire up components into a complete system:

```python
class BrainCommunicationSystem:
    """
    The complete brain communication system.
    
    This class manages all components and their connections,
    representing the 14 communication systems.
    """
    def __init__(self):
        # === CREATE COMPONENTS ===
        self.spinal_cord = SpinalCord()
        self.brainstem = Brainstem()
        # self.cerebellum = Cerebellum()  # Would define similarly
        # self.thalamus = Thalamus()
        # self.cortex = Cortex()
        # ... etc
        
        self.components: Dict[str, Component] = {
            "spinal_cord": self.spinal_cord,
            "brainstem": self.brainstem,
            # ... etc
        }
        
        # === CREATE CONNECTIONS ===
        self.connections: Dict[str, Any] = {}
        
        self._setup_system1_sensory_ascending()
        self._setup_system8_neuromodulation()
        self._setup_system10_emergency()
        # ... etc
    
    def _setup_system1_sensory_ascending(self):
        """
        System 1: Sensory Ascending Pathways
        
        Type: One-way UP
        Architecture: Linear pathway
        """
        # System 1A: Body sensations via spinal cord
        # Spinal cord sensory relay → Brainstem relay → (Thalamus → Cortex)
        
        # Connect spinal cord relay output to brainstem relay input
        self.spinal_cord.sensory_relay.connect_to(
            self.brainstem.body_sensory_relay._input
        )
        
        # The pathway continues: brainstem → thalamus → cortex
        # (Would connect when those components are added)
        
        self.connections["system1a"] = Pathway("sensory_ascending_body")
        self.connections["system1a"].add_segment(
            OneWayConnection(
                "spinal_to_brainstem",
                self.spinal_cord.sensory_relay._output,
                self.brainstem.body_sensory_relay._input
            )
        )
    
    def _setup_system8_neuromodulation(self):
        """
        System 8: Neuromodulatory Broadcast
        
        Type: Broadcast
        Architecture: One-to-many
        """
        # Norepinephrine broadcast from brainstem to everywhere
        ne_broadcast = BroadcastConnection(
            "norepinephrine_broadcast",
            self.brainstem.norepinephrine_out
        )
        
        # Subscribe all components that have NE receptors
        ne_broadcast.subscribe(self.spinal_cord.neuromodulation_in)
        # ne_broadcast.subscribe(self.thalamus.neuromodulation_in)
        # ne_broadcast.subscribe(self.cortex.neuromodulation_in)
        # ... etc
        
        self.connections["system8_ne"] = ne_broadcast
    
    def _setup_system10_emergency(self):
        """
        System 10: Emergency/Urgent Communication
        
        Type: Bypass
        Architecture: Multiple shortcut pathways
        """
        # Spinal reflex - entirely local, bypasses brain
        # Already wired within SpinalCord component
        
        # For bypass routing, we'd need to implement the normal path
        # and the bypass path, then use BypassConnection to route
        pass
    
    def simulate_stepping_on_glass(self):
        """
        Simulate the emergency response to stepping on something sharp.
        
        This demonstrates how multiple systems work together:
        1. Spinal reflex (System 10) - immediate withdrawal
        2. Sensory ascending (System 1) - pain signal to brain
        3. Neuromodulatory broadcast (System 8) - alert signal
        4. Autonomic (System 9) - fight/flight preparation
        """
        print("=== Simulating: Stepping on Sharp Object ===\n")
        
        # T=0: Sharp object triggers nociceptors
        pain_signal = Signal(
            payload=ReflexTrigger(
                stimulus_type="nociceptive",
                intensity=0.9,
                location="right_foot"
            ),
            source="peripheral_nociceptor",
            priority=10
        )
        
        # Phase 1: Spinal reflex (T=0-50ms)
        print("Phase 1: Spinal Reflex (0-50ms)")
        print("  - Pain signal enters spinal cord")
        self.spinal_cord.reflex_trigger.receive(pain_signal)
        print("  - Withdrawal reflex executed locally")
        print("  - Foot withdrawing BEFORE brain knows\n")
        
        # Phase 2: Sensory signal ascending (T=50-200ms)
        print("Phase 2: Sensory Ascending (50-200ms)")
        sensory_signal = Signal(
            payload=BodySensation(
                modality="pain",
                location="right_foot",
                intensity=0.9
            ),
            source="spinal_cord",
            priority=8
        )
        self.spinal_cord.sensory_relay._input.receive(sensory_signal)
        print("  - Pain signal relayed through brainstem")
        print("  - (Would continue to thalamus → cortex)\n")
        
        # Phase 3: Locus coeruleus fires (T=100-300ms)
        print("Phase 3: Alert Broadcast (100-300ms)")
        self.brainstem.fire_locus_coeruleus(mode="phasic")
        print("  - Locus coeruleus fires phasically")
        print("  - Norepinephrine broadcast to entire brain")
        print("  - Alert signal: 'Something important happened!'\n")
        
        print("=== Simulation Complete ===")


# Example usage
if __name__ == "__main__":
    system = BrainCommunicationSystem()
    system.simulate_stepping_on_glass()
```

---

## Summary: The Complete Architecture

### Components define WHAT exists
- Each brain structure is a Component
- Components have Ports (connection interfaces)
- Components have Capabilities (local processing)

### Ports define WHAT CAN connect
- InputPort: receives signals
- OutputPort: sends signals
- RelayPort: receives, transforms, forwards
- BidirectionalPort: sends and receives
- ModulatorPort: sends modulatory signals

### Connections define HOW information flows
- OneWayConnection: unidirectional flow
- BidirectionalConnection: paired one-way channels
- BroadcastConnection: one-to-many pub-sub
- LoopConnection: multi-node circular processing
- BypassConnection: fast parallel path

### Communication Types are properties of Connections
- One-way: fire and forget
- Bidirectional: mutual exchange
- Broadcast: publish-subscribe
- Bypass: priority routing

---

## References

For the conceptual framework underlying this implementation:
- **brain-communication-framework.md** — Communication types, architectures, structural roles

For detailed descriptions of each system:
- **brain-communication-systems-overview.md** — All 14 systems with pathways and examples

---

*This document provides the software architecture for implementing brain-inspired communication systems in Python. It defines the core abstractions (Signal, Port, Component, Connection) and shows how to implement specific brain structures (SpinalCord, Brainstem) using these abstractions.*
