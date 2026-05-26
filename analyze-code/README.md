# analyze-code

A Claude Code skill for multi-lens code audits. Applies five specialist
perspectives — architecture, quality, performance, security, and coding
style — to existing code and produces a deep review of what was found, not a
gate decision.

## When to Use

* Auditing a module or codebase for health before a large change
* Personal quality gate before opening a PR
* Evaluating inherited or legacy code
* Assessing technical debt level

**When NOT to use:**

* Writing new code → use `/using-software-specialists`
* Diagnosing a specific bug → use `/using-software-specialists` with the
  `troubleshooter` specialist

## How It Works

The skill runs a scope-and-boundary frame, five lenses (Architecture, Quality, Performance, Security, Style) and the project's configured tooling, then synthesizes findings into a ranked report split into **System-level** and **Code-level** sections. See [SKILL.md](SKILL.md) for the full workflow and [references.md](references.md) for heavy reference (scanner-per-file-type matrix, tooling discovery paths, skip-path patterns, specialist routing).

Each finding carries severity, confidence (Suspected/Confirmed), scope tag (system/code), file:line, evidence snippet, impact, action, and a routing specialist for the audit → fix loop.

## Usage

```
/analyze-code
/analyze-code review the auth module
/analyze-code src/payments/ before the Q3 release
```

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — lenses, severity scale, workflow, report template, false-positive markers, findings cap, good-vs-bad example |
| [references.md](references.md) | Tooling discovery paths, per file-type scanner matrix, skip-path patterns, specialist routing |
