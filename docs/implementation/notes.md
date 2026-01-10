# Implementation Notes

Notes and decisions to reference when implementing brain-mimc components.

---

## Edge Transformation (2026-01-10)

**Decision:** Continuous → Discrete transformation happens at the edge.

**Brain model:** Retina
- Photoreceptors: continuous (graded potentials)
- RGCs: discrete (spikes)
- Transformation at: Bipolar → RGC synapse
- Compression: 126M → 1M

**Software implication:**
- SpinalCord/sensors convert raw streams to discrete events
- No video streams on network - only events
- Fire on change, not continuous polling

**Example:**
```
Camera → SpinalCord → [MotionDetected, ObjectAppeared] → Network
```

---

(Add more notes as decisions are made)
