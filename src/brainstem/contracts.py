from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Tuple

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
# Brainstem message contracts
# =============================================================================

@dataclass(frozen=True)
class RelayBundle:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    channel: str               # somatic|auditory|visual_orient|visceral|...
    window_ms: int
    summary_features: Mapping[str, Any]
    sources: Optional[Sequence[str]] = None
    salience: Optional[float] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class PatternTrigger:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    pattern_type: str          # startle|orient|stabilize|...
    urgency: float             # 0..1
    deadline_ms: Optional[int]
    trigger: Mapping[str, Any]


@dataclass(frozen=True)
class PatternResponse:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    pattern_type: str
    request_id: Optional[str]
    status: str                # accepted|ignored|done|failed
    recommendation: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class GlobalBroadcast:
    meta: Meta
    scope_level: ScopeLevel
    scope: str
    state: Mapping[str, Any]   # e.g., {"high_alert": True}
    half_life_ms: Optional[int] = None
    expires_at_ms: Optional[int] = None


# =============================================================================
# Topic helpers (Brainstem-owned prefixes)
# =============================================================================

def topic_bs_relay(scope_level: ScopeLevel, scope: str, channel: str) -> str:
    """Build relay bundle topic with path sanitization."""
    return (
        f"/bs/relay/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/channel/{sanitize_path_component(channel, 'channel')}"
    )


def topic_bs_pattern_trigger(scope_level: ScopeLevel, scope: str, pattern_type: str) -> str:
    """Build pattern trigger topic with path sanitization."""
    return (
        f"/bs/pattern/{scope_level.value}/{sanitize_path_component(scope, 'scope')}"
        f"/{sanitize_path_component(pattern_type, 'pattern_type')}/trigger"
    )


def topic_bs_global_alert(scope_level: ScopeLevel, scope: str) -> str:
    """Build global alert topic with path sanitization."""
    return f"/bs/global/{scope_level.value}/{sanitize_path_component(scope, 'scope')}/alert"


# =============================================================================
# Brainstem façade (typed ports + reject-on-wrong-type)
# =============================================================================

class Brainstem(BasePlaneFacade):
    """Brainstem plane façade.

    Accepts:
      - AfferentSignal (for transformation only)
      - RelayBundle (optional internal coordination)
      - PatternTrigger
      - GlobalBroadcast

    Rejects everything else by emitting a RejectEvent to Reflect.
    """

    ALLOWED_INBOUND: Tuple[MessageType, ...] = (
        MessageType.AFFERENT_SIGNAL,
        MessageType.RELAY_BUNDLE,
        MessageType.PATTERN_TRIGGER,
        MessageType.GLOBAL_BROADCAST,
    )
    ORIGIN_PLANE = Plane.BRAINSTEM
    REJECT_HINT = "Brainstem accepts AfferentSignal, RelayBundle, PatternTrigger, GlobalBroadcast."

    def __init__(
        self,
        core_bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str = "brainstem",
        default_window_ms: int = 200,
    ) -> None:
        super().__init__(core_bus, reflect_bus, publisher_id)
        self._window_ms = default_window_ms

    async def publish_relay_bundle(self, bundle: RelayBundle) -> None:
        await self._bus.publish(topic_bs_relay(bundle.scope_level, bundle.scope, bundle.channel), bundle)


__all__ = [
    "RelayBundle",
    "PatternTrigger",
    "PatternResponse",
    "GlobalBroadcast",
    "topic_bs_relay",
    "topic_bs_pattern_trigger",
    "topic_bs_global_alert",
    "Brainstem",
]
