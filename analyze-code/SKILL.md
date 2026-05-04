---
name: analyze-code
description: Use when auditing an existing codebase, module, or directory for health — legacy code assessments, pre-release gates, inherited-code reviews, or when you need a multi-lens view across quality, security, performance, and architecture concerns on code you didn't just write
---

# Analyze Code

Multi-lens code audit. Applies four specialist perspectives to existing code and produces a structured report with prioritized findings and a verdict.

## When to Use

**Use for:** auditing a module, codebase health check, pre-release gate, evaluating inherited or legacy code, assessing technical debt before a large change.

**When NOT to use:**
- Writing new code → use `using-software-specialists`
- Diagnosing a specific bug → use `using-software-specialists` with the `troubleshooter` specialist

**MCP enhancements (optional):**
- `sequential-thinking` — for cross-lens synthesis to avoid single-lens tunnel vision. Fall back to step-by-step inline reasoning if unavailable.
- `serena` — for code navigation across all four lenses. Prefer `get_symbols_overview` / `find_symbol` over full-file `Read`, and `find_referencing_symbols` over repo-wide `Grep`. Load symbol bodies only when a finding needs the detail.

## The Four Lenses

Each lens asks a different question. Apply **all four** — single-lens analysis misses cross-cutting issues.

| Lens | Reference | Question it asks |
|------|-----------|------------------|
| **Architecture** | `system-architect` (via `using-software-specialists`) | Where are coupling hotspots, and what breaks when each component fails? |
| **Quality** | `refactoring-expert` (via `using-software-specialists`) | What's hard to change, untested, or overly complex? |
| **Performance** | `performance-engineer` (via `using-software-specialists`) | Where is time actually spent, and what fails under realistic load? |
| **Security** | `security-engineer` (via `using-software-specialists`) | What inputs are trusted, what auth is assumed, where's the insecure default? |

Run them in this order: architecture frames the context, quality and performance surface implementation debt, security is the final gate. Invoking `using-software-specialists` for each lens is optional — adopting the lens question directly produces equivalent output.

## Severity Scale

| Severity | Definition | Examples |
|----------|-----------|----------|
| **Critical** | Data loss, security breach, or production-outage risk | SQL injection, hardcoded secret, auth bypass, race condition in state writes |
| **High** | Significant bug or smell with downstream blast radius | N+1 in hot path, missing input validation, god class, inverted test pyramid |
| **Medium** | Maintainability debt or code smell | High cyclomatic complexity, missing edge-case tests, obvious anti-patterns |
| **Low** | Style, naming, or non-blocking suggestion | Magic numbers, commented-out code, inconsistent naming |

**Rule:** Don't inflate severity. Low is low. Style nits stay Low.

## Verdict

After collecting findings across all four lenses, issue one verdict:

| Verdict | When |
|---------|------|
| **APPROVE** | No Critical findings, ≤2 High findings |
| **NEEDS-WORK** | 1 Critical, **or** 3+ High findings |
| **BLOCK** | 2+ Critical findings, **or** systemic architectural/security issues requiring redesign |

## Workflow

1. **Frame the target** — what are you analyzing, and why now? (pre-release, inheritance, regression, tech-debt assessment)
2. **Architecture lens** — map components and coupling; flag failure-mode and boundary smells
3. **Quality lens** — assess test coverage, complexity, duplication
4. **Performance lens** — identify hot paths, obvious algorithmic/DB issues; note profiling gaps (call them out as "unknown" rather than guessing)
5. **Security lens** — apply `security-best-practices` for the language/framework; check auth, input trust, secrets handling
6. **Synthesize** — group related findings, dedupe, rank by severity, set verdict
7. **Deliver report** — use the template below; lead with verdict and top 3 priorities

## Report Template

```markdown
# Analysis: <target>

**Verdict:** APPROVE | NEEDS-WORK | BLOCK
**Summary:** <1-2 sentences — the headline finding>

## Priority Actions
1. [Critical|High] <action> — <file:line>
2. ...

## Findings by Lens

### Architecture
- [Severity] <Finding> — <file:line> — <impact> — <recommended action>

### Quality
- [Severity] ...

### Performance
- [Severity] ...

### Security
- [Severity] ...

## Out of Scope
- <what was intentionally not covered and why (e.g., "runtime profiling not run — no production access")>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Applying one lens only | All four lenses — single-lens analysis misses cross-cutting issues |
| Dumping raw findings without synthesis | Group by severity, dedupe, rank — top priorities must read first |
| Skipping architecture because "the code looks fine" | Architecture issues hide in the gap between what you see and how components interact |
| Inflating severity to seem thorough | Low stays Low. Reserve Critical for real blast-radius issues |
| Treating "no findings" as complete | State explicitly what you checked and what's out of scope |
| Guessing at performance without evidence | If you can't profile, say "profiling gap" — don't invent numbers |
