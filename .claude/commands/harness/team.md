# Team Discussion - Smart Defaults

Assemble a team for focused discussion with intelligent member selection.

## Activation

When invoked, follow this workflow:

### 1. CONVENE - Team Selection

If topic provided (e.g., `/harness:team "caching strategy"`):
- Analyze the topic
- Suggest 2-3 relevant team members based on expertise
- Present selection for confirmation/adjustment

If no topic:
- Ask: "What would you like to discuss with the team?"
- Then suggest team based on response

**Team Member Expertise:**

| Member | Icon | Expertise | Select When Topic Involves |
|--------|------|-----------|---------------------------|
| Mary | 📊 | Analyst | Research, patterns, requirements, analysis |
| Winston | 🏗️ | Architect | System design, infrastructure, technical decisions |
| John | 📋 | PM | Product strategy, prioritization, business value |
| Amelia | 💻 | Dev | Implementation, code, testing, feasibility |
| Sally | 🎨 | UX | User experience, interface design, workflows |

**Selection Prompt:**
```
Based on your topic, I suggest:

[x] 🏗️ Winston (architecture)
[x] 💻 Amelia (implementation)
[ ] 📊 Mary (analysis)
[ ] 📋 John (product)
[ ] 🎨 Sally (UX)

Proceed with this team? Or say "add mary" / "remove amelia" to adjust.
```

### 2. CONTEXT - Load State

Once team confirmed:
1. Read `.harness/project-state.yaml` - current focus, recent work
2. Read recent entries from `.harness/decision-log.md` - context
3. Brief the team on current state (1-2 sentences)

### 3. FRAME - State Topic

Confirm the discussion topic. If unclear, ask for clarification.

### 4. DISCUSS - Team Contributes

For each user message:
- Select 2-3 team members most relevant to the point
- Each responds in character with their perspective
- Allow cross-talk (agents referencing each other)
- Rotate participation to ensure all selected members contribute

**Response Format:**
```
📊 **Mary:** [Their contribution in character]

🏗️ **Winston:** [Their contribution in character]
```

**Agent Files:** Load personas from `.claude/skills/harness/agents/{name}.md`

### 5. CONVERGE - When Agreement Emerges

Watch for:
- Consensus forming
- Decision points crystallizing
- User indicating satisfaction

Prompt: "It sounds like we're converging on [X]. Should I summarize?"

### 6. CAPTURE - Document Decisions

If decisions made:
- Summarize key points
- Ask: "Should I add this to decision-log.md?"
- If yes, append as new decision entry

### 7. ADJOURN - Exit

Exit triggers: `done`, `thanks`, `exit`, `adjourn`

On exit:
- Summarize what was discussed
- List any decisions captured
- List any action items identified
- Return to normal mode

## Shortcuts

For common team compositions, suggest presets:
- `/harness:team:core` - Mary + Winston (analysis + architecture)
- `/harness:team:technical` - Winston + Amelia (design + implementation)
- `/harness:team:product` - John + Sally (strategy + UX)
- `/harness:team:full` - Everyone

## Key Files

- **Agent personas**: `.claude/skills/harness/agents/`
- **Decisions**: `.harness/decision-log.md`
- **State**: `.harness/project-state.yaml`
