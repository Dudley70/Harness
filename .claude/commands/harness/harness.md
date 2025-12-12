# Harness - AI-Native Development Methodology

Load the Harness control center skill and present the main menu.

## Activation

1. Read `.claude/skills/harness/SKILL.md` to understand capabilities
2. Check session state from hook output or `.harness/project-state.yaml`
3. Present the main menu

## Main Menu

| # | Option | Description |
|---|--------|-------------|
| 1 | **Status** | Show project state, recent decisions, blockers |
| 2 | **Agents** | Access specialized agents (Analyst, Architect, PM, Dev) |
| 3 | **Party** | Multi-agent discussion mode |
| 4 | **Recovery** | Session recovery and context restoration |
| 5 | **Capture** | End-of-session capture protocol |

## Usage

User types a number or keyword to select. Example interactions:

- `1` or `status` → Show current project state
- `2` or `agents` → List available agents, then select one
- `3` or `party` → Start multi-agent party mode
- `4` or `recovery` → Run recovery scan, show checklist
- `5` or `capture` → Guide through end-of-session protocol

## Agent Selection (Option 2)

When user selects Agents, present:

| # | Agent | Role |
|---|-------|------|
| 1 | Mary (Analyst) | Research, requirements, analysis |
| 2 | Winston (Architect) | System design, technical decisions |
| 3 | John (PM) | Product strategy, prioritization |
| 4 | Amelia (Dev) | Implementation, code review |

Load the selected agent from `.claude/skills/harness/agents/{name}.md`

## Key Files

- **State**: `.harness/project-state.yaml`
- **Decisions**: `.harness/decision-log.md`
- **Map**: `.harness/PROJECT-MAP.md`
- **Controls**: `.harness/document-controls.yaml`

## Principles

1. Start fresh - check hook output first
2. Reference, don't duplicate - point to files
3. Capture everything - documentation IS memory
4. Append-only - mark DONE/OBSOLETE, never delete
