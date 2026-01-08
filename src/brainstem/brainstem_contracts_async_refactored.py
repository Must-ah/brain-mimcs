from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Tuple

from shared.contracts_base_async import (
    MessageType,
    Meta,
    Plane,
    RejectEvent,
    ScopeLevel,
    TopicBus,
)

from spinal_cord.spinal_contracts_async_refactored import topic_reflect_reject  # keep RejectEvent topic consistent


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
    return f"/bs/relay/{scope_level.value}/{scope}/channel/{channel}"


def topic_bs_pattern_trigger(scope_level: ScopeLevel, scope: str, pattern_type: str) -> str:
    return f"/bs/pattern/{scope_level.value}/{scope}/{pattern_type}/trigger"


def topic_bs_global_alert(scope_level: ScopeLevel, scope: str) -> str:
    return f"/bs/global/{scope_level.value}/{scope}/alert"


# =============================================================================
# Brainstem façade (typed ports + reject-on-wrong-type)
# =============================================================================

class Brainstem:
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

    def __init__(
        self,
        core_bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str = "brainstem",
        default_window_ms: int = 200,
    ) -> None:
        self._bus = core_bus
        self._reflect = reflect_bus
        self._publisher_id = publisher_id
        self._window_ms = default_window_ms

    async def ingest(self, topic: str, msg: Any) -> None:
        mt = getattr(getattr(msg, "meta", None), "message_type", None)
        if mt not in self.ALLOWED_INBOUND:
            await self._reject(topic, msg, reason="wrong_type_or_missing_meta")
            return
        return

    async def publish_relay_bundle(self, bundle: RelayBundle) -> None:
        await self._bus.publish(topic_bs_relay(bundle.scope_level, bundle.scope, bundle.channel), bundle)

    async def _reject(self, topic: str, msg: Any, reason: str) -> None:
        now_ms = getattr(getattr(msg, "meta", None), "timestamp_ms", 0) or 0
        scope_level = getattr(msg, "scope_level", None) or ScopeLevel.HOUSE
        scope = getattr(msg, "scope", None) or "unknown"

        rej = RejectEvent(
            meta=Meta(
                message_type=MessageType.REJECT_EVENT,
                schema_version="v1",
                origin_plane=Plane.BRAINSTEM,
                timestamp_ms=int(now_ms),
                correlation_id=getattr(getattr(msg, "meta", None), "correlation_id", None),
                source=self._publisher_id,
            ),
            reason=reason,
            original_topic=topic,
            publisher_id=getattr(getattr(msg, "meta", None), "source", None),
            details={
                "observed_type": str(getattr(getattr(msg, "meta", None), "message_type", None)),
                "hint": "Brainstem accepts AfferentSignal, RelayBundle, PatternTrigger, GlobalBroadcast.",
            },
        )
        await self._reflect.publish(topic_reflect_reject(scope_level, scope), rej)


__all__ = [
    # contracts
    "RelayBundle",
    "PatternTrigger",
    "PatternResponse",
    "GlobalBroadcast",
    # topics
    "topic_bs_relay",
    "topic_bs_pattern_trigger",
    "topic_bs_global_alert",
    # façade
    "Brainstem",
]
