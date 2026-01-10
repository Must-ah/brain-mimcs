---
name: Architecture Check
description: This skill should be used for quick inline architecture validation during coding. Use when the user asks "is this the right pattern?", "should this be async?", "does this follow BasePlaneFacade?", or similar quick architecture questions. For deep analysis, recommend the brain-software-arch-expert agent instead.
version: 0.1.0
---

# Quick Architecture Check for brain-mimc

This skill provides quick inline architecture validation during coding. Use it for fast "is this correct?" checks.

## When to Use This Skill

- Quick "is this good architecture?" checks
- Pattern verification (BasePlaneFacade, contracts-first, etc.)
- Validate single implementation decision
- Immediate answer needed

## When to Use the Agent Instead

If the question requires:
- Deep analysis of multiple files
- Full codebase audit
- Stress-testing an idea
- Implementation planning

Recommend: "This requires deeper analysis. Use the `brain-software-arch-expert` agent instead."

## Quick Check Process

1. Read the relevant code section
2. Check against brain-mimc patterns
3. Provide immediate answer with reasoning
4. Flag if deeper analysis is needed

## Brain-mimc Patterns to Check

| Pattern | Quick Check |
|---------|-------------|
| **BasePlaneFacade** | Does the plane inherit from BasePlaneFacade? |
| **Contracts-first** | Is there a Protocol class for this implementation? |
| **Frozen dataclasses** | Is the message type using `@dataclass(frozen=True)`? |
| **Raw never goes up** | Is data being transformed before ascending? |
| **Drivers vs Modulators** | Is driver changing gate state? (violation) |
| **Scope-based** | Is the component properly scoped? |
| **Idempotency** | Does the command use action_id? |
| **No blocking in async** | Any `time.sleep()` or sync calls in async? |
| **Component isolation** | Can this run standalone with mocked I/O? |

## Communication Lanes Quick Reference

| Lane | Direction | Quick Check |
|------|-----------|-------------|
| A (DRIVER) | Ascending | Is it going up? Transformed at each level? |
| B (MODULATOR) | Cortex -> Thalamus | Feedback direction correct? |
| C (COMMAND) | Descending | Going down only? |
| D (GLOBAL) | Broadcast | Is this truly global? |
| E (ERROR) | Learning | Proper error routing? |
| G (GATE) | Control-plane | Is this control, not data? |
| X (REFLECTION) | Non-blocking | Not blocking primary flow? |

## Response Format

For quick checks, respond with:

```
## /arch-check Result

**Pattern:** [Pattern being checked]
**Status:** [PASS / FAIL / NEEDS REVIEW]
**Reason:** [Brief explanation]
**Fix:** [If FAIL, how to fix]
```

If deeper analysis is needed:
```
## /arch-check Result

**Status:** NEEDS DEEPER ANALYSIS
**Reason:** [Why this can't be answered quickly]
**Recommendation:** Use `brain-software-arch-expert` agent for full analysis
```

## Examples

### Example 1: Checking BasePlaneFacade

User: `/arch-check Does this follow BasePlaneFacade pattern?`

```
## /arch-check Result

**Pattern:** BasePlaneFacade
**Status:** FAIL
**Reason:** Class does not inherit from BasePlaneFacade, missing ingress validation
**Fix:** Inherit from BasePlaneFacade and implement dispatch() method
```

### Example 2: Checking Lane Usage

User: `/arch-check Which lane should this message use?`

```
## /arch-check Result

**Pattern:** Lane Assignment
**Status:** PASS - Should use Lane A (DRIVER)
**Reason:** This is content data ascending from spinal cord to brainstem
**Fix:** N/A
```

### Example 3: Needs Deeper Analysis

User: `/arch-check Is this architecture correct for the thalamus nucleus routing?`

```
## /arch-check Result

**Status:** NEEDS DEEPER ANALYSIS
**Reason:** Thalamus nucleus routing involves multiple patterns and cross-references
**Recommendation:** Use `brain-software-arch-expert` agent for full analysis
```
