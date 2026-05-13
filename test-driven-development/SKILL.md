---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing any production code. Trigger this whenever the user says "implement X", "add feature Y", "fix bug Z", "build a function that…", starts a coding task from scratch, or modifies existing behavior — even if they don't say "TDD" or "tests". This skill must run before implementation, not after. If you're about to write production code without having seen a failing test first, stop and use this skill.
---

# Test-Driven Development

Write the test first. Watch it fail. Write minimal code to pass it. Clean up.

That order matters because tests written *before* code force you to think through the interface, edge cases, and failure modes before you're committed to an implementation. Tests written *after* only verify what you already built — they confirm, not specify.

The goal isn't ritual compliance. It's producing focused, testable code where every behavior is covered by a test that actually proved something by failing first.

---

## The cycle

```
RED → GREEN → REFACTOR → repeat
```

Each step has a gate. Don't proceed until the gate clears.

### RED — Write a failing test

Write one test for the *next* behavior you want to add. Not several. One.

The test should:
- Name the behavior, not the mechanism (`calculates_discount_for_bulk_orders`, not `test_function`)
- Assert what the caller observes — return value, raised error, emitted event — not how the internals work
- Use the API you *wish* existed, not the one you're about to write

**Gate:** Run the test. Confirm it fails. Confirm it fails for the right reason — "function doesn't exist" or "assertion failed on expected behavior", not "syntax error" or "import missing". If it passes immediately, you're testing existing behavior; rewrite the test.

See [@writing-unit-tests](../writing-unit-tests/SKILL.md) for guidance on scenario selection, test structure, and what makes a test worth keeping.

### GREEN — Write the minimum code to pass

Write *just enough* production code to turn red into green. No more.

Not the clever solution. Not the general solution. The smallest thing that makes the test pass without cheating (hardcoding the test's expected value, skipping the logic, etc.). The test defines the scope — every line you write beyond what the test requires is scope creep.

See [@coding-discipline](../coding-discipline/SKILL.md) — the scope creep and speculative complexity failure modes apply directly here.

**Gate:** Run the full suite. Every test — not just the new one — must be green. If you broke something, fix it now. Don't move to refactor with a failing test.

### REFACTOR — Clean up without adding behavior

With everything green, improve the code: remove duplication, sharpen names, extract helpers. Change only *how* the code is structured, not *what* it does.

**Gate:** Suite must stay green throughout. If a refactor breaks a test, either the refactor changed behavior (undo it) or the test was testing implementation (fix the test). Don't ship a passing-but-messy refactor just to move on — this is where sustainable code is made.

For significant structural changes (applying SOLID principles, breaking apart large classes, strangler-fig migrations), load the [Refactoring Expert](../using-software-specialists/references/refactoring-expert.md) specialist from `using-software-specialists` — it covers scope control, knowing when to stop, and safe incremental transformation.

Then repeat. Write the next failing test.

---

## When code already exists

If you're adding to or fixing existing code, the cycle adapts — you don't start from zero.

**Adding new behavior to existing code:** Write the failing test for the new behavior before touching the implementation. The existing code stays; only the new behavior needs a test-first approach.

**Fixing a bug:** Write a test that reproduces the bug before applying the fix. The test failing on the current code is your proof the bug exists; it passing after the fix is your proof it's resolved.

**Refactoring existing code:** Characterize the current behavior with tests first. Run them green on the *unmodified* code. Then refactor — the suite is your safety net throughout. (See the REFACTOR section above.)

**Starting fresh:** Write the test before writing any production code. If you have exploratory sketch code that helped you understand the problem, that's fine — but treat it as scratch work. Write tests against the design you want, then implement against those tests. Peeking at your sketch while writing tests is fine; letting the sketch drive the tests defeats the purpose.

---

## When TDD is harder

### "I don't know the right interface yet"

That's a signal, not an obstacle. Write the test using the interface you *wish* existed. If the test feels awkward to write, the interface is probably awkward to use. Let the test drive the design.

### "The existing code has no tests"

Characterize the existing behavior with tests first, then modify. Write tests that pass on the current code before touching anything — that's your baseline. Then make the change and watch the relevant tests go red → green.

### "This is a bug fix"

A failing test that reproduces the bug is the proof that the bug existed and the fix works. Write the test first, watch it fail, then fix. The test stays in the suite as a regression guard.

### "This is a UI component / infrastructure / glue code"

TDD applies more broadly than it might seem. For infrastructure, write tests against the interface (e.g., "the cache returns stale values after TTL"). For UI, write tests against observable state (e.g., "submit button is disabled when form is empty"). The grain of the test adapts; the order doesn't.

---

## Common shortcuts and why they don't work

| Shortcut | What actually happens |
|---|---|
| Write tests after, same coverage | Tests-after confirm what you built. Tests-before specify what to build. Fundamentally different information. |
| "I manually tested every path" | Manual tests don't run on CI, don't prevent regressions, and don't document the expected behavior for the next developer. |
| "Too simple to need a test" | Simple code breaks under refactoring. A 3-line test costs less than the future debugging session. |
| "I'll add tests before the PR" | You've lost the design forcing function. The interface is already baked in. |
| "This will slow me down" | TDD is faster than: writing code, testing manually, finding the bug, debugging, fixing, re-testing. |

---

## Checklist before marking a task complete

- [ ] Every new function or behavior has a test that was written first
- [ ] Watched each test fail before writing implementation
- [ ] Each failure was the *expected* failure (not a setup error or typo)
- [ ] Wrote the minimum code to pass each test
- [ ] All tests pass, including pre-existing ones
- [ ] Refactored with the suite green throughout
- [ ] No test asserts internal implementation details

Can't check all boxes? Identify which step was skipped and apply it now — add the missing test, verify it fails on the current code, then confirm it passes after your change.
