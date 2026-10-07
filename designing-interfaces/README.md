# designing-interfaces

A Claude Code skill that makes interface width visible before the
implementation is written. Loaded alongside `coding-discipline` on every
coding turn, and by `analyze-code`'s Quality lens on review.

The core rule: **a zero-line diff is not a zero-cost change.** The cheapest
change to write is usually the one that pushes complexity out to the callers,
where no diff records it.

## When to Use

Adding or changing anything other code will call — a type, function, method,
module, or package — before the implementation exists. Also when a caller needs
data a module doesn't currently expose, which is the moment the shallow design
gets chosen.

## What it asks for

A contract, written before the code for a reader who hasn't seen the session:
what it does, where it lives, its signature with inputs and outputs, and the
caller's code using it. The design is checked against ten interface principles (real work
for the caller, complexity kept inside, single responsibility, minimal inputs,
descriptive names, and others) and gets another pass when it breaks one.

## Why it exists

`coding-discipline` minimizes what you build; this skill constrains what you
expose. They conflict in exactly one place — the shallow design is almost
always the smaller diff — and this skill owns that case.

## Provenance

Written test-first against a measured baseline: four independent agents were
given the same feature in a real Go codebase with the existing skills loaded.
All four shipped the same shallow design, all four passed build, tests, vet,
lint and race, and all four reported the work as done. The rationalization
table is quoted verbatim from what they wrote.

The deep-module vocabulary (depth as leverage at the interface, seams,
adapters, the deletion test) follows John Ousterhout's *A Philosophy of
Software Design* and Michael Feathers' notion of a seam.
