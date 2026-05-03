---
name: style-checker
description: "Use when checking, reviewing, or auditing code style, formatting, or naming conventions — even if the user just says 'check my code style' or 'does this follow Google style'."
---

# Google Style Checker

Reviews code files in a repository against Google's official style guidelines, focusing on **formatting** and **naming conventions** only. Produces a structured violation report grouped by severity.

## Scope

This skill covers **formatting and naming conventions only**. It does not check logic, architecture, or code quality (SOLID, code smells, etc.). It also does not attempt to auto-fix issues or rewrite code, but rather reports violations clearly for developers to address.

Supported languages: **Go, Java, Python, JavaScript, TypeScript, Shell, Markdown**

## Workflow

### Step 1: Identify languages and load references

Scan the repo to identify which supported languages are present. For each language found, read the corresponding reference file **before** scanning code:

| Language | Reference file | Detection |
|----------|---------------|-----------|
| Python | `references/python.md` | `*.py` |
| Java | `references/java.md` | `*.java` |
| JavaScript | `references/javascript.md` | `*.js`, `*.jsx`, `*.mjs` |
| TypeScript | `references/typescript.md` | `*.ts`, `*.tsx` |
| Go | `references/go.md` | `*.go` |
| Shell | `references/shell.md` | `*.sh`, `*.bash` |
| Markdown | `references/markdown.md` | `*.md` |

If the user specifies files or a directory, limit the scan to those. Otherwise scan the full repo (skip `vendor/`, `node_modules/`, `.git/`, and files with `// Code generated` or `# Generated` headers).

If no supported-language files are detected, report this to the user and exit.

### Step 2: Advisor mode (optional)

If the user asks a style question rather than requesting a file scan (e.g., "how should I name constants in Go?"), answer directly from the loaded reference without scanning files. You can do both: answer the question, then optionally offer to scan relevant files.

### Step 3: Scan for violations

For each file, check against the rules in the reference. Focus on:
- Naming conventions (case style for identifiers, packages, files)
- Formatting (indentation, line length, brace style)
- Import/module organization
- Comment and documentation style

Flag each violation with:
- **File path and line number** (or line range)
- **Rule violated** (short description)
- **What was found** vs **what is expected**
- **Severity** (see below)

### Step 4: Produce the report

Structure violations as follows:

```
# Google Style Check Report

## Summary
- Files scanned: N
- Languages: [list]
- Total violations: N (Critical: N, High: N, Medium: N, Low: N)

## Critical
### <Language>
- `path/to/file.go:12` — **Rule**: Expected `lowerCamelCase` for unexported function, found `my_Function`

## High
### <Language>
- `path/to/file.py:45` — **Rule**: Class names must use `CapWords`, found `my_class`

## Medium
### <Language>
- `path/to/file.java:88` — **Rule**: Line exceeds 100 characters (found 117)

## Low
### <Language>
- `path/to/file.ts:10` — **Rule**: Use `import type` for type-only imports

## Clean files
List any files with zero violations. Omit this section if all files have violations.
```

## Severity Classification

| Severity | What it covers |
|----------|---------------|
| **Critical** | Wrong exported/unexported casing in Go; tabs vs spaces; fundamental structure violations |
| **High** | Wrong case style for identifiers (classes, functions, constants, variables) |
| **Medium** | Line length, indentation size, brace placement, import ordering |
| **Low** | Comment formatting, blank lines, minor whitespace, optional style preferences |

## Tips

- When scanning large repos, prioritize source files over test/generated files unless the user asks otherwise.
- If a file has many violations of the same rule, report the first 3 occurrences and note "and N more".
- Go projects: `gofmt` compliance is the source of truth — note if running `gofmt` would fix issues automatically.
- See `expected_outputs/sample-report.md` for a full example of the violation report format.

## Common Mistakes

- **Scanning test/spec files by default**: when the user says "check my code", deprioritize `*_test.go`, `*.spec.*`, `test_*.py` etc. unless explicitly asked to include them.
- **Wrong severity for Go constants**: `UPPER_SNAKE_CASE` in Go is a **Critical** violation (breaks the fundamental MixedCaps rule), not High.
- **Flagging generated or vendored code**: skip `vendor/`, `*.pb.go`, `*_generated.go`, and any file whose first lines contain `// Code generated` or `# Generated` — even if the explicit header is missing, known generated file patterns should be excluded.
