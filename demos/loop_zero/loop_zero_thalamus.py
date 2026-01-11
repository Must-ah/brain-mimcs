#!/usr/bin/env python3
"""
Loop Zero - Thalamus Process

Thalamic relay with TRN gating:
- Receives driver signals from Cortex L5 (Lane A)
- Checks TRN gate state before relaying
- Relays to Cortex L4 if gate is open (TONIC mode)
- Blocks if gate is closed (BURST mode)

Runs as a separate process to prove non-blocking concurrency.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Dict, Optional

import paho.mqtt.client as mqtt

from loop_zero_contracts import (
    CortexLayer,
    GateState,
    NucleusId,
    RelayMessage,
    ScopeLevel,
    ThalamicEnvelope,
    TRNMode,
    TRNSector,
    driver_topic,
    gate_topic,
    get_sector_for_nucleus,
    relay_topic,
)

logging.basicConfig(
    level=logging.INFO,
    format=f"[THALAMUS PID={os.getpid()}] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Configuration
BROKER_HOST = os.environ.get("MQTT_HOST", "localhost")
BROKER_PORT = int(os.environ.get("MQTT_PORT", "1883"))
SCOPE = os.environ.get("SCOPE", "demo_room")
SCOPE_LEVEL = ScopeLevel.ROOM

# Nucleus -> Cortex area mapping (simplified for demo)
NUCLEUS_TO_CORTEX = {
    NucleusId.LGN: "V1",       # Visual
    NucleusId.MGN: "A1",       # Auditory
    NucleusId.VPL: "S1",       # Somatosensory
    NucleusId.VPM: "S1",       # Somatosensory
    NucleusId.VL: "M1",        # Motor
    NucleusId.VA: "M1",        # Motor
    NucleusId.PULVINAR: "PPC", # Posterior parietal (higher-order)
    NucleusId.MD: "PFC",       # Prefrontal (higher-order)
}


class ThalamusProcess:
    """Thalamus process with relay and gating logic."""

    def __init__(self, broker_host: str, broker_port: int):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client: Optional[mqtt.Client] = None
        self.running = False
        self.messages_received = 0
        self.messages_relayed = 0
        self.messages_blocked = 0

        # Gate state per sector (default: all open)
        self.gate_states: Dict[TRNSector, GateState] = {}

    def get_gate_state(self, sector: TRNSector) -> GateState:
        """Get current gate state for a sector, default to TONIC (open)."""
        if sector not in self.gate_states:
            # Default: gate is open
            return GateState(
                scope=SCOPE,
                scope_level=SCOPE_LEVEL,
                sector=sector,
                gpe_inhibition=0.0,
                intra_trn_inhibition=0.0,
                mode=TRNMode.TONIC,
                timestamp_ms=int(time.time() * 1000),
                reason="default_open",
            )
        return self.gate_states[sector]

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            log.info("Connected to MQTT broker")

            # Subscribe to driver signals (Lane A)
            driver_pattern = f"/A/driver/{SCOPE_LEVEL.value}/{SCOPE}/nucleus/+"
            client.subscribe(driver_pattern)
            log.info(f"Subscribed to drivers: {driver_pattern}")

            # Subscribe to gate states (Lane G)
            gate_pattern = f"/G/gate/{SCOPE_LEVEL.value}/{SCOPE}/sector/+"
            client.subscribe(gate_pattern)
            log.info(f"Subscribed to gates: {gate_pattern}")
        else:
            log.error(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """Handle incoming messages."""
        topic = msg.topic

        if "/A/driver/" in topic:
            self.handle_driver(msg)
        elif "/G/gate/" in topic:
            self.handle_gate(msg)
        else:
            log.warning(f"Unknown topic: {topic}")

    def handle_driver(self, msg):
        """Handle driver signal from Cortex - relay if gate is open."""
        try:
            envelope = ThalamicEnvelope.from_json(msg.payload.decode())
            self.messages_received += 1

            # Get the sector for this nucleus
            sector = get_sector_for_nucleus(envelope.nucleus)
            gate = self.get_gate_state(sector)

            log.info(
                f"RECEIVED #{self.messages_received}: "
                f"nucleus={envelope.nucleus.value} "
                f"sector={sector.value} "
                f"gate={gate.mode.value}"
            )

            if gate.is_open():
                # Gate is open - relay to cortex
                self.relay_to_cortex(envelope)
            else:
                # Gate is closed - block
                self.messages_blocked += 1
                log.info(
                    f"BLOCKED #{self.messages_blocked}: "
                    f"nucleus={envelope.nucleus.value} "
                    f"reason=gate_{gate.mode.value}"
                )

        except Exception as e:
            log.error(f"Error handling driver: {e}")

    def handle_gate(self, msg):
        """Handle gate state update from TRN."""
        try:
            gate = GateState.from_json(msg.payload.decode())
            old_mode = self.gate_states.get(gate.sector)
            old_mode_str = old_mode.mode.value if old_mode else "none"

            self.gate_states[gate.sector] = gate

            log.info(
                f"GATE UPDATE: sector={gate.sector.value} "
                f"{old_mode_str} -> {gate.mode.value} "
                f"(gpe={gate.gpe_inhibition:.2f}, intra={gate.intra_trn_inhibition:.2f})"
            )

        except Exception as e:
            log.error(f"Error handling gate: {e}")

    def relay_to_cortex(self, envelope: ThalamicEnvelope):
        """Relay message to appropriate cortex area."""
        target_area = NUCLEUS_TO_CORTEX.get(envelope.nucleus, "unknown")
        target_layer = CortexLayer.L4  # First-order relay to L4

        relay = RelayMessage(
            envelope=envelope,
            target_area=target_area,
            target_layer=target_layer,
            timestamp_ms=int(time.time() * 1000),
        )

        topic = relay_topic(SCOPE_LEVEL, SCOPE, target_area, target_layer)
        self.client.publish(topic, relay.to_json())
        self.messages_relayed += 1

        log.info(
            f"RELAYED #{self.messages_relayed}: "
            f"nucleus={envelope.nucleus.value} -> {target_area}/{target_layer.value}"
        )

    async def run(self):
        """Main loop."""
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"thalamus_{os.getpid()}",
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        log.info(f"Connecting to {self.broker_host}:{self.broker_port}")
        self.client.connect(self.broker_host, self.broker_port)
        self.client.loop_start()

        self.running = True
        log.info("Thalamus process started - relaying with TRN gating")

        try:
            while self.running:
                # Just keep running - all work is in callbacks
                await asyncio.sleep(1.0)

        except KeyboardInterrupt:
            log.info("Shutting down...")
        finally:
            self.running = False
            self.client.loop_stop()
            self.client.disconnect()
            log.info(
                f"Thalamus stopped. "
                f"Received={self.messages_received}, "
                f"Relayed={self.messages_relayed}, "
                f"Blocked={self.messages_blocked}"
            )


async def main():
    log.info("=" * 60)
    log.info("LOOP ZERO - THALAMUS PROCESS")
    log.info(f"PID: {os.getpid()}")
    log.info("=" * 60)

    thalamus = ThalamusProcess(BROKER_HOST, BROKER_PORT)
    await thalamus.run()


if __name__ == "__main__":
    asyncio.run(main())
