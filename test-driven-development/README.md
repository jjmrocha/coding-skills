# test-driven-development

A Claude Code skill for strict test-first development. Enforces the
Red→Green→Refactor cycle before any production code is written, ensuring
every behavior is specified by a failing test before it is implemented.

## When to Use

* Implementing any new feature or function
* Fixing a bug (write a reproducing test before applying the fix)
* Adding new behavior to existing code
* Refactoring — characterize current behavior with tests before touching
  anything

**When NOT to use:**

* Writing tests for already-completed code → the design forcing function is
  gone; load `/writing-unit-tests` instead
* Exploratory spikes where the goal is learning, not shipping

## How It Works

The skill enforces three gates, one per cycle phase:

| Phase | What you do | Gate |
|-------|------------|------|
| **RED** | Write one failing test for the next behavior | Confirm it fails for the right reason |
| **GREEN** | Write the minimum code to pass the test | Full suite must be green — no regressions |
| **REFACTOR** | Improve structure without changing behavior — walk six items (duplication, naming, cognitive complexity, single responsibility, side effects, dead code) and report one line each | Checklist reported, then suite green |

Repeat until the feature is complete.

## Usage

```
/test-driven-development
/test-driven-development implement the discount calculator
/test-driven-development fix the race condition in the job queue
```

## Related Skills

* [writing-unit-tests](../writing-unit-tests/) — scenario selection,
  FIRST-U principles, and language-specific test patterns (referenced from
  within this skill)
* [coding-discipline](../coding-discipline/) — scope creep and speculative
  complexity failure modes that apply during the GREEN phase
