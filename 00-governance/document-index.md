# Harness Document Index

> **TL;DR:** Each document has ONE purpose. No duplication. This index defines what goes where.

---

## Core Governance Documents

| Document | Purpose | Source of Truth For | Audience |
|----------|---------|---------------------|----------|
| `CLAUDE.md` | Project context, core principles, HOW to work here | Always-loaded operational context | LLM |
| `working-agreement.md` | HOW we work together | Processes, protocols, validated learnings | Human + LLM |
| `document-index.md` | WHERE things go | Document purposes, no duplication rule | Human + LLM |
| `capture-protocol.md` | HOW we capture information | Capture methodology, session boundaries | Human + LLM |

## Operational Documents (`.harness/`)

| Document | Purpose | Source of Truth For | Audience |
|----------|---------|---------------------|----------|
| `decision-log.md` | WHEN and WHY we decided things | Historical record of all decisions | LLM primarily |
| `project-state.yaml` | WHERE we are NOW | Current phase, blockers, next actions | LLM primarily |
| `lessons-learned.md` | WHAT went wrong and how we fixed it | Failure patterns, solutions | Human + LLM |
| `recovery-state.json` | Recovery script state | Last check timestamp, processed files | Script only |

## Key Rules

### 1. Single Source of Truth
- Each concept lives in ONE document
- Other documents REFERENCE, never duplicate
- Core principles live in CLAUDE.md (always loaded by LLM)

### 2. Document Updates Flow
```
Decision made → decision-log.md (immediate)
                    ↓
            If core principle → CLAUDE.md (curated)
                    ↓
            If process changes → working-agreement.md
```

### 3. Recovery Script Checks
On SessionStart, the recovery script verifies:
- [ ] Any undocumented items flagged in transcript?
- [ ] Git health (uncommitted changes, unpushed branches)

---

*Created: 2025-12-11 (Session 3)*
