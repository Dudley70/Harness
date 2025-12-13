---
name: harness
description: AI-Native Development Methodology skill. Use when starting a session, checking project state, following Harness methodology, or working with .harness/ files. Provides init ritual, progressive disclosure, and knowledge routing.
---

# Harness Skill

AI-Native Development Methodology - channeling AI power through human-designed controls.

## When to Use

Invoke this skill when:
- Starting a new session on a Harness project
- Needing to understand project state or context
- Following Harness methodology for development work
- Working with `.harness/` directory files

## Menu

When invoked, present this menu:

```
🔧 HARNESS - AI-Native Development

What would you like to do?

AGENTS (invoke a persona):
1. 📊 Mary (Analyst) - Research, patterns, requirements
2. 🏗️ Winston (Architect) - System design, tech decisions
3. 📋 John (PM) - Product strategy, prioritization
4. 💻 Amelia (Dev) - Implementation, code quality
5. 🎨 Sally (UX) - User experience, interface design

WORKFLOWS:
6. 👥 Team Discussion - Multi-agent discussion (or use presets below)
   • /harness:team:core - Mary + Winston
   • /harness:team:technical - Winston + Amelia
   • /harness:team:product - John + Sally
   • /harness:team:full - Everyone
7. 📝 Capture Decision - Document a decision

UTILITIES:
8. 🔄 Refresh Context - Reload critical files
9. 📊 Project Status - Show current state

Pick a number or describe what you need.
```

### Menu Actions

| # | Action |
|---|--------|
| 1-5 | Load agent from `./agents/{name}.md`, activate persona |
| 6 | Load `./workflows/team.md`, run team discussion |
| 7 | Read decision-log.md, append new decision |
| 8 | Run `/harness:refresh` |
| 9 | Read project-state.yaml, summarize |

## Initialization Ritual

Run these steps at session start (per D12):

1. **Confirm location**: `pwd` → Verify project root
2. **Load state**: Read `.harness/project-state.yaml` → Current phase, focus, blockers
3. **Check config**: Read `.harness/project.yaml` → User, environment, paths
4. **Recent decisions**: Read `.harness/decision-log.md` → Latest decisions (D13 is current)
5. **Git status**: `git log --oneline -5` + `git status` → Recent commits, uncommitted work
6. **Recovery context**: Check `.harness/transcripts/` → Any session recovery needed?
7. **Ready**: Brief user, offer contextual options

## Key Files

| Purpose | Location |
|---------|----------|
| **State** (load first) | `.harness/project-state.yaml` |
| **Config** | `.harness/project.yaml` |
| **Decisions** | `.harness/decision-log.md` |
| **Map** | `.harness/PROJECT-MAP.md` |

## Progressive Disclosure

| Level | What | When |
|-------|------|------|
| 0 | This skill + project-state.yaml | Every session |
| 1 | decision-log.md | When context needed |
| 2 | Full transcripts, patterns | Deep analysis |
| 3 | BMAD module docs | When using BMAD workflows |

## Core Principles

1. **Documentation IS memory** - If not documented, it doesn't exist
2. **Single source of truth** - `.harness/` is canonical, reference don't duplicate
3. **Fresh sessions preferred** - New context over compaction
4. **Strangler Fig transitions** - Gradual migration, don't break existing

## For More

- Project map: `.harness/PROJECT-MAP.md`
- Patterns: `.harness/patterns-and-ideas.md`
- Knowledge atoms: `.harness/atoms.jsonl`
- Archived brief: `.harness/reference/project-brief.md`
