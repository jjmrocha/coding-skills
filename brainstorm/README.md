# brainstorm

A Claude Code skill for Socratic requirements discovery. Turns vague ideas
into concrete, validated designs through guided dialogue — one question at a
time, no implementation until the design is approved. The approved design
(the spec) lives in the conversation; brainstorm then hands off to planning,
which produces the durable plan.

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

See [a worked example session](expected_outputs/sample-session.md) for what the dialogue looks like end to end.

## Credit

Based on the [SuperClaude Framework's `/sc:brainstorm` command](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/src/superclaude/commands/brainstorm.md)
(MIT-licensed).
