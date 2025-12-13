---
name: team
description: Team discussion workflow with adaptive structure. Assembles selected team members for collaborative discussion. Uses progressive structure (light by default, adds phases when complexity demands) and progressive capture (continuous, don't wait for end). Use when a topic needs multiple expert perspectives.
---

# Team Discussion Workflow

Multi-agent discussion with intelligent team selection and adaptive structure.

## When to Use

- Topic needs multiple expert perspectives
- Making architectural or strategic decisions
- Brainstorming solutions to complex problems
- Reviewing proposals that span multiple domains

## Team Members

> Defined in `./agents/`. Load dynamically based on selection.

When assembling, read each agent's frontmatter for: icon, name, role, description.

## Workflow (Adaptive)

### Default (Light Mode)

```
CONTEXT → FRAME → DISCUSS → CONVERGE → CAPTURE
```

### Escalated (Structured Mode)

```
CONTEXT → FRAME → [DIVERGE → ANALYZE] → CONVERGE → CAPTURE
```

### Phases

| Phase | Purpose |
|-------|---------|
| **CONTEXT** | Search past discussions (decision-log, atoms), load project state |
| **FRAME** | Clarify: problem, success criteria, constraints |
| **DIVERGE** | Generate all options, suspend judgment |
| **ANALYZE** | Evaluate each option: pros, cons, risks |
| **CONVERGE** | Decide + document what we DIDN'T pick |
| **CAPTURE** | Rich output (continuous throughout) |

### Escalation Triggers

Shift from light → structured when:
- 3+ options mentioned → suggest DIVERGE
- Disagreement between agents → suggest ANALYZE
- User says "important" / "critical" → offer full structure
- Architecture/strategy topic → auto-suggest structure

## Progressive Capture

**DON'T wait for "done".** Capture as insights emerge:

| When | Action |
|------|--------|
| Decision crystallizes | → Append to `decision-log.md` NOW |
| New idea emerges | → Add to `ideas.yaml` NOW |
| Question surfaces | → Add to `questions.yaml` NOW |
| Topic concludes | → Summarize before moving on |

## Discussion Controls

### Response Format

Each agent responds with icon and name:
```
📊 **Mary:** [Their contribution in character]

🏗️ **Winston:** [Their contribution in character]
```

### Agent Selection Per Round

- Analyze message/topic
- Select 2-3 most relevant agents
- Rotate to ensure diverse participation
- Include agent if addressed by name

### Pause for User

When an agent asks the user a question:
- End that response round
- Wait for user input
- Resume with new context

### Cross-talk

Agents can:
- Reference each other's points
- Respectfully disagree
- Build on contributions
- Ask each other questions

## Rich Capture Format

When capturing decisions:

```markdown
## Decision: [Title]
**Decision:** X
**Alternatives Considered:**
- Y: rejected because...
**Concerns Noted:** (even if we proceeded)
**Assumptions:** (can revisit if wrong)
**Spawned:**
- IDEA-XXX: [description]
- Q-XXX: [question]
```

## Invocation

| Method | Command |
|--------|---------|
| Smart selection | `/harness:team` or `/harness:team "topic"` |
| Core preset | `/harness:team:core` (Mary + Winston) |
| Technical preset | `/harness:team:technical` (Winston + Amelia) |
| Product preset | `/harness:team:product` (John + Sally) |
| Full team | `/harness:team:full` (everyone) |
| Natural language | "discuss X with the team" |

## Key Files

- **Agent personas**: `./agents/`
- **Decisions**: `.harness/decision-log.md`
- **Ideas**: `.harness/ideas.yaml`
- **Questions**: `.harness/questions.yaml`
- **State**: `.harness/project-state.yaml`
