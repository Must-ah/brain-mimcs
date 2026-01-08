from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple

from shared.contracts_base_async import (
    MessageType,
    Meta,
    Plane,
    RejectEvent,
    ScopeLevel,
    TopicBus,
)

from shared.topics_async import topic_reflect_reject


# =============================================================================
# SpinalCord message contracts
# =============================================================================

@dataclass(frozen=True)
class AfferentSignal:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    sensor_type: str
    payload: Mapping[str, Any]
    units: Optional[str] = None
    confidence: Optional[float] = None
    salience: Optional[float] = None


@dataclass(frozen=True)
class EfferentCommand:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    actuator_type: str
    action_id: str  # idempotency key
    payload: Mapping[str, Any]
    deadline_ms: Optional[int] = None
    priority: Optional[int] = None
    safety_constraints: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class OutcomeEvent:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    device_id: str
    action_id: str
    status: str  # ack|in_progress|done|failed
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexRule:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexTrigger:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ReflexEvent:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    reflex_id: str
    action_id: str
    payload: Mapping[str, Any]


# =============================================================================
# Topic helpers (Spinal-owned prefixes)
# =============================================================================

def topic_sc_aff(scope_level: ScopeLevel, scope: str, sensor_type: str, device_id: str) -> str:
    return f"/sc/aff/{scope_level.value}/{scope}/sensor/{sensor_type}/device/{device_id}"


def topic_sc_eff(scope_level: ScopeLevel, scope: str, actuator_type: str, device_id: str, action_id: str) -> str:
    return f"/sc/eff/{scope_level.value}/{scope}/act/{actuator_type}/device/{device_id}/cmd/{action_id}"


def topic_sc_out(scope_level: ScopeLevel, scope: str, device_id: str, action_id: str) -> str:
    return f"/sc/out/{scope_level.value}/{scope}/device/{device_id}/action/{action_id}"


def topic_sc_reflex_config(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    return f"/sc/reflex/{scope_level.value}/{scope}/rule/{reflex_id}/configure"


def topic_sc_reflex_trigger(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    return f"/sc/reflex/{scope_level.value}/{scope}/rule/{reflex_id}/trigger"


# =============================================================================
# SpinalCord façade (typed ports + reject-on-wrong-type)
# =============================================================================

class SpinalCord:
    """SpinalCord plane façade.

    Accepts only:
      - AfferentSignal
      - EfferentCommand
      - ReflexRule / ReflexTrigger

    Rejects everything else by emitting a RejectEvent to Reflect (Broker X).
    """

    ALLOWED_INBOUND: Tuple[MessageType, ...] = (
        MessageType.AFFERENT_SIGNAL,
        MessageType.EFFERENT_COMMAND,
        MessageType.REFLEX_RULE,
        MessageType.REFLEX_TRIGGER,
    )

    def __init__(
        self,
        spinal_bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str = "spinal",
    ) -> None:
        self._bus = spinal_bus
        self._reflect = reflect_bus
        self._publisher_id = publisher_id

    async def ingest(self, topic: str, msg: Any) -> None:
        mt = getattr(getattr(msg, "meta", None), "message_type", None)
        if mt not in self.ALLOWED_INBOUND:
            await self._reject(topic, msg, reason="wrong_type_or_missing_meta")
            return
        return

    async def publish_outcome(self, evt: OutcomeEvent) -> None:
        await self._bus.publish(
            topic_sc_out(evt.scope_level, evt.scope, evt.device_id, evt.action_id),
            evt,
        )

    async def _reject(self, topic: str, msg: Any, reason: str) -> None:
        now_ms = getattr(getattr(msg, "meta", None), "timestamp_ms", 0) or 0
        scope_level = getattr(msg, "scope_level", None) or ScopeLevel.HOUSE
        scope = getattr(msg, "scope", None) or "unknown"

        rej = RejectEvent(
            meta=Meta(
                message_type=MessageType.REJECT_EVENT,
                schema_version="v1",
                origin_plane=Plane.SPINAL,
                timestamp_ms=int(now_ms),
                correlation_id=getattr(getattr(msg, "meta", None), "correlation_id", None),
                source=self._publisher_id,
            ),
            reason=reason,
            original_topic=topic,
            publisher_id=getattr(getattr(msg, "meta", None), "source", None),
            details={
                "observed_type": str(getattr(getattr(msg, "meta", None), "message_type", None)),
                "hint": "SpinalCord accepts only AfferentSignal, EfferentCommand, ReflexRule, ReflexTrigger.",
            },
        )
        await self._reflect.publish(topic_reflect_reject(scope_level, scope), rej)


__all__ = [
    "AfferentSignal",
    "EfferentCommand",
    "OutcomeEvent",
    "ReflexRule",
    "ReflexTrigger",
    "ReflexEvent",
    "topic_sc_aff",
    "topic_sc_eff",
    "topic_sc_out",
    "topic_sc_reflex_config",
    "topic_sc_reflex_trigger",
    "SpinalCord",
]
