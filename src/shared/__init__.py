"""Shared package (Pattern A).

Single source of truth for:
- core enums/types (ScopeLevel, Plane, MessageType, Meta, RejectEvent)
- TopicBus protocol + InMemoryTopicBus (for demos/tests)
- shared topic helpers (e.g., topic_reflect_reject)
"""

from .contracts_base_async import *  # noqa: F401,F403
from .topics_async import *  # noqa: F401,F403
