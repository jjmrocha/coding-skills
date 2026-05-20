---
name: using-software-specialists
description: Use when starting any software task — feature, bug fix, refactor, deployment, performance work, troubleshooting, debugging, investigating an issue, or planning implementation — before writing code, diagnosing a problem, or proposing a fix
---

# Using Software Specialists

**Core principle:** Every software task touches multiple domains. A single generalist perspective misses vulnerabilities, accessibility gaps, and quality failures that specialist thinking catches. Each specialist asks a question the others don't — skipping one means that question never gets asked.

## When to Use

**Use for:** new features, bug fixes, refactors, deployments, security reviews, requirements gathering, research, documentation, LLM/prompt work, performance tuning, troubleshooting, and planning execution of an approved design.

**Skip when:** trivial one-line fix with no cross-domain impact, or you already applied the relevant specialist this session.

## How Specialists Work Together

Specialists apply in **phases**, not all at once. Each phase has a different goal:

```
REQUIREMENTS → DESIGN → PLAN → IMPLEMENTATION → TESTING → VALIDATION → DOCUMENTATION
     ↑           ↑       ↑           ↑              ↑           ↑              ↑
   what?    what shape?  order?     how?       does it work?  is it safe?  who maintains?
```

**Note:** Backend and Frontend implementation can run in parallel against an agreed API contract — the contract is the seam.

**Transition signals** — move to the next phase only when the current one's output is complete:

| Phase | Done when... |
|------|--------------|
| Requirements | Acceptance criteria are testable, scope exclusions are explicit, NFRs are listed |
| Design | Component boundaries defined, data model serves all access patterns, API contracts written |
| Plan | Tasks decomposed, dependencies explicit, riskiest work first, verification check per step |
| Implementation | Feature works end-to-end (not just compiles), error/loading/empty states handled, contracts honored — **load `test-driven-development` and `coding-discipline` before writing code** |
| Testing | Edge cases enumerated and covered, no flaky tests, tests pass in CI not just locally |
| Validation | Security review passed, QE strategy confirmed, "Validate Before Done" checklist answered |
| Documentation | Public APIs/READMEs/runbooks updated, owner assigned, outdated docs deleted |

## Task Routing

Forward lookup by task domain. "Start with" = the lead mindset. "Then add" = complementary perspectives during/after implementation. "Before done" = validation gate, never skip.

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
| Prompt optimization, few-shot design, LLM eval | Prompt Engineer | — | — |

**Minimum rule:** Security Engineer + Quality Engineer must appear in "Before done" for any task that touches APIs, user data, or production code.

## The Question Each Specialist Asks

Use this to disambiguate when two specialists could both fire. Each one asks a question no one else does — that's their unique value. For *when to load*, use Task Routing or the Symptom table; for *what they look at*, scan their reference file (link below).

| Specialist | The question only they ask |
|-----------|--------------------------|
| [Requirements Analyst](references/requirements-analyst.md) | "What are we assuming, and what are we explicitly NOT building?" |
| [Project Planner](references/project-planner.md) | "What's the minimal decomposition where each step is independently verifiable, and is the riskiest work scheduled first?" |
| [Deep Research Agent](references/deep-research-agent.md) | "Is this source reliable, and do we have enough evidence to act?" |
| [System Architect](references/system-architect.md) | "What is the simplest architecture that works, and what fails when each component goes down?" |
| [Backend Engineer](references/backend-engineer.md) | "What if this request is duplicated? What fails when retried?" |
| [Database Designer](references/database-designer.md) | "What queries will this serve, and what happens at 100M rows?" |
| [Frontend Engineer](references/frontend-engineer.md) | "What does the user see when this fails? Where does this state live?" |
| [Tester](references/tester.md) | "What are all the edge cases, and does each test name explain the bug if it fails?" |
| [Quality Engineer](references/quality-engineer.md) | "Are we testing at the right level? Is this design even testable?" |
| [DevOps Engineer](references/devops-engineer.md) | "What's the blast radius if this deploy fails, and how fast can we roll back?" |
| [Security Engineer](references/security-engineer.md) | "What's the insecure default here, and how do we make the safe path the easy path?" |
| [Refactoring Expert](references/refactoring-expert.md) | "Do we have tests first, and when do we stop?" |
| [Troubleshooter](references/troubleshooter.md) | "What changed between when it worked and when it broke?" |
| [Performance Engineer](references/performance-engineer.md) | "Where is time actually spent, and what does the production workload actually look like?" |
| [Technical Writer](references/technical-writer.md) | "Who will maintain this, and what should we delete first?" |
| [Prompt Engineer](references/prompt-engineer.md) | "Do we have an eval set, and does this prompt work across models?" |

## Symptom → Specialist (Reverse Lookup)

When you don't know which domain you're in but you can describe what you're *seeing*, scan this first.

| If you're seeing / hearing... | Start here |
|------------------------------|-----------|
| "It worked yesterday", regression, sudden break, mystery error | Troubleshooter |
| Slow, latency spike, p99 climbing, OOM, CPU pegged, missed SLO | Performance Engineer |
| Slow page load, bad LCP/CLS/INP, large bundle, jank | Frontend Engineer + Performance Engineer |
| Slow query, lock contention, table scan, N+1 | Database Designer + Performance Engineer |
| Flaky test, test passes locally fails in CI, intermittent | Quality Engineer |
| "Add a test for this function" | Tester |
| Untestable design, can't isolate, too many mocks needed | Quality Engineer (push back on design) |

| Auth, login, token, session, cookie, CORS, CSRF, OAuth, JWT | Security Engineer |
| PII, GDPR, SOC2, encryption-at-rest/in-transit, audit log | Security Engineer |
| "Can someone retry this safely?", duplicate request, webhook idempotency | Backend Engineer |
| Schema change, migration, ALTER TABLE, index, foreign key | Database Designer |
| CI failing, slow build, deploy stuck, rollback needed | DevOps Engineer (or Troubleshooter if "what changed?") |
| Pipeline secrets, supply chain, signed artifacts, SBOM | DevOps Engineer + Security Engineer |
| "Component boundaries", "monolith vs services", failure modes | System Architect |
| Prompt injection, jailbreak, LLM output rendered as code or used in downstream decisions | Security Engineer + Prompt Engineer |
| Big-bang rewrite tempting, legacy code needs replacing without downtime | Refactoring Expert (strangler-fig) |
| a11y, keyboard navigation, screen reader, WCAG | Frontend Engineer |

If two rows fire, load both — they ask different questions.

### Tester vs Quality Engineer

These two are complementary, not interchangeable:

- **Tester** = the craftsperson. Writes individual tests well. Thinks about edge cases for *this* function, mock boundaries for *this* module, assertion clarity for *this* test.
- **Quality Engineer** = the strategist. Thinks about whether you're testing at the right level, whether the design is testable at all, whether the test pyramid is inverted, whether flaky tests are eroding trust.

**Rule of thumb:** Load the Tester during implementation to write good tests. Load the Quality Engineer before done to check the testing strategy is sound.

**The "systematic coverage" trap:** Edge case enumeration for a specific function — null inputs, boundary values, invalid types, overflow — IS Tester work, even when it feels systematic. QE handles whether you're testing at the right *level* (pyramid shape, design testability), not whether you've covered all cases for *this function*. "Write tests for `calculateDiscount()`" → Tester leads.

## Validate Before Done

Before marking any task complete, answer each item that applies. Security and QA are universal; the rest trigger when their conditions apply.

- **Security** *(always)*: What inputs are trusted? What can be abused? Is auth enforced?
- **QA** *(always)*: What edge cases haven't been tested? What fails under bad input or load?
- **Troubleshoot** *(if you debugged anything)*: Is the root cause confirmed, or just the symptom patched?
- **Refactor** *(if you changed existing code)*: Is all existing behavior preserved? Are tests still passing?
- **Docs** *(if anything user- or operator-facing changed)*: Are public APIs / READMEs / runbooks updated? Who owns the doc going forward?

## Anti-Patterns

If you catch yourself thinking any of these, stop and reload the right specialist.

| If you think... | Reality |
|---|---|
| "Load all specialists up front" | Load per phase — design → implement → test → validate → document |
| "I'll load the specialist after writing the code" | Retrofitting is harder; load before the first line |
| "I don't need `coding-discipline`, I know what I'm doing" | Silent assumptions, scope creep, and hallucination happen even on familiar code — load it before composing any diff |
| "The 'Start with' specialist is enough" | "Then add" and "Before done" columns are not optional |
| "The validate step is optional" | It is the gate; non-negotiable |
| "Tester and Quality Engineer are the same" | Tester writes good tests; QE validates the testing *strategy* |
| "I'll add validation later" | Security belongs in design, not after |
| "It's internal, no security concerns" | Internal APIs still have auth gaps, injection, and trust-boundary risks |
| "I'm already handling the basic security things (prepared statements, validation)" | Basic hygiene ≠ Security Engineer gate. Authz ownership checks, auth enforcement, rate limiting, and data exposure require systematic Security Engineer review — not a mental note. |
| "Tests can be written after" | Load Tester during implementation; tests-after answer the wrong question |
| "I know the fix, I'll just apply it" | Load Troubleshooter — diagnose root cause before patching symptoms |
| "Too small to need architecture review" | Small tasks that ignore boundaries create coupling debt |
| "I'll deploy manually this once" | One-offs become the process; load DevOps |
| "Happy path tests are enough" | Load Tester — edge case enumeration is the whole point |

**Cross-specialist handoff:** When a specialist spots an issue outside their domain, flag it explicitly for the relevant specialist (e.g., a backend engineer who spots suspicious auth patterns flags it for the security engineer). Don't silently ignore cross-domain concerns.
