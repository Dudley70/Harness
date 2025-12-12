# Harness Project Map

> **Purpose**: This is the "where is everything" reference for session startup orientation.
> Updated: 2025-12-12 (Session 5)

## Quick Reference

| Need | Location |
|------|----------|
| Current state | `.harness/project-state.yaml` |
| Decisions | `.harness/decision-log.md` |
| Lessons | `.harness/lessons-learned.md` |
| Patterns | `.harness/patterns-and-ideas.md` |
| Session history | `.harness/transcripts/` |
| Journal narratives | `.harness/journal/sessions/` |
| Vision/governance | `00-governance/` |
| BMAD agents | `.bmad/modules/bmm/agents/` |
| Slash commands | `.claude/commands/bmad/` |

---

## Structure Overview

```
bold-jemison/
├── ROOT FILES
│   ├── PROJECT.md              # Strategic context
│   ├── SESSION.md              # Current session state
│   └── CLAUDE.md               # Claude Code instructions (TBD)
│
├── 00-governance/              # Working agreement, protocols
│   ├── working-agreement.md
│   ├── capture-protocol.md
│   └── document-index.md
│
├── docs/                       # User-facing documentation
│   └── INDEX.md
│
├── .harness/                   # HARNESS INFRASTRUCTURE
│   ├── project-state.yaml      # LOAD FIRST - master state
│   ├── decision-log.md         # D1-D12 decisions
│   ├── lessons-learned.md      # L1-L4 failures/learnings
│   ├── patterns-and-ideas.md   # Research patterns
│   ├── recovery-state.json     # Recovery tracking
│   ├── PROJECT-MAP.md          # THIS FILE
│   │
│   ├── journal/                # Narrative history
│   │   ├── README.md
│   │   ├── sessions/           # Session stories
│   │   └── decisions/          # Expanded ADRs
│   │
│   ├── transcripts/            # Auto-exported sessions
│   │   └── auto-recovery-*.md
│   │
│   ├── templates/              # Reusable templates
│   │   └── session-journal.md
│   │
│   ├── scripts/                # Automation
│   │   ├── session-recovery.py # SessionStart hook
│   │   ├── export-session.py   # Manual export
│   │   └── analyze-session.py
│   │
│   └── reference/              # Research materials
│       └── hbmad-architecture-draft.md
│
├── .claude/                    # CLAUDE CODE CONFIG
│   ├── settings.local.json     # Permissions
│   └── commands/bmad/          # Slash commands → agents
│       ├── core/agents/bmad-master.md
│       └── bmm/agents/*.md     # 9 specialist agents
│
└── .bmad/                      # BMAD FRAMEWORK
    ├── core/                   # Framework foundation
    │   ├── module.yaml         # Core config
    │   ├── agents/bmad-master.agent.yaml
    │   ├── workflows/party-mode/
    │   └── workflows/brainstorming/
    │
    └── modules/                # Installed modules
        ├── bmm/                # Method (9 agents, 34+ workflows)
        ├── bmb/                # Builder (create agents/workflows)
        ├── bmgd/               # Game Development
        └── cis/                # Creative Innovation
```

---

## Key Files by Purpose

### Session Startup (read these first)
1. `.harness/project-state.yaml` - Current phase, blockers, next actions
2. `.harness/decision-log.md` - Recent decisions (D18 is latest)

### Recovery & History
- `.harness/transcripts/` - Raw session exports
- `.harness/journal/sessions/` - Curated narratives
- `.harness/recovery-state.json` - What's been processed

### Creating/Editing
- Use BMB workflows: `.bmad/modules/bmb/workflows/create-*/`
- Agent definitions: `.bmad/modules/*/agents/*.agent.yaml`
- Slash commands: `.claude/commands/bmad/`

### Methodology
- `00-governance/capture-protocol.md` - End-of-session checklist
- `.harness/lessons-learned.md` - What to avoid
- `.harness/patterns-and-ideas.md` - What to embrace

---

## Current State (Session 5)

- **Phase**: Architecture-Design
- **Key Decision**: D12 - Skills-based architecture
- **Active Work**: Smart greeting system, CLAUDE.md design
- **Context**: Hook fires on SessionStart, provides recovery summary

---

## Progressive Disclosure Levels

| Level | What | When to Load |
|-------|------|--------------|
| 0 | This map + project-state.yaml | Every session start |
| 1 | decision-log.md | When context needed |
| 2 | Full transcripts, patterns | Deep analysis only |
| 3 | BMAD module docs | When using that module |
