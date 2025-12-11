# HBMAD Architecture Draft (Pre-Validation)

> **Status:** Early draft requiring research, validation, and refinement
> **Author:** User (pre-Harness exploration)
> **Date:** ~December 2025
> **Note:** This synthesizes BMAD + Anthropic Harness + Spec Kit concepts.
> Session 4 research validated many patterns independently.

---

## Relevance to Harness

This paper captures the VISION for what Harness aims to become. Key validated concepts:

- Context Window Problem framing ✅
- Externalized state (JSON + MD + Git) ✅
- Two-Agent pattern (Initializer/Coding) ✅
- Scale-adaptive methodology (Levels 0-4) ✅
- Artifact-driven handoffs ✅
- Constitutional enforcement ✅

**Not yet validated:**
- Spec Kit integration (needs research)
- Knowledge Graph extension (future)
- Full hook implementations (needs prototyping)
- Enterprise/Security tracks (needs definition)

**Updates needed based on Session 4:**
- Add Skills-based architecture (native Claude Code)
- Add helpers.md pattern (token efficiency)
- Add Superpowers integration points
- Simplify for progressive disclosure

---

## Original Paper

# **Harnessed BMAD (HBMAD) Architecture: A Unified Framework for Long-Running, Autonomous Software Development**

## **Executive Summary**

The paradigm of software engineering is undergoing a seismic shift from human-centric coding assisted by AI to AI-centric autonomous development supervised by humans. However, this transition faces a critical theoretical and practical barrier known as the **Context Window Problem**. While modern Large Language Models (LLMs) like Claude 3.5 Sonnet exhibit reasoning capabilities that rival senior engineers within a single session, they suffer from catastrophic amnesia and "context drift" over the extended lifecycles required to build complex enterprise software. As a project scales, the sheer volume of code, architectural decisions, and state changes exceeds the model's finite token limit, causing the agent to lose the "strategic thread," hallucinate interfaces, and degrade into incoherent "vibe coding."

This report presents the comprehensive design and architectural specification for **Harnessed BMAD (HBMAD)**, a novel, synthesized framework engineered to solve the Context Window Problem. HBMAD does not merely extend the context window; it fundamentally restructures the agentic workflow by integrating three cutting-edge methodologies into a cohesive, self-correcting operational system:

1. **The BMAD Method (Cognitive Architecture):** Provides the macro-level process governance through a 4-Phase Lifecycle and a team of 19 specialized Agent Personas (e.g., Product Manager, Architect, Test Architect).
2. **Anthropic Harness Discipline (Execution Architecture):** Provides the micro-level execution environment, enforcing strict state management via artifact-driven handoffs (feature_list.json, claude-progress.txt) and a "Two-Agent" initialization model.
3. **Spec Kit Governance (Normative Architecture):** Provides the "Conscience" of the system through the Constitution Pattern (constitution.md) and the rigid separation of Specification (Spec) from Implementation (Plan), ensuring architectural integrity persists across thousands of autonomous sessions.

By harnessing the specialized expertise of BMAD agents within the rigorous, state-preserving session management of Anthropic's protocols, and governing their decisions through Spec Kit's constitutional frameworks, HBMAD enables truly long-running, self-healing, and architecturally consistent autonomous software development.

---

## **1. The Context Window Crisis in Autonomous Development**

### **1.1 The Theoretical Barrier: Finite Context and Attention Decay**

The fundamental unit of interaction with an LLM is the "Session" or "Context Window." Within this window, the model maintains perfect recall and reasoning. However, complex software projects generate information far exceeding the capacity of even the largest commercial context windows.

When an autonomous agent attempts to "hold" the entire project context in memory, it encounters several degradation phenomena:

* **Recall Degradation ("Lost in the Middle"):** Information buried in the middle of a massive context prompt is often ignored or hallucinated.
* **Context Drift:** As the session progresses, the initial architectural constraints are diluted by the noise of subsequent code generation.
* **The One-Shot Fallacy:** Naive agents often attempt to generate entire complex features in a single pass, leading to truncated code and logic errors.

### **1.2 The Failure of Unharnessed Agents**

Common failure modes include:

1. **Premature Victory:** The agent implements a surface-level feature, sees no syntax errors, and marks the task as "Complete" without rigorous verification.
2. **Architectural Entropy:** Without a persistent "Super-Ego" or Constitution, the agent drifts towards the path of least resistance.
3. **The "Amnesiac" Loop:** An agent encounters a bug, fixes it, but introduces a regression. Without persistent history of failed attempts, the system enters an infinite loop.

### **1.3 The Solution: Externalized State and Harnessed Execution**

The solution is not to wait for infinite context windows, but to treat the context window as a temporary "scratchpad." The true state of the project must be externalized into a rigorous file-based schema—the "Harness."

The Harness manages:
* **Context Injection:** Loading only the relevant state for the specific task
* **State Persistence:** Forcing the agent to write its "memories" to structured files
* **Constitutional Enforcement:** Injecting non-negotiable rules into every session

---

## **2. The Three Pillars of HBMAD Architecture**

### **2.1 Pillar I: The BMAD Method (The Cognitive Architecture)**

#### **2.1.1 The 4-Phase Lifecycle**

1. **Analysis (Phase 1):** Explore the problem space, conduct market research, define product vision.
2. **Planning (Phase 2):** Create PRDs and Technical Specifications.
3. **Solutioning (Phase 3):** Design system architecture, data models, and UX flows.
4. **Implementation (Phase 4):** Story-driven development where code is written, tested, and validated.

#### **2.1.2 The 19 Specialized Agent Personas**

Key agents include: Analyst, PM, Architect, Test Architect, UX Designer, Developer, Code Reviewer, Scrum Master, BMad Master.

### **2.2 Pillar II: The Anthropic Harness Discipline (The Execution Architecture)**

#### **2.2.1 The Two-Agent Model**

1. **Initializer Agent:** Bootstraps repository, creates init.sh, generates initial feature_list.json.
2. **Coding Agent:** Iterative agent that picks single tasks, implements, verifies, and hands off.

#### **2.2.2 Artifact-Driven State Management**

* **feature_list.json:** Central backlog tracking every feature's status.
* **claude-progress.txt:** Narrative "Flight Recorder" - diary entry at end of session.
* **init.sh:** Standardized "boot" script for environment setup.
* **Git History:** Ultimate source of truth.

### **2.3 Pillar III: Spec Kit Governance (The Normative Architecture)**

#### **2.3.1 The Constitution Pattern**

Non-negotiable laws of the project, injected into every agent session.

#### **2.3.2 Separation of Spec and Plan**

* **Spec:** Pure requirements and user value (no implementation details).
* **Plan:** Pure technical implementation (libraries, schemas, algorithms).

---

## **3. The HBMAD State Layer (The "Memory Bank")**

### **3.2.1 The Constitution (.specify/memory/constitution.md)**

Immutable rules of engagement. Updated only by Architect or BMad Master.

### **3.2.2 The Unified Workflow Status (bmm-workflow-status.yaml)**

```yaml
project_level: 2 # Scale-Adaptive Track (0-4)
current_phase: "Implementation"
governance:
  constitution_hash: "sha256..."
phases:
  analysis:
    status: "complete"
    artifact: "specs/product_brief.md"
  # ...
backlog:
  - id: "FEAT-001"
    name: "User Authentication"
    status: "pending"
    verification_steps: "Run npm test auth"
```

### **3.2.3 The Narrative Progress Log (claude-progress.txt)**

Chronological, human-readable summary of attempts, failures, and focus areas for next agent.

---

## **4. Operational Workflows**

### **4.3.1 The Harness Execution Loop Protocol**

**Step 1: Session Initialization (The "Context Load")**
- Hook: SessionStart
- Injections: Persona, Constitution, State, Target task, Environment

**Step 2: The "Get Bearings" Ritual**
1. pwd (Verify location)
2. cat feature_list.json (Read backlog)
3. ./init.sh (Verify environment)
4. npm test (Verify baseline is Green)

**Step 3: TDD Cycle**
1. Isolation (git worktree)
2. Red (failing test)
3. Green (minimal code)
4. Refactor
5. Verify
6. Commit

**Step 4: Handoff & Compaction**
- Hook: PreCompact
- Update feature_list.json
- Write diary to claude-progress.txt
- Exit

---

## **5. Scale-Adaptive Intelligence**

| Track | Harness Behavior | Requirements |
|-------|------------------|--------------|
| **Quick Flow** | Relaxed. TDD encouraged not forced. | /tech-spec only |
| **BMad Method** | Standard. init.sh mandatory. TDD mandatory. | /prd + /architecture |
| **Enterprise** | Strict. Security scans. Code review required. | Full Constitution |

---

## **6. Deep Insights**

### **6.1 Decoupling "Planning" and "Doing"**

Phase 2 produces compressed artifacts (feature_list.json) that allow Coding Agent to run with "light" context.

### **6.2 Self-Healing via "Red" States**

TDD creates a ratchet - once green, system cannot slide back without detection.

### **6.3 Constitution as "Anti-Drift" Anchor**

Injected fresh every session - agent never "drifts" because every session is "Day 1" for enthusiasm but "Day 100" for context.

---

## **7. Future Directions: Knowledge Graph Extension**

Replace claude-progress.txt with Graph Database for semantic queries:
- "Where is the authentication logic defined?"
- Returns direct pointer to src/middleware/auth.ts

---

## Sources

1. BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD
2. Anthropic Harness: https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
3. Spec Kit: https://github.com/github/spec-kit
4. claude-code-bmad-skills: https://github.com/aj-geddes/claude-code-bmad-skills
5. Superpowers: https://github.com/obra/superpowers

---
