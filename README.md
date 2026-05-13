# coding-skills

A collection of Claude Code skills for software development — reusable behavioral modules that load specialist mindsets, enforce discipline, and structure complex workflows.

## What's a Skill?

A Claude Code skill is a Markdown file (or directory) with a `SKILL.md` at the root. The file starts with a YAML header declaring a `name` and `description`. Claude Code loads it on demand via the `/skill-name` slash command, injecting focused instructions for a specific domain.

## Skills

| Skill | What it does |
|-------|-------------|
| [analyze-code](analyze-code/) | Multi-lens audit of existing code across architecture, quality, performance, and security. Produces a prioritized findings report with an APPROVE / NEEDS-WORK / BLOCK verdict. |
| [brainstorm](brainstorm/) | Turns vague ideas into concrete, validated specs through Socratic dialogue — one question at a time. No implementation until the design is approved. |
| [coding-discipline](coding-discipline/) | Names the five most common LLM coding failure modes (silent assumption, scope creep, speculative complexity, hallucination, drift) and the counter-move for each. |
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

## License

MIT — see [LICENSE](LICENSE).
