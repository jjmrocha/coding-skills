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

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Phase model, task routing, anti-patterns, validation gate |
| [references/specialist-questions.md](references/specialist-questions.md) | The one disambiguating question each specialist asks — load when unsure which to invoke |
| [references/](references/) | One file per specialist (17 total) — triggers, mindset, focus areas, red flags |

## Specialists

Backend Engineer, Frontend Engineer, System Architect, Database Designer,
Security Engineer, Quality Engineer, Tester, DevOps Engineer, Performance
Engineer, Refactoring Expert, Troubleshooter, Requirements Analyst, Project
Planner, Deep Research Agent, Technical Writer, Prompt Engineer, ML Engineer.

## Credit & What's Adapted

This skill is **based on the
[SuperClaude Framework's `agents/` library](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/master/src/superclaude/agents)**
(MIT-licensed). The work is a substantial adaptation, not a copy — here's
what's borrowed and what's original.

### Adapted from SuperClaude

* **The per-specialist file template.** Every file in
  [references/](references/) is adapted from SuperClaude's section schema
  (`Triggers / Behavioral Mindset / Focus Areas / Key Actions / Outputs /
  Boundaries`), with a `name / description` frontmatter. The current schema
  trims Key Actions, Outputs, and Boundaries down to a single
  `Hands off to:` line.
* **~10 of the 16 specialist names**, some renamed: `security-engineer`,
  `requirements-analyst`, `system-architect`, `technical-writer`,
  `performance-engineer`, `quality-engineer`, `refactoring-expert`,
  `deep-research-agent` are direct counterparts; `troubleshooter` ≈
  SuperClaude's `root-cause-analyst`; `project-planner` ≈ `pm-agent`;
  `backend-engineer` / `frontend-engineer` ≈ `backend-architect` /
  `frontend-architect`.
* **General topic coverage** within each file's `Focus Areas` section.

### Original to this skill

* **The entire [SKILL.md](SKILL.md)**: phase model (Requirements → Design →
  Plan → Implementation → Testing → Validation → Documentation),
  transition signals, Task Routing table, "The Question Each Specialist Asks"
  disambiguation (in [references/specialist-questions.md](references/specialist-questions.md)),
  Anti-Patterns table, "Validate Before Done" checklist, Tester vs. Quality
  Engineer distinction. SuperClaude uses `@agent-*` invocations rather than
  a phase-routing skill — the orchestration layer here is new.
* **4 specialists not in SuperClaude:** `prompt-engineer`, `tester`,
  `database-designer`, `ml-engineer`.
* **`Red Flags` table** at the bottom of each reference file
  (rationalization → reality).
* **`Skip when:` line** under each `## Triggers` section.
* **Sharper, more concrete content** in each file's `Behavioral Mindset`
  and `Focus Areas` (e.g., security-engineer's "make the insecure path
  hard, not just the secure path documented" vs. SuperClaude's generic
  "zero-trust mindset").
