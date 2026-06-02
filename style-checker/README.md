# style-checker

A Claude Code skill that reviews code against **Google's official style
guidelines**, focused on formatting and naming conventions only. Produces a
structured violation report grouped by severity (Critical / High / Medium /
Low). It reports violations for you to fix — it does not auto-fix.

For logic, architecture, or code-quality concerns (SOLID, code smells,
etc.), use the `analyze-code` skill instead.

## When to Use

* "Check my code style" / "does this follow Google style?"
* Auditing naming conventions, indentation, line length, import ordering
* Quick advisor questions ("how should I name constants in Go?")

## Supported Languages

Go, Java, Python, JavaScript, TypeScript, Shell, Markdown.

## Output Format

See [expected_outputs/sample-report.md](expected_outputs/sample-report.md)
for a full example. Reports include a summary, violations grouped by
severity and language, and a "Clean files" section.
