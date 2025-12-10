# Harness Decision Log

> Add new decisions at TOP of the log

---

## Decision #11 - 2025-12-11 (Session 3)
**Topic:** BMAD Master as Default Entry Point
**Decision:** BMAD Master is the recommended default agent for all Harness interactions
**Rationale:**
- Master has LIGHTEST context cost (~500 tokens vs ~700-1000 for specialists)
- Acts as recovery coordinator - reads recovery transcripts on startup
- Can route to specialists when deep work is needed
- Party mode orchestration lives here
- Direct specialist access still allowed when task is clear
**Options Considered:**
- Master as Router: dispatch to specialists for all work
- Master as Default + Escalation: handles light work, escalates for depth (CHOSEN)
- Direct Specialist: skip Master entirely
**Implementation:**
- Master checks for recovery files on activation
- Offers `recovery-check` and `deep-recovery` menu options
- Briefs user on session context before presenting menu
**Status:** Approved

---

## Decision #10 - 2025-12-11 (Session 3)
**Topic:** Recovery Handoff Protocol
**Decision:** SessionStart hook stays lightweight; BMAD Master handles full context restoration
**Rationale:**
- Hook executes Python script - ZERO context window cost
- Console output shows ~200-500 tokens (just flags, not full transcript)
- Full transcript sits on disk, read only when needed
- Master reads recovery file and briefs team on activation
- Optional `deep-recovery` for full LLM analysis (user-triggered, higher cost)
**Components:**
1. **Hook (lightweight):** Runs `session-recovery.py`, outputs flags to console
2. **Auto-export:** Transcript with progressive disclosure format
3. **BMAD Master:** Reads recovery file, presents checklist, offers deep analysis
**Progressive Disclosure Format:**
- Level 0: Session Profile (tool stats, character type)
- Level 1: Files Touched (grouped by directory)
- Level 2: Recovery Checklist (prioritized, with checkboxes)
- Level 3: Full Transcript
**Status:** Approved

---

## Decision #9 - 2025-12-10 (Session 2)
**Topic:** Capture Protocol as Core Methodology
**Decision:** Capture and documentation is the FOUNDATION of Harness, not an add-on
**Rationale:**
- "If documentation is the only memory, capture is ESSENTIAL"
- Context is ephemeral - compaction, resets, new sessions lose everything
- HOW we document determines WHAT survives
- Session 1 proved: undocumented insights are LOST insights
**Implementation:**
- Created `00-governance/capture-protocol.md`
- Three phases: Continuous Capture, Session Boundary, Post-Session Recovery
- End-of-Session Checklist is MANDATORY
- Transcript export is standard practice
**Status:** Approved

---

## Decision #8 - 2025-12-10 (Session 2)
**Topic:** End-of-Session Checklist
**Decision:** Mandatory checklist before ending ANY session
**Rationale:**
- Session 1 nearly lost 23 Lean patterns due to no systematic capture check
- "Documented everything" is dangerous assumption
- Checklist forces verification, not assumption
**Checklist Items:**
- [ ] All sub-agent outputs written to files?
- [ ] Decisions logged with rationale?
- [ ] Lessons/failures captured?
- [ ] Next session has explicit actions?
- [ ] Transcript exported?
- [ ] "Fresh AI Test" passed?
**Status:** Approved

---

## Decision #7 - 2025-12-10 (Session 2)
**Topic:** Transcript Capture as Essential Memory
**Decision:** Session transcripts must be captured and stored for recovery
**Rationale:**
- Discovered Claude stores sessions to `~/.claude/projects/[project]/[session].jsonl`
- Session 1 transcript: 166KB of discussion, only ~30% made it to docs
- Transcripts enable gap analysis and recovery of undocumented insights
- JSONL contains tool calls; exported MD contains readable conversation
**Evidence:**
- Session 1 JSONL: 1.19MB total, 128KB human-readable, 397KB tool data
- Gap analysis identified 5+ major undocumented insights
- Successfully recovered Claude Desktop vs Code comparison from transcript
**Storage:** `.harness/transcripts/sessionN-transcript.md`
**Status:** Approved

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
