# brainstorm

A Claude Code skill for Socratic requirements discovery. It turns a vague idea
into a concrete, validated design through questions, asked one at a time.
Nothing is implemented until you approve the design.

Brainstorm splits every feature into small sub-tasks and saves the agreed
scope and the sub-task list in a feature plan. It then designs one sub-task at
a time. Each approved design, the spec, is saved in that sub-task's section of
the feature plan, and `/using-software-specialists` implements it from there.

## When to use

- You present a vague idea, such as "I want to build X".
- The requirements are unclear and must be drawn out before coding.
- A feature should be scoped and designed before any code is written.
- An existing feature plan must change. Brainstorm asks only about the parts
  that change and updates the plan in place.

## Usage

```
/brainstorm
/brainstorm I want to build a rate limiter for our API
/brainstorm add collaborative editing to the document service
/brainstorm continue the notifications feature
```

[A worked example session](expected_outputs/sample-session.md) shows the
dialogue from start to end.

## Credit

Based on the [SuperClaude Framework's `/sc:brainstorm` command](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/src/superclaude/commands/brainstorm.md)
(MIT-licensed).
