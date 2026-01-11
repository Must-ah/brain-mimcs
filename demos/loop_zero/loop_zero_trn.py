#!/usr/bin/env python3
"""
Loop Zero - TRN (Thalamic Reticular Nucleus) Process

Controls thalamic gating:
- Publishes GateState to Lane G
- Alternates between TONIC (open) and BURST (closed) modes
- Demonstrates per-sector gating control

Runs as a separate process to prove non-blocking concurrency.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import time
from typing import Optional

import paho.mqtt.client as mqtt

from loop_zero_contracts import (
    GateState,
    ScopeLevel,
    TRNMode,
    TRNSector,
    gate_topic,
)

logging.basicConfig(
    level=logging.INFO,
    format=f"[TRN PID={os.getpid()}] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Configuration
BROKER_HOST = os.environ.get("MQTT_HOST", "localhost")
BROKER_PORT = int(os.environ.get("MQTT_PORT", "1883"))
SCOPE = os.environ.get("SCOPE", "demo_room")
SCOPE_LEVEL = ScopeLevel.ROOM


class TRNProcess:
    """TRN process - controls gating for thalamic relay."""

    def __init__(self, broker_host: str, broker_port: int):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client: Optional[mqtt.Client] = None
        self.running = False
        self.gate_updates = 0

        # Current mode per sector
        self.modes = {sector: TRNMode.TONIC for sector in TRNSector}

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            log.info("Connected to MQTT broker")
        else:
            log.error(f"Connection failed with code {rc}")

    def publish_gate_state(
        self,
        sector: TRNSector,
        mode: TRNMode,
        reason: str,
        gpe_inhibition: float = 0.0,
        intra_trn_inhibition: float = 0.0,
    ):
        """Publish gate state for a sector."""
        gate = GateState(
            scope=SCOPE,
            scope_level=SCOPE_LEVEL,
            sector=sector,
            gpe_inhibition=gpe_inhibition,
            intra_trn_inhibition=intra_trn_inhibition,
            mode=mode,
            timestamp_ms=int(time.time() * 1000),
            reason=reason,
        )

        topic = gate_topic(SCOPE_LEVEL, SCOPE, sector)
        self.client.publish(topic, gate.to_json())
        self.gate_updates += 1

        status = "OPEN" if mode == TRNMode.TONIC else "CLOSED"
        log.info(
            f"GATE #{self.gate_updates}: "
            f"sector={sector.value} -> {status} "
            f"(mode={mode.value}, reason={reason})"
        )

    def toggle_sector(self, sector: TRNSector, reason: str):
        """Toggle a sector between TONIC and BURST."""
        current = self.modes[sector]
        new_mode = TRNMode.BURST if current == TRNMode.TONIC else TRNMode.TONIC
        self.modes[sector] = new_mode

        # When in BURST mode, higher inhibition values
        if new_mode == TRNMode.BURST:
            gpe = random.uniform(0.5, 0.8)
            intra = random.uniform(0.3, 0.6)
        else:
            gpe = random.uniform(0.0, 0.2)
            intra = random.uniform(0.0, 0.2)

        self.publish_gate_state(sector, new_mode, reason, gpe, intra)

    async def run(self):
        """Main loop: periodically toggle gates to demonstrate gating."""
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"trn_{os.getpid()}",
        )
        self.client.on_connect = self.on_connect

        log.info(f"Connecting to {self.broker_host}:{self.broker_port}")
        self.client.connect(self.broker_host, self.broker_port)
        self.client.loop_start()

        self.running = True
        log.info("TRN process started - controlling thalamic gates")

        # Initial state: all gates open
        for sector in [TRNSector.VISUAL, TRNSector.AUDITORY, TRNSector.SOMATOSENSORY]:
            self.publish_gate_state(
                sector, TRNMode.TONIC, "initial_open", 0.1, 0.1
            )

        cycle = 0
        try:
            while self.running:
                cycle += 1

                # Every few seconds, toggle a random sector
                await asyncio.sleep(random.uniform(4.0, 8.0))

                # Pick a sector to toggle
                sector = random.choice([
                    TRNSector.VISUAL,
                    TRNSector.AUDITORY,
                    TRNSector.SOMATOSENSORY,
                ])

                reason = f"attention_shift_cycle_{cycle}"
                self.toggle_sector(sector, reason)

                # Occasionally toggle motor (less frequently)
                if random.random() < 0.2:
                    await asyncio.sleep(0.5)
                    self.toggle_sector(TRNSector.MOTOR, f"motor_check_{cycle}")

        except KeyboardInterrupt:
            log.info("Shutting down...")
        finally:
            self.running = False
            self.client.loop_stop()
            self.client.disconnect()
            log.info(f"TRN stopped. Gate updates={self.gate_updates}")


async def main():
    log.info("=" * 60)
    log.info("LOOP ZERO - TRN (THALAMIC RETICULAR NUCLEUS) PROCESS")
    log.info(f"PID: {os.getpid()}")
    log.info("=" * 60)

    trn = TRNProcess(BROKER_HOST, BROKER_PORT)
    await trn.run()


if __name__ == "__main__":
    asyncio.run(main())
