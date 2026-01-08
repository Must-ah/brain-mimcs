from __future__ import annotations

from .contracts_base_async import ScopeLevel


def topic_reflect_reject(scope_level: ScopeLevel, scope: str) -> str:
    """Canonical RejectEvent topic (shared across planes)."""
    return f"/X/reflect/{scope_level.value}/{scope}/lane/reject"
