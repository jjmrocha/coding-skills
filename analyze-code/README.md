# analyze-code

A Claude Code skill for multi-lens code audits. Applies five specialist perspectives — architecture, quality, performance, security, and coding style — to existing code and produces a deep review of what was found, not a gate decision.

## When to Use

- Auditing a module or codebase for health before a large change
- Personal quality gate before opening a PR
- Evaluating inherited or legacy code
- Assessing technical debt level

**When NOT to use:**
- Writing new code → use `/using-software-specialists`
- Diagnosing a specific bug → use `/using-software-specialists` with the `troubleshooter` specialist

## How It Works

The skill runs five lenses in sequence, then synthesizes findings into a single ranked report:

| Lens | Question it asks |
|------|-----------------|
| **Architecture** | Where are coupling hotspots, and what breaks when each component fails? |
| **Quality** | What's hard to change, untested, or overly complex? |
| **Performance** | Where is time actually spent, and what fails under realistic load? |
| **Security** | What inputs are trusted, what auth is assumed, where's the insecure default? |
| **Coding Style** | Does the code follow the language's style guide for formatting and naming? (delegates to the `/style-checker` skill) |

The final report leads with a summary and top priority actions, with findings in a single severity-ordered list (not grouped by lens).

## Usage

```
/analyze-code
/analyze-code review the auth module
/analyze-code src/payments/ before the Q3 release
```

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — lenses, severity scale, workflow, report template |
