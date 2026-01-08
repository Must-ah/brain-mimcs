from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple

from shared.contracts_base_async import (
    MessageType,
    Meta,
    Plane,
    ScopeLevel,
    TopicBus,
    sanitize_path_component,
)
from shared.plane_base_async import BasePlaneFacade


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
    """Build afferent signal topic with path sanitization."""
    return (
        f"/sc/aff/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/sensor/{sanitize_path_component(sensor_type, 'sensor_type')}"
        f"/device/{sanitize_path_component(device_id, 'device_id')}"
    )


def topic_sc_eff(scope_level: ScopeLevel, scope: str, actuator_type: str, device_id: str, action_id: str) -> str:
    """Build efferent command topic with path sanitization."""
    return (
        f"/sc/eff/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/act/{sanitize_path_component(actuator_type, 'actuator_type')}"
        f"/device/{sanitize_path_component(device_id, 'device_id')}"
        f"/cmd/{sanitize_path_component(action_id, 'action_id')}"
    )


def topic_sc_out(scope_level: ScopeLevel, scope: str, device_id: str, action_id: str) -> str:
    """Build outcome event topic with path sanitization."""
    return (
        f"/sc/out/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/device/{sanitize_path_component(device_id, 'device_id')}"
        f"/action/{sanitize_path_component(action_id, 'action_id')}"
    )


def topic_sc_reflex_config(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    """Build reflex configuration topic with path sanitization."""
    return (
        f"/sc/reflex/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/rule/{sanitize_path_component(reflex_id, 'reflex_id')}/configure"
    )


def topic_sc_reflex_trigger(scope_level: ScopeLevel, scope: str, reflex_id: str) -> str:
    """Build reflex trigger topic with path sanitization."""
    return (
        f"/sc/reflex/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/rule/{sanitize_path_component(reflex_id, 'reflex_id')}/trigger"
    )


# =============================================================================
# SpinalCord façade (typed ports + reject-on-wrong-type)
# =============================================================================

class SpinalCord(BasePlaneFacade):
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
    ORIGIN_PLANE = Plane.SPINAL
    REJECT_HINT = "SpinalCord accepts only AfferentSignal, EfferentCommand, ReflexRule, ReflexTrigger."

    def __init__(
        self,
        spinal_bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str = "spinal",
    ) -> None:
        super().__init__(spinal_bus, reflect_bus, publisher_id)

    async def publish_outcome(self, evt: OutcomeEvent) -> None:
        await self._bus.publish(
            topic_sc_out(evt.scope_level, evt.scope, evt.device_id, evt.action_id),
            evt,
        )


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
