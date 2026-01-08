from __future__ import annotations

import asyncio
from typing import Any, Optional

# Pattern A imports (your current tree layout under src/)
from shared.contracts_base_async import (
    InMemoryTopicBus,
    Meta,
    MessageType,
    Plane,
    ScopeLevel,
)
from shared.topics_async import topic_reflect_reject

from spinal_cord.spinal_contracts_async_refactored_v2 import (
    AfferentSignal,
    EfferentCommand,
    SpinalCord,
    topic_sc_aff,
)

from brainstem.brainstem_contracts_async_refactored_v2 import (
    Brainstem,
    RelayBundle,
    topic_bs_relay,
)


async def _next_or_none(aiter, timeout_s: float = 1.0) -> Optional[Any]:
    """Wait for the next item from an async iterator, with timeout."""
    try:
        return await asyncio.wait_for(aiter.__anext__(), timeout=timeout_s)
    except asyncio.TimeoutError:
        return None


async def demo_spinal_brainstem() -> None:
    """Demo:
    1) Send a spinal afferent (accepted by SpinalCord)
    2) Publish a Brainstem RelayBundle (simulate transform)
    3) Send a wrong-type message to Brainstem to trigger a RejectEvent

    NOTE: This version avoids a race condition by subscribing BEFORE publishing.
    """

    # In-memory buses (stand-ins for separate brokers)
    spinal_bus = InMemoryTopicBus()
    core_bus = InMemoryTopicBus()
    reflect_bus = InMemoryTopicBus()

    spinal = SpinalCord(
        spinal_bus=spinal_bus, reflect_bus=reflect_bus, publisher_id="spinal-demo"
    )
    brainstem = Brainstem(
        core_bus=core_bus, reflect_bus=reflect_bus, publisher_id="brainstem-demo"
    )

    scope_level = ScopeLevel.ROOM
    scope = "living_room"

    # ---- 1) Spinal afferent arrives (accepted) ----
    aff_topic = topic_sc_aff(scope_level, scope, sensor_type="motion", device_id="m1")
    aff = AfferentSignal(
        meta=Meta(
            message_type=MessageType.AFFERENT_SIGNAL,
            schema_version="v1",
            origin_plane=Plane.SPINAL,
            timestamp_ms=1,
            correlation_id="corr-1",
            source="device:m1",
        ),
        scope_level=scope_level,
        scope=scope,
        device_id="m1",
        sensor_type="motion",
        payload={"motion": 1, "confidence": 0.85},
        units=None,
        confidence=0.85,
        salience=0.6,
    )

    await spinal.ingest(aff_topic, aff)
    print(f"[ok] SpinalCord accepted AfferentSignal on {aff_topic}")

    # ---- 2) Brainstem publishes a relay bundle (simulate transform) ----
    relay = RelayBundle(
        meta=Meta(
            message_type=MessageType.RELAY_BUNDLE,
            schema_version="v1",
            origin_plane=Plane.BRAINSTEM,
            timestamp_ms=2,
            correlation_id="corr-1",
            source="brainstem-demo",
        ),
        scope_level=scope_level,
        scope=scope,
        channel="somatic",
        window_ms=200,
        summary_features={"events": ["motion"], "max_salience": 0.6},
        sources=["m1"],
        salience=0.6,
        confidence=0.85,
    )

    relay_topic = topic_bs_relay(scope_level, scope, channel="somatic")

    # Subscribe BEFORE publishing to avoid missing the message.
    relay_sub = core_bus.subscribe(relay_topic)
    await brainstem.publish_relay_bundle(relay)
    received_relay = await _next_or_none(relay_sub, timeout_s=1.0)

    if received_relay is None:
        print(f"[warn] No RelayBundle received on {relay_topic}")
    else:
        print(
            f"[ok] Brainstem published RelayBundle on {relay_topic}: {received_relay}"
        )

    # ---- 3) Wrong-type to Brainstem => RejectEvent on Reflect ----
    bad = EfferentCommand(
        meta=Meta(
            message_type=MessageType.EFFERENT_COMMAND,  # not allowed inbound to Brainstem
            schema_version="v1",
            origin_plane=Plane.RELIABLE,
            timestamp_ms=3,
            correlation_id="corr-2",
            source="reliable-demo",
        ),
        scope_level=scope_level,
        scope=scope,
        device_id="lamp1",
        actuator_type="light",
        action_id="act-1",
        payload={"power": "on"},
        deadline_ms=1000,
        priority=10,
        safety_constraints=None,
    )

    reject_topic = topic_reflect_reject(scope_level, scope)

    # Subscribe BEFORE sending the bad message.
    reject_sub = reflect_bus.subscribe(reject_topic)
    await brainstem.ingest(topic="/bs/ingress/demo", msg=bad)
    rej = await _next_or_none(reject_sub, timeout_s=1.0)

    if rej is None:
        print(f"[warn] No RejectEvent observed on {reject_topic}")
    else:
        print(
            f"[ok] Brainstem rejected wrong-type message; RejectEvent on {reject_topic}: {rej}"
        )


if __name__ == "__main__":
    asyncio.run(demo_spinal_brainstem())
