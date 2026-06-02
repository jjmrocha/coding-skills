# using-software-specialists

A Claude Code skill that loads domain-specific specialist mindsets (security
engineer, system architect, tester, frontend engineer, etc.) at the right
phase of a software task. The premise: every task touches multiple domains,
and a single generalist perspective misses vulnerabilities, accessibility
gaps, and quality failures that specialist thinking catches.

## When to Use

Any non-trivial software task — feature, bug fix, refactor, deployment,
performance work, troubleshooting, planning. Skip only for one-line fixes
with no cross-domain impact.

## Specialists

Backend Engineer, Frontend Engineer, System Architect, Database Designer,
Security Engineer, Quality Engineer, Tester, DevOps Engineer, Performance
Engineer, Refactoring Expert, Troubleshooter, Requirements Analyst, Project
Planner, Deep Research Agent, Technical Writer, Prompt Engineer, ML Engineer.

## Credit

Based on the
[SuperClaude Framework's `agents/` library](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/master/src/superclaude/agents)
(MIT-licensed). The per-specialist reference files adapt SuperClaude's section
schema and several of its specialist roles; the orchestration layer — the phase
model, Task Routing, disambiguation, and "Validate Before Done" checklist — is
original to this skill.
