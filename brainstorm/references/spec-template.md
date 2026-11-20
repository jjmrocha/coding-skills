# Spec Template

Use this to structure the spec you present for approval (Steps 5–8). On approval, the spec is saved in the sub-task's section of the feature plan, and implementation starts from it. Scale each section to complexity — a simple project may have 2-3 sentences per section; a complex one may have several paragraphs.

---

```markdown
# [Project/Feature Name] — Design Spec
**Date:** YYYY-MM-DD  
**Status:** Draft | Approved

## Problem Statement
What problem does this solve? Who is affected? Why now?

## Goals
- [Concrete outcome 1]
- [Concrete outcome 2]

## Non-Goals (out of scope)
- [Explicitly excluded item]

## Architecture
High-level description of the system architecture and its components.
Describe integration points and configuration parameters.

## Components

### [Component A]
Purpose and responsibilities. For each interface it exposes, its `designing-interfaces` contract.

### [Component B]
Purpose and responsibilities. For each interface it exposes, its `designing-interfaces` contract.

## Data Flow
How data moves through the system. Include sequence if ordering matters.

## Error Handling
How errors are surfaced and recovered. What the user sees vs. what is logged.

## Testing Approach
The level the tests run at (unit / integration / e2e) and what they fake. The test cases are chosen during implementation with `writing-unit-tests`.

## Open Questions
Any unresolved decisions that need follow-up before implementation.
```

---

## Self-Review Checklist

Before sharing with the user:

- [ ] No TBD, TODO, or placeholder text
- [ ] Architecture section matches the feature descriptions
- [ ] All parameters and configuration options named explicitly
- [ ] Scope is narrow enough for a single sub-task
- [ ] No requirement can be interpreted two ways

## What a Good Spec Avoids

| Anti-pattern | Why it causes problems |
|---|---|
| Listing every possible feature | Scope bloat — use Non-Goals to make exclusions explicit |
| Passive voice ("data will be stored...") | Obscures which component is responsible |
| No error handling section | Developers invent their own, inconsistently |
