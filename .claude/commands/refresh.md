---
name: 'refresh'
description: 'Reload critical context to prevent memory fade in long conversations'
---

# Context Refresh Protocol

You are executing a context refresh to combat attention fade in extended conversations.

## Why This Matters

In long conversations, early context fades from active attention. This causes:
- Agent persona drift (generic responses)
- Forgotten project state (wrong assumptions)
- Re-litigating settled decisions
- Hallucinated file contents

## Refresh Procedure

Execute these steps IN ORDER:

### 1. Reload Project State
Read and acknowledge: `.harness/project-state.yaml`
- Current phase, focus, blockers
- What we're working on RIGHT NOW

### 2. Reload Key Decisions
Read and acknowledge recent entries from: `.harness/decision-log.md`
- Focus on last 3-5 decisions
- Note any that are relevant to current conversation

### 3. Reload CLAUDE.md
Read and acknowledge: `CLAUDE.md`
- Core principles
- Session protocols

### 4. Reload Active Agent(s)

**If in party mode**, reload ALL participating agents:
- `.bmad/core/agents/bmad-master.agent.yaml` (BMad Master)
- `.bmad/modules/bmm/agents/pm.agent.yaml` (John)
- `.bmad/modules/bmm/agents/architect.agent.yaml` (Winston)
- `.bmad/modules/bmm/agents/analyst.agent.yaml` (Mary)
- `.bmad/modules/bmm/agents/dev.agent.yaml` (Amelia)
- `.bmad/modules/cis/agents/creative-problem-solver.agent.yaml` (Dr. Quinn)

**If single agent mode**, re-read that agent's file to restore persona.

**If no agent active**, skip this step.

### 5. Summarize Refresh
After reading, provide a brief summary:
```
## Context Refreshed

**Project State:** [current phase/focus]
**Recent Decisions:** [relevant ones]
**Active Agent:** [if any]
**Ready to continue:** [current task]
```

## Usage Notes

- Use `/refresh` when you notice drift or confusion
- Use `/refresh` proactively every 20-30 turns in long sessions
- Use `/refresh` after returning from a tangent
- Combine with `/context` to check budget before/after
