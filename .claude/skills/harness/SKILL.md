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
| **Vision** | `00-governance/vision.md` |
| **Map** | `.harness/PROJECT-MAP.md` |

## Progressive Disclosure

| Level | What | When |
|-------|------|------|
| 0 | This skill + project-state.yaml | Every session |
| 1 | decision-log.md, vision.md | When context needed |
| 2 | Full transcripts, patterns | Deep analysis |
| 3 | BMAD module docs | When using BMAD workflows |

## Core Principles

1. **Documentation IS memory** - If not documented, it doesn't exist
2. **Single source of truth** - `.harness/` is canonical, reference don't duplicate
3. **Fresh sessions preferred** - New context over compaction
4. **Strangler Fig transitions** - Gradual migration, don't break existing

## For More

- Full methodology: `00-governance/vision.md`
- Project map: `.harness/PROJECT-MAP.md`
- Patterns: `.harness/patterns-and-ideas.md`
- Knowledge atoms: `.harness/atoms.jsonl`
