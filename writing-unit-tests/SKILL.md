---
name: writing-unit-tests
description: Use when writing unit tests for specific code — adding tests, improving coverage, or starting a TDD cycle. Triggers on "add tests", "write tests for X", or when modifying code that needs tests.
---

# Writing Unit Tests

A unit test asserts **observable behavior**, never implementation. Given state + input, verify output + side effects the caller can observe. If you're asserting call counts, internal fields, or private methods, step back.

For a detailed human-readable guide, see [docs/how-to-write-unit-tests.md](docs/how-to-write-unit-tests.md).

## Steps

1. **Inspect existing tests** — read 2-3 nearby test files. Note naming, assertion library, mock framework, fixture patterns. Existing project conventions override the language reference.
2. **List scenarios** — enumerate cases across the four quadrants. Present for confirmation before writing (skip if user says proceed).
3. **Read the language reference** — pick the matching file from the dispatch table below.
4. **Write tests** — one behavior per test. AAA structure. Run the full suite — never leave it red.

## Scenario Quadrants

| Quadrant | What to verify |
|----------|----------------|
| **Happy path** | Valid inputs → expected successful output |
| **Negative inputs** | Nulls, empty, out-of-range, malformed — expect explicit errors or sentinel returns |
| **Boundary conditions** | 0, 1, off-by-one, max/min, overflow — bugs cluster here |
| **Error paths** | Dependency failures: DB down, network timeout, third-party error response |

## FIRST-U

| Principle | Rule |
|-----------|------|
| **Fast** | Single-digit ms. No real I/O. |
| **Isolated** | No shared state. Tests run in any order. |
| **Repeatable** | No real clock, RNG, network, or filesystem. Pin time, seed randomness. |
| **Self-validating** | Explicit assertions. No manual inspection. |
| **Timely** | Write with the code, not months later. |
| **Understandable** | Name reads like a spec; body is short. A reader understands what's tested without reading the implementation. |

## Structure: Arrange–Act–Assert

1. **Arrange** — create unit under test, prepare inputs, configure doubles
2. **Act** — exactly one call. Multiple calls = multiple behaviors; split.
3. **Assert** — verify observable result and side effects

Use `// given` / `// when` / `// then` comments only if the existing codebase uses them.

## Mock Rules

- **Mock at boundaries** — external APIs, databases, queues, filesystem, time, randomness
- **Don't mock internals** — value objects, DTOs, pure functions use real instances
- **Mock your own port, not the third-party SDK** — wrap external libraries behind an interface you control

## Language References

Read the matching reference before drafting tests. If no reference exists for the project's language, apply the principles above universally and mirror existing project conventions.

| Reference | Stack |
|-----------|-------|
| [javascript_unit_test.md](references/javascript_unit_test.md) | Jest / Vitest |
| [python_pytest_unit_test.md](references/python_pytest_unit_test.md) | pytest + monkeypatch / unittest.mock |
| [java_unit_test.md](references/java_unit_test.md) | JUnit 5 + AssertJ + Mockito |
| [go_std_unit_test.md](references/go_std_unit_test.md) | Go `testing` stdlib |
| [go_testify_unit_test.md](references/go_testify_unit_test.md) | Go + testify |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asserting call counts when output would do | Assert return value; mock only when the side effect IS the behavior |
| `new Date()`, `Math.random()`, real clock | Pin time, seed randomness — non-determinism breaks Repeatable |
| Mocking the third-party SDK directly | Wrap in a port you own, mock the port |
| Silently copying broken patterns from existing tests | Flag the anti-pattern to the user |