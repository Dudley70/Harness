# Harness Knowledge Index

Quick routing to all Harness knowledge. Read SKILL.md first.

## State & Config

| File | Purpose |
|------|---------|
| `.harness/project-state.yaml` | Current phase, session history, next actions |
| `.harness/project.yaml` | User config, environment, paths |
| `.harness/recovery-state.json` | Recovery system tracking |

## Decisions & Learnings

| File | Purpose |
|------|---------|
| `.harness/decision-log.md` | All decisions D1-D13+ with rationale |
| `.harness/lessons-learned.md` | Failures and learnings L1-L4+ |
| `.harness/patterns-and-ideas.md` | Research patterns, ideas |

## Knowledge Base

| File | Purpose |
|------|---------|
| `.harness/atoms.jsonl` | 267+ knowledge atoms (queryable) |
| `.harness/taxonomy.yaml` | Classification types |
| `.harness/questions.yaml` | Open questions Q1-Q8+ |
| `.harness/ideas.yaml` | Captured ideas with lifecycle |

## Governance

| File | Purpose |
|------|---------|
| `00-governance/vision.md` | Project vision and principles |
| `00-governance/capture-protocol.md` | End-of-session checklist |
| `00-governance/working-agreement.md` | Process agreements |

## Scripts

| Script | Purpose |
|--------|---------|
| `.harness/scripts/session-recovery.py` | SessionStart hook, recovery scan |
| `.harness/scripts/extract-atoms.py` | Extract atoms from transcripts |
| `.harness/scripts/export-session.py` | Export session to markdown |

## BMAD (Optional)

BMAD is source material, not foundation. Use when needed:

| Resource | Purpose |
|----------|---------|
| `/bmad:core:agents:bmad-master` | Party mode, orchestration |
| `.bmad/modules/bmm/agents/` | Specialist agents (PM, Architect, etc.) |
| `.bmad/core/workflows/` | Brainstorming, party-mode workflows |
