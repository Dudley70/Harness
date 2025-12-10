# Harness Decision Log

> Add new decisions at TOP of the log

---

## Decision #6 - 2025-12-10
**Topic:** Context Monitoring Solution Found
**Decision:** Use `/context` slash command for context visibility; Sonnet 4.5 for self-aware sub-agents
**Rationale:**
- `/context` command provides full breakdown for ALL models
- Shows: used/total tokens, breakdown by component, autocompact buffer
- Autocompact buffer is 22.5% (45k tokens) - reserved, not usable
- MCP tools overhead is ~15% (31k tokens) - fixed cost
- Actual usable context is ~53.5% after overhead and buffer
- Sonnet 4.5 (but not Opus 4.5) can self-report remaining tokens via `<system_warning>`
**Evidence:**
- `/context` output: 106k/200k (53%), with full breakdown
- Sonnet sub-agent successfully reported: "194,180 remaining out of 200,000"
- Opus confirmed: cannot see `<system_warning>` messages
**Practical Zones:**
- 0-50%: GREEN - normal operation
- 50-65%: YELLOW - consider wrapping up
- 65-77%: ORANGE - complete task, document, prepare handoff
- 77%+: RED - approaching autocompact, stop new work
**Status:** Validated

---

## Decision #5 - 2025-12-10
**Topic:** Context Window Awareness Findings
**Decision:** Accept that we cannot self-monitor context usage; rely on defensive practices
**Rationale:**
- `<system_warning>` token tracking EXISTS in Claude (format: `Token usage: X/Y; Z remaining`)
- Feature available in Opus 4.5, Sonnet 4.5, Haiku 4.5
- HOWEVER: Not visible in current session output (empirically tested)
- "Context anxiety" documented: models take shortcuts near limits (Cognition/Devin research)
- User can run `/cost` to check externally
**Evidence:**
- Official Claude docs confirm feature
- Empirical test: ran 2 tool calls, no warning visible in output
- Cognition blog documents behavioral changes near context limits
**Implications:**
- Cannot programmatically self-monitor in current interface
- Defensive strategy validated: short sessions, sub-agents, proactive checkpoints
- Stay well under limits to avoid "context anxiety" shortcuts
**Status:** Validated

---

## Decision #4 - 2025-12-10
**Topic:** Context Management Strategy
**Decision:** Adopt graceful degradation approach rather than relying on auto-compact
**Rationale:**
- Auto-compact thresholds vary wildly (65-99% across platforms)
- Quality degrades before compaction triggers
- Context awareness features exist but not visible in our interface
**Evidence:** Web search results, GitHub issues #6123, #11819, #9964
**Status:** Validated

---

## Decision #3 - 2025-12-10
**Topic:** Sub-Agent Architecture
**Decision:** Sub-agents write files directly; orchestrator stays lean
**Rationale:**
- Empirically tested: sub-agent successfully created test-subagent-write.md
- Lean methodology test: 23 patterns extracted with explicit format instructions
- Keeps orchestrator context available for synthesis, not data storage
**Evidence:** Successful file creation test, Lean research quality
**Status:** Validated

---

## Decision #2 - 2025-12-10
**Topic:** Document Structure
**Decision:** Progressive disclosure with layered documents
**Rationale:**
- Context is precious - every token loaded increases compression risk
- Layer 0 (anchors) → Layer 1 (summaries) → Layer 2 (details)
- Load only what's needed, when needed
**Evidence:** Team discussion, context compression research
**Status:** Approved

---

## Decision #1 - 2025-12-10
**Topic:** Project Name and Vision
**Decision:** Named "Harness" - AI-Native Development Methodology
**Rationale:**
- Horse/civilization analogy: harness channels power, doesn't limit it
- Humans provide controls and constraints to channel AI power
- Not improving BMAD, but creating its successor through first-principles research
**Evidence:** Team consensus during party mode session
**Status:** Approved

---
