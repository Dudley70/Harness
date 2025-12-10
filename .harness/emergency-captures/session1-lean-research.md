# Emergency Capture: Lean Research Data

> **WARNING:** This data was almost lost. Captured reactively at 83%+ context.
> See `.harness/lessons-learned.md` for the meta-lesson.

---

## Lean Software Development - Pattern Extraction

### Summary
- Lean Software Development, formalized by Mary and Tom Poppendieck (2003), adapts Toyota Production System principles to software through 7 core principles and 22 thinking tools
- Core focus on eliminating seven types of waste (partially done work, extra features, context switching, waiting, relearning, handoffs, defects)
- Emphasizes flow optimization through pull systems, WIP limits, and queuing theory
- Balances speed with quality through TDD, continuous integration, pair programming
- Challenges traditional project management by deferring decisions, empowering teams, optimizing whole value streams

### Extracted Patterns

| # | Pattern Name | Original Purpose | AI-Age Relevance | Transfers/Obsolete | Notes |
|---|--------------|------------------|------------------|-------------------|-------|
| 1 | Value Stream Mapping | Visualize entire development process to identify bottlenecks | Highly relevant - AI creates new waste types (prompt iteration, output validation, hallucination debugging) | Transfer | Need new VSM categories for AI-specific activities |
| 2 | Eliminate Partially Done Work | Prevent WIP accumulation that never reaches production | Critical - AI can generate massive partially-done code that's never integrated | Transfer | AI amplifies risk: easy to generate, hard to integrate |
| 3 | Eliminate Extra Features | Avoid building features customers don't need/use | Transforms - AI makes feature creation nearly free, but complexity/maintenance costs remain | Transform | Economics shift: creation cost→0, but lifecycle cost remains |
| 4 | Minimize Context Switching | Reduce task-switching waste; flow state takes 15min to achieve | Transforms - AI handles context differently; human switches between AI oversight vs direct coding | Transform | Human role shifts to orchestration across AI-generated outputs |
| 5 | Eliminate Waiting/Delays | Remove idle time waiting for approvals, dependencies, or handoffs | Transforms - AI reduces some waits (code generation) but creates new ones (validation, testing) | Transform | Bottleneck shifts from creation to verification |
| 6 | Prevent Relearning | Avoid repeated learning through documentation, knowledge sharing | Critical - AI lacks memory across sessions; humans must re-explain context repeatedly | Transfer | Knowledge management becomes more critical, not less |
| 7 | Minimize Handoffs | Reduce knowledge transfer waste between teams/individuals | Transforms - Human-to-AI handoffs create new translation layer (requirements→prompts) | Transform | New handoff type: natural language→executable code |
| 8 | Prevent Defects Early | Build quality in through TDD, continuous integration, automated testing | Critical - AI generates plausible-but-wrong code; testing becomes verification bottleneck | Transfer | Quality gates shift earlier (prompt validation) and later (output verification) |
| 9 | Set-Based Concurrent Engineering | Explore multiple design solutions in parallel, eliminate poor options progressively | Amplified - AI enables cheap parallel exploration of design alternatives | Transfer | AI makes SBCE economically viable for smaller decisions |
| 10 | Decide at Last Responsible Moment | Defer decisions until maximum information available | Transforms - AI enables cheaper experimentation, pushing "last responsible moment" later | Transform | Lower cost of change extends decision horizon |
| 11 | Pull Systems | Work flows based on downstream demand, not upstream push | Partially obsolete - When code generation is instant, pull signals lose timing value | Transform | Pull applies to requirements/validation, not code generation |
| 12 | Work-In-Progress (WIP) Limits | Limit concurrent tasks to prevent overload, make bottlenecks visible | Transforms - Limits apply to validation capacity, not generation capacity | Transform | WIP limits shift to human verification, not code creation |
| 13 | Amplify Learning via Pair Programming | Two developers collaborate real-time to catch errors, share knowledge | Transforms - Pairing becomes human+AI; knowledge sharing patterns change | Transform | Pair = human+AI, not human+human; different knowledge dynamics |
| 14 | Amplify Learning via Code Reviews | Peer review distributes knowledge, catches defects before production | Critical - Reviews must validate AI-generated code understanding, not just correctness | Transfer | Review scope expands: correctness + maintainability + comprehension |
| 15 | Continuous Integration | Integrate and test code frequently to catch integration issues early | Critical - AI-generated code must integrate with existing systems; more frequent need | Transfer | CI becomes validation bottleneck as generation speed increases |
| 16 | Test-Driven Development (TDD) | Write tests before code to clarify requirements and ensure quality | Transforms - Tests-first gives AI clear specification; TDD becomes prompt-engineering tool | Transform | TDD shifts from discipline to AI instruction mechanism |
| 17 | Refactoring | Improve internal code structure while preserving external behavior | Critical - AI generates working-but-messy code; refactoring debt accumulates faster | Transfer | Refactoring burden increases as AI optimizes for "works now" not "maintainable" |
| 18 | MVP (Minimum Viable Product) | Release minimal feature set to validate learning with least effort | Amplified - AI accelerates MVP creation, enabling faster hypothesis testing | Transfer | MVP cycle time compresses; learning velocity increases |
| 19 | Empower the Team | Give autonomy to people closest to work; they understand it best | Critical - Human judgment for architecture, tradeoffs, and context remains essential | Transfer | Empowerment includes choosing when/how to use AI tools |
| 20 | Optimize the Whole Value Stream | Improve end-to-end flow, not local efficiencies; avoid sub-optimization | Critical - Optimizing code generation alone creates verification bottleneck | Transfer | System optimization must include human+AI workflow |
| 21 | Build Conceptual Integrity | Maintain consistent architecture and design philosophy across system | Critical - AI lacks cross-component architectural vision; human role essential | Transfer | Architectural coherence requires human oversight |
| 22 | Queuing Theory Application | Use Little's Law (WIP = Throughput × Lead Time) to identify bottlenecks | Transforms - Bottlenecks shift from code creation to validation/review/integration | Transform | Queue math still applies but to different process stages |
| 23 | Cost of Delay Calculation | Quantify financial impact of delays to prioritize bottleneck removal | Transforms - Delay costs shift from "waiting for code" to "waiting for validation" | Transform | ROI calculations must account for near-zero generation cost |

### Source References
- Leany Labs - 7 Principles of Lean Software Development
- Wikipedia - Lean software development
- Businessmap - Lean Software Development Principles
- Built In - 7 Principles of Lean Software Development
- O'Reilly - Lean Software Development: An Agile Toolkit
- Mark Barber, Medium - 7 Wastes of Lean
- ActiveCollab - 7 Wastes of Lean in Software Development
- Kanban Tool - Queuing Theory & Kanban
- LeSS - Queueing Theory
- GeeksforGeeks - Lean Software Development
- TechTarget - What is Lean Software Development?
- Ardalis Blog - Principles of Lean Software Development
