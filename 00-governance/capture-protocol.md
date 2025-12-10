# Harness Capture & Documentation Protocol

> **TL;DR:** Context is ephemeral. Documents are memory. Capture is not optional - it's the foundation of AI-assisted work.

---
title: Capture & Documentation Protocol
status: draft
owner: Team
created: 2025-12-10
updated: 2025-12-10
phase: governance
summary: Defines how insights, decisions, and learnings are captured and documented to survive context loss.
---

## Core Principle

**If documentation is the only memory, capture is ESSENTIAL.**

- AI context windows compress, compact, or reset
- Human memory fades and biases
- Only persistent documentation survives
- HOW we document determines WHAT survives

---

## The Three Phases of Capture

### Phase 1: Continuous Capture (During Session)

Capture happens IN REAL-TIME, not retrospectively.

| What | Where | When | Who |
|------|-------|------|-----|
| Key decisions | `.harness/decision-log.md` | As decided | Orchestrator |
| Lessons/failures | `.harness/lessons-learned.md` | Immediately | Orchestrator |
| Sub-agent research | `01-research/[topic].md` | Sub-agent writes directly | Sub-agent |
| State changes | `.harness/project-state.yaml` | After each milestone | Orchestrator |

**Critical Rule:** Sub-agents write directly to files. They return CONFIRMATION, not data.

```markdown
SUB-AGENT PROTOCOL:
1. Sub-agent performs research/analysis
2. Sub-agent WRITES output to specified file
3. Sub-agent returns: "Written [N] items to [path]. Summary: [3-5 bullets]"
4. Orchestrator NEVER holds research data - only references
```

### Phase 2: Session Boundary (Before Ending)

Run the END-OF-SESSION CHECKLIST before ANY session ends.

```markdown
## End-of-Session Checklist

□ All sub-agent outputs written to files?
□ Decisions logged with rationale?
□ Lessons/failures captured immediately?
□ Vision/purpose still documented? (not just state)
□ Next session has explicit actions AND resources to do them?
□ Research data persisted? (not in context only)
□ Transcript exported? (user copies to .harness/transcripts/[session].md)

FRESH AI TEST:
□ Could a new session understand WHY we're doing this?
□ Could a new session DO the next steps from docs alone?

Only AFTER all boxes checked → git commit and end session
```

### Phase 3: Post-Session Recovery (Next Session Start)

Every new session begins with recovery verification.

```markdown
## Session Start Protocol

1. Load .harness/project-state.yaml FIRST
2. Review recent decision-log.md entries
3. Check lessons-learned.md for relevant learnings
4. If gaps found → mine transcript for undocumented insights
5. Run /context to check starting budget
6. Continue with documented next actions
```

---

## Transcript Management

### Why Keep Transcripts

- Transcripts contain ~7x more information than our documents (162KB vs 23KB in session 1)
- Rich discussion context survives for recovery
- Evidence for decisions can be traced
- Gaps can be identified by comparing transcript to docs

### Where Transcripts Live

```
.harness/transcripts/
├── session1-transcript.md    # Full conversation export
├── session2-transcript.md
└── ...
```

### How to Export (User Action Required)

Claude Code sessions persist to `~/.claude/projects/[project]/[session-id].jsonl`

**To export readable transcript:**
1. Open session in Claude Desktop (shows full history)
2. Copy conversation
3. Paste into Google Docs or text editor
4. Export as .md
5. Save to `.harness/transcripts/sessionN-transcript.md`

**Alternative:** Use jsonl directly (machine-readable, includes tool calls)

### Transcript Mining Protocol

When a new session identifies documentation gaps:

```markdown
## Transcript Recovery Process

1. Identify gap: "What's missing that a fresh session would need?"
2. Search transcript: grep for keywords related to gap
3. Extract insight: Pull relevant discussion sections
4. Document: Add to appropriate file (vision, working-agreement, lessons-learned)
5. Cite: Note "Recovered from session N transcript"
```

---

## Documentation Standards

### The HOW of Documentation

| Principle | Implementation | Why |
|-----------|----------------|-----|
| **Progressive Disclosure** | TL;DR → Summary → Details | Load only what's needed |
| **One Topic, One File** | Split large docs | Focused context loading |
| **Source of Truth** | No duplication | Contradictions kill AI |
| **Actionable** | Next steps explicit | AI can execute |
| **Traceable** | Link to evidence | Decisions can be verified |

### Document Structure Template

```markdown
# [Topic Title]

> **TL;DR:** [One sentence - the absolute essence]

---
title: [Title]
status: draft | review | approved
owner: [Who]
created: YYYY-MM-DD
updated: YYYY-MM-DD
phase: governance | research | design | build
summary: [2-3 sentences for index/search]
---

## Summary
[3-5 bullets - enough to make decisions without reading further]

## Details
[Full content - only read if Summary insufficient]

## References
[Links to supporting documents, transcripts, evidence]
```

### Token Budgets (Guidance)

| Document Type | Target Size | Purpose |
|---------------|-------------|---------|
| Context anchors | 200-300 tokens | ALWAYS loaded |
| Topic summaries | 500-800 tokens | Loaded when entering topic |
| Detail documents | 2000-4000 tokens | Loaded only when needed |
| Transcripts | Unlimited | Archive, not loaded |

---

## Quality Gates

### Document Quality Criteria

Before a document is considered complete:

- [ ] Has TL;DR that captures essence
- [ ] Summary is self-sufficient for 80% of use cases
- [ ] Sources/evidence cited for claims
- [ ] No duplication with other docs (links instead)
- [ ] Next actions clear if applicable
- [ ] Reviewed by different perspective (human or AI agent)

### Capture Quality Metrics

Track these to improve capture effectiveness:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Gap rate | <10% | Transcript items not in docs |
| Recovery time | <5 min | Time to context from cold start |
| Fresh AI success | 100% | Can new session execute from docs? |
| Data loss incidents | 0 | Sub-agent data lost to context |

---

## Anti-Patterns

### What NOT to Document

- Exploratory dead-ends (unless they teach something)
- Verbose discussions that led to simple conclusion (document conclusion only)
- Duplicate information (link instead)
- Process mechanics that won't be referenced
- Speculation without evidence

### Test Before Documenting

> "Will a future session NEED this specific information to make decisions or take action?"

If NO → Don't document
If YES → Document with appropriate detail level

---

## Emergency Procedures

### Data at Risk (Pre-Compaction)

If context is high (>65%) and undocumented data exists:

1. STOP new work
2. Identify what's only in context
3. Write to `.harness/emergency-captures/[description].md`
4. Note in lessons-learned.md that emergency capture occurred
5. Review process for why this happened

### Post-Compaction Recovery

If compaction occurs before capture:

1. Check if transcript exists (`.claude/projects/` or exported)
2. Mine transcript for lost insights
3. Document what was recovered
4. Add to lessons-learned.md
5. Improve capture process to prevent recurrence

---

## Integration with Harness Methodology

This protocol is not separate from Harness - it IS Harness.

The methodology only works if:
- Context loss doesn't derail projects
- Fresh AI sessions can execute from docs alone
- 24+ hour autonomous operation is possible

**Capture makes this possible.**

---

*Protocol established: 2025-12-10 (Session 2)*
*Based on learnings from Session 1 data loss incident*
