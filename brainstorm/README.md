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
* A feature splits into atomic parts — brainstorm agrees scope, saves a
  feature plan with the sub-tasks, then designs, plans and hands off one
  sub-task at a time

## Usage

```
/brainstorm
/brainstorm I want to build a rate limiter for our API
/brainstorm add collaborative editing to the document service
/brainstorm continue the notifications feature
```

See [a worked example session](expected_outputs/sample-session.md) for what the dialogue looks like end to end.

## Credit

Based on the [SuperClaude Framework's `/sc:brainstorm` command](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/src/superclaude/commands/brainstorm.md)
(MIT-licensed).
