# using-software-specialists

A Claude Code skill that loads specialist mindsets (security engineer, system
architect, tester, frontend engineer and others) at the right phase of a
software task. The premise is that every task touches several domains, and a
single generalist view misses the vulnerabilities, accessibility gaps and
quality failures that a specialist catches.

## When to use

Any non-trivial software task: a feature, bug fix, refactor, deployment,
performance work, troubleshooting or planning. Skip it only for one-line fixes
that affect no other domain.

## Specialists

Backend Engineer, Frontend Engineer, System Architect, Database Designer,
Security Engineer, Quality Engineer, Tester, DevOps Engineer, Performance
Engineer, Refactoring Expert, Troubleshooter, Requirements Analyst, Project
Planner, Deep Research Agent, Technical Writer, Prompt Engineer, ML Engineer.

## Usage

```
/using-software-specialists add OAuth support to the backend
/using-software-specialists the nightly export job fails since yesterday's deploy
```

## Credit

Based on the
[SuperClaude Framework's `agents/` library](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/master/src/superclaude/agents)
(MIT-licensed). The per-specialist reference files adapt SuperClaude's section
schema and several of its specialist roles. The orchestration layer (the phase
model, the task routing, the disambiguation and the "Validate Before Done"
checklist) is original to this skill.
