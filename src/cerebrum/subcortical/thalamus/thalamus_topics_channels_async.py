from __future__ import annotations

"""
Thalamus/TRN topic helpers using Channel as the partition key.

Convention:
- event vs state is encoded in the topic.
- GateState is retained state: /th/gate/state/...
- ModulatorSignal is event:  /th/mod/event/...
- Gated relay output is event: /th/relay/event/...

These helpers are *pure string builders* (wire routing only).
"""

from typing import Optional
from contracts_base_async import ScopeLevel
from channels_async import Channel, channel_selector


def th_modulator_event(scope_level: ScopeLevel, scope: str, channel: Channel) -> str:
    return f"/th/mod/event/{scope_level.value}/{scope}/{channel_selector(channel)}"


def th_gate_state(scope_level: ScopeLevel, scope: str, channel: Channel) -> str:
    # Retained by broker (state topic)
    return f"/th/gate/state/{scope_level.value}/{scope}/{channel_selector(channel)}"


def th_relay_event(scope_level: ScopeLevel, scope: str, channel: Channel) -> str:
    return f"/th/relay/event/{scope_level.value}/{scope}/{channel_selector(channel)}"


def th_route_audit_event(scope_level: ScopeLevel, scope: str, channel: Channel) -> str:
    return f"/th/route/event/{scope_level.value}/{scope}/{channel_selector(channel)}"


def bs_relay_event(scope_level: ScopeLevel, scope: str, channel: Channel) -> str:
    """Brainstem RelayBundle topic canonicalization (if you standardize here)."""
    return f"/bs/relay/event/{scope_level.value}/{scope}/{channel_selector(channel)}"


def sc_media_event(scope_level: ScopeLevel, scope: str, device_id: str, kind: str) -> str:
    """MediaEvent is link-free and lives under /sc/media."""
    kind_norm = kind.strip().lower().replace(" ", "_")
    return f"/sc/media/event/{scope_level.value}/{scope}/device/{device_id}/kind/{kind_norm}"
