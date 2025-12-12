# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Harness

**AI-Native Development Methodology** - A synthesis of proven methodologies evaluated for the AI-assisted era, built on Claude Code native features (Skills, hooks, CLAUDE.md).

Harness is NOT a child of BMAD. BMAD is source material, alongside Anthropic patterns and methodology research.

**User**: Dudley
**Note**: This project uses git worktrees - multiple branches checked out simultaneously. Main worktree at `/Users/dudley/projects/Harness`, session worktrees at `~/.claude-worktrees/Harness/`.

## Architecture (D12)

Harness is built on **Skills-based architecture** per Decision #12:
- Claude Code native features (Skills, hooks, CLAUDE.md) over custom infrastructure
- Filesystem discovery over context stuffing
- Fresh sessions preferred over compaction

**Planned structure** (not yet implemented):
```
.claude/skills/harness/
├── SKILL.md          # Entry point + init ritual
├── state/            # JSON (project-state, tasks, recovery)
├── context/          # MD (vision, decisions, progress)
└── deep/             # Reference (patterns, research, transcripts)
```

See `.harness/decision-log.md` → D12 for full rationale.

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
| Project config | `.harness/project.yaml` |
| Decisions | `.harness/decision-log.md` |
| Lessons learned | `.harness/lessons-learned.md` |
| Patterns | `.harness/patterns-and-ideas.md` |
| Vision/principles | `00-governance/vision.md` |
| Capture protocol | `00-governance/capture-protocol.md` |

## Commands

```bash
# Check context usage
/context
```

## Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `session-recovery.py` | Scan sessions, export transcripts, show recovery checklist | Auto-runs via hook; manual: `python3 .harness/scripts/session-recovery.py` |
| `export-session.py` | Export JSONL session to readable Markdown | `python3 .harness/scripts/export-session.py [session-id]` |
| `extract-atoms.py` | Extract knowledge atoms from transcripts to atoms.jsonl | `python3 .harness/scripts/extract-atoms.py [--reprocess]` |
| `analyze-session.py` | Analyze JSONL content breakdown (text vs tools) | `python3 .harness/scripts/analyze-session.py <file>` |

## Knowledge Base

Accumulated knowledge from sessions:

| File | Contents | Query |
|------|----------|-------|
| `.harness/atoms.jsonl` | 267 knowledge atoms (decisions, learnings, patterns) | `grep "keyword" .harness/atoms.jsonl \| python3 -m json.tool` |
| `.harness/questions.yaml` | Open questions (Q1-Q8+) awaiting exploration | Read directly |
| `.harness/ideas.yaml` | Captured ideas with lifecycle status | Read directly |
| `.harness/taxonomy.yaml` | Classification types and maturity model | Reference for atom extraction |

### BMAD Agents

Use for **party mode** (multi-agent brainstorm) or **role-based thinking**:
- `/bmad:core:agents:bmad-master` - Orchestrator, party-mode
- `/bmad:bmm:agents:pm` - John: product strategy, WHY questions
- `/bmad:bmm:agents:architect` - Winston: system design
- `/bmad:bmm:agents:analyst` - Mary: research, patterns
- `/bmad:bmm:agents:dev` - Amelia: implementation
- `/bmad:bmm:agents:ux-designer` - Sally: user experience

Default: work directly. Invoke agents when role-specific perspective adds value.

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

## When Things Go Wrong

| Problem | Solution |
|---------|----------|
| Hook doesn't fire | Run manually: `python3 .harness/scripts/session-recovery.py` |
| project-state.yaml stale | Check `git log -5` for recent work, read decision-log.md |
| No recovery transcript | Check `~/.claude/projects/` for JSONL, run `export-session.py` |
| Lost context mid-session | Read PROJECT-MAP.md, then project-state.yaml |
| Git in bad state | Run `git status`, check hook output for suggestions |

**Fallback orientation**: If all else fails, read files in this order:
1. `.harness/PROJECT-MAP.md` → structure overview
2. `.harness/project-state.yaml` → current phase
3. `.harness/decision-log.md` → recent decisions (D12 is key)

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
