# Harness Decision Log

> Add new decisions at TOP of the log

---

## Decision #18 - 2025-12-13 (Session 10)
**Topic:** Document Purpose & Audience Requirements
**Decision:** Every document must declare purpose and audience. Kill vision.md - it duplicates CLAUDE.md and lacks clear purpose.

**Status:** Approved

**Core Principle:**
> If you can't define the purpose, the document shouldn't exist.

**Context (Party Mode Discussion):**
- Asked "why do we manually sync vision.md with decisions?"
- Discovered BMAD doesn't have vision.md - it's a workflow step outputting to Product Brief
- Our vision.md was "emergency capture at 102% context" (Session 1) - never designed
- 50% duplicates decision-log principles, 50% is human narrative
- CLAUDE.md already has operational LLM context

**Analysis:**

| vision.md Content | LLM Needs It? | Already In |
|-------------------|---------------|------------|
| Horse/harness analogy | No | - |
| Problem/Opportunity | No | - |
| Success criteria | Maybe | Could be project-state |
| Core Principles | No | CLAUDE.md lines 124-132 |

**Decision:**

1. **Every document must declare metadata:**
   ```yaml
   metadata:
     purpose: "One sentence job description"
     audience: "human | llm | both"
     source_of_truth: "authoritative | derived"
   ```

2. **Kill vision.md:**
   - Archive to `.harness/reference/project-brief.md`
   - Remove all active references
   - Delete sync check from `session-recovery.py`

3. **Rationale:**
   - CLAUDE.md already contains operational LLM context
   - Narrative content is human-interest, not LLM-operational
   - Sync maintenance was overhead with no value
   - Eliminates "SYNC NEEDED" warnings permanently

**Files Affected:**
- `00-governance/vision.md` → DELETE (archive first)
- `CLAUDE.md` → Remove references
- `.claude/skills/harness/SKILL.md` → Remove references
- `.harness/PROJECT-MAP.md` → Remove from map
- `.harness/scripts/session-recovery.py` → Delete `check_decision_sync()`
- `.harness/document-controls.yaml` → Add metadata schema, remove from protected

---

## Decision #17 - 2025-12-13 (Session 8)
**Topic:** Document Structure, Location & Registration Enforcement
**Decision:** Extend document-controls.yaml with location rules and registration requirements. Add PostToolUse hook for real-time validation.

**Status:** Implemented (Session 9)

**Core Principle:**
> Every document has a home. Every home is on the map.

**Problem:**
D16 provides integrity rules (append-only, immutable) but not:
- Location rules (where content types belong)
- Registration enforcement (must be in PROJECT-MAP.md)
- Real-time validation (currently only at commit time)

**Gap Analysis:**

| Have | Don't Have |
|------|------------|
| Integrity rules | Location rules |
| Commit-time validation | Real-time validation |
| Static PROJECT-MAP.md | Registration enforcement |

**Design - Extended Schema:**

```yaml
# document-controls.yaml (additions)

# WHERE content types belong
locations:
  decisions:
    file: .harness/decision-log.md
    format: "## Decision #N"
    description: "All decisions go here, not separate files"

  lessons:
    file: .harness/lessons-learned.md
    format: "## Lesson #N"

  tasks:
    file: .harness/project-state.yaml
    section: next_session_actions
    format: '"P[0-2]:'

  ideas:
    file: .harness/ideas.yaml

  questions:
    file: .harness/questions.yaml

  patterns:
    file: .harness/patterns-and-ideas.md
    format: "## "

  session_summaries:
    file: .harness/project-state.yaml
    section: sessions

  research:
    directory: .harness/research/
    register_in: PROJECT-MAP.md
    description: "Each research topic gets own file"

  transcripts:
    directory: .harness/transcripts/
    auto_generated: true
    register_in: null  # Not required

# WHAT must be registered for discoverability
registration:
  index_file: .harness/PROJECT-MAP.md
  required_for:
    - .harness/*.md
    - .harness/*.yaml
    - 00-governance/*.md
  excludes:
    - .harness/transcripts/*
    - .harness/scripts/*
    - .harness/hooks/*
    - .harness/templates/*
```

**Design - PostToolUse Hook:**

```yaml
# ~/.claude/settings.json (addition)
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      path_pattern: "**/.harness/**|**/00-governance/**"
      command: "python3 .harness/scripts/validate-integrity.py --realtime $FILE"
```

Hook behavior:
1. Triggers on Edit/Write to .harness/ or 00-governance/
2. Runs validation immediately (not waiting for commit)
3. Warns if:
   - Content in wrong location (decision not in decision-log.md)
   - File not registered in PROJECT-MAP.md
   - Append-only content removed

**Design - Validation Enhancements:**

```python
# validate-integrity.py additions

def check_content_location(file_path, content):
    """Warn if content type is in wrong file."""
    # If contains "## Decision #" but not decision-log.md → WARN
    # If contains "## Lesson #" but not lessons-learned.md → WARN

def check_registration(file_path):
    """Warn if file not in PROJECT-MAP.md."""
    # Read PROJECT-MAP.md
    # Check if file_path is mentioned
    # If not → WARN with suggestion to add

def validate_realtime(file_path):
    """Real-time validation for PostToolUse hook."""
    check_append_only(file_path)  # Existing
    check_content_location(file_path)  # New
    check_registration(file_path)  # New
```

**Progressive Disclosure Path:**

```
User asks question
    ↓
CLAUDE.md "Find Things" table
    ↓
PROJECT-MAP.md (lists all documents)
    ↓
document-controls.yaml (locations + rules)
    ↓
Actual file
```

**If file not in PROJECT-MAP.md → Invisible to progressive disclosure**

**Implementation Tasks (Next Session):**

1. Add `locations:` section to document-controls.yaml
2. Add `registration:` section to document-controls.yaml
3. Add `--realtime` mode to validate-integrity.py
4. Add PostToolUse hook to settings.json
5. Add `check_content_location()` function
6. Add `check_registration()` function
7. Update PROJECT-MAP.md with any missing files
8. Test end-to-end

**Validation Layers (Complete):**

```
Layer 1: CLAUDE.md           → Awareness (always loaded)
Layer 2: document-mgmt skill → Operations (model-invoked)
Layer 3: PostToolUse hook    → Real-time warning (NEW)
Layer 4: Pre-commit hook     → Commit-time block
Layer 5: Location rules      → Right place enforcement (NEW)
Layer 6: Registration        → Discoverability enforcement (NEW)
```

**Success Criteria:**
- [ ] Cannot create decision outside decision-log.md without warning
- [ ] Cannot create .harness/ file without PROJECT-MAP.md registration warning
- [ ] Real-time feedback on document integrity violations
- [ ] All documents discoverable via progressive disclosure

---

## Decision #16 - 2025-12-13 (Session 8)
**Topic:** Document Integrity as Core Infrastructure
**Decision:** All Harness files must be registered in `document-controls.yaml` with explicit integrity rules. Validation is config-driven, not hardcoded.

**Core Principle:**
> Files ARE the memory. Memory corruption = system failure.

Harness is built on the principle "documentation IS memory." If files can be silently corrupted, deleted, or have content removed, the entire system fails. Document integrity isn't a feature—it's foundational infrastructure, like ACID guarantees for a database.

**The Problem (Session 8 Discovery):**
- Audited git history: **26 task items silently deleted** across Sessions 4-8
- No one noticed until explicit audit
- AI "cleaned up" lists without asking
- This violates Harness core principle

**Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                 document-controls.yaml                   │
│            (Schema for Harness memory)                   │
├─────────────────────────────────────────────────────────┤
│  append_only:     Files where content cannot be deleted │
│  immutable:       Files that cannot change at all       │
│  protected:       Files that must exist                 │
│  free:            No constraints                        │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              validate-integrity.py                       │
│         (Reads config, enforces rules)                   │
├─────────────────────────────────────────────────────────┤
│  - Pre-commit hook blocks violations                    │
│  - Audit mode scans full history                        │
│  - Warns on unregistered .harness/ files                │
│  - Verifies protected files exist                       │
└─────────────────────────────────────────────────────────┘
```

**Rule Types:**

| Rule | Meaning | Enforcement |
|------|---------|-------------|
| `append_only` | Can add, cannot delete | Block commits removing matching lines |
| `immutable` | Cannot change at all | Block any modification |
| `protected` | Must exist | Warn if missing |
| `free` | No constraints | No validation |

**Config Example:**
```yaml
files:
  append_only:
    .harness/project-state.yaml:
      sections:
        next_session_actions:
          pattern: '"P[0-2]:'
          valid_prefixes: [DONE, OBSOLETE, PARKED]
    .harness/decision-log.md:
      pattern: '^## Decision #\d+'

  immutable:
    .harness/atoms.jsonl: true

  protected:
    - .harness/project-state.yaml
    - CLAUDE.md
```

**Analogy to Database:**

| Database | Harness |
|----------|---------|
| Tables | Files |
| Schema | document-controls.yaml |
| Constraints | Rules (append-only, immutable) |
| Transactions | Git commits |
| Integrity checks | Pre-commit validation |

**Implementation:**
1. `document-controls.yaml` - Config file defining all rules
2. `validate-integrity.py` - Config-driven validation script
3. Pre-commit hook - Automatic enforcement
4. Audit command - Historical violation detection

**Key Principle:**
> Unregistered files in `.harness/` are a code smell. All critical files must be explicitly registered with their integrity rules.

**Status:** Approved - Implementation in progress

---

## Decision #15 - 2025-12-13 (Session 8)
**Topic:** Entry Points, Menu Navigation, and BMAD Independence
**Decision:** Single `/harness` entry point with internal menus; agents and workflows as co-located skills; BMAD as reference material only

**Context:**
- BMAD requires installer to generate `_cfg/agent-manifest.csv` - file was missing, party-mode failed
- BMAD agents have menus pointing to BMAD workflows - deep dependency
- Harness principle: filesystem discovery over generated infrastructure

**Key Decisions:**

### 1. Entry Points (Minimal Slash Commands)
```
.claude/commands/
├── harness.md       # /harness - main entry, shows menu
└── party.md         # /party - shortcut for common use (optional)
```
- NOT a slash command for every agent/workflow
- Entry points lead to menus, menus lead to capabilities

### 2. Internal Menu Navigation
```
/harness →
┌─────────────────────────────────────┐
│  🔧 HARNESS                         │
├─────────────────────────────────────┤
│  Agents:                            │
│  1. 📊 Analyst (Mary)               │
│  2. 🏗️ Architect (Winston)          │
│  ...                                │
│  Workflows:                         │
│  4. 🎉 Party mode                   │
│  5. 💡 Brainstorm                   │
└─────────────────────────────────────┘
```
- Discoverable (shows what's available)
- Conversational (not command-line)
- Nested (agent → agent menu → action)

### 3. Skills Structure (Agents + Workflows Co-located)
```
.claude/skills/harness/
├── SKILL.md              # Core skill, init ritual
├── agents/
│   ├── analyst.md        # Persona + agent menu
│   ├── architect.md
│   ├── pm.md
│   └── dev.md
└── workflows/
    ├── brainstorm.md     # Can reference ../agents/*
    ├── decision.md
    └── party.md          # Multi-agent orchestration
```
- Co-location enables discovery (workflows glob for agents)
- Filesystem IS the registry
- No manifest generation required

### 4. BMAD Independence
| Component | BMAD | Harness |
|-----------|------|---------|
| Agent definitions | `.bmad/**/*.agent.yaml` | `.claude/skills/harness/agents/*.md` |
| Workflows | BMAD workflows | Harness workflows (to be built) |
| Loading | Installer → CSV manifest | Filesystem discovery |
| Format | YAML | Markdown (Claude-native) |

- BMAD agents are **reference material** for persona design
- Harness agents are **new implementations** in Markdown
- No runtime dependency on BMAD infrastructure

### 5. Agent File Format (Markdown with Frontmatter)
```markdown
---
name: Mary
role: Analyst
icon: 📊
---

## Persona
Strategic analyst who treats analysis like a treasure hunt...

## Principles
- Ground findings in evidence
- Every challenge has root causes

## Menu
1. Research topic
2. Analyze patterns
3. Party mode
4. [Chat freely]

## Activation
When invoked, focus on patterns, research, structured analysis...
```

**Rationale:**
- Markdown is Claude-native (reads naturally, no parsing needed)
- Frontmatter provides structured metadata when needed
- Menus are human-readable, not YAML trigger definitions
- Simpler than BMAD's YAML structure

**Relationship to Previous Decisions:**
- Refines D14 (Skills as Universal Architecture) with entry point specifics
- Implements D12 principle: "filesystem discovery over context stuffing"
- Advances D13: BMAD compatibility via reference, not runtime dependency

**Status:** Approved - Ready for prototype

---

## Decision #14 - 2025-12-12 (Session 7)
**Topic:** Skills as Universal Progressive Disclosure Architecture
**Decision:** All Harness capabilities (personas, workflows, knowledge, toolbox) become Claude Code Skills with shared helpers.md

**Rationale:**
- Context is ephemeral - personas fade during long sessions (observed this session)
- Skills are model-invoked - Claude loads what's relevant, when relevant
- Progressive disclosure is native - L1 (name/desc) → L2 (SKILL.md) → L3 (supporting files)
- helpers.md pattern provides 70-85% token savings via section references
- Composable - Claude picks multiple skills as needed (party mode = multiple personas)

**Research Sources:**
1. **Superpowers** (github.com/obra/superpowers) - 20 focused skills, verb-first naming, flat structure
2. **Anthropic docs** (code.claude.com/docs/en/skills) - Model-invoked, description triggers activation
3. **claude-code-bmad-skills** (github.com/aj-geddes) - helpers.md pattern, BMAD as native skills

**Architecture:**
```
.claude/skills/
├── harness/                    # Meta: init ritual, orientation
│   ├── SKILL.md
│   └── index.md
├── helpers.md                  # Shared operations (all skills reference)
├── personas/
│   ├── pm/SKILL.md            # John - product thinking
│   ├── architect/SKILL.md     # Winston - system design
│   ├── analyst/SKILL.md       # Mary - research, patterns
│   └── ...
├── workflows/
│   ├── capturing-decisions/SKILL.md
│   ├── session-handoff/SKILL.md
│   └── brainstorming/SKILL.md
├── toolbox/
│   ├── systematic-debugging/SKILL.md
│   ├── test-driven-dev/SKILL.md
│   └── git-worktrees/SKILL.md
└── knowledge/
    ├── querying-atoms/SKILL.md
    └── promoting-patterns/SKILL.md
```

**helpers.md Pattern:**
```markdown
# In any skill:
Per helpers.md#Load-Project-State
Per helpers.md#Log-Decision
Per helpers.md#Session-Handoff-Checklist
```

**Key Principles:**
- **Focused skills** - One capability per skill (Anthropic guidance)
- **Verb-first naming** - `capturing-decisions` not `decision-capture` (Superpowers)
- **Description is trigger** - "Use when..." tells Claude when to invoke
- **Reference, don't embed** - helpers.md eliminates duplication

**What This Replaces:**
- BMAD slash commands → model-invoked persona skills
- Manual protocols → workflow skills
- Ad-hoc approaches → toolbox skills
- Reading docs → knowledge skills

**Answers Open Question:** Q6 (Unified Architecture) - Skills ARE the unified architecture

**Status:** Approved

---

## Decision #13 - 2025-12-12 (Session 7)
**Topic:** Harness-Native Configuration with BMAD Compatibility
**Decision:** Project configuration lives in `.harness/project.yaml` as single source of truth, with symlinks for BMAD compatibility

**Rationale:**
- Harness is a new product, not a BMAD wrapper
- BMAD is source material - we use its workflows/agents but don't depend on its architecture
- Single source of truth prevents config drift
- Symlinks allow gradual transition without breaking existing workflows

**Implementation:**
```
.harness/project.yaml        ← SOURCE OF TRUTH
.bmad/core/config.yaml       ← symlink → ../../.harness/project.yaml
.bmad/modules/*/config.yaml  ← symlink as needed (future)
```

**Transition Plan (Strangler Fig Pattern):**
1. **Now:** Harness config as source, BMAD reads via symlink
2. **Gradual:** New Harness workflows read `.harness/` directly
3. **Eventually:** BMAD becomes optional module

**Status:** Approved and Implemented

---

## Decision #12 - 2025-12-11 (Session 4)
**Topic:** Harness Architectural Foundation - Skills-Based Context System
**Decision:** Harness will be a NEW framework replacing BMAD, built on Skills-based architecture informed by Anthropic's proven patterns

**Rationale:**
- BMAD demonstrates what agent-based methodology CAN be, but architecture must be rebuilt on proven foundations
- Anthropic's research provides authoritative patterns for long-running autonomous agents
- Claude Code Skills provide native progressive disclosure with model-invoked discovery
- "Documentation is the only memory" requires systematic context management across sessions

**Sources Informing This Decision:**
1. **Claude Code Skills** (https://code.claude.com/docs/en/skills)
   - Progressive disclosure: SKILL.md loaded first, supporting files on-demand
   - Model-invoked: Claude decides when to use based on description
   - Native to Claude Code - zero custom infrastructure

2. **Long-Running Agents Paper** (anthropic.com/engineering/effective-harnesses-for-long-running-agents)
   - Two-agent pattern: Initializer (plans) + Coding Agent (executes)
   - Artifacts as memory: JSON > Markdown for state (less corruption risk)
   - Immutable task lists: Only modify "passes" field, never delete/edit features
   - Git as recovery: Commit history enables state restoration

3. **Claude 4 Best Practices** (platform.claude.com - multi-context-window-workflows)
   - Fresh context windows > compaction (Claude 4.5 excels at filesystem discovery)
   - Three-layer state: Structured (JSON) + Unstructured (MD) + Git
   - Prescriptive discovery ritual: pwd → read state → check git → verify baseline

4. **Autonomous Coding Quickstart** (github.com/anthropics/claude-quickstarts/autonomous-coding)
   - 7-step initialization ritual (reference implementation)
   - feature_list.json as single source of truth
   - Session closure protocol: commit, document, leave working state

**Architecture:**
```
.claude/skills/harness/
├── SKILL.md                      # Entry point + init ritual
├── index.md                      # Route to all knowledge
├── state/                        # STRUCTURED (JSON)
│   ├── project-state.json
│   ├── task-list.json
│   └── recovery-state.json
├── context/                      # UNSTRUCTURED (MD)
│   ├── vision.md
│   ├── decisions.md
│   ├── progress.md
│   └── methodology.md
└── deep/                         # REFERENCE (on-demand)
    ├── patterns/
    ├── research/
    └── transcripts/
```

**Initialization Ritual (in SKILL.md):**
1. pwd → Confirm project location
2. Read state/project-state.json → Current phase and focus
3. Read state/task-list.json → What's done, what's pending
4. Read context/progress.md → Recent session activity
5. git log --oneline -5 → Recent commits
6. git status → Uncommitted changes
7. Verify baseline → Ready to proceed

**Relationship to BMAD:**
- BMAD becomes SOURCE MATERIAL, not foundation
- Cherry-pick best patterns: agents, workflows, party mode
- Redesign context management from first principles
- Rebuild methodology documentation for Harness

**What Harness IS:**
```
HARNESS = BMAD Patterns + Anthropic Best Practices + Skills Architecture
        = Methodology    + Proven Patterns           + Native Context System
```

**Implications:**
- Create new Skills-based context system
- Migrate valuable BMAD patterns to Harness architecture
- Document Harness methodology (not BMAD methodology)
- SessionStart hook complements Skills (bridge vs persistent)

**Status:** Approved

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
