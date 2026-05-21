---
name: analyze-code
description: Use when auditing an existing codebase, module, or directory for health — legacy code assessments, inherited-code reviews, or when you need a multi-lens view across quality, security, performance, and architecture concerns on code you didn't just write
---

# Analyze Code

Multi-lens code audit. Applies five specialist perspectives to existing code and produces a prioritized findings report — a deep review of what was found, not a gate decision.

## When to Use

**Use for:** personal quality gate before opening a PR, auditing a module, codebase health check, evaluating inherited or legacy code, assessing technical debt before a large change.

**When NOT to use:**
- Writing new code → use `using-software-specialists`
- Diagnosing a specific bug → use `using-software-specialists` with the `troubleshooter` specialist

**MCP enhancements (optional):**
- `sequential-thinking` — for cross-lens synthesis to avoid single-lens tunnel vision. Fall back to step-by-step inline reasoning if unavailable.
- `serena` — for code navigation across all four lenses. Prefer `get_symbols_overview` / `find_symbol` over full-file `Read`, and `find_referencing_symbols` over repo-wide `Grep`. Load symbol bodies only when a finding needs the detail.

## The Five Lenses

Each lens asks a different question. Apply **all five** — single-lens analysis misses cross-cutting issues.

| Lens | Reference | Question it asks |
|------|-----------|------------------|
| **Architecture** | `system-architect` (via `using-software-specialists`) | Where are coupling hotspots, and what breaks when each component fails? |
| **Quality** | `refactoring-expert` (via `using-software-specialists`) | What's hard to change, untested, or overly complex? |
| **Performance** | `performance-engineer` (via `using-software-specialists`) | Where is time actually spent, and what fails under realistic load? |
| **Security** | `security-engineer` (via `using-software-specialists`) | What inputs are trusted, what auth is assumed, where's the insecure default? |
| **Coding Style** | `style-checker` skill | Does the code follow the language's style guide for formatting and naming? |

Run them in this order: architecture frames the context, quality and performance surface implementation debt, security is the final gate, and coding style closes the audit with formatting/naming conformance. Invoking `using-software-specialists` for each lens is optional — adopting the lens question directly produces equivalent output. For the **Coding Style** lens, delegate to the `style-checker` skill rather than re-deriving rules inline; it already loads the right language reference (Go, Java, Python, JavaScript, TypeScript, Shell, Markdown) and produces a structured violation list you can fold into the report.

## Severity Scale

| Severity | Definition | Examples |
|----------|-----------|----------|
| **Critical** | Data loss, security breach, or production-outage risk | SQL injection, hardcoded secret, auth bypass, race condition in state writes |
| **High** | Significant bug or smell with downstream blast radius | N+1 in hot path, missing input validation, god class, inverted test pyramid |
| **Medium** | Maintainability debt or code smell | High cyclomatic complexity, missing edge-case tests, obvious anti-patterns |
| **Low** | Style, naming, or non-blocking suggestion | Magic numbers, commented-out code, inconsistent naming |

**Rule:** Don't inflate severity. Low is low. Style nits stay Low.

## Workflow

1. **Frame the target** — what are you analyzing, and why now? (inheritance, regression, tech-debt assessment)
2. **Breaking-change scan (when auditing modified code)** — for every existing function, method, or public symbol whose signature, return type, raised errors, side effects, or invariants changed: enumerate every caller in the codebase using `find_referencing_symbols` (serena) or `grep`, and verify each call site still compiles and still gets correct behavior under the new contract. List affected callers as findings; severity tracks blast radius — public-API breaks are Critical/High, single internal caller is Medium. Skip this step on greenfield audits.
3. **Architecture lens** — map components and coupling; flag failure-mode and boundary smells
4. **Quality lens** — assess test coverage, complexity, duplication
5. **Performance lens** — identify hot paths, algorithmic complexity issues, N+1 queries, unnecessary allocations. Report what the code reveals — don't note that profiling wasn't done.
6. **Security lens** — apply `security-best-practices` for the language/framework; check auth, input trust, secrets handling
7. **Coding Style lens** — invoke the `style-checker` skill on the target files/directory; map its severities into this skill's scale (most style violations are **Low**, only systemic style breakage rises to **Medium**)
8. **Run available tooling** — if the project has a configured linter, formatter, or test suite, run it (e.g., `eslint`, `ruff`, `go vet`, `pytest`, `go test`). Fold failures into the report at the severity their nature warrants (a failing security test → Critical; a lint nit → Low). If the tooling is configured but currently red, that's a finding in itself. If no tooling is configured, note it as a Medium "CI hygiene" finding — don't silently skip.
9. **Synthesize** — group related findings, dedupe, rank by severity
10. **Deliver report** — use the template below; lead with summary and top priorities

## Report Template

```markdown
# Analysis: <target>

**Summary:** <1-2 sentences — the headline findings>

## Priority Actions
1. [Critical|High] <action> — <file:line>
2. ...

## Findings

- [Severity] <Finding> — <file:line> — <impact> — <recommended action>
- ...

## Coding Style

<Summary of style findings, or inline the most important ones. For full detail,
reference the style-checker report.>
```

Findings are listed in severity order (Critical first), not grouped by lens. The lenses are an internal analysis framework — the user reads a single prioritized list.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Applying one lens only | All five lenses — single-lens analysis misses cross-cutting issues |
| Re-deriving style rules inline | Delegate the Coding Style lens to the `style-checker` skill — it already encodes the language references |
| Letting style nits dominate the report | Most style findings are Low; don't let them push real Critical/High issues out of the top priorities |
| Dumping raw findings without synthesis | Group by severity, dedupe, rank — top priorities must read first |
| Organizing output by lens | The lens-separated report is hard to scan. Output a single prioritized list — severity order, not lens order. |
| Skipping architecture because "the code looks fine" | Architecture issues hide in the gap between what you see and how components interact |
| Inflating severity to seem thorough | Low stays Low. Reserve Critical for real blast-radius issues |
| Reporting what wasn't checked as findings | Focus on what the code reveals. Don't list profiling gaps or tests not run as if they're defects. |
| Reporting style/quality issues without running the linter or tests when they're configured | Run them; "looked at the code" is not a substitute for executing the available tooling |
| Changing a function's signature/contract without sweeping its callers | Every modified existing symbol needs a caller sweep — `find_referencing_symbols` or `grep` — and each call site is checked against the new contract |
