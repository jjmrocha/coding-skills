---
name: analyze-code
description: Use when auditing existing code — legacy or inherited code reviews, pre-PR self-review of changed modules, module health checks, or tech-debt assessment before a large change
---

# Analyze Code

Multi-lens audit of existing code. Applies five specialist perspectives and produces a prioritized findings report — a deep review, not a gate decision.

## What Makes Good Code?

1. Readable and Self-Explanatory
* **Clear Naming:** Variables and functions should use descriptive names (e.g., `customerRecord` instead of `x`).
* **Minimal Comments:** Code should be intuitive enough that it explains what it does on its own. Comments should only be used to explain the *why* behind complex or counter-intuitive logic.
* **No "Clever" Tricks:** Straightforward, simple logic is always better than heavily condensed, unreadable one-liners.

2. Maintainable and Modular
* **Single Responsibility Principle (SRP):** Functions and classes should do one thing, and do it well.
* **DRY (Don't Repeat Yourself):** Avoid duplicating logic so that future updates only require changes in one place.
* **Separation of Concerns:** Keep core business logic separate from input/output operations.

3. Testable and Reliable
* **Automated Testing:** Good code is written in a way that allows automated unit tests to verify that every component functions correctly.
* **Error Handling:** It anticipates edge cases and fails gracefully rather than crashing unexpectedly.

4. Efficient (Within Reason)
* It runs fast enough to deliver a smooth user experience without wasting computing power. However, optimization should never come at the cost of readability unless absolutely necessary.


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

1. **Frame** — what's the target, and why now (inheritance, regression, pre-change debt)? **If `kb_path` is configured in CLAUDE.md, also load `knowledge-base` and read the current repo's `wiki/<repo>/index.md`, plus the matching plan at `<kb_path>/plans/<current-branch>.md` if one exists.** The plan lets the audit compare implementation against intent; the system pages reveal what external surfaces the code touches; the helpers and patterns lists are the canonical answer to *"does this already exist?"* and *"is there a documented way to do this?"*. Drill into specific helper/pattern pages on demand when the code under review suggests overlap. May follow cross-repo `[[wiki-links]]` (e.g., to other repos' consumer pages for events this repo produces) when judged relevant. **Wiki ↔ code disagreements are findings**, not silently ignored — intent-vs-implementation drift is often a bug, surfaced at Medium or higher depending on blast radius. Two specific finding types under this rule: **"reinvents existing helper"** (code introduces a function semantically equivalent to one listed in `helpers/`) and **"violates documented pattern"** (code diverges from a `patterns/<name>.md` page — severity scales with `kind:`, `convention` violations usually Medium, `template` divergence Low, `recipe` step-skipping Medium when it skips a safety step).
2. **Breaking-change scan** (audits of modified code only) — for each changed signature, return type, raised error, side effect, or invariant on an existing symbol, list every caller via `find_referencing_symbols` or `grep`, verify the new contract holds at each call site, and report any caller that breaks (compile error, wrong behavior under the new contract, or assumption violated) as a finding. Public-API breaks are Critical/High; a single internal caller is Medium. Skip on greenfield.
3. **Convention & duplication scan** (audits of new or modified code only) — verify changes follow existing codebase patterns: same helper utilities, same error-handling style, same module layout, same naming conventions. For each new helper, type, or pattern introduced, search the codebase with `find_symbol`/`grep` for an existing equivalent before accepting it. Flag duplicated helpers, re-implemented utilities, or one-off solutions that diverge from established patterns. Severity: parallel implementation of an existing utility is **High**; convention drift (naming, error style) is usually **Medium**; minor inconsistency is **Low**. Skip on greenfield.
4. **Architecture lens** — map components and coupling; flag failure-mode and boundary smells.
5. **Quality lens** — assess complexity, duplication, test coverage.
6. **Performance lens** — hot paths, algorithmic complexity, N+1, unnecessary allocations. Report what the code reveals; don't flag missing profiling as a defect.
7. **Security lens** — apply security best practices for the language/framework; check auth, input trust, secrets.
8. **Style lens** — always run the `style-checker` skill. **If the project also has a linter/formatter configured (eslint, ruff, golangci-lint, rubocop, etc.), run it too — on any conflicting rule, the linter is authoritative.** Map severities (most → Low, systemic breakage → Medium).
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

## Suggested Next Actions
- **Critical / High** → re-enter `using-software-specialists` with the matching specialist (Security Engineer for auth/input/secrets, Backend Engineer for logic/idempotency, Database Designer for schema/query, Performance Engineer for hot-path, Refactoring Expert for structural debt). One fix loop per finding cluster.
- **Medium** → ticket / batch into a planned cleanup, or address now if the cluster is cheap.
- **Low** → optional inline fix, batch with the next touch of the file, or accept.
```

Findings are severity-ordered, not lens-grouped. The lenses are the internal analysis framework; the user reads one list. The "Suggested Next Actions" block exists to close the audit → fix loop: each finding points back at the specialist who should own the remediation, so the user can dispatch targeted fixes through `using-software-specialists` without re-classifying. Do not invent new severities to fill the block — if there are no Critical/High findings, say so.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Applying one lens only | All five — cross-cutting issues hide between lenses |
| Lens-grouped output | Output one severity-ordered list; lenses are internal scaffolding |
| Inflating severity | Low stays Low; reserve Critical for real blast radius |
| Reporting non-findings | Skip "profiling wasn't done" or "tests not run" — focus on what the code reveals |
| Skipping the linter/test suite when configured | If a linter exists, you must run it — its output is authoritative on conflicting rules and "looked at the code" is never a substitute |
| Skipping `style-checker` because a linter is configured | Run both — `style-checker` always runs; linter wins only where rules conflict |
| Changing a signature/contract without checking for breaking changes | Step 2 is mandatory for every modified existing symbol — sweep every caller against the new contract |
| Accepting a new helper without checking for existing equivalents | Step 3 — `find_symbol`/`grep` for similar utilities before treating a new helper as additive |
| Treating convention drift as a style nit | Diverging from established codebase patterns (naming, error handling, module layout) is Medium, not Low |
| Re-deriving style rules inline | Delegate to `style-checker` — it already encodes the language references |
