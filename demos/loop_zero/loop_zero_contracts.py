"""
Loop Zero Contracts - Minimal contracts for concurrent proof-of-concept.

These are self-contained for the demo, using the converged GateState design
from docs/interface_specs.md (TRNSector, TRNMode, dual inhibition).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional


# ---------- Enums ----------


class ScopeLevel(str, Enum):
    DEVICE = "device"
    ROOM = "room"
    HOUSE = "house"
    USER_SESSION = "user_session"


class NucleusId(str, Enum):
    """Thalamic nuclei for routing."""
    LGN = "lgn"      # visual
    MGN = "mgn"      # auditory
    VPL = "vpl"      # somatosensory (body)
    VPM = "vpm"      # somatosensory (face)
    VL = "vl"        # motor
    VA = "va"        # motor
    PULVINAR = "pulvinar"  # higher-order
    MD = "md"        # mediodorsal


class SignalKind(str, Enum):
    DRIVER = "driver"        # payload ("what happened")
    MODULATOR = "modulator"  # context/control ("how to treat it")


class CortexLayer(str, Enum):
    L4 = "l4"  # receives from thalamus
    L5 = "l5"  # sends higher-order drivers
    L6 = "l6"  # sends modulatory feedback


class TRNSector(str, Enum):
    """TRN is organized by sectors, not individual nuclei (Cho et al. 2025)."""
    VISUAL = "visual"              # -> LGN
    AUDITORY = "auditory"          # -> MGN
    SOMATOSENSORY = "somatosensory"  # -> VPL, VPM
    MOTOR = "motor"                # -> VL, VA
    LIMBIC = "limbic"              # -> MD, AN, Reuniens


class TRNMode(str, Enum):
    """TRN operates in two modes (Sherman 2016)."""
    TONIC = "tonic"  # Awake: relay mode (gate open)
    BURST = "burst"  # Sleep/attention shift: block mode (gate closed)


# ---------- Contracts ----------


@dataclass(frozen=True)
class ThalamicEnvelope:
    """Driver or modulator signal through thalamus."""
    kind: SignalKind
    nucleus: NucleusId
    scope: str
    scope_level: ScopeLevel
    timestamp_ms: int
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    source: Optional[str] = None

    def to_json(self) -> str:
        d = asdict(self)
        d["kind"] = self.kind.value
        d["nucleus"] = self.nucleus.value
        d["scope_level"] = self.scope_level.value
        return json.dumps(d)

    @classmethod
    def from_json(cls, data: str) -> "ThalamicEnvelope":
        d = json.loads(data)
        return cls(
            kind=SignalKind(d["kind"]),
            nucleus=NucleusId(d["nucleus"]),
            scope=d["scope"],
            scope_level=ScopeLevel(d["scope_level"]),
            timestamp_ms=d["timestamp_ms"],
            payload=d["payload"],
            correlation_id=d.get("correlation_id"),
            source=d.get("source"),
        )


@dataclass(frozen=True)
class GateState:
    """
    TRN gating state - converged design from expert discussion.

    Per-sector (not per-nucleus) with dual inhibition model:
    - gpe_inhibition: Global gain from Basal Ganglia (GPe -> TRN)
    - intra_trn_inhibition: Local focus from lateral inhibition within TRN

    Source: Cho et al. 2025, Sherman 2016
    """
    scope: str
    scope_level: ScopeLevel
    sector: TRNSector
    gpe_inhibition: float         # 0..1: Global gain from BG
    intra_trn_inhibition: float   # 0..1: Local focus
    mode: TRNMode                 # TONIC (relay) or BURST (block)
    timestamp_ms: int
    reason: Optional[str] = None

    def to_json(self) -> str:
        d = asdict(self)
        d["scope_level"] = self.scope_level.value
        d["sector"] = self.sector.value
        d["mode"] = self.mode.value
        return json.dumps(d)

    @classmethod
    def from_json(cls, data: str) -> "GateState":
        d = json.loads(data)
        return cls(
            scope=d["scope"],
            scope_level=ScopeLevel(d["scope_level"]),
            sector=TRNSector(d["sector"]),
            gpe_inhibition=d["gpe_inhibition"],
            intra_trn_inhibition=d["intra_trn_inhibition"],
            mode=TRNMode(d["mode"]),
            timestamp_ms=d["timestamp_ms"],
            reason=d.get("reason"),
        )

    def is_open(self) -> bool:
        """Gate is open (allows relay) when in TONIC mode."""
        return self.mode == TRNMode.TONIC


@dataclass(frozen=True)
class RelayMessage:
    """Message relayed from Thalamus to Cortex."""
    envelope: ThalamicEnvelope
    target_area: str
    target_layer: CortexLayer
    timestamp_ms: int

    def to_json(self) -> str:
        return json.dumps({
            "envelope": json.loads(self.envelope.to_json()),
            "target_area": self.target_area,
            "target_layer": self.target_layer.value,
            "timestamp_ms": self.timestamp_ms,
        })

    @classmethod
    def from_json(cls, data: str) -> "RelayMessage":
        d = json.loads(data)
        return cls(
            envelope=ThalamicEnvelope.from_json(json.dumps(d["envelope"])),
            target_area=d["target_area"],
            target_layer=CortexLayer(d["target_layer"]),
            timestamp_ms=d["timestamp_ms"],
        )


# ---------- Topic Helpers ----------


def driver_topic(scope_level: ScopeLevel, scope: str, nucleus: NucleusId) -> str:
    """Lane A: Driver signals to thalamus."""
    return f"/A/driver/{scope_level.value}/{scope}/nucleus/{nucleus.value}"


def gate_topic(scope_level: ScopeLevel, scope: str, sector: TRNSector) -> str:
    """Lane G: TRN gate state."""
    return f"/G/gate/{scope_level.value}/{scope}/sector/{sector.value}"


def relay_topic(scope_level: ScopeLevel, scope: str, area: str, layer: CortexLayer) -> str:
    """Thalamus -> Cortex relay."""
    return f"/thalamus/relay/{scope_level.value}/{scope}/cortex/{area}/layer/{layer.value}"


# ---------- Nucleus -> Sector Mapping ----------


NUCLEUS_TO_SECTOR: Dict[NucleusId, TRNSector] = {
    NucleusId.LGN: TRNSector.VISUAL,
    NucleusId.MGN: TRNSector.AUDITORY,
    NucleusId.VPL: TRNSector.SOMATOSENSORY,
    NucleusId.VPM: TRNSector.SOMATOSENSORY,
    NucleusId.VL: TRNSector.MOTOR,
    NucleusId.VA: TRNSector.MOTOR,
    NucleusId.PULVINAR: TRNSector.VISUAL,  # Pulvinar is primarily visual
    NucleusId.MD: TRNSector.LIMBIC,
}


def get_sector_for_nucleus(nucleus: NucleusId) -> TRNSector:
    """Get the TRN sector that gates a given nucleus."""
    return NUCLEUS_TO_SECTOR.get(nucleus, TRNSector.LIMBIC)
