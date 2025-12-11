# Harness Retrospective Process

> How to extract knowledge from session history. Designed and validated in Session 5.

## When to Run

- Periodically (e.g., every 5-10 sessions)
- Before major design decisions
- When context feels fragmented
- When starting fresh after a break

## The Process

### 1. Inventory Sessions

```bash
ls -la .harness/transcripts/
```

Count transcripts, note date range, identify gaps.

### 2. Run Atom Extraction

```bash
python3 .harness/scripts/extract-atoms.py --reprocess
```

This will:
- Parse all transcripts
- Apply taxonomy.yaml types and keywords
- Output to atoms.jsonl
- Show summary by type and session

### 3. Review Type Distribution

```bash
python3 -c "
import json
from collections import Counter
types = Counter()
with open('.harness/atoms.jsonl') as f:
    for line in f:
        atom = json.loads(line)
        types[atom['primary_type']] += 1
for t, c in types.most_common():
    print(f'{t}: {c}')
"
```

Look for:
- High DECISION count = many choices made
- High ERROR count = debugging sessions
- High QUESTION count = exploration phase
- High IDEA count = brainstorming phase

### 4. Query Specific Topics

```bash
# Find all atoms about a topic
python3 -c "
import json
TOPIC = 'skills'  # change this
with open('.harness/atoms.jsonl') as f:
    for line in f:
        atom = json.loads(line)
        if TOPIC in atom['keywords']:
            print(f\"[{atom['primary_type']}] {atom['content'][:100]}...\")
"
```

### 5. Populate Lifecycle Stores

Extract from atoms to structured stores:

```bash
# IDEAs → ideas.yaml
grep -l '"IDEA"' atoms.jsonl  # or use Python

# OPEN_QUESTIONs → questions.yaml
# Review and add to questions.yaml manually
```

### 6. Update Documentation

Based on findings:
- New decisions → decision-log.md
- New principles → vision.md
- New patterns → patterns-and-ideas.md
- Open questions → questions.yaml
- Ideas to explore → ideas.yaml

### 7. Check Sync Status

```bash
# What's in decision-log but not in vision.md?
python3 .harness/scripts/session-recovery.py
```

Look for "SYNC NEEDED" warnings.

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Atoms | `.harness/atoms.jsonl` | Queryable knowledge base |
| Ideas | `.harness/ideas.yaml` | Tracked possibilities |
| Questions | `.harness/questions.yaml` | Open research items |
| Patterns | `.harness/patterns-and-ideas.md` | Validated approaches |

---

## Session 5 Example

**Input:** 16 transcripts across ~5 days

**Process:**
1. Read all transcripts (in-context for analysis)
2. Designed taxonomy (10 core + 5 domain types)
3. Built extract-atoms.py
4. Ran extraction → 267 atoms
5. Queried topics (e.g., "skills" → 11 atoms)
6. Created ideas.yaml (8 ideas) and questions.yaml (10 questions)
7. Captured 8 open questions (Q1-Q8) in patterns-and-ideas.md

**Output:** Complete knowledge extraction system + bootstrapped stores

---

## Tips

- **Context matters**: Do retrospectives when you have context space to read transcripts
- **Batch processing**: The extraction script runs outside context (minimal cost)
- **Topic queries**: Use keywords to trace threads across sessions
- **Don't discard**: Even "micro-test" sessions may contain valuable atoms
- **Multi-type**: Atoms can have multiple types - query by any of them

---

*Created: Session 5 (2025-12-12)*
