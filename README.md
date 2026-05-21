# coding-skills

A collection of Claude Code skills for software development — reusable behavioral modules that load specialist mindsets, enforce discipline, and structure complex workflows.

## What's a Skill?

A Claude Code skill is a Markdown file (or directory) with a `SKILL.md` at the root. The file starts with a YAML header declaring a `name` and `description`. Claude Code loads it on demand via the `/skill-name` slash command, injecting focused instructions for a specific domain.

## Skills

| Skill | What it does |
|-------|-------------|
| [analyze-code](analyze-code/) | Multi-lens audit of existing code across architecture, quality, performance, security, and style. Produces a prioritized findings report — a deep review, not a gate decision. |
| [brainstorm](brainstorm/) | Turns vague ideas into concrete, validated specs through Socratic dialogue — one question at a time. No implementation until the design is approved. |
| [coding-discipline](coding-discipline/) | Names the six most common LLM coding failure modes (silent assumption, scope creep, speculative complexity, hallucination, drift, parallel solution) and the counter-move for each. |
| [style-checker](style-checker/) | Reviews code against Google's official style guidelines. Produces a structured violation report grouped by severity (Critical / High / Medium / Low). Supports Go, Java, Python, JavaScript, TypeScript, Shell, and Markdown. |
| [test-driven-development](test-driven-development/) | Enforces the Red→Green→Refactor cycle before any production code is written. Covers the full TDD workflow: writing a failing test first, minimal implementation, and safe refactoring with a green suite. |
| [using-software-specialists](using-software-specialists/) | Routes software tasks to the right specialist mindset (security engineer, architect, tester, DBA, etc.) at the right phase. Includes a task-routing table, symptom → specialist reverse lookup, and a "Validate Before Done" gate. |
| [writing-unit-tests](writing-unit-tests/) | Guides unit test authorship in any language — scenario identification across four quadrants, FIRST-U principles, Arrange–Act–Assert structure, mocking strategy, and language-specific references. |

## Installation

Copy the skill directories you want into your Claude Code skills folder:

```bash
cp -r analyze-code brainstorm coding-discipline style-checker test-driven-development using-software-specialists writing-unit-tests ~/.claude/skills/
```

Skills are then available as slash commands in any Claude Code session:

```
/analyze-code
/brainstorm
/coding-discipline
/style-checker
/test-driven-development
/using-software-specialists
/writing-unit-tests
```

## Usage

Invoke a skill by typing its slash command, optionally followed by a description of your task:

```
/brainstorm I want to build a rate limiter for our API
/style-checker review the auth module
/using-software-specialists add OAuth support to the backend
```

See each skill's own `README.md` for detailed usage, file structure, and examples.

## Workflows

A typical feature-development loop using these skills:

1. **Define** — `/brainstorm` scopes the change and produces an approved plan. For cross-repo work, save the plan to a path outside the repo (e.g., `~/plans/YYYY-MM-DD-<topic>.md`) so all repos can reference it.
2. **Build** — `/using-software-specialists` ingests the plan, validates it against the Plan-phase done-criteria, and implements. The Implementation phase loads `coding-discipline` (and optionally `/test-driven-development` + `/writing-unit-tests`) before any code is written.
3. **Audit** — `/analyze-code` reviews the result and produces a severity-ranked findings report with a *Suggested Next Actions* block that routes each finding cluster back to the right specialist.

The loop then closes through one of three back-edges:

- **Findings to apply** → re-enter `/using-software-specialists` with the specialist named in the analyze-code report.
- **Plan needs changes** → re-enter `/brainstorm` against the existing plan file. It enters revision mode — diffs the requested change, asks only about the deltas, and updates the plan in place.
- **Bug surfaced during testing** → re-enter `/using-software-specialists` starting with Troubleshooter.

`/style-checker` is invoked on demand, or implicitly by `/analyze-code` when the project has no configured linter.

```
            ┌─────────────┐
            │  brainstorm │ ◄─── plan needs changes
            └──────┬──────┘
                   │ approved plan (file)
                   ▼
      ┌────────────────────────┐
      │ using-software-        │ ◄─── findings to apply
      │   specialists          │ ◄─── bug during testing
      └────────────┬───────────┘
                   │ implemented
                   ▼
            ┌─────────────┐
            │ analyze-code│
            └─────────────┘
                   │ findings + next actions
                   └──────────► back to one of the above
```

## License

MIT — see [LICENSE](LICENSE).
