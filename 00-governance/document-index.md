# Harness Document Index

> **TL;DR:** Each document has ONE purpose. No duplication. This index defines what goes where.

---

## Core Governance Documents

| Document | Purpose | Source of Truth For | Audience |
|----------|---------|---------------------|----------|
| `vision.md` | WHY we're building, WHAT we're building | Project purpose, scope, success criteria, core principles | Human + LLM |
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
- Example: Vision statement lives in `vision.md`, `working-agreement.md` links to it

### 2. Document Updates Flow
```
Decision made → decision-log.md (immediate)
                    ↓
            If new principle emerges → vision.md
                    ↓
            If process changes → working-agreement.md
```

### 3. Recovery Script Checks
On SessionStart, the recovery script verifies:
- [ ] New decisions in decision-log.md synced to vision.md principles?
- [ ] Any undocumented items flagged in transcript?

---

*Created: 2025-12-11 (Session 3)*
