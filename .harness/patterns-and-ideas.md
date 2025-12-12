# Harness Patterns & Ideas

> Capture interesting patterns, ideas, and techniques discovered during research.
> These may inform future design decisions.

---

## Quick Reference

| Pattern | One-liner | Source |
|---------|-----------|--------|
| Tiered Context Anchoring | Reload RIGHT things at RIGHT time to prevent fade | Party Mode S7 |
| helpers.md | Centralize shared ops, reference via anchors | bmad-skills |
| Level-based methodology | Right-size process for project complexity | bmad-skills |
| 7-step init ritual | Consistent session start via filesystem discovery | Anthropic |
| Immutable task lists | JSON state, only flip pass/fail, never delete | Anthropic |
| Three-layer state | JSON (structured) + MD (unstructured) + Git (history) | Anthropic |
| Fresh windows > compaction | Filesystem discovery beats lossy compression | Anthropic |
| Two-agent pattern | Initializer plans, Coding Agent executes | Anthropic |
| Skills progressive disclosure | SKILL.md first, supporting files on-demand | Claude Code |

---

## Historical Learnings (Sessions 1-3)

> TODO: Consolidate from project-state.yaml sessions 1-3

---

## Session 4 Discoveries (2025-12-11)

### Pattern: helpers.md with Section References

**Source:** claude-code-bmad-skills repo

Instead of embedding instructions in every skill/command, centralize in `helpers.md` and reference via anchors:

```markdown
"Follow helper instructions in utils/helpers.md#Load-Global-Config"
"Execute Step 1-3 from helpers.md#Combined-Config-Load"
```

**Benefits:**
- 70-85% token reduction vs embedded approach
- Single source of truth for shared operations
- Claude loads only referenced sections

**Harness Application:** Create `harness/helpers.md` for shared operations (config loading, state management, git operations).

---

### Pattern: Level-Based Methodology

**Source:** claude-code-bmad-skills repo

Right-size methodology based on project complexity:

```
Level 0 (1 story):      Minimal docs, tech-spec only
Level 1 (1-10 stories): Light docs, tech-spec required
Level 2 (5-15 stories): Full docs, architecture required
Level 3 (12-40 stories): Full docs, architecture required
Level 4 (40+ stories):  Full docs, comprehensive architecture
```

**Benefits:**
- Prevents over-engineering small projects
- Ensures adequate planning for large projects
- Auto-adjusts workflow recommendations

**Harness Application:** Implement project leveling in skill routing logic.

---

### Pattern: 7-Step Initialization Ritual

**Source:** Anthropic autonomous-coding quickstart

Every session starts with explicit discovery:

```
1. pwd                    → Know where you are
2. ls                     → See project files
3. Read state file        → Current status
4. Read task list         → What's done/pending
5. Read progress notes    → Recent activity
6. Check git history      → Recent commits
7. Run baseline test      → Verify nothing broke
```

**Benefits:**
- Consistent session start
- Filesystem discovery vs context stuffing
- Catches regressions immediately

**Harness Application:** Encode in SKILL.md as mandatory init sequence.

---

### Pattern: Immutable Task Lists (JSON)

**Source:** Anthropic long-running agents paper

Task lists should be:
- Stored in JSON (less corruption than Markdown/YAML)
- NEVER delete or edit task descriptions
- Only modify "passes" field from false → true

**Benefits:**
- Prevents scope creep
- Clear progress tracking
- Recovery-friendly

**Harness Application:** Use `task-list.json` instead of markdown checklists.

---

### Pattern: Three-Layer State

**Source:** Claude 4 best practices

Combine three state mechanisms:

```
Layer 1: Structured (JSON)   → Tasks, status, metrics
Layer 2: Unstructured (MD)   → Progress notes, decisions, vision
Layer 3: Git                 → History, recovery, checkpoints
```

**Benefits:**
- Right format for right purpose
- JSON for machine state, MD for human context
- Git for history and rollback

**Harness Application:** Skills route to appropriate layer based on query type.

---

### Pattern: Fresh Windows > Compaction

**Source:** Claude 4 best practices

> "Consider a brand new context window rather than using compaction. Claude 4.5 models are extremely effective at discovering state from the local filesystem."

**Benefits:**
- No lossy compression
- Clean context
- Filesystem discovery is reliable

**Harness Application:** Already decided (D-previous). Recovery hook bridges sessions.

---

### Pattern: Two-Agent Architecture

**Source:** Anthropic long-running agents paper

Separate concerns:
- **Initializer Agent:** Plans, creates structure, establishes guardrails
- **Coding Agent:** Executes incrementally, one feature at a time

**Benefits:**
- Planning doesn't compete with execution for context
- Clear handoff protocol
- Prevents "over-ambition" failure mode

**Harness Application:** Maps to BMAD's Analyst/PM/Architect (plan) vs Dev (execute).

---

### Pattern: Skills Progressive Disclosure

**Source:** Claude Code skills documentation

```
SKILL.md loaded first (minimal)
    ↓
Supporting files loaded on-demand
    ↓
Deep reference docs only when needed
```

**Benefits:**
- Model-invoked (Claude decides when)
- Token efficient
- Native to Claude Code

**Harness Application:** Core of our D12 architecture decision.

---

## Ideas for Future Exploration

### Meta-Skill Library
A single skill that knows how to find and invoke other skills. Like a "tool search tool" but for skills.

### Session Profiles
Detect session "character" from tool usage patterns:
- Heavy edits = Implementation session
- Heavy reads = Research session
- Heavy git = DevOps session

Use profile to adjust behavior/suggestions.

### Verification Tools
Anthropic emphasizes browser automation (Puppeteer) for verification. Could Harness include verification patterns for different project types?

---

## Session 5 Open Questions (2025-12-12)

> These emerged from Session 5 after implementing atom extraction (267 atoms from 16 transcripts).
> Each is a significant design decision - schedule dedicated sessions.

### Q1: SDLC Stage Awareness

**Question:** Should atoms be tagged with project/SDLC stage? Does `[DECISION]` mean something different in Discovery vs Implementation?

**Why it matters:**
- An exploratory decision may change; an implementation decision is committal
- Stage context affects how we weight/surface atoms
- Could enable "show me all architecture decisions from design phase"

**Considerations:**
- How do we know current stage? Manual tag? Auto-detect from patterns?
- Does stage apply to session or to individual atoms?
- Taxonomy extension needed: `stage: discovery | design | implementation | maintenance`

---

### Q2: Auto-Populate Documents from Atoms

**Question:** Can/should atoms auto-populate documents like decision-log.md, patterns-and-ideas.md?

**Why it matters:**
- Manual documentation is a bottleneck
- Atoms already contain the information
- Could reduce "end of session capture" burden

**Risk assessment:**

| Approach | Risk | Value |
|----------|------|-------|
| Auto-write to docs | HIGH - overwrites human judgment | Low trust |
| Draft for review | LOW - human approves | High efficiency |
| Suggest only | NONE - just flags | Medium help |

**Recommendation:** Start with "draft" mode - generate but don't commit. Human promotes.

---

### Q3: Conversation Visualization (Mind Map)

**Question:** Can we visualize the conversation/atoms as a mind map or network graph?

**Why it matters:**
- Spatial understanding reveals patterns not obvious in lists
- Shows how topics cluster and connect
- Could aid onboarding - "here's what this project discussed"

**Technical options:**
- **Obsidian** - Markdown + graph view (existing tool)
- **Mermaid** - In-markdown diagrams (portable)
- **D3.js** - Custom visualization (flexible)
- **Markmap** - Markdown → mind map (simple)

**Data already exists:** Atoms have keywords. Keywords = edges. Sessions = clusters.

---

### Q4: Knowledge Graph Structure

**Question:** Is the atom system suitable for a proper knowledge graph? What schema?

**Why it matters:**
- Graph queries more powerful than keyword grep
- Relationships between atoms not currently captured
- Could enable: "What led to decision D12?" (trace the reasoning chain)

**Proposed schema:**
```
Atom → has_type → DECISION
Atom → has_keyword → 'skills'
Atom → from_session → Session
Atom → followed_by → Atom (temporal)
Atom → relates_to → Atom (semantic)
Session → has_stage → Stage
Pattern → extracted_from → [Atom...]
```

**Tools:** Neo4j (full graph DB), SQLite + JSON (lightweight), Pure JSONL + query scripts

---

### Q5: Pattern Library / Architecture Repository

**Question:** How do we promote atoms to reusable patterns? What's the curation workflow?

**Why it matters:**
- Not every atom is a pattern - human judgment needed
- Validated patterns should be easily discoverable
- Could build institutional knowledge across projects

**Proposed flow:**
```
Atom extracted (tagged PATTERN or ARCHITECTURE)
    ↓
Human reviews, validates, generalizes
    ↓
Promoted to .harness/library/ or .harness/patterns/
    ↓
Available for future projects (cross-project knowledge)
```

**Open sub-questions:**
- What makes an atom "pattern-worthy"?
- How to generalize from specific context?
- Cross-project pattern sharing mechanism?

---

### Q6: Meta-Design - How These Fit Together

**Question:** What's the unified architecture for stage awareness + auto-docs + visualization + graph + patterns?

**Sketch (needs validation):**

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION CONVERSATION                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              ATOM EXTRACTION (taxonomy.yaml)                 │
│  - Types: DECISION, ERROR, ACTION, INSIGHT, etc.            │
│  - Keywords: project vocabulary                              │
│  - Stage: discovery | design | implementation | maintenance  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ATOM STORE (atoms.jsonl)                  │
│  - Queryable knowledge base                                  │
│  - Temporal ordering preserved                               │
│  - Cross-session searchable                                  │
└─────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   QUERY/VIEW    │  │  AUTO-DRAFT     │  │   KNOWLEDGE     │
│                 │  │                 │  │   GRAPH         │
│ - Topic search  │  │ - Draft docs    │  │                 │
│ - Mind map      │  │ - Human review  │  │ - Relationships │
│ - Timeline      │  │ - Promote/reject│  │ - Trace chains  │
│ - Stage filter  │  │                 │  │ - Visualize     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PATTERN LIBRARY                           │
│  - Curated, validated patterns                               │
│  - Cross-project reusable                                    │
│  - Human-promoted from atoms                                 │
└─────────────────────────────────────────────────────────────┘
```

**Priority for exploration:**
1. Stage awareness (taxonomy extension) - enables filtering
2. Auto-draft docs (low risk experiment)
3. Visualization (Mermaid/Markmap for quick win)
4. Knowledge graph (larger investment, defer?)
5. Pattern library (needs curation process first)

---

### Q7: Idea & Question Lifecycle Management

**Question:** How do we capture and track ideas/questions that aren't immediately acted on? How do they evolve, connect, and resurface?

**Why it matters:**
- Ideas disappear if not immediately acted on
- Questions may get answered later but aren't tracked back
- Connections between ideas emerge over time
- Some "parked" ideas become relevant with new context
- Bulk research/review of accumulated questions is valuable

**Proposed stores:**

| Store | Contents | Lifecycle States |
|-------|----------|------------------|
| `questions.yaml` | Open questions | pending → answered \| obsolete |
| `ideas.yaml` | Unvalidated ideas | captured → exploring → promoted \| parked |
| `features.yaml` | Potential capabilities | backlog → planned → implemented |
| `roadmap.yaml` | Strategic items | future → current → done |

**Self-organization signals:**

| Signal | Meaning | Action |
|--------|---------|--------|
| Mentioned multiple times | High relevance | Surface as "hot" |
| Connected to many atoms | Central concept | Highlight as hub |
| Referenced in decisions | Validated importance | Promote priority |
| Never revisited (N sessions) | Possibly obsolete | Flag for review |
| New atoms connect to old idea | Idea gaining relevance | Resurface |

**Proposed schema:**
```yaml
ideas:
  - id: IDEA-001
    created: 2025-12-12
    session_origin: auto-recovery-20251212
    status: captured  # captured | exploring | promoted | parked | obsolete
    title: "Meta-skill library"
    description: "A skill that knows how to find other skills"
    connections:
      atoms: [atom-123, atom-456]
      questions: [Q3]
      ideas: [IDEA-005]
      decisions: [D12]
    mentions: 3
    last_mentioned: 2025-12-12
    priority: null  # null until ranked, then 1-5
    notes:
      - date: 2025-12-12
        note: "Could combine with skill routing"
```

**Automation possibilities:**
- Auto-capture from atoms tagged `PROPOSAL` or `QUESTION`
- Track mention frequency across sessions
- Compute "heat" score from connections + recency
- Weekly digest: "Hot ideas", "Answered questions", "Stale items"
- Bulk research mode: "Show all unanswered questions about X"

**Key insight:** Ideas are living things. They connect, evolve, hibernate, and sometimes resurrect. The system should support this lifecycle, not just capture-and-forget.

---

### Q8: DIKW Maturity Model for Atoms

**Question:** How do we incorporate Data → Information → Knowledge → Wisdom lifecycle into atom management?

**The DIKW Pyramid:**
```
        WISDOM (principles, judgment)
       /                            \
    KNOWLEDGE (connected, validated)
   /                                  \
  INFORMATION (typed, contextualized)
 /                                      \
DATA (raw transcripts, JSONL)
```

**Mapping to Harness:**

| DIKW Level | Harness Equivalent | Maturity State |
|------------|-------------------|----------------|
| Data | Session JSONL, raw transcripts | (pre-extraction) |
| Information | Atoms - typed, keyworded | `extracted` |
| Knowledge | Validated atoms, patterns | `synthesized` |
| Wisdom | vision.md principles, decisions | `principled` |

**Proposed atom maturity field:**
```yaml
atom:
  maturity: extracted  # extracted | synthesized | principled
  promoted_to: null    # e.g., 'vision.md#principle-5'
  validated_by: null   # human or session that validated
  validated_at: null   # timestamp
```

**Lifecycle flow:**
```
Raw transcript (DATA)
    ↓ auto-extraction
Atom created (INFORMATION) - maturity: 'extracted'
    ↓ human reviews, connects
Atom validated (KNOWLEDGE) - maturity: 'synthesized'
    ↓ promoted to principles
In vision.md (WISDOM) - maturity: 'principled'
```

**Value:**
- Track knowledge maturation over time
- Distinguish trusted (synthesized) from raw (extracted)
- Know what's become principled wisdom
- Query by maturity: "Show all synthesized patterns not yet in library"

**Added to taxonomy.yaml:** `maturity_levels` section with DIKW mapping.

---

## Session 7 Discoveries (2025-12-12)

### Pattern: Tiered Context Anchoring

**Source:** Party Mode discussion - John, Winston, Mary, Dr. Quinn, Amelia

**Problem:** In extended conversations, critical context "fades" as it gets pushed back in the attention window:
- Agent personas drift toward generic responses
- Project state assumptions become outdated
- Decisions get re-litigated
- File contents read early are forgotten/hallucinated

**Root Cause:** LLMs have a flat context buffer doing the job of working memory, short-term memory, AND long-term memory. Recent tokens get more attention weight than distant ones.

**Solution: Stratified Reinforcement**

```
┌─────────────────────────────────────────────┐
│           CONTEXT TIERS                      │
├─────────────────────────────────────────────┤
│ TIER 1: ALWAYS FRESH (reload every N turns) │
│   • Agent persona (who am I?)               │
│   • Current task/goal (what am I doing?)    │
│   • Active constraints (what can't I do?)   │
├─────────────────────────────────────────────┤
│ TIER 2: CHECKPOINT REFRESH (at transitions) │
│   • project-state.yaml                      │
│   • Recent decisions from decision-log.md   │
│   • Files actively being edited             │
├─────────────────────────────────────────────┤
│ TIER 3: ON-DEMAND (pull when referenced)    │
│   • Historical decisions                    │
│   • Other project files                     │
│   • Documentation                           │
└─────────────────────────────────────────────┘
```

**What Fades (by severity):**

| Context Type | Fade Rate | Impact When Lost |
|--------------|-----------|------------------|
| Project state | Fast | Wrong assumptions, outdated info |
| Decision history | Fast | Re-litigating settled decisions |
| File contents read early | Very Fast | Hallucinated code, wrong patterns |
| Agent personas | Medium | Personality drift, generic responses |
| Current task/goal | Medium | Scope creep, tangents |
| Constraints/boundaries | Fast | Violating established rules |
| User preferences | Medium | Tone/style drift |

**Implementation Approaches:**

| Approach | Token Cost | Effectiveness | Complexity |
|----------|------------|---------------|------------|
| Full agent reload | High | High | Low |
| Anchor reminders (lightweight summary) | Low | Medium | Medium |
| Shorter sessions | Zero | High | Zero |
| Hybrid (anchors + periodic full reload) | Medium | High | Medium |
| Turn-based hook auto-injection | Medium | High | Medium |

**Proposed Implementation:**

```yaml
# .harness/context-anchors.yaml
anchors:
  always_reload:
    - path: "CLAUDE.md"
      frequency: 15  # every 15 turns
    - path: ".harness/project-state.yaml"
      frequency: 10
    - path: "active-agent-file"  # dynamic
      frequency: 10

  conditional_reload:
    - trigger: "architecture|design|system"
      path: ".harness/decision-log.md"
      filter: "grep -A5 'Architecture'"
    - trigger: "goal|objective|scope"
      path: ".harness/project-state.yaml"
      section: "current_focus"
```

**Key Insight:** It's not "reload more" vs "reload less" - it's **reload the RIGHT things at the RIGHT time.**

**Wishlist for Anthropic:**
- Explicit memory tiers / "pin this" markers
- Selective compaction control
- Attention weighting hints
- Cross-session memory primitives

**Harness Application:**
1. `/refresh` command - manual context reload trigger
2. Turn-based hook - automatic anchor injection every N turns
3. Topic-aware triggers - reload relevant decisions when topics arise

---

## Sources Referenced

1. **Claude Code Skills:** https://code.claude.com/docs/en/skills
2. **Long-Running Agents:** https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
3. **Claude 4 Best Practices:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
4. **Autonomous Coding Quickstart:** https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding
5. **Advanced Tool Use:** https://anthropic.com/engineering/advanced-tool-use
6. **BMAD Skills Implementation:** https://github.com/aj-geddes/claude-code-bmad-skills
7. **Superpowers (PRIORITY):** https://github.com/obra/superpowers
   - Complete workflow system for AI coding agents
   - Skills as mandatory workflows (not optional)
   - Subagent coordination, git worktrees, Socratic brainstorming
   - Multi-platform: Claude Code, Codex, OpenCode
   - **TODO: Deep dive next session - highly relevant prior art**
8. **Spec Kit:** https://github.com/github/spec-kit
   - Constitution pattern for immutable project rules
   - Spec/Plan separation (What vs How)
   - Referenced in HBMAD draft - needs research
9. **HBMAD Architecture Draft:** `.harness/reference/hbmad-architecture-draft.md`
   - User's pre-Harness synthesis of BMAD + Anthropic + Spec Kit
   - Vision document for what Harness aims to become
   - Status: Pre-validation, needs updates with Session 4 learnings

---
