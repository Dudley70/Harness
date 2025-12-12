# Registering New Documents

When creating new files in `.harness/` or `00-governance/`, they must be registered in the document controls.

## The Registry

**Location:** `.harness/document-controls.yaml`

This is the schema for Harness memory. All files should be registered here.

## Registration Process

### 1. Determine the Rule Type

| If the file contains... | Use rule | Example |
|------------------------|----------|---------|
| Tasks, action items | `append_only` | project-state.yaml |
| Decisions, permanent records | `append_only` | decision-log.md |
| Extracted facts | `immutable` | atoms.jsonl |
| Core system files | `protected` | CLAUDE.md |
| Generated/temporary content | `free` | transcripts/* |

### 2. Add to document-controls.yaml

**For append-only files:**
```yaml
append_only:
  .harness/my-new-file.md:
    description: "What this file is for"
    pattern: '^## '  # Regex for protected content
    note: "Additional guidance"
```

**For append-only with sections:**
```yaml
append_only:
  .harness/my-new-file.yaml:
    description: "What this file is for"
    sections:
      important_section:
        pattern: '- item'
        description: "Items in this section are append-only"
```

**For immutable files:**
```yaml
immutable:
  .harness/my-facts.jsonl:
    description: "Immutable fact store"
    note: "Append new lines only, never modify existing"
```

**For protected files:**
```yaml
protected:
  - .harness/my-core-file.md
```

**For free files:**
```yaml
free:
  - .harness/my-scratch/*
```

### 3. Commit Both Together

```bash
# Create the file
# Edit document-controls.yaml
git add .harness/my-new-file.md .harness/document-controls.yaml
git commit -m "feat: Add my-new-file with append-only protection"
```

## Common Patterns

### Research Documents
```yaml
append_only:
  .harness/research/topic-research.md:
    description: "Research findings on topic"
    pattern: '^## Finding'
    note: "Findings accumulate, never removed"
```

### Status Tracking
```yaml
append_only:
  .harness/status/sprint-1.yaml:
    description: "Sprint 1 status tracking"
    sections:
      completed:
        pattern: '- '
        description: "Completed items never removed"
```

### Reference Documents
```yaml
free:
  - .harness/reference/*
```
Reference material can be freely edited.

## Unregistered File Warnings

The pre-commit hook warns when `.harness/` files aren't registered:

```
⚠️  UNREGISTERED FILES DETECTED:
  [UNREGISTERED] .harness/my-new-file.md

  Add to .harness/document-controls.yaml or the file may be unprotected.
```

This is a warning, not a blocker—but unregistered files have no integrity protection.

## Verification

After registering, verify:

```bash
# Check all protected files exist
python3 .harness/scripts/validate-integrity.py --check

# Full validation
python3 .harness/scripts/validate-integrity.py --full
```

## Quick Reference

| Want to protect... | Add to section |
|-------------------|----------------|
| Entire file from deletion | `append_only` with `pattern: '.*'` |
| Specific content (headers, items) | `append_only` with specific pattern |
| File from any changes | `immutable` |
| File existence only | `protected` |
| Nothing (scratch/temp) | `free` |
