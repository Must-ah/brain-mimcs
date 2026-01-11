#!/usr/bin/env python3
"""
Loop Zero - Cortex Process

Simulates cortical layers:
- L4: Receives relay messages from Thalamus
- L5: Sends driver signals to Thalamus

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
    CortexLayer,
    NucleusId,
    RelayMessage,
    ScopeLevel,
    SignalKind,
    ThalamicEnvelope,
    driver_topic,
    relay_topic,
)

logging.basicConfig(
    level=logging.INFO,
    format=f"[CORTEX PID={os.getpid()}] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Configuration
BROKER_HOST = os.environ.get("MQTT_HOST", "localhost")
BROKER_PORT = int(os.environ.get("MQTT_PORT", "1883"))
SCOPE = os.environ.get("SCOPE", "demo_room")
SCOPE_LEVEL = ScopeLevel.ROOM


class CortexProcess:
    """Cortex process with L4 (receive) and L5 (send) functionality."""

    def __init__(self, broker_host: str, broker_port: int):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client: Optional[mqtt.Client] = None
        self.running = False
        self.messages_received = 0
        self.messages_sent = 0

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            log.info("Connected to MQTT broker")
            # L4: Subscribe to relay messages from Thalamus
            # Subscribe to all cortex areas and layers
            topic = f"/thalamus/relay/{SCOPE_LEVEL.value}/{SCOPE}/cortex/+/layer/+"
            client.subscribe(topic)
            log.info(f"L4 subscribed to: {topic}")
        else:
            log.error(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """L4: Receive relay messages from Thalamus."""
        try:
            relay = RelayMessage.from_json(msg.payload.decode())
            self.messages_received += 1
            log.info(
                f"L4 RECEIVED #{self.messages_received}: "
                f"nucleus={relay.envelope.nucleus.value} "
                f"area={relay.target_area} "
                f"payload={relay.envelope.payload}"
            )
        except Exception as e:
            log.error(f"Error processing message: {e}")

    def send_driver_signal(self, nucleus: NucleusId, payload: dict):
        """L5: Send driver signal to Thalamus."""
        envelope = ThalamicEnvelope(
            kind=SignalKind.DRIVER,
            nucleus=nucleus,
            scope=SCOPE,
            scope_level=SCOPE_LEVEL,
            timestamp_ms=int(time.time() * 1000),
            payload=payload,
            source="cortex_l5",
        )
        topic = driver_topic(SCOPE_LEVEL, SCOPE, nucleus)
        self.client.publish(topic, envelope.to_json())
        self.messages_sent += 1
        log.info(
            f"L5 SENT #{self.messages_sent}: "
            f"nucleus={nucleus.value} "
            f"payload={payload}"
        )

    async def run(self):
        """Main loop: periodically generate sensory events."""
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"cortex_{os.getpid()}",
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        log.info(f"Connecting to {self.broker_host}:{self.broker_port}")
        self.client.connect(self.broker_host, self.broker_port)
        self.client.loop_start()

        self.running = True
        log.info("Cortex process started - generating mock sensory events")

        nuclei = [NucleusId.LGN, NucleusId.MGN, NucleusId.VPL]

        try:
            while self.running:
                # Generate a mock sensory event
                nucleus = random.choice(nuclei)
                payload = {
                    "event_type": "sensory",
                    "intensity": random.uniform(0.1, 1.0),
                    "timestamp": int(time.time() * 1000),
                }
                self.send_driver_signal(nucleus, payload)

                # Non-blocking wait
                await asyncio.sleep(random.uniform(1.0, 3.0))

        except KeyboardInterrupt:
            log.info("Shutting down...")
        finally:
            self.running = False
            self.client.loop_stop()
            self.client.disconnect()
            log.info(
                f"Cortex stopped. Sent={self.messages_sent}, Received={self.messages_received}"
            )


async def main():
    log.info("=" * 60)
    log.info("LOOP ZERO - CORTEX PROCESS")
    log.info(f"PID: {os.getpid()}")
    log.info("=" * 60)

    cortex = CortexProcess(BROKER_HOST, BROKER_PORT)
    await cortex.run()


if __name__ == "__main__":
    asyncio.run(main())
