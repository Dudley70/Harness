# Harness Project - Working Agreement

---
title: Working Agreement
status: draft
owner: Team
created: 2025-12-10
updated: 2025-12-10
phase: governance
summary: Defines how the Harness team works, validated through empirical testing on 2025-12-10.
---

## Vision & Principles

> See **[vision.md](./vision.md)** for project vision, purpose, and core principles.

This working agreement focuses on HOW we work, not WHY we're building (that's vision.md's job).

## Working Principles

These are operational principles for how we execute work:

### 1. Research Before Conclusions
- Document **hypotheses**, not conclusions, until research validates them
- Remain flexible to whatever structure emerges from findings

### 2. Context-Loss Resilience
- Any team member (human or AI) should be able to resume from documents alone
- Critical state lives in `.harness/` - always load this first
- **Assume context loss can happen at any time**

### 3. Progressive Disclosure (Document Structure)
- **Layer 0 - Context Anchors:** ~200-300 tokens each, ALWAYS loaded
- **Layer 1 - Summaries:** ~500-800 tokens, loaded when entering topic
- **Layer 2 - Details:** Full content, loaded ONLY when specifically needed

### 4. Single Source of Truth
- Each concept has ONE authoritative document
- Other documents REFERENCE, don't duplicate
- Contradictions are resolved immediately when discovered

---

## Validated Learnings (Empirically Tested 2025-12-10)

### Sub-Agent Capabilities

| Capability | Status | Evidence |
|------------|--------|----------|
| Sub-agents can write files directly | ✅ CONFIRMED | Created test-subagent-write.md successfully |
| Sub-agents can perform web search | ✅ CONFIRMED | Lean methodology research returned 12 valid URLs |
| Explicit format instructions work | ✅ CONFIRMED | Requested 10-15 patterns, received 23 in exact table format |
| Focused scope improves quality | ✅ CONFIRMED | Single methodology = high quality vs all methodologies = thin |

### Sub-Agent Protocol

**WHEN TO SPAWN:**
- Research tasks requiring external sources
- Analysis requiring significant reference material
- Any task that would pollute orchestrator context
- Heavy work that should write directly to files

**HOW TO PROMPT:**
```markdown
You are a research sub-agent. Your task is to [SPECIFIC TASK].

CRITICAL INSTRUCTIONS:
1. DO NOT return data to orchestrator
2. WRITE output directly to: [EXPLICIT FILE PATH]
3. Return ONLY: confirmation of file written + brief summary (3-5 bullets)

OUTPUT FORMAT in file:
[Explicit structure specification - tables, lists, etc.]

AFTER WRITING:
Report back: "Written [N] items to [path]. Summary: [3-5 bullets]"
```

**KEY PRINCIPLES:**
- ONE focused topic per sub-agent
- Explicit output format prevents summarization
- Minimum deliverable targets set expectations
- Sub-agents write to files; orchestrator stays lean
- Orchestrator NEVER holds research data - only references to where it's stored

### Sub-Agent Architecture (Validated Session 1)

**Why Sub-Agents Summarize by Default:**
- Sub-agents are optimized to compress output for context return
- Without explicit instructions, they synthesize rather than extract
- "Return raw data" vs "return findings" produces different outputs

**What Works (Empirically Tested):**
| Instruction | Result |
|-------------|--------|
| "Extract 10-15 patterns" | Got 23 patterns (exceeded target) |
| "TABLE FORMAT ONLY" | Clean structured output |
| "DO NOT summarize" | Raw data, not synthesis |
| "Write directly to file" | Data persists, orchestrator stays lean |

**Claude Code vs Claude Desktop:**
| Aspect | Claude Desktop | Claude Code |
|--------|----------------|-------------|
| Research tool | `launch_extended_search_task` | `Task` tool |
| Artifact creation | Optional parameter | Orchestrator writes files |
| File handling | Can create artifacts | Sub-agent writes OR returns |
| Web search | Built into research task | Sub-agent uses WebSearch |

**The pattern holds across both:** Explicit format instructions + focused scope = quality output

### Context Management

| Finding | Detail | Source |
|---------|--------|--------|
| Auto-compact threshold varies | 65-99% depending on platform | GitHub issues |
| VS Code triggers earlier | ~65-75% full | User reports |
| CLI triggers later | ~95-99% full | User reports |
| Quality degrades before compaction | ~75% is practical limit | User experience |
| Manual compact > auto-compact | Proactive beats reactive | User consensus |

### Context Window Awareness (Validated 2025-12-10)

| Finding | Detail | Source |
|---------|--------|--------|
| **`/context` command available** | Shows full breakdown - USE THIS | Empirical test |
| `<system_warning>` exists for Sonnet 4.5 | Sonnet can self-report remaining tokens | Empirical test |
| Opus 4.5 cannot self-monitor | No `<system_warning>` visibility | Empirical test |
| Autocompact buffer = 22.5% | Reserved space, not usable | `/context` output |
| MCP tools overhead = ~15% | Fixed cost before work begins | `/context` output |
| "Context anxiety" in models | Models take shortcuts near limits | Cognition/Devin blog |

**Context Budget Reality (from /context):**
```
Total:              200k tokens (100%)
├── Overhead:       ~48k tokens (~24%) - system prompt, tools, MCP
├── Autocompact:    ~45k tokens (~22.5%) - RESERVED, can't use
└── Usable:         ~107k tokens (~53.5%) - actual working space
```

**Revised Context Zones:**
```
0-50%:    GREEN  - Normal operation
50-65%:   YELLOW - Consider wrapping up, check /context
65-77%:   ORANGE - Complete task, document, prepare handoff
77%+:     RED    - Approaching autocompact buffer, stop new work
```

**User Protocol:**
- Run `/context` periodically to check usage
- Watch "Messages" growth - that's the conversation content
- Sonnet 4.5 sub-agents can report their own context if needed

**Defensive Practices:**
1. Short sessions by design - don't let context accumulate
2. Sub-agents for heavy work - keep orchestrator lean
3. Frequent manual checkpoints - document state proactively
4. PreCompact hook as last resort - emergency state save

---

## Session Protocol

### Starting a Session
1. Load `.harness/project-state.yaml` - understand current state
2. Load `.harness/context-anchors/` - critical context that must persist
3. Review recent entries in `.harness/decision-log.md`
4. Check todo list for in-progress work

### During a Session
- Update project-state after each significant task
- Use sub-agents for research/heavy lifting
- Keep orchestrator context lean
- Document decisions as they're made

### Ending a Session
1. Update `.harness/project-state.yaml` with current state
2. Log any decisions made to `.harness/decision-log.md`
3. Create handoff notes if work is incomplete
4. Commit all changes with descriptive message

### On Context Loss / New Session
1. Read this working agreement first
2. Follow "Starting a Session" protocol
3. Do NOT proceed with work until context is re-established

---

## Document Standards

### File Naming
```
[category]-[topic].md
Examples:
methodology-lean.md
synthesis-patterns.md
```

### Required Frontmatter
```yaml
---
title: [Clear descriptive title]
status: draft | review | approved
owner: [Responsible party]
created: YYYY-MM-DD
updated: YYYY-MM-DD
phase: governance | research | design | build
summary: [2-3 sentence summary - enough for Layer 0/1 decisions]
dependencies: [list of related documents]
---
```

### Document Structure (Progressive Disclosure)
```markdown
# Title
> **TL;DR:** [One sentence - the absolute essence]

## Summary
[3-5 bullets - enough to make decisions without reading further]

## Details
[Full content - only read if Summary insufficient]

## References
[Links to supporting documents]
```

---

## Decision Gates

| Gate | Name | Entry Criteria | Exit Criteria |
|------|------|----------------|---------------|
| G0 | **Initiation** | Vision aligned, team committed | Working agreement approved, structure created, research plan ready |
| G1 | **Research Complete** | All planned methodologies analyzed | Synthesis document approved, patterns identified, hypotheses formed |
| G2 | **Design Complete** | Research synthesis approved | Architecture specified, no contradictions, reviewed |
| G3 | **Build Ready** | Design specifications locked | Implementation plan approved, success criteria defined |

---

## Prioritization

### For Features/Capabilities (MoSCoW)
- **Must** - Required for the methodology to function
- **Should** - Important but not critical
- **Could** - Nice to have if time permits
- **Won't** - Explicitly out of scope (for now)

### For Tasks
- **P0** - Blocking other work, do immediately
- **P1** - Important, do this session
- **P2** - Do when P0/P1 complete
- **P3** - Backlog

---

## Open Questions (To Be Resolved)

- [x] Context window warning mechanisms - RESOLVED: exists but not visible in output
- [x] Capture Protocol - RESOLVED: see `00-governance/capture-protocol.md`
- [ ] Pattern Extraction Schema - define before research phase
- [ ] PreCompact hook configuration - specific implementation for Harness
- [ ] Optimal session length - to be determined through practice

---

## Related Documents

- **Capture Protocol:** `00-governance/capture-protocol.md` - How we capture and document
- **Vision:** `00-governance/vision.md` - Why we're building Harness
- **Decision Log:** `.harness/decision-log.md` - All decisions with rationale
- **Lessons Learned:** `.harness/lessons-learned.md` - Failures and fixes

---

## Amendment Process

This working agreement can be amended by:
1. Proposing change in `.harness/decision-log.md`
2. Documenting rationale and evidence
3. Updating this document
4. Noting the change in decision log

---

*Agreement established: 2025-12-10*
*Last reviewed: 2025-12-10*
*Status: DRAFT - Context warning info added, pending schema and hook setup*
