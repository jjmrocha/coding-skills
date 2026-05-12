# How to Write Unit Tests

---

## 1. Mindset

A unit test asserts the **observable behavior** of a module, never its implementation.

> A module has a state. When it receives a specific input, it produces a specific output and a specific set of side effects. The test asserts exactly that — given a state, when an input arrives, the observable output and side effects match what was expected.

If you find yourself asserting *how* a method called its collaborators (interaction verification, internal field state, call counts), step back. The right question is *what the caller observes* — return values, state changes, emitted events, written rows, response bodies. That is the contract; everything else is an implementation detail that should be free to change without breaking the test.

---

## 2. Workflow

Follow these steps to write good tests:

1. **Identify Scenarios** — list the test scenarios (edge cases, success paths, error handling).
2. **Write Tests** — implement the tests based on the previous list.
3. **Run and Fix** — execute all tests and fix any failures before considering the work done.

---

## 3. Defining Test Scenarios

### 3.1 One Behavior per Test

Avoid "megatests" that verify multiple behaviors at once. Each test should focus on a single concept or condition. If a test fails, it should be immediately obvious which specific rule was broken.

### 3.2 Cover the Four Quadrants of Inputs

To ensure comprehensive coverage, identify scenarios across four distinct areas:

- **Happy Path** — valid inputs that lead to a successful outcome.
- **Negative Scenarios** — invalid inputs (e.g., empty strings, nulls, wrong types) that should be handled gracefully.
- **Boundary Conditions** — the exact limits of a system (e.g., exactly 0 balance, maximum character limit, off-by-one values).
- **Exception / Error Paths** — the system's response when a dependency fails (e.g., database is down, network timeout, disk full).

### 3.3 Map to User Stories (Acceptance Criteria)

Whenever possible, test scenarios should be derived directly from User Story acceptance criteria.

- **Strategy:** Use *Example Mapping* to break a user story into concrete rules and examples. Each example naturally becomes a test scenario.
- **Verification:** Ensure every business requirement links back to at least one test scenario through a Traceability Matrix to avoid coverage gaps.

---

## 4. Rules for Writing Good Unit Tests — The FIRST-U Principles

### Fast

Unit tests must execute quickly; slow tests erode the feedback loop that makes testing valuable. In TDD, short iterations of "change code → run tests" are the norm — if the tests are slow, the methodology loses its power.

**Why it matters:** on a sufficiently large system you may have thousands of tests. If 2,000 tests average 200 ms each, a full suite takes ~6.5 minutes. Run that several times a day and the cost compounds. As the codebase grows, slow tests become a bottleneck that discourages developers from running them at all.

**Guidelines:**
- A single unit test should complete in **single-digit milliseconds**.
- Eliminate I/O (network, disk, database) from unit tests; use fakes or in-memory substitutes.
- If a test needs a heavy setup phase, consider whether it has crossed the boundary into integration testing.

### Isolated / Independent

Tests must never depend on other tests. You should be able to run any single test, at any time, in any order, and get the same result.

**Why it matters:** inter-dependent tests create false positives and false negatives. When a chain of tests fails, you waste time tracing which test introduced the problem instead of fixing the actual defect.

**Guidelines:**
- Each test sets up its own state and tears it down afterward.
- Apply the Single Responsibility Principle: if a test can fail for more than one unrelated reason, split it.
- Avoid shared mutable state across tests (static variables, class-level fields mutated between tests).

### Repeatable

A repeatable test produces the same result every time it runs, regardless of environment, time of day, or execution order.

**Why it matters:** flaky tests destroy trust in the test suite. Developers begin ignoring failures, and real bugs slip through.

**Guidelines:**
- Isolate tests from anything not under your direct control (system clock, network, filesystem, random number generators).
- Use deterministic fakes, stubs, or in-memory databases instead of shared external resources.
- If you must interact with an external system, use a private sandbox to avoid conflicts with other developers.

### Self-Validating

Each test must be able to determine on its own whether it passed or failed. There must be no manual interpretation of results.

**Guidelines:**
- Every test ends with explicit assertions, not console output that a human must inspect.
- Automate all setup — do not require manual steps (pre-cooked data, manually started services) before the test can run.
- For database-dependent logic, create an in-memory database, build the schema, and insert test data programmatically.

### Timely

Write tests close in time to the code they verify. You *can* write tests after the code is production-ready, but you gain far more value by writing them during development.

**Guidelines:**
- Adopt TDD or write tests immediately after each small unit of functionality.
- Establish team guidelines or automated gates (PR checks, coverage thresholds) that reject code without sufficient tests.
- Writing smaller chunks of code before tackling the corresponding test makes both the code and the test easier to write.

### Understandable

A test is documentation. Anyone reading it — including your future self — should understand what is being tested, under what conditions, and what the expected outcome is, without needing to read the implementation.

**Guidelines:**
- Use descriptive test names that read like a specification, e.g., `transferFunds_insufficientBalance_throwsOverdraftException`.
- Never name tests `test1`, `test2`, etc.
- Keep the test body short and readable; extract complex setup into well-named helper methods.

---

## 5. Test Organization

### 5.1 Arrange–Act–Assert (Given–When–Then)

Structure every test in three clearly separated sections:

1. **Arrange (Given)** — initialize the unit under test in a specific state, create mocks/stubs, and define the expected result.
2. **Act (When)** — execute the single operation being tested.
3. **Assert (Then)** — compare the actual output with the expected output.

Keep the Act section to a single method call. If you need multiple calls, you may be testing more than one behavior.

### 5.2 Table-Driven / Parameterized Tests

When multiple scenarios share the same test structure but differ only in inputs and expected outputs, prefer table-driven (parameterized) tests. They reduce duplication and make the scenario list easy to read and extend.

```
// Pseudocode example
testCases = [
    { scenario: "positive numbers",  a: 2,  b: 3,  expected: 5  },
    { scenario: "negative numbers",  a: -1, b: -1, expected: -2 },
    { scenario: "zero operand",      a: 0,  b: 5,  expected: 5  },
]

for each case in testCases:
    result = add(case.a, case.b)
    assertEqual(result, case.expected, case.scenario)
```

---

## 6. Mocking

Use mocking as a surgical tool, not a default. Over-mocking leads to brittle tests that pass even when the system is broken, because they only verify that mocks were called — not that the logic is correct.

### 6.1 Mock Only What You Must

Prioritize real objects for internal logic and reserve mocks for external or unstable boundaries.

- **Mock:** out-of-process dependencies — APIs, databases, file systems, message queues — to keep tests fast and repeatable.
- **Don't Mock:** value objects, DTOs, or simple utility classes. If a class is fast to instantiate and side-effect-free, the real object increases test fidelity.

### 6.2 Choose the Right Test Double

Not every fake is a mock. Using the correct type keeps test intent clear:

- **Stub** — provides canned answers; use when you just need a dependency to return a value so the test can proceed.
- **Mock** — records interactions for later verification; use when a side effect *is* the behavior under test (e.g., "was `sendEmail` called exactly once with the correct recipient?").
- **Fake** — a simplified but working implementation (e.g., an in-memory repository instead of a real database).
- **Spy** — wraps a real object and records calls; useful when you want real behavior *plus* interaction verification.
- **Dummy** — a placeholder passed to satisfy a parameter list but never actually used.

### 6.3 Avoid Implementation Coupling

The biggest mocking pitfall is verifying every internal method call. This makes refactoring impossible because any structural change breaks the test — even if the output remains correct.

**Rule of thumb:** only verify interactions that produce an observable side effect you care about (an email sent, a row written, an event published). If no side effect exists, assert the return value instead.

### 6.4 Don't Mock Third-Party Code Directly

Avoid mocking libraries you don't own (AWS SDK, an ORM, a payment gateway). Instead, wrap them behind an interface (port/adapter) you control, and mock that interface. This protects your tests from breaking when the library updates its API.

---

## 7. What to Test — Layer by Layer

### 7.1 Controllers / Handlers

- Mock the service layer.
- Focus on the contract:
  - Parameter validation (types, required fields, allowed ranges).
  - Payload validation (request body structure, missing fields).
  - Security checks (authentication, authorization).
  - Response format (status codes, response body shape, headers).

### 7.2 Services / Use Cases

- Mock the repository (data access) layer.
- Mock external service clients.
- Do **not** mock internal modules unless they carry external dependencies.
- Test the business logic: given a state, when the function is called with these inputs, it produces the expected outputs and/or the expected side effects.

### 7.3 Builders / Mappers / Transformers

- Avoid mocks entirely — these are pure functions or close to it.
- Verify that every combination of inputs produces the correct output.
- Good candidates for table-driven / parameterized tests.

### 7.4 External Service Clients (REST, gRPC, etc.)

- If possible, mock the external service at the HTTP level (e.g., WireMock, MockServer, `nock`, `httptest`) so your production code is exercised unchanged.
- Test how your code handles every response scenario: success, client errors (4xx), server errors (5xx), timeouts, malformed bodies.
- Assert that outbound requests conform to the contract: correct URL, parameters, headers, and payload.

### 7.5 Event Producers / Consumers

- Verify the event payload is correct (schema, required fields, serialization).
- For consumers, test behavior for valid events, malformed events, and duplicate events.

---

## 8. Naming Conventions

### 8.1 Test Names

Use descriptive names that read as specifications. A popular pattern is:

```
methodUnderTest_scenario_expectedBehavior
```

Examples:
- `withdraw_insufficientBalance_throwsOverdraftException`
- `parseDate_invalidFormat_returnsNull`
- `createOrder_validCart_persistsOrderAndSendsConfirmation`

### 8.2 Variables Inside Tests

- Use the **same parameter names** as the function under test for input variables — this makes the connection obvious.
- Name the actual output `result` (or `actual`).
- Name the expected value `expected` or `expectedXxx` (e.g., `expectedTotal`).

---

## 9. Test Data as Documentation

Unit tests are living documentation of the system. When defining test data, use realistic, domain-valid values rather than throwaway strings like `"foo"` or `"test123"`. Meaningful data makes the test's intent clearer and can expose issues that generic data would hide.

---

## 10. Verification

Always run the full test suite after writing or modifying tests.

- If a test fails because of a bug in the production code — fix the code.
- If a test fails because the test itself is wrong — fix the test.
- Never leave a red test suite and move on.
