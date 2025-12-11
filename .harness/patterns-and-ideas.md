# Harness Patterns & Ideas

> Capture interesting patterns, ideas, and techniques discovered during research.
> These may inform future design decisions.

---

## Quick Reference

| Pattern | One-liner | Source |
|---------|-----------|--------|
| helpers.md | Centralize shared ops, reference via anchors | bmad-skills |
| Level-based methodology | Right-size process for project complexity | bmad-skills |
| 7-step init ritual | Consistent session start via filesystem discovery | Anthropic |
| Immutable task lists | JSON state, only flip pass/fail, never delete | Anthropic |
| Three-layer state | JSON (structured) + MD (unstructured) + Git (history) | Anthropic |
| Fresh windows > compaction | Filesystem discovery beats lossy compression | Anthropic |
| Two-agent pattern | Initializer plans, Coding Agent executes | Anthropic |
| Skills progressive disclosure | SKILL.md first, supporting files on-demand | Claude Code |

---

## Historical Learnings (Sessions 1-3)

> TODO: Consolidate from project-state.yaml sessions 1-3

---

## Session 4 Discoveries (2025-12-11)

### Pattern: helpers.md with Section References

**Source:** claude-code-bmad-skills repo

Instead of embedding instructions in every skill/command, centralize in `helpers.md` and reference via anchors:

```markdown
"Follow helper instructions in utils/helpers.md#Load-Global-Config"
"Execute Step 1-3 from helpers.md#Combined-Config-Load"
```

**Benefits:**
- 70-85% token reduction vs embedded approach
- Single source of truth for shared operations
- Claude loads only referenced sections

**Harness Application:** Create `harness/helpers.md` for shared operations (config loading, state management, git operations).

---

### Pattern: Level-Based Methodology

**Source:** claude-code-bmad-skills repo

Right-size methodology based on project complexity:

```
Level 0 (1 story):      Minimal docs, tech-spec only
Level 1 (1-10 stories): Light docs, tech-spec required
Level 2 (5-15 stories): Full docs, architecture required
Level 3 (12-40 stories): Full docs, architecture required
Level 4 (40+ stories):  Full docs, comprehensive architecture
```

**Benefits:**
- Prevents over-engineering small projects
- Ensures adequate planning for large projects
- Auto-adjusts workflow recommendations

**Harness Application:** Implement project leveling in skill routing logic.

---

### Pattern: 7-Step Initialization Ritual

**Source:** Anthropic autonomous-coding quickstart

Every session starts with explicit discovery:

```
1. pwd                    → Know where you are
2. ls                     → See project files
3. Read state file        → Current status
4. Read task list         → What's done/pending
5. Read progress notes    → Recent activity
6. Check git history      → Recent commits
7. Run baseline test      → Verify nothing broke
```

**Benefits:**
- Consistent session start
- Filesystem discovery vs context stuffing
- Catches regressions immediately

**Harness Application:** Encode in SKILL.md as mandatory init sequence.

---

### Pattern: Immutable Task Lists (JSON)

**Source:** Anthropic long-running agents paper

Task lists should be:
- Stored in JSON (less corruption than Markdown/YAML)
- NEVER delete or edit task descriptions
- Only modify "passes" field from false → true

**Benefits:**
- Prevents scope creep
- Clear progress tracking
- Recovery-friendly

**Harness Application:** Use `task-list.json` instead of markdown checklists.

---

### Pattern: Three-Layer State

**Source:** Claude 4 best practices

Combine three state mechanisms:

```
Layer 1: Structured (JSON)   → Tasks, status, metrics
Layer 2: Unstructured (MD)   → Progress notes, decisions, vision
Layer 3: Git                 → History, recovery, checkpoints
```

**Benefits:**
- Right format for right purpose
- JSON for machine state, MD for human context
- Git for history and rollback

**Harness Application:** Skills route to appropriate layer based on query type.

---

### Pattern: Fresh Windows > Compaction

**Source:** Claude 4 best practices

> "Consider a brand new context window rather than using compaction. Claude 4.5 models are extremely effective at discovering state from the local filesystem."

**Benefits:**
- No lossy compression
- Clean context
- Filesystem discovery is reliable

**Harness Application:** Already decided (D-previous). Recovery hook bridges sessions.

---

### Pattern: Two-Agent Architecture

**Source:** Anthropic long-running agents paper

Separate concerns:
- **Initializer Agent:** Plans, creates structure, establishes guardrails
- **Coding Agent:** Executes incrementally, one feature at a time

**Benefits:**
- Planning doesn't compete with execution for context
- Clear handoff protocol
- Prevents "over-ambition" failure mode

**Harness Application:** Maps to BMAD's Analyst/PM/Architect (plan) vs Dev (execute).

---

### Pattern: Skills Progressive Disclosure

**Source:** Claude Code skills documentation

```
SKILL.md loaded first (minimal)
    ↓
Supporting files loaded on-demand
    ↓
Deep reference docs only when needed
```

**Benefits:**
- Model-invoked (Claude decides when)
- Token efficient
- Native to Claude Code

**Harness Application:** Core of our D12 architecture decision.

---

## Ideas for Future Exploration

### Meta-Skill Library
A single skill that knows how to find and invoke other skills. Like a "tool search tool" but for skills.

### Session Profiles
Detect session "character" from tool usage patterns:
- Heavy edits = Implementation session
- Heavy reads = Research session
- Heavy git = DevOps session

Use profile to adjust behavior/suggestions.

### Verification Tools
Anthropic emphasizes browser automation (Puppeteer) for verification. Could Harness include verification patterns for different project types?

---

## Sources Referenced

1. **Claude Code Skills:** https://code.claude.com/docs/en/skills
2. **Long-Running Agents:** https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
3. **Claude 4 Best Practices:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
4. **Autonomous Coding Quickstart:** https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
5. **Advanced Tool Use:** https://anthropic.com/engineering/advanced-tool-use
6. **BMAD Skills Implementation:** https://github.com/aj-geddes/claude-code-bmad-skills
7. **Superpowers (PRIORITY):** https://github.com/obra/superpowers
   - Complete workflow system for AI coding agents
   - Skills as mandatory workflows (not optional)
   - Subagent coordination, git worktrees, Socratic brainstorming
   - Multi-platform: Claude Code, Codex, OpenCode
   - **TODO: Deep dive next session - highly relevant prior art**

---
