# Harness Journey Journal

This folder captures the **narrative history** of Harness development - the story of how we got here.

## What Goes Where?

| Location | Purpose | Style |
|----------|---------|-------|
| `../decision-log.md` | Formal decisions with rationale | Structured (ADR-like) |
| `../lessons-learned.md` | Failures and what we learned | Post-mortem format |
| `../patterns-and-ideas.md` | Patterns discovered/proposed | Pattern catalog |
| `sessions/` | Session narratives | Storytelling, contextual |
| `decisions/` | Reserved for expanded ADRs | (if needed for complex decisions) |

## Session Journal Format

Each session entry in `sessions/` follows this structure:

```markdown
# Session N - YYYY-MM-DD

## Context
- Where we left off
- Session goals

## Key Discussions
- Topics explored (brief bullets)

## Decisions Made
- [D##] Reference to decision-log.md entries

## Lessons Learned
- [L##] Reference to lessons-learned.md entries (if applicable)

## Artifacts Created
- Files created/modified this session

## Open Questions
- Unresolved items for future sessions

## Next Session
- Recommended starting point
```

## Why Keep a Journal?

1. **Decisions lack context** - The log says WHAT, journal says WHY and HOW we got there
2. **Onboarding** - New contributors can read the journey, not just the destination
3. **Recovery** - If transcripts are lost, journal preserves the narrative
4. **Reflection** - Patterns emerge when you see the story unfold

## Relationship to Transcripts

- `../transcripts/` = Raw session exports (verbose, complete)
- `sessions/` = Curated narrative (readable, essential)

The journal distills transcripts into the parts worth preserving long-term.
