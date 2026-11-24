# analyze-code

A Claude Code skill for reviewing existing code. It looks at the code through
five specialist lenses (architecture, quality, performance, security and
style) and writes a ranked report of what it found. The report is a deep
review and gives no pass or fail verdict.

## When to use

- Auditing a module or codebase for health before a large change.
- Checking your own work before you open a pull request.
- Evaluating inherited or legacy code.
- Assessing the level of technical debt.

## When not to use

- Writing new code. Use `/using-software-specialists`.
- Diagnosing a specific bug. Use `/using-software-specialists` with the
  troubleshooter specialist.

## How it works

The review runs in this order:

1. It fixes the scope of the review and the files to skip.
2. It checks the change against its spec or plan, looks for breaking changes,
   and looks for code that drifts from the project's conventions or
   duplicates something the project already has.
3. It applies the five lenses.
4. It runs the linters, scanners and test suites that the project has
   configured.
5. A separate verifier, which has not seen the reasoning behind each candidate
   finding, confirms or rejects it.
6. The findings that survive go into a report ranked by severity, with one
   section for system-level findings and one for code-level findings.

Each finding has a severity, the verifier's verdict (Confirmed or Plausible),
its scope, the file and line, an evidence snippet, the impact, the action to
take, and the specialist who should fix it.

The skill reports only and never applies fixes. Use `/addressing-findings` to
work through the report. [SKILL.md](SKILL.md) has the full workflow.

## Usage

```
/analyze-code
/analyze-code review the auth module
/analyze-code src/payments/ before the Q3 release
```
