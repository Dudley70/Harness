# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Harness** is an AI-Native Development Methodology - a synthesis of proven methodologies (Lean, Agile, etc.) evaluated for the AI-assisted era, built on Skills-based architecture using Claude Code native features.

**Critical**: Harness is NOT a child of BMAD. It's a synthesis that includes Anthropic's patterns, Claude Code features, methodology research, and BMAD's agent approach as one of many inputs.

## Session Initialization Ritual

Every session must start with this 7-step sequence:

1. **pwd** → Confirm project location
2. **Read .harness/project-state.yaml** → Current phase, focus, blockers
3. **Read .harness/decision-log.md** → Recent decisions (D12 is latest)
4. **Read 00-governance/vision.md** → Project principles
5. **git log --oneline -5** → Recent commits
6. **git status** → Uncommitted changes
7. **Verify baseline** → Ready to proceed

**Note**: SessionStart hook automatically provides recovery context - check hook output for high-priority items before proceeding.

## Architecture

```
Harness/
├── .harness/                    # Infrastructure (LOAD FIRST)
│   ├── project-state.yaml       # Master state - current phase/focus
│   ├── decision-log.md          # D1-D12 decisions
│   ├── lessons-learned.md       # L1-L4 failures
│   ├── patterns-and-ideas.md    # Research patterns
│   ├── atoms.jsonl              # Knowledge atoms (267 extracted)
│   ├── taxonomy.yaml            # Classification system
│   ├── PROJECT-MAP.md           # File location reference
│   ├── scripts/                 # Automation
│   │   ├── session-recovery.py  # SessionStart hook
│   │   └── extract-atoms.py     # Knowledge extraction
│   ├── journal/                 # Narrative history
│   └── transcripts/             # Auto-exported sessions
│
├── 00-governance/               # Vision, working agreement
│   ├── vision.md                # Project principles
│   ├── working-agreement.md     # How we work
│   ├── capture-protocol.md      # Documentation rules
│   └── document-index.md        # Document purposes
│
├── .bmad/                       # BMAD framework (source material)
│   ├── core/                    # Framework foundation
│   │   ├── agents/bmad-master.agent.yaml
│   │   └── workflows/           # party-mode, brainstorming
│   └── modules/                 # BMM, BMB, BMGD, CIS modules
│
└── .claude/                     # Claude Code config
    ├── settings.local.json      # Permissions + hooks
    └── commands/bmad/           # Slash commands → agents
```

## Common Commands

### Session Management
```bash
# Check git health (shows branch status, worktrees, uncommitted)
git status

# Run recovery scan manually (normally auto-runs via SessionStart hook)
python3 .harness/scripts/session-recovery.py

# Extract knowledge atoms from sessions
python3 .harness/scripts/extract-atoms.py

# Check context usage
/context
```

### BMAD Agent Activation
Use slash commands to activate BMAD agents (these are **source material** for Harness, not the implementation):

- `/bmad:core:agents:bmad-master` - Master orchestrator, recovery coordinator
- `/bmad:bmm:agents:pm` - Product Manager (John)
- `/bmad:bmm:agents:architect` - System Architect (Winston)
- `/bmad:bmm:agents:analyst` - Research Analyst (Mary)
- `/bmad:bmm:agents:dev` - Developer Agent
- `/bmad:bmm:agents:ux-designer` - UX Designer

**Note**: These agents demonstrate what agent-based methodology CAN be, but Harness architecture is being rebuilt on Skills-based patterns.

## Key Patterns

### Progressive Disclosure
- **Level 0**: Anchors (200-300 tokens) - always loaded
- **Level 1**: Summaries (500-800 tokens) - loaded when entering topic
- **Level 2**: Details (full content) - only when specifically needed

### Sub-Agent Protocol
When spawning sub-agents for research/analysis:
1. ONE focused topic per sub-agent
2. Explicit output format prevents summarization
3. Sub-agents write directly to files (NEVER return data to orchestrator)
4. Orchestrator stays lean - only holds references

### State Management
- **Structured state**: JSON files in `.harness/` (less corruption than YAML/MD)
- **Unstructured context**: Markdown in `00-governance/`
- **Git as recovery**: Commit history enables state restoration
- **Atoms as knowledge units**: Granular insights extracted to `atoms.jsonl`

### Documentation Rules
- **Single source of truth**: Each concept has ONE authoritative document
- **Reference, don't duplicate**: Other docs point to source
- **Capture is MANDATORY**: End-of-session checklist required (see `00-governance/capture-protocol.md`)
- **Fresh sessions > compaction**: Claude 4.5 excels at filesystem discovery

## Current Phase: Architecture-Design

**Status**: D12 approved - Harness will use Skills-based architecture
**Active Work**: Prototyping Skills structure, integrating atom extraction into SessionStart hook
**Next Actions** (from `.harness/project-state.yaml`):
- P0: Integrate atom extraction into SessionStart hook
- P0: Deep dive Superpowers repo
- P1: Address Q1-Q8 from questions.yaml
- P1: Prototype Harness skill structure

## Critical Decisions

**D12 (2025-12-11)**: Harness Architectural Foundation
- Skills-based context system (Claude Code native)
- Filesystem discovery > context stuffing
- Fresh context windows preferred over compaction
- Atoms as knowledge units
- Source: Anthropic patterns + Skills documentation

**D11 (2025-12-11)**: BMAD Master as default entry point
- Lightest context cost (~500 tokens)
- Acts as recovery coordinator
- Routes to specialists when needed

**D10 (2025-12-11)**: Recovery Handoff Protocol
- SessionStart hook runs `session-recovery.py` (zero context cost)
- Auto-exports transcript with progressive disclosure
- BMAD Master handles full context restoration

See `.harness/decision-log.md` for complete decision history.

## Core Principles

1. **Documentation IS memory** - If not documented, it doesn't exist
2. **Context is ephemeral** - Nothing valuable exists only in context
3. **Prevention > Recovery** - Make data loss impossible, not recoverable
4. **Sub-agents write directly** - Don't return data to orchestrator
5. **Validate before proceeding** - Checklists, not assumptions
6. **Skills-based architecture** - Native features over custom infrastructure
7. **Fresh sessions preferred** - New context window over compaction
8. **Atoms as knowledge units** - Extract granular insights

## SessionStart Hook

The hook automatically:
1. Scans ALL Harness-related folders for new JSONL entries
2. Exports new sessions to `.harness/transcripts/auto-recovery-*.md`
3. Provides recovery checklist with high-priority items
4. Checks git health (branches, uncommitted changes)
5. Flags if vision.md needs syncing with decision-log.md

**Hook output structure**:
- Session profile (tools used, character)
- Recovery checklist (decisions, errors, actions)
- Git status table
- Suggested actions

## End-of-Session Checklist

Before ending ANY session (from `00-governance/capture-protocol.md`):
- [ ] All sub-agent outputs written to files?
- [ ] Decisions logged with rationale in `.harness/decision-log.md`?
- [ ] Lessons/failures captured in `.harness/lessons-learned.md`?
- [ ] Next session has explicit actions in `.harness/project-state.yaml`?
- [ ] Update session summary in `.harness/project-state.yaml`?
- [ ] Commit all changes with descriptive message?

## Knowledge System

**Atoms** (267 extracted as of Session 5):
- Stored in `.harness/atoms.jsonl`
- Multi-type classification via `taxonomy.yaml`
- DIKW maturity model: extracted → synthesized → principled
- Query with Python or build visualization tools

**Taxonomy** (10 core types, 5 domain types):
- Core: DECISION, LEARNING, PATTERN, RESEARCH, QUESTION, IDEA, BLOCKER, ACTION, ERROR, TODO
- Domain: METHODOLOGY, TOOL, ARCHITECTURE, PROCESS, DOCUMENTATION
- Plus maturity levels and session classifications

## Context Budget Management

- Use `/context` to check usage
- **Zones**:
  - 0-50%: GREEN - normal operation
  - 50-65%: YELLOW - consider wrapping up
  - 65-77%: ORANGE - complete task, prepare handoff
  - 77%+: RED - approaching autocompact, stop new work

Session 5 ended at 95% (RED zone) - demonstrates autocompact frees space dynamically.

## References

- **Anthropic Sources**:
  - Long-Running Agents: anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - Claude 4 Best Practices: platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
  - Skills Documentation: code.claude.com/docs/en/skills
  - Autonomous Coding: github.com/anthropics/claude-quickstarts/autonomous-coding

- **Research Material**:
  - BMAD Skills: github.com/aj-geddes/claude-code-bmad-skills (helpers.md pattern)
  - Superpowers: github.com/obra/superpowers (parked for P0 deep dive)
  - Compression Project: /Users/dudley/projects/Compression/ (77% compression, tested)

## Working in This Repository

1. **Always start with initialization ritual** (7 steps above)
2. **Check SessionStart hook output** for recovery context
3. **Load .harness/PROJECT-MAP.md** if you need to locate files
4. **Read working-agreement.md** for sub-agent protocol
5. **Follow capture-protocol.md** at session end
6. **Update project-state.yaml** with session summary
7. **Commit frequently** - git is recovery mechanism
