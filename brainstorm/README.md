# brainstorm

A Claude Code skill for Socratic requirements discovery. Turns vague ideas
into concrete, validated designs through guided dialogue — one question at a
time, no implementation until the design is approved. Only writes a spec
file when the user explicitly asks for it.

## When to Use

* A user presents a vague idea ("I want to build X")
* Requirements are unclear and need to be drawn out before coding
* A feature should be scoped and designed before a plan is written

## Usage

```
/brainstorm
/brainstorm I want to build a rate limiter for our API
/brainstorm add collaborative editing to the document service
```

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — workflow, Socratic rules, principles |
| [references/spec-template.md](references/spec-template.md) | Starting structure for the output spec |
| [expected_outputs/sample-session.md](expected_outputs/sample-session.md) | Worked example session |

## Credit

Based on the [SuperClaude Framework's `/sc:brainstorm` command](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/src/superclaude/commands/brainstorm.md)
(MIT-licensed).
