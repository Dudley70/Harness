# Document Management Skill

> **Use when:** Creating, modifying, or managing files in `.harness/` or `00-governance/`

## Core Principle

> **Files ARE the memory. Memory corruption = system failure.**

Harness documents are not disposable notes—they're the permanent record. Nothing is deleted; everything has a lifecycle.

## Quick Reference

### Before Creating/Editing

1. Check the registry: `.harness/document-controls.yaml`
2. Know the rule type (append-only, immutable, protected, free)
3. Follow the lifecycle for that content type

### Rule Types

| Rule | Meaning | Action |
|------|---------|--------|
| `append_only` | Cannot delete content | Mark as DONE/OBSOLETE instead |
| `immutable` | Cannot change at all | Create new entries, don't modify |
| `protected` | Must exist | Never delete the file |
| `free` | No constraints | Normal editing |

### Common Operations

| I want to... | Do this |
|--------------|---------|
| Complete a task | Change `"P0: Do X"` → `"DONE: Do X (Session N)"` |
| Remove obsolete task | Change to `"OBSOLETE: X (reason)"` |
| Update a decision | Add NEW decision referencing old, don't edit old |
| Abandon an idea | Change status to `ABANDONED` in ideas.yaml |
| Answer a question | Change status to `ANSWERED` in questions.yaml |
| Create new file | Create file, then register in document-controls.yaml |

## Progressive Disclosure

| Need | Read |
|------|------|
| Full rule definitions | `.harness/document-controls.yaml` |
| Lifecycle state details | `./lifecycle.md` |
| How to register files | `./registration.md` |
| Why this exists | Decision #16 in `.harness/decision-log.md` |

## Enforcement

- **Pre-commit hook** validates all changes automatically
- Violations block commit with explanation
- Run `python3 .harness/scripts/validate-integrity.py --check` to verify

## Status Prefixes (Allowed "Deletions")

These prefixes allow content to transition without violating append-only:

```
DONE:      - Task completed
OBSOLETE:  - No longer relevant
PARKED:    - Deferred, not forgotten
ANSWERED:  - Question resolved
PROMOTED:  - Became a decision/feature
ABANDONED: - Idea not viable
MERGED:    - Combined with another item
```

## Red Flags

Stop and think if you're about to:
- Delete lines from project-state.yaml
- Remove a decision from decision-log.md
- Edit content in atoms.jsonl
- Delete any file from `.harness/`

These are likely violations. Use lifecycle status instead.
