# Document Lifecycle States

Each content type has defined lifecycle states. Content transitions between states but is never deleted.

## Tasks (project-state.yaml → next_session_actions)

```
┌─────────┐
│   NEW   │  "P0: Build feature X"
└────┬────┘
     │
     ▼
┌─────────┐
│ ACTIVE  │  (being worked on - no prefix change)
└────┬────┘
     │
     ├──────────────┬──────────────┐
     ▼              ▼              ▼
┌─────────┐  ┌───────────┐  ┌─────────┐
│  DONE   │  │ OBSOLETE  │  │ PARKED  │
└─────────┘  └───────────┘  └─────────┘
```

**Transitions:**
| From | To | When | Format |
|------|----|------|--------|
| NEW | DONE | Task completed | `"DONE: Build feature X (Session 8)"` |
| NEW | OBSOLETE | No longer needed | `"OBSOLETE: Build feature X (superseded by Y)"` |
| NEW | PARKED | Deferred | `"PARKED: Build feature X (blocked by Z)"` |
| PARKED | NEW | Resume work | Remove PARKED prefix |

---

## Decisions (decision-log.md)

```
┌─────────────┐
│   DRAFTED   │  Written during session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  APPROVED   │  Status: Approved
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ IMPLEMENTED │  Status: Implemented
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ SUPERSEDED  │  New decision references this one
└─────────────┘
```

**Rules:**
- Decisions are **append-only** - never edit existing decisions
- To change a decision: Add NEW decision that references and supersedes old
- Add `**Supersedes:** D12` to new decision
- Add `**Status:** Superseded by D15` to old decision

---

## Lessons (lessons-learned.md)

```
┌────────────┐
│  CAPTURED  │  Lesson documented
└─────┬──────┘
      │
      ▼
┌────────────┐
│  EMBEDDED  │  Incorporated into methodology/tooling
└────────────┘
```

**Rules:**
- Lessons are permanent record
- Once captured, never deleted
- Can add "Embedded in: D16" note when lesson becomes part of system

---

## Ideas (ideas.yaml)

```
┌──────────┐
│ CAPTURED │  Initial capture
└────┬─────┘
     │
     ▼
┌────────────┐
│ EXPLORING  │  Being investigated
└─────┬──────┘
      │
      ├────────────┬─────────────┬────────────┐
      ▼            ▼             ▼            ▼
┌──────────┐ ┌───────────┐ ┌─────────┐ ┌─────────┐
│ PROMOTED │ │ ABANDONED │ │ MERGED  │ │ PARKED  │
└──────────┘ └───────────┘ └─────────┘ └─────────┘
```

**Format in ideas.yaml:**
```yaml
ideas:
  context_compression:
    status: exploring
    captured: 2025-12-10
    description: "..."

  # After promotion:
  context_compression:
    status: promoted
    captured: 2025-12-10
    promoted_to: "D14"
    description: "..."
```

---

## Questions (questions.yaml)

```
┌────────┐
│  OPEN  │  Question captured
└───┬────┘
    │
    ▼
┌────────────┐
│ EXPLORING  │  Being investigated
└─────┬──────┘
      │
      ├─────────────┬─────────────┬────────────┐
      ▼             ▼             ▼            ▼
┌──────────┐  ┌──────────┐  ┌─────────┐ ┌─────────┐
│ ANSWERED │  │ PROMOTED │  │ PARKED  │ │ INVALID │
└──────────┘  └──────────┘  └─────────┘ └─────────┘
```

**Format in questions.yaml:**
```yaml
questions:
  Q6:
    status: answered
    question: "What's the unified architecture?"
    answer: "Skills - see D14"
    answered_in: "Session 7"
```

---

## Patterns (patterns-and-ideas.md)

```
┌────────────┐
│  OBSERVED  │  Pattern noticed
└─────┬──────┘
      │
      ▼
┌────────────┐
│ DOCUMENTED │  Written up with examples
└─────┬──────┘
      │
      ▼
┌────────────┐
│  EMBEDDED  │  Built into tooling/methodology
└────────────┘
```

**Rules:**
- Patterns accumulate, never deleted
- Can mark as `[EMBEDDED]` when built into system
- Can mark as `[SUPERSEDED by X]` if better pattern found

---

## Atoms (atoms.jsonl)

```
┌───────────┐
│ EXTRACTED │  One-time extraction from transcript
└───────────┘
     │
     X  (no transitions - atoms are immutable)
```

**Rules:**
- Atoms are **immutable** - never modify
- Wrong atom? Extract new, corrected atom
- Atoms are facts about what happened, not editable records
