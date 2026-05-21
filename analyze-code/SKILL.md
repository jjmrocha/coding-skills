---
name: analyze-code
description: Use when auditing existing code — legacy or inherited code reviews, pre-PR self-review of changed modules, module health checks, or tech-debt assessment before a large change
---

# Analyze Code

Multi-lens audit of existing code. Applies five specialist perspectives and produces a prioritized findings report — a deep review, not a gate decision.

## When NOT to Use

- Writing new code → `using-software-specialists`
- Diagnosing a specific bug → `using-software-specialists` with `troubleshooter`

## The Five Lenses

| Lens | Question it asks | Reference |
|------|------------------|-----------|
| **Architecture** | Where are coupling hotspots? What breaks when each component fails? | `system-architect` |
| **Quality** | What's hard to change, untested, overly complex, or reinvents an existing helper/pattern? | `refactoring-expert` |
| **Performance** | Where is time spent? What fails under realistic load? | `performance-engineer` |
| **Security** | What inputs are trusted? What auth is assumed? Where's the insecure default? | `security-engineer` |
| **Style** | Does the code follow the language's style guide? | `style-checker` skill |

Apply **all five** — single-lens audits miss cross-cutting issues. Order: architecture frames context → quality/performance surface debt → security gates → style closes. Adopting each lens's question directly is equivalent to invoking `using-software-specialists`; don't reflexively invoke it five times. Delegate the style lens to the `style-checker` skill rather than re-deriving rules.

## Severity Scale

| Severity | Definition |
|----------|-----------|
| **Critical** | Data loss, security breach, or outage risk (SQLi, hardcoded secret, auth bypass, race in state writes) |
| **High** | Significant bug or smell with downstream blast radius (N+1 in hot path, missing input validation, god class) |
| **Medium** | Maintainability debt or anti-pattern (high complexity, missing edge-case tests) |
| **Low** | Style, naming, magic numbers — non-blocking |

Don't inflate severity. Low stays Low.

## Workflow

1. **Frame** — what's the target, and why now (inheritance, regression, pre-change debt)?
2. **Breaking-change scan** (audits of modified code only) — for each changed signature, return type, raised error, side effect, or invariant on an existing symbol, list every caller via `find_referencing_symbols` or `grep`, verify the new contract holds at each call site, and report any caller that breaks (compile error, wrong behavior under the new contract, or assumption violated) as a finding. Public-API breaks are Critical/High; a single internal caller is Medium. Skip on greenfield.
3. **Convention & duplication scan** (audits of new or modified code only) — verify changes follow existing codebase patterns: same helper utilities, same error-handling style, same module layout, same naming conventions. For each new helper, type, or pattern introduced, search the codebase with `find_symbol`/`grep` for an existing equivalent before accepting it. Flag duplicated helpers, re-implemented utilities, or one-off solutions that diverge from established patterns. Severity: parallel implementation of an existing utility is **High**; convention drift (naming, error style) is usually **Medium**; minor inconsistency is **Low**. Skip on greenfield.
4. **Architecture lens** — map components and coupling; flag failure-mode and boundary smells.
5. **Quality lens** — assess complexity, duplication, test coverage.
6. **Performance lens** — hot paths, algorithmic complexity, N+1, unnecessary allocations. Report what the code reveals; don't flag missing profiling as a defect.
7. **Security lens** — apply `security-best-practices` for the language/framework; check auth, input trust, secrets.
8. **Style lens** — **if the project has a linter/formatter configured (eslint, ruff, golangci-lint, rubocop, etc.), run it — it is authoritative over generic style rules.** Only fall back to the `style-checker` skill when no linter is configured. Map severities (most → Low, systemic breakage → Medium).
9. **Run configured tooling** — for every linter, formatter, or test suite the project ships (eslint, ruff, go vet, pytest, go test, mypy, tsc), **you must run it — "looked at the code" is not a substitute**. Fold failures into findings at their natural severity (failing security test → Critical; lint nit → Low). Tooling configured but currently red is itself a finding. No tooling configured at all is a Medium "CI hygiene" finding — don't silently skip.
10. **Synthesize & deliver** — group, dedupe, rank by severity. Output one prioritized list, not lens-grouped.

## MCP Enhancements (optional)

- `sequential-thinking` — for cross-lens synthesis; fall back to inline reasoning if unavailable.
- `serena` — prefer `get_symbols_overview`/`find_symbol` over full-file `Read`, and `find_referencing_symbols` over repo-wide `Grep`. Load symbol bodies only when a finding needs the detail.

## Report Template

```markdown
# Analysis: <target>

**Summary:** <1-2 sentences — headline findings>

## Priority Actions
1. [Critical|High] <action> — <file:line>

## Findings
- [Severity] <Finding> — <file:line> — <impact> — <recommended action>

## Coding Style
<Summary of style findings; reference the style-checker report for full detail.>
```

Findings are severity-ordered, not lens-grouped. The lenses are the internal analysis framework; the user reads one list.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Applying one lens only | All five — cross-cutting issues hide between lenses |
| Lens-grouped output | Output one severity-ordered list; lenses are internal scaffolding |
| Inflating severity | Low stays Low; reserve Critical for real blast radius |
| Reporting non-findings | Skip "profiling wasn't done" or "tests not run" — focus on what the code reveals |
| Skipping the linter/test suite when configured | If a linter exists, you must run it — its output is authoritative over generic style rules and "looked at the code" |
| Using generic style rules when the project has its own linter | Defer to the configured linter (eslint/ruff/golangci-lint/etc.); the `style-checker` skill is the fallback, not the default |
| Changing a signature/contract without checking for breaking changes | Step 2 is mandatory for every modified existing symbol — sweep every caller against the new contract |
| Accepting a new helper without checking for existing equivalents | Step 3 — `find_symbol`/`grep` for similar utilities before treating a new helper as additive |
| Treating convention drift as a style nit | Diverging from established codebase patterns (naming, error handling, module layout) is Medium, not Low |
| Re-deriving style rules inline | Delegate to `style-checker` — it already encodes the language references |
