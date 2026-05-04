# analyze-code

A Claude Code skill for multi-lens code audits. Applies four specialist perspectives — architecture, quality, performance, and security — to existing code and produces a structured report with prioritized findings and a verdict.

## When to Use

- Auditing a module or codebase for health before a large change
- Pre-release gate review
- Evaluating inherited or legacy code
- Assessing technical debt level

**When NOT to use:**
- Writing new code → use `/using-software-specialists`
- Diagnosing a specific bug → use `/using-software-specialists` with the `troubleshooter` specialist

## How It Works

The skill runs four lenses in sequence, then synthesizes findings into a single ranked report:

| Lens | Question it asks |
|------|-----------------|
| **Architecture** | Where are coupling hotspots, and what breaks when each component fails? |
| **Quality** | What's hard to change, untested, or overly complex? |
| **Performance** | Where is time actually spent, and what fails under realistic load? |
| **Security** | What inputs are trusted, what auth is assumed, where's the insecure default? |

The final report leads with a verdict (APPROVE / NEEDS-WORK / BLOCK), top priority actions, and findings grouped by lens and severity.

## Usage

```
/analyze-code
/analyze-code review the auth module
/analyze-code src/payments/ before the Q3 release
```

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — lenses, severity scale, verdict criteria, workflow, report template |
