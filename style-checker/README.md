# style-checker

A Claude Code skill that reviews code against **Google's official style guidelines**, focused on formatting and naming conventions only. Produces a structured violation report grouped by severity (Critical / High / Medium / Low).

For logic, architecture, or code-quality concerns (SOLID, code smells, etc.), use the `code-reviewer` skill instead.

## When to Use

- "Check my code style" / "does this follow Google style?"
- Auditing naming conventions, indentation, line length, import ordering
- Quick advisor questions ("how should I name constants in Go?")

## Supported Languages

Go, Java, Python, JavaScript, TypeScript, Shell, Markdown.

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — workflow, severity rubric, common mistakes |
| [references/](references/) | One file per supported language with the Google style rules |
| [expected_outputs/sample-report.md](expected_outputs/sample-report.md) | Reference output format for the violation report |

## Output Format

See [expected_outputs/sample-report.md](expected_outputs/sample-report.md) for a full example. Reports include a summary, violations grouped by severity and language, and a "Clean files" section.
