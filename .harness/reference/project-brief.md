# Harness Project Brief (Archived)

> **ARCHIVED per D18 (Session 10):** This file preserves the original vision.md content for historical reference. It is NOT active documentation. See CLAUDE.md for operational context and decision-log.md for principles.

---

# Harness Vision

> **TL;DR:** A synthesis of the best methodologies humanity has developed - evaluated rigorously, not adopted blindly - designed for modern AI-assisted product lifecycle management.

## The Name

**Harness** - Just as ancient humanity harnessed the horse to build civilization, we now harness AI to build the future. The harness doesn't limit the horse's power - it **channels** it productively. Humans provide controls and constraints to channel AI power.

## What Harness Is

**Harness is NOT a child of BMAD** or any single methodology. It is the combined learnings from:
- Research into every methodology humans have used (Lean, Agile, Waterfall, etc.)
- Anthropic's patterns for long-running agents and autonomous coding
- Claude Code native features (Skills, hooks, CLAUDE.md)
- BMAD's agent-based approach (promising but not foundational)
- Superpowers and other emerging AI-native tools
- First-principles questioning of WHY each practice exists

Harness is **methodology-agnostic by design**. All approaches are inputs to be evaluated, validated, and synthesized - not doctrines to follow.

## Why We're Building This

### The Problem with Current Approaches
- Existing methods adapt **human** development practices for AI assistance
- No one has asked: "What methodology would we design WITH AI collaboration in mind?"
- Existing methodologies (Lean, Agile, etc.) were created to solve **human** problems:
  - Lean: Eliminate waste because **human dev is expensive** → But AI dev is cheap
  - Agile: Respond to change because **humans are slow** → But AI is fast
  - Waterfall: Reduce rework because **human rework is costly** → But AI rework is cheap

### The Opportunity
- AI changes fundamental economics of software development
- Creation cost → near zero
- New bottlenecks: validation, testing, integration, human oversight
- Need methodology designed FOR these new constraints

## The Hypothesis (Flexible - Let Research Guide)

Initial thinking suggests layers (but research may reveal different structure):

1. **SDLC Methodology** - First-principles lifecycle for AI-native development
2. **Specification & Control** - Documents, workflows, task management for AI
3. **Testing Mechanisms** - Comprehensive validation (testing is now cheap)
4. **Progressive Architecture Disclosure** - Code + docs structured for AI comprehension
5. **Harness Controls** - Orchestration preventing context collapse, maintaining coherence

**IMPORTANT:** These are hypotheses, NOT conclusions. Research may reveal 3 layers, 7 layers, or a completely different structure.

## Research Approach

Analyze existing methodologies to extract:
- WHY each practice was created
- WHAT assumption it makes about cost/humans/technology
- WHETHER that assumption holds in AI age
- WHAT transfers, transforms, or becomes obsolete

### Methodologies to Analyze (~20)

**Traditional:**
- Waterfall, V-Model, Spiral
- RUP, DSDM, FDD

**Agile Family:**
- Agile Manifesto/Principles, Scrum, Kanban
- XP (Extreme Programming), Crystal

**Lean/Flow:**
- Lean Software Development ✅ (analyzed session 1)
- Theory of Constraints, Kanban (detailed)

**Scaled:**
- SAFe, LeSS, Nexus

**Modern:**
- DevOps, SRE practices
- Shape Up, Basecamp's approach

**AI-Native (emerging):**
- BMAD Method
- Anthropic's agent patterns
- Other emerging AI dev frameworks

## Success Criteria

Harness succeeds if:
1. A fresh AI session can execute the methodology from docs alone
2. Context loss doesn't derail projects (state persists externally)
3. 24+ hour autonomous operation is possible (like Anthropic's harness paper)
4. The methodology is DESIGNED for AI constraints, not adapted from human methods

## Core Principles (Historical - see decision-log.md for current)

### From Session 1:
- **Prevention > Recovery** - Make data loss impossible, not recoverable
- **Context is ephemeral** - Nothing valuable exists only in context
- **Sub-agents write directly** - Don't return data to orchestrator
- **Progressive disclosure** - Layer 0 → Layer 1 → Layer 2
- **Validate before proceeding** - Checklists, not assumptions

### From Session 2:
- **Documentation IS memory** - If it's not documented, it doesn't exist
- **Transcripts are essential** - Raw conversation is recoverable context
- **Capture is MANDATORY** - End-of-session checklist, not optional

### From Session 3:
- **Recovery is automated** - SessionStart hook, not manual checking
- **Master coordinates recovery** - Single entry point for context restoration
- **Lightweight detection, opt-in depth** - Hook flags, Master analyzes

### From Session 4 (D12):
- **Skills-based architecture** - Claude Code native features over custom infrastructure
- **Filesystem discovery > context stuffing** - Let Claude find state, don't preload everything
- **Atoms as knowledge units** - Extract granular insights, not whole sessions
- **Living taxonomy** - Classification evolves with project vocabulary
- **Fresh sessions preferred** - New context window over compaction (per Anthropic best practices)

### From Session 7 (D13):
- **Single source of truth** - One config location (`.harness/project.yaml`), symlinks for compatibility
- **Strangler Fig transitions** - Gradual migration without breaking existing workflows
- **BMAD as optional module** - Source material, not foundation; Harness works without it

### From Session 7 (D14):
- **Skills as universal architecture** - All capabilities (personas, workflows, toolbox, knowledge) become Skills
- **Model-invoked > user-invoked** - Claude decides when to load, not slash commands
- **Design for ephemeral context** - Personas fade; load fresh when relevant
- **helpers.md pattern** - Shared operations referenced, not embedded (70-85% token savings)

---

*Original file: 00-governance/vision.md*
*Created: 2025-12-10 (Session 1, emergency capture at 102% context)*
*Archived: 2025-12-13 (Session 10, per D18)*
