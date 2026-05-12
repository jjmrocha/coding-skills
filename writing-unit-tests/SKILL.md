---
name: writing-unit-tests
description: Use when writing, adding, modifying, refactoring, or reviewing unit tests in any language. Trigger this whenever the user asks to "add tests", "write tests for X", "improve coverage", "fix this test", starts a TDD cycle, or modifies code that has or needs tests, even when they don't say "unit tests" explicitly.
---

# Writing Unit Tests

A unit test asserts the **observable behavior** of a module, never its implementation. Given a state and an input, it verifies the output and the side effects the caller can observe. If you find yourself asserting *how* a method called its collaborators — call counts, internal field state, private method invocations — step back. That is implementation, and it should be free to change without breaking the test.

This skill covers **unit tests only** — no real I/O, no real dependencies, single-digit millisecond execution. For integration or E2E tests, the principles still apply but real services and longer runtimes are acceptable. Follow this skill in order.

---

## 1. Inspect the existing codebase first

Read 2–3 nearby test files. Note:

- File layout (mirroring production? same-package?)
- Test naming pattern
- GWT/AAA comment style and assertion library
- Mocking framework and how doubles are created
- Fixture/builder patterns

Then **read the matching reference file** (§12) for the project's stack before drafting any tests.

**Existing project conventions override the language reference.** If existing tests violate FIRST-U in damaging ways — shared mutable fixtures, mocks asserting internals, real I/O — flag the anti-pattern to the user before propagating it.

---

## 2. Workflow — four steps, in order

1. **Identify scenarios.** List every test case covering the four quadrants (§3).
2. **Get approval.** Present the scenario list as a numbered plan and wait for confirmation before writing any tests. If the user says to skip approval, proceed without waiting — but always list the scenarios at the top of your output so they can sanity-check.
3. **Write tests.** One behavior per test.
4. **Run and fix.** Execute the full suite. Never stop at red.

---

## 3. Scenario taxonomy — the four quadrants

| Quadrant | What to verify |
|----------|----------------|
| **Happy path** | Valid inputs → expected successful output |
| **Negative inputs** | Nulls, empty values, out-of-range, malformed payloads — verify explicit errors or sentinel returns |
| **Boundary conditions** | 0, 1, off-by-one, max/min length, overflow — bugs cluster here |
| **Error paths** | Dependency failures: DB down, network timeout, disk full, third-party error response |

Every acceptance criterion maps to at least one scenario. If no explicit criteria exist (legacy code, exploratory additions), derive scenarios from the function signature, doc comments, and return-value contract. If none of those exist either, read the implementation body and treat each distinct return or throw path as an implicit scenario. **One behavior per test** — if a test can fail for two unrelated reasons, split it.

---

## 4. FIRST-U principles

| Principle | What it means in practice |
|-----------|---------------------------|
| **Fast** | Single-digit milliseconds per test. No real I/O. If setup is heavy, you've crossed into integration. |
| **Isolated** | Each test sets up and tears down its own state. No shared mutable fixtures between tests. Tests run in any order, same result. |
| **Repeatable** | No real clock, RNG, network, or shared filesystem. Pin time, seed randomness, use in-memory substitutes. |
| **Self-validating** | Every test ends in explicit assertions. No "look at the output and decide". No manual setup steps. |
| **Timely** | Write tests close in time to the code (TDD or right after each small change). Old code accreting tests months later is the worst case. |
| **Understandable** | The name reads like a specification; the body is short. A reader understands what's being tested without reading the implementation. |

The most common violation is **Repeatable**: `new Date()` or real random values break determinism — pin them.

---

## 5. Arrange–Act–Assert (Given–When–Then)

Structure every test in three blocks:

1. **Arrange / Given** — create the unit under test, prepare inputs, configure doubles.
2. **Act / When** — exactly **one** call. Multiple calls = multiple behaviors; split.
3. **Assert / Then** — verify the observable result and any side effects.

Use the three marker comments in every test body — `// given` / `// when` / `// then` for C-family languages (Go, Java, JavaScript) and `# given` / `# when` / `# then` for Python. They are never optional. For multiple cases sharing the same shape, use the language's idiomatic parameterized test mechanism — see the language reference.

---

## 6. Mocking — surgical, not default

Reserve doubles for what you can't bring in cheaply: external APIs, databases, queues, file systems, time, randomness. Use real instances for value objects, DTOs, and pure functions.

| Double | When |
|--------|------|
| **Stub** | Returns canned values so the test can proceed past a dependency. |
| **Mock** | Records calls — use when a side effect *is* the behavior (e.g., "was `sendEmail` called with the right recipient?", or its negative: "was `sendEmail` **not** called on a dry-run?"). |
| **Fake** | Working in-process implementation (in-memory repo). Often the best choice. |
| **Spy** | Wraps real object + call recording — when you want real behavior *and* need to assert it was called. |
| **Dummy** | Placeholder that satisfies a parameter list but is never actually used. |

**Rule:** Verify a call only when the call is the observable outcome. If a refactor that preserves behavior breaks the test, the test is coupled to implementation — that's a smell.

**Rule:** Never mock third-party SDKs directly. Wrap them behind a port you own and mock the port — this shields tests from SDK API changes.

---

## 7. What to test, by layer

Mock at architectural boundaries you don't own: repositories, external clients, queues, file systems. Use real instances for pure functions, value objects, DTOs, and any in-process module you control. For a full per-layer breakdown see the "What to test, by layer" table in the language reference.

---

## 8. Naming and structure

**Test name = specification**: method + scenario + expected behavior. Never `test1`, `shouldWork`, `testCase`. Name the output variable `result`; expected values `expected`. For idiomatic format and casing see the language reference.

---

## 9. Test data is documentation

Use realistic, domain-valid values — `"alice@example.com"` not `"foo"`, `12500` for cents not `123`. Meaningful data makes intent obvious and surfaces bugs that generic values mask (e.g., a regex that matches `"foo"` but not real email shapes).

---

## 10. Verification

Always run the full suite after writing or modifying tests:

- A test fails for a real bug → fix the **production code**.
- A test fails because it's wrong → fix the **test**.
- Never leave a red suite or commit failing tests.

When you finish, report in this format:
```
N tests added, all passing.
Pre-existing failures: [list each with one-line note, or "none"].
```

---

## 11. Common mistakes

| Mistake | Fix |
|---------|-----|
| Asserting call counts when the call isn't the observable outcome | Assert return value or state; only assert calls when the side effect IS the behavior under test |
| Using `new Date()`, `Math.random()`, or real clocks | Pin time, seed randomness — non-determinism breaks **Repeatable** |
| Mocking the third-party SDK directly | Wrap the SDK in a port you own; mock the port — protects tests from SDK version changes |
| Silently inheriting broken patterns from existing tests | Flag the violation to the user before propagating |

---

## 12. Language references

**Read the matching reference before drafting any tests.** Each describes exact libraries, naming conventions, fixture patterns, and idiomatic styles for greenfield code:

- `references/java_unit_test.md` — JUnit 5 + AssertJ + Mockito
- `references/go_std_unit_test.md` — Go `testing` stdlib only
- `references/go_testify_unit_test.md` — Go with testify (`assert`, `require`, `mock`)
- `references/python_pytest_unit_test.md` — pytest + `monkeypatch` / `unittest.mock`
- `references/javascript_unit_test.md` — Jest (notes for Vitest, mostly the same API)

**If existing project tests differ from the reference, follow the existing tests.** The reference is the starting point for greenfield code, not a license to refactor the world.

**If the project's language has no reference file** (Kotlin, C#, Rust, Ruby, TypeScript standalone, etc.): apply FIRST-U, four-quadrant scenarios, and AAA structure universally; mirror the naming, assertion style, and mock conventions already in the project.
