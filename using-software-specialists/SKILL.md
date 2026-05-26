---
name: using-software-specialists
description: Use when starting any non-trivial software task — feature, bugfix, refactor, migration, security/auth work, performance work, or turning a spec into a plan — before writing code, diagnosing, or proposing a fix.
---

# Using Software Specialists

**Core principle:** Every software task touches multiple domains. Each specialist asks a question the others don't — skipping one means that question never gets asked.

**If the conversation was compacted, re-invoke this skill before continuing.**

## When NOT to Use

| Don't load when... | Instead... |
|---|---|
| Pure copy/paste, rename, typo, comment-only change | Just do it |
| Single-line edit you already verified touches no auth, payment, schema, or public API | Just do it |
| The relevant specialist was already applied this session for the same surface | Reuse the prior framing |

## How Specialists Work Together

Specialists apply in **phases**, not all at once. Each phase has a different goal:

```
REQUIREMENTS → DESIGN → PLAN → IMPLEMENTATION → TESTING → VALIDATION → DOCUMENTATION
     ↑           ↑       ↑           ↑              ↑           ↑              ↑
   what?    what shape?  order?     how?       does it work?  is it safe?  who maintains?
```

Backend and Frontend implementation can run in parallel against an agreed API contract — the contract is the seam.

**If the user provides a plan file** (e.g., *"plan and implement using ~/plans/X.md"*), read it first and validate it against the Plan row's done-criteria below. Stop and surface gaps if **any** of these are missing: testable acceptance criteria, explicit scope exclusions, listed NFRs, decomposed steps with dependencies, riskiest work first, verification per step. Do not start coding against an incomplete plan.

**Implementation:** load `coding-discipline` and `test-driven-development`. If `kb_path` is configured, also load `knowledge-base` first.

Move to the next phase only when the current one's output is complete:

| Phase | Done when... |
|------|--------------|
| Requirements | Acceptance criteria testable, scope exclusions explicit, NFRs listed |
| Design | Component boundaries defined, data model serves all access patterns, API contracts written |
| Plan | Tasks decomposed, dependencies explicit, riskiest work first, verification check per step |
| Implementation | Feature works end-to-end (not just compiles), error/loading/empty states handled, contracts honored |
| Testing | Edge cases enumerated and covered, no flaky tests, tests pass in CI not just locally |
| Validation | Security review passed, QE strategy confirmed, "Validate Before Done" checklist answered |
| Documentation | Public APIs/READMEs/runbooks updated, owner assigned, outdated docs deleted |

## Task Routing

Forward lookup by task domain. "Start with" = lead mindset. "Then add" = complementary perspectives during/after implementation. "Before done" = validation gate, never skip.

| Task | Start with | Then add | Before done |
|------|-----------|----------|-------------|
| Backend development (APIs, server logic, caching) | Backend Engineer | Tester | Security Engineer, Quality Engineer |
| Data modeling, schema design, migrations, indexing | Database Designer | Backend Engineer | Security Engineer, Quality Engineer |
| Frontend development (UI, state, accessibility, performance) | Frontend Engineer | Tester | Security Engineer, Quality Engineer |
| New service or system design | System Architect | Backend Engineer, Database Designer | Security Engineer, Quality Engineer |
| Full-stack feature | System Architect | Backend Engineer, Database Designer, Frontend Engineer, Tester | Security Engineer, Quality Engineer |
| Auth, security, compliance, threat modeling | Security Engineer | Backend Engineer | Quality Engineer |
| Test strategy, quality gates, flaky tests, inverted pyramid | Quality Engineer | Tester | — |
| Writing unit/integration tests for specific code | Tester | — | Quality Engineer |
| CI/CD, deployment, infra, monitoring | DevOps Engineer | — | Security Engineer, Quality Engineer |
| Code quality, refactoring, technical debt | Refactoring Expert | Tester | Quality Engineer |
| Bug, build failure, deploy failure, regression after a change | Troubleshooter | Performance Engineer (if perf-related) | Quality Engineer |
| Performance tuning, profiling, capacity planning, load testing | Performance Engineer | Backend Engineer, Database Designer, Frontend Engineer (if FE/Core Web Vitals) | Quality Engineer |
| New project, requirements, scoping, PRDs | Requirements Analyst | — | — |
| Turning an approved spec into an execution plan | Project Planner | — | — |
| Technical investigation, research, analysis | Deep Research Agent | — | — |
| Documentation, user guides, API references | Technical Writer | — | — |
| Prompt optimization, few-shot design, LLM eval, prompt-cache layout, long-context strategy | Prompt Engineer | — | Security Engineer |
| LLM-powered feature, AI agent, RAG pipeline, AI-assisted action | Prompt Engineer | ML Engineer (if retrieval/embeddings), Backend Engineer | Security Engineer, Quality Engineer |
| ML training, fine-tuning, model evaluation, retrieval/embedding design, fairness/bias audit | ML Engineer | Prompt Engineer (if LLM), Backend Engineer (if pipeline) | Security Engineer, Quality Engineer |

**Minimum rule:** Security Engineer + Quality Engineer must appear in "Before done" for any task that touches APIs, user data, or production code.

## The Question Each Specialist Asks

When two specialists could both fire, each asks a unique disambiguating question — see [references/specialist-questions.md](references/specialist-questions.md). Load it before invoking a specialist whose role you're unsure of.

### Tester vs Quality Engineer

Complementary, not interchangeable:

- **Tester** = craftsperson. Edge cases for *this* function, mock boundaries for *this* module, assertion clarity for *this* test.
- **Quality Engineer** = strategist. Whether you're testing at the right level, whether the design is testable at all, whether the pyramid is inverted, whether flaky tests are eroding trust.

**Rule:** Tester during implementation to write good tests; QE before done to validate the strategy.

**The "systematic coverage" trap:** Edge case enumeration for a specific function — null inputs, boundary values, invalid types, overflow — IS Tester work, even when it feels systematic. QE handles whether you're testing at the right *level*, not whether you've covered all cases for *this function*. "Write tests for `calculateDiscount()`" → Tester leads.

## Validate Before Done

Before marking any task complete, answer each item that applies. Security and QA are universal; the rest trigger when their conditions apply.

- **Security** *(always)*: What inputs are trusted? What can be abused? Is auth enforced?
- **QA** *(always)*: What edge cases haven't been tested? What fails under bad input or load?
- **Troubleshoot** *(if you debugged anything)*: Is the root cause confirmed, or just the symptom patched?
- **Refactor** *(if you changed existing code)*: Is all existing behavior preserved? Are tests still passing?
- **Docs** *(if anything user- or operator-facing changed)*: Are public APIs / READMEs / runbooks updated? Who owns the doc going forward?

## Anti-Patterns

Routing rationalizations only — process discipline lives in `coding-discipline`.

| If you think... | Reality |
|---|---|
| "The 'Start with' specialist is enough" / "The validate step is optional" | "Then add" and "Before done" columns are non-negotiable gates |
| "Tester and Quality Engineer are the same" | Tester writes good tests; QE validates the testing *strategy* |
| "I'll add validation later" / "It's internal, no security concerns" | Security belongs in design. Internal APIs have auth gaps, injection, and trust-boundary risks. |
| "Existing tests still pass after the auth refactor, ship it" | Auth bugs don't fail tests — they create bypass paths your tests weren't written to catch. Auth refactors always require Security Engineer review regardless of test results. |

**Cross-specialist handoff:** When a specialist spots an issue outside their domain, flag it explicitly for the relevant specialist. Don't silently ignore cross-domain concerns.
