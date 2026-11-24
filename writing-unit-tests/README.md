# writing-unit-tests

A Claude Code skill for writing unit tests in any language. The agent reads
[SKILL.md](SKILL.md), a short checklist. People read
[docs/how-to-write-unit-tests.md](docs/how-to-write-unit-tests.md), the
detailed guide with the reasons and examples.

## When to use

- Adding tests to new or existing code.
- Improving coverage for a module or function.
- Fixing or refactoring broken tests.
- Reproducing a proven bug with a failing test before fixing it.
- Reviewing whether existing tests follow good practice.

## When not to use

- Integration or end-to-end tests that use real services. The FIRST-U
  principles still apply, but this skill is about tests of isolated units.
- Diagnosing a flaky test suite. Use `/using-software-specialists` with the
  quality-engineer specialist first.

## How it works

The skill first reads the project's existing tests to learn its conventions.
Test files named in CLAUDE.md take priority over the tests next to the code.
It then lists the test cases in four groups (happy path, negative inputs,
boundary conditions and error paths) and asks you to confirm them before it
writes anything. It writes one behavior per test, runs the full suite, and never
leaves it failing. For a test whose contract is a side effect on a mock, it breaks
that side effect once to prove that the test fails.

Every test must meet the **FIRST-U principles** (Fast, Isolated, Repeatable,
Self-validating, Timely, Understandable) and follow the Arrange, Act, Assert
structure, also called Given, When, Then.

Language references cover Go (standard library and testify), Java, JavaScript
and Python with pytest.

## Usage

```
/writing-unit-tests
/writing-unit-tests add tests for the UserService
/writing-unit-tests improve coverage on the payment module
```
