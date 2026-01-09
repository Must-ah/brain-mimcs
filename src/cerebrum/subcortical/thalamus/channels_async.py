from __future__ import annotations

"""
Channel model (v1): a **stable software abstraction** for thalamic / basal-ganglia
"parallel loops".

Why it exists:
- In the brain, basal ganglia–thalamo–cortical processing runs in **parallel loops**
  (motor, oculomotor, cognitive, limbic, plus sensory relays).
- In our system, we need a deterministic partition key so Thalamus/TRN can gate and
  relay concurrently without becoming a single bottleneck.

Design rule:
- Topics should carry the channel explicitly (e.g., .../channel/motor).
- GateState is typically keyed by (scope_level, scope, channel).
"""

from enum import Enum
from typing import Dict, Optional


class Channel(str, Enum):
    # ---- Sensory-style (first-order analogs) ----
    VISUAL = "visual"
    AUDIO = "audio"
    SOMATIC = "somatic"   # touch/proprioception/body sensors
    VISCERAL = "visceral" # interoception/homeostasis (optional)

    # ---- Action / selection loops (basal ganglia analogs) ----
    MOTOR = "motor"
    OCULOMOTOR = "oculomotor"  # gaze/attention shifts (cheap, fast)
    COGNITIVE = "cognitive"    # strategy / working plan selection
    LIMBIC = "limbic"          # value / motivation / valence

    # ---- Association / diffuse ----
    ASSOCIATION = "association"  # pulvinar/MD-like routing among cortical areas
    ATTENTION = "attention"      # control/attend meta-channel (often modulators)
    DIFFUSE = "diffuse"          # intralaminar/midline-like broad broadcast

    # ---- Special ----
    MEDIA = "media"              # NOT for streaming; only for media *events*


# Common aliases you might see in payloads / topics.
_CHANNEL_ALIASES: Dict[str, Channel] = {
    "vision": Channel.VISUAL,
    "video": Channel.VISUAL,       # note: video *events* still go under /sc/media/*
    "auditory": Channel.AUDIO,
    "sound": Channel.AUDIO,
    "somatosensory": Channel.SOMATIC,
    "body": Channel.SOMATIC,
    "interoception": Channel.VISCERAL,
    "homeostasis": Channel.VISCERAL,

    "eye": Channel.OCULOMOTOR,
    "gaze": Channel.OCULOMOTOR,

    "exec": Channel.COGNITIVE,
    "executive": Channel.COGNITIVE,
    "strategy": Channel.COGNITIVE,

    "value": Channel.LIMBIC,
    "motivation": Channel.LIMBIC,

    "assoc": Channel.ASSOCIATION,
    "routing": Channel.ASSOCIATION,

    "attn": Channel.ATTENTION,

    "arousal": Channel.DIFFUSE,
    "intralaminar": Channel.DIFFUSE,
}


def parse_channel(value: str) -> Optional[Channel]:
    """
    Convert a string to Channel using exact match or common aliases.
    Returns None if unknown (caller can reject or map to a default).
    """
    if not value:
        return None
    v = value.strip().lower().replace(" ", "_")
    try:
        return Channel(v)  # exact
    except Exception:
        return _CHANNEL_ALIASES.get(v)


def channel_selector(channel: Channel) -> str:
    """Canonical selector segment used in topics and GateState keys."""
    return f"channel/{channel.value}"


def describe_channel(channel: Channel) -> str:
    """
    Human-readable guidance. Useful for docs, logs, and reject hints.
    """
    descriptions = {
        Channel.VISUAL: "Visual/sight relay lane (LGN-like).",
        Channel.AUDIO: "Auditory/sound relay lane (MGN-like).",
        Channel.SOMATIC: "Somatic/touch/body relay lane (VP-like).",
        Channel.VISCERAL: "Interoceptive/homeostasis lane (hypothalamic/brainstem-adjacent).",
        Channel.MOTOR: "Motor program selection + execution bias (VA/VL + BG motor loop).",
        Channel.OCULOMOTOR: "Gaze/attention shift selection (oculomotor BG loop).",
        Channel.COGNITIVE: "Strategy/plan selection (associative BG loop).",
        Channel.LIMBIC: "Value/motivation bias (limbic BG loop).",
        Channel.ASSOCIATION: "Cortex↔cortex routing via higher-order thalamus (pulvinar/MD-like).",
        Channel.ATTENTION: "Attention-control lane (modulator coordination).",
        Channel.DIFFUSE: "Diffuse arousal/broadcast lane (intralaminar/midline-like).",
        Channel.MEDIA: "Media *events* only; streaming is out-of-band (WebRTC).",
    }
    return descriptions.get(channel, channel.value)
