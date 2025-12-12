# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Harness

**AI-Native Development Methodology** - A synthesis of proven methodologies evaluated for the AI-assisted era, built on Claude Code native features (Skills, hooks, CLAUDE.md).

Harness is NOT a child of BMAD. BMAD is source material, alongside Anthropic patterns and methodology research.

**User**: Dudley
**Note**: This project uses git worktrees - multiple branches checked out simultaneously. Main worktree at `/Users/dudley/projects/Harness`, session worktrees at `~/.claude-worktrees/Harness/`.

## Session Start

1. **Check hook output** - SessionStart hook provides recovery context, git health, priorities
2. **Read `.harness/project-state.yaml`** - Current phase, focus, blockers
3. **git status** - Uncommitted work?
4. **Ready to proceed**

**If no hook output**: Run `python3 .harness/scripts/session-recovery.py` manually.

## Session Greeting

When greeting the user at session start:
- Acknowledge hook recovery context briefly (don't repeat everything)
- Surface **HIGH priority items first** (blockers, failing tests, unmerged branches)
- Offer 2-3 **contextual options** based on last session type
- Adapt to time gap: long absence (>1 day) = more context; quick return = minimal
- Keep greeting **under 10 lines** unless user asks for details

Example options format:
```
What would you like to do?
1. [Continue] Resume X from last session
2. [Review] Check git status / unmerged work
3. [Fresh] Start new task
```

## If Lost

Read `.harness/PROJECT-MAP.md` - it maps the entire project structure.

For full orientation, read in order:
1. `.harness/project-state.yaml` - where we are
2. `.harness/decision-log.md` - key decisions (D12 is architectural foundation)
3. `00-governance/vision.md` - why we're building this

## Find Things

| Need | Location |
|------|----------|
| Project map | `.harness/PROJECT-MAP.md` |
| Current state | `.harness/project-state.yaml` |
| Decisions | `.harness/decision-log.md` |
| Lessons learned | `.harness/lessons-learned.md` |
| Patterns | `.harness/patterns-and-ideas.md` |
| Vision/principles | `00-governance/vision.md` |
| Capture protocol | `00-governance/capture-protocol.md` |

## Commands

```bash
# Recovery scan (normally auto-runs via hook)
python3 .harness/scripts/session-recovery.py

# Check context usage
/context
```

### BMAD Agents (source material, not Harness implementation)
- `/bmad:core:agents:bmad-master` - Orchestrator, recovery, party-mode
- `/bmad:bmm:agents:pm` - Product Manager (John)
- `/bmad:bmm:agents:architect` - Architect (Winston)
- `/bmad:bmm:agents:analyst` - Analyst (Mary)

## Core Principles

1. **Documentation IS memory** - If not documented, it doesn't exist
2. **Context is ephemeral** - Nothing valuable exists only in context
3. **Sub-agents write directly** - Never return data to orchestrator
4. **Reference, don't duplicate** - Point to source files
5. **Fresh sessions preferred** - New context > compaction
6. **Instructions, not information** - CLAUDE.md tells HOW, files contain WHAT

## SessionStart Hook

Automatically runs on session start:
- Scans for new session content
- Exports to `.harness/transcripts/`
- Shows recovery checklist
- Git health check with suggested actions
- Flags sync issues

## Context Budget

Use `/context` to check. Zones:
- **0-50%**: GREEN - normal
- **50-65%**: YELLOW - wrap up soon
- **65-77%**: ORANGE - complete task, handoff
- **77%+**: RED - stop new work

## End Session

Before ending, see `00-governance/capture-protocol.md`. Key checks:
- [ ] Sub-agent outputs written to files?
- [ ] Decisions logged?
- [ ] project-state.yaml updated?
- [ ] Changes committed?

## Working Here

1. Check hook output first
2. Load PROJECT-MAP.md if lost
3. Follow capture-protocol.md at end
4. Commit frequently - git is recovery
