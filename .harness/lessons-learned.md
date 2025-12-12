# Harness Project - Lessons Learned

> **TL;DR:** Document this file's lessons into the methodology itself. These are real failures we experienced.

---

## Lesson #1: Sub-Agent Output Must Be Written Immediately

**Date:** 2025-12-10 (Session 1)
**Severity:** 🔴 CRITICAL
**Category:** Data Loss Prevention

### What Happened
- Sub-agent performed Lean methodology research
- Returned 23 high-quality patterns to orchestrator
- Orchestrator discussed the results but **never wrote them to a file**
- At 83% context, user asked "what would a fresh session be missing?"
- Realized the Lean data existed ONLY in context and would be **permanently lost**

### Root Cause
- Sub-agent returned data TO orchestrator instead of writing directly to file
- Orchestrator treated sub-agent output as "discussion material" not "artifact to persist"
- No checkpoint/validation step asking "did we save this?"

### The Fix (For Harness Methodology)
```
SUB-AGENT OUTPUT RULE:
1. Sub-agents MUST write research output directly to files
2. Sub-agents return CONFIRMATION of what was written, not the data itself
3. Orchestrator NEVER holds research data - only references to where it's stored
4. After any sub-agent task: verify file exists before proceeding
```

### Sub-Agent Prompt Template (Corrected)
```markdown
You are a research sub-agent. Your task is to [SPECIFIC TASK].

CRITICAL INSTRUCTIONS:
1. DO NOT return data to orchestrator
2. WRITE output directly to: [EXPLICIT FILE PATH]
3. Return ONLY: confirmation of file written + brief summary (3-5 bullets)

OUTPUT FORMAT in file:
[Explicit structure specification]

AFTER WRITING:
Report back: "Written [N] items to [path]. Summary: [3-5 bullets]"
```

---

## Lesson #2: State Documentation ≠ Context Recovery

**Date:** 2025-12-10 (Session 1)
**Severity:** 🟡 MEDIUM
**Category:** Documentation Completeness

### What Happened
- Created project-state.yaml with decisions, learnings, next actions
- Felt confident we had "documented everything"
- User asked: "what would a fresh session be missing?"
- Realized state doc captured WHAT but not WHY

### What Was Missing
| Had | Missing |
|-----|---------|
| "Project named Harness" | WHY - the horse/civilization analogy, channeling power |
| "6 decisions made" | The CONTEXT that led to those decisions |
| "Research phase next" | WHICH methodologies? How many? Scope? |
| "Sub-agents validated" | The actual TEMPLATE that worked |

### Root Cause
- Documented outcomes, not reasoning
- Assumed context would persist (it won't)
- No "explain to a stranger" test

### The Fix (For Harness Methodology)
```
DOCUMENTATION COMPLETENESS TEST:
Before ending any session, ask:
"If a completely fresh AI read only our files, could it:
1. Understand WHY we're doing this? (Vision)
2. Know WHAT to do next? (Actions)
3. Have the TOOLS to do it? (Templates, schemas)
4. Access ALL generated artifacts? (Data)

If any answer is NO → document before ending.
```

---

## Lesson #3: "Documented Everything" is a Dangerous Assumption

**Date:** 2025-12-10 (Session 1)
**Severity:** 🔴 CRITICAL
**Category:** Process Gap

### What Happened
- Felt productive - created working agreement, decision log, state file
- Committed and pushed to GitHub
- Ready to end session feeling accomplished
- User's question revealed we had 6 gaps including LOST DATA

### Root Cause
- Documentation happened organically during discussion
- No systematic checkpoint asking "what exists only in context?"
- Confirmation bias: "we wrote a lot, so we must have captured everything"

### The Fix (For Harness Methodology)
```
END-OF-SESSION CHECKLIST (Mandatory):
□ All sub-agent outputs written to files (not just returned)?
□ Vision/purpose documented (not just decisions)?
□ Next session has explicit actions AND the resources to do them?
□ Research data persisted (not in context)?
□ Templates/schemas saved as reusable artifacts?
□ "Fresh AI test" passed?

Only AFTER all boxes checked → commit and end session
```

---

## Lesson #4: Emergency Captures Are a Smell

**Date:** 2025-12-10 (Session 1)
**Severity:** 🟡 MEDIUM
**Category:** Process Design

### What Happened
- Created `.harness/emergency-captures/` folder to save Lean data reactively
- This worked, but indicates a process failure

### The Insight
> "If you need an emergency folder, your normal process is broken."

Emergency captures mean:
- Something should have been captured proactively
- The process has gaps
- We're reacting instead of preventing

### The Fix (For Harness Methodology)
```
DESIGN PRINCIPLE:
The process should make data loss IMPOSSIBLE, not recoverable.

- Sub-agents write directly → data persists immediately
- Checkpoints validate files exist → gaps caught early
- End-of-session checklist → nothing left in context only

Emergency captures folder exists for edge cases,
but needing it should trigger process review.
```

---

## How These Lessons Apply to Harness

These aren't just project lessons - they're **methodology requirements**:

1. **Harness must enforce sub-agent file writes** - not optional
2. **Harness must include context recovery protocols** - not assumed
3. **Harness must have end-of-session validation** - mandatory checklist
4. **Harness should make data loss structurally impossible** - by design

The fact that WE experienced these failures while BUILDING a methodology to prevent AI failures is itself valuable data.

---

## Lesson #5: Task Lists are Append-Only

**Date:** 2025-12-13 (Session 8)
**Severity:** 🔴 CRITICAL
**Category:** Data Loss Prevention

### What Happened
- Updating `next_session_actions` in project-state.yaml
- Made "judgment calls" about what was "replaced" vs "subsumed"
- Removed items without explicit instruction
- User caught it: "why is anything removed? this is very dangerous"

### What Was Lost (Temporarily)
- "Prototype visualization (Q3 - mind map from atoms)"
- "Build first workflow skill (capturing-decisions)"
- Several other items "merged" into new items

### Root Cause
- Assumed I could "clean up" the list
- Made unilateral decisions about what was redundant
- Treated task list as editable document, not immutable log

### The Fix (For Harness Methodology)
```
TASK LIST RULES:
1. ONLY ADD new items
2. Mark completed as DONE (don't delete)
3. Mark obsolete as OBSOLETE with reason (don't delete)
4. NEVER remove without explicit "remove X" instruction
5. Task lists are append-only logs, like decision-log.md

WHY:
- Items represent commitments or intentions
- "Subsumed" is a judgment call that may be wrong
- History matters - even obsolete tasks show what was considered
- User should decide what's removed, not AI
```

### The Pattern
This is the same as Lesson #1 (Sub-Agent Output) and Lesson #3 ("Documented Everything"):
> **When in doubt, preserve. Deletion is irreversible.**

---

---

## Lesson #6: Session End is Unreliable; Enforce at Session Start

**Date:** 2025-12-13 (Session 11)
**Severity:** 🟡 MEDIUM
**Category:** Process Design / Git Hygiene

### What Happened
- Opened new Claude Code session expecting latest code
- Branch `gifted-volhard` was created from `main`
- But `main` was stale — previous session's work on `crazy-jones` was never merged
- Result: new session missing 2 commits (including D18 rename of vision.md)
- Spent time debugging "why is vision.md still here?"

### Root Cause
- Previous session ended without merging to main
- Sessions end unpredictably: terminal close, timeout, user leaves, new session elsewhere
- **There is no reliable "session end" event** — Claude Code has no SessionEnd hook
- New worktrees branch from `main`, inheriting stale state

### The Insight
```
Session END = unreliable (no hook, user may vanish)
Session START = reliable (hook fires, Claude present)

∴ All enforcement happens at START, not END
```

### The Fix (For Harness Methodology)
```
GIT HYGIENE ENFORCEMENT:

1. SESSION START (reliable):
   - SessionStart hook detects unmerged branches
   - Shows prominent warning if current branch is behind
   - Claude prompts: "Shall I merge X to main first?"
   - User agrees → auto-merge (fast-forward only)

2. SESSION END (best-effort via tool call hooks):
   - PostToolUse hook can fire on patterns (e.g., after git commit)
   - Prompt cleanup when activity suggests winding down
   - BUT: cannot rely on this — user may just close terminal

3. MECHANISM: Tool call hooks (PreToolUse, PostToolUse)
   - Fire on every tool invocation
   - Can pattern-match to trigger at appropriate moments
   - Not a "session end" event, but can approximate it
```

### Implementation Status
- [x] Session start warning added to `session-recovery.py`
- [ ] "Agree then action" prompt flow (Claude interprets hook output)
- [ ] Tool call hook for session-end cleanup (best-effort)
- [ ] Document in capture-protocol.md

### The Pattern
> **If you can't guarantee an event fires, move enforcement to an event that does.**

Session start is guaranteed. Session end is not. Design accordingly.

---

*First captured: 2025-12-10*
*Updated: 2025-12-13 (Lesson #6)*
*These lessons should inform the Harness methodology design.*
