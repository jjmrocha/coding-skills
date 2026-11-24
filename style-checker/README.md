# style-checker

A Claude Code skill that reviews code against **Google's official style
guidelines**, for formatting and naming conventions only. It produces a
violation report grouped by severity (Critical, High, Medium and Low). It
reports the violations for you to fix and does not fix them itself.

For logic, architecture or code-quality concerns (SOLID, code smells and
similar), use the `analyze-code` skill instead.

## When to use

- "Check my code style" or "does this follow Google style?"
- Auditing naming conventions, indentation, line length and import ordering.
- Quick questions such as "how should I name constants in Go?"

## Supported languages

C++, C#, Go, Haskell, HTML/CSS, Java, JavaScript, JSON, Kotlin, Python,
TypeScript, Shell and Markdown.

## Output

[expected_outputs/sample-report.md](expected_outputs/sample-report.md) shows a
full example. A report has a summary, the violations grouped by severity and
language, and a list of clean files.

## Usage

```
/style-checker
/style-checker review the auth module
```
