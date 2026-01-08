from __future__ import annotations

from typing import Any, Tuple

from .contracts_base_async import (
    MessageType,
    Meta,
    Plane,
    RejectEvent,
    ScopeLevel,
    TopicBus,
)
from .topics_async import topic_reflect_reject


class BasePlaneFacade:
    """Base class for plane facades with common ingress validation and reject logic.

    Responsibilities (shared across all planes):
    - Ingress validation: check meta.message_type against ALLOWED_INBOUND
    - Reject pipeline: emit RejectEvent with consistent fields to reflect topic

    Subclasses must define:
    - ALLOWED_INBOUND: tuple of MessageType values accepted by this plane
    - ORIGIN_PLANE: the Plane enum value for this facade
    - REJECT_HINT: human-readable hint for rejection messages

    Subclasses should override:
    - dispatch(topic, msg): called when message passes validation

    Design principles:
    - Base class knows ONLY: envelope/meta, reject event contract, reflect topic rule
    - Base class does NOT know: domain topics, channels, device mappings, payload formats
    """

    ALLOWED_INBOUND: Tuple[MessageType, ...] = ()
    ORIGIN_PLANE: Plane = Plane.UNKNOWN
    REJECT_HINT: str = ""

    def __init__(
        self,
        bus: TopicBus,
        reflect_bus: TopicBus,
        publisher_id: str,
    ) -> None:
        self._bus = bus
        self._reflect = reflect_bus
        self._publisher_id = publisher_id

    async def ingest(self, topic: str, msg: Any) -> None:
        """Validate incoming message; dispatch if valid, reject otherwise."""
        mt = getattr(getattr(msg, "meta", None), "message_type", None)
        if mt not in self.ALLOWED_INBOUND:
            await self._reject(topic, msg, reason="wrong_type_or_missing_meta")
            return
        await self.dispatch(topic, msg)

    async def dispatch(self, topic: str, msg: Any) -> None:
        """Handle a validated message. Override in subclass for domain logic."""
        pass

    async def _reject(self, topic: str, msg: Any, reason: str) -> None:
        """Emit a RejectEvent to the reflect bus."""
        now_ms = getattr(getattr(msg, "meta", None), "timestamp_ms", 0) or 0
        scope_level = getattr(msg, "scope_level", None) or ScopeLevel.HOUSE
        scope = getattr(msg, "scope", None) or "unknown"

        rej = RejectEvent(
            meta=Meta(
                message_type=MessageType.REJECT_EVENT,
                schema_version="v1",
                origin_plane=self.ORIGIN_PLANE,
                timestamp_ms=int(now_ms),
                correlation_id=getattr(getattr(msg, "meta", None), "correlation_id", None),
                source=self._publisher_id,
            ),
            reason=reason,
            original_topic=topic,
            publisher_id=getattr(getattr(msg, "meta", None), "source", None),
            details={
                "observed_type": str(getattr(getattr(msg, "meta", None), "message_type", None)),
                "hint": self.REJECT_HINT,
            },
        )
        await self._reflect.publish(topic_reflect_reject(scope_level, scope), rej)


__all__ = ["BasePlaneFacade"]
