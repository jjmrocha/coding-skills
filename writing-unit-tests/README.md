# writing-unit-tests

A Claude Code skill for writing unit tests in any language. Guides test scenario identification, applies the FIRST-U quality principles, enforces Arrange–Act–Assert structure, and produces a runnable, passing suite.

## When to Use

- Adding tests to new or existing code
- Improving coverage for a module or function
- Fixing or refactoring broken tests
- Starting a TDD cycle before writing production code
- Reviewing whether existing tests follow good practices

**When NOT to use:**
- Integration or E2E tests where real services are involved → FIRST-U still applies, but this skill focuses on unit-level isolation
- Diagnosing a flaky test suite → use `/using-software-specialists` with the `quality-engineer` specialist first

## How It Works

The skill follows a four-step workflow:

| Step | What happens |
|------|-------------|
| **1. Inspect** | Read 2–3 nearby test files to learn project conventions (naming, assertion library, mock framework, fixture patterns) |
| **2. Identify scenarios** | List test cases across four quadrants: happy path, negative inputs, boundary conditions, and error paths |
| **3. Get approval** | Present the scenario list and wait for confirmation before writing |
| **4. Write & run** | Implement one behavior per test, run the full suite, fix any failures |

All tests must satisfy the **FIRST-U principles** — Fast, Isolated, Repeatable, Self-validating, Timely, Understandable — and be structured with Arrange–Act–Assert (Given–When–Then).

## Usage

```
/writing-unit-tests
/writing-unit-tests add tests for the UserService
/writing-unit-tests improve coverage on the payment module
```

## Blueprint

The rules in this skill — mindset, FIRST-U principles, scenario taxonomy, AAA structure, mocking strategy, naming conventions, and layer-by-layer guidance — were derived from:

**[docs/how-to-write-unit-tests.md](docs/how-to-write-unit-tests.md)**

That document is the canonical reference. [`SKILL.md`](SKILL.md) is its Claude-optimized, actionable form.

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Core skill — workflow, FIRST-U table, four-quadrant taxonomy, mocking guide, naming conventions, language dispatch |
| [docs/how-to-write-unit-tests.md](docs/how-to-write-unit-tests.md) | Blueprint — the canonical document from which this skill's rules were derived |
| [references/java_unit_test.md](references/java_unit_test.md) | JUnit 5 + AssertJ + Mockito patterns |
| [references/go_std_unit_test.md](references/go_std_unit_test.md) | Go `testing` stdlib patterns |
| [references/go_testify_unit_test.md](references/go_testify_unit_test.md) | Go with testify (`assert`, `require`, `mock`) |
| [references/python_pytest_unit_test.md](references/python_pytest_unit_test.md) | pytest + `monkeypatch` / `unittest.mock` |
| [references/javascript_unit_test.md](references/javascript_unit_test.md) | Jest (with notes for Vitest) |
